---
title: np.vdot — producto punto que aplana ambos a 1D y conjuga el primero (siempre escalar)
aliases:
  - vdot
  - np.vdot
  - producto interno
  - producto hermítico
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np
tipo: funcion
retorna: escalar
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.vdot — producto punto aplanado y conjugado (siempre escalar)

`np.vdot` es el producto interno "de libro de texto": **aplana ambos operandos a 1D**, **conjuga el
primero** y suma el producto término a término. A diferencia de [[np.dot]], **siempre devuelve un
escalar** sin importar el shape de la entrada, y para números complejos calcula el **producto interno
hermítico** $\langle a, b\rangle = \sum_i \bar a_i\, b_i$. Es la operación correcta para normas y
ángulos en espacios complejos, donde un `dot` sin conjugar daría el resultado equivocado.

> [!warning] No existe `np.linalg.vdot`
> `np.vdot` vive en el **namespace raíz** (`np.vdot`); el nombre del archivo es histórico. Es
> estrictamente para **dos arrays** (no matrices por lotes); si necesitas el producto matricial usa
> [[np.matmul]], y si no quieres ni aplanar ni conjugar, [[np.dot]].

## La idea en una fórmula

`np.vdot` ignora la forma: **aplana** `a` y `b` (en orden C, fila a fila), **conjuga** `a` y contrae
el único eje resultante. El **mapa de shapes** colapsa *cualquier* entrada a un escalar:

$$
(\dots)\ \times\ (\dots)\ \longrightarrow\ ()
$$

mientras `a.size == b.size`. La fórmula por índices, sobre los elementos ya aplanados:

$$
c \;=\; \sum_{i} \overline{a_i}\, b_i \qquad c \in \mathbb{C}
$$

donde $\overline{a_i}$ es el **conjugado complejo** de $a_i$ (para reales, $\overline{a_i}=a_i$ y la
conjugación no hace nada). Las **dos diferencias** con [[np.dot]] son exactamente: (1) aplana antes
de operar, (2) conjuga el primer operando.

Visual con dos vectores reales (la conjugación no actúa):

```text
a = [a0 a1 a2]
b = [b0 b1 b2]   →   c = a0·b0 + a1·b1 + a2·b2   (escalar, shape ())
```

Visual del **aplanado**: una matriz se recorre fila a fila antes de contraer:

$$
A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \;\Rightarrow\; \mathrm{ravel}(A) = [1\ 2\ 3\ 4]
\qquad
B = \begin{bmatrix} 5 & 6 \\ 7 & 8 \end{bmatrix} \;\Rightarrow\; \mathrm{ravel}(B) = [5\ 6\ 7\ 8]
$$

$$
\mathrm{vdot}(A, B) = 1\cdot 5 + 2\cdot 6 + 3\cdot 7 + 4\cdot 8 = 70
$$

(un escalar, no una matriz)

Visual con **complejos** (se conjuga `a`):

```text
a = [1+2j, 3+4j]   conj(a) = [1-2j, 3-4j]
b = [5+6j, 7+8j]
vdot(a, b) = (1-2j)(5+6j) + (3-4j)(7+8j)
```

## Firma

```python
np.vdot(a, b) -> escalar
```

## Los parámetros en detalle

### `a` — el primer operando (el que se conjuga)
`array_like` de cualquier shape. Se **aplana** a 1D (orden C) y se le aplica el **conjugado
complejo** antes de contraer. El orden importa con complejos: `np.vdot(a, b)` conjuga `a`, mientras
`np.vdot(b, a)` conjuga `b` y da el **conjugado** del primero, no el mismo valor.

```python
a = np.array([1+2j, 3+4j])
b = np.array([1-1j, 2+0j])
np.vdot(a, b)            # conjuga a: (1-2j)(1-1j) + (3-4j)(2)
np.vdot(b, a) == np.conj(np.vdot(a, b))   # True → intercambiar conjuga el total
```

### `b` — el segundo operando (sin conjugar)
`array_like` con **el mismo número de elementos** que `a` (`a.size == b.size`); su shape concreto da
igual porque también se aplana. No se conjuga.

```python
np.vdot(np.ones((2, 3)), np.ones((3, 2)))   # 6.0  → shapes distintos, mismo size
np.vdot(np.ones((2, 3)), np.ones((2, 4)))   # ValueError: tamaños 6 vs 8
```

> `np.vdot` **no** tiene `out`, `dtype`, `axis` ni ningún otro parámetro: es deliberadamente mínima.
> Solo dos arrays entran, un escalar sale.

## El caso N-D

No hay "caso N-D" en el sentido habitual: `np.vdot` **destruye** toda la estructura dimensional al
aplanar. Un tensor `(2, 3, 4)` y otro `(4, 3, 2)` se tratan igual que dos vectores de 24 elementos.
Esto es justo lo que lo distingue de [[np.dot]] y [[np.matmul]], que **respetan** los ejes:

| `a.shape` | `b.shape` | `np.vdot` | (compara) `np.dot` |
|-----------|-----------|-----------|--------------------|
| `(k,)` | `(k,)` | `()` escalar, conjuga `a` | `()` escalar, sin conjugar |
| `(m, n)` | `(m, n)` | `()` — aplana ambos | `(m, m)` si casan los ejes (o error) |
| `(2, 3)` | `(3, 2)` | `()` — solo importa `size` | `(2, 2)` producto matricial |
| `(2, 3, 4)` | `(4, 3, 2)` | `()` — 24 elementos | producto tensorial (rango 4) |

```python
A = np.arange(6).reshape(2, 3)
B = np.arange(6).reshape(3, 2)
np.vdot(A, B)    # 55  → ravel(A)·ravel(B) = sum([0..5] * [0..5])
np.dot(A, B)     # matriz (2,2), otra operación por completo
```

## Vectorización

`np.vdot` es la forma vectorizada del producto interno con conjugación, delegado a BLAS. El bucle
Python equivalente debe aplanar y conjugar a mano:

```python
# Bucle Python (lento, explícito):
def vdot(a, b):
    af, bf = a.ravel(), b.ravel()
    s = 0
    for i in range(af.size):
        s += np.conj(af[i]) * bf[i]
    return s

# Vectorizado: aplana y contrae en C / BLAS
np.vdot(a, b)
```

Mismo resultado; la versión vectorizada evita el bucle del intérprete y la conjugación elemento a
elemento. Conceptualmente equivale a `np.sum(np.conj(a) * b)` pero en una sola pasada optimizada
(ver [[concepto_shape]] para por qué el aplanado hace el shape irrelevante).

## Valor de retorno

`np.vdot` **siempre devuelve un escalar** (0-d), nunca un `ndarray`, sea cual sea el rango de la
entrada:

| `a` | `b` | salida | tipo |
|-----|-----|--------|------|
| cualquier shape | mismo `size` | `()` escalar | escalar de NumPy |
| real × real | — | `()` | `np.float64` / `np.int64` (según promoción) |
| complejo × complejo | — | `()` | `np.complex128` |

- El `dtype` sigue las reglas de **promoción**: si alguno es complejo, el resultado es complejo;
  `int` × `float` → `float`.
- Para reales, `np.vdot(a, b) == np.dot(a.ravel(), b.ravel())` (la conjugación es la identidad).

```python
np.vdot([1, 2, 3], [4, 5, 6])           # np.int64(32)
np.vdot([1+1j], [1+1j])                  # (2+0j)  → |1+1j|² = conj·z, real positivo
type(np.vdot(np.ones((2, 2)), np.ones((2, 2))))   # numpy.float64 (escalar, no array)
```

## Casos de uso

### Producto interno real (idéntico a `dot` en 1D)
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
np.vdot(a, b)        # 32   → 1·4 + 2·5 + 3·6
```

### Norma al cuadrado de un vector complejo (lo que `dot` haría mal)
```python
z = np.array([1+2j, 3-1j])
np.vdot(z, z)        # (15+0j)  → Σ |z_i|² = 1²+2² + 3²+1² = 15, REAL y positivo
np.dot(z, z)         # (5+10j)  → Σ z_i²  → ¡no es la norma! (no conjuga)
```
Para la norma hermítica $\lVert z\rVert^2 = \sum_i |z_i|^2$ **hay que conjugar**; `np.vdot` lo hace,
`np.dot` no. Por eso `np.vdot(z, z)` es siempre real y no negativo.

### Producto interno hermítico $\langle a, b\rangle$ (mecánica cuántica, señales)
```python
a = np.array([1+0j, 0+1j])     # estado
b = np.array([1+0j, 1+0j])
np.vdot(a, b)        # (1-1j)  → conj(a)·b = (1)(1) + (-1j)(1)
```

### Da igual el shape: aplana y opera
```python
M = np.array([[1, 2], [3, 4]])
N = np.array([[5, 6], [7, 8]])
np.vdot(M, N)        # 70   → 1·5+2·6+3·7+4·8 (ambos aplanados a 4 elementos)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Norma compleja sale compleja/negativa | usaste [[np.dot]] (no conjuga) | usar `np.vdot(z, z)` → real ≥ 0 |
| Resultado conjugado del esperado | conjuga el **primer** argumento | revisar el orden: `vdot(a,b)` conjuga `a` |
| Esperar una matriz de salida | `np.vdot` **siempre** da escalar | usar [[np.dot]]/[[np.matmul]] si quieres ndarray |
| `ValueError` de tamaños | `a.size != b.size` | igualar el número total de elementos |
| Estructura N-D ignorada | `vdot` **aplana** ambos | si necesitas respetar ejes, usa [[np.dot]]/[[np.inner]] |

## Notas relacionadas

- [[concepto_shape]] — por qué el aplanado vuelve irrelevante el shape de entrada
- [[np.dot]] — el producto que **no** aplana ni conjuga (respeta los ejes)
- [[np.inner]] — producto sobre el **último eje** sin conjugar (no aplana del todo)
- [[np.matmul]] — el producto matricial (`@`) para matrices y lotes
- [[np.multiply]] · [[np.vdot]]
