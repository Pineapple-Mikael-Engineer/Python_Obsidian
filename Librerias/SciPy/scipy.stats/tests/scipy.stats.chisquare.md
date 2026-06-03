---
title: scipy.stats.chisquare — test chi-cuadrado de bondad de ajuste
aliases:
  - chisquare
  - scipy.stats.chisquare
  - chi-cuadrado bondad de ajuste
  - goodness of fit
tags:
  - scipy
  - api/funcion
  - tests
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: Power_divergenceResult (statistic, pvalue)
requiere:
  - numpy
draft: false
---

# scipy.stats.chisquare — test chi-cuadrado de bondad de ajuste

Contrasta si un conjunto de **frecuencias observadas** sobre categorias se ajusta a una **distribucion esperada**. Trabaja con **conteos** (frecuencias absolutas), no con proporciones. Compara `f_obs` contra `f_exp` (por defecto, una distribucion **uniforme** que reparte el total entre todas las categorias). Devuelve un **objeto-resultado** con `.statistic` (el estadistico chi-cuadrado) y `.pvalue`, desempaquetable como tupla.

> Es bondad de ajuste de **una** clasificacion. Para comprobar **independencia entre dos variables categoricas** (tabla de contingencia) se usa `chi2_contingency`, no esta funcion.

El estadistico es la suma de `(observado - esperado)^2 / esperado` sobre las categorias; cuanto mayor, peor el ajuste.

## Firma

```python
scipy.stats.chisquare(
    f_obs,        # array_like: frecuencias OBSERVADAS (conteos, no proporciones)
    f_exp=None,   # array_like | None: frecuencias esperadas; None -> uniforme
    ddof=0,       # int: ajuste a los grados de libertad (k - 1 - ddof)
    axis=0,       # int | None: eje sobre el que se aplica el test
) -> Power_divergenceResult
```

## Valor de retorno

Objeto-resultado (`Power_divergenceResult`, tipo Bunch) con acceso por atributo y desempaquetable como tupla.

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `statistic` | `float` / `ndarray` | Estadistico chi-cuadrado observado |
| `pvalue` | `float` / `ndarray` | p-valor del contraste |

```python
chi2, p = chisquare(f_obs)         # desempaquetado como tupla
res = chisquare(f_obs)             # o como objeto
res.statistic, res.pvalue
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Ajuste a uniforme | `chisquare(f_obs)` |
| Ajuste a esperadas explicitas | `chisquare(f_obs, f_exp=esperadas)` |
| Con parametros estimados (corregir gl) | `chisquare(f_obs, f_exp, ddof=k_estimados)` |

## Parametros en detalle

### `f_obs` (obligatorio)

Vector de **frecuencias observadas** por categoria: cuantas veces aparece cada clase. Deben ser **conteos**, no porcentajes ni proporciones. La suma es el tamaño muestral.

```python
import numpy as np
from scipy.stats import chisquare

# Tirar un dado 60 veces; conteo por cara:
observado = np.array([8, 9, 12, 11, 10, 10])
chi2, p = chisquare(observado)   # f_exp uniforme = 10 por cara
chi2   # → ~1.0
p      # → ~0.96  (p alto -> compatible con dado justo)
```

### `f_exp`

Frecuencias **esperadas** bajo H0. Si es `None`, se asume **uniforme**: el total repartido por igual entre las categorias. Si se da, **debe sumar lo mismo que** `f_obs` (mismo total), o el resultado carece de sentido.

```python
# Modelo no uniforme: se esperan ciertas proporciones
total = observado.sum()
esperado = total * np.array([0.1, 0.2, 0.2, 0.2, 0.2, 0.1])
chi2, p = chisquare(observado, f_exp=esperado)
```

### `ddof`

Ajusta los grados de libertad: por defecto `gl = k - 1` (con `k` categorias). Si los parametros de la distribucion esperada se **estimaron a partir de los mismos datos**, hay que restar uno por cada parametro estimado pasando `ddof = numero_de_parametros`. Internamente `gl = k - 1 - ddof`.

## Casos de uso

### Comprobar un dado justo

```python
import numpy as np
from scipy.stats import chisquare

observado = np.array([18, 22, 16, 14, 12, 18])   # 100 tiradas
chi2, p = chisquare(observado)
p    # p alto -> no hay evidencia de sesgo
```

### Ajuste a una distribucion teorica

```python
# Conteos de un experimento vs frecuencias predichas por un modelo
res = chisquare(conteos, f_exp=predichas)
res.pvalue    # p bajo -> los datos NO siguen el modelo propuesto
```

## Interpretacion del p-valor

- **H0**: las frecuencias observadas **siguen la distribucion esperada** (`f_obs` proviene de la poblacion descrita por `f_exp`).
- **H1**: las frecuencias observadas difieren de las esperadas.
- Se fija `alfa` (p. ej. 0.05) **antes** de ver los datos.
- Si `pvalue < alfa` → se **rechaza H0**: los datos **no** se ajustan a la distribucion esperada.
- Si `pvalue >= alfa` → **no se rechaza H0**: los datos son compatibles con la distribucion esperada.

```python
alfa = 0.05
chi2, p = chisquare(observado)
if p < alfa:
    print("Se rechaza H0: el ajuste a la distribucion esperada falla")
else:
    print("No se rechaza H0: datos compatibles con lo esperado")
```

## Buenas practicas

1. Pasa **conteos**, nunca proporciones: si tienes porcentajes, multiplicalos por el total primero.
2. Asegura que `f_exp` **sume el mismo total** que `f_obs`.
3. Procura **frecuencias esperadas >= 5** en cada categoria; con esperadas pequeñas la aproximacion chi-cuadrado es poco fiable (agrupar categorias o usar un test exacto).
4. Si estimaste parametros del modelo desde los datos, corrige con `ddof`.
5. Para independencia entre dos variables categoricas usa `chi2_contingency` en lugar de esta funcion.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar proporciones | El test espera conteos | Multiplicar por el total muestral |
| `f_exp` no suma igual que `f_obs` | Totales distintos | Reescalar `f_exp` al total de `f_obs` |
| Esperadas < 5 | Aproximacion invalida | Agrupar categorias o test exacto |
| Olvidar `ddof` con parametros estimados | gl mal calculados, p-valor sesgado | `ddof = nº parametros estimados` |
| Usarlo para tabla de contingencia | Es bondad de ajuste, no independencia | Usar `chi2_contingency` |

## Limitaciones

- Aproximacion asintotica: poco fiable con frecuencias esperadas bajas (regla del 5).
- Solo categorias mutuamente excluyentes con conteos no negativos.
- No mide independencia entre variables (eso es `chi2_contingency`).
- Sensible al numero de categorias y a como se agrupan los datos continuos en bins.

## Notas relacionadas

- [[scipy.stats.kstest]]
- [[scipy.stats.shapiro]]
- [[OptimizeResult]]
