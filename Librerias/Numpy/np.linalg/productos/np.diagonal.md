---
title: np.diagonal — extrae la diagonal (la añade como último eje)
aliases:
  - diagonal
  - np.diagonal
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
  - concepto_views_vs_copias
draft: false
---

# np.diagonal — extrae los elementos de la diagonal

`np.diagonal` **extrae** la diagonal de una matriz como un vector: recorre los elementos donde
$i = j$ y los devuelve en un eje nuevo. A diferencia de [[np.trace]] (que los **suma**), aquí se
conservan los valores individuales. En N-D extrae la diagonal de cada matriz de un lote. Un detalle
clave de memoria: desde NumPy ≥ 1.9 el resultado es una **vista de solo lectura**.

## La idea en una fórmula

Para una matriz $A$ de shape $(n, m)$, la diagonal es el vector indexado por $i$ con $i = j$:

$$
d_i \;=\; A_{ii} \qquad i = 0, \dots, \min(n, m) - 1
$$

La longitud de la diagonal es $\min(n, m)$: en una matriz no cuadrada se detiene en el lado corto.
Con `offset`, la diagonal desplazada es $d_i = A_{i,\,i+\text{offset}}$.

**El mapa de shapes** (la relación entrada → salida, incluido el caso por lotes N-D):

$$
(n_0,\dots,n_{k-1},\, m,\, p)\ \xrightarrow{\ \text{diagonal}\ }\ (n_0,\dots,n_{k-1},\ \min(m, p))
$$

Los **dos ejes** de la matriz (`axis1`, `axis2`) **se eliminan** y la diagonal de longitud
$\min(m,p)$ se **añade como ÚLTIMO eje**. Esto sorprende: aunque diagonalices los dos primeros ejes,
el eje de la diagonal aparece al **final**, no donde estaban. Una matriz $(m,p)$ da $(\min(m,p),)$;
una pila $(b,m,m)$ da $(b, m)$ —una diagonal por matriz—.

Visualmente, para una matriz $3\times 3$ se extraen los elementos marcados (los $A_{ii}$) a un
vector:

$$
\begin{bmatrix}
\mathbf{A_{00}} & \cdot & \cdot \\
\cdot & \mathbf{A_{11}} & \cdot \\
\cdot & \cdot & \mathbf{A_{22}}
\end{bmatrix}
\ \longrightarrow\ \begin{bmatrix} A_{00} & A_{11} & A_{22} \end{bmatrix}
\qquad (\text{offset}=0,\ \text{longitud } 3)
$$

## Firma

```python
np.diagonal(
    a,           # array_like: tensor con al menos 2 ejes
    offset=0,    # int: diagonal a extraer (0 principal, >0 arriba, <0 abajo)
    axis1=0,     # int: primer eje del par que forma la matriz
    axis2=1,     # int: segundo eje del par que forma la matriz
) -> ndarray     # VISTA de solo lectura (numpy >= 1.9)
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` con `ndim >= 2`. La matriz se forma con los ejes `axis1`/`axis2`; el resto son lote. No
necesita ser cuadrada: la diagonal extraída tiene longitud $\min(n, m)$.

### `offset` — qué diagonal se extrae
`int` (defecto `0`). `offset > 0` toma la diagonal por encima de la principal ($A_{i,\,i+\text{offset}}$),
`offset < 0` la de por debajo. Misma convención que [[np.trace]].

```python
A = np.arange(9).reshape(3, 3)   # [[0,1,2],[3,4,5],[6,7,8]]
np.diagonal(A)            # [0, 4, 8]   principal
np.diagonal(A, offset=1)  # [1, 5]      diagonal de encima (más corta)
np.diagonal(A, offset=-1) # [3, 7]      diagonal de debajo
```

### `axis1`, `axis2` — qué par de ejes forman la matriz
`int` (defecto `0` y `1`). En N-D eligen **cuáles** ejes son la matriz a diagonalizar; los demás son
lote. Como en [[np.trace]], los defectos toman los **dos primeros** ejes (no los dos últimos); para
un lote `(b, n, n)` casi siempre quieres `axis1=-2, axis2=-1`.

```python
P = np.arange(2*3*3).reshape(2, 3, 3)
np.diagonal(P, axis1=-2, axis2=-1).shape   # (2, 3) → una diagonal por matriz
np.diagonal(P).shape                        # (3, 2) → diagonaliza ejes 0,1 (raro)
```

## El eje y el caso N-D

La regla mecánica: **los ejes `axis1` y `axis2` se eliminan** y se **añade** la diagonal como último
eje. Los ejes de lote sobreviven en orden delante.

| `a.shape` | parámetros | salida | lectura |
|-----------|-----------|--------|---------|
| `(n, n)` | defecto | `(n,)` | la diagonal |
| `(n, m)` | defecto | `(min(n,m),)` | diagonal del lado corto |
| `(b, n, n)` | `axis1=-2, axis2=-1` | `(b, n)` | una diagonal por matriz del lote |
| `(b, n, n)` | defecto (`axis1=0, axis2=1`) | `(n, b)` | diagonaliza ejes 0,1 → la diagonal va al final |
| `(b, c, n, n)` | `axis1=-2, axis2=-1` | `(b, c, n)` | diagonal de cada matriz de la rejilla |

```python
batch = np.arange(2*3*3).reshape(2, 3, 3)
np.diagonal(batch, axis1=-2, axis2=-1)
# [[ 0,  4,  8],
#  [ 9, 13, 17]]   → la diagonal de cada matriz, shape (2, 3)
```

## Vectorización

Extraer la diagonal de cada matriz de un lote sin bucle Python es [[concepto_vectorizacion]]; además
es casi **gratis** porque devuelve una vista (no copia datos):

```python
# Bucle Python: una diagonal por matriz del lote
def batch_diag(P):
    return np.stack([np.diagonal(P[i]) for i in range(P.shape[0])])

# Vectorizado: una sola llamada, devuelve una vista
np.diagonal(P, axis1=-2, axis2=-1)
```

## Valor de retorno

| Entrada | parámetros | salida (shape) | tipo |
|---------|-----------|----------------|------|
| `(n, n)` | defecto | `(n,)` | `ndarray` (**vista de solo lectura**) |
| `(n, m)` | defecto | `(min(n,m),)` | `ndarray` (vista de solo lectura) |
| `(b, n, n)` | par de ejes | `(b, n)` | `ndarray` (vista de solo lectura) |

El `dtype` es el mismo de `a` (no hay acumulación, solo se seleccionan elementos).

> [!warning] Devuelve una VISTA de SOLO LECTURA (numpy ≥ 1.9)
> Desde NumPy 1.9, `np.diagonal` (y `a.diagonal()`) devuelve una **vista** del array original marcada
> como **no escribible**. Asignarle valores lanza `ValueError: assignment destination is read-only`.
> Antes de 1.9 devolvía una copia escribible; el cambio se hizo por eficiencia (ver
> [[concepto_views_vs_copias|vistas vs copias]]: una vista no duplica el buffer). Para **modificar**
> la diagonal tienes dos caminos:
> - `np.fill_diagonal(a, valor)` — escribe la diagonal **in place** sobre `a`.
> - `np.diagonal(a).copy()` — una **copia** independiente y escribible si solo quieres trabajar con
>   los valores sin tocar `a`.

```python
A = np.zeros((3, 3))
d = np.diagonal(A)
d[:] = 1                       # ValueError: assignment destination is read-only
np.fill_diagonal(A, 1)         # OK → A es ahora la identidad
np.diagonal(A).copy()[:] = 9   # OK (modifica la copia, no A)
```

## Casos de uso

### Leer la diagonal de una matriz
Con números concretos, se extraen los $A_{ii}$ resaltados a un vector:

$$
\begin{bmatrix}
\mathbf{10} & 2 & 3 \\
4 & \mathbf{20} & 6 \\
7 & 8 & \mathbf{30}
\end{bmatrix}
\ \longrightarrow\ \begin{bmatrix} 10 & 20 & 30 \end{bmatrix}
$$

```python
M = np.array([[10, 2, 3], [4, 20, 6], [7, 8, 30]])
np.diagonal(M)          # [10, 20, 30]
np.diagonal(M).sum()    # 60  → equivale a np.trace(M)
```

### Diagonal desplazada y matrices no cuadradas
```python
R = np.arange(12).reshape(3, 4)
np.diagonal(R)            # [0, 5, 10]      longitud min(3,4)=3
np.diagonal(R, offset=1)  # [1, 6, 11]      una por encima
```

### Diagonales de un lote de matrices N-D
```python
covs = np.random.rand(50, 4, 4)             # 50 matrices 4x4
varianzas = np.diagonal(covs, axis1=-2, axis2=-1)
varianzas.shape          # (50, 4)  → la diagonal (varianzas) de cada matriz
```

### Lote 4D: una diagonal por matriz de una rejilla
Con un tensor `(2, 3, n, n)` —rejilla `2x3` de matrices `n×n`— la diagonal sobre los dos últimos
ejes elimina ese par y **añade** la diagonal de longitud $\min(n,n)=n$ como último eje:

```python
T = np.arange(2*3*4*4).reshape(2, 3, 4, 4)   # shape (2, 3, 4, 4)
d = np.diagonal(T, axis1=-2, axis2=-1)
d.shape    # (2, 3, 4)  → (2, 3, min(4,4)): una diagonal por matriz de la rejilla 2x3
```

El mapa de shapes: $(2,3,\mathbf{4},\mathbf{4})\xrightarrow{\ \text{diagonal}\ }(2,3,\ \min(4,4))
=(2,3,4)$ —los dos ejes de la matriz (en negrita) se eliminan y la diagonal va al último eje—.

## `np.diagonal` vs `np.diag`

No confundir con [[np.diag]], que es **ambivalente** según la dimensión del input:

| Función | Entrada | Hace | Salida |
|---------|---------|------|--------|
| `np.diagonal(M)` | 2D (o N-D) | **extrae** la diagonal (vista solo lectura) | 1D (o lote) |
| `np.diag(M)` | 2D | **extrae** la diagonal (copia) | 1D |
| `np.diag(v)` | 1D | **construye** una matriz diagonal | 2D |

`np.diag` solo trabaja en 2D y decide entre extraer/construir según el `ndim` de la entrada;
`np.diagonal` siempre **extrae** y es el que soporta lotes N-D con `axis1`/`axis2`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: ...read-only` | intentar asignar a la diagonal devuelta | `np.fill_diagonal(a, ...)` o `.copy()` |
| Shape de salida inesperado en un lote | los defectos toman los dos PRIMEROS ejes y la diagonal va al final | `axis1=-2, axis2=-1` |
| Esperar una matriz al pasar un vector | usaste `np.diagonal` para **construir** | para construir usa [[np.diag]] o [[np.diagflat]] |
| Diagonal más corta de lo esperado | matriz no cuadrada: longitud $\min(n,m)$ | es correcto; revisa el shape |
| `ndim < 2` falla | la entrada es 1D | `np.diagonal` exige al menos 2 ejes |

## Notas relacionadas

- [[concepto_shape]] — los dos ejes de la matriz se eliminan y la diagonal va al último eje
- [[concepto_views_vs_copias]] — por qué la diagonal es una vista de solo lectura
- [[np.trace]] — la suma de la diagonal (esta función la extrae)
- [[np.diag]] · [[np.diagflat]] · [[np.fill_diagonal]] — construir/escribir diagonales
