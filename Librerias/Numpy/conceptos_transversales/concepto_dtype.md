---
title: Dtype — El sistema de tipos de NumPy
aliases:
  - dtype
  - tipo de dato
  - data type
tags:
  - numpy
  - concepto
  - dtype
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
draft: false
---

# Dtype — El sistema de tipos de NumPy

## Definicion fundamental

El **dtype** (data type) es el metadato que define **como interpretar los bytes** de cada elemento del buffer de un [[concepto_ndarray|ndarray]]: cuantos bytes ocupa, si es entero o flotante, con o sin signo, su endianness.

**Caracteristica esencial:** un array es estrictamente **homogeneo**. Todos sus elementos comparten el mismo dtype. Esto es lo que permite el almacenamiento contiguo de tamaño fijo y la [[concepto_vectorizacion|vectorizacion]] en C.

## Por que existe un sistema de tipos propio

Python usa objetos con tipado dinamico: un `int` de Python es un objeto completo con overhead. NumPy necesita lo contrario para ser rapido:

```python
import numpy as np

# Python: cada entero es un objeto (~28 bytes), tipos mezclables
lista = [1, 2.5, "tres"]

# NumPy: un tipo fijo, bytes compactos, sin overhead por elemento
arr = np.array([1, 2, 3], dtype=np.int32)
arr.itemsize   # 4 bytes por elemento, exactos
```

El dtype fijo es lo que habilita operar sobre el buffer directamente en codigo C compilado.

## Categorias y tamaños

| Categoria | Tipos | Bytes | Rango / nota |
|-----------|-------|-------|--------------|
| Booleano | `bool_` | 1 | `True` / `False` |
| Entero con signo | `int8`, `int16`, `int32`, `int64` | 1–8 | `int8`: -128..127 |
| Entero sin signo | `uint8`, `uint16`, `uint32`, `uint64` | 1–8 | `uint8`: 0..255 |
| Flotante | `float16`, `float32`, `float64` | 2–8 | `float64` es el por defecto |
| Complejo | `complex64`, `complex128` | 8–16 | parte real + imaginaria |
| Texto | `str_` (`<U`), `bytes_` (`<S`) | variable | longitud fija por elemento |
| Objeto | `object_` | puntero | rompe la vectorizacion |

**Por defecto:** enteros de Python → `int64` (plataforma dependiente), flotantes → `float64`.

```python
np.array([1, 2, 3]).dtype       # int64
np.array([1.0, 2.0]).dtype      # float64
np.array([1, 2.0]).dtype        # float64  → promocion
```

## La regla central: promocion de tipos (upcasting)

Cuando se combinan dtypes distintos, NumPy promueve al tipo **mas general** capaz de representar ambos, siguiendo la jerarquia:

```
bool → int → uint → float → complex
```

| Operacion | dtype A | dtype B | dtype resultado |
|-----------|---------|---------|-----------------|
| `int32 + int64` | int32 | int64 | int64 |
| `int32 + float32` | int32 | float32 | float64 |
| `float32 + float64` | float32 | float64 | float64 |
| `int + complex` | int | complex128 | complex128 |
| `bool + int8` | bool | int8 | int8 |

```python
a = np.array([1, 2], dtype=np.int32)
b = np.array([0.5, 1.5], dtype=np.float32)
(a + b).dtype   # float64  → upcasting para no perder precision
```

## Conversion explicita con `astype`

`astype` **siempre crea una copia** con el nuevo dtype:

```python
arr = np.array([1.7, 2.9, 3.1])
arr.astype(np.int32)    # [1, 2, 3]  → truncamiento, NO redondeo
arr.astype(np.bool_)    # [True, True, True]  → 0 es False, resto True
```

## Casos que fallan (errores tipicos)

### Error 1: overflow silencioso en enteros

```python
arr = np.array([250], dtype=np.uint8)  # rango 0..255
arr + 10
# array([4], dtype=uint8)  → 260 da la vuelta (wrap-around), sin aviso
```

### Error 2: perdida de precision al truncar

```python
np.array([3.99]).astype(np.int32)   # array([3])  → no redondea, trunca
# Para redondear: np.round(arr).astype(np.int32)
```

### Error 3: dtype `object` que mata el rendimiento

```python
arr = np.array([1, "dos", 3.0])   # dtype('O') → object
# Opera elemento a elemento en Python: se pierde la vectorizacion
```

### Error 4: comparar flotantes por igualdad exacta

```python
a = np.array([0.1 + 0.2])
a == 0.3              # array([False])  → error de redondeo binario
np.isclose(a, 0.3)   # array([ True])  → forma correcta
```

## Ejemplos progresivos

### Nivel 1: declarar el dtype al crear

```python
np.zeros(3, dtype=np.int8)      # [0, 0, 0] en int8
np.ones(3, dtype=np.float32)    # [1., 1., 1.] en float32
np.array([1, 2], dtype=complex) # [1.+0.j, 2.+0.j]
```

### Nivel 2: elegir el dtype para ahorrar memoria

```python
# Imagen 1000x1000 en escala de grises 0..255
img64 = np.zeros((1000, 1000))             # float64 → 8 MB
img8  = np.zeros((1000, 1000), np.uint8)   # uint8   → 1 MB (8x menos)
```

### Nivel 3: inspeccionar y decidir conversiones

```python
arr = np.array([1.0, 2.0, 3.0])
arr.dtype.kind      # 'f'  → flotante
arr.dtype.itemsize  # 8

# kinds: 'b' bool, 'i' int, 'u' uint, 'f' float, 'c' complex, 'U' str, 'O' object
if arr.dtype.kind == 'f':
    arr = arr.astype(np.float32)  # mitad de memoria
```

## Valores especiales de los flotantes

Solo los dtypes flotantes y complejos admiten estos valores:

| Valor | Significado | Como detectarlo |
|-------|-------------|-----------------|
| `np.nan` | Not a Number | `np.isnan(arr)` |
| `np.inf` | Infinito positivo | `np.isinf(arr)` |
| `-np.inf` | Infinito negativo | `np.isinf(arr)` |

```python
arr = np.array([1.0, np.nan, np.inf])
np.isnan(arr)   # [False,  True, False]
arr.sum()       # nan  → cualquier operacion con nan propaga nan
np.nansum(arr)  # inf  → las variantes nan* ignoran los nan
```

## Relacion con otros conceptos

- [[concepto_ndarray]]
- [[concepto_vectorizacion]]
- [[concepto_shape]]
- [[concepto_ufuncs]]
- [[ndarray.astype]]
- [[ndarray.dtype]]
