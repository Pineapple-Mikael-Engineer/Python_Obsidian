---
title: np.linalg.svd — factoriza A = U Σ Vᴴ (la descomposición universal)
aliases:
  - svd
  - linalg.svd
  - np.linalg.svd
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple (U, S, Vh) o ndarray (S)
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.svd — factoriza A = U Σ Vᴴ (la descomposición universal)

`np.linalg.svd` **descompone** una matriz $A$ en tres factores, $A = U\,\Sigma\,V^{H}$, con $U$ y $V$
ortonormales y $\Sigma$ diagonal de **valores singulares** no negativos. Es la descomposición más
general y estable del álgebra lineal: existe para **cualquier** matriz (cuadrada o no, singular o no) y
es la base del rango numérico, la pseudo-inversa, PCA y la compresión de rango bajo. Devuelve **tres
objetos** (`U, S, Vh`), donde `S` es un vector 1D con los valores singulares —no una matriz—; los
parámetros `full_matrices` y `compute_uv` cambian los shapes y se desambiguan en tablas.

## La idea en una fórmula

La SVD escribe $A$ como una rotación ($V^{H}$), un escalado por ejes ($\Sigma$) y otra rotación ($U$):

$$
A = U\,\Sigma\,V^{H} \qquad U^{H}U = I,\quad V^{H}V = I,\quad \Sigma = \mathrm{diag}(\sigma_1 \ge \dots \ge \sigma_k \ge 0)
$$

El **mapa de shapes** (con $k = \min(m, n)$); nótese que `S` es **1D** y `Vh` ya es la conjugada
traspuesta:

$$
(\underbrace{\dots}_{\text{lote}},\, m,\, n)\ \xrightarrow{\ \text{svd}\ }\
U\,(\dots,\, m,\, m\,|\,k),\ \ S\,(\dots,\, k),\ \ V\!h\,(\dots,\, n\,|\,k,\, n)
\qquad k=\min(m,n)
$$

(las dos opciones de $U$/$V\!h$ son `full_matrices=True` | `False`). Por índices, $A$ es una suma de
$k$ productos externos ponderados por los valores singulares:

$$
A = \sum_{r=1}^{k} \sigma_r\, u_r\, v_r^{H}
$$

Truncar esa suma a los primeros componentes da la **mejor aproximación de rango bajo** (base de la
compresión). Visualmente, una $A$ de $(2\times 3)$:

$$
\underbrace{\begin{bmatrix} a_{00} & a_{01} & a_{02} \\ a_{10} & a_{11} & a_{12} \end{bmatrix}}_{A\ (2\times 3)}
=
\underbrace{\begin{bmatrix} u_{00} & u_{01} \\ u_{10} & u_{11} \end{bmatrix}}_{U\ (2\times 2)\ \text{ortonormal}}
\underbrace{\begin{bmatrix} \sigma_0 & 0 & 0 \\ 0 & \sigma_1 & 0 \end{bmatrix}}_{\Sigma\ (2\times 3)\ \sigma\ \text{descendente}}
\underbrace{\begin{bmatrix} v_{00} & v_{01} & v_{02} \\ v_{10} & v_{11} & v_{12} \\ v_{20} & v_{21} & v_{22} \end{bmatrix}}_{V\!h\ (3\times 3)}
$$

## Firma

```python
np.linalg.svd(
    a,                    # array_like: matriz (..., m, n)
    full_matrices=True,   # bool: U y Vh cuadradas (True) o recortadas a k (False)
    compute_uv=True,      # bool: si False devuelve solo S
    hermitian=False,      # bool: asume a hermítica → algoritmo más eficiente
) -> tuple[ndarray, ndarray, ndarray] | ndarray
```

## Los parámetros en detalle

### `a` — la matriz de entrada
`array_like` de [[concepto_shape|shape]] `(..., m, n)`, de cualquier forma. Los dos últimos ejes son la
matriz; los `…` anteriores son lote. Enteros se promueven a `float64`.

```python
A = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])      # (2, 3)
U, S, Vh = np.linalg.svd(A)
```

### `full_matrices` — tamaño de `U` y `Vh`
`bool`, defecto `True`. Con `True`, `U` y `Vh` son cuadradas completas `(..., m, m)` / `(..., n, n)`.
Con `False`, se recortan a `(..., m, k)` / `(..., k, n)` —la **forma reducida (thin SVD)**, más barata
y suficiente para reconstruir `a`—. Importa mucho cuando $m$ y $n$ difieren: evita construir matrices
enormes.

```python
A = np.random.rand(100, 5)
U, S, Vh = np.linalg.svd(A, full_matrices=False)
U.shape    # (100, 5)  en vez de (100, 100)  → mucho más ligero
```

### `compute_uv` — calcular o no los vectores singulares
`bool`, defecto `True`. Si `False`, omite `U` y `Vh` y devuelve **solo** `S` (un único ndarray, no una
tupla). Útil cuando solo hacen falta los valores singulares (rango, norma 2, número de condición). Es
exactamente lo que calcula [[np.linalg.svdvals]] de forma directa.

```python
S = np.linalg.svd(A, compute_uv=False)   # devuelve un solo array, no tupla
rango = np.sum(S > 1e-10)                # rango numérico
cond  = S[0] / S[-1]                      # número de condición
```

### `hermitian` — optimización para matrices hermíticas
`bool`, defecto `False`. Si `True`, asume que `a` es hermítica (simétrica si es real) y usa un
algoritmo basado en autovalores, más eficiente y preciso. Solo úsalo si la matriz lo es de verdad.

## El caso N-D

La descomposición se aplica **a los dos últimos ejes** `(m, n)` y trata los anteriores como **lote**:
NumPy hace la SVD de cada matriz por separado y apila `U`, `S` (1D) y `Vh`. `S` gana un eje por cada
eje de lote, no por la matriz.

| `a.shape` | `full_matrices` | `U.shape` | `S.shape` | `Vh.shape` |
|-----------|-----------------|-----------|-----------|------------|
| `(m, n)` | `True` | `(m, m)` | `(k,)` | `(n, n)` |
| `(m, n)` | `False` | `(m, k)` | `(k,)` | `(k, n)` |
| `(b, m, n)` | `False` | `(b, m, k)` | `(b, k)` | `(b, k, n)` |

```python
lote = np.random.rand(5, 3, 4)   # 5 matrices 3×4
U, S, Vh = np.linalg.svd(lote)
S.shape                          # (5, 3)  → un vector de 3 valores singulares por matriz
```

## Vectorización

El lote de SVD es [[concepto_vectorizacion|vectorización]]: NumPy recorre los ejes previos en código
compilado y delega cada factorización en **LAPACK** (`gesdd`), sin un bucle Python por matriz:

```python
# Bucle Python: una SVD por matriz, con salto al intérprete
def svd_lote(stack):
    out = []
    for i in range(stack.shape[0]):
        out.append(np.linalg.svd(stack[i], full_matrices=False))
    return out

# Vectorizado: NumPy itera el lote sobre los dos últimos ejes
U, S, Vh = np.linalg.svd(stack, full_matrices=False)
```

## Valor de retorno

El retorno **depende de `compute_uv`**. Con `True` (defecto) es una **tupla de 3 arrays**; con `False`,
**solo** `S`. Para `a` de shape `(m, n)` y $k = \min(m, n)$:

| `compute_uv` | `full_matrices` | objetos | shapes |
|--------------|-----------------|---------|--------|
| `True` | `True` | `(U, S, Vh)` | `U (m, m)`, `S (k,)`, `Vh (n, n)` |
| `True` | `False` | `(U, S, Vh)` | `U (m, k)`, `S (k,)`, `Vh (k, n)` |
| `False` | — | `S` (un ndarray) | `S (k,)` |

`S` es **1D** con valores **reales $\ge 0$ en orden descendente**; `Vh` es ya $V^{H}$ (conjugada
traspuesta), **no** `V`. `dtype` de punto flotante; `S` siempre real aunque `a` sea compleja.

```python
A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])   # (2, 3)
U, S, Vh = np.linalg.svd(A)
U.shape, S.shape, Vh.shape        # (2, 2), (2,), (3, 3)

# Reconstrucción: a = U @ diag(S) @ Vh  (S no es matriz; hay que enmarcarlo en Σ)
Sigma = np.zeros((2, 3))
Sigma[:2, :2] = np.diag(S)
np.allclose(A, U @ Sigma @ Vh)    # True
# Para obtener V (no Vh): V = Vh.conj().T
```

## Casos de uso

### Pseudo-inversa de Moore-Penrose
```python
A = np.random.rand(4, 3)
U, S, Vh = np.linalg.svd(A, full_matrices=False)
A_pinv = Vh.conj().T @ np.diag(1.0 / S) @ U.conj().T
# equivalente directo: np.linalg.pinv(A)
```

### Compresión / aproximación de rango bajo
```python
U, S, Vh = np.linalg.svd(imagen, full_matrices=False)
k = 20                                  # conservar 20 componentes
aprox = U[:, :k] @ np.diag(S[:k]) @ Vh[:k, :]
```

### Rango numérico y número de condición
```python
S = np.linalg.svd(M, compute_uv=False)
rango = np.count_nonzero(S > S.max() * 1e-12)
cond  = S[0] / S[-1]
```

### PCA por SVD (datos centrados)
```python
X = X - X.mean(axis=0)                   # centrar (n muestras × d features)
U, S, Vh = np.linalg.svd(X, full_matrices=False)
componentes = Vh                         # direcciones principales (filas)
scores = U * S                           # proyección de cada muestra
```

### Lote de SVD (N-D)
```python
stack = np.random.rand(8, 6, 4)          # 8 matrices 6×4
U, S, Vh = np.linalg.svd(stack, full_matrices=False)
S.shape                                  # (8, 4)  → 8 vectores singulares, sin bucle
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: SVD did not converge` | datos con `NaN`/`inf` o caso patológico | limpiar entradas; comprobar `np.isfinite(a).all()` |
| Reconstrucción no coincide | usar `V` en vez de `Vh`, o `diag(S)` mal dimensionado | reconstruir con `U @ Sigma @ Vh` y `Sigma` del shape correcto |
| `U`/`Vh` enormes en memoria | `full_matrices=True` con matriz muy rectangular | `full_matrices=False` |
| `ValueError` al desempaquetar | `compute_uv=False` devuelve solo `S`, no una tupla | asignar a una sola variable |
| `LinAlgError: Last 2 dimensions...` | entrada de menos de 2 dimensiones | pasar al menos una matriz 2D |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes y por qué `S` es 1D
- [[concepto_vectorizacion]] — el lote de SVD sin bucle (LAPACK)
- [[Librerias/Numpy/np.linalg/descomposiciones/index|descomposiciones]] — la familia completa
- [[np.linalg.svdvals]] · [[np.linalg.qr]] · [[np.linalg.cholesky]] · [[np.linalg.pinv]] · [[np.linalg.matrix_rank]]
