---
title: ndarray.T — la traspuesta, una vista con los ejes invertidos
aliases:
  - T
  - ndarray.T
tags:
  - numpy
  - api/atributo
  - shape
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.T — la traspuesta, una vista con los ejes invertidos

La traspuesta del array: una **vista** con el orden de todos sus ejes completamente invertido. Es un **atributo**, no un método (`arr.T`, sin paréntesis), equivalente a [[np.transpose]] sin argumentos: el shape $(d_0, d_1, \dots, d_n)$ pasa a $(d_n, \dots, d_1, d_0)$. No copia datos: solo invierte shape y strides.

## Tipo y lectura/escritura

| Tipo de dato | ¿Asignable? |
|--------------|-------------|
| `ndarray` (**vista**) | **No** como atributo (`arr.T = ...` no existe). Pero la vista comparte buffer: escribir en `arr.T` modifica `arr` |

## En detalle

`.T` invierte **todos** los ejes a la vez. Para 2D es la traspuesta matricial habitual; para N-D invierte la tupla entera.

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])
arr.shape    # (2, 3)
arr.T.shape  # (3, 2)
arr.T        # [[1, 4], [2, 5], [3, 6]]

np.zeros((2, 3, 4)).T.shape   # (4, 3, 2)   invierte TODOS los ejes
```

Es una vista, así que comparte memoria:

```python
arr = np.array([[1, 2], [3, 4]])
t = arr.T
t[0, 0] = 99
arr[0, 0]   # 99   → T y arr comparten el mismo buffer
```

> [!warning] `.T` sobre un 1D no hace nada
> Transponer permuta ejes; con un solo eje no hay nada que permutar. `np.array([1,2,3]).T.shape` sigue siendo `(3,)`. Para una columna real hay que **añadir** un eje: `v[:, np.newaxis]` → `(3, 1)`.

**`.T` vs [[np.linalg.matrix_transpose]]:** `.T` invierte *todos* los ejes; `matrix_transpose` (y `arr.mT`) intercambia **solo los dos últimos**, tratando los ejes previos como un lote de matrices. En 2D coinciden; en 3D+ no.

## Casos de uso

```python
# Producto matricial con la traspuesta
G = arr.T @ arr             # matriz de Gram (n×n)

# Cambiar (alto, ancho) → (ancho, alto) en operaciones 2D
img_t = img.T

# Iterar columnas como si fueran filas
for col in arr.T:
    ...

# Traspuesta de un lote de matrices (NO usar .T): solo los 2 últimos ejes
lote.swapaxes(-1, -2)       # o lote.mT
```

## Notas relacionadas

- [[np.transpose]]
- [[np.linalg.matrix_transpose]]
- [[concepto_views_vs_copias]]
- [[concepto_shape]]
- [[ndarray.shape]]
