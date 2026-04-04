---
title: Contiguidad de Memoria — Orden C, Orden F y strides
aliases:
  - contiguidad
  - C-order
  - F-order
  - row-major
  - column-major
  - strides
tags:
  - numpy
  - concepto
  - memoria
  - rendimiento
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
draft: false
---

# Contiguidad de Memoria — Orden C, Orden F y strides

## Definicion fundamental

La contiguidad de memoria en NumPy se refiere a como estan dispuestos los elementos de un [[concepto_ndarray|array]] en el buffer lineal de memoria. Un array es **contiguo** si sus elementos se almacenan en un bloque sin interrupciones y en un orden predecible.

Existen dos ordenes principales:
- **C-order (row-major)**: Los elementos de la ultima dimension son contiguos
- **F-order (column-major)**: Los elementos de la primera dimension son contiguos

## Comparacion entre C-order y F-order

| Caracteristica | C-order (row-major) | F-order (column-major) |
|----------------|---------------------|------------------------|
| Tambien llamado | Orden por filas | Orden por columnas |
| Dimension contigua | Ultima dimension | Primera dimension |
| Orden por defecto | SI (NumPy) | NO |
| Compatible con | C, C++ | Fortran, MATLAB |
| Strides tipicos | `(m*itemsize, itemsize)` | `(itemsize, n*itemsize)` |

### Visualizacion para matriz 2×3

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

# C-order: buffer = [1, 2, 3, 4, 5, 6]
# Recorrido: fila 0 (1,2,3), luego fila 1 (4,5,6)

# F-order: buffer = [1, 4, 2, 5, 3, 6]
arr_f = np.array([[1, 2, 3],
                  [4, 5, 6]], order='F')
# Recorrido: columna 0 (1,4), luego columna 1 (2,5), luego columna 2 (3,6)
```

## El rol de los strides

Los **strides** son el mecanismo interno que NumPy usa para navegar por el buffer de memoria.

### Definicion

Un stride es el numero de bytes que hay que saltar en el buffer para avanzar una posicion en una dimension determinada.

### Calculo de strides para array contiguo

```python
arr = np.arange(12).reshape(3, 4)
# shape = (3, 4)
# dtype = int64 → itemsize = 8 bytes

# Para C-order:
# strides[1] = itemsize = 8 (avanzar en columnas)
# strides[0] = shape[1] * itemsize = 4 * 8 = 32 (avanzar en filas)

print(arr.strides)  # (32, 8)

# Para F-order:
arr_f = np.arange(12).reshape(3, 4, order='F')
# strides[0] = itemsize = 8 (avanzar en filas)
# strides[1] = shape[0] * itemsize = 3 * 8 = 24 (avanzar en columnas)

print(arr_f.strides)  # (8, 24)
```

### Strides en arrays no contiguos (vistas)

Cuando se crea una vista mediante slicing o transpuesta, NumPy ajusta los strides sin copiar datos. Este es el mecanismo fundamental que permite las [[concepto_views_vs_copias|vistas]] eficientes.

```python
arr = np.arange(12).reshape(3, 4)

# Tomar una columna (no contigua en C-order)
columna = arr[:, 1]
print(columna.strides)  # (32,)
print(columna.flags.c_contiguous)  # False

# Tomar cada 2 elementos
cada_2 = arr[::2, ::2]
print(cada_2.strides)  # (64, 16)
```

## Flags de contiguidad

NumPy proporciona flags para verificar la contiguidad de un array:

| Flag | Significado |
|------|-------------|
| `arr.flags.c_contiguous` (C) | Array es contiguo en C-order |
| `arr.flags.f_contiguous` (F) | Array es contiguo en F-order |
| `arr.flags.contiguous` | Es C-contiguous (alias) |

```python
arr = np.arange(12).reshape(3, 4)
print(arr.flags.c_contiguous)  # True
print(arr.flags.f_contiguous)  # False

arr_t = arr.T
print(arr_t.flags.c_contiguous)  # False
print(arr_t.flags.f_contiguous)  # True

arr_f = np.arange(12).reshape(3, 4, order='F')
print(arr_f.flags.c_contiguous)  # False
print(arr_f.flags.f_contiguous)  # True
```

## Por que la contiguidad importa

### 1. Rendimiento de operaciones

Las operaciones son mas rapidas en arrays contiguos porque el CPU puede cargar bloques de memoria secuencialmente (cache locality).

```python
import time

arr_c = np.random.rand(1000, 1000)
arr_f = np.random.rand(1000, 1000).copy(order='F')

# Suma por filas (optimo para C-order)
inicio = time.time()
for i in range(1000):
    arr_c[i, :] + 1
print(f"C-order: {time.time() - inicio:.4f} seg")

# Suma por columnas (suboptimo para C-order)
inicio = time.time()
for i in range(1000):
    arr_c[:, i] + 1
print(f"C-order (columnas): {time.time() - inicio:.4f} seg")
```

### 2. Operaciones que requieren contiguidad

| Operacion | Requiere contiguidad | Comportamiento si no es contiguo |
|-----------|---------------------|--------------------------------|
| reshape (vista) | SI | Crea copia |
| ravel (vista) | SI | Crea copia |
| transpose | NO | Crea vista (cambia strides) |
| flatten | NO | Siempre crea copia |

### 3. Compatibilidad con otras librerias

```python
def funcion_c(arr):
    # Espera arr.flags.c_contiguous == True
    pass

arr = np.random.rand(100, 100).T
print(arr.flags.c_contiguous)  # False

arr_contiguo = np.ascontiguousarray(arr)
print(arr_contiguo.flags.c_contiguous)  # True
```

## Como cambiar la contiguidad

### `np.ascontiguousarray` y `np.asfortranarray`

```python
arr = np.random.rand(100, 100)

arr_c = np.ascontiguousarray(arr)
print(arr_c.flags.c_contiguous)  # True

arr_f = np.asfortranarray(arr)
print(arr_f.flags.f_contiguous)  # True
```

### `copy` con orden especifico

```python
arr = np.random.rand(100, 100).T

arr_c = arr.copy(order='C')
print(arr_c.flags.c_contiguous)  # True

arr_f = arr.copy(order='F')
print(arr_f.flags.f_contiguous)  # True
```

## Casos practicos

### Caso 1: Transponer y luego operar

```python
arr = np.random.rand(1000, 1000)
arr_t = arr.T

# Si la operacion siguiente espera C-contiguous
resultado = np.sum(arr_t, axis=0)

# Mejor: forzar contiguidad antes
arr_t_contiguo = np.ascontiguousarray(arr_t)
resultado = np.sum(arr_t_contiguo, axis=0)
```

### Caso 2: Reshape despues de transponer

```python
arr = np.arange(12).reshape(3, 4)
arr_t = arr.T  # Shape (4, 3), F-contiguous

# Esto crea copia (reshape no puede usar vista no contigua)
copia = arr_t.reshape(12)

# Esto es vista (contiguo)
vista = arr.reshape(12)
```

### Caso 3: Indexado con pasos

```python
arr = np.arange(1000000)
pasos = arr[::10]  # No contiguo (strides = 80 bytes)

# Operaciones sobre pasos pueden ser mas lentas
print(pasos.flags.c_contiguous)  # False

# Forzar contiguidad si se opera muchas veces
pasos_contiguo = pasos.copy()
```

## Deteccion de problemas de contiguidad

### Verificar antes de operaciones criticas

```python
def operacion_optimizada(arr):
    if not arr.flags.c_contiguous:
        arr = np.ascontiguousarray(arr)
    return arr * 2
```

### Usar `np.may_share_memory` para depurar

```python
arr = np.arange(100)
vista = arr[::2]
copia = vista.copy()

print(np.may_share_memory(arr, vista))  # True
print(np.may_share_memory(arr, copia))  # False
```

## Tabla resumen de contiguidad por operacion

| Operacion | Resultado contiguo? | Nota |
|-----------|--------------------|------|
| `np.array(..., order='C')` | C-contiguous | Por defecto |
| `np.array(..., order='F')` | F-contiguous | Especificar order |
| `arr.reshape()` | Si (si fue posible vista) | Depende del original |
| `arr.T` | Invierte contiguidad | C→F, F→C |
| `arr[::2]` | No contiguo | Strides > itemsize |
| `arr.copy()` | C-contiguous | Por defecto |
| `arr.copy(order='F')` | F-contiguous | Especificar |
| `arr.flatten()` | C-contiguous | Siempre |
| `np.ascontiguousarray()` | C-contiguous | Fuerza conversion |

## Relacion con otros conceptos

- [[concepto_ndarray]]
- [[concepto_views_vs_copias]]
- [[np.reshape]]
- [[np.ravel]]
- [[ndarray.flatten]]
- [[ndarray.flags]]
- [[ndarray.strides]]
- [[ndarray.itemsize]]
- [[concepto_dtype_sistema]]
- [[np.transpose]]
- [[np.ascontiguousarray]]
- [[np.asfortranarray]]
