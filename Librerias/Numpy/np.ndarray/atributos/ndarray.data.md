---
title: ndarray.data — Buffer de Python con la memoria cruda
aliases:
  - data
  - ndarray.data
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.data — Buffer de Python con la memoria cruda

## Qué representa

Objeto `memoryview` (buffer de Python) que apunta al **bloque lineal de bytes** donde el array almacena sus valores. Es el componente fundamental del ndarray: el buffer crudo que `shape`, `dtype` y `strides` interpretan. Rara vez se usa directamente; sirve para interoperar con el protocolo buffer de Python o inspeccionar la memoria subyacente: ver [[concepto_ndarray]].

## Tipo y acceso

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `memoryview` (buffer de Python) |
| Acceso | **SOLO LECTURA** del atributo (no se reasigna el buffer) |
| Contenido | Bytes brutos del array |
| Uso típico | Protocolo buffer / interop de bajo nivel |

## Ejemplos

```python
import numpy as np

arr = np.array([1, 2, 3], dtype=np.int8)

arr.data                    # → <memory at 0x...>
bytes(arr.data)             # → b'\x01\x02\x03'
arr.data.nbytes             # → 3

mv = arr.data
mv.readonly                 # → False  (escribible si el array lo es)
```

## Relación con la arquitectura interna

| Componente | Atributo | Rol |
|------------|----------|-----|
| Buffer crudo | `ndarray.data` | Bytes en memoria |
| Forma | `ndarray.shape` | Cómo se agrupan |
| Tipo | `ndarray.dtype` | Cómo se decodifican |
| Saltos | `ndarray.strides` | Cómo se recorren |

## Notas relacionadas

- [[concepto_ndarray]]
- [[ndarray.ctypes]]
