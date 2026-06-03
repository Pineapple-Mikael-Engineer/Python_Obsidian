---
title: scipy.stats.spearmanr — correlacion de rangos de Spearman (rho) y p-valor
aliases:
  - spearmanr
  - scipy.stats.spearmanr
  - correlacion de Spearman
tags:
  - scipy
  - api/funcion
  - estadistica
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: SignificanceResult
requiere:
  - numpy
draft: false
---

# scipy.stats.spearmanr — correlacion de rangos de Spearman (rho) y p-valor

Calcula la **correlacion de rangos de Spearman** `rho ∈ [-1, 1]` entre dos variables, junto con un **p-valor** (H0: no hay correlacion). Es la correlacion de Pearson aplicada **sobre los rangos** de los datos en lugar de sobre sus valores: por eso mide la fuerza de una relacion **monotona** (cuando una variable crece, la otra crece o decrece de forma consistente) **sin exigir que sea lineal**. Es **no parametrica** (no asume normalidad) y **robusta a outliers**, ya que el rango de un valor extremo es solo "el mayor", no su magnitud. Devuelve un objeto con `statistic` (rho) y `pvalue`. A diferencia de Pearson, puede operar sobre **matrices** y devolver una **matriz de correlaciones**.

> Regla practica: usa Spearman cuando la relacion sea monotona pero quizas no lineal, cuando haya outliers, o cuando los datos sean ordinales. Usa Pearson cuando busques especificamente linealidad y los datos sean aproximadamente normales.

## Firma

```python
scipy.stats.spearmanr(
    a,                       # array_like: 1D, o 2D (variables en columnas por defecto)
    b=None,                  # array_like 1D opcional: segunda variable
    axis=0,                  # int | None: 0 = variables en columnas, 1 = en filas
    nan_policy='propagate',  # str: 'propagate' | 'raise' | 'omit'
    alternative='two-sided', # str: 'two-sided' | 'greater' | 'less'
) -> SignificanceResult
```

## Valor de retorno

Objeto **SignificanceResult**. Acceso por atributo o desempaquetado `(rho, p)`.

| Campo | Tipo | Significado |
|-------|------|-------------|
| `statistic` | `float` / `ndarray` | Coeficiente rho `∈ [-1, 1]`; **matriz** si la entrada tiene >2 variables |
| `pvalue` | `float` / `ndarray` | p-valor (H0: no correlacion); misma forma que `statistic` |

```python
res = spearmanr(a, b)
res.statistic, res.pvalue        # acceso por atributo
rho, p = spearmanr(a, b)         # desempaquetado (rho, p)
```

> Con dos vectores `statistic` es un escalar. Con una matriz de `k>2` columnas, `statistic` es una **matriz k×k** de correlaciones por pares (y `pvalue` su matriz de p-valores).

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Correlacion entre dos vectores | `rho, p = spearmanr(x, y)` |
| Objeto completo | `res = spearmanr(x, y)` |
| Matriz de correlaciones (columnas = variables) | `spearmanr(M)` |
| Variables en filas | `spearmanr(M, axis=1)` |
| Ignorar NaN | `spearmanr(x, y, nan_policy='omit')` |
| Contraste unilateral | `spearmanr(x, y, alternative='greater')` |

## Parametros en detalle

### `a`, `b`

`a` puede ser **un vector 1D** (entonces `b` es el otro vector) o **una matriz 2D** (entonces se ignora `b` y se correlacionan todas las variables entre si). `b` es la segunda variable cuando `a` es 1D.

```python
import numpy as np
from scipy.stats import spearmanr

x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 4, 9, 16, 25])      # relacion monotona NO lineal (cuadratica creciente)
rho, p = spearmanr(x, y)
rho  # → 1.0   (perfecta monotona: Spearman la capta entera)
```

Compara: Pearson sobre estos mismos datos daria `r < 1` porque la relacion no es lineal.

### `axis`

Con una matriz, `axis=0` (defecto) trata **cada columna** como una variable; `axis=1` cada fila. `axis=None` aplana todo.

```python
M = np.array([[1, 10, 100],
              [2, 25, 80],
              [3, 32, 60],
              [4, 47, 30]])
res = spearmanr(M)            # columnas = 3 variables
res.statistic.shape          # → (3, 3)   (matriz de correlaciones)
```

### `nan_policy`

`'propagate'` (defecto) devuelve `NaN` si hay huecos; `'omit'` los descarta antes de rangear; `'raise'` lanza error.

### `alternative`

Direccion del contraste del p-valor: `'two-sided'`, `'greater'` (rho>0) o `'less'` (rho<0). No altera el valor de rho.

## Casos de uso

### Relacion monotona pero no lineal

```python
import numpy as np
from scipy.stats import spearmanr, pearsonr

dosis = np.array([1, 2, 3, 4, 5, 6])
efecto = np.array([2, 5, 9, 20, 45, 110])   # crece de forma acelerada
spearmanr(dosis, efecto).statistic           # → 1.0   (monotona perfecta)
pearsonr(dosis, efecto).statistic            # → ~0.9  (menor: no es lineal)
```

### Robustez ante un outlier

```python
x = np.array([1, 2, 3, 4, 5])
y = np.array([1, 2, 3, 4, 500])              # ultimo punto es outlier
spearmanr(x, y).statistic                    # → 1.0   (los rangos no cambian)
pearsonr(x, y).statistic                     # arrastrado por el valor extremo
```

### Matriz de correlaciones entre variables de un dataset

```python
datos = np.random.default_rng(0).normal(size=(50, 4))
res = spearmanr(datos)
res.statistic        # matriz 4x4 de rho por pares
res.pvalue           # matriz 4x4 de p-valores
```

## Buenas practicas

1. Prefiere Spearman cuando la relacion sea **monotona pero no necesariamente lineal**, o cuando los datos sean ordinales.
2. Usala como alternativa robusta cuando sospeches **outliers** que distorsionarian a Pearson.
3. Al pasar una matriz, fija `axis` segun esten las variables en columnas o filas.
4. Con datos faltantes usa `nan_policy='omit'` para no contaminar toda la matriz con `NaN`.
5. Reporta `rho` junto a su `pvalue`; un rho alto con `n` pequeño puede no ser significativo.
6. Recuerda que mide **monotonia**, no la forma exacta de la relacion: no sustituye a un ajuste.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar que mida linealidad | Spearman mide **monotonia** sobre rangos | Usar `pearsonr` para linealidad |
| Sorprenderse de recibir una matriz | Entrada con >2 variables devuelve matriz | Indexar la celda deseada de `res.statistic` |
| Matriz llena de `NaN` | `nan_policy='propagate'` con huecos | Usar `nan_policy='omit'` |
| Confundir el eje de variables | `axis=0` trata columnas como variables | Ajustar `axis` a la orientacion real |
| Tratar el retorno solo como tupla | Es un objeto (tambien desempaquetable) | `rho, p = spearmanr(...)` o `res.statistic` |
| Interpretar rho como pendiente | rho no cuantifica la magnitud del cambio | Para pendiente usar regresion lineal |

## Limitaciones

- Mide **monotonia**, no linealidad ni la forma concreta de la relacion.
- No da pendiente ni permite predecir valores: para eso se usa una regresion.
- Con muchos empates (valores repetidos) el calculo de rangos pierde precision.
- El p-valor de muestras muy pequeñas es poco fiable; valorar contrastes exactos.
- rho cercano a 0 no implica independencia: relaciones **no monotonas** (p. ej. en forma de U) pueden anularlo.

## Notas relacionadas

- [[scipy.stats.pearsonr]]
- [[scipy.stats.linregress]]
- [[scipy.stats.describe]]
