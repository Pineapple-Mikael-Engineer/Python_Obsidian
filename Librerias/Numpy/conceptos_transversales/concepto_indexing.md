---
title: Indexing — Acceso y selección de elementos
aliases:
  - indexing
  - indexado
  - selección
  - slicing
tags:
  - numpy
  - concepto
  - indexado
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_shape
draft: false
---

# Indexing — Acceso y selección de elementos

## Definición fundamental

El **indexing** es el conjunto de mecanismos para leer o escribir subconjuntos de un [[concepto_ndarray|ndarray]]. NumPy extiende la indexación de listas de Python con tres familias: indexación **básica** (enteros y slices), **avanzada o fancy** (arrays de enteros) y **booleana** (máscaras). La pieza que de verdad hay que dominar es doble: **qué tipo de memoria devuelve cada familia** y **qué shape tiene el resultado**.

## Por qué importa la distinción

Las tres familias se escriben casi igual (`a[...]`) pero tienen comportamiento de memoria opuesto: la básica devuelve una [[concepto_views_vs_copias|vista]] sobre el mismo buffer; la avanzada y la booleana devuelven **copias** independientes. Confundirlas es una de las fuentes de bugs más comunes en NumPy.

```python
import numpy as np
arr = np.array([10, 20, 30, 40, 50])

# Básica → vista: modificar afecta al original
sub = arr[1:4]
sub[0] = 99
arr            # [10, 99, 30, 40, 50]  ← cambió el original

# Avanzada → copia: el original queda intacto
sub2 = arr[[1, 2, 3]]
sub2[0] = 0
arr            # [10, 99, 30, 40, 50]  ← sin cambios
```

## La regla central

La regla mínima a memorizar relaciona **familia → memoria → quién dicta el shape**:

| Familia | Sintaxis | Devuelve | Shape del resultado lo dicta |
|---------|----------|----------|------------------------------|
| **Básica** (enteros/slices) | `a[1:3, :]`, `a[0]` | **vista** | el propio array y los slices |
| **Avanzada / fancy** (arrays de enteros) | `a[[0, 2]]`, `a[idx_f, idx_c]` | **copia** | los **arrays de índices** (se broadcastean entre sí) |
| **Booleana** (máscara) | `a[a > 0]` | **copia** | el número de `True` de la máscara |

> [!regla] El núcleo del fancy indexing
> En la indexación básica, el shape de salida se deduce del array original (cuántos ejes quedan tras aplicar slices). En la **avanzada**, el shape lo dictan los **arrays de índices**, no el array original. Esto es lo que más confunde, y se explica en el mapa de shapes.

## El mapa de shapes del fancy indexing

Cuando se indexa con un array de índices por eje, NumPy **broadcastea los arrays de índices entre sí** y el shape del resultado es el shape (broadcasteado) de esos índices. El array original solo aporta los **valores**, no la forma:

$$ a[\,\mathbf{i},\ \mathbf{j}\,] \quad\text{con}\quad \mathbf{i},\mathbf{j}\ \text{de shape}\ (p, q)\ \longrightarrow\ \text{resultado de shape}\ (p, q) $$

$$ \text{resultado}[u, v] \;=\; a[\,\mathbf{i}[u,v],\ \mathbf{j}[u,v]\,] $$

Es decir, por cada posición `(u, v)` de los arrays de índices se recoge **un** elemento de `a`; el resultado tiene exactamente la forma de los índices.

```python
a = np.arange(12).reshape(3, 4)
# [[ 0,  1,  2,  3],
#  [ 4,  5,  6,  7],
#  [ 8,  9, 10, 11]]

idx_filas = np.array([[0, 0],
                      [2, 2]])   # shape (2, 2)
idx_cols  = np.array([[1, 3],
                      [0, 2]])   # shape (2, 2)

a[idx_filas, idx_cols]
# recoge a[0,1], a[0,3], a[2,0], a[2,2]
# [[ 1,  3],
#  [ 8, 10]]   ← shape (2, 2), el de los índices, NO el de a
```

Si los arrays de índices tienen shapes distintos pero compatibles, se aplica [[concepto_broadcasting|broadcasting]] entre ellos antes de recoger:

```python
filas = np.array([[0], [2]])    # shape (2, 1)
cols  = np.array([1, 3])        # shape (2,)  → broadcast a (2, 2)
a[filas, cols]
# (2,1) y (2,) → (2,2): recoge a[0,1],a[0,3],a[2,1],a[2,3]
# [[ 1,  3],
#  [ 9, 11]]
```

## El mapa de shapes de la máscara booleana

Una máscara booleana `mask` con el mismo shape que `a` **aplana a 1D** los elementos donde `mask` es `True`. El shape del resultado es siempre 1D, con tantos elementos como `True` haya:

$$ a[\text{mask}] \longrightarrow \text{shape}\ \big(\texttt{mask.sum()},\big) $$

```python
a = np.arange(12).reshape(3, 4)
mask = a % 3 == 0       # múltiplos de 3
mask.sum()              # 4
a[mask]                 # [0, 3, 6, 9]  → shape (4,), 1D
```

Una máscara con menos ejes que `a` selecciona **a lo largo de los primeros ejes**: `a[mask_filas]` con `mask_filas` de shape `(3,)` elige filas completas.

## Ejemplos progresivos

### Nivel 1: básica — un elemento, una fila, una submatriz

Se separan los índices por coma, **un índice por eje**:

```python
M = np.arange(12).reshape(3, 4)
M[1, 1]     # 5            → escalar
M[1]        # [4,5,6,7]    → fila completa (eje 1 implícito)
M[:, 1]     # [1,5,9]      → columna 1 completa
M[0:2, 1:3] # [[1,2],[5,6]]→ submatriz, todo vistas
```

Slicing `inicio:fin:paso`:

```python
arr = np.arange(10)   # [0,1,2,3,4,5,6,7,8,9]
arr[2:8:2]            # [2, 4, 6]
arr[::-1]             # [9,8,7,6,5,4,3,2,1,0]  (invertido, sigue siendo vista)
```

### Nivel 2: booleana — filtrar y reemplazar

```python
arr = np.array([1, -2, 3, -4, 5])

mascara = arr > 0            # [True, False, True, False, True]
arr[mascara]                 # [1, 3, 5]  → copia 1D

# Combinar condiciones con &, |, ~ y paréntesis (NUNCA and/or/not)
arr[(arr > 0) & (arr < 5)]   # [1, 3]

# Asignación condicional (modifica in-place)
arr[arr < 0] = 0             # [1, 0, 3, 0, 5]
```

### Nivel 3: fancy — recoger, repetir y reordenar

```python
arr = np.array([10, 20, 30, 40, 50])
arr[[0, 2, 4]]      # [10, 30, 50]
arr[[4, 4, 0]]      # [50, 50, 10]  → puede repetir y reordenar

# Diagonal antidiagonal de una matriz 3×3
M = np.arange(9).reshape(3, 3)
M[[0, 1, 2], [2, 1, 0]]   # [2, 4, 6]  → recoge (0,2),(1,1),(2,0)
```

### Nivel 4: N-D — indexar un tensor `(b, n, m)`

En un tensor de lotes `(b, n, m)`, fancy indexing sobre el primer eje selecciona **planos completos**, y el shape de salida concatena el shape de los índices con los ejes que sobreviven:

$$ a\ \text{de shape}\ (b, n, m),\quad \mathbf{i}\ \text{de shape}\ (k,)\ \Longrightarrow\ a[\mathbf{i}]\ \text{tiene shape}\ (k, n, m) $$

```python
a = np.arange(24).reshape(2, 3, 4)   # 2 lotes de 3×4

# Reordenar / duplicar lotes
a[[1, 0, 1]].shape        # (3, 3, 4)  ← (k, n, m)

# Un elemento por lote: índices de fila y columna por cada lote
lote = np.array([0, 1])               # shape (2,)
fila = np.array([0, 2])               # shape (2,)
col  = np.array([3, 1])               # shape (2,)
a[lote, fila, col]        # [3, 21]   → shape (2,), recoge a[0,0,3] y a[1,2,1]
```

### Nivel 5: combinación básico + avanzado

Al mezclar un slice (básico) con un array de índices (avanzado), el eje del slice **se mantiene** y el eje fancy aporta su shape:

```python
a = np.arange(12).reshape(3, 4)
a[:, [0, 2]]              # todas las filas, columnas 0 y 2
# [[ 0,  2],
#  [ 4,  6],
#  [ 8, 10]]   → shape (3, 2)
```

## Casos que fallan (errores típicos)

### Error 1: esperar que fancy indexing sea una vista

```python
arr = np.arange(5)
sub = arr[[1, 2]]    # COPIA, no vista
sub[0] = 999
arr                  # [0, 1, 2, 3, 4]  → el original NO cambió
```

### Error 2: `a[i][j] = x` no modifica si `a[i]` es copia

El acceso encadenado evalúa `a[i]` primero; si `i` es fancy/booleano, eso ya es una copia temporal y la asignación se pierde:

```python
a = np.arange(12).reshape(3, 4)
a[[0, 1]][:, 0] = 99     # a[[0,1]] es copia → la asignación se descarta
a[:, 0]                  # [0, 4, 8]  → sin cambios

# Correcto: un solo indexado que NumPy puede asignar in-place
a[[0, 1], 0] = 99
a[:, 0]                  # [99, 99, 8]
```

### Error 3: mezclar slice y fancy y sorprenderse del shape

Cuando los ejes fancy **no son contiguos** (hay un slice en medio), NumPy mueve el eje de resultado del broadcasting al frente, y el shape deja de ser intuitivo:

```python
a = np.arange(24).reshape(2, 3, 4)
a[[0, 1], :, [0, 3]].shape    # (2, 3), NO (2, 3, 2)
# los dos arrays fancy se broadcastean a (2,) y el slice ':' queda detrás
```

### Error 4: usar `and`/`or` con máscaras

```python
arr = np.array([1, 2, 3])
# arr[(arr > 0) and (arr < 3)]
# ValueError: truth value of an array is ambiguous
arr[(arr > 0) & (arr < 3)]   # correcto: & con paréntesis
```

### Error 5: índice fuera de rango

```python
arr = np.arange(3)
arr[5]   # IndexError: index 5 is out of bounds for axis 0 with size 3
```

## Relación con otros conceptos

- [[concepto_views_vs_copias]]
- [[concepto_shape]]
- [[concepto_broadcasting]]
- [[concepto_ndarray]]
- [[concepto_vectorizacion]]
- [[np.where]]
- [[np.take]]
