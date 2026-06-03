---
title: scipy.stats.kstest — test de Kolmogorov-Smirnov de ajuste
aliases:
  - kstest
  - scipy.stats.kstest
  - Kolmogorov-Smirnov
  - test KS
tags:
  - scipy
  - api/funcion
  - tests
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: KstestResult (statistic, pvalue)
requiere:
  - numpy
draft: false
---

# scipy.stats.kstest — test de Kolmogorov-Smirnov de ajuste

Compara una **muestra** con una **distribucion de referencia** (modo de una muestra) o **dos muestras entre si** (si el segundo argumento es tambien un array). Se basa en la **maxima distancia vertical** entre la funcion de distribucion empirica de los datos y la CDF de referencia (o entre las dos empiricas). Devuelve un **objeto-resultado** con `.statistic` (el estadistico D, esa maxima distancia) y `.pvalue`, desempaquetable como tupla.

> A diferencia de `shapiro` (solo normalidad), `kstest` admite **cualquier** distribucion de referencia: se pasa su nombre (`'norm'`, `'expon'`, `'uniform'`, ...) o un callable de la CDF.

## Firma

```python
scipy.stats.kstest(
    rvs,                     # array_like | str | callable: la muestra (o generador)
    cdf,                     # str | callable | array_like: CDF de referencia o 2a muestra
    args=(),                 # tuple: parametros de la distribucion de referencia
    N=20,                    # int: tamaño si rvs es un nombre de distribucion
    alternative='two-sided', # str: 'two-sided' | 'less' | 'greater'
    method='auto',           # str: metodo de calculo del p-valor
) -> KstestResult
```

## Valor de retorno

Objeto-resultado (`KstestResult`, tipo Bunch) con acceso por atributo y desempaquetable como tupla.

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `statistic` | `float` | Estadistico D: maxima distancia entre las CDF |
| `pvalue` | `float` | p-valor del contraste |

```python
D, p = kstest(datos, 'norm')   # desempaquetado como tupla
res = kstest(datos, 'norm')    # o como objeto
res.statistic, res.pvalue
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Ajuste a normal estandar | `kstest(datos, 'norm')` |
| Ajuste a normal con parametros | `kstest(datos, 'norm', args=(mu, sigma))` |
| Ajuste a exponencial | `kstest(datos, 'expon')` |
| Con CDF callable | `kstest(datos, mi_cdf)` |
| Dos muestras | `kstest(muestra1, muestra2)` |
| Unilateral | `kstest(datos, 'norm', alternative='greater')` |

## Parametros en detalle

### `rvs` (obligatorio)

Normalmente el **array de la muestra** a contrastar. Tambien admite el nombre de una distribucion o un callable generador (para simulacion), pero el uso habitual es pasar los datos observados.

### `cdf` (obligatorio)

La referencia con la que se compara. Tres formas:

- **Nombre** de una distribucion de `scipy.stats` como cadena: `'norm'`, `'expon'`, `'uniform'`, etc.
- **Callable** que evalua la CDF de referencia.
- **Otra muestra** (array): activa el **test de dos muestras**, que compara si ambas vienen de la misma distribucion.

```python
import numpy as np
from scipy.stats import kstest

rng = np.random.default_rng(0)
datos = rng.normal(0, 1, size=200)

# Una muestra vs normal estandar:
D, p = kstest(datos, 'norm')
D    # → distancia pequeña
p    # → p alto -> compatible con normal estandar
```

### `args`

Tupla con los **parametros** de la distribucion de referencia (p. ej. `loc` y `scale`). Si se omiten, se usan los valores por defecto de la distribucion (`'norm'` -> media 0, desviacion 1).

```python
# Comparar contra una normal de media 5 y desviacion 2:
D, p = kstest(datos, 'norm', args=(5, 2))
```

> **Aviso critico**: si los parametros de `cdf` se **estiman a partir de los mismos datos** (p. ej. usar `datos.mean()` y `datos.std()` como `args`), el p-valor de `kstest` **deja de ser valido** (es conservador, tiende a no rechazar). Para normalidad con parametros estimados usa `shapiro` o el test de Lilliefors.

### `alternative`

`'two-sided'` (defecto) detecta cualquier desviacion; `'less'`/`'greater'` contrastan que la CDF empirica este por debajo/encima de la de referencia.

### Dos muestras

```python
a = rng.normal(0, 1, size=150)
b = rng.normal(0.5, 1, size=180)
D, p = kstest(a, b)      # H0: a y b vienen de la misma distribucion
p    # → p bajo si difieren en localizacion/forma
```

## Casos de uso

### Comprobar ajuste a una distribucion teorica

```python
import numpy as np
from scipy.stats import kstest

muestra = np.random.default_rng(1).exponential(scale=2.0, size=300)
D, p = kstest(muestra, 'expon', args=(0, 2.0))   # loc=0, scale=2
p    # p alto -> datos compatibles con esa exponencial
```

### Comparar dos grupos sin asumir distribucion

```python
res = kstest(grupo_A, grupo_B)
res.pvalue    # p bajo -> las dos muestras difieren en distribucion
```

## Interpretacion del p-valor

- **H0**: la muestra **sigue la distribucion dada** (modo una muestra) o **ambas muestras provienen de la misma distribucion** (modo dos muestras).
- **H1**: la muestra no sigue esa distribucion (o las dos muestras difieren).
- Se fija `alfa` (p. ej. 0.05) **antes** de ver los datos.
- Si `pvalue < alfa` → se **rechaza H0**: la muestra **no** se ajusta a la referencia (o las muestras difieren).
- Si `pvalue >= alfa` → **no se rechaza H0**: los datos son compatibles con la distribucion de referencia.

```python
alfa = 0.05
D, p = kstest(datos, 'norm')
if p < alfa:
    print("Se rechaza H0: la muestra no sigue la distribucion de referencia")
else:
    print("No se rechaza H0: compatible con la referencia")
```

## Buenas practicas

1. **No estimes los parametros de la referencia desde los mismos datos**: invalida el p-valor. Usa parametros conocidos a priori o un test apropiado (`shapiro`, Lilliefors).
2. Especifica los parametros con `args` cuando la distribucion tenga `loc`/`scale` no triviales.
3. Para contrastar solo normalidad en muestras pequeñas-medianas, `shapiro` suele ser mas potente; ver [[scipy.stats.shapiro]].
4. KS es mas sensible a diferencias en el **centro** de la distribucion que en las colas; tenlo en cuenta si las colas importan.
5. Para comparar dos grupos sin asumir forma, usa el modo de dos muestras pasando un array como `cdf`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Estimar `args` desde los datos | p-valor deja de ser valido | Parametros a priori o usar `shapiro` |
| Olvidar `args` con loc/scale no triviales | Compara contra la referencia estandar equivocada | Pasar `args=(loc, scale)` |
| Esperar que detecte bien las colas | KS es debil en colas | Usar `anderson` si las colas importan |
| Confundir D con el p-valor | `statistic` es la distancia, no la probabilidad | Decidir con `.pvalue` |
| Pasar conteos como si fueran la CDF | `cdf` es nombre, callable o muestra | Revisar el tipo del 2o argumento |

## Limitaciones

- Con parametros estimados de los datos, el p-valor es **invalido** (conservador).
- Mas sensible al centro que a las colas de la distribucion.
- Pensado para distribuciones **continuas**; con datos discretos o muchos empates pierde precision.
- En el modo una muestra requiere especificar bien la distribucion de referencia y sus parametros.

## Notas relacionadas

- [[scipy.stats.shapiro]]
- [[scipy.stats.chisquare]]
- [[OptimizeResult]]
