---
title: np.linalg.svdvals — solo los valores singulares de una matriz
aliases:
  - svdvals
  - linalg.svdvals
  - np.linalg.svdvals
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray (valores singulares, 1D)
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.svdvals — solo los valores singulares de una matriz

`np.linalg.svdvals` (NumPy 2.0+) calcula **únicamente los valores singulares** de una matriz $A$, sin
los vectores singulares $U$ y $V$. Es exactamente `svd(a, compute_uv=False)` con un nombre propio y una
firma mínima: devuelve un vector 1D con los $\sigma_i$ **reales $\ge 0$ ordenados de forma
descendente**. Se usa cuando solo importan las magnitudes —rango numérico, número de condición, norma
espectral— y construir $U$/$V\!h$ sería un gasto inútil. Es la versión "barata" de [[np.linalg.svd]].

## La idea en una fórmula

Los valores singulares son la diagonal de $\Sigma$ en la SVD $A = U\,\Sigma\,V^{H}$; `svdvals` extrae
solo esa lista:

$$
\sigma(A) = (\sigma_1 \ge \sigma_2 \ge \dots \ge \sigma_k \ge 0),\qquad k=\min(m,n)
$$

El **mapa de shapes**: colapsa los dos ejes de la matriz a un único eje de longitud $k$, en
[[concepto_shape|lote]] sobre los ejes previos:

$$
(\underbrace{\dots}_{\text{lote}},\, m,\, n)\ \xrightarrow{\ \text{svdvals}\ }\ (\underbrace{\dots}_{\text{lote}},\, \min(m, n))
$$

Equivalencia exacta: $\sigma_i = \sqrt{\lambda_i(A^{H}A)}$, las raíces de los autovalores de
$A^{H}A$ (de ahí que sean reales y no negativos para cualquier $A$).

## Firma

```python
np.linalg.svdvals(
    x,                 # array_like: matriz (..., m, n)
    /,
) -> ndarray
```

## Los parámetros en detalle

### `x` — la matriz de entrada
`array_like` de [[concepto_shape|shape]] `(..., m, n)`, de cualquier forma (no tiene que ser cuadrada).
Es un parámetro **posicional únicamente** (sigue la API de array estándar). Los dos últimos ejes son la
matriz; los `…` anteriores son lote. Enteros se promueven a `float64`. No hay más parámetros: para
elegir tamaños de `U`/`Vh` o reconstruir, hay que usar [[np.linalg.svd]].

```python
A = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0]])      # (2, 3)
np.linalg.svdvals(A)                # [9.508, 0.773]  aprox, descendente
```

## El caso N-D

Se aplica **a los dos últimos ejes** `(m, n)` y trata los anteriores como **lote**: cada matriz produce
su propio vector de $\min(m, n)$ valores singulares, y todos se apilan.

| `x.shape` | salida | lectura |
|-----------|--------|---------|
| `(m, n)` | `(min(m, n),)` | un vector de valores singulares |
| `(b, m, n)` | `(b, min(m, n))` | `b` vectores, uno por matriz |
| `(b, c, m, n)` | `(b, c, min(m, n))` | lote 2D de matrices |

```python
lote = np.random.rand(5, 3, 4)   # 5 matrices 3×4
np.linalg.svdvals(lote).shape    # (5, 3)  → min(3,4)=3 valores por matriz
```

## Vectorización

Igual que la SVD completa, el lote es [[concepto_vectorizacion|vectorización]]: NumPy recorre los ejes
de lote en código compilado y delega cada cálculo en **LAPACK**, sin bucle Python por matriz:

```python
# Bucle Python: un cálculo por matriz, con salto al intérprete
def svals_lote(stack):
    out = np.empty((stack.shape[0], min(stack.shape[1:])))
    for i in range(stack.shape[0]):
        out[i] = np.linalg.svdvals(stack[i])
    return out

# Vectorizado: NumPy itera el lote sobre los dos últimos ejes
np.linalg.svdvals(stack)
```

## Valor de retorno

Devuelve un **único ndarray 1D** (por lote, `(..., k)`) con los valores singulares **reales $\ge 0$ en
orden descendente**:

| `x.shape` | salida | dtype |
|-----------|--------|-------|
| `(m, n)` | `(min(m, n),)` | `float64` (o `float32` si la entrada lo es) |
| `(..., m, n)` | `(..., min(m, n))` | flotante real, **siempre** (aunque `x` sea complejo) |

A diferencia de [[np.linalg.svd]], no devuelve tupla: es directo equiparar con
`svd(x, compute_uv=False)`.

```python
A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
s = np.linalg.svdvals(A)
np.allclose(s, np.linalg.svd(A, compute_uv=False))   # True
s[0]                                                 # el mayor (norma espectral)
```

## Casos de uso

### Rango numérico
```python
s = np.linalg.svdvals(M)
rango = np.count_nonzero(s > s.max() * 1e-12)   # tolerancia relativa
```

### Número de condición (norma 2)
```python
s = np.linalg.svdvals(A)
cond = s[0] / s[-1]              # σ_max / σ_min  → equivale a np.linalg.cond(A)
```

### Norma espectral (norma 2 de la matriz)
```python
norma2 = np.linalg.svdvals(A)[0]   # el mayor valor singular
```

### Lote: condicionamiento de muchas matrices (N-D)
```python
stack = np.random.rand(100, 6, 6)
s = np.linalg.svdvals(stack)        # (100, 6)
conds = s[:, 0] / s[:, -1]          # número de condición de cada una, sin bucle
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: SVD did not converge` | datos con `NaN`/`inf` o caso patológico | limpiar entradas; comprobar `np.isfinite(x).all()` |
| `AttributeError: module ... has no attribute 'svdvals'` | NumPy anterior a 2.0 | usar `np.linalg.svd(x, compute_uv=False)` |
| Esperar `U`/`Vh` de vuelta | `svdvals` **solo** da los valores singulares | usar [[np.linalg.svd]] si necesitas los vectores |
| `LinAlgError: Last 2 dimensions...` | entrada de menos de 2 dimensiones | pasar al menos una matriz 2D |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes `(..., m, n) → (..., min(m, n))`
- [[concepto_vectorizacion]] — el lote de valores singulares sin bucle (LAPACK)
- [[Librerias/Numpy/np.linalg/descomposiciones/index|descomposiciones]] — la familia completa
- [[np.linalg.svd]] · [[np.linalg.matrix_rank]] · [[np.linalg.cond]] · [[np.linalg.norm]]
