---
title: ndarray.ndim — número de dimensiones
aliases:
  - ndim
  - ndarray.ndim
tags:
  - numpy
  - api/atributo
  - shape
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.ndim — número de dimensiones

## Qué representa

Entero con el número de ejes (dimensiones) del array, también llamado *rank*. Equivale a la longitud de la tupla [[concepto_shape|shape]].

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `int` | **Solo lectura** — es una propiedad derivada del shape |

**Fórmula:** `ndim == len(shape)`.

## Ejemplos

```python
import numpy as np
np.array(5).ndim          # → 0   escalar 0D
np.array([1, 2, 3]).ndim  # → 1   vector
np.zeros((2, 3)).ndim     # → 2   matriz
np.zeros((2, 3, 4)).ndim  # → 3   tensor
```

```python
arr = np.zeros((2, 3, 4))
arr.ndim          # → 3
len(arr.shape)    # → 3   equivalente
```

## Mapa shape → ndim

| Shape | ndim | Nombre común |
|-------|------|--------------|
| `()` | 0 | Escalar 0D |
| `(n,)` | 1 | Vector |
| `(m, n)` | 2 | Matriz |
| `(p, m, n)` | 3 | Tensor 3D |

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_ndarray]]
- [[ndarray.shape]]
- [[ndarray.size]]
