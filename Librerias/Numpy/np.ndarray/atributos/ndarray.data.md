---
title: ndarray.data — Buffer crudo de memoria del array
aliases:
  - data
  - ndarray.data
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
mod: np.ndarray
tipo: atributo
draft: false
---

# ndarray.data — Buffer crudo de memoria del array

Objeto `memoryview` (buffer de Python) que apunta al **bloque lineal de bytes** donde el array guarda sus valores. Es el dato bruto que `shape`, `dtype` y `strides` interpretan como tensor: ver [[concepto_ndarray]]. Rara vez se accede directamente; sirve para interoperar con el protocolo buffer de Python o inspeccionar la memoria de bajo nivel.

## Tipo y lectura/escritura

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `memoryview` (buffer de Python) |
| Lectura/escritura | **Solo lectura** del atributo (el buffer no se reasigna) |
| Contenido | Bytes brutos del array |
| Uso típico | Protocolo buffer / interop de bajo nivel |

## En detalle

El `memoryview` es escribible si el array lo es, pero el atributo `data` en sí no se reasigna. Acceder a los bytes respeta el orden de almacenamiento del buffer (C-order por defecto), no la forma lógica.

```python
import numpy as np

arr = np.array([1, 2, 3], dtype=np.int8)

arr.data                    # → <memory at 0x...>
bytes(arr.data)             # → b'\x01\x02\x03'
arr.data.nbytes             # → 3

mv = arr.data
mv.readonly                 # → False  (escribible si el array lo es)
```

Lugar de `data` entre los componentes del ndarray:

| Componente | Atributo | Rol |
|------------|----------|-----|
| Buffer crudo | `ndarray.data` | Bytes en memoria |
| Forma | `ndarray.shape` | Cómo se agrupan |
| Tipo | `ndarray.dtype` | Cómo se decodifican |
| Saltos | `ndarray.strides` | Cómo se recorren |

## Casos de uso

- Exponer el array a una API que consume el protocolo buffer de Python.
- Inspeccionar los bytes crudos para depurar endianness o empaquetado.
- Pasar memoria sin copia a bibliotecas que aceptan `memoryview`.

## Notas relacionadas

- [[concepto_ndarray]]
- [[ndarray.ctypes]]
