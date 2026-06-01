---
title: np.hstack — Apilar arrays horizontalmente (por columnas)
aliases:
  - hstack
  - np.hstack
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

# np.hstack — Apilar arrays horizontalmente (por columnas)

## Firma de la función

```python
np.hstack(tup) -> ndarray
```

## Valor de retorno

Devuelve un nuevo array uniendo la secuencia **horizontalmente**: en el eje 1 para arrays 2D, y en el eje 0 para arrays 1D. Es un atajo de [[np.concatenate]].

| Entrada | Shapes | Salida |
|---------|--------|--------|
| dos `(3,)` | 1D | `(6,)` |
| `(2, 3)` y `(2, 2)` | 2D | `(2, 5)` |

```python
import numpy as np
a = np.array([[1], [2], [3]])
b = np.array([[4], [5], [6]])
np.hstack((a, b))
# array([[1, 4],
#        [2, 5],
#        [3, 6]])      # (3, 2)
```

## El caso 1D (cuidado)

Con arrays 1D, `hstack` concatena en el **eje 0**, no crea columnas:

```python
np.hstack((np.array([1, 2]), np.array([3, 4])))   # [1, 2, 3, 4]  → (4,)
```

Para tratar vectores 1D como columnas, usa [[np.column_stack]].

## Parámetros en detalle

### `tup` — secuencia de arrays

Tupla o lista. En 2D deben coincidir en el número de **filas** (eje 0).

## Casos de uso

### Añadir columnas a una matriz de diseño

```python
X = np.ones((100, 3))
extra = np.random.rand(100, 2)
X = np.hstack((X, extra))      # (100, 5)
```

### Concatenar tramos de una señal 1D

```python
señal = np.hstack((tramo1, tramo2, tramo3))
```

## Buenas prácticas

1. Úsalo para crecer "a lo ancho" (más columnas) en 2D; para más filas, [[np.vstack]].
2. Con vectores 1D que deban ser columnas, usa [[np.column_stack]] (evita el aplanado).
3. Acumula en lista y une una vez para no copiar en cada paso.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Vectores 1D se aplanan en vez de formar columnas | `hstack` une 1D en eje 0 | usar [[np.column_stack]] |
| `dimensions must match` | nº de filas distinto en 2D | igualar el eje 0 |

## Limitaciones

- El eje de unión depende de `ndim` (0 en 1D, 1 en 2D+): para control explícito usa [[np.concatenate]].

## Notas relacionadas

- [[concepto_shape]]
- [[np.concatenate]]
- [[np.vstack]]
- [[np.column_stack]]
