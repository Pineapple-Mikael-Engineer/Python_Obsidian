---
title: np.linalg.matrix_transpose — transpone los dos últimos ejes (consciente de lotes)
aliases:
  - matrix_transpose
  - linalg.matrix_transpose
  - np.matrix_transpose
  - np.linalg.matrix_transpose
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.matrix_transpose — transpone los dos últimos ejes (consciente de lotes)

`np.linalg.matrix_transpose` (≡ `np.matrix_transpose`, añadida en **NumPy 2.0**) intercambia los
**dos últimos ejes** de un array, dejando intactos los ejes anteriores. Es la transpuesta **consciente
de lotes**: en un stack $(n_0,\dots,n_{k-1}, m, n)$ transpone cada matriz por separado y conserva los ejes de
lote. Esa es exactamente su diferencia con `.T` / [[np.transpose]], que invierten **todos** los ejes y
por tanto **mezclan el lote** en N-D. Equivale a `np.swapaxes(x, -1, -2)`. Es la transpuesta que
quieres siempre que trabajes con pilas de matrices.

## La idea en una fórmula

Transponer una matriz intercambia filas y columnas: $(A^{\mathsf T})_{ij} = A_{ji}$. En N-D la regla
solo toca los **dos últimos ejes** (los que representan la matriz):

$$
B_{\,\dots,\, i,\, j} = A_{\,\dots,\, j,\, i}
$$

**El mapa de shapes** — los ejes de lote $n_0,\dots,n_{k-1}$ quedan intactos y solo se permutan los dos últimos:

$$
(n_0,\dots,n_{k-1},\, m,\, n)\ \xrightarrow{\ \text{matrix\_transpose}\ }\ (n_0,\dots,n_{k-1},\, n,\, m)
$$

Contrástalo con `.T`, que aplica la permutación que **invierte la tupla entera** de ejes:

$$
(d_0, d_1, \dots, d_{k-1})\ \xrightarrow{\ .T\ }\ (d_{k-1}, \dots, d_1, d_0)
$$

En 2D ambas coinciden ($(m,n)\to(n,m)$); en 3D+ **no**: para $(b, m, n)$, `matrix_transpose` da
$(b, n, m)$ pero `.T` da $(n, m, b)$ —arrastra el eje de lote al final y rompe la semántica de "lote de
matrices".

## Firma

```python
np.linalg.matrix_transpose(x, /) -> ndarray
```

## Los parámetros en detalle

### `x` — el array a transponer
`array_like` con `ndim >= 2`. Los **dos últimos ejes** se interpretan como la matriz $(m, n)$ y se
intercambian; **todos los ejes anteriores** son lote y se preservan en su sitio. Un array 1D lanza
`ValueError` (no hay dos ejes que permutar). Cuando es posible devuelve una **vista** (solo reordena
strides, no copia datos).

```python
A = np.arange(6).reshape(2, 3)
np.linalg.matrix_transpose(A)
# [[0, 3],
#  [1, 4],
#  [2, 5]]   → shape (3, 2)
```

## El caso N-D

Aquí está la clave de la función. En un stack, transpone **cada matriz del lote** sin tocar los ejes
previos, a diferencia de `.T`:

| `x.shape` | `matrix_transpose(x)` | `x.T` | comentario |
|-----------|------------------------|-------|------------|
| `(m, n)` | `(n, m)` | `(n, m)` | en 2D **coinciden** |
| `(b, m, n)` | `(b, n, m)` ✅ | `(n, m, b)` ⚠️ | `.T` arrastra el lote al final |
| `(p, q, m, n)` | `(p, q, n, m)` ✅ | `(n, m, q, p)` ⚠️ | `.T` invierte los 4 ejes |

```python
T = np.ones((10, 2, 3))                 # 10 matrices 2x3
np.linalg.matrix_transpose(T).shape     # (10, 3, 2)  → por lotes, correcto
T.T.shape                               # (3, 2, 10)  → invierte TODO, mezcla el lote
```

Para entender por qué difieren, razona en términos de [[concepto_shape]]: `.T` revierte la tupla
completa de ejes; `matrix_transpose` solo permuta los dos que representan la matriz.

## Vectorización

`matrix_transpose` aplica la transposición a **todo el lote** sin un `for` por matriz: como solo
reordena strides, es una operación de metadatos (típicamente $O(1)$, sin copiar memoria). El bucle
Python equivalente sería:

```python
# Bucle Python: transponer matriz a matriz
def transpose_loop(T):
    return np.stack([T[i].T for i in range(T.shape[0])])

# Vectorizado: una reordenación de strides para todo el lote
np.linalg.matrix_transpose(T)
```

La versión vectorizada evita el bucle y la copia; encadena de forma natural con [[np.matmul]] para
expresar operaciones como $A^{\mathsf T} A$ por lotes.

## Valor de retorno

| `x.shape` | salida | tipo |
|-----------|--------|------|
| `(m, n)` | `(n, m)` | `ndarray` (vista cuando es posible) |
| `(b, m, n)` | `(b, n, m)` | `ndarray` (vista) |
| `(..., m, n)` | `(..., n, m)` | `ndarray` (vista) |

- Conserva el `dtype` exacto (no calcula nada, solo reordena ejes).
- **No conjuga**: para complejos transpone pero deja el conjugado intacto (la transpuesta hermitiana
  $A^{\mathsf H}$ es `matrix_transpose(x).conj()`).
- Devuelve una **vista** que comparte el buffer con `x` siempre que el reordenamiento de strides lo
  permita.

## Casos de uso

### Transponer una matriz concreta $(2,3)\to(3,2)$
Sobre una matriz $2\times 3$ con números, la transpuesta intercambia filas por columnas
$(B_{ij} = A_{ji})$ y el shape pasa de $(2, 3)$ a $(3, 2)$:

$$
A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
\qquad
\text{matrix\_transpose}(A) = \begin{bmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}
$$

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])                 # shape (2, 3)
np.linalg.matrix_transpose(A)
# [[1, 4],
#  [2, 5],
#  [3, 6]]                                # shape (3, 2)
```

### Transponer un stack de matrices sin tocar el eje de lote
```python
batch = np.random.rand(32, 4, 5)               # 32 matrices 4x5
batch_t = np.linalg.matrix_transpose(batch)    # (32, 5, 4)  → lote intacto
```

### Construir productos del tipo $A^{\mathsf T} A$ por lotes
```python
A = np.random.rand(8, 4, 3)
AtA = np.matmul(np.linalg.matrix_transpose(A), A)   # (8, 3, 3)
```

### N-D: ver por qué `.T` falla y `matrix_transpose` no
```python
T = np.arange(24).reshape(2, 3, 4)       # lote de 2 matrices 3x4
np.linalg.matrix_transpose(T).shape      # (2, 4, 3)  → cada matriz transpuesta
T.T.shape                                # (4, 3, 2)  → orden de ejes invertido
```

### Dimensión alta: lote 4D `(4, 5, 2, 3)` — `matrix_transpose` vs `.T`
Con un lote 4D —rejilla $4\times 5$ de matrices $2\times 3$— `matrix_transpose` permuta **solo los dos
últimos ejes** (los $4\cdot 5 = 20$ ejes de lote quedan fijos), mientras que `.T` **invierte la tupla
entera** y por tanto reordena también el lote:

$$
(4,\, 5,\, 2,\, 3)\ \xrightarrow{\ \text{matrix\_transpose}\ }\ (4,\, 5,\, 3,\, 2)
\qquad\text{pero}\qquad
(4,\, 5,\, 2,\, 3)\ \xrightarrow{\ .T\ }\ (3,\, 2,\, 5,\, 4)
$$

```python
G = np.random.rand(4, 5, 2, 3)           # 20 matrices 2x3 en rejilla 4x5
np.linalg.matrix_transpose(G).shape      # (4, 5, 3, 2)  ✅ lote intacto, matriz transpuesta
G.T.shape                                # (3, 2, 5, 4)  ⚠️ invierte los 4 ejes, mezcla el lote
```

### Transpuesta conjugada (hermitiana) de complejos
```python
Z = np.array([[1+2j, 3-1j], [0+1j, 2+0j]])
ZH = np.linalg.matrix_transpose(Z).conj()   # A^H, transpuesta + conjugado
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Lote mezclado en 3D+ | se usó `.T` en un stack | usar `matrix_transpose` (`.T` invierte todos los ejes) |
| `ValueError: ... at least 2 dimensions` | `x` es 1D | dar forma 2D antes de transponer |
| Esperar el conjugado | solo transpone, no conjuga | añadir `.conj()` para la hermitiana |
| Creer que copia | devuelve una vista | usar `.copy()` si necesitas datos independientes |

## Notas relacionadas

- [[concepto_shape]] — `.T` invierte la tupla; `matrix_transpose` solo los dos últimos ejes
- [[np.transpose]] — la transposición general por permutación de ejes (de la que `.T` es atajo)
- [[np.matmul]] — el producto que suele combinarse con la transpuesta ($A^{\mathsf T} A$)
- [[np.linalg.matrix_power]] · [[np.linalg.multi_dot]]
