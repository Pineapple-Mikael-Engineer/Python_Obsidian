---
title: ndarray.T — vista transpuesta con los ejes invertidos
aliases:
  - T
  - ndarray.T
tags:
  - numpy
  - api/atributo
  - shape
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.T — vista transpuesta con los ejes invertidos

## Qué representa

Vista del array con el orden de sus ejes completamente invertido. Es equivalente a [[np.transpose]] sin argumentos: el shape `(d0, d1, ..., dn)` pasa a `(dn, ..., d1, d0)`. No copia datos: solo reescribe shape y strides.

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `ndarray` (vista) | **Solo lectura** como atributo (no se reasigna `arr.T = ...`); pero la vista comparte memoria, así que escribir en ella modifica el array base |

## Ejemplos

```python
import numpy as np
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
arr.shape    # → (2, 3)
arr.T.shape  # → (3, 2)
arr.T        # → [[1, 4], [2, 5], [3, 6]]
```

```python
np.zeros((2, 3, 4)).T.shape  # → (4, 3, 2)   invierte TODOS los ejes
```

## Caso 1D: transponer no hace nada

```python
v = np.array([1, 2, 3])  # shape (3,)
v.T.shape                # → (3,)   un vector 1D no cambia
# Para una columna real: v[:, np.newaxis]  → (3, 1)
```

## Es una vista (comparte memoria)

```python
arr = np.array([[1, 2], [3, 4]])
t = arr.T
t[0, 0] = 99
arr[0, 0]   # → 99   T y arr comparten el mismo buffer
```

## Notas relacionadas

- [[concepto_views_vs_copias]]
- [[concepto_shape]]
- [[np.transpose]]
- [[ndarray.shape]]
