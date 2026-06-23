---
title: np.linalg.det — determinante, colapsa una matriz a un escalar (factor de volumen)
aliases:
  - det
  - linalg.det
  - np.linalg.det
  - determinante
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: escalar | ndarray
inplace: false
requiere:
  - concepto_shape
  - concepto_vectorizacion
draft: false
---

# np.linalg.det — determinante de una matriz

`np.linalg.det` **colapsa una matriz cuadrada entera a un único escalar**: el determinante. Ese
número resume dos cosas a la vez: el **factor por el que la transformación lineal escala el
volumen** (en valor absoluto) y, sobre todo, **si la matriz es invertible** — $\det = 0$ ⟺ matriz
**singular** (no invertible). La pregunta que se responde con `det` no es "¿cuánto vale?" sino, casi
siempre, "¿es esta matriz invertible o degenerada?".

## La idea en una fórmula

El determinante toma los $n\times n$ números de la matriz y los reduce a **uno solo**. Para una
matriz $A$ de shape $(n, n)$ es la suma alternada sobre todas las permutaciones de columnas:

$$
\det(A) \;=\; \sum_{\sigma \in S_n} \operatorname{sgn}(\sigma)\, \prod_{i=1}^{n} A_{i,\sigma(i)}
$$

Lo que importa para usarlo no es esa fórmula sino sus dos lecturas:

$$
\det(A) = 0 \;\Longleftrightarrow\; A \text{ singular (no invertible)}
\qquad\qquad
|\det(A)| = \text{factor de escala de volumen}
$$

**El mapa de shapes** — el determinante **colapsa los dos últimos ejes** (la matriz $n\times n$) a un
escalar, dejando intactos los ejes de lote anteriores:

$$
(\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}},\, n,\, n)\ \xrightarrow{\ \det\ }\ (\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}})
$$

Para una sola matriz $(n,n)$ el lote es vacío y la salida es un **escalar** `()`; para una pila
$(b,n,n)$ la salida es `(b,)`, **un determinante por matriz**.

$$
\begin{vmatrix} a_{00} & a_{01} \\ a_{10} & a_{11} \end{vmatrix}
\ (2\times 2)
\;\longrightarrow\; \det = a_{00}\cdot a_{11} - a_{01}\cdot a_{10}
\;\longrightarrow\; \text{un escalar } ()
$$

## Firma

```python
np.linalg.det(a) -> ndarray | escalar
```

`det` no tiene parámetros opcionales: ni `axis`, ni `out`, ni `dtype`. Toda la riqueza está en el
**shape** de `a` (una matriz o un lote de matrices).

## Los parámetros en detalle

### `a` — la matriz (o pila de matrices)
`array_like` cuyos **dos últimos ejes deben ser cuadrados**: shape `(..., n, n)`. Los ejes
anteriores (`...`) son ejes de **lote**: `det` se aplica de forma independiente a cada matriz $n\times
n$ que contienen (ver [[concepto_shape]]).

- El cálculo es por **descomposición LU**, así que el resultado es siempre **flotante** aunque `a`
  sea de enteros (`int` → `float64`). Por eso un determinante "exacto" 0 puede salir como `±1e-16`.
- No hay forma de pedir un determinante exacto/simbólico: para eso está SymPy, no NumPy.

```python
np.linalg.det(np.array([[1, 2], [3, 4]]))   # -2.0   (entrada int → salida float)
```

## El caso N-D

Los **dos últimos ejes** son siempre la matriz; **todo lo anterior es lote**. `det` reduce cada
bloque $n\times n$ a un escalar, de modo que el resultado tiene exactamente el shape del lote:

| `a.shape` | salida | lectura |
|-----------|--------|---------|
| `(n, n)` | `()` escalar | el determinante de la matriz |
| `(b, n, n)` | `(b,)` | un determinante por cada una de las `b` matrices |
| `(b, c, n, n)` | `(b, c)` | una rejilla `b×c` de determinantes |

```python
batch = np.array([[[1., 2.], [3., 4.]],    # det = -2
                  [[2., 0.], [0., 2.]],    # det =  4
                  [[1., 1.], [1., 1.]]])   # det =  0 (singular)
batch.shape                # (3, 2, 2)
np.linalg.det(batch)       # array([-2.,  4.,  0.])   → (3,)
```

El eje de las matrices **desaparece dos veces** (los dos últimos ejes colapsan a un escalar); el lote
sobrevive intacto.

## Vectorización

El soporte `(..., n, n)` es [[concepto_vectorizacion]] puro: en vez de iterar matriz por matriz en
Python, NumPy recorre el lote en C llamando a LAPACK para cada bloque. Las dos versiones dan lo
mismo; la vectorizada evita el bucle del intérprete:

```python
# Bucle Python: un det por matriz del lote
def dets_loop(batch):
    return np.array([np.linalg.det(M) for M in batch])

# Vectorizado: NumPy recorre el lote internamente
np.linalg.det(batch)
```

Razonar "los dos últimos ejes son la matriz, lo demás es lote" permite obtener los determinantes de
un tensor 4D de matrices sin un solo `for`.

## Valor de retorno

El retorno es **escalar si `a` es 2D**, y **ndarray si `a` tiene ejes de lote**:

| Entrada `a.shape` | salida (shape) | tipo |
|-------------------|----------------|------|
| `(n, n)` | `()` | **escalar de NumPy** (`np.float64` o `np.complex128`) |
| `(..., n, n)` | `(...)` | `ndarray` |

- El `dtype` es **siempre flotante**: real (`float64`) si `a` es real, complejo (`complex128`) si `a`
  es compleja. Nunca entero.
- Por el error numérico de la LU, **no compares con `== 0`**: una matriz singular puede devolver
  `1e-16`. Usa `np.isclose(det, 0)`.

```python
np.linalg.det(np.eye(3))            # np.float64(1.0)   → escalar 0-d, no ndarray
type(np.linalg.det(np.ones((5,2,2))))  # numpy.ndarray   → lote (5,)
```

## Casos de uso

### Determinante $2\times 2$ trabajado a mano
La regla del $2\times 2$ (producto de la diagonal menos el de la antidiagonal):

$$
\begin{vmatrix} 1 & 2 \\ 3 & 4 \end{vmatrix}
= 1\cdot 4 - 2\cdot 3 = 4 - 6 = -2
$$

```python
np.linalg.det(np.array([[1., 2.],
                        [3., 4.]]))   # -2.0  → coincide con el cálculo a mano
```

### Determinante $3\times 3$ por la regla de Sarrus

$$
\begin{vmatrix} 2 & 0 & 1 \\ 3 & 1 & 2 \\ 1 & 0 & 1 \end{vmatrix}
= 2(1\cdot 1 - 2\cdot 0) - 0 + 1(3\cdot 0 - 1\cdot 1) = 2 - 1 = 1
$$

```python
np.linalg.det(np.array([[2., 0., 1.],
                        [3., 1., 2.],
                        [1., 0., 1.]]))   # 1.0
```

### Comprobar invertibilidad antes de invertir
```python
A = np.array([[2.0, 1.0], [1.0, 1.0]])
if not np.isclose(np.linalg.det(A), 0):    # no usar == 0 (error numérico)
    A_inv = np.linalg.inv(A)
```

### Volumen de un paralelepípedo definido por vectores fila/columna
```python
M = np.array([[1, 0, 0],
              [0, 2, 0],
              [0, 0, 3]], dtype=float)
abs(np.linalg.det(M))    # 6.0  → |det| = volumen escalado
```

### Determinante de un lote de matrices (N-D, sin bucle)
```python
rot = np.random.rand(100, 3, 3)   # 100 matrices 3x3
d = np.linalg.det(rot)            # (100,)  → un determinante por matriz
(d != 0).all()                    # ¿todas invertibles?
```

### Lote 4D: una rejilla de determinantes $2\times 2$
Con dos ejes de lote, los **dos últimos ejes** colapsan a un escalar y sobreviven los dos primeros:
$4\times 5 = 20$ matrices $2\times 2$ dan una rejilla `(4, 5)` de determinantes, sin un solo `for`:

$$
\underbrace{(4,\,5,\,2,\,2)}_{\text{lote de matrices}}\ \xrightarrow{\ \det\ }\ \underbrace{(4,\,5)}_{\text{rejilla de escalares}}
$$

```python
A = np.random.rand(4, 5, 2, 2)   # (4, 5, 2, 2): 20 matrices 2x2
d = np.linalg.det(A)
d.shape                           # (4, 5)  → un determinante por matriz del lote
```

### Relación con los autovalores
El determinante es el **producto de los autovalores**, $\det A = \prod_i \lambda_i$. Por eso
$\det = 0$ equivale a tener algún autovalor nulo (y por tanto matriz singular):

```python
A = np.array([[2., 0.], [0., 3.]])
np.prod(np.linalg.eigvals(A))    # 6.0 + 0j  ≈ det(A) = 6
```

> [!warning] La trampa: overflow / underflow del determinante
> El determinante es un **producto** de $n$ pivotes, así que crece o decae **exponencialmente** con
> el tamaño. Para matrices grandes (o de valores muy dispares) `det` **desborda a `inf` o subdesborda
> a `0`** con facilidad, perdiendo toda la información:
> ```python
> M = np.eye(2000) * 10.0     # det "real" = 10**2000
> np.linalg.det(M)            # inf  → inútil
> ```
> Cuando solo necesitas la **magnitud** (o trabajas con $\log\det$, como en estadística), usa
> [[np.linalg.slogdet]], que devuelve signo y $\log|\det|$ sin desbordar.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions of the array must be square` | matriz no cuadrada | reformar a `(..., n, n)` |
| `det` da `inf` / `0` por overflow/underflow | producto de muchos pivotes en matriz grande | usar [[np.linalg.slogdet]] |
| `det == 0` exacto que nunca se cumple | comparación estricta con error numérico de la LU | `np.isclose(det, 0)` |
| Resolver un sistema vía regla de Cramer con `det` | lento e inestable | usar `np.linalg.solve` |
| Esperar un entero de una matriz entera | la LU devuelve flotante | el resultado es `float64`, redondea si hace falta |

## Notas relacionadas

- [[concepto_shape]] — los dos últimos ejes son la matriz; el resto es lote
- [[concepto_vectorizacion]] — el determinante de un lote sin bucle (LAPACK)
- [[np.linalg.slogdet]] — signo y $\log|\det|$, estable frente al overflow de `det`
- [[np.linalg.inv]] · [[np.linalg.solve]] · [[np.linalg.matrix_rank]] · [[np.linalg.eigvals]]
