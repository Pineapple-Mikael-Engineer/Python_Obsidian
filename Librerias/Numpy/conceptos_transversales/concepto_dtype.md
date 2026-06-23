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

## Definición fundamental

El **dtype** (data type) es el metadato que define **cómo interpretar los bytes** de cada elemento del buffer de un [[concepto_ndarray|ndarray]]: cuántos bytes ocupa (`itemsize`), si es entero o flotante, con o sin signo, su endianness.

**Característica esencial:** un array es estrictamente **homogéneo** — un único `dtype` para todo el array, así que **todos sus elementos comparten el mismo `itemsize` y la misma interpretación**. Esto es lo que permite el almacenamiento contiguo de tamaño fijo y la [[concepto_vectorizacion|vectorización]] en C.

## Por qué existe un sistema de tipos propio

Python usa objetos con tipado dinámico: un `int` de Python es un objeto completo con overhead (~28 bytes) y una lista puede mezclar tipos. NumPy necesita lo contrario para ser rápido:

```python
import numpy as np

# Python: cada entero es un objeto (~28 bytes), tipos mezclables
lista = [1, 2.5, "tres"]

# NumPy: un tipo fijo, bytes compactos, sin overhead por elemento
arr = np.array([1, 2, 3], dtype=np.int32)
arr.itemsize   # 4 bytes por elemento, exactos
```

Con un `itemsize` fijo y conocido, NumPy sabe en qué posición de memoria está cada elemento sin inspeccionarlo, y opera sobre el buffer directamente en código C compilado.

## Categorías y tamaños

| Categoría | Tipos | Bytes | Rango / nota |
|-----------|-------|-------|--------------|
| Booleano | `bool_` | 1 | `True` / `False` |
| Entero con signo | `int8`, `int16`, `int32`, `int64` | 1–8 | `int8`: -128..127 |
| Entero sin signo | `uint8`, `uint16`, `uint32`, `uint64` | 1–8 | `uint8`: 0..255 |
| Flotante | `float16`, `float32`, `float64` | 2–8 | `float64` es el por defecto |
| Complejo | `complex64`, `complex128` | 8–16 | parte real + imaginaria |
| Texto | `str_` (`<U`), `bytes_` (`<S`) | variable | longitud fija por elemento |
| Objeto | `object_` | puntero | rompe la vectorización |

**Por defecto:** enteros de Python → `int64` (dependiente de plataforma), flotantes → `float64`.

```python
np.array([1, 2, 3]).dtype       # int64
np.array([1.0, 2.0]).dtype      # float64
np.array([1, 2.0]).dtype        # float64  → promoción
```

## La regla central: promoción de tipos (type promotion)

Cuando se combinan dtypes distintos, NumPy promueve al tipo **más amplio que preserva los valores** de ambos operandos. La idea: el resultado debe poder representar cualquier valor de A y de B sin perder información, siguiendo la jerarquía de "amplitud":

$$ \texttt{bool} \;\rightarrow\; \texttt{int} \;\rightarrow\; \texttt{uint} \;\rightarrow\; \texttt{float} \;\rightarrow\; \texttt{complex} $$

Dentro de cada categoría gana el de mayor `itemsize`. Al **cruzar** categorías (entero + flotante) sube al flotante, y si el entero no cabe en la mantisa elegida, sube a `float64`.

| Operación | dtype A | dtype B | dtype resultado | Por qué |
|-----------|---------|---------|-----------------|---------|
| `int + float` | int64 | float64 | float64 | cruza a flotante |
| `int32 + int64` | int32 | int64 | int64 | mismo grupo, mayor ancho |
| `float32 + float64` | float32 | float64 | float64 | mismo grupo, mayor ancho |
| `int + bool` | int64 | bool | int64 | `bool` es el más bajo |
| `int32 + float32` | int32 | float32 | float64 | int32 no cabe en la mantisa de float32 |
| `int + complex` | int64 | complex128 | complex128 | complex domina a todo |
| `uint8 + int8` | uint8 | int8 | int16 | hace falta signo **y** rango |

```python
a = np.array([1, 2], dtype=np.int32)
b = np.array([0.5, 1.5], dtype=np.float32)
(a + b).dtype   # float64  → int32 no cabe en float32: sube a float64
```

> [!note] El detalle de `int32 + float32 → float64`
> `float32` solo tiene 24 bits de mantisa; un `int32` puede valer hasta ~2.1e9, que no es exactamente representable en `float32`. Para no perder valores, NumPy elige `float64`. En cambio `int16 + float32 → float32`, porque un `int16` sí cabe.

## Memoria, precisión y `itemsize`

El `itemsize` fija **el coste en memoria** y **la precisión disponible**:

| dtype | itemsize | mantisa | dígitos decimales fiables |
|-------|----------|---------|---------------------------|
| `float16` | 2 | 11 bits | ~3 |
| `float32` | 4 | 24 bits | ~7 |
| `float64` | 8 | 53 bits | ~16 |

Elegir un dtype más estrecho ahorra memoria y ancho de banda de cache, a cambio de rango y precisión. Es un compromiso explícito que se decide al crear el array.

## El peligro de los enteros: overflow silencioso (wrap-around)

Los enteros de ancho fijo **dan la vuelta** al superar su rango, **sin aviso ni excepción**. No hay promoción automática que rescate al acumulador:

```python
arr = np.array([100], dtype=np.int8)   # rango -128..127
arr + 50
# array([-106], dtype=int8)  → 150 da la vuelta (wrap-around), en silencio

u = np.array([250], dtype=np.uint8)    # rango 0..255
u + 10
# array([4], dtype=uint8)    → 260 mod 256 = 4
```

A diferencia del `int` de Python (que crece sin límite), aquí la aritmética es **modular** dentro del `itemsize`.

## Casting: conversión explícita de tipos

`astype` **siempre crea una copia** con el nuevo dtype:

```python
arr = np.array([1.7, 2.9, 3.1])
arr.astype(np.int32)    # [1, 2, 3]  → truncamiento hacia 0, NO redondeo
arr.astype(np.bool_)    # [True, True, True]  → 0 es False, resto True
```

El parámetro `casting` controla **qué conversiones se permiten** en ufuncs y en `astype`, de más estricto a más laxo:

| `casting` | Permite | Ejemplo permitido | Ejemplo rechazado |
|-----------|---------|-------------------|-------------------|
| `'no'` | nada | — | cualquier cambio |
| `'safe'` | solo sin pérdida | `int32 → int64` | `float64 → int32` |
| `'same_kind'` | dentro del kind o ensanchando | `float64 → float32` | `float → int` |
| `'unsafe'` (defecto de `astype`) | todo | `float64 → int8` | — |

```python
a = np.array([1.5, 2.5])
a.astype(np.int32)                      # OK (unsafe por defecto)
a.astype(np.int32, casting='safe')      # TypeError: no es seguro
```

## Ejemplos progresivos

### Nivel 1: declarar el dtype al crear

```python
np.zeros(3, dtype=np.int8)       # [0, 0, 0] en int8
np.ones(3, dtype=np.float32)     # [1., 1., 1.] en float32
np.array([1, 2], dtype=complex)  # [1.+0.j, 2.+0.j]
```

### Nivel 2: el dtype como compromiso memoria/precisión

```python
# Imagen 1000x1000 en escala de grises 0..255
img64 = np.zeros((1000, 1000))             # float64 → 8 MB
img8  = np.zeros((1000, 1000), np.uint8)   # uint8   → 1 MB (8x menos)
```

### Nivel 3: un tensor N-D, float32 frente a float64

```python
t32 = np.ones((100, 100, 100), dtype=np.float32)
t64 = np.ones((100, 100, 100), dtype=np.float64)

t32.nbytes   # 4_000_000  → 4 MB   (1e6 elementos × 4 bytes)
t64.nbytes   # 8_000_000  → 8 MB   (× 8 bytes)

# Precisión: sumar muchos términos pequeños revela la diferencia
x32 = np.full(10**7, 0.1, dtype=np.float32)
x64 = np.full(10**7, 0.1, dtype=np.float64)
x32.sum()    # ~833333.3   → error visible (mantisa de 24 bits se satura)
x64.sum()    # ~1000000.0  → error despreciable
```

Mismo número de elementos, mismo shape `(100, 100, 100)`: el `dtype` decide el doble de memoria y varios órdenes de magnitud de precisión.

## Casos que fallan (errores típicos)

### Error 1: overflow silencioso en enteros pequeños

```python
arr = np.array([60], dtype=np.int8)   # rango -128..127
arr * 3
# array([-76], dtype=int8)  → 180 da la vuelta, sin aviso
# Solución: usar un dtype más ancho (int32/int64) para el acumulador
```

### Error 2: subir a `float64` sin querer al mezclar dtypes

```python
img = np.zeros((1000, 1000), dtype=np.float32)  # 4 MB
img = img + 1.0     # 1.0 es float de Python → resultado float64: 8 MB
# Se duplicó la memoria en silencio.
# Solución: img += np.float32(1.0)  o usar escalares del mismo dtype
```

### Error 3: pérdida de precisión al castear

```python
np.array([3.99]).astype(np.int32)   # array([3])  → trunca, no redondea
# Para redondear: np.round(arr).astype(np.int32)  → array([4])

grande = np.array([2**60], dtype=np.int64)
grande.astype(np.float64).astype(np.int64)
# El valor cambia: float64 no representa exactamente enteros > 2**53
```

### Error 4: dtype `object` que mata el rendimiento

```python
arr = np.array([1, "dos", 3.0])   # dtype('O') → object
# Opera elemento a elemento en Python: se pierde la vectorización
```

### Error 5: comparar flotantes por igualdad exacta

```python
a = np.array([0.1 + 0.2])
a == 0.3              # array([False])  → error de redondeo binario
np.isclose(a, 0.3)   # array([ True])  → forma correcta
```

## Valores especiales de los flotantes

Solo los dtypes flotantes y complejos admiten estos valores:

| Valor | Significado | Cómo detectarlo |
|-------|-------------|-----------------|
| `np.nan` | Not a Number | `np.isnan(arr)` |
| `np.inf` | Infinito positivo | `np.isinf(arr)` |
| `-np.inf` | Infinito negativo | `np.isinf(arr)` |

```python
arr = np.array([1.0, np.nan, np.inf])
np.isnan(arr)   # [False,  True, False]
arr.sum()       # nan  → cualquier operación con nan propaga nan
np.nansum(arr)  # inf  → las variantes nan* ignoran los nan
```

## Relación con otros conceptos

El `dtype` es uno de los tres metadatos que definen un [[concepto_ndarray]] (junto con el shape y los strides), y gobierna la promoción de tipos que aplican las [[concepto_ufuncs]] al combinar arrays.

- [[concepto_ndarray]]
- [[concepto_vectorizacion]]
- [[concepto_shape]]
- [[concepto_ufuncs]]
- [[ndarray.astype]]
- [[ndarray.dtype]]
