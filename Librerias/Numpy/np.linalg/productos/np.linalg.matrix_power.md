---
title: np.linalg.matrix_power — potencia entera de una matriz cuadrada (A^n)
aliases:
  - matrix_power
  - linalg.matrix_power
  - np.linalg.matrix_power
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

# np.linalg.matrix_power — potencia entera de una matriz cuadrada (A^n)

`np.linalg.matrix_power` eleva una matriz **cuadrada** $A$ a una potencia **entera** $n$ usando el
**producto matricial repetido**: $A^n = A\,@\,A\,@\,\dots\,@\,A$ ($n$ veces). Es la versión matricial
de `**`, no la potencia elemento a elemento. La operación está gobernada por el [[np.matmul|producto
matricial]]: cada paso contrae la dimensión interior, por lo que la matriz debe ser cuadrada para
poder multiplicarse consigo misma. Aparece en cadenas de Markov, sistemas dinámicos discretos
($x_{t} = A^t x_0$) y cualquier iteración lineal repetida.

## La idea en una fórmula

Para $A$ de shape $(n_0,\dots,n_{k-1}, m, m)$, la potencia $n$-ésima encadena $n$ productos matriciales:

$$
A^n = \underbrace{A \cdot A \cdots A}_{n\ \text{factores}} \qquad (A^n)_{ij} = \sum_{k_1,\dots,k_{n-1}} A_{i k_1} A_{k_1 k_2} \cdots A_{k_{n-1} j}
$$

**El mapa de shapes** — la matriz debe ser **cuadrada** ($m \times m$) y la salida conserva el shape;
los $n_0,\dots,n_{k-1}$ son ejes de lote que se preservan intactos:

$$
(n_0,\dots,n_{k-1},\, m,\, m)\ \xrightarrow{\ \text{matrix\_power},\ n\ }\ (n_0,\dots,n_{k-1},\, m,\, m)
$$

El exponente $n$ es un entero con tres regímenes según su signo:

$$
A^n =
\begin{cases}
\underbrace{A \cdots A}_{n} & n > 0 \quad \text{(producto repetido)} \\[4pt]
I_m & n = 0 \quad \text{(identidad } m\times m\text{)} \\[4pt]
\underbrace{A^{-1} \cdots A^{-1}}_{|n|} & n < 0 \quad \text{(potencia de la inversa, requiere } A \text{ invertible)}
\end{cases}
$$

## Firma

```python
np.linalg.matrix_power(a, n) -> ndarray
```

## Los parámetros en detalle

### `a` — la matriz (o lote de matrices) a elevar
`array_like` con `ndim >= 2` cuyos **dos últimos ejes son iguales** (`a.shape[-1] == a.shape[-2]`),
es decir cuadrada $(n_0,\dots,n_{k-1}, m, m)$. Admite **pilas**: los ejes anteriores son lote y cada matriz del
lote se eleva por separado. Si no es cuadrada, lanza `LinAlgError`.

### `n` — el exponente entero
Un **entero** de Python o NumPy (no acepta floats; un float lanza `TypeError`). Su signo determina el
comportamiento:
- `n > 0`: producto matricial repetido `n` veces. Internamente usa **exponenciación binaria**
  (cuadrados sucesivos), así que `A**16` no hace 16 productos sino unos $\log_2 16 = 4$.
- `n == 0`: devuelve la **identidad** $I_m$ del tamaño adecuado, sea cual sea `a` (mientras sea
  cuadrada).
- `n < 0`: eleva la **inversa** `inv(a)` a `abs(n)`; requiere que `a` sea **invertible** (no
  singular), o lanza `LinAlgError: Singular matrix`.

```python
A = np.array([[2, 0], [0, 3]])
np.linalg.matrix_power(A, 3)    # [[8, 0], [0, 27]]   → A @ A @ A
np.linalg.matrix_power(A, 0)    # [[1, 0], [0, 1]]    → identidad
np.linalg.matrix_power(A, -1)   # [[0.5, 0], [0, 0.333...]]  → inv(A)
```

## El caso N-D

Como toda la familia de productos, `matrix_power` trata los **dos últimos ejes** como la matriz y
**todos los anteriores como un lote**. Cada matriz del lote se eleva de forma independiente; el shape
no cambia:

| `a.shape` | `n` | resultado | qué pasa |
|-----------|-----|-----------|----------|
| `(m, m)` | `> 0` | `(m, m)` | potencia de una sola matriz |
| `(m, m)` | `0` | `(m, m)` | identidad $I_m$ |
| `(m, m)` | `< 0` | `(m, m)` | potencia de la inversa |
| `(b, m, m)` | `k` | `(b, m, m)` | **lote**: `b` potencias independientes |
| `(p, q, m, m)` | `k` | `(p, q, m, m)` | lote 2D de potencias |

```python
# Lote de 4 matrices 2x2, cada una elevada al cubo
batch = np.tile(np.array([[2, 0], [0, 3]]), (4, 1, 1))   # shape (4, 2, 2)
np.linalg.matrix_power(batch, 3).shape   # (4, 2, 2)  → 4 potencias, sin bucle
np.linalg.matrix_power(batch, 3)[0]      # [[8, 0], [0, 27]]
```

## Vectorización

El valor de `matrix_power` es doble. Por un lado, frente a un bucle Python que encadena `@` a mano,
delega los productos en **BLAS** y usa **exponenciación binaria** (menos productos que `n`):

```python
# Bucle Python ingenuo: n-1 productos explícitos
def power_loop(A, n):
    out = A.copy()
    for _ in range(n - 1):
        out = out @ A
    return out

# Vectorizado: BLAS + exponenciación binaria (≈ log2(n) productos)
np.linalg.matrix_power(A, n)
```

Por otro lado, en N-D recorre el **lote en C** sin un `for` por matriz. Razonar "los dos últimos ejes
son la matriz, lo demás es lote" (ver [[concepto_shape]]) es lo que permite elevar un tensor de
matrices de golpe.

## Valor de retorno

| `a` | `n` | salida | tipo |
|-----|-----|--------|------|
| `(m, m)` int | `> 0` | `(m, m)` | `ndarray`, dtype de `a` |
| `(m, m)` | `0` | `(m, m)` identidad | `ndarray` |
| `(m, m)` | `< 0` | `(m, m)` | `ndarray` **float** (la inversa promueve a float) |
| `(b, m, m)` | cualquiera | `(b, m, m)` | `ndarray` |

- Con `n >= 0` y `a` entera, el resultado conserva el `dtype` entero.
- Con `n < 0` el resultado es **float** porque `inv(a)` lo es, aunque `a` sea entera.
- Siempre devuelve un `ndarray` nuevo (nunca una vista).

## Casos de uso

### Cadena de Markov: distribución tras varios pasos
```python
P = np.array([[0.9, 0.1],
              [0.5, 0.5]])
P10 = np.linalg.matrix_power(P, 10)   # matriz de transición tras 10 pasos
```

### Sistema dinámico discreto $x_t = A^t x_0$
```python
A = np.array([[1.0, 1.0], [0.0, 1.0]])   # avance con "inercia"
x0 = np.array([0.0, 1.0])
A5 = np.linalg.matrix_power(A, 5)
x5 = A5 @ x0                              # estado en t=5
```

### Identidad del tamaño adecuado
```python
I = np.linalg.matrix_power(A, 0)   # identidad MxM coherente con A
```

### N-D: potencia por lotes
```python
M = np.random.rand(8, 3, 3)        # 8 matrices 3x3
np.linalg.matrix_power(M, 4).shape # (8, 3, 3)  → 8 potencias en lote
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions ... must be square` | matriz no cuadrada | dar forma `(..., M, M)` |
| `TypeError: exponent must be an integer` | `n` es float | pasar un entero |
| `LinAlgError: Singular matrix` | `n < 0` con matriz no invertible | usar `n >= 0` o una matriz regular |
| Resultado elemento a elemento inesperado | se usó `**` | usar `matrix_power` (ver [[np.multiply]]) |
| Esperar `dtype` entero con `n < 0` | la inversa promueve a float | esperado: la inversa es float |

## Notas relacionadas

- [[np.matmul]] — el producto matricial que se repite en cada paso
- [[concepto_shape]] — los dos últimos ejes son la matriz; lo demás es lote
- [[np.multiply]] — la potencia elemento a elemento (`**`), no confundir
- [[np.linalg.matrix_transpose]] · [[np.linalg.multi_dot]]
