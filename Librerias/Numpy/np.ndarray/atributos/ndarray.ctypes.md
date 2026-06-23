---
title: ndarray.ctypes — Interfaz para pasar el array a código C
aliases:
  - ctypes
  - ndarray.ctypes
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.ctypes — Interfaz para pasar el array a código C

Objeto que expone la memoria del array a través de la librería `ctypes`, para pasar **punteros** (a los datos, al `shape` y a los `strides`) a funciones escritas en C/C++ o cargadas desde bibliotecas compartidas. No copia datos: entrega referencias crudas al buffer del [[concepto_ndarray|ndarray]], así que el array debe seguir vivo mientras el puntero esté en uso. Es interoperabilidad avanzada.

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | objeto `_ctypes` interno de NumPy |
| Lectura/escritura | **Solo lectura** |
| Atributos clave | `.data` (puntero a los datos), `.shape`, `.strides` |
| Métodos clave | `.data_as(...)`, `.shape_as(...)`, `.strides_as(...)` |

## En detalle

`arr.ctypes.data` es la **dirección de memoria** (un entero) del primer byte del buffer; `.data_as(POINTER(...))` lo envuelve en un puntero `ctypes` tipado, listo para una llamada C. Para que el código C lea el array correctamente debe ser **contiguo**; si no lo es, conviene pasar también `shape` y `strides`.

```python
import numpy as np
import ctypes

arr = np.array([1, 2, 3], dtype=np.int32)

arr.ctypes.data                     # → dirección de memoria (int)
ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
ptr[0]                              # → 1  (acceso vía puntero C)

arr.ctypes.shape                    # → puntero a la tupla shape
arr.ctypes.strides                  # → puntero a la tupla strides
```

## Casos de uso

- Llamar a una función de una `.so`/`.dll` cargada con `ctypes.CDLL`, pasando `data_as(...)`.
- Compartir el buffer con código nativo sin copiarlo (rendimiento en bucles C).
- Escribir wrappers de bajo nivel que necesitan punteros a `data`, `shape` y `strides`.

## Notas relacionadas

- [[concepto_ndarray]]
- [[ndarray.data]]
