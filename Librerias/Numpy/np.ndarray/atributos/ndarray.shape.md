---
title: ndarray.shape — tupla con el tamaño de cada dimensión
aliases:
  - shape
  - ndarray.shape
tags:
  - numpy
  - api/atributo
  - shape
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.shape — tupla con el tamaño de cada dimensión

## Qué representa

Tupla de enteros no negativos donde cada elemento indica cuántos elementos hay en el eje correspondiente. Es el metadato que convierte el buffer lineal en una estructura multidimensional navegable; ver [[concepto_shape]].

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `tuple` de `int` | **Asignable** — reasignar hace un reshape *in-place* si el `size` es compatible (no copia datos) |

## Ejemplos

```python
import numpy as np
arr = np.zeros((2, 3))
arr.shape          # → (2, 3)
len(arr.shape)     # → 2   (igual a arr.ndim)
```

```python
np.array(5).shape  # → ()    escalar 0D, tupla vacía
np.arange(4).shape # → (4,)  la coma no es opcional
```

## Reasignación in-place

Asignar a `shape` reinterpreta el mismo buffer sin copiar, siempre que el `size` total se conserve:

```python
arr = np.arange(12)
arr.shape = (3, 4)   # OK → producto = 12
arr.shape            # → (3, 4)

arr.shape = (5, 2)   # ValueError: total size must be unchanged (5*2=10 != 12)
```

A diferencia de `reshape`, la asignación a `shape` **falla** si la operación requiriese una copia (array no contiguo).

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_ndarray]]
- [[ndarray.ndim]]
- [[ndarray.size]]
- [[np.reshape]]
