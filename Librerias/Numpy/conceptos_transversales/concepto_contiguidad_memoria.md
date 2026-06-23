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

## Definición fundamental

El buffer de un [[concepto_ndarray|array]] es **lineal**: una secuencia plana de bytes. La **contigüidad** describe en qué **orden** se colocan en ese buffer los elementos de un array N-D. Es ortogonal al [[concepto_dtype|dtype]]:

- el **dtype** dice **cómo leer** cada elemento (cuántos bytes y cómo interpretarlos),
- la **contigüidad** dice **en qué orden** están los elementos en el buffer.

Un array es **contiguo** si sus elementos ocupan un bloque sin huecos y en un orden predecible. Hay dos órdenes canónicos:

- **C-order (row-major):** los elementos de la **última** dimensión son los más juntos en memoria.
- **F-order (column-major):** los elementos de la **primera** dimensión son los más juntos.

## Por qué existe: el array N-D no es físicamente N-D

La memoria es unidimensional, pero pensamos los arrays como rejillas N-D. Hace falta una **convención** que aplane los índices `(i, j, k, …)` a un único offset en bytes. C y Fortran eligieron convenciones opuestas, y NumPy las soporta ambas para poder **interoperar** con código de ambos mundos sin copiar.

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])

# C-order  (defecto): buffer = [1, 2, 3, 4, 5, 6]
#   se recorre fila 0 (1,2,3), luego fila 1 (4,5,6)

arr_f = np.array([[1, 2, 3],
                  [4, 5, 6]], order='F')
# F-order: buffer = [1, 4, 2, 5, 3, 6]
#   se recorre columna 0 (1,4), columna 1 (2,5), columna 2 (3,6)
```

## La regla / el modelo: strides y la fórmula del offset

Los **strides** son el mecanismo que conecta el índice N-D con el buffer: `strides[k]` es el **número de bytes** que hay que saltar para avanzar **una posición en el eje `k`**. El offset en bytes de un elemento es el producto índice·stride sumado sobre todos los ejes:

$$ \text{offset}(i_0,\dots,i_{k}) \;=\; \sum_{p=0}^{k} i_p \cdot \text{strides}[p] $$

Para un array **C-contiguo** de shape $(n_0,\dots,n_k)$ y `itemsize` $s$, los strides salen del producto de las dimensiones **a la derecha** de cada eje:

$$ \text{strides}[p] \;=\; s \cdot \prod_{q>p} n_q $$

El último eje tiene el **stride menor** ($s$), es decir es el que está contiguo. En F-order es al revés: el stride menor lo tiene el **primer** eje, y se acumula hacia la izquierda ($\text{strides}[p] = s \cdot \prod_{q<p} n_q$).

```python
arr = np.arange(12).reshape(3, 4)   # C-order, dtype int64 → itemsize 8
# strides[1] = 8           (avanzar una columna = 1 elemento)
# strides[0] = 4 * 8 = 32  (avanzar una fila = saltar 4 elementos)
arr.strides                          # (32, 8)

arr_f = np.arange(12).reshape(3, 4, order='F')
# strides[0] = 8           (avanzar una fila = 1 elemento)
# strides[1] = 3 * 8 = 24  (avanzar una columna = saltar 3 elementos)
arr_f.strides                        # (8, 24)
```

### Strides en vistas no contiguas

Slicing y transpuesta producen **vistas**: NumPy ajusta los strides sin tocar el buffer ([[concepto_views_vs_copias|vistas vs copias]]).

```python
arr = np.arange(12).reshape(3, 4)

columna = arr[:, 1]                  # una columna: salta de fila en fila
columna.strides                      # (32,)
columna.flags['C_CONTIGUOUS']        # False  → hay huecos en memoria

cada_2 = arr[::2, ::2]               # paso 2 en ambos ejes
cada_2.strides                       # (64, 16)
```

## La transpuesta invierte los strides

`a.T` no mueve ni un byte: **invierte el orden de los ejes y, con ellos, los strides**. Por eso la transpuesta de un array C-contiguo queda **F-contigua** (y viceversa):

```python
arr = np.arange(12).reshape(3, 4)
arr.strides                # (32, 8)   C-contiguo
arr.T.strides              # (8, 32)   strides invertidos → F-contiguo
arr.T.flags['C_CONTIGUOUS'] # False
arr.T.flags['F_CONTIGUOUS'] # True
```

## Cuándo `reshape` es vista y cuándo copia

`reshape` reinterpreta el **orden lógico** de los elementos (por defecto en C-order). Puede devolver una **vista** solo si el nuevo shape se puede expresar con strides sobre el buffer **existente**; si no, **fuerza una copia**. La condición práctica:

| Situación | `reshape` devuelve |
|-----------|--------------------|
| Array C-contiguo, reshape en C-order | **Vista** |
| Array F-contiguo, reshape con `order='F'` | **Vista** |
| Array no contiguo (p. ej. tras `.T` o slicing con pasos) | **Copia** |

```python
arr = np.arange(12).reshape(3, 4)    # C-contiguo

arr.reshape(12)          # VISTA  → el orden C ya coincide con el buffer
arr.T.reshape(12)        # COPIA  → la T es F-contigua; aplanar en C reordena
```

`np.ascontiguousarray` fuerza una versión C-contigua (copiando solo si hace falta); `np.asfortranarray` hace lo análogo en F.

## Por qué importa la contigüidad

1. **Interoperar con C/Fortran.** Muchas extensiones esperan un buffer C-contiguo (o F-contiguo) concreto. Pasar una vista no contigua produce una copia oculta o un error.
2. **Rendimiento al iterar.** Recorrer el eje de stride menor explota la **localidad de cache**: el CPU carga bloques secuenciales. Recorrer un eje de stride grande salta por memoria y desperdicia cache.
3. **Diagnóstico.** `arr.flags['C_CONTIGUOUS']` / `['F_CONTIGUOUS']` revelan el layout antes de operar.

```python
arr = np.arange(12).reshape(3, 4)
arr.flags['C_CONTIGUOUS']    # True
arr.flags['F_CONTIGUOUS']    # False

def funcion_c(buf):
    # Espera buf.flags['C_CONTIGUOUS'] == True
    ...

v = arr.T                                  # no C-contiguo
funcion_c(np.ascontiguousarray(v))         # copia solo si hace falta
```

## Ejemplos progresivos

### Nivel 1: matriz 2×3, los dos órdenes

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
arr.flags['C_CONTIGUOUS']   # True   → buffer [1,2,3,4,5,6]

arr_f = np.asfortranarray(arr)
arr_f.flags['F_CONTIGUOUS'] # True   → buffer [1,4,2,5,3,6]
```

### Nivel 2: transponer cambia el layout, no los datos

```python
arr = np.random.rand(1000, 1000)
arr_t = arr.T

arr_t.flags['F_CONTIGUOUS']  # True   → la T es F-contigua
arr_t.flags['C_CONTIGUOUS']  # False

# Si lo que sigue espera C-contiguo, materialízalo una vez:
arr_t_c = np.ascontiguousarray(arr_t)   # ahora C-contiguo (con copia)
```

### Nivel 3: un tensor `(2, 3, 4)`, su `.T` y un reshape que copia

```python
t = np.arange(24).reshape(2, 3, 4)   # C-contiguo, itemsize 8
t.strides              # (96, 32, 8)   = (3*4*8, 4*8, 8)
t.flags['C_CONTIGUOUS'] # True

tt = t.T               # shape (4, 3, 2): ejes y strides invertidos
tt.strides             # (8, 32, 96)
tt.flags['F_CONTIGUOUS'] # True
tt.flags['C_CONTIGUOUS'] # False

# reshape de la transpuesta a 1-D en C-order: no encaja en el buffer → COPIA
plano = tt.reshape(24)
np.may_share_memory(t, plano)   # False  → se copió

# reshape del original: el orden C ya coincide → VISTA
vista = t.reshape(6, 4)
np.may_share_memory(t, vista)   # True
```

## Casos que fallan (errores típicos)

### Error 1: asumir que `reshape` nunca copia

```python
arr = np.arange(12).reshape(3, 4)
plano = arr.T.reshape(12)          # COPIA silenciosa (la T no es C-contigua)
plano[0] = 999
arr[0, 0]                          # 0  → modificar 'plano' NO toca 'arr'
# Si esperabas una vista, el cambio se pierde. Verifica con may_share_memory.
```

### Error 2: pasar un array no contiguo a una librería C

```python
arr = np.random.rand(100, 100).T   # F-contiguo, no C-contiguo
# Una extensión que asume C-order leerá los bytes en el orden equivocado
# o disparará una copia oculta en cada llamada.
arr_c = np.ascontiguousarray(arr)  # materializa C-contiguo una sola vez
```

### Error 3: iterar por el eje de stride grande

```python
arr_c = np.random.rand(2000, 2000)   # C-contiguo
arr_c.sum(axis=1)   # rápido: recorre el último eje (stride menor)
arr_c.sum(axis=0)   # más lento: salta de fila en fila (stride mayor)
# Si vas a operar muchas veces por columnas, considera un layout F-contiguo.
```

## Tabla resumen de contigüidad por operación

| Operación | Resultado contiguo | Vista o copia |
|-----------|--------------------|---------------|
| `np.array(..., order='C')` | C-contiguo | — |
| `np.array(..., order='F')` | F-contiguo | — |
| `arr.reshape(...)` | depende del original | vista si encaja, si no copia |
| `arr.T` | invierte (C↔F) | siempre vista |
| `arr[::2]` | no contiguo | vista |
| `arr.copy()` | C-contiguo | copia |
| `arr.copy(order='F')` | F-contiguo | copia |
| `arr.flatten()` | C-contiguo | siempre copia |
| `np.ascontiguousarray(arr)` | C-contiguo | copia solo si hace falta |
| `np.asfortranarray(arr)` | F-contiguo | copia solo si hace falta |

## Relación con otros conceptos

La contigüidad es la cara física de los strides de un [[concepto_ndarray]], y determina si una operación de reforma puede devolver una vista o se ve forzada a copiar ([[concepto_views_vs_copias]]).

- [[concepto_ndarray]]
- [[concepto_views_vs_copias]]
- [[concepto_dtype]]
- [[np.reshape]]
- [[np.ravel]]
- [[ndarray.flatten]]
- [[ndarray.flags]]
- [[ndarray.strides]]
- [[np.transpose]]
- [[np.ascontiguousarray]]
- [[np.asfortranarray]]
