---
title: ndarray.strides — Bytes a saltar por dimensión
aliases:
  - strides
  - ndarray.strides
tags:
  - numpy
  - api/atributo
  - memoria
lib: numpy
obj: ndarray
tipo: atributo
draft: false
---

# ndarray.strides — Bytes a saltar por dimensión

## Qué representa

Tupla que indica, **en bytes**, cuánto avanzar en el buffer de memoria para moverse una posición a lo largo de cada dimensión. Es el mecanismo que permite reinterpretar el mismo bloque lineal de memoria con distintas formas y crear vistas sin copiar datos: ver [[concepto_views_vs_copias]]. Cambiar el orden de los strides (transponer, slicing) produce vistas; un array con strides "naturales" se considera contiguo en memoria, ver [[concepto_contiguidad_memoria]].

## Tipo y acceso

| Aspecto | Valor |
|---------|-------|
| Tipo devuelto | `tuple` de `int` (longitud = `ndim`) |
| Acceso | **SOLO LECTURA** (asignación posible pero avanzada y peligrosa) |
| Unidad | Bytes |
| Relación con shape | `strides[i]` = bytes para avanzar 1 en el eje `i` |

## Ejemplos

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]], dtype=np.int64)
# itemsize = 8 bytes, shape = (2, 3)

arr.strides         # → (24, 8)
#   fila:    3 elementos × 8 = 24 bytes
#   columna: 1 elemento  × 8 =  8 bytes

arr.T.strides       # → (8, 24)  (vista: strides invertidos)
arr[::2].strides    # → (48, 8)  (vista: salto doblado por eje)
```

## Por qué importan

| Uso | Detalle |
|-----|---------|
| Vistas sin copia | Slicing/transpose solo reescriben strides |
| Contiguidad | Strides "naturales" → C-order o F-order |
| Rendimiento | Strides grandes/no contiguos degradan la iteración |
| Trucos avanzados | `as_strided` fabrica ventanas deslizantes |

## Notas relacionadas

- [[concepto_views_vs_copias]]
- [[concepto_contiguidad_memoria]]
