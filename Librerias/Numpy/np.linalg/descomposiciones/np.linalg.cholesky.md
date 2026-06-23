---
title: np.linalg.cholesky — factoriza una matriz SPD como A = L Lᴴ
aliases:
  - cholesky
  - linalg.cholesky
  - np.linalg.cholesky
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray (L triangular inferior)
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.cholesky — factoriza una matriz SPD como A = L Lᴴ

`np.linalg.cholesky` **descompone** una matriz **hermítica definida positiva** $A$ en el producto
$A = L\,L^{*}$, donde $L$ es **triangular inferior** (ceros por encima de la diagonal). Es la
factorización más barata del álgebra lineal numérica —el doble de rápida que una LU porque explota la
simetría— y es la herramienta estándar para resolver sistemas con matrices de covarianza, muestrear
gaussianas multivariantes y, de paso, **comprobar** si una matriz es definida positiva (si no lo es,
falla). A diferencia de una reducción como [[np.sum]], esta función no colapsa un eje: **parte** una
matriz en un factor con estructura del que se reconstruye el original.

## La idea en una fórmula

Cholesky busca el factor triangular inferior $L$ tal que, al multiplicarlo por su traspuesta
conjugada, recupera $A$:

$$
A = L\,L^{*} \qquad L \text{ triangular inferior},\quad L^{*} = L^{H} = \overline{L}^{\,T}
$$

El **mapa de shapes** mantiene la dimensión —descompone una matriz cuadrada en otra del mismo tamaño,
en [[concepto_shape|lote]] sobre los ejes previos:

$$
(n_0,\dots,n_{k-1},\, n,\, n)\ \xrightarrow{\ \text{cholesky}\ }\ L\,(n_0,\dots,n_{k-1},\, n,\, n)
$$

Por índices, cada entrada de $L$ se obtiene por sustitución hacia adelante (los elementos por encima
de la diagonal son cero):

$$
L_{jj} = \sqrt{A_{jj} - \sum_{k<j} |L_{jk}|^2}
\qquad
L_{ij} = \frac{1}{L_{jj}}\Bigl(A_{ij} - \sum_{k<j} L_{ik}\,\overline{L_{jk}}\Bigr)\ (i>j)
$$

Visualmente, una $A$ de $(3\times 3)$ se factoriza en un triángulo inferior y su espejo superior:

$$
\underbrace{\begin{bmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \\ a_{20} & a_{21} & a_{22} \end{bmatrix}}_{A\ (n\times n)}
=
\underbrace{\begin{bmatrix} l_{00} & 0 & 0 \\ l_{10} & l_{11} & 0 \\ l_{20} & l_{21} & l_{22} \end{bmatrix}}_{L\ (n\times n)}
\underbrace{\begin{bmatrix} l_{00} & l_{10} & l_{20} \\ 0 & l_{11} & l_{21} \\ 0 & 0 & l_{22} \end{bmatrix}}_{L^{H}\ (n\times n)}
$$

## Firma

```python
np.linalg.cholesky(
    a,                 # array_like: matriz (..., n, n) hermítica definida positiva
    /,
    *,
    upper=False,       # bool (NumPy 2.0+): si True devuelve la triangular superior
) -> ndarray
```

## Los parámetros en detalle

### `a` — la matriz de entrada
`array_like` de [[concepto_shape|shape]] `(..., n, n)` que debe ser **hermítica definida positiva**
(simétrica definida positiva en el caso real). Los dos últimos ejes son la matriz; los `…` anteriores
son lote. NumPy **solo lee el triángulo inferior** de `a` (el superior se ignora), pero la matriz debe
ser realmente definida positiva: si algún autovalor es $\le 0$, lanza `LinAlgError`.

```python
A = np.array([[4.0, 2.0],
              [2.0, 3.0]])      # simétrica definida positiva
L = np.linalg.cholesky(A)       # (2, 2), triangular inferior
```

### `upper` — qué triángulo devolver (NumPy 2.0+)
`bool`, defecto `False`. Por defecto devuelve el factor **inferior** $L$ con $A = L\,L^{*}$. Con
`upper=True` devuelve el factor **superior** $U = L^{*}$ con $A = U^{*}\,U$. En versiones anteriores a
NumPy 2.0 el parámetro no existe: para la superior, transpón y conjuga el resultado (`L.conj().T`).

```python
np.linalg.cholesky(A, upper=True)   # triangular superior U, con A = Uᴴ U
```

## El caso N-D

La factorización se aplica **a los dos últimos ejes** `(n, n)` y trata todos los ejes anteriores como
un **lote**: dada una pila `(..., n, n)`, NumPy factoriza cada matriz cuadrada por separado y apila los
resultados con el mismo shape. No hay broadcasting de factores: cada matriz del lote produce su propio
$L$.

| `a.shape` | salida `L.shape` | lectura |
|-----------|------------------|---------|
| `(n, n)` | `(n, n)` | una sola factorización |
| `(b, n, n)` | `(b, n, n)` | `b` factorizaciones independientes |
| `(b, c, n, n)` | `(b, c, n, n)` | lote 2D: `b·c` matrices `(n, n)` |

```python
lote = np.array([[[2.0, 0.0], [0.0, 2.0]],
                 [[4.0, 1.0], [1.0, 3.0]]])   # 2 matrices 2×2 SPD
L = np.linalg.cholesky(lote)
L.shape                                       # (2, 2, 2)  → un L por matriz
```

## Vectorización

El lote de Cholesky es [[concepto_vectorizacion|vectorización]] pura: en vez de un bucle Python que
llama a `cholesky` matriz por matriz, NumPy recorre el lote en código compilado y delega cada
factorización en **LAPACK** (`potrf`). El contraste:

```python
# Bucle Python: una llamada LAPACK por matriz, con salto al intérprete
def chol_lote(stack):
    out = np.empty_like(stack)
    for i in range(stack.shape[0]):
        out[i] = np.linalg.cholesky(stack[i])
    return out

# Vectorizado: NumPy itera el lote en C sobre los dos últimos ejes
np.linalg.cholesky(stack)
```

Mismo resultado; la versión vectorizada evita `stack.shape[0]` saltos al intérprete.

## Valor de retorno

Devuelve un **único ndarray** `L` (no una tupla, a diferencia de [[np.linalg.qr]] o
[[np.linalg.svd]]), triangular inferior, tal que `a == L @ L.conj().T`:

| Salida | Shape | Propiedad |
|--------|-------|-----------|
| `L` (`upper=False`) | `(..., n, n)` | triangular **inferior**, `a = L @ L.conj().T` |
| `U` (`upper=True`) | `(..., n, n)` | triangular **superior**, `a = U.conj().T @ U` |

El `dtype` es de punto flotante (`float64` o `complex128` según la entrada); enteros se promueven a
`float64`.

```python
A = np.array([[4.0, 2.0], [2.0, 3.0]])
L = np.linalg.cholesky(A)
L
# [[2.        , 0.        ],
#  [1.        , 1.41421356]]        → triangular inferior
np.allclose(A, L @ L.T)            # True  (datos reales: L Lᵀ)
```

## Casos de uso

### Ejemplo trabajado con números
La $A$ de $(2\times 2)$ SPD del resto de la nota se factoriza en un triángulo inferior concreto. Como
$L_{00}=\sqrt{4}=2$, $L_{10}=2/2=1$ y $L_{11}=\sqrt{3-1^2}=\sqrt{2}$:

$$
A=\begin{bmatrix} 4 & 2 \\ 2 & 3 \end{bmatrix}
= L\,L^{T},\qquad
L=\begin{bmatrix} 2 & 0 \\ 1 & \sqrt{2} \end{bmatrix},\quad
L^{T}=\begin{bmatrix} 2 & 1 \\ 0 & \sqrt{2} \end{bmatrix}
$$

Comprobación del producto $L\,L^{T}$: $\begin{bmatrix}2\cdot2 & 2\cdot1\\ 1\cdot2 & 1\cdot1+2\end{bmatrix}=\begin{bmatrix}4&2\\2&3\end{bmatrix}=A$.

```python
A = np.array([[4.0, 2.0], [2.0, 3.0]])
L = np.linalg.cholesky(A)
L                                 # [[2., 0.], [1., 1.41421356]]  → √2 ≈ 1.4142
np.allclose(A, L @ L.T)           # True
```

### Resolver un sistema SPD de forma eficiente
```python
# A x = b con A definida positiva: dos sustituciones triangulares
L = np.linalg.cholesky(A)
y = np.linalg.solve(L, b)             # L y = b   (triangular inferior)
x = np.linalg.solve(L.conj().T, y)    # Lᴴ x = y  (triangular superior)
```

### Muestrear de una gaussiana multivariante
```python
# x ~ N(mu, Sigma): L "colorea" ruido blanco con la covarianza deseada
L = np.linalg.cholesky(Sigma)
z = np.random.standard_normal(mu.shape)
x = mu + L @ z                        # tiene covarianza Sigma
```

### Comprobar si una matriz es definida positiva
```python
def es_definida_positiva(M):
    try:
        np.linalg.cholesky(M)
        return True
    except np.linalg.LinAlgError:
        return False
```

### Lote de covarianzas (N-D)
```python
# 3D: factorizar 100 matrices de covarianza 3×3 de golpe
Sigmas = np.random.rand(100, 3, 3)
Sigmas = Sigmas @ Sigmas.transpose(0, 2, 1) + 3 * np.eye(3)  # SPD por construcción
Ls = np.linalg.cholesky(Sigmas)
Ls.shape                              # (100, 3, 3)  → un L por matriz, sin bucle

# 4D: lote (8, 5) de matrices 3×3  → 40 factorizaciones independientes
S4 = np.random.rand(8, 5, 3, 3)
S4 = S4 @ S4.transpose(0, 1, 3, 2) + 3 * np.eye(3)           # (8, 5, 3, 3) SPD
L4 = np.linalg.cholesky(S4)
L4.shape                              # (8, 5, 3, 3)  → mismo shape que la entrada
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Matrix is not positive definite` | la matriz no es SPD (autovalor $\le 0$) | verificar con [[np.linalg.eigvalsh]]; regularizar sumando `εI` |
| Resultado inesperado | matriz no simétrica (solo se lee el triángulo inferior) | simetrizar: `A = (A + A.T) / 2` |
| Esperar la triangular superior | por defecto se devuelve `L` **inferior** | usar `upper=True` (NumPy 2.0+) o `L.conj().T` |
| `LinAlgError` por redondeo | SPD teórica pero numéricamente indefinida | añadir un pequeño jitter en la diagonal (`εI`) |
| `LinAlgError: Last 2 dimensions...` | entrada no cuadrada o de menos de 2D | pasar una matriz cuadrada `(..., n, n)` |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes `(..., n, n) → (..., n, n)`
- [[concepto_vectorizacion]] — por qué el lote de factorizaciones evita el bucle
- [[Librerias/Numpy/np.linalg/descomposiciones/index|descomposiciones]] — la familia completa
- [[np.linalg.solve]] · [[np.linalg.eigvalsh]] · [[np.linalg.qr]] · [[np.linalg.svd]]
