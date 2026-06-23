---
title: Broadcasting — Alineación automática de shapes
aliases:
  - broadcasting
  - reglas de broadcasting
tags:
  - numpy
  - concepto
  - transformaciones
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_shape
draft: false
---

# Broadcasting — Alineación automática de shapes

## Definición fundamental

**Broadcasting** es el mecanismo por el cual [[concepto_ndarray|NumPy]] permite operar arrays de distintos [[concepto_shape|shapes]] como si tuvieran la misma forma, **sin copiar datos**. NumPy "estira" virtualmente los ejes de tamaño `1` hasta que las formas coinciden, y entonces aplica la operación elemento a elemento.

Es la pieza que vuelve naturales expresiones como `matriz + vector` o `tabla - media_por_columna`: no hay que materializar la forma común, NumPy la deduce y la recorre con `strides` de paso cero.

## Por qué existe broadcasting

Sin broadcasting, para sumar un vector a cada fila de una matriz habría que materializar la copia:

```python
# Sin broadcasting (tedioso y caro en memoria)
matriz = np.array([[1, 2, 3],
                   [4, 5, 6]])
vector = np.array([10, 20, 30])
vector_tiled = np.tile(vector, (2, 1))  # copia física (2, 3)
resultado = matriz + vector_tiled

# Con broadcasting (directo, sin copia)
resultado = matriz + vector  # NumPy alinea (2,3) con (3,) automáticamente
```

Broadcasting elimina los arrays intermedios explícitos: ahorra memoria, ahorra código y deja el bucle dentro de la [[concepto_ufuncs|ufunc]] compilada en C.

## La regla formal (2 pasos)

Dadas dos shapes, broadcasting decide la forma común aplicando dos pasos, **alineando siempre por la derecha**:

> [!regla] Los 2 pasos
> 1. **Igualar `ndim`:** la shape con menos dimensiones se **rellena con `1` por la IZQUIERDA** hasta tener tantos ejes como la otra.
> 2. **Comparar eje a eje:** en cada eje los tamaños deben ser **iguales**, o **uno de ellos ser `1`** (ese eje se "estira" virtualmente al otro tamaño). Si no, las shapes son incompatibles → `ValueError`.

El tamaño del eje resultante es `max(dim_A, dim_B)` (y como uno es `1` cuando difieren, equivale a "el que no es `1`").

### Visualización: alineación por la derecha

La clave es ver las shapes **pegadas a la derecha**. Un vector `(4,)` NO es una columna: alinea como **fila** en el último eje.

```text
A      (3, 1)
B         (4,)  →  (1, 4)     ← paso 1: rellena con 1 por la izquierda
---------------
eje -1:  1 vs 4  →  4         ← uno es 1, se estira
eje -2:  3 vs 1  →  3         ← uno es 1, se estira
---------------
out    (3, 4)
```

El mismo esquema con un fallo, para fijar la idea de "alinear por la derecha":

```text
A      (3,)
B      (4,)
---------------
eje -1:  3 vs 4  →  ✗  ninguno es 1 y son distintos → ValueError
```

## El mapa de shapes

Broadcasting es una transformación de formas. Para dos arrays `A` y `B`, tras alinear por la derecha y rellenar con `1`:

$$ (a_0,\dots,a_{k}),\ (b_0,\dots,b_{k}) \ \xrightarrow{\ \text{broadcast}\ }\ (\max(a_0,b_0),\,\dots,\,\max(a_k,b_k)) $$

válido **si y solo si** en cada eje $a_i = b_i$ o $a_i = 1$ o $b_i = 1$.

El caso canónico que conviene memorizar es el "producto de mallas" entre una columna y una fila:

$$ (n, 1),\ (1, m)\ \longrightarrow\ (n, m) $$

```text
columna (n,1):  estira el eje -1 (1 → m)
fila    (1,m):  estira el eje -2 (1 → n)
out     (n,m):  cada celda combina la fila i con la columna j
```

### Ejemplo N-D

Un caso 3-D típico: un tensor por lotes `(b, 1, m)` contra un vector columna `(n, 1)`.

```text
A      (b, 1, m)
B         (n, 1)  →  (1, n, 1)
------------------------------
eje -1:  m vs 1   →  m
eje -2:  1 vs n   →  n
eje -3:  b vs 1   →  b
------------------------------
out    (b, n, m)
```

Cada "lámina" `b` produce una malla `(n, m)`: el eje `n` viene de `B`, el eje `m` viene de `A`.

## Ejemplos progresivos

### Nivel 1 — Escalar + array

El escalar se trata como shape vacía, que rellena a `1` en todos los ejes.

```python
import numpy as np

arr = np.array([[1, 2, 3],
                [4, 5, 6]])      # (2, 3)
resultado = arr + 10             # escalar → (1, 1) → (2, 3)
# [[11, 12, 13],
#  [14, 15, 16]]
```

### Nivel 2 — Vector fila + vector columna (la malla)

```python
fila    = np.array([1, 2, 3])    # (3,)  → alinea como (1, 3)
columna = np.array([[10],
                    [20],
                    [30]])       # (3, 1)

resultado = fila + columna       # (3,1) con (1,3) → (3, 3)
# [[11, 12, 13],
#  [21, 22, 23],
#  [31, 32, 33]]
```

| Array | Shape original | Tras alinear | Tras estirar |
|-------|---------------|--------------|--------------|
| fila | `(3,)` | `(1, 3)` | `(3, 3)` |
| columna | `(3, 1)` | `(3, 1)` | `(3, 3)` |
| resultado | — | — | `(3, 3)` |

### Nivel 3 — Tensor 3-D + vector

```python
arr_3d = np.ones((2, 3, 4))      # (2, 3, 4)
vector = np.array([1, 2, 3, 4])  # (4,)

resultado = arr_3d + vector
# vector: (4,) → (1, 1, 4) → (2, 3, 4)
```

El vector `[1,2,3,4]` se suma a lo largo del **último eje** en cada una de las `2×3` filas. Para sumarlo a otro eje habría que insertarle un eje con `np.newaxis` (ver más abajo).

## Casos que fallan

### Fallo 1 — shapes incompatibles (`(3,)` vs `(4,)`)

```python
np.array([1, 2, 3]) + np.array([1, 2, 3, 4])
# eje -1: 3 vs 4 → ninguno es 1 → ValueError
# operands could not be broadcast together with shapes (3,) (4,)
```

### Fallo 2 — creer que `(n,)` alinea como columna

El error más común: esperar que un vector `(3,)` se combine como **columna** con una matriz. Broadcasting alinea **por la derecha**, así que `(3,)` es una **fila** `(1, 3)`.

```python
arr = np.ones((3, 4))
vector = np.array([1, 2, 3])     # (3,) → (1, 3)
arr + vector
# eje -1: 4 vs 3 → ValueError (NO suma por columnas)
```

**Solución:** forzar la forma columna con `np.newaxis`:

```python
arr + vector[:, np.newaxis]      # (3,1) con (3,4) → (3, 4)  ✓
```

### Fallo 3 — eje intermedio incompatible

```python
arr = np.ones((2, 3, 4))
vector = np.array([1, 2])        # (2,) → (1, 1, 2)
arr + vector
# eje -1: 4 vs 2 → ValueError
```

## Memoria y rendimiento

**Broadcasting NO copia datos.** El "estiramiento" se implementa con [[concepto_views_vs_copias|vistas]] cuyos `strides` valen `0` en los ejes estirados: avanzar por ese eje no mueve el puntero, repite el mismo valor.

```python
arr = np.array([1, 2, 3])
col = arr[:, np.newaxis]         # (3, 1)
col.strides                      # (8, 0)  ← stride 0 = repetición sin copia
```

| Método | Memoria extra | Coste |
|--------|---------------|-------|
| Broadcasting | 0 bytes | bucle único en C |
| `np.tile` / arrays explícitos | `n×` elementos | copia + bucle |

## Forzar la forma: `np.newaxis` y `reshape`

`np.newaxis` (alias de `None`) inserta un eje de tamaño `1` en la posición indicada, lo que permite controlar **dónde** se estira:

```python
v = np.array([1, 2, 3])          # (3,)
v[:, np.newaxis]                 # (3, 1)  columna
v[np.newaxis, :]                 # (1, 3)  fila
```

```python
arr = np.ones((4, 4))
vec = np.array([1, 2, 3, 4])     # (4,)
arr + vec                        # suma a cada FILA   (alinea (1,4))
arr + vec[:, np.newaxis]         # suma a cada COLUMNA (fuerza (4,1))
```

## Predecir el shape resultado (ejercicio)

¿Qué shape sale de cada operación? (Pista: rellena con `1` a la izquierda y toma el `max` por eje.)

| A | B | Resultado |
|---|---|-----------|
| `(6, 1)` | `(5,)` | ? |
| `(4, 1, 6)` | `(2, 1, 5)` | ? |
| `(1, 5, 1, 4)` | `(3, 1, 4, 1)` | ? |

**Respuestas:**
1. `(6, 5)` — `(6,1)` con `(1,5)` → `(6,5)`.
2. `(4, 2, 6, 5)` — `(4,1,6,1)` con `(1,2,1,5)` → `(4,2,6,5)`.
3. `(3, 5, 4, 4)` — `(1,5,1,4)` con `(3,1,4,1)` → `(3,5,4,4)`.

## Relación con otros conceptos

- [[concepto_shape]] — la forma sobre la que opera la regla.
- [[concepto_vectorizacion]] — broadcasting es lo que evita el bucle Python.
- [[concepto_ufuncs]] — toda ufunc aplica broadcasting automáticamente.
- [[concepto_ndarray]]
- [[concepto_views_vs_copias]]
- [[np.newaxis]]
- [[np.reshape]]
