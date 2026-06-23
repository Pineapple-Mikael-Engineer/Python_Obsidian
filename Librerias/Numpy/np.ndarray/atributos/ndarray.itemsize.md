---
title: ndarray.itemsize — bytes que ocupa un elemento
aliases:
  - itemsize
  - ndarray.itemsize
tags:
  - numpy
  - api/atributo
  - dtype
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.itemsize — bytes que ocupa un elemento

Entero con el tamaño en bytes de **un único elemento** del array. Depende exclusivamente del [[concepto_dtype|dtype]]: equivale a `dtype.itemsize` (p. ej. `float64` → 8). Como el array es homogéneo, todos los elementos ocupan lo mismo, y de ahí sale `nbytes = size × itemsize`.

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `int` |
| Lectura/escritura | **Solo lectura** — derivado del dtype |

**Fórmula:** $\text{itemsize} = \text{dtype.itemsize}$.

## En detalle

El `itemsize` lo fija el dtype al crear el array; cambiarlo exige cambiar el dtype (`astype`). Es el factor que decide cuántos strides (en bytes) separan a elementos vecinos.

```python
import numpy as np

np.array([1, 2], dtype=np.int8).itemsize     # → 1
np.array([1, 2], dtype=np.int64).itemsize    # → 8
np.array([1.0], dtype=np.float32).itemsize   # → 4
np.array([1.0], dtype=np.float64).itemsize   # → 8
np.array([1j], dtype=np.complex128).itemsize # → 16
```

Bytes por dtype común:

| dtype | itemsize (bytes) |
|-------|------------------|
| `bool_` | 1 |
| `int8` / `uint8` | 1 |
| `int16` / `uint16` | 2 |
| `int32` / `float32` | 4 |
| `int64` / `float64` | 8 |
| `complex128` | 16 |

## Casos de uso

- Calcular la memoria total junto con `size`: `arr.size * arr.itemsize == arr.nbytes`.
- Verificar la precisión activa de un array flotante (8 bytes → `float64`).
- Razonar sobre los strides, que son múltiplos del `itemsize`.

## Notas relacionadas

- [[concepto_dtype]]
- [[ndarray.nbytes]]
