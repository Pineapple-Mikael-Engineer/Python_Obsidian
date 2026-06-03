---
title: np.cov — Matriz de covarianza
aliases:
  - cov
  - np.cov
  - covarianza
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.cov — Matriz de covarianza

## Firma de la función

```python
np.cov(
    m,
    y=None,
    rowvar=True,
    bias=False,
    ddof=None,
    fweights=None,
    aweights=None
) -> ndarray
```

## Valor de retorno

Devuelve la **matriz de covarianza** entre variables. El elemento `[i, j]` es la covarianza entre la variable `i` y la `j`; la diagonal son las varianzas.

```python
import numpy as np
X = np.array([[1, 2, 3, 4],
              [2, 4, 6, 8]])   # 2 variables, 4 observaciones
np.cov(X)
# [[1.667, 3.333],
#  [3.333, 6.667]]
```

## ⚠️ El parámetro `rowvar`

| `rowvar` | Interpretación de las filas |
|----------|------------------------------|
| `True` (por defecto) | cada **fila** es una variable |
| `False` | cada **columna** es una variable (filas = observaciones) |

Con datos en formato `(n_muestras, n_features)` (lo habitual en ML), usa `rowvar=False`:

```python
datos = np.random.rand(100, 3)   # 100 muestras, 3 features
np.cov(datos, rowvar=False)      # matriz 3×3
```

## Parámetros en detalle

### `m`, `y` — datos

`m` es la matriz de variables; `y` opcional añade más variables.

### `ddof` / `bias` — normalización

`ddof=1` (por defecto, divisor `N-1`, insesgada) o `ddof=0`/`bias=True` (divisor `N`).

## Casos de uso

### Covarianza entre dos series

```python
np.cov(x, y)[0, 1]   # covarianza cruzada
```

## Buenas prácticas

1. Define `rowvar=False` si tus datos son `(muestras, features)`.
2. Para correlación normalizada (−1 a 1), usa [[np.corrcoef]].
3. La diagonal coincide con [[np.var]] (con el mismo `ddof`).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Matriz del tamaño equivocado | `rowvar` mal puesto | usar `rowvar=False` para `(n, features)` |

## Limitaciones

- Sensible a la escala de las variables (de ahí [[np.corrcoef]]).

## Notas relacionadas

- [[concepto_shape]]
- [[np.corrcoef]]
- [[np.var]]
