---
title: np.linalg.qr — factoriza A = QR (Q ortonormal · R triangular superior)
aliases:
  - qr
  - linalg.qr
  - np.linalg.qr
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: tuple (Q, R) o ndarray según mode
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.qr — factoriza A = QR (Q ortonormal · R triangular superior)

`np.linalg.qr` **descompone** una matriz $A$ en el producto $A = QR$, donde $Q$ tiene **columnas
ortonormales** y $R$ es **triangular superior**. Es la herramienta estándar para resolver mínimos
cuadrados de forma estable y para **ortonormalizar** una base (alternativa robusta a Gram-Schmidt,
basada en reflectores de Householder). A diferencia de una reducción, no colapsa un eje: parte la
matriz en dos factores con estructura. El parámetro `mode` cambia los **shapes** de los factores, así
que la nota lo desambigua en una tabla.

## La idea en una fórmula

QR factoriza $A$ en una parte ortonormal $Q$ (preserva ángulos y longitudes) y una triangular superior
$R$ (los coeficientes):

$$
A = Q\,R \qquad Q^{H} Q = I \ (\text{columnas ortonormales}),\quad R \text{ triangular superior}
$$

El **mapa de shapes** depende de `mode`; en el modo `reduced` (defecto), con $k = \min(m, n)$:

$$
(n_0,\dots,n_{k-1},\, m,\, n)\ \xrightarrow{\ \text{qr, reduced}\ }\ Q\,(n_0,\dots,n_{k-1},\, m,\, r),\ R\,(n_0,\dots,n_{k-1},\, r,\, n)\qquad r=\min(m,n)
$$

Para una matriz **alta** ($m > n$), $k = n$: $Q$ es $(m, n)$ con columnas ortonormales y $R$ es
$(n, n)$ cuadrada triangular. Visualmente, una $A$ de $(3\times 2)$:

$$
\underbrace{\begin{bmatrix} a_{00} & a_{01} \\ a_{10} & a_{11} \\ a_{20} & a_{21} \end{bmatrix}}_{A\ (3\times 2)}
=
\underbrace{\begin{bmatrix} q_{00} & q_{01} \\ q_{10} & q_{11} \\ q_{20} & q_{21} \end{bmatrix}}_{Q\ (3\times 2)\ \text{ortonormales}}
\underbrace{\begin{bmatrix} r_{00} & r_{01} \\ 0 & r_{11} \end{bmatrix}}_{R\ (2\times 2)\ \text{triangular sup.}}
$$

## Firma

```python
np.linalg.qr(
    a,                  # array_like: matriz (..., m, n)
    mode='reduced',     # 'reduced' | 'complete' | 'r' | 'raw'
) -> tuple[ndarray, ndarray] | ndarray
```

## Los parámetros en detalle

### `a` — la matriz de entrada
`array_like` de [[concepto_shape|shape]] `(..., m, n)`, de cualquier forma (no tiene que ser
cuadrada). Los dos últimos ejes son la matriz; los `…` anteriores son lote. Enteros se promueven a
`float64`.

```python
A = np.array([[1.0, 2.0],
              [3.0, 4.0],
              [5.0, 6.0]])      # (3, 2)
Q, R = np.linalg.qr(A)         # reduced: Q (3,2), R (2,2)
```

### `mode` — variante de la descomposición (cambia el retorno y los shapes)
`str`, defecto `'reduced'`. Controla **qué** se devuelve y con **qué shapes** (con $k = \min(m, n)$):

| `mode` | Retorno | Shapes | Cuándo |
|--------|---------|--------|--------|
| `'reduced'` (defecto) | tupla `(Q, R)` | `Q (..., m, k)`, `R (..., k, n)` | el habitual; económico, basta para `A = Q @ R` |
| `'complete'` | tupla `(Q, R)` | `Q (..., m, m)`, `R (..., m, n)` | base ortonormal **completa** (incluye el complemento ortogonal) |
| `'r'` | solo `R` (ndarray) | `R (..., k, n)` | cuando solo interesa `R` (evita calcular `Q`) |
| `'raw'` | tupla `(h, tau)` | `h (..., n, m)`, `tau (..., k)` | reflectores de Householder crudos (uso avanzado / LAPACK) |

En `'reduced'` y `'complete'` se cumple `Q.conj().T @ Q == I` y `R` triangular superior. La diferencia:
`'complete'` rellena $Q$ hasta ser cuadrada $(m, m)$ y $R$ hasta $(m, n)$ con filas de ceros abajo.

```python
R = np.linalg.qr(A, mode='r')              # devuelve SOLO R (un array)
Qc, Rc = np.linalg.qr(A, mode='complete')  # Qc (3,3), Rc (3,2)
```

## El caso N-D

La descomposición se aplica **a los dos últimos ejes** `(m, n)` y trata los anteriores como **lote**:
dada una pila `(..., m, n)`, NumPy calcula la QR de cada matriz por separado y apila los $Q$ y $R$. No
hay broadcasting entre matrices; cada una produce su propio par de factores.

| `a.shape` | `mode` | `Q.shape` | `R.shape` |
|-----------|--------|-----------|-----------|
| `(m, n)` | `reduced` | `(m, k)` | `(k, n)` |
| `(b, m, n)` | `reduced` | `(b, m, k)` | `(b, k, n)` |
| `(b, m, n)` | `complete` | `(b, m, m)` | `(b, m, n)` |

```python
lote = np.random.rand(4, 5, 3)    # 4 matrices 5×3
Q, R = np.linalg.qr(lote)
Q.shape                           # (4, 5, 3)   → k = min(5,3) = 3
R.shape                           # (4, 3, 3)
```

## Vectorización

El lote de QR es [[concepto_vectorizacion|vectorización]]: NumPy recorre los ejes previos en código
compilado y delega cada factorización en **LAPACK** (`geqrf` + `orgqr`), sin un bucle Python por
matriz:

```python
# Bucle Python: una QR por matriz, con salto al intérprete
def qr_lote(stack):
    Qs, Rs = [], []
    for i in range(stack.shape[0]):
        q, r = np.linalg.qr(stack[i])
        Qs.append(q); Rs.append(r)
    return np.stack(Qs), np.stack(Rs)

# Vectorizado: NumPy itera el lote sobre los dos últimos ejes
Q, R = np.linalg.qr(stack)
```

## Valor de retorno

El tipo del retorno **depende de `mode`** (tabla del parámetro). Para `a` de shape `(m, n)` y
$k = \min(m, n)$:

| `mode` | objetos devueltos | shapes |
|--------|-------------------|--------|
| `'reduced'` | tupla `(Q, R)` | `Q (m, k)`, `R (k, n)` |
| `'complete'` | tupla `(Q, R)` | `Q (m, m)`, `R (m, n)` |
| `'r'` | un único ndarray `R` | `R (k, n)` |
| `'raw'` | tupla `(h, tau)` | `h (n, m)`, `tau (k,)` |

`dtype` de punto flotante (`float64`/`complex128`). En los modos con `Q` se cumple
`np.allclose(A, Q @ R)`.

```python
A = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])   # (3, 2)
Q, R = np.linalg.qr(A)
Q.shape, R.shape                  # (3, 2), (2, 2)
np.allclose(A, Q @ R)            # True
np.allclose(Q.T @ Q, np.eye(2))  # True  → columnas ortonormales
```

## Casos de uso

### Ejemplo trabajado con números
Una $A$ de $(3\times 2)$ con factor $R$ de entradas enteras. $Q$ tiene columnas ortonormales
($Q^{T}Q=I$) y $R$ es triangular superior:

$$
A=\begin{bmatrix} 12 & -51 \\ 6 & 167 \\ -4 & 24 \end{bmatrix}
= Q\,R,\quad
Q=\begin{bmatrix} -0.857 & 0.394 \\ -0.429 & -0.903 \\ 0.286 & -0.171 \end{bmatrix},\quad
R=\begin{bmatrix} -14 & -21 \\ 0 & -175 \end{bmatrix}
$$

Las dos columnas de $Q$ tienen norma 1 y son ortogonales entre sí; $R$ guarda los coeficientes
triangulares. El signo global de cada columna de $Q$ (y la fila de $R$) puede variar según LAPACK.

```python
A = np.array([[12.0, -51.0], [6.0, 167.0], [-4.0, 24.0]])   # (3, 2)
Q, R = np.linalg.qr(A)
R                                  # [[-14., -21.], [0., -175.]]  → triangular superior
np.allclose(A, Q @ R)              # True
np.allclose(Q.T @ Q, np.eye(2))    # True  → columnas ortonormales
```

### Mínimos cuadrados (sistema sobredeterminado)
```python
# Resolver A x ≈ b con A (m, n), m > n: QR es más estable que las ecuaciones normales
Q, R = np.linalg.qr(A)
x = np.linalg.solve(R, Q.T @ b)        # R x = Qᵀ b (triangular, barato)
```

### Ortonormalizar un conjunto de vectores
```python
V = np.random.rand(5, 3)               # 3 vectores columna en R^5
Q, _ = np.linalg.qr(V)                 # columnas de Q: base ortonormal de span(V)
np.allclose(Q.T @ Q, np.eye(3))        # True
```

### Solo R, sin calcular Q
```python
R = np.linalg.qr(A, mode='r')          # más barato si Q no hace falta
```

### Lote de QR (N-D)
```python
# 3D: 10 matrices 6×4 → k = min(6,4) = 4
stack = np.random.rand(10, 6, 4)
Q, R = np.linalg.qr(stack)
Q.shape, R.shape                       # (10, 6, 4), (10, 4, 4)  → sin bucle

# 4D: lote (8, 5) de matrices 6×4  → 40 factorizaciones, k = 4
stack4 = np.random.rand(8, 5, 6, 4)
Q4, R4 = np.linalg.qr(stack4)
Q4.shape, R4.shape                     # (8, 5, 6, 4), (8, 5, 4, 4)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError` al converger | entrada con `NaN`/`inf` | validar con `np.isfinite(a).all()` |
| Esperar `Q` con `mode='r'` | ese modo devuelve **solo** `R` | usar `'reduced'`/`'complete'` si quieres `Q` |
| `ValueError` al desempaquetar | `mode='r'` no devuelve tupla | asignar a una sola variable |
| `R` no parece triangular | confundir `R` con `Q`, o lote mal interpretado | recordar el orden `(Q, R)` y los shapes |
| `Q @ R` no reconstruye `A` | mezclar resultados de modos distintos | usar `Q` y `R` del **mismo** `mode` |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes `(m, n) → Q(m, k), R(k, n)`
- [[concepto_vectorizacion]] — por qué el lote de factorizaciones evita el bucle
- [[Librerias/Numpy/np.linalg/descomposiciones/index|descomposiciones]] — la familia completa
- [[np.linalg.svd]] · [[np.linalg.cholesky]] · [[np.linalg.solve]] · [[np.linalg.lstsq]]
