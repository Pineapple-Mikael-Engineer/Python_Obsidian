---
title: ndarray.dtype — tipo de los elementos del array
aliases:
  - dtype
  - ndarray.dtype
tags:
  - numpy
  - api/atributo
  - dtype
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.dtype — tipo de los elementos del array

Objeto `numpy.dtype` que describe el tipo **uniforme** de todos los elementos del array: cuántos bytes ocupa cada uno (`itemsize`), si es entero o flotante, con o sin signo, su endianness. Por la homogeneidad estricta del [[concepto_ndarray|ndarray]], todos los elementos comparten este mismo tipo. El sistema de tipos completo (categorías, promoción, casting) vive en [[concepto_dtype]].

## Tipo y lectura/escritura

| Tipo de dato | ¿Asignable? |
|--------------|-------------|
| `numpy.dtype` | **No directamente.** Para cambiar el tipo se usa [[ndarray.astype]] (convierte valores, crea copia) |

> [!warning] Reasignar `arr.dtype` no convierte: reinterpreta
> `arr.dtype = ...` es técnicamente posible, pero **reinterpreta los bytes crudos** sin convertir valores (un `float64` se lee como dos `int32`, etc.). Es una operación de bajo nivel equivalente a `.view`, peligrosa. Para **convertir** tipos usar siempre `astype`.

## En detalle

El objeto `dtype` no es un simple string: expone subcampos útiles para introspección.

```python
import numpy as np

arr = np.array([1, 2, 3])     # dtype('int64')
arr.dtype.name       # 'int64'
arr.dtype.itemsize   # 8       bytes por elemento
arr.dtype.kind       # 'i'     'i'nt, 'u'int, 'f'loat, 'b'ool, 'c'omplex, 'U' str…
arr.dtype.char       # 'l'
```

Convertir el tipo se hace con `astype`, que crea una copia nueva y **no toca** el original:

```python
arr   = np.array([1, 2, 3])     # int64
arr_f = arr.astype(np.float64)  # nueva copia
arr_f.dtype   # dtype('float64')
arr.dtype     # dtype('int64')  → el original no cambia
```

## Casos de uso

```python
# Ramificar según la familia del tipo
if arr.dtype.kind == 'f':
    arr = np.nan_to_num(arr)

# Asegurar un tipo antes de pasar a una librería que lo exige
arr = arr.astype(np.float32, copy=False)   # copia solo si hace falta

# Comparar dtypes
if a.dtype == b.dtype:
    ...

# Memoria total = size * itemsize (también en arr.nbytes)
arr.size * arr.dtype.itemsize
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `arr.dtype = np.float64` no convierte los datos | Reinterpreta bytes, no castea | Usar `arr.astype(np.float64)` |
| Comparar con string suelto y fallar | `arr.dtype == 'int'` es ambiguo por plataforma | Comparar con `np.int64`, `np.float32`… explícitos |
| Esperar redondeo al castear a entero | `astype(int)` **trunca** hacia 0 | `np.round(arr).astype(int)` para redondear |

## Notas relacionadas

- [[concepto_dtype]]
- [[concepto_ndarray]]
- [[ndarray.itemsize]]
- [[ndarray.astype]]
