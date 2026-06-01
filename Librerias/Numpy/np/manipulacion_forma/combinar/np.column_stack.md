---
title: np.column_stack — Apilar vectores 1D como columnas
aliases:
  - column_stack
  - np.column_stack
tags:
  - numpy
  - api/funcion
  - manipulacion

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

# np.column_stack — Apilar vectores 1D como columnas

## Firma de la función

```python
np.column_stack(tup) -> ndarray
```

## Valor de retorno

Devuelve una matriz 2D donde cada array 1D de entrada se convierte en una **columna**. Resuelve el problema de [[np.hstack]], que con 1D los aplana en lugar de formar columnas.

| Entrada | Shapes | Salida |
|---------|--------|--------|
| tres `(3,)` | 1D | `(3, 3)` |
| `(3,)` y `(3, 2)` | mixto | `(3, 3)` |

```python
import numpy as np
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
np.column_stack((x, y))
# array([[1, 4],
#        [2, 5],
#        [3, 6]])      # (3, 2)
```

## column_stack vs hstack

```python
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
np.hstack((x, y))         # [1, 2, 3, 4, 5, 6]   → (6,)  aplana
np.column_stack((x, y))   # [[1,4],[2,5],[3,6]]  → (3, 2)  columnas
```

## Parámetros en detalle

### `tup` — secuencia de arrays 1D o 2D

Cada 1D de longitud `n` se trata como columna `(n, 1)`. Todos deben tener la misma longitud en el eje 0.

## Casos de uso

### Construir una matriz de diseño a partir de variables

```python
edad = np.array([25, 30, 45])
ingreso = np.array([30000, 45000, 80000])
X = np.column_stack((edad, ingreso))   # (3, 2)
```

### Emparejar coordenadas X, Y

```python
puntos = np.column_stack((xs, ys))     # cada fila es un punto (x, y)
```

## Buenas prácticas

1. Úsalo siempre que tengas **vectores 1D que deben ser columnas**; es más claro que `hstack` + `reshape`.
2. Para apilar como filas, usa [[np.vstack]].
3. Equivale a `np.stack(tup, axis=1)` cuando todas las entradas son 1D del mismo largo.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado 1D inesperado | se usó `hstack` con 1D | usar `column_stack` |
| `dimensions must match` | longitudes distintas | igualar el largo de los vectores |

## Limitaciones

- Pensado para construir columnas; para profundidad usa [[np.dstack]].

## Notas relacionadas

- [[concepto_shape]]
- [[np.hstack]]
- [[np.vstack]]
- [[np.stack]]
