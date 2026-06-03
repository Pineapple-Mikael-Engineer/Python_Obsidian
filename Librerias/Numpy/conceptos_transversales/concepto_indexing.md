---
title: Indexing — Acceso y seleccion de elementos
aliases:
  - indexing
  - indexado
  - seleccion
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

# Indexing — Acceso y seleccion de elementos

## Definicion fundamental

El **indexing** es el conjunto de mecanismos para leer o escribir subconjuntos de un [[concepto_ndarray|ndarray]]. NumPy extiende la indexacion de listas de Python con indexacion multidimensional, booleana y por arrays de enteros.

**Caracteristica esencial:** existen dos familias con comportamiento de memoria opuesto. La indexacion **basica** (enteros y slices) devuelve [[concepto_views_vs_copias|vistas]]; la indexacion **avanzada** (booleana y por arrays) devuelve **copias**.

## Por que importa la distincion vista/copia

```python
import numpy as np
arr = np.array([10, 20, 30, 40, 50])

# Basica → vista: modificar afecta al original
sub = arr[1:4]
sub[0] = 99
arr            # [10, 99, 30, 40, 50]  ← cambio el original

# Avanzada → copia: el original queda intacto
sub2 = arr[[1, 2, 3]]
sub2[0] = 0
arr            # [10, 99, 30, 40, 50]  ← sin cambios
```

Confundir ambas es una de las fuentes de bugs mas comunes en NumPy.

## Las tres familias de indexing

| Familia | Sintaxis | Devuelve | Ejemplo |
|---------|----------|----------|---------|
| Basica (entero) | `arr[i]` | vista / escalar | `arr[0]` |
| Basica (slice) | `arr[i:j:k]` | vista | `arr[1:4]` |
| Avanzada (booleana) | `arr[mascara]` | copia | `arr[arr > 0]` |
| Avanzada (fancy) | `arr[lista]` | copia | `arr[[0, 2, 4]]` |

## Indexacion basica: enteros y slices

### En multiples dimensiones

Se separan los indices por coma, **un indice por eje**:

```python
M = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

M[0, 0]     # 1     → fila 0, columna 0
M[1, 2]     # 6     → fila 1, columna 2
M[2]        # [7,8,9]  → fila completa (eje 1 implicito)
M[:, 1]     # [2,5,8]  → columna 1 completa
M[0:2, 1:3] # [[2,3],[5,6]]  → submatriz
```

### Slicing `inicio:fin:paso`

| Slice | Significado |
|-------|-------------|
| `arr[2:5]` | de la posicion 2 a la 4 (fin exclusivo) |
| `arr[:3]` | desde el inicio hasta la 2 |
| `arr[3:]` | desde la 3 hasta el final |
| `arr[::2]` | todos, de 2 en 2 |
| `arr[::-1]` | invertido |
| `arr[-1]` | ultimo elemento |

```python
arr = np.arange(10)   # [0,1,2,3,4,5,6,7,8,9]
arr[2:8:2]            # [2, 4, 6]
arr[::-1]             # [9,8,7,6,5,4,3,2,1,0]
```

## Indexacion booleana (mascaras)

Se selecciona con un array de `bool` de shape compatible. Es la base del filtrado vectorizado.

```python
arr = np.array([1, -2, 3, -4, 5])

mascara = arr > 0       # [True, False, True, False, True]
arr[mascara]            # [1, 3, 5]  → copia con los que cumplen

# Combinar condiciones: & (and), | (or), ~ (not) con parentesis
arr[(arr > 0) & (arr < 5)]   # [1, 3]

# Asignacion condicional (modifica in-place)
arr[arr < 0] = 0        # [1, 0, 3, 0, 5]
```

**Importante:** se usan `&`, `|`, `~`, NO `and`, `or`, `not` (estos fallan con arrays).

## Indexacion fancy (por arrays de enteros)

Se pasa una lista o array de indices; el resultado toma el shape del array de indices.

```python
arr = np.array([10, 20, 30, 40, 50])

arr[[0, 2, 4]]      # [10, 30, 50]
arr[[4, 4, 0]]      # [50, 50, 10]  → puede repetir y reordenar

# En 2D: pares (fila, columna)
M = np.arange(9).reshape(3, 3)
M[[0, 1, 2], [2, 1, 0]]   # [2, 4, 6]  → (0,2),(1,1),(2,0) la diagonal anti
```

## Ejemplos progresivos

### Nivel 1: leer un elemento y una fila

```python
M = np.arange(12).reshape(3, 4)
M[1, 1]   # 5
M[1]      # [4, 5, 6, 7]
```

### Nivel 2: filtrar y reemplazar

```python
datos = np.array([3.2, -1.0, 5.5, -0.3, 8.1])
datos[datos < 0] = np.nan      # marca negativos como nan
positivos = datos[datos > 0]   # copia solo positivos
```

### Nivel 3: seleccion combinada multidimensional

```python
img = np.random.randint(0, 256, (4, 4))

# Poner a 0 todos los pixeles oscuros (< 128)
img[img < 128] = 0

# Tomar las esquinas con fancy indexing
filas = [0, 0, 3, 3]
cols  = [0, 3, 0, 3]
esquinas = img[filas, cols]    # shape (4,)
```

## Casos que fallan (errores tipicos)

### Error 1: usar `and`/`or` con mascaras

```python
arr = np.array([1, 2, 3])
# arr[arr > 0 and arr < 3]
# ValueError: truth value of an array is ambiguous
arr[(arr > 0) & (arr < 3)]   # correcto: & con parentesis
```

### Error 2: asumir que el slice es una copia

```python
arr = np.arange(5)
sub = arr[1:3]    # vista
sub[:] = 0
arr               # [0, 0, 0, 3, 4]  → el original cambio
# Si se necesita independencia: sub = arr[1:3].copy()
```

### Error 3: index out of bounds

```python
arr = np.arange(3)
arr[5]   # IndexError: index 5 is out of bounds for axis 0 with size 3
```

## Tabla resumen: vista vs copia

| Tipo de acceso | Ejemplo | Resultado |
|----------------|---------|-----------|
| Entero / slice | `arr[2]`, `arr[1:4]` | vista |
| Booleano | `arr[arr > 0]` | copia |
| Fancy (lista/array) | `arr[[0, 2]]` | copia |
| Con `.copy()` | `arr[1:4].copy()` | copia explicita |

## Relacion con otros conceptos

- [[concepto_ndarray]]
- [[concepto_shape]]
- [[concepto_views_vs_copias]]
- [[concepto_vectorizacion]]
- [[np.where]]
- [[np.take]]
