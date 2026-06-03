---
title: scipy.stats.describe — resumen estadistico en una llamada (DescribeResult)
aliases:
  - describe
  - scipy.stats.describe
  - resumen estadistico
tags:
  - scipy
  - api/funcion
  - estadistica
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: DescribeResult
requiere:
  - numpy
draft: false
---

# scipy.stats.describe — resumen estadistico en una llamada (DescribeResult)

Calcula de una sola pasada los **estadisticos descriptivos** mas usados de un array: numero de observaciones, minimo y maximo, media, varianza, asimetria (skewness) y curtosis (kurtosis). Devuelve un objeto-resultado **DescribeResult** (un namedtuple, accesible por atributo). Sustituye a llamar por separado a `len`, `min`, `max`, `mean`, `var`, `skew` y `kurtosis`. Por defecto opera columna a columna (`axis=0`) y usa varianza **muestral** (`ddof=1`), a diferencia de `numpy.var`, que por defecto usa `ddof=0`.

## Firma

```python
scipy.stats.describe(
    a,                       # array_like: datos de entrada
    axis=0,                  # int | None: eje sobre el que reducir (None = aplanar todo)
    ddof=1,                  # int: delta grados de libertad para la varianza (1 = muestral)
    bias=True,               # bool: False -> corrige el sesgo de skewness y kurtosis
    nan_policy='propagate',  # str: 'propagate' | 'raise' | 'omit'
) -> DescribeResult
```

## Valor de retorno

Objeto **DescribeResult** (namedtuple). Acceso por atributo `res.mean` o por posicion `res[2]`; tambien desempaquetable.

| Campo | Tipo | Significado |
|-------|------|-------------|
| `nobs` | `int` / `ndarray` | Numero de observaciones a lo largo del eje |
| `minmax` | `tuple(min, max)` | Par con el minimo y el maximo (cada uno escalar o array) |
| `mean` | `float` / `ndarray` | Media aritmetica |
| `variance` | `float` / `ndarray` | Varianza con los grados de libertad de `ddof` (muestral por defecto) |
| `skewness` | `float` / `ndarray` | Asimetria: 0 simetrica, >0 cola a la derecha, <0 cola a la izquierda |
| `kurtosis` | `float` / `ndarray` | Curtosis **de Fisher** (exceso): 0 = normal, >0 colas pesadas, <0 colas ligeras |

```python
res = describe(datos)
res.mean, res.variance        # acceso por atributo
n, (mn, mx), m, v, s, k = res  # desempaquetado en orden
```

> La curtosis es de **Fisher (exceso)**: la normal da `0`, no `3`. El minmax llega como una **tupla anidada**: `res.minmax[0]` es el minimo, `res.minmax[1]` el maximo.

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Resumen de un vector 1D | `describe(x)` |
| Resumen por columnas de una matriz | `describe(M, axis=0)` |
| Resumen por filas | `describe(M, axis=1)` |
| Tratar toda la matriz como un solo conjunto | `describe(M, axis=None)` |
| Varianza poblacional (no muestral) | `describe(x, ddof=0)` |
| Skewness/kurtosis corregidas por sesgo | `describe(x, bias=False)` |
| Ignorar NaN | `describe(x, nan_policy='omit')` |

## Parametros en detalle

### `a` (obligatorio)

Datos de entrada (`array_like`). Si es multidimensional, el resumen se calcula a lo largo de `axis`.

```python
import numpy as np
from scipy.stats import describe

datos = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
res = describe(datos)
res.nobs       # → 8
res.minmax     # → (2.0, 9.0)
res.mean       # → 5.0
res.variance   # → 4.571...   (ddof=1, muestral)
```

### `axis`

Eje de reduccion. `axis=0` (defecto) resume **cada columna**; `axis=1` cada fila; `axis=None` aplana y resume todo el array.

```python
M = np.array([[1.0, 10.0],
              [2.0, 20.0],
              [3.0, 30.0]])
res = describe(M, axis=0)
res.mean       # → array([ 2., 20.])   (una media por columna)
```

### `ddof`

Grados de libertad de la varianza. `ddof=1` (defecto) da la varianza **muestral** (divide por `n-1`); `ddof=0` la **poblacional** (divide por `n`). Es el punto donde `describe` difiere de `numpy.var`.

### `bias`

Con `bias=True` (defecto) skewness y kurtosis son los estimadores **sesgados** (formulas directas de momentos). Con `bias=False` se aplica la **correccion de sesgo** para muestras pequeñas.

### `nan_policy`

Como tratar los `NaN`: `'propagate'` (defecto) contamina el resultado con `NaN`; `'omit'` los descarta; `'raise'` lanza error si hay alguno.

```python
x = np.array([1.0, 2.0, np.nan, 4.0])
describe(x).mean                    # → nan        ('propagate')
describe(x, nan_policy='omit').mean # → 2.333...   (ignora el NaN)
```

## Casos de uso

### Diagnostico rapido de una muestra experimental

```python
import numpy as np
from scipy.stats import describe

medidas = np.array([9.81, 9.79, 9.83, 9.80, 9.78, 9.82])
r = describe(medidas)
r.mean        # → 9.805
r.variance    # → ~3.5e-4
r.minmax      # → (9.78, 9.83)
```

### Interpretar forma de la distribucion

```python
sesgada = np.array([1, 1, 1, 2, 2, 3, 8, 12])  # cola larga a la derecha
r = describe(sesgada)
r.skewness    # → ~1.1   (>0: asimetria positiva, cola derecha)
r.kurtosis    # → ~0.0..  (cercano a 0: colas tipo normal)
```

Una `skewness` positiva indica cola hacia valores altos; una `kurtosis` (Fisher) positiva indica colas mas pesadas que la normal y mayor presencia de outliers.

### Resumen por variables de un dataset tabular

```python
X = np.random.default_rng(0).normal(size=(100, 3))
r = describe(X, axis=0)
r.mean        # → array de 3 medias, una por variable
r.variance    # → array de 3 varianzas
```

## Buenas practicas

1. Accede por atributo (`res.mean`, `res.skewness`) por legibilidad; el orden posicional solo si desempaquetas.
2. Recuerda que la varianza es **muestral** por defecto (`ddof=1`); usa `ddof=0` para igualar el comportamiento de `numpy.var`.
3. Interpreta `kurtosis` como **exceso de Fisher**: compara contra `0`, no contra `3`.
4. Define `axis` explicitamente al trabajar con matrices para no confundir filas con columnas.
5. Usa `nan_policy='omit'` si la muestra puede contener huecos en vez de limpiarla a mano.
6. Para correlacion o regresion entre dos variables, este resumen univariante no basta: ahi entran funciones como las de correlacion.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar `3.0` de curtosis en datos normales | `kurtosis` es de Fisher (exceso) | Comparar contra `0`; sumar 3 si se quiere Pearson |
| Varianza no coincide con `np.var` | `describe` usa `ddof=1`, `np.var` usa `ddof=0` | Igualar `ddof` en una de las dos |
| `res.minmax` tratado como escalar | Es una **tupla** `(min, max)` | Indexar: `res.minmax[0]`, `res.minmax[1]` |
| Resultado lleno de `NaN` | `nan_policy='propagate'` con huecos | Usar `nan_policy='omit'` |
| Resumen sobre el eje equivocado | `axis=0` por defecto reduce columnas | Fijar `axis` segun la orientacion de los datos |

## Limitaciones

- Resume **una variable por columna**; no mide relacion entre variables (correlacion/regresion).
- No devuelve mediana ni percentiles; para esos usar `numpy.median` / `numpy.percentile`.
- Skewness y kurtosis son poco fiables con muestras muy pequeñas; valorar `bias=False`.
- Sensible a outliers: media y varianza se ven arrastradas por valores extremos.

## Notas relacionadas

- [[scipy.stats.pearsonr]]
- [[scipy.stats.spearmanr]]
- [[scipy.stats.linregress]]
