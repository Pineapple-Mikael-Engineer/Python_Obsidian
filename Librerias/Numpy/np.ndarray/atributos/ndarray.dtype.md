---
title: ndarray.dtype — tipo de dato de los elementos
aliases:
  - dtype
  - ndarray.dtype
tags:
  - numpy
  - api/atributo
  - dtype
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.dtype — tipo de dato de los elementos

## Qué representa

Objeto `numpy.dtype` que describe el tipo uniforme de todos los elementos del array. Por la homogeneidad estricta del [[concepto_dtype|ndarray]], todos los valores comparten este mismo tipo y ocupan los mismos bytes.

## Tipo y acceso

| Tipo de dato | ¿Solo lectura o asignable? |
|--------------|----------------------------|
| `numpy.dtype` | **Solo lectura** en la práctica — para cambiar el tipo se usa `astype` (crea una copia convertida), no asignación |

> Reasignar `dtype` directamente es técnicamente posible pero **reinterpreta los bytes crudos** sin convertir valores; es una operación de bajo nivel y peligrosa. Para convertir tipos, usar siempre `astype`.

## Ejemplos

```python
import numpy as np
np.array([1, 2, 3]).dtype        # → dtype('int64')
np.array([1.0, 2.0]).dtype       # → dtype('float64')
np.array([True, False]).dtype    # → dtype('bool')
```

```python
arr = np.array([1, 2, 3])
arr.dtype.name      # → 'int64'
arr.dtype.itemsize  # → 8   bytes por elemento
arr.dtype.kind      # → 'i' (signed integer)
```

## Conversión correcta de tipo

```python
arr = np.array([1, 2, 3])          # dtype int64
arr_f = arr.astype(np.float64)     # nueva copia
arr_f.dtype                        # → dtype('float64')
arr.dtype                          # → dtype('int64')  el original no cambia
```

## Notas relacionadas

- [[concepto_dtype]]
- [[concepto_ndarray]]
- [[ndarray.itemsize]]
- [[ndarray.astype]]
