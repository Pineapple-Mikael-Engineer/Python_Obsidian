---
title: np.linalg.eigvals — solo los autovalores de una matriz general
aliases:
  - eigvals
  - linalg.eigvals
  - np.linalg.eigvals
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

# np.linalg.eigvals — solo los autovalores de una matriz general

`np.linalg.eigvals` calcula **solo los autovalores** de una matriz cuadrada **general**, sin los
autovectores. Es la versión **barata** de [[np.linalg.eig]]: cuando solo te importa el espectro
—estabilidad, radio espectral, condicionamiento— evita el coste extra de calcular la matriz de
autovectores `v`. Si tu matriz es **simétrica/Hermítica**, prefiere [[np.linalg.eigvalsh]] (reales y
ordenados).

## La idea en una fórmula

Los autovalores son los $\lambda$ de la ecuación central; aquí solo nos quedamos con ellos:

$$
A\,\mathbf{v} = \lambda\,\mathbf{v} \quad\Longrightarrow\quad \det(A-\lambda I)=0
$$

Son las raíces del **polinomio característico**. `eigvals` los devuelve sin resolver el vector
$\mathbf{v}$.

**El mapa de shapes** — entrada `(...,n,n)` → **una sola** salida `(...,n)` (a diferencia de `eig`,
que devuelve dos):

$$
\underbrace{(n_0,\dots,n_{k-1},\,n,\,n)}_{A}\ \xrightarrow{\ \text{eigvals}\ }\ \underbrace{(n_0,\dots,n_{k-1},\,n)}_{w}
$$

Los dos últimos ejes de $A$ (la matriz) **se contraen** a un vector de $n$ autovalores; los `…`
anteriores son ejes de **lote** que sobreviven.

## Firma

```python
np.linalg.eigvals(a) -> ndarray
# a : array_like, shape (..., n, n) — matriz(ces) cuadrada(s) general(es)
```

## Los parámetros en detalle

### `a` — la(s) matriz(ces) de entrada
`array_like` de shape `(..., n, n)`: una matriz cuadrada o un lote apilado. **No** requiere simetría.
Acepta `dtype` real o complejo; con entrada real el resultado **puede ser complejo**. Es el único
parámetro: `eigvals` no expone `out` ni nada configurable.

```python
lote = np.random.rand(4, 3, 3)
np.linalg.eigvals(lote).shape   # (4, 3)  → 3 autovalores por matriz
```

## El caso N-D

Los **dos últimos ejes** son la matriz; los anteriores son **lote**. No hay `axis`.

| `a.shape` | `w.shape` | qué pasa |
|-----------|-----------|----------|
| `(n, n)` | `(n,)` | autovalores de una matriz |
| `(b, n, n)` | `(b, n)` | espectro de cada una de las `b` matrices |
| `(b, c, n, n)` | `(b, c, n)` | lote 2D |

```python
lote = np.random.rand(100, 5, 5)
w = np.linalg.eigvals(lote)       # (100, 5)
radios = np.abs(w).max(axis=1)    # radio espectral por matriz → (100,)
```

## Vectorización

El lote descompone muchas matrices sin bucle Python, delegando en **LAPACK**:

```python
# Bucle Python: un eigvals por matriz
def batch_eigvals(A):
    return np.array([np.linalg.eigvals(A[k]) for k in range(A.shape[0])])

# Vectorizado: NumPy recorre el lote en C / LAPACK
w = np.linalg.eigvals(A)
```

Ver [[concepto_vectorizacion]]: pides el espectro de todo el lote de golpe.

## Valor de retorno

Devuelve **un solo `ndarray`** (no una tupla): los autovalores de `a`.

| Salida | Shape | Contenido |
|--------|-------|-----------|
| `w` | `(..., n)` | los $n$ autovalores por matriz, **1D**, **sin orden garantizado**. Pueden ser **complejos aunque `a` sea real** |

- **Complejos desde una matriz real:** una rotación o cualquier matriz no simétrica con raíces
  complejas conjugadas devuelve `w` con `dtype` complejo.
- **Orden:** `eigvals` **no** ordena. Para ordenar, `np.sort(w)` (módulo o parte real según el caso).
- **Relación con traza y determinante:** `w.sum() == np.trace(a)` y `w.prod() == np.linalg.det(a)`.

```python
a = np.array([[2.0, 0.0],
              [0.0, 3.0]])
np.linalg.eigvals(a)            # array([2., 3.])

r = np.array([[0.0, -1.0],
              [1.0,  0.0]])      # rotación real
np.linalg.eigvals(r)            # array([0.+1.j, 0.-1.j]) → complejos
```

## Casos de uso

### Ejemplo trabajado con números: espectro de una matriz general

Para una matriz **triangular** el espectro es la diagonal, lo que permite comprobar `eigvals` a ojo:

$$
A=\begin{bmatrix} 2 & 5 & 1 \\ 0 & 3 & 4 \\ 0 & 0 & 7 \end{bmatrix}
\ \xrightarrow{\ \text{eigvals}\ }\
w=\begin{bmatrix} 2 & 3 & 7 \end{bmatrix}
$$

Y para una matriz **no simétrica** con raíces complejas conjugadas, `eigvals` devuelve `dtype`
complejo aunque `a` sea real:

$$
R=\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix}
\ \xrightarrow{\ \text{eigvals}\ }\
w=\begin{bmatrix} +i & -i \end{bmatrix}
$$

```python
a = np.array([[2.0, 5.0, 1.0],
              [0.0, 3.0, 4.0],
              [0.0, 0.0, 7.0]])
np.linalg.eigvals(a)            # array([2., 3., 7.])  (triangular → diagonal; sin orden garantizado)

r = np.array([[0.0, -1.0],
              [1.0,  0.0]])
np.linalg.eigvals(r)           # array([0.+1.j, 0.-1.j]) → complejos conjugados
```

### Radio espectral: ¿converge `x_{k+1} = A x_k`?
```python
A = np.array([[0.5, 0.1], [0.2, 0.4]])
radio = np.max(np.abs(np.linalg.eigvals(A)))
radio < 1      # True → la iteración converge
```

### Estabilidad sin calcular autovectores
```python
A = np.array([[-1.0, 2.0], [0.0, -3.0]])
np.all(np.linalg.eigvals(A).real < 0)   # True → sistema estable
```

### Lote (N-D): chequeo de consistencia traza/det

Para un lote `(b, n, n)` la salida es `(b, n)`: los dos ejes de la matriz se contraen a un vector de
`n` autovalores, y los ejes de lote sobreviven.

```python
lote = np.random.rand(10, 3, 3)         # b=10 matrices 3×3  → shape (10, 3, 3)
w = np.linalg.eigvals(lote)             # w: (10, 3)
w.shape                                 # (10, 3)
np.allclose(w.sum(axis=1), np.trace(lote, axis1=1, axis2=2))   # True (suma = traza)

# lote 2D (4D): (b, c, n, n) → (b, c, n)
lote4d = np.random.rand(12, 7, 5, 5)
np.linalg.eigvals(lote4d).shape         # (12, 7, 5)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | verificar `a.shape[-1] == a.shape[-2]` |
| Esperar una tupla `(w, v)` | `eigvals` devuelve **solo** `w` | usar [[np.linalg.eig]] para los autovectores |
| Resultado complejo inesperado | matriz real no simétrica | es correcto; usar `eigvalsh` si es simétrica |
| Orden inesperado de los autovalores | `eigvals` no ordena | `np.sort(w)` o usar `eigvalsh` |

## Notas relacionadas

- [[concepto_shape]] — el lote `(..., n, n)` y la contracción a `(..., n)`
- [[np.linalg.eig]] — autovalores **y** autovectores (matriz general)
- [[np.linalg.eigvalsh]] — solo autovalores de una matriz simétrica/Hermítica
- [[np.linalg.eigh]] · [[np.trace]] · [[np.linalg.det]]
