---
title: ndarray.nbytes — bytes totales consumidos por los datos
aliases:
  - nbytes
  - ndarray.nbytes
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.nbytes — bytes totales consumidos por los datos

## Qué representa

Entero con el total de bytes que ocupan los elementos del array en memoria: el número de elementos por el tamaño de cada uno. Mide el buffer de datos del [[concepto_ndarray|ndarray]], no el overhead del objeto Python ni metadatos.

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `int` | **Solo lectura** — derivado de `size` e `itemsize` |

**Fórmula:** `nbytes == size * itemsize`.

## Ejemplos

```python
import numpy as np
arr = np.zeros((2, 3), dtype=np.int64)
arr.size       # → 6
arr.itemsize   # → 8
arr.nbytes     # → 48   = 6 * 8
```

```python
np.zeros((1000,), dtype=np.float32).nbytes  # → 4000
np.zeros((1000,), dtype=np.float64).nbytes  # → 8000
```

## nbytes no cuenta vistas ni overhead

Una vista comparte el buffer con su array base, pero `nbytes` reporta el tamaño lógico de la vista, no la memoria realmente reservada. Para el consumo real del objeto Python ver `sys.getsizeof`, que sí incluye la cabecera del array.

## Notas relacionadas

- [[concepto_contiguidad_memoria]]
- [[concepto_ndarray]]
- [[ndarray.size]]
- [[ndarray.itemsize]]
