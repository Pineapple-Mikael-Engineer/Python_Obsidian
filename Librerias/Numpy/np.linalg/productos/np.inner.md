---
title: np.inner — producto sobre el último eje de cada array
aliases:
  - inner
  - np.inner
  - producto interno
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

# np.inner — producto sobre el último eje de cada array

`np.inner(a, b)` **contrae el último eje** de cada operando: empareja `a.shape[-1]` con
`b.shape[-1]` (deben ser iguales), multiplica y **suma sobre él**, haciéndolo desaparecer. Para dos
vectores 1D es el producto punto de toda la vida; para N-D es la regla anterior generalizada, donde
los ejes que **sobreviven** de `a` y de `b` se **concatenan** en el resultado. Es el primo de
[[np.dot]], pero contrayendo el **último** eje de `b` en lugar del penúltimo.

## La idea en una fórmula

La clave es el **último eje común** de tamaño $k$: `a.shape[-1] == b.shape[-1] == k`. Ese es el eje
que se contrae; todos los demás ejes de ambos arrays sobreviven y se concatenan, primero los de `a`,
luego los de `b`.

**El mapa de shapes** — para `a.shape = (n_0,\dots,n_{p-1}, k)` y `b.shape = (m_0,\dots,m_{q-1}, k)`:

$$
(n_0,\dots,n_{p-1},\,k),\ (m_0,\dots,m_{q-1},\,k)\ \longrightarrow\ (n_0,\dots,n_{p-1},\,m_0,\dots,m_{q-1})
$$

El último eje (el de tamaño $k$) **desaparece de ambos**; lo que queda son los ejes previos de `a`
seguidos de los ejes previos de `b`. La **fórmula por índices** lo dice exactamente: cada elemento
de la salida es la suma sobre $k$ del producto de las dos "fibras" finales:

$$
C_{\,i_0\dots i_{p-1},\ j_0\dots j_{q-1}} \;=\; \sum_{k} a_{\,i_0\dots i_{p-1}\,k}\; b_{\,j_0\dots j_{q-1}\,k}
$$

Para el caso **1D·1D** ($p=q=0$) la salida es un escalar y coincide con el producto punto:

$$
\langle a, b\rangle \;=\; \sum_{k} a_k\, b_k
$$

Visualmente, con $a$ de shape $(2, 3)$ y $b$ de shape $(2, 3)$ (último eje $k=3$ común), el resultado
es $(2, 2)$: cada fila de `a` se contrae contra cada fila de `b`.

$$
a = \begin{bmatrix} a_0 = [a_{00}\ a_{01}\ a_{02}] \\ a_1 = [a_{10}\ a_{11}\ a_{12}] \end{bmatrix}
\qquad
b = \begin{bmatrix} b_0 = [b_{00}\ b_{01}\ b_{02}] \\ b_1 = [b_{10}\ b_{11}\ b_{12}] \end{bmatrix}
$$

Cada fila es una fibra de longitud $k=3$. Con $C_{ij} = a_i \cdot b_j = \sum_k a_{ik}\,b_{jk}$, la salida tiene shape $(2, 2)$:

$$
C = \begin{bmatrix} a_0 \cdot b_0 & a_0 \cdot b_1 \\ a_1 \cdot b_0 & a_1 \cdot b_1 \end{bmatrix}
$$

el eje $k=3$ se contrae y desaparece.

## Firma

```python
np.inner(a, b, /) -> ndarray | escalar
```

`np.inner` es una función "histórica" sin parámetros extra: no acepta `out`, `axis`, `dtype` ni
`where`. El eje de contracción está **fijado**: siempre el último de cada operando.

## Los parámetros en detalle

### `a`, `b` — los dos operandos
`array_like` (ndarray, lista, escalar). La **única** restricción de forma es que coincida el último
eje: `a.shape[-1] == b.shape[-1]`. Los ejes anteriores son libres y se concatenan en la salida.

```python
a = np.arange(6).reshape(2, 3)   # último eje = 3
b = np.arange(9).reshape(3, 3)   # último eje = 3  → compatible
np.inner(a, b).shape             # (2, 3)  → ejes previos: (2,) de a + (3,) de b
```

Hay un atajo: si **uno** de los dos es un **escalar**, `np.inner` se reduce a una multiplicación
ordinaria (`np.inner(a, 3) == a * 3`). Es el único caso en que no hay contracción de eje.

## El eje y el caso N-D

El eje contraído es **siempre el último** de cada array; no es configurable (a diferencia de
[[np.tensordot]], que sí deja elegir los ejes). La regla mecánica: quita el último eje de `a` y el
último de `b`, y concatena lo que queda.

| `a.shape` | `b.shape` | salida | lectura |
|-----------|-----------|--------|---------|
| `(k,)` | `(k,)` | `()` escalar | producto punto: $\sum_k a_k b_k$ |
| `(m, k)` | `(k,)` | `(m,)` | una matriz contra un vector (por filas) |
| `(m, k)` | `(n, k)` | `(m, n)` | cada fila de `a` contra cada fila de `b` |
| `(p, m, k)` | `(n, k)` | `(p, m, n)` | se concatenan los ejes previos `(p, m)` + `(n,)` |
| `(p, m, k)` | `(q, n, k)` | `(p, m, q, n)` | todos los ejes previos, en orden a→b |

```python
A = np.ones((2, 4, 3))   # ejes previos (2, 4), último eje k=3
B = np.ones((5, 3))      # ejes previos (5,),   último eje k=3
np.inner(A, B).shape     # (2, 4, 5)  → (2,4) de A ⊕ (5,) de B, k desaparece
```

> [!warning] `np.inner` vs `np.dot` en N-D
> Ambas contraen un eje, pero **distinto en `b`**: `np.inner` usa el **último** eje de `b`, mientras
> [[np.dot]] usa el **penúltimo**. Para 1D·1D coinciden (producto punto); para 2D, `np.dot(a, b)` es
> el producto matricial estándar (`a.shape[-1]` contra `b.shape[-2]`), pero `np.inner(a, b)` contrae
> `a.shape[-1]` contra `b.shape[-1]` — equivale a `a @ b.T`. No son intercambiables.

## Vectorización

`np.inner` calcula **todas** las contracciones de fibras de golpe, sin un bucle Python por pareja de
índices. El contraste con la versión explícita, para el caso 2D·2D (`(m,k)` contra `(n,k)`):

```python
# Bucle Python: una contracción por cada par (i, j)
def inner_lento(a, b):
    m, n = a.shape[0], b.shape[0]
    out = np.empty((m, n))
    for i in range(m):
        for j in range(n):
            out[i, j] = np.sum(a[i] * b[j])   # contrae el último eje
    return out

# Vectorizado: NumPy recorre todo en C / BLAS
np.inner(a, b)
```
Mismo resultado; la versión vectorizada evita $m \times n$ saltos al intérprete y delega la suma de
productos en código numérico optimizado. Es la idea de [[concepto_vectorizacion]]: describes *qué*
eje contraer, no *cómo* iterar sobre las parejas.

## Valor de retorno

| `a` | `b` | salida (shape) | tipo |
|-----|-----|----------------|------|
| 1D `(k,)` | 1D `(k,)` | `()` | **escalar de NumPy** |
| 2D `(m, k)` | 1D `(k,)` | `(m,)` | `ndarray` |
| N-D | N-D | concatenación de ejes previos | `ndarray` |
| cualquiera | escalar | igual que `a` | `ndarray` (es `a * b`) |

- El `dtype` sigue las reglas de **promoción**: `int` × `float` → `float`; `float32` × `float64`
  → `float64`. No hay parámetro `dtype` para forzarlo (convierte los operandos antes si lo necesitas).
- El resultado 1D·1D es un **escalar de NumPy** (0-dimensional), no un `ndarray`.

## Casos de uso

### Producto punto de dos vectores
```python
u = np.array([1, 2, 3])
v = np.array([4, 5, 6])
np.inner(u, v)        # 32  → 1·4 + 2·5 + 3·6
```

### Similitud de cada fila contra cada fila (matriz de productos)
```python
X = np.array([[1., 0.],
              [0., 1.],
              [1., 1.]])
np.inner(X, X)        # (3, 3): producto interno de cada par de filas (matriz de Gram)
# [[1, 0, 1],
#  [0, 1, 1],
#  [1, 1, 2]]
```

### Una matriz contra un vector (por filas)
```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
w = np.array([1, 0, -1])
np.inner(M, w)        # [-2, -2]  → fila·w para cada fila
```

### N-D trabajado con valores concretos
Con `a` de shape `(2, 2)` y `b` de shape `(2, 2)`, último eje $k=2$. La salida es `(2, 2)`: cada
fila de `a` contra cada fila de `b`.

```python
a = np.array([[1, 2],
              [3, 4]])
b = np.array([[10, 20],
              [30, 40]])
np.inner(a, b)
# [[ 50, 110],     a0·b0 = 1·10+2·20 = 50 ;  a0·b1 = 1·30+2·40 = 110
#  [110, 250]]     a1·b0 = 3·10+4·20 =110 ;  a1·b1 = 3·30+4·40 = 250
```
Subiendo a 3D, con `A.shape = (2, 1, 3)` y `B.shape = (4, 3)` se concatenan los ejes que sobreviven:

```python
A = np.arange(6).reshape(2, 1, 3)   # ejes previos (2, 1), k=3
B = np.arange(12).reshape(4, 3)     # ejes previos (4,),   k=3
np.inner(A, B).shape                # (2, 1, 4)  → (2,1) ⊕ (4,), el eje k=3 se contrae
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `shapes ... not aligned` | el último eje no coincide (`a.shape[-1] != b.shape[-1]`) | igualar el último eje; quizá querías `b.T` |
| Esperar el producto matricial estándar | `np.inner` contrae el **último** de `b`, no el penúltimo | usar `a @ b` o [[np.dot]] para el matricial |
| Resultado con rango más alto del esperado en N-D | se concatenan **todos** los ejes previos de ambos | recordar el mapa de shapes; quizá querías [[np.tensordot]] con ejes elegidos |
| Confundir `np.inner` con `np.outer` | `inner` contrae (suma); `outer` aplana y multiplica todas las parejas | ver [[np.outer]] |

## Notas relacionadas

- [[concepto_shape]] — razonar la contracción del último eje como un mapa de shapes
- [[concepto_vectorizacion]] — todas las contracciones de fibras sin bucle (BLAS)
- [[np.dot]] — contrae el **penúltimo** eje de `b` (producto matricial); no confundir
- [[np.outer]] · [[np.matmul]] · [[np.tensordot]]
