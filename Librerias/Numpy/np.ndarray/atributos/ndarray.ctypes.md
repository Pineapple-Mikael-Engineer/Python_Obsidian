---
title: ndarray.ctypes — Interfaz para pasar el array a C
aliases:
  - ctypes
  - ndarray.ctypes
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.ctypes — Interfaz para pasar el array a C

## Qué representa

Objeto que expone la memoria del array a través de la librería `ctypes`, permitiendo pasar **punteros** (a los datos, al shape y a los strides) a funciones escritas en C/C++ o cargadas vía bibliotecas compartidas. No copia datos: entrega referencias crudas al buffer subyacente, por lo que la vida del array debe sobrevivir al uso del puntero.

## Tipo y acceso

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `numpy.core._internal._ctypes` |
| Acceso | **SOLO LECTURA** |
| Atributos clave | `.data`, `.shape`, `.strides` |
| Métodos clave | `.data_as(...)`, `.shape_as(...)`, `.strides_as(...)` |

## Ejemplos

```python
import numpy as np
import ctypes

arr = np.array([1, 2, 3], dtype=np.int32)

arr.ctypes.data                     # → direccion de memoria (int)
ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
ptr[0]                              # → 1  (acceso via puntero C)

arr.ctypes.shape                    # → puntero a la tupla shape
arr.ctypes.strides                  # → puntero a la tupla strides
```

## Cuándo usarlo

| Escenario | Uso |
|-----------|-----|
| Llamar función C externa | Pasar `data_as(POINTER(...))` |
| Interop con `ctypes.CDLL` | Evitar copias del buffer |
| Wrappers de bajo nivel | Acceso directo a memoria |

## Notas relacionadas

- [[concepto_ndarray]]
- [[ndarray.data]]
