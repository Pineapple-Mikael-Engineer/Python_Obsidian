---
title: np.kron — producto de Kronecker (A ⊗ B), cada elemento escala el bloque entero B
aliases:
  - producto de Kronecker
  - kron
  - np.kron
  - "A ⊗ B"
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.kron — producto de Kronecker `A ⊗ B`

El producto de Kronecker **expande** dos matrices en una matriz por bloques mucho más grande: cada
elemento $a_{ij}$ de $A$ multiplica una **copia completa** de $B$, y esas copias se colocan en una
rejilla con la misma disposición que $A$. Es la operación detrás de los productos tensoriales,
los espacios de estados de sistemas cuánticos compuestos y la construcción de mallas/operadores
separables. A diferencia del producto matricial (que **contrae** un eje, ver [[np.matmul]]), `kron`
**multiplica las dimensiones**: nada se suma, todo se replica.

## La idea en una fórmula

Para $A$ de shape $(m, n)$ y $B$ de shape $(p, q)$, el resultado es una matriz por **bloques** donde
el bloque $(i, j)$ es la matriz entera $B$ escalada por $a_{ij}$:

$$
A \otimes B \;=\;
\begin{pmatrix}
a_{11}B & a_{12}B & \cdots & a_{1n}B \\
a_{21}B & a_{22}B & \cdots & a_{2n}B \\
\vdots  & \vdots  & \ddots & \vdots  \\
a_{m1}B & a_{m2}B & \cdots & a_{mn}B
\end{pmatrix}
$$

**El mapa de shapes** (la relación entrada → salida): las dimensiones **se multiplican**, no se
contraen.

$$
(m,\, n) \;\otimes\; (p,\, q) \;\longrightarrow\; (m\,p,\ n\,q)
$$

A nivel de índices, el elemento $(r, s)$ del resultado descompone $r = i\,p + k$ y $s = j\,q + l$
(división y resto): elige el bloque $(i, j)$ por el cociente y la posición $(k, l)$ dentro del
bloque por el resto:

$$
(A \otimes B)_{\,i p + k,\ j q + l} \;=\; a_{ij}\, b_{kl}
$$

Visualmente, para $A_{(2\times2)}$ y $B_{(2\times2)}$ el resultado es $(4\times4)$ por bloques:

$$
A = \begin{bmatrix} a & b \\ c & d \end{bmatrix} \qquad
B = \begin{bmatrix} e & f \\ g & h \end{bmatrix}
$$

$$
A \otimes B =
\begin{bmatrix} a\,B & b\,B \\ c\,B & d\,B \end{bmatrix}
=
\left[\begin{array}{cc|cc}
ae & af & be & bf \\
ag & ah & bg & bh \\ \hline
ce & cf & de & df \\
cg & ch & dg & dh
\end{array}\right]
\quad (4\times4)
$$

Cada uno de los 4 bloques `(2×2)` es una copia de `B` escalada por el elemento de `A` que ocupa esa
posición: el eje de `A` y el eje de `B` se **entrelazan**, no se cancelan.

## Firma

```python
np.kron(a, b) -> ndarray
```

`kron` es deliberadamente simple: **no** tiene `axis`, `out`, `dtype` ni `keepdims`. Toda su
riqueza está en cómo combina los shapes de los dos operandos.

## Los parámetros en detalle

### `a`, `b` — los dos operandos
`array_like` (ndarray, lista, escalar). Se convierten a `ndarray`. **No hay restricción de shape
entre ellos**: a diferencia de [[np.matmul]], las dimensiones interiores no tienen que coincidir,
porque no se contrae nada. Cualquier $(m, n)$ se combina con cualquier $(p, q)$.

```python
A = np.array([[1, 0], [0, 1]])   # (2, 2)
B = np.array([[1, 2], [3, 4]])   # (2, 3) no hace falta: cualquier shape vale
np.kron(A, B).shape              # (4, 4) → 2*2 por 2*2
```

El **orden importa**: `kron(A, B) != kron(B, A)` en general (no es conmutativo), aunque ambos
resultados son *permutaciones* uno del otro.

## El caso N-D

`kron` generaliza a cualquier número de dimensiones: el resultado tiene `ndim = max(a.ndim, b.ndim)`,
y cada eje del resultado es el **producto** de los ejes correspondientes (alineados por la derecha,
rellenando con tamaño 1 el array de menor rango):

$$
(\dots, m_0, m_1, \dots, m_k) \;\otimes\; (\dots, p_0, p_1, \dots, p_k)
\;\longrightarrow\; (\dots, m_0 p_0,\ m_1 p_1,\ \dots,\ m_k p_k)
$$

| `a.shape` | `b.shape` | resultado | qué pasa |
|-----------|-----------|-----------|----------|
| `(m,)` | `(p,)` | `(m*p,)` | producto de Kronecker de vectores |
| `(m, n)` | `(p, q)` | `(m*p, n*q)` | matriz por bloques (el caso típico) |
| `(2, 2)` | `(2, 2)` | `(4, 4)` | el visual de arriba |
| `(a, b, c)` | `(d, e, f)` | `(a*d, b*e, c*f)` | cada eje se multiplica con su par |
| `(m, n)` | `(p,)` | `(m, n*p)` | el de menor rango se alinea por la derecha → `(1, p)` |

```python
T = np.ones((2, 3, 4))
S = np.ones((5, 6, 7))
np.kron(T, S).shape    # (10, 18, 28)  → (2*5, 3*6, 4*7), eje a eje
```

La regla mecánica: empareja los ejes por la derecha y **multiplica** sus tamaños. Es el dual exacto
del [[concepto_shape|mapa de shapes]] de una reducción, que en vez de multiplicar elimina un eje.

## Vectorización

`kron` construye la matriz expandida en C sin que el usuario escriba un solo bucle sobre los
bloques. El equivalente manual recorrería cada elemento de `A` colocando una copia escalada de `B`:

```python
# Bucle Python: copiar B escalado en cada bloque
def kron_lento(A, B):
    m, n = A.shape
    p, q = B.shape
    out = np.empty((m*p, n*q))
    for i in range(m):
        for j in range(n):
            out[i*p:(i+1)*p, j*q:(j+1)*q] = A[i, j] * B
    return out

# Vectorizado: NumPy lo hace con outer + reshape internamente
np.kron(A, B)
```

Internamente NumPy lo resuelve como un **producto externo** seguido de un reordenamiento de ejes
(`reshape`/`transpose`), no como `m*n` asignaciones desde el intérprete: el coste de iterar los
bloques se queda en C. Ver [[concepto_vectorizacion]].

## Valor de retorno

| `a` | `b` | salida (shape) | tipo |
|-----|-----|----------------|------|
| `(m,)` | `(p,)` | `(m*p,)` | `ndarray` |
| `(m, n)` | `(p, q)` | `(m*p, n*q)` | `ndarray` |
| N-D | N-D | producto eje a eje | `ndarray` |

- Siempre devuelve un **`ndarray`** (nunca un escalar suelto, aunque dos escalares 0-d den un 0-d).
- El `dtype` sigue las reglas de **promoción**: `int ⊗ float → float`, etc.
- `size` del resultado = `a.size * b.size` (las dimensiones se multiplican): cuidado, **crece muy
  rápido** y consume memoria con operandos grandes.

```python
A = np.array([[1, 2],
              [3, 4]])
B = np.eye(2)            # identidad 2x2
np.kron(A, B)
# [[1., 0., 2., 0.],
#  [0., 1., 0., 2.],
#  [3., 0., 4., 0.],
#  [0., 3., 0., 4.]]
```

## Casos de uso

### Producto tensorial de operadores (sistema cuántico de 2 qubits)
El espacio de estados de dos qubits es el producto tensorial de los individuales: un operador que
actúa sobre el par se construye con `kron`.

```python
X = np.array([[0, 1], [1, 0]])   # puerta NOT (Pauli-X)
I = np.eye(2)
# Aplicar X al primer qubit, identidad al segundo: X ⊗ I (4x4)
np.kron(X, I)
# [[0, 0, 1, 0],
#  [0, 0, 0, 1],
#  [1, 0, 0, 0],
#  [0, 1, 0, 0]]
```

### Replicar un patrón (escalado por bloques)
`kron` con una matriz de unos "amplía" cada celda a un bloque, útil para upscaling de mallas o
imágenes por vecino más cercano.

```python
patron = np.array([[1, 2],
                   [3, 4]])
np.kron(patron, np.ones((2, 2), dtype=int))
# [[1, 1, 2, 2],
#  [1, 1, 2, 2],
#  [3, 3, 4, 4],
#  [3, 3, 4, 4]]   → cada píxel se vuelve un bloque 2x2
```

### Operador separable sobre una malla N-D
El laplaciano 2D de una malla rectangular se ensambla como `kron` de operadores 1D, aprovechando que
las dimensiones se multiplican.

```python
n = 4
D = np.diag(-2*np.ones(n)) + np.diag(np.ones(n-1), 1) + np.diag(np.ones(n-1), -1)  # (4,4)
I = np.eye(n)
L2 = np.kron(D, I) + np.kron(I, D)   # (16, 16) → laplaciano sobre la malla 4x4
L2.shape                             # (16, 16)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar que contraiga un eje (como `@`) | `kron` **multiplica** dimensiones, no las suma | usar [[np.matmul]] si querías el producto matricial |
| `MemoryError` / array gigante | `size` resultante = `a.size * b.size` | verificar el tamaño antes; los operandos crecen rápido |
| Esperar `kron(A, B) == kron(B, A)` | **no es conmutativo** (solo permutación) | respetar el orden de los factores |
| Confundirlo con el producto externo `np.outer` | `outer` es el caso 1D sin estructura por bloques | usar `kron` para la matriz por bloques N-D |
| Resultado con `dtype` float inesperado | promoción `int ⊗ float` | fijar el `dtype` de los operandos antes |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes: aquí las dimensiones se **multiplican**
- [[concepto_vectorizacion]] — por qué no hace falta el bucle por bloques
- [[np.matmul]] — el producto matricial (contrae un eje), no confundir con `kron`
- [[np.outer]] · [[np.tensordot]] · [[np.linalg.matrix_power]]
