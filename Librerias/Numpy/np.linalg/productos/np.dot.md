---
title: np.dot — el producto "clásico", punto en 1D, matricial en 2D, tensorial en N-D
aliases:
  - dot
  - np.dot
  - producto punto
  - producto escalar
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

# np.dot — el producto "clásico" (punto · matricial · tensorial)

`np.dot` es el producto **general y más antiguo** de NumPy: cambia de significado según el rango de
sus operandos. Con dos vectores hace el **producto punto** ($\sum_k a_k b_k$, un escalar); con dos
matrices, el **producto matricial**; en N-D hace un **producto tensorial** que contrae el último
eje de `a` con el penúltimo de `b`. La pregunta clave nunca es "¿qué hace `dot`?" sino
**"¿qué eje contrae y qué shape resulta?"** — y en >2D su respuesta difiere de [[np.matmul]].

> [!warning] No existe `np.linalg.dot`
> `np.dot` vive en el **namespace raíz** (`np.dot`), no en `np.linalg`. El nombre del archivo es
> histórico. Para el producto **elemento a elemento** (Hadamard) ver [[np.multiply]] (`*`); para
> lotes/broadcasting de matrices en N-D, prefiere [[np.matmul]] / `@`.

## La idea en una fórmula

`np.dot` contrae **el último eje de `a` con el penúltimo de `b`** (en 1D, "penúltimo" = "único").
Esa única regla genera todos los casos. El **mapa de shapes** general:

$$
(n_0,\dots,n_{r-1},\, i,\, k)\ \times\ (m_0,\dots,m_{s-1},\, k,\, j)\ \longrightarrow\ (n_0,\dots,n_{r-1},\, i,\ m_0,\dots,m_{s-1},\, j)
$$

El eje compartido $k$ **se contrae y desaparece**; todos los demás ejes de `a` y de `b`
**se concatenan** en el resultado (de ahí el rango alto en N-D). La fórmula por índices en el caso
matricial $(m,k)\times(k,n)$:

$$
C_{ij} = \sum_{k} a_{ik}\, b_{kj} \qquad C \in \mathbb{R}^{m \times n}
$$

y en el caso 1D·1D, donde no sobreviven ejes, el resultado es un **escalar**:

$$
c = \sum_{k} a_k\, b_k \qquad c \in \mathbb{R}
$$

**El mapa de shapes por caso** (el corazón de la nota):

$$
\begin{aligned}
\text{1D·1D:}\quad & (k),\ (k) &&\longrightarrow\ () && \text{escalar} \\
\text{2D·2D:}\quad & (m,k),\ (k,n) &&\longrightarrow\ (m,n) && \text{matricial} \\
\text{2D·1D:}\quad & (m,k),\ (k) &&\longrightarrow\ (m) && \text{matriz · vector} \\
\text{1D·2D:}\quad & (k),\ (k,n) &&\longrightarrow\ (n) && \text{vector · matriz} \\
\text{N-D:}\quad & (n_0,\dots,n_{r-1},i,k),\ (m_0,\dots,m_{s-1},k,j) &&\longrightarrow\ (n_0,\dots,n_{r-1},i,m_0,\dots,m_{s-1},j) && \text{tensorial}
\end{aligned}
$$

Visualmente, para $A_{(2\times 3)}$ y $B_{(3\times 2)}$ se contrae la dimensión $3$:

$$
\begin{bmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \end{bmatrix}_{(2\times 3)}
\begin{bmatrix} b_{00} & b_{01} \\ b_{10} & b_{11} \\ b_{20} & b_{21} \end{bmatrix}_{(3\times 2)}
=
\begin{bmatrix} c_{00} & c_{01} \\ c_{10} & c_{11} \end{bmatrix}_{(2\times 2)}
$$

$c_{00}=a_{00}b_{00}+a_{01}b_{10}+a_{02}b_{20}$ y $c_{01}=a_{00}b_{01}+a_{01}b_{11}+a_{02}b_{21}$ (suma sobre $k=0,1,2$); el eje interior $k=3$ desaparece.

Y el caso 1D·1D, donde todo colapsa a un número:

$$
a = \begin{bmatrix} a_0 & a_1 & a_2 \end{bmatrix} \qquad b = \begin{bmatrix} b_0 & b_1 & b_2 \end{bmatrix} \qquad c = a_0 b_0 + a_1 b_1 + a_2 b_2
$$

(un escalar, shape `()`)

## Firma

```python
np.dot(a, b, out=None) -> ndarray | escalar
```

## Los parámetros en detalle

### `a`, `b` — los operandos
Los dos tensores a multiplicar. La regla de compatibilidad es **siempre la misma**: el **último eje
de `a`** debe coincidir con el **penúltimo eje de `b`** (o el único, si `b` es 1D):
`a.shape[-1] == b.shape[-2]` en general, `a.shape[-1] == b.shape[-1]` si `b` es 1D. A diferencia de
[[np.matmul]], `np.dot` **sí acepta escalares**: si `a` o `b` es un escalar, `np.dot` equivale a la
multiplicación elemento a elemento `a * b`.

```python
np.dot(3, 4)            # 12   → escalar · escalar = producto normal
np.dot(2, np.array([1, 2, 3]))   # [2, 4, 6]  → escalar · array = a * b
```

### `out` — buffer de salida
`ndarray` preasignado con el shape **exacto** del resultado y un `dtype` compatible. Evita asignar
memoria nueva; útil al repetir el producto en un bucle. Debe ser C-contiguo y del tipo correcto, o
NumPy lo ignora/lanza error.

```python
A = np.ones((2, 3)); B = np.ones((3, 2))
C = np.empty((2, 2))
np.dot(A, B, out=C)     # escribe el resultado en C, sin asignar
```

> `np.dot` **no** acepta `dtype`/`casting`/`order`/`where`: es la API antigua. Para control fino del
> tipo o del lote en N-D, usa [[np.matmul]] (`np.matmul(..., dtype=np.float64)`).

## El caso N-D

En 1D y 2D, `np.dot` es el producto de toda la vida (punto y matricial). La diferencia **crucial**
aparece en **N-D**: `np.dot` no trata los ejes anteriores como un "lote", sino que hace un
**producto tensorial** — contrae el último eje de `a` con el penúltimo de `b` y **concatena todos los
demás ejes**, produciendo un resultado de **rango más alto**:

| `a.shape` | `b.shape` | resultado | qué pasa |
|-----------|-----------|-----------|----------|
| `(k,)` | `(k,)` | `()` escalar | producto punto: $\sum_k a_k b_k$ |
| `(m, k)` | `(k, n)` | `(m, n)` | matricial estándar |
| `(m, k)` | `(k,)` | `(m,)` | matriz · vector |
| `(k,)` | `(k, n)` | `(n,)` | vector · matriz |
| `(b, m, k)` | `(k, n)` | `(b, m, n)` | contrae `k`; sobreviven `(b, m)` y `(n)` |
| `(b, m, k)` | `(c, k, n)` | `(b, m, c, n)` | **producto tensorial**: rango 4, no un lote |
| `(p, q, k)` | `(r, k, s)` | `(p, q, r, s)` | concatena `(p, q)` y `(r, s)`, contrae `k` |

```python
A = np.ones((10, 2, 3))     # rango 3
B = np.ones((10, 3, 4))     # rango 3
np.dot(A, B).shape          # (10, 2, 10, 4)  → rango 4 (¡tensorial!)
np.matmul(A, B).shape       # (10, 2, 4)      → lote de 10 productos (lo habitual)
```

La diferencia **`np.dot` vs `@`/`np.matmul` en >2D**: `np.dot` concatena ejes (producto tensorial,
rango mayor); `matmul`/`@` hacen *broadcasting por lotes* de los dos últimos ejes. En N-D casi
siempre quieres `@`/`np.matmul`; `np.dot` solo en 1D/2D o cuando de verdad buscas el producto
tensorial.

| Caso | `np.dot` | `@` / [[np.matmul]] |
|------|----------|---------------------|
| 1D × 1D | producto punto → escalar | producto punto → escalar (igual) |
| 2D × 2D | matricial | matricial (igual) |
| Pila N-D | producto tensorial (rango mayor) | lote por broadcasting de los 2 últimos ejes |
| Escalar | permitido (equivale a `*`) | **no permitido** |

## Vectorización

Como todo producto en NumPy, `np.dot` delega cada multiplicación-suma en **BLAS** (código numérico
optimizado en C/Fortran), no en el intérprete de Python. Para un producto punto, eso reemplaza un
bucle explícito de acumulación:

```python
# Bucle Python (lento, explícito):
def punto(a, b):
    s = 0.0
    for k in range(len(a)):
        s += a[k] * b[k]
    return s

# Vectorizado: NumPy recorre el eje en C / BLAS
np.dot(a, b)
```

Mismo resultado; la versión vectorizada evita `len(a)` saltos al intérprete y usa instrucciones
SIMD/BLAS. Razonar "el último eje de `a` se contrae contra el penúltimo de `b`" es lo que permite
predecir el shape sin ejecutar — el principio de [[concepto_shape]] aplicado al producto.

## Valor de retorno

El tipo del retorno **depende del rango de los operandos**:

| `a` | `b` | salida (shape) | tipo |
|-----|-----|----------------|------|
| 1D `(k,)` | 1D `(k,)` | `()` | **escalar** de NumPy |
| 2D | 2D | `(m, n)` | `ndarray` |
| 2D | 1D | `(m,)` | `ndarray` |
| 1D | 2D | `(n,)` | `ndarray` |
| N-D | N-D | `(..., i, ..., j)` (tensorial) | `ndarray` |
| escalar | cualquiera | igual que `a * b` | escalar / `ndarray` |

- El `dtype` sigue las reglas de **promoción**: `int` × `float` → `float`; `float32` × `float64`
  → `float64`. No hay parámetro `dtype` para forzarlo (usa [[np.matmul]] o `a.astype(...)` antes).
- Solo el caso **1D·1D** (y escalar·escalar) devuelve un escalar de NumPy; el resto devuelve
  `ndarray`.

```python
np.dot([1, 2, 3], [4, 5, 6])      # np.int64(32)   → escalar (1·4 + 2·5 + 3·6)
type(np.dot([[1, 2]], [[3], [4]]))  # numpy.ndarray  → (1,1)
```

## Casos de uso

### Producto punto de dos vectores (escalar)
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
np.dot(a, b)        # 32   → 1·4 + 2·5 + 3·6
a @ b               # 32   → idéntico en 1D
```

### Producto matricial 2D (igual que `@`)
```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
np.dot(A, B)        # [[19, 22], [43, 50]]
```

### Matriz · vector (transformación lineal)
```python
M = np.array([[2, 0], [0, 3]])   # escalado
v = np.array([1, 1])
np.dot(M, v)        # [2, 3]
```

### Escalar como operando (lo que `@` no permite)
```python
np.dot(5, np.array([1, 2, 3]))   # [5, 10, 15]  → equivale a 5 * v
# np.matmul(5, ...) → ValueError
```

### N-D trabajado: el producto tensorial con valores
```python
A = np.arange(8).reshape(2, 2, 2)   # rango 3
#   [[[0,1],[2,3]], [[4,5],[6,7]]]
B = np.array([[1, 0], [0, 1]])      # identidad 2x2

R = np.dot(A, B)
R.shape    # (2, 2, 2)  → contrae el último eje de A (tam 2) con la fila de B
R          # [[[0,1],[2,3]], [[4,5],[6,7]]]  (B=I → no cambia)

# Caso que revela el rango alto:
P = np.ones((3, 2, 4))    # último eje = 4
Q = np.ones((5, 4, 6))    # penúltimo eje = 4
np.dot(P, Q).shape        # (3, 2, 5, 6)  → concatena (3,2)+(5,6), contrae el 4
```
El shape de salida sale **mecánicamente del mapa**: se quita el `k=4` compartido y se pegan los
ejes sobrevivientes `(3, 2)` de `P` y `(5, 6)` de `Q`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `shapes ... not aligned` | el último eje de `a` no casa con el penúltimo de `b` | asegurar `a.shape[-1] == b.shape[-2]` |
| Resultado de rango inesperado en N-D | `np.dot` hace producto **tensorial**, no lote | usar [[np.matmul]] / `@` para lotes |
| Esperar `np.dot(A, B) == np.dot(B, A)` | el producto **no es conmutativo** | respetar el orden |
| Esperar escalar de un `(1, n)·(n, 1)` | eso da `(1, 1)`, no `()` | usar 1D·1D, o `.item()` |
| Producto elemento a elemento inesperado | usaste `np.dot` con un escalar sin querer | recuerda: escalar → `a * b` |

## Notas relacionadas

- [[concepto_shape]] — razonar el producto en términos de ejes que se contraen y sobreviven
- [[np.matmul]] — el producto matricial moderno (`@`): lotes/broadcasting en N-D, no tensorial
- [[np.vdot]] — producto punto que aplana y conjuga; siempre escalar
- [[np.multiply]] — el producto elemento a elemento (`*`), no confundir
- [[np.inner]] · [[np.linalg.multi_dot]]
