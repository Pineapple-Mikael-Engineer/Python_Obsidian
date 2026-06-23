---
title: np.linalg.eig — autovalores y autovectores de una matriz general
aliases:
  - eig
  - linalg.eig
  - np.linalg.eig
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple (eigenvalues, eigenvectors)
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.eig — autovalores y autovectores de una matriz general

`np.linalg.eig` resuelve el **problema de autovalores** de una matriz cuadrada **general** (no
necesariamente simétrica): encuentra los escalares $\lambda$ y los vectores $\mathbf{v}\neq\mathbf{0}$
que la matriz solo **estira** sin girar. Devuelve dos cosas a la vez —los autovalores y los
autovectores— en una tupla con nombres. Es la herramienta detrás de la diagonalización, el análisis
de estabilidad de sistemas lineales y las frecuencias propias. Si tu matriz es
**simétrica/Hermítica**, no uses esta: usa [[np.linalg.eigh]], que es más rápida y estable.

## La idea en una fórmula

Un par autovalor–autovector $(\lambda, \mathbf{v})$ cumple la ecuación central: aplicar $A$ a
$\mathbf{v}$ equivale a escalar $\mathbf{v}$ por $\lambda$.

$$
A\,\mathbf{v} = \lambda\,\mathbf{v} \qquad \mathbf{v}\neq\mathbf{0}
$$

Para una matriz $n\times n$ hay $n$ pares. Apilando los autovectores como **columnas** de $V$ y los
autovalores en una diagonal $\Lambda=\operatorname{diag}(\lambda_0,\dots,\lambda_{n-1})$, la ecuación
se vuelve la **diagonalización**:

$$
A\,V = V\,\Lambda \qquad\Longrightarrow\qquad A = V\,\Lambda\,V^{-1}
$$

**El mapa de shapes** — la entrada `(...,n,n)` produce **dos** salidas, una `(...,n)` y otra
`(...,n,n)`:

$$
\underbrace{(n_0,\dots,n_{k-1},\,n,\,n)}_{A}\ \xrightarrow{\ \text{eig}\ }\ \big(\ \underbrace{(n_0,\dots,n_{k-1},\,n)}_{w}\ ,\ \underbrace{(n_0,\dots,n_{k-1},\,n,\,n)}_{v}\ \big)
$$

Los dos últimos ejes de $A$ son la matriz; los `…` anteriores son ejes de **lote**. Por cada matriz
del lote salen $n$ autovalores (vector) y una matriz $n\times n$ de autovectores en columnas.

$$
v = \begin{bmatrix} v_{00} & v_{01} \\ v_{10} & v_{11} \\ v_{20} & v_{21} \end{bmatrix}
\qquad
w = \begin{bmatrix} \lambda_0 & \lambda_1 & \lambda_2 \end{bmatrix}
$$

- `v[:, i]` = autovector $i$-ésimo (**COLUMNA**), norma 1.
- `w[i]` = autovalor del autovector `v[:, i]`.
- Relación: `A @ v[:, i] == w[i] * v[:, i]`.

## Firma

```python
np.linalg.eig(a) -> EigResult(eigenvalues, eigenvectors)
# a : array_like, shape (..., n, n) — matriz(ces) cuadrada(s) general(es)
```

## Los parámetros en detalle

### `a` — la(s) matriz(ces) de entrada
`array_like` de shape `(..., n, n)`: una matriz cuadrada o un **lote** de ellas apiladas en los ejes
anteriores. **No** requiere simetría. Acepta `dtype` real o complejo; con entrada real el resultado
**puede ser complejo** (ver abajo). No tiene más parámetros: `eig` no expone `out`, `UPLO` ni nada
configurable.

```python
lote = np.random.rand(5, 3, 3)   # 5 matrices 3×3 generales
w, v = np.linalg.eig(lote)
w.shape    # (5, 3)      → 3 autovalores por matriz
v.shape    # (5, 3, 3)   → matriz de autovectores por matriz
```

## El caso N-D

Igual que [[np.matmul]], `eig` trata los **dos últimos ejes** como la matriz y **todos los
anteriores como lote**. No hay `axis`: la operación es siempre sobre el bloque `(n, n)` final.

| `a.shape` | `w.shape` | `v.shape` | qué pasa |
|-----------|-----------|-----------|----------|
| `(n, n)` | `(n,)` | `(n, n)` | una sola descomposición |
| `(b, n, n)` | `(b, n)` | `(b, n, n)` | `b` descomposiciones independientes |
| `(b, c, n, n)` | `(b, c, n)` | `(b, c, n, n)` | lote 2D de matrices |

```python
lote = np.random.rand(8, 4, 4)
w, v = np.linalg.eig(lote)
# El par i de la matriz k:  lote[k] @ v[k][:, i] == w[k, i] * v[k][:, i]
np.allclose(lote @ v, v @ (w[..., None, :] * np.eye(4)))   # True (reconstrucción por lote)
```

## Vectorización

El caso por lotes es [[concepto_vectorizacion]] puro: una sola llamada descompone muchas matrices sin
bucle Python, delegando en **LAPACK** (rutina `geev`):

```python
# Bucle Python: una eig por matriz del lote
def batch_eig(A):
    ws, vs = [], []
    for k in range(A.shape[0]):
        w, v = np.linalg.eig(A[k])
        ws.append(w); vs.append(v)
    return np.array(ws), np.array(vs)

# Vectorizado: NumPy recorre el lote en C / LAPACK
w, v = np.linalg.eig(A)
```

## Valor de retorno

Devuelve un **namedtuple** `EigResult(eigenvalues, eigenvectors)`, es decir la tupla
`(autovalores, autovectores)` — desempaquetable como `w, v = np.linalg.eig(a)`.

| Posición | Nombre | Shape | Contenido |
|----------|--------|-------|-----------|
| 0 | `eigenvalues` (`w`) | `(..., n)` | los $n$ autovalores, **1D por matriz**, **sin orden garantizado**. Pueden ser **complejos aunque `a` sea real** |
| 1 | `eigenvectors` (`v`) | `(..., n, n)` | matriz cuyas **columnas** son los autovectores: `v[..., :, i]` corresponde a `w[..., i]`, normalizado a norma 1 |

> [!warning] Los autovectores son las COLUMNAS de `v`
> El autovector del autovalor `w[i]` es `v[:, i]`, **no** `v[i]` (que es una fila). Este es el error
> clásico. Además los autovectores vienen **normalizados** (norma 1) y su signo/fase no está fijado.

- **Complejos desde una matriz real:** una rotación real tiene autovalores complejos conjugados. Si
  `a` es real con autovalores reales, `w` puede salir igualmente con `dtype` complejo (parte
  imaginaria nula).
- **Orden:** `eig` **no** ordena `w`. Para ordenar, `idx = np.argsort(w)` y reindexar `w` y las
  columnas de `v`.

```python
a = np.array([[4.0, 1.0],
              [2.0, 3.0]])
w, v = np.linalg.eig(a)
v[:, 0]                               # autovector de w[0] (COLUMNA)
np.allclose(a @ v, v @ np.diag(w))    # True → A V = V Λ

r = np.array([[0.0, -1.0],
              [1.0,  0.0]])           # rotación real
np.linalg.eig(r).eigenvalues          # array([0.+1.j, 0.-1.j]) → complejos
```

## Casos de uso

### Diagonalización para potencias de matriz
```python
a = np.array([[2.0, 0.0], [0.0, 0.5]])
w, v = np.linalg.eig(a)
a_10 = v @ np.diag(w**10) @ np.linalg.inv(v)   # a**10 barato vía Λ
```

### Estabilidad de un sistema lineal `x' = A x`
```python
A = np.array([[-1.0, 2.0], [0.0, -3.0]])
estable = np.all(np.linalg.eig(A).eigenvalues.real < 0)   # True → estable
```

### Lote de matrices (N-D): descomponer muchas a la vez
```python
lote = np.random.rand(100, 3, 3)
w, v = np.linalg.eig(lote)            # w:(100,3)  v:(100,3,3)
radios = np.abs(w).max(axis=1)        # radio espectral de cada matriz → (100,)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | comprobar `a.shape[-1] == a.shape[-2]` |
| Autovector equivocado | usar `v[i]` (fila) en vez de `v[:, i]` (columna) | indexar por **columna** |
| Resultado complejo inesperado | matriz real con autovalores complejos | es correcto; usa `eigh` si `a` es simétrica |
| Autovalores en orden raro | `eig` no ordena | `np.argsort(w)` y reindexar `v` por columnas |
| Imprecisión/lentitud en simétricas | usar `eig` en matriz simétrica | usar [[np.linalg.eigh]] |

## Notas relacionadas

- [[concepto_shape]] — razonar el lote `(..., n, n)` y el mapa a las dos salidas
- [[np.linalg.eigh]] — versión para matrices simétricas/Hermíticas (preferida si aplica)
- [[np.linalg.eigvals]] — solo los autovalores, sin los autovectores
- [[np.linalg.eigvalsh]] · [[np.trace]] · [[np.linalg.det]]
