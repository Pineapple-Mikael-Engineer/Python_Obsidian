---
title: np.matmul — producto matricial (@), contrae la dimensión interior
aliases:
  - producto matricial
  - matmul
  - np.matmul
  - "@"
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
  - concepto_vectorizacion
draft: false
---

# producto matricial — `@` / `np.matmul` / `np.dot`

El producto matricial **contrae** una dimensión: toma la dimensión interior compartida de dos
tensores, multiplica y **suma sobre ella**, haciéndola desaparecer. Es la operación detrás de toda
transformación lineal, capa densa de una red o cambio de base. En NumPy se escribe con el operador
`@` (recomendado, PEP 465), o las funciones [[np.matmul]]/`np.dot`.

> [!warning] No existe `np.linalg.dot`
> El producto matricial vive en el **namespace raíz** (`@`, `np.matmul`, `np.dot`), no en
> `np.linalg`. Esta nota documenta el producto matricial general; el nombre del archivo es histórico.
> Para el producto **elemento a elemento** (Hadamard) ver [[np.multiply]] (`*`).

## La idea en una fórmula

Para dos matrices $A$ de shape $(m, k)$ y $B$ de shape $(k, n)$, el elemento $(i, j)$ del resultado
es la **contracción** sobre el eje compartido $k$:

$$
C_{ij} = \sum_{k} A_{ik}\, B_{kj} \qquad C \in \mathbb{R}^{m \times n}
$$

El eje $k$ —la dimensión interior— **aparece en el sumatorio y desaparece** del resultado.

**El mapa de shapes** (la relación entrada → salida, incluido el caso por lotes N-D):

$$
(n_0,\dots,n_{k-1},\, m,\, p)\ \times\ (n_0,\dots,n_{k-1},\, p,\, q)\ \longrightarrow\ (n_0,\dots,n_{k-1},\, m,\, q)
$$

Los **dos últimos ejes** son la matriz; los $n_0,\dots,n_{k-1}$ anteriores son ejes de lote que se alinean por
broadcasting; el eje interior $p$ se **contrae y desaparece**. Esta única regla gobierna todos los
casos: producto punto ($p$ contra $p$ → escalar), matriz·vector, y la pila N-D.

Visualmente, para $A_{(2\times 3)}$ y $B_{(3\times 2)}$ se contrae la dimensión $3$:

$$
\begin{bmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \end{bmatrix}_{(2\times 3)}
\begin{bmatrix} b_{00} & b_{01} \\ b_{10} & b_{11} \\ b_{20} & b_{21} \end{bmatrix}_{(3\times 2)}
=
\begin{bmatrix} c_{00} & c_{01} \\ c_{10} & c_{11} \end{bmatrix}_{(2\times 2)}
$$

$c_{00}=a_{00}b_{00}+a_{01}b_{10}+a_{02}b_{20}$ y $c_{01}=a_{00}b_{01}+a_{01}b_{11}+a_{02}b_{21}$ (suma sobre $k=0,1,2$); el eje interior $k=3$ desaparece.

## Firma

```python
A @ B                                          # operador (recomendado)
np.matmul(x1, x2, /, out=None, *, casting='same_kind', order='K', dtype=None) -> ndarray
np.dot(a, b, out=None) -> ndarray
```

## Los parámetros en detalle

### `x1`, `x2` (matmul) / `a`, `b` (dot) — los operandos
Los dos tensores a multiplicar. La regla de compatibilidad es **siempre la misma**: la dimensión
interior debe coincidir, `x1.shape[-1] == x2.shape[-2]`. Lo que cambia es cómo se interpretan los
ejes **anteriores** (ver N-D, abajo).

### `out` — buffer de salida
`ndarray` preasignado con el shape exacto del resultado. Evita asignar memoria; útil al repetir el
producto en un bucle. En `matmul` debe tener `dtype` compatible.

### `casting`, `order`, `dtype` (solo `matmul`)
- `dtype`: fuerza el tipo de salida (y del cómputo). Útil para acumular en `float64` aunque los
  operandos sean `float32`.
- `casting='same_kind'` (defecto): controla qué conversiones de tipo se permiten entre operandos y
  `out`/`dtype`. Rara vez se toca; importa si pasas un `out` de tipo distinto.
- `order='K'`: layout de memoria del resultado (`'C'` filas, `'F'` columnas, `'K'` el que más se
  parezca a las entradas). Solo afecta rendimiento/contigüidad, no los valores.

> `np.dot` **no** acepta `where`/`order`/`dtype`: es la API antigua. Para control fino, usa `matmul`.

## El eje y el caso N-D

En 2D el producto es el de toda la vida. En **N-D**, `@`/`matmul` tratan los **dos últimos ejes**
como la matriz y **todos los anteriores como un lote** (batch) que se alinea por
[[concepto_broadcasting|broadcasting]]:

| `A.shape` | `B.shape` | resultado | qué pasa |
|-----------|-----------|-----------|----------|
| `(k,)` | `(k,)` | `()` escalar | producto punto (1D·1D): $\sum_k a_k b_k$ |
| `(m, k)` | `(k, n)` | `(m, n)` | matricial estándar |
| `(m, k)` | `(k,)` | `(m,)` | matriz · vector |
| `(k,)` | `(k, n)` | `(n,)` | vector · matriz |
| `(b, m, k)` | `(b, k, n)` | `(b, m, n)` | **lote**: `b` productos matriciales |
| `(b, m, k)` | `(k, n)` | `(b, m, n)` | `B` se **broadcastea** a todo el lote |
| `(b, 1, m, k)` | `(1, c, k, n)` | `(b, c, m, n)` | lote 2D por broadcasting de los ejes previos |

```python
P = np.ones((10, 2, 3))     # 10 matrices 2x3
Q = np.ones((10, 3, 4))     # 10 matrices 3x4
(P @ Q).shape               # (10, 2, 4)  → 10 productos en lote
(P @ np.ones((3, 4))).shape # (10, 2, 4)  → la misma matriz aplicada a las 10
```
La diferencia clave **`matmul` vs `dot` en >2D**: `matmul`/`@` hacen *broadcasting por lotes* de los
dos últimos ejes; `np.dot` hace un **producto tensorial** distinto (suma el último eje de `a` con el
penúltimo de `b`), generando un resultado de mayor rango. En N-D casi siempre quieres `@`/`matmul`.

| Caso | `@` / `np.matmul` | `np.dot` |
|------|-------------------|----------|
| 2D × 2D | matricial | matricial (igual) |
| Pila N-D | lote por broadcasting de los 2 últimos ejes | producto tensorial (rango mayor) |
| Escalar | **no permitido** | permitido (equivale a `*`) |

## Vectorización

El caso por lotes es el ejemplo perfecto de [[concepto_vectorizacion]]: aplicar el mismo producto a
muchas matrices **sin bucle Python**. Además, NumPy delega cada producto en **BLAS** (código
numérico optimizado), no en el intérprete:

```python
# Bucle Python: un matmul por elemento del lote
def batch_matmul(P, Q):
    out = np.empty((P.shape[0], P.shape[1], Q.shape[2]))
    for i in range(P.shape[0]):
        out[i] = P[i] @ Q[i]
    return out

# Vectorizado: NumPy recorre el lote en C / BLAS
P @ Q
```
Mismo resultado; la versión vectorizada evita `P.shape[0]` saltos al intérprete y aprovecha BLAS.
Razonar en términos de "los dos últimos ejes son la matriz, lo demás es lote" es lo que permite
escribir el producto de un tensor 4D sin un solo `for`.

## Valor de retorno

| `A` | `B` | salida | tipo |
|-----|-----|--------|------|
| 1D `(k,)` | 1D `(k,)` | `()` | **escalar** de NumPy |
| 2D | 2D/1D | `(m, n)` / `(m,)` | `ndarray` |
| N-D | N-D/2D | lote `(..., m, n)` | `ndarray` |

- El `dtype` sigue las reglas de **promoción**: `int` × `float` → `float`; `float32` × `float64`
  → `float64`. Para forzarlo, `np.matmul(..., dtype=np.float64)`.
- `@` y `np.matmul` **no** aceptan escalares: `5 @ A` es error (usa `5 * A`).

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
A @ B          # [[19, 22], [43, 50]]
B @ A          # [[23, 34], [31, 46]]  ≠ A@B → no conmutativo
A * B          # [[5, 12], [21, 32]]   → Hadamard (elemento a elemento), otra operación
```

## Casos de uso

### Producto matricial trabajado con números (2×2 · 2×2)
La contracción del eje interior, hecha a mano sobre matrices concretas:

$$
\begin{bmatrix}1&2\\3&4\end{bmatrix}
\begin{bmatrix}5&6\\7&8\end{bmatrix}
=
\begin{bmatrix}1\cdot5+2\cdot7 & 1\cdot6+2\cdot8\\ 3\cdot5+4\cdot7 & 3\cdot6+4\cdot8\end{bmatrix}
=
\begin{bmatrix}19&22\\43&50\end{bmatrix}
$$

Cada $c_{ij}$ suma la fila $i$ de la izquierda contra la columna $j$ de la derecha; el eje interior (tamaño 2) se contrae y desaparece.

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
A @ B          # [[19, 22], [43, 50]]  → coincide con la cuenta a mano
```

### Transformación lineal de un vector (rotación)
```python
theta = np.pi / 2
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
v = np.array([1, 0])
R @ v          # [0, 1]  → rota 90°
```

### Cadena de transformaciones (capa densa)
```python
X = np.random.rand(64, 784)   # 64 muestras de 784 features
W = np.random.rand(784, 128)  # pesos
Y = X @ W                     # (64, 128)  → una capa lineal para todo el lote
```

### Producto por lotes de matrices N-D (rejilla 4D de productos)
Con dos ejes de lote, `@` aplica un producto matricial **por cada celda** de la rejilla de lote, alineada por broadcasting. Aquí una rejilla $4\times 5$ de productos $(2\times 3)\cdot(3\times 4)$:

```python
A = np.random.rand(4, 5, 2, 3)   # rejilla 4×5 de matrices 2×3
B = np.random.rand(4, 5, 3, 4)   # rejilla 4×5 de matrices 3×4
(A @ B).shape                    # (4, 5, 2, 4)  → 20 productos en lote, sin bucle
```

Los **dos últimos ejes** `(2, 3)` y `(3, 4)` son la matriz —contraen el interior `3`→ `(2, 4)`—; los **dos primeros** `(4, 5)` son ejes de lote que se conservan: $20 = 4\cdot 5$ productos independientes en una sola llamada. El caso más simple `(8, 3, 3) @ (8, 3, 3) → (8, 3, 3)` es esta misma idea con un único eje de lote.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `shapes ... not aligned` | la dimensión interior no coincide | asegurar `A.shape[-1] == B.shape[-2]` |
| Esperar `A @ B == B @ A` | el producto **no es conmutativo** | respetar el orden |
| Resultado elemento a elemento inesperado | usaste `*` en vez de `@` | `*` es Hadamard; usa `@` (ver [[np.multiply]]) |
| `matmul`/`@` con escalar falla | no admiten escalares | usar `*` o `np.dot` |
| Resultado de rango raro en N-D | usaste `np.dot` en >2D | usar `@`/`np.matmul` para lotes |

## Notas relacionadas

- [[concepto_shape]] — razonar el producto en términos de ejes
- [[concepto_vectorizacion]] — el producto por lotes sin bucle (BLAS)
- [[np.multiply]] — el producto elemento a elemento (`*`), no confundir
- [[np.matmul]] · [[np.linalg.multi_dot]] · [[np.linalg.matrix_power]]
