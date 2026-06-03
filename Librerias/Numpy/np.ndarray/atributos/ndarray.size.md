---
title: ndarray.size — número total de elementos
aliases:
  - size
  - ndarray.size
tags:
  - numpy
  - api/atributo
  - shape
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.size — número total de elementos

## Qué representa

Entero igual al número total de elementos del array: el producto de todas las dimensiones del [[concepto_shape|shape]]. No depende del `dtype`, solo de la forma.

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `int` | **Solo lectura** — es una propiedad derivada del shape |

**Fórmula:** `size == producto(shape)`.

## Ejemplos

```python
import numpy as np
np.zeros((2, 3)).size     # → 6    = 2*3
np.zeros((2, 3, 4)).size  # → 24   = 2*3*4
np.array(5).size          # → 1    escalar 0D tiene 1 elemento
np.zeros((0, 3)).size     # → 0    array vacío
```

```python
arr = np.arange(12).reshape(3, 4)
arr.size                  # → 12
arr.shape[0] * arr.shape[1]  # → 12  equivalente manual
```

## Diferencia con len()

| Expresión | Devuelve | En array 2×3 |
|-----------|----------|--------------|
| `arr.size` | total de elementos | `6` |
| `len(arr)` | tamaño del primer eje (shape[0]) | `2` |

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_ndarray]]
- [[ndarray.shape]]
- [[ndarray.ndim]]
- [[ndarray.nbytes]]
