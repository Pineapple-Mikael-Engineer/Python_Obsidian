---
title: ndarray.flat — Iterador 1D sobre los elementos
aliases:
  - flat
  - ndarray.flat
tags:
  - numpy
  - api/atributo
  - estructura
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.flat — Iterador 1D sobre los elementos

## Qué representa

Devuelve un iterador `np.flatiter` que recorre **todos los elementos** del array como si fuera 1D, en orden C (row-major), sin importar su forma. No es un array nuevo: es un objeto indexable y asignable que opera directamente sobre la memoria original. Para obtener un array aplanado real conviene usar [[np.ravel]] o `ndarray.flatten`.

## Tipo y acceso

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `numpy.flatiter` |
| Acceso | **ASIGNABLE** (escritura in-place) e indexable |
| Orden de recorrido | C-order (row-major) |
| Crea copia | No (opera sobre la memoria original) |

## Ejemplos

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

list(arr.flat)      # → [1, 2, 3, 4, 5, 6]
arr.flat[3]         # → 4  (indexado 1D)
arr.flat[2:5]       # → array([3, 4, 5])

arr.flat[0] = 99    # asignacion in-place
arr                 # → array([[99, 2, 3], [4, 5, 6]])

for x in arr.flat:  # iterable elemento a elemento
    pass
```

## Diferencia con ravel/flatten

| Forma | Resultado | Memoria |
|-------|-----------|---------|
| `arr.flat` | Iterador `flatiter` | Sobre el original |
| `arr.ravel()` | `ndarray` 1D | Vista si es posible |
| `arr.flatten()` | `ndarray` 1D | Siempre copia |

## Notas relacionadas

- [[np.ravel]]
- [[concepto_ndarray]]
