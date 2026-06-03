---
title: scipy.stats.ttest_rel — t-test de muestras pareadas o relacionadas
aliases:
  - ttest_rel
  - scipy.stats.ttest_rel
  - t-test pareado
  - test de medidas repetidas
tags:
  - scipy
  - api/funcion
  - tests
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: TtestResult (statistic, pvalue)
requiere:
  - numpy
draft: false
---

# scipy.stats.ttest_rel — t-test de muestras pareadas o relacionadas

Contrasta si **dos medidas emparejadas** del mismo sujeto (tipicamente antes/despues) difieren en media. Trabaja sobre las **diferencias** `d = a - b` de cada par y comprueba si su media es cero. Requiere que `a` y `b` tengan **igual longitud** y esten **alineados par a par**. Devuelve un **objeto-resultado** con `.statistic` y `.pvalue`, desempaquetable como tupla.

> Pareado vs independiente: `ttest_rel` exige una correspondencia uno-a-uno entre observaciones (el sujeto i de `a` es el mismo que el sujeto i de `b`). Si los grupos son de sujetos distintos sin emparejar, el test correcto es `ttest_ind`.

Al modelar las diferencias intra-sujeto, el test pareado elimina la variabilidad entre sujetos y suele tener **mas potencia** que el independiente cuando el emparejamiento es real.

## Firma

```python
scipy.stats.ttest_rel(
    a,                       # array_like: primera medida (p. ej. antes)
    b,                       # array_like: segunda medida (p. ej. despues), MISMA longitud
    axis=0,                  # int | None: eje del calculo
    nan_policy='propagate',  # str: 'propagate' | 'raise' | 'omit'
    alternative='two-sided', # str: 'two-sided' | 'less' | 'greater'
) -> TtestResult
```

## Valor de retorno

Objeto-resultado (`TtestResult`, tipo Bunch) con acceso por atributo y desempaquetable como tupla.

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `statistic` | `float` / `ndarray` | Estadistico t sobre las diferencias |
| `pvalue` | `float` / `ndarray` | p-valor del contraste |
| `df` | `float` | Grados de libertad (`n_pares - 1`) |

```python
t, p = ttest_rel(antes, despues)   # desempaquetado como tupla
res = ttest_rel(antes, despues)    # o como objeto
res.statistic, res.pvalue
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Test pareado estandar | `ttest_rel(antes, despues)` |
| H1: antes > despues (mejora) | `ttest_rel(antes, despues, alternative='greater')` |
| H1: antes < despues | `ttest_rel(antes, despues, alternative='less')` |
| Ignorando NaN por par | `ttest_rel(antes, despues, nan_policy='omit')` |

## Parametros en detalle

### `a`, `b` (obligatorios)

Las dos medidas emparejadas. **Deben tener la misma longitud** y estar ordenadas de modo que la posicion `i` de ambas corresponda al mismo sujeto. El test opera sobre `a - b`.

```python
import numpy as np
from scipy.stats import ttest_rel

antes   = np.array([120, 135, 128, 142, 119])   # presion antes
despues = np.array([115, 130, 125, 138, 117])   # misma persona despues
t, p = ttest_rel(antes, despues)
t    # → positivo: en promedio antes > despues
p    # → p pequeño -> el tratamiento cambio la media
```

Si las longitudes difieren se lanza `ValueError`: el emparejamiento es obligatorio.

### `alternative`

Sobre la media de las diferencias `d = a - b`:

- `'two-sided'` (defecto): la diferencia media es distinta de cero.
- `'greater'`: la diferencia media es mayor que cero (`mean(a) > mean(b)`).
- `'less'`: la diferencia media es menor que cero (`mean(a) < mean(b)`).

### `nan_policy`

`'omit'` descarta los **pares** con algun NaN; `'propagate'` devuelve NaN; `'raise'` lanza error.

## Casos de uso

### Efecto de una intervencion (antes/despues)

```python
import numpy as np
from scipy.stats import ttest_rel

rng = np.random.default_rng(0)
antes   = rng.normal(70, 8, size=30)
despues = antes - rng.normal(3, 2, size=30)   # baja unos puntos por sujeto
res = ttest_rel(antes, despues)
res.pvalue    # p pequeño -> hay cambio sistematico
```

### Comparacion de dos metodos sobre los mismos items

```python
# Dos instrumentos miden las mismas 25 muestras
t, p = ttest_rel(metodo_A, metodo_B)
```

## Interpretacion del p-valor

- **H0**: la **diferencia media de los pares es cero** (`mean(a - b) = 0`); las dos condiciones no difieren en promedio.
- **H1**: la diferencia media no es cero (o `>` / `<` segun `alternative`).
- Se fija `alfa` (p. ej. 0.05) **antes** de ver los datos.
- Si `pvalue < alfa` → se **rechaza H0**: hay evidencia de que la media cambio entre las dos medidas.
- Si `pvalue >= alfa` → **no se rechaza H0**: no hay evidencia de cambio.

```python
alfa = 0.05
t, p = ttest_rel(antes, despues)
if p < alfa:
    print("Se rechaza H0: la media cambio entre condiciones")
else:
    print("No se rechaza H0")
```

## Buenas practicas

1. Asegura el **alineamiento par a par**: el elemento `i` de `a` y `b` debe ser el mismo sujeto/item.
2. Usa el pareado cuando exista emparejamiento real: aprovecha la correlacion intra-sujeto y gana potencia.
3. Verifica normalidad de las **diferencias** `a - b`, no de `a` y `b` por separado.
4. Con NaN dispersos usa `nan_policy='omit'` para descartar solo los pares afectados.
5. Si las muestras son de sujetos distintos sin emparejar, cambia al test independiente; ver [[scipy.stats.ttest_ind]].

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError` por longitudes distintas | `a` y `b` no emparejados | Igualar longitudes y alinear pares |
| Usar pareado con grupos independientes | Sujetos distintos en `a` y `b` | Usar `ttest_ind` |
| Comprobar normalidad de `a` y `b` sueltos | El supuesto es sobre `a - b` | Testear las diferencias |
| Desordenar uno de los arrays | Se rompe la correspondencia de pares | Mantener el mismo orden en ambos |
| `pvalue` NaN | Hay NaN en algun par | `nan_policy='omit'` |

## Limitaciones

- Solo dos condiciones emparejadas; para mas de dos medidas repetidas se usa ANOVA de medidas repetidas (fuera de esta funcion).
- Asume diferencias aproximadamente normales; con n pequeño y diferencias muy no-normales considerar el test de Wilcoxon de signos `wilcoxon`.
- Sensible a outliers en las diferencias.
- Exige emparejamiento valido: un alineamiento incorrecto invalida el resultado silenciosamente.

## Notas relacionadas

- [[scipy.stats.ttest_ind]]
- [[scipy.stats.shapiro]]
- [[OptimizeResult]]
