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
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.size — número total de elementos

Entero igual al número **total** de elementos del array: el producto de todos los tamaños del [[concepto_shape|shape]], $\text{size} = \prod_{i=0}^{k-1} n_i$. No depende del `dtype`, solo de la forma.

## Tipo y lectura/escritura

| Tipo de dato | ¿Asignable? |
|--------------|-------------|
| `int` | **No.** Solo lectura; es una propiedad derivada del shape |

## En detalle

`size` cuenta elementos, no bytes (para bytes está `nbytes = size × itemsize`). Un escalar 0D tiene un elemento; un array con algún eje de tamaño 0 tiene `size == 0`.

```python
import numpy as np

np.zeros((2, 3)).size     # 6    = 2*3
np.zeros((2, 3, 4)).size  # 24   = 2*3*4
np.array(5).size          # 1    escalar 0D tiene 1 elemento
np.zeros((0, 3)).size     # 0    array vacío
```

> [!important] `size` no es `len(arr)`
> `len(arr)` devuelve **solo el primer eje** (`shape[0]`), no el total. En un `(2, 3)`: `size == 6` pero `len(arr) == 2`.

| Expresión | Devuelve | En array `(2, 3)` |
|-----------|----------|-------------------|
| `arr.size` | total de elementos ($\prod n_i$) | `6` |
| `len(arr)` | tamaño del primer eje (`shape[0]`) | `2` |

## Casos de uso

```python
# Detectar un array vacío sin tocar el shape entero
if arr.size == 0:
    return

# Reformar a 1D sin conocer las dimensiones
plano = arr.reshape(arr.size)        # o arr.reshape(-1)

# Estimar memoria: elementos * bytes por elemento (= arr.nbytes)
mem_bytes = arr.size * arr.itemsize

# Comprobar compatibilidad antes de un reshape
nuevo_size == arr.size   # condición para que reshape sea posible
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Usar `len(arr)` como total | `len` es solo `shape[0]` | Usar `arr.size` para el conteo total |
| Esperar `> 0` para un array vacío | `(0, 3)` tiene `size == 0` aunque `ndim == 2` | Comprobar `arr.size == 0`, no `len(arr)` |

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_ndarray]]
- [[ndarray.shape]]
- [[ndarray.ndim]]
- [[ndarray.nbytes]]
