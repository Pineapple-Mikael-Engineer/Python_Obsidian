---
title: ndarray.nbytes — bytes totales que ocupan los datos
aliases:
  - nbytes
  - ndarray.nbytes
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.nbytes — bytes totales que ocupan los datos

Entero con los **bytes totales** que consumen los elementos del array en memoria: el número de elementos por el tamaño de cada uno. Mide solo el buffer de datos del [[concepto_ndarray|ndarray]], **no** el overhead del objeto Python ni los metadatos (`shape`, `strides`, cabecera).

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `int` |
| Lectura/escritura | **Solo lectura** — derivado de `size` e `itemsize` |

**Fórmula:** $\text{nbytes} = \text{size} \times \text{itemsize}$.

## En detalle

`nbytes` es el tamaño **lógico** del bloque de datos. Sobre una vista reporta los bytes de los elementos que la vista cubre, no la memoria realmente reservada por el array base. Para el peso real del objeto Python (con cabecera incluida) se usa `sys.getsizeof`.

```python
import numpy as np

arr = np.zeros((2, 3), dtype=np.int64)
arr.size       # → 6
arr.itemsize   # → 8
arr.nbytes     # → 48   = 6 * 8

np.zeros((1000,), dtype=np.float32).nbytes  # → 4000   (1000 × 4)
np.zeros((1000,), dtype=np.float64).nbytes  # → 8000   (1000 × 8)
```

## Casos de uso

- Estimar el coste en memoria de un array grande antes de crearlo o cargarlo.
- Comparar el ahorro de un dtype más estrecho: `float32` ocupa la mitad que `float64`.
- Convertir a unidades legibles: `arr.nbytes / 1024**2` → megabytes.

## Notas relacionadas

- [[concepto_ndarray]]
- [[ndarray.itemsize]]
