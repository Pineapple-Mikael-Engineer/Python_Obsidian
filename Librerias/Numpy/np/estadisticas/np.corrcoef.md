---
title: np.corrcoef — Matriz de correlación de Pearson
aliases:
  - corrcoef
  - np.corrcoef
  - correlacion
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

# np.corrcoef — Matriz de correlación de Pearson

## Firma de la función

```python
np.corrcoef(
    x,
    y=None,
    rowvar=True,
    *,
    dtype=None
) -> ndarray
```

## Valor de retorno

Devuelve la **matriz de correlación de Pearson**: la [[np.cov|covarianza]] normalizada a `[-1, 1]`. El elemento `[i, j]` mide la relación lineal entre las variables `i` y `j`; la diagonal es siempre `1`.

| Valor | Relación lineal |
|-------|-----------------|
| `+1` | perfecta positiva |
| `0` | sin correlación lineal |
| `-1` | perfecta negativa |

```python
import numpy as np
x = np.array([1, 2, 3, 4])
y = np.array([2, 4, 6, 8])     # = 2x
np.corrcoef(x, y)
# [[1., 1.],
#  [1., 1.]]   → correlación perfecta
```

## Parámetros en detalle

### `x`, `y` — datos

`x` matriz de variables; `y` opcional añade otra variable.

### `rowvar` — orientación

Igual que en [[np.cov]]: `True` (filas = variables) por defecto; usa `False` para datos `(muestras, features)`.

## Casos de uso

### Correlación entre features

```python
datos = np.random.rand(100, 4)
np.corrcoef(datos, rowvar=False)   # matriz 4×4
```

### Correlación entre dos series

```python
r = np.corrcoef(serie_a, serie_b)[0, 1]
```

## Buenas prácticas

1. Más interpretable que la covarianza (escala fija −1..1).
2. Solo mide relación **lineal**: correlación 0 no implica independencia.
3. Define `rowvar=False` con datos `(muestras, features)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Correlación 0 con relación clara | la relación no es lineal | inspeccionar con gráfico |
| Matriz mal dimensionada | `rowvar` incorrecto | usar `rowvar=False` |
| `nan` | varianza 0 (variable constante) | revisar datos |

## Limitaciones

- Solo capta relaciones **lineales**.
- Variables constantes → división por 0 → NaN.

## Notas relacionadas

- [[concepto_shape]]
- [[np.cov]]
- [[np.std]]
