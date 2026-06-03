---
title: ndarray.itemsize — bytes que ocupa cada elemento
aliases:
  - itemsize
  - ndarray.itemsize
tags:
  - numpy
  - api/atributo
  - dtype
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.itemsize — bytes que ocupa cada elemento

## Qué representa

Entero con el tamaño en bytes de un único elemento del array. Depende exclusivamente del [[concepto_dtype|dtype]]: equivale a `dtype.itemsize`. Como el array es homogéneo, todos los elementos ocupan lo mismo.

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `int` | **Solo lectura** — derivado del dtype |

**Fórmula:** `itemsize == dtype.itemsize`.

## Ejemplos

```python
import numpy as np
np.array([1, 2], dtype=np.int8).itemsize     # → 1
np.array([1, 2], dtype=np.int64).itemsize    # → 8
np.array([1.0], dtype=np.float32).itemsize   # → 4
np.array([1.0], dtype=np.float64).itemsize   # → 8
np.array([1j], dtype=np.complex128).itemsize # → 16
```

## Bytes por dtype común

| dtype | itemsize (bytes) |
|-------|------------------|
| `bool_` | 1 |
| `int8` / `uint8` | 1 |
| `int16` / `uint16` | 2 |
| `int32` / `float32` | 4 |
| `int64` / `float64` | 8 |
| `complex128` | 16 |

## Notas relacionadas

- [[concepto_dtype]]
- [[ndarray.dtype]]
- [[ndarray.nbytes]]
