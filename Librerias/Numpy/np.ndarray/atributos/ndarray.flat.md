---
title: ndarray.flat — Iterador 1D sobre todos los elementos
aliases:
  - flat
  - ndarray.flat
tags:
  - numpy
  - api/atributo
  - estructura
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.flat — Iterador 1D sobre todos los elementos

Devuelve un iterador `numpy.flatiter` que recorre **todos los elementos** del array como si fuera 1D, en **orden C** (row-major), sea cual sea su forma. No es un array nuevo: es un objeto **indexable** (`a.flat[i]`) y **asignable** que opera directamente sobre la memoria original. Para obtener un array 1D real, no un iterador, se usa [[np.ravel]] (vista si puede) o `ndarray.flatten` (copia).

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `numpy.flatiter` |
| Lectura/escritura | **Asignable** (escritura in-place) e **indexable** |
| Orden de recorrido | C-order (row-major) |
| Crea copia | No — opera sobre la memoria original |

## En detalle

`flat` admite indexado entero y por slices con un solo índice plano, sin importar el `ndim` del array. Asignar a través de él reescribe el buffer original.

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

list(arr.flat)      # → [1, 2, 3, 4, 5, 6]
arr.flat[3]         # → 4  (índice plano 1D)
arr.flat[2:5]       # → array([3, 4, 5])

arr.flat[0] = 99    # asignación in-place
arr                 # → array([[99, 2, 3], [4, 5, 6]])

for x in arr.flat:  # iterable elemento a elemento
    pass
```

Diferencia con `ravel`/`flatten`, que **sí** devuelven un array:

| Forma | Resultado | Memoria |
|-------|-----------|---------|
| `arr.flat` | Iterador `flatiter` | Sobre el original |
| `arr.ravel()` | `ndarray` 1D | Vista si es posible |
| `arr.flatten()` | `ndarray` 1D | Siempre copia |

## Casos de uso

- Indexar el elemento $i$-ésimo en orden C sin aplanar el array: `arr.flat[i]`.
- Asignar a posiciones planas (`arr.flat[[0, 2]] = -1`) sin crear copia.
- Iterar elemento a elemento cuando no importa la forma, ahorrando un `ravel`.

## Notas relacionadas

- [[np.ravel]]
- [[concepto_ndarray]]
