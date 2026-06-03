---
title: Shape — La forma dimensional de un array
aliases:
  - shape
  - forma
  - dimensiones
tags:
  - numpy
  - concepto
  - shape
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
draft: false
---

# Shape — La forma dimensional de un array

## Definicion fundamental

El **shape** es una tupla de enteros no negativos que describe cuantos elementos hay en cada dimension de un [[concepto_ndarray|ndarray]]. Es el metadato que convierte un buffer lineal de memoria en una estructura multidimensional navegable.

**Caracteristica esencial:** El shape no almacena datos; describe como interpretar el buffer. El mismo bloque de memoria puede tener distintos shapes sin copiar un solo byte.

## Por que el shape es central

Sin shape, un array seria solo una secuencia plana de numeros. El shape es lo que permite:

```python
import numpy as np

# Mismo buffer [0,1,2,3,4,5], distinta interpretacion
plano = np.arange(6)              # shape (6,)    → vector
matriz = np.arange(6).reshape(2, 3)  # shape (2, 3) → matriz 2×3
tensor = np.arange(6).reshape(1, 2, 3)  # shape (1,2,3) → tensor
```

Toda operacion de NumPy se razona preguntando primero: **que le pasa al shape?**

## Anatomia del shape

| Concepto | Definicion | Atributo | Ejemplo |
|----------|------------|----------|---------|
| Shape | Tupla con tamaño de cada eje | `ndarray.shape` | `(2, 3)` |
| Rank / ndim | Numero de dimensiones | `ndarray.ndim` | `2` |
| Size | Total de elementos | `ndarray.size` | `6` |
| Eje (axis) | Posicion dentro de la tupla shape | — | eje 0, eje 1 |

**Relacion clave:** `ndim == len(shape)` y `size == producto(shape)`.

```python
arr = np.zeros((2, 3, 4))
arr.shape   # (2, 3, 4)
arr.ndim    # 3
arr.size    # 24  → 2*3*4
```

## Lectura del shape por dimensiones

| Shape | ndim | Nombre comun | Interpretacion |
|-------|------|--------------|----------------|
| `()` | 0 | Escalar 0D | Un unico valor, sin ejes |
| `(n,)` | 1 | Vector | `n` elementos en linea |
| `(m, n)` | 2 | Matriz | `m` filas × `n` columnas |
| `(p, m, n)` | 3 | Tensor 3D | `p` matrices de `m`×`n` |
| `(b, c, h, w)` | 4 | Tensor 4D | Tipico en imagenes (batch, canal, alto, ancho) |

**Convencion de ejes (de izquierda a derecha):** el eje 0 es el mas externo (filas), el ultimo eje es el mas interno (columnas / elementos contiguos en C-order).

## La coma en `(n,)` no es opcional

Un punto de confusion frecuente:

| Expresion | Es | Significado |
|-----------|----|-------------|
| `(3)` | un `int` | El numero 3 entre parentesis |
| `(3,)` | una `tuple` | Shape de un vector de 3 elementos |

```python
np.zeros((3,))   # shape (3,)   → vector 1D
np.zeros((3, 1)) # shape (3, 1) → matriz columna
np.zeros((1, 3)) # shape (1, 3) → matriz fila
```

`(3,)`, `(3, 1)` y `(1, 3)` tienen los mismos 3 valores pero **no son intercambiables**: afectan al [[concepto_broadcasting|broadcasting]] y a las operaciones.

## Operaciones que transforman el shape

### Reshape (reinterpreta sin copiar)

`reshape` cambia el shape siempre que `size` se conserve. Suele devolver una [[concepto_views_vs_copias|vista]].

```python
arr = np.arange(12)       # shape (12,)
arr.reshape(3, 4)         # shape (3, 4)
arr.reshape(2, 6)         # shape (2, 6)
arr.reshape(2, 2, 3)      # shape (2, 2, 3)

arr.reshape(5, 2)         # ValueError: no se puede acomodar 12 en 5*2=10
```

### La dimension inferida `-1`

NumPy calcula automaticamente una dimension si se indica `-1`:

```python
arr = np.arange(12)
arr.reshape(3, -1)   # NumPy deduce 4  → (3, 4)
arr.reshape(-1, 2)   # NumPy deduce 6  → (6, 2)
arr.reshape(-1)      # aplana a (12,)
```

Solo se permite **un** `-1` por llamada.

### Tabla de operaciones segun su efecto sobre el shape

| Operacion | Efecto sobre el shape | Ejemplo |
|-----------|----------------------|---------|
| `reshape` | Redistribuye respetando `size` | `(12,) → (3, 4)` |
| `ravel` / `flatten` | Aplana a 1D | `(3, 4) → (12,)` |
| `transpose` / `.T` | Invierte el orden de los ejes | `(3, 4) → (4, 3)` |
| `expand_dims` / `newaxis` | Inserta un eje de tamaño 1 | `(3,) → (1, 3)` |
| `squeeze` | Elimina ejes de tamaño 1 | `(1, 3, 1) → (3,)` |
| Reduccion (`sum`, `mean`) | Colapsa el eje indicado por `axis` | `(2, 3) → (3,)` |

## Ejemplos progresivos

### Nivel 1: inspeccionar y validar

```python
arr = np.array([[1, 2, 3],
                [4, 5, 6]])
arr.shape   # (2, 3)
arr.ndim    # 2

# Validar antes de operar
assert arr.shape == (2, 3)
```

### Nivel 2: añadir y quitar ejes

```python
v = np.array([1, 2, 3])     # shape (3,)

columna = v[:, np.newaxis]  # shape (3, 1)
fila    = v[np.newaxis, :]  # shape (1, 3)

columna.squeeze().shape     # (3,)  → elimina el eje de tamaño 1
```

### Nivel 3: shapes que habilitan broadcasting

```python
A = np.ones((4, 3))   # shape (4, 3)
b = np.ones((3,))     # shape (3,)   → compatible por la derecha

(A + b).shape         # (4, 3)

c = np.ones((4,))     # shape (4,)   → NO alinea con la ultima dim (3)
# A + c → ValueError; arreglar con c[:, np.newaxis] → (4, 1)
```

## Casos que fallan (errores tipicos)

### Error 1: reshape con size incompatible

```python
np.arange(10).reshape(3, 4)
# ValueError: cannot reshape array of size 10 into shape (3,4)
# 3*4 = 12 != 10
```

### Error 2: confundir `(n,)` 1D con `(n, 1)` 2D

```python
v = np.array([1, 2, 3])      # shape (3,)
M = np.ones((3, 3))

M @ v        # OK → resultado shape (3,)
M @ v[:, np.newaxis]  # OK → resultado shape (3, 1) (otra cosa)
```

### Error 3: asumir que `.T` afecta a un vector 1D

```python
v = np.array([1, 2, 3])  # shape (3,)
v.T.shape                # (3,)  → transponer un 1D no hace nada
# Para una columna real: v.reshape(-1, 1) o v[:, np.newaxis]
```

## Shape y memoria

Cambiar el shape con `reshape` normalmente **no mueve datos**: solo reescribe los `strides` y la tupla shape, creando una vista sobre el mismo buffer. Por eso es una operacion barata. La excepcion es cuando el array no es contiguo y el nuevo shape obliga a una copia.

```python
arr = np.arange(12)
vista = arr.reshape(3, 4)
vista[0, 0] = 99
arr[0]   # 99  → comparten memoria
```

## Relacion con otros conceptos

- [[concepto_ndarray]]
- [[concepto_broadcasting]]
- [[concepto_views_vs_copias]]
- [[concepto_axis_parametro]]
- [[np.reshape]]
- [[np.newaxis]]
