---
title: ndarray.ndim — número de ejes del array
aliases:
  - ndim
  - ndarray.ndim
tags:
  - numpy
  - api/atributo
  - shape
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.ndim — número de ejes del array

Entero $k$ con el número de ejes (dimensiones) del array, también llamado *rank* del tensor. Es exactamente la longitud de la tupla [[concepto_shape|shape]]: $k = \text{len(shape)}$.

## Tipo y lectura/escritura

| Tipo de dato | ¿Asignable? |
|--------------|-------------|
| `int` | **No.** Solo lectura; es una propiedad derivada del shape |

## En detalle

`ndim` clasifica el array por su número de ejes, independientemente del tamaño de cada uno.

```python
import numpy as np

np.array(5).ndim          # 0   escalar 0D     → shape ()
np.array([1, 2, 3]).ndim  # 1   vector         → shape (3,)
np.zeros((2, 3)).ndim     # 2   matriz         → shape (2, 3)
np.zeros((2, 3, 4)).ndim  # 3   tensor 3D      → shape (2, 3, 4)

arr = np.zeros((2, 3, 4))
arr.ndim == len(arr.shape)   # True   siempre
```

| Shape | `ndim` | Nombre común |
|-------|--------|--------------|
| `()` | 0 | escalar 0D |
| `(n,)` | 1 | vector |
| `(m, n)` | 2 | matriz |
| `(p, m, n)` | 3 | tensor 3D |

## Casos de uso

```python
# Aceptar 1D o 2D y normalizar a 2D
if arr.ndim == 1:
    arr = arr[np.newaxis, :]

# Validar que llega un tensor del rango esperado
assert imgs.ndim == 4, "se esperaba (lote, alto, ancho, canales)"

# Construir un índice genérico para cualquier rango
arr[(0,) * arr.ndim]   # el primer elemento, sea cual sea ndim
```

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_ndarray]]
- [[ndarray.shape]]
- [[ndarray.size]]
