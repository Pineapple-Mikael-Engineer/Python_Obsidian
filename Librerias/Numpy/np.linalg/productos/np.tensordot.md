---
title: np.tensordot — contrae los ejes especificados de dos tensores
aliases:
  - tensordot
  - np.tensordot
  - producto tensorial contraído
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np
tipo: funcion
retorna: ndarray | escalar
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.tensordot — contrae los ejes especificados de dos tensores

`np.tensordot` es la **contracción general** de dos tensores: tú eliges qué ejes de `a` se emparejan
con qué ejes de `b`, NumPy los **multiplica y suma sobre ellos**, haciéndolos desaparecer. Es la
generalización de `dot`/`inner`/[[np.matmul]] a un número arbitrario de ejes contraídos: donde
`matmul` siempre contrae la dimensión interior, `tensordot` contrae **los ejes que tú especifiques**
mediante el parámetro `axes`. La salida son los **ejes libres de `a` seguidos de los ejes libres de
`b`**.

## La idea en una fórmula

Contraer significa: tomar $N$ ejes de `a` y $N$ ejes de `b` del **mismo tamaño**, alinearlos,
multiplicar y **sumar sobre ellos**. Los ejes contraídos $c_1\dots c_N$ aparecen en el sumatorio y
**desaparecen** del resultado; los ejes no contraídos (libres) sobreviven.

**El mapa de shapes** — la salida es la concatenación de los ejes libres de `a` con los de `b`:

$$
(\underbrace{n_0,\dots,n_{r-1}}_{a\ \text{libres}},\, c_1\dots c_N)\ ,\ (c_1\dots c_N,\, \underbrace{m_0,\dots,m_{s-1}}_{b\ \text{libres}})\ \longrightarrow\ (\underbrace{n_0,\dots,n_{r-1}}_{a\ \text{libres}},\, \underbrace{m_0,\dots,m_{s-1}}_{b\ \text{libres}})
$$

La fórmula por índices, con los ejes libres $i$ de `a` y $j$ de `b`, sumando sobre los ejes
contraídos $k_1,\dots,k_N$:

$$
C_{\,i,\,j} \;=\; \sum_{k_1}\cdots\sum_{k_N} a_{\,i,\,k_1\dots k_N}\; b_{\,k_1\dots k_N,\,j}
$$

> [!important] Los ejes contraídos deben coincidir en tamaño
> Si emparejas el eje $p$ de `a` con el eje $q$ de `b`, hace falta `a.shape[p] == b.shape[q]`.
> El orden importa: `axes=([1,2],[0,1])` empareja `a`-eje-1 con `b`-eje-0 y `a`-eje-2 con `b`-eje-1,
> **en ese orden**.

Visualmente, contraer el último eje de $A_{(2\times 3)}$ con el primero de $B_{(3\times 2)}$
(`axes=([1],[0])`, que es justo el producto matricial) suma sobre la dimensión $3$:

$$
A = \begin{bmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \end{bmatrix} \ (2\times3)
\qquad
B = \begin{bmatrix} b_{00} & b_{01} \\ b_{10} & b_{11} \\ b_{20} & b_{21} \end{bmatrix} \ (3\times2)
$$

$$
\begin{aligned}
c_{00} &= a_{00}b_{00} + a_{01}b_{10} + a_{02}b_{20} \\
c_{01} &= a_{00}b_{01} + a_{01}b_{11} + a_{02}b_{21}
\end{aligned}
\qquad (\text{suma sobre } k=0,1,2)
$$

El resultado $(2\times2)$: el eje contraído de tamaño $3$ desaparece.

## Firma

```python
np.tensordot(a, b, axes=2) -> ndarray
#   a, b : array_like     → los dos tensores
#   axes : int | (seq, seq)
#          - int N        → contrae los últimos N ejes de a con los primeros N de b
#          - (a_axes, b_axes) → empareja explícitamente esos ejes (mismo orden)
```

## Los parámetros en detalle

### `a`, `b` — los operandos
Los dos tensores a contraer. No tienen por qué tener el mismo rango; lo único obligatorio es que los
**ejes emparejados** por `axes` coincidan en tamaño. Se convierten a `ndarray` si no lo son.

### `axes` — qué ejes se contraen (el parámetro central)
Define **qué se suma**. Tiene dos formas:

- **Entero `N`** — contrae los **últimos `N` ejes de `a`** con los **primeros `N` ejes de `b`**, en
  orden. Es el atajo. `axes=2` (el defecto) contrae los dos últimos de `a` con los dos primeros de
  `b`.

  ```python
  a = np.ones((3, 4, 5))
  b = np.ones((4, 5, 6))
  np.tensordot(a, b, axes=2).shape   # (3, 6) → contrae (4,5) de a con (4,5) de b
  ```

- **Par de secuencias `([ejes_a], [ejes_b])`** — empareja explícitamente. `axes=([1,2],[0,1])`
  empareja `a`-eje-1↔`b`-eje-0 y `a`-eje-2↔`b`-eje-1. Da control total sobre **qué eje contra
  cuál** y en qué orden, sin tener que reordenar los tensores antes.

  ```python
  np.tensordot(a, b, axes=([1, 2], [0, 1])).shape   # (3, 6) → idéntico, pero explícito
  ```

> [!tip] El entero es un caso particular del par
> `axes=N` equivale a `axes=(range(-N, 0), range(0, N))`: los últimos `N` de `a` contra los primeros
> `N` de `b`. Si necesitas otro emparejamiento, usa el par de listas.

## El caso N-D

`tensordot` es **intrínsecamente N-D**: su razón de ser es contraer varios ejes a la vez. La regla
mecánica para predecir el shape de salida:

1. Quita de `a.shape` los ejes listados en `axes[0]` → quedan los **libres de `a`**.
2. Quita de `b.shape` los ejes listados en `axes[1]` → quedan los **libres de `b`**.
3. La salida es `(*libres_a, *libres_b)`.

| `a.shape` | `b.shape` | `axes` | salida | qué contrae |
|-----------|-----------|--------|--------|-------------|
| `(m, k)` | `(k, n)` | `1` | `(m, n)` | el eje `k` → **producto matricial** |
| `(k,)` | `(k,)` | `1` | `()` escalar | producto punto |
| `(3, 4, 5)` | `(4, 5, 6)` | `([1,2],[0,1])` | `(3, 6)` | los ejes `4` y `5` |
| `(3, 4, 5)` | `(4, 5, 6)` | `2` | `(3, 6)` | últimos 2 de `a`, primeros 2 de `b` |
| `(2, 3)` | `(4, 5)` | `0` | `(2, 3, 4, 5)` | **nada** → producto externo |
| `(2, 3, 4)` | `(5, 3)` | `([1],[1])` | `(2, 4, 5)` | el eje de tamaño `3` |

### Ejemplo trabajado con shapes concretos

```python
a = np.arange(3*4*5).reshape(3, 4, 5)   # shape (3, 4, 5)
b = np.arange(4*5*6).reshape(4, 5, 6)   # shape (4, 5, 6)

# Contrae el eje 1 de a (tamaño 4) con el eje 0 de b (tamaño 4),
# y el eje 2 de a (tamaño 5) con el eje 1 de b (tamaño 5):
c = np.tensordot(a, b, axes=([1, 2], [0, 1]))
c.shape    # (3, 6)  → libres: eje 0 de a (3) + eje 2 de b (6)
```

El mapa de shapes en acción: $(3,\,\mathbf{4},\,\mathbf{5}),(\mathbf{4},\,\mathbf{5},\,6)
\xrightarrow{\ \text{axes}=([1,2],[0,1])\ } (3, 6)$, sumando sobre los dos ejes en negrita.

## Vectorización

`tensordot` evita el bucle anidado sobre los ejes contraídos: internamente **reordena** ambos
tensores para juntar los ejes a contraer, los **aplana** a una matriz 2D y delega el producto en
**BLAS** (el mismo motor que [[np.matmul]]). Frente al bucle Python explícito sobre los índices
libres y los contraídos:

```python
# Bucle Python: suma manual sobre los dos ejes contraídos (4 y 5)
def contraer(a, b):
    out = np.zeros((a.shape[0], b.shape[2]))
    for i in range(a.shape[0]):
        for j in range(b.shape[2]):
            for k1 in range(a.shape[1]):
                for k2 in range(a.shape[2]):
                    out[i, j] += a[i, k1, k2] * b[k1, k2, j]
    return out

# Vectorizado: NumPy aplana los ejes contraídos y llama a BLAS
np.tensordot(a, b, axes=([1, 2], [0, 1]))
```

Mismo resultado; la versión vectorizada sustituye cuatro `for` anidados por una sola contracción
optimizada. Es el principio de [[concepto_vectorizacion]]: describes *qué ejes contraer*, no *cómo
iterar*.

## Valor de retorno

| `a` | `b` | `axes` | salida (shape) | tipo |
|-----|-----|--------|----------------|------|
| 1D `(k,)` | 1D `(k,)` | `1` | `()` | **escalar** de NumPy |
| 2D | 2D | `1` | `(m, n)` | `ndarray` |
| N-D | N-D | par/int | `(*libres_a, *libres_b)` | `ndarray` |
| cualquiera | cualquiera | `0` | producto externo | `ndarray` |

- El `dtype` sigue las reglas de **promoción**: `int` × `float` → `float`, `float32` × `float64`
  → `float64`.
- Si **todos** los ejes se contraen (no quedan libres), el resultado es un escalar 0-d.

## Casos de uso

### Reproducir el producto matricial
```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
np.tensordot(A, B, axes=([1], [0]))   # [[19, 22], [43, 50]]  ≡ A @ B
np.tensordot(A, B, axes=1)            # idéntico (atajo)
```

### Reproducir el producto punto (inner) y el externo (outer)
```python
u = np.array([1, 2, 3])
v = np.array([4, 5, 6])
np.tensordot(u, v, axes=1)   # 32        → producto punto (todos los ejes contraídos)
np.tensordot(u, v, axes=0)   # (3, 3)    → producto externo (ningún eje contraído)
```

### Doble contracción de tensores (física / mecánica)
```python
# Tensor de tensiones (3,3) y tensor de deformaciones (3,3):
# energía = sum_ij  sigma_ij * eps_ij   → contraer AMBOS ejes
sigma = np.random.rand(3, 3)
eps   = np.random.rand(3, 3)
np.tensordot(sigma, eps, axes=([0, 1], [0, 1]))   # escalar
```

### Aplicar un tensor de rigidez de rango 4
```python
# C de rango 4 (3,3,3,3) contraído con deformación (3,3) sobre sus dos últimos ejes:
C   = np.random.rand(3, 3, 3, 3)
eps = np.random.rand(3, 3)
sigma = np.tensordot(C, eps, axes=([2, 3], [0, 1]))
sigma.shape   # (3, 3)  → libres: los dos primeros ejes de C
```

### Contraer un eje no terminal con el par de listas
```python
a = np.arange(2*3*4).reshape(2, 3, 4)   # (2, 3, 4)
b = np.arange(5*3).reshape(5, 3)        # (5, 3)
np.tensordot(a, b, axes=([1], [1])).shape   # (2, 4, 5) → contrae el eje de tamaño 3
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `shape-mismatch for sum` | los ejes emparejados no coinciden en tamaño | revisar `a.shape[axes[0]] == b.shape[axes[1]]` |
| Salida con ejes en orden inesperado | la salida es `(libres_a, libres_b)`, no el orden original | usar [[np.transpose]] tras la contracción |
| Emparejamiento cruzado mal | el orden de las dos listas de `axes` no se corresponde | `axes=([1,2],[0,1])`: 1↔0 y 2↔1, en ese orden |
| Esperar broadcasting por lotes | `tensordot` **no** hace lotes como `matmul` | usar `@`/[[np.matmul]] o [[np.einsum]] con `'bij,bjk->bik'` |
| Producto externo inesperado | usaste `axes=0` | `axes=0` no contrae nada (outer); usa `axes=1` para el punto |

## Notas relacionadas

- [[concepto_shape]] — la salida es la concatenación de los ejes libres
- [[concepto_vectorizacion]] — la contracción sin bucles anidados (BLAS)
- [[np.matmul]] — el caso particular: contraer la dimensión interior
- [[np.einsum]] — la misma contracción, pero con notación de subíndices explícita
- [[np.matmul]] · [[np.linalg.multi_dot]] · [[np.linalg.matrix_power]]
