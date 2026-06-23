---
title: np.eye — identidad (o diagonal desplazada), posiblemente no cuadrada
aliases:
  - eye
  - np.eye
tags:
  - numpy
  - api/funcion
  - creacion
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
  - concepto_dtype
draft: false
---

# np.eye — identidad (o diagonal desplazada), posiblemente no cuadrada

`np.eye` construye una matriz 2D con **unos en una diagonal** y ceros en el resto. En su forma más
común es la **matriz identidad** $I$ (cuadrada, unos en la diagonal principal), pero es más general
que [[np.identity]]: admite forma **rectangular** $(N, M)$ y una **diagonal desplazada** con `k`. Es
la herramienta para fabricar la identidad del producto matricial, codificar one-hot o levantar
matrices de desplazamiento y banda.

## La idea

El resultado es la matriz $(N, M)$ cuyo elemento vale $1$ exactamente en la diagonal indicada por
`k`, y $0$ en todo lo demás:

$$
E_{ij} = \begin{cases} 1 & \text{si } j = i + k \\ 0 & \text{en otro caso} \end{cases}
$$

Con los valores por defecto ($M = N$, $k = 0$) eso es la **identidad** $I$ de orden $N$:

$$
I = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

El parámetro `k` **desliza** la franja de unos: $k > 0$ la sube por encima de la principal, $k < 0$
la baja. Por ejemplo `np.eye(3, k=1)` pone los unos en la superdiagonal:

$$
\text{eye}(3,\, k=1) = \begin{bmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 0 & 0 & 0 \end{bmatrix}
\qquad
\text{eye}(3,\, k=-1) = \begin{bmatrix} 0 & 0 & 0 \\ 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}
$$

Y con $M \neq N$ la matriz es rectangular: la diagonal de unos se detiene donde se acaba el lado
corto. El **mapa de shapes** es trivial porque la forma se pasa por parámetro: $(N, M)$, con
$M = N$ si se omite. Ver [[concepto_shape]].

## Firma

```python
np.eye(
    N,            # int: número de filas
    M=None,       # int | None: número de columnas (None → M = N, cuadrada)
    k=0,          # int: índice de la diagonal (0 principal, >0 arriba, <0 abajo)
    dtype=float,  # tipo de los elementos (los unos y ceros)
    order='C',    # 'C' | 'F': orden en memoria
    *,
    like=None,    # array_like: prototipo para crear el array en otro backend
) -> ndarray
```

## Los parámetros en detalle

### `N` — número de filas
`int` obligatorio. Define la altura de la matriz. Si solo das `N`, la matriz sale cuadrada $N\times N$.

### `M` — número de columnas
`int` o `None` (defecto). Con `None` se toma $M = N$ (matriz cuadrada). Pásalo para una matriz
**rectangular**: `np.eye(2, 3)` da una $(2, 3)$ con la diagonal de unos recortada al lado corto.

```python
np.eye(2, 3)
# array([[1., 0., 0.],
#        [0., 1., 0.]])
```

### `k` — diagonal a rellenar
`int` (defecto `0`). `0` es la diagonal principal; `k > 0` desplaza los unos a una superdiagonal;
`k < 0` a una subdiagonal. Es lo que diferencia a `eye` de [[np.identity]]. Útil para matrices de
desplazamiento (`shift`) y bandas. Si $|k|$ supera el ancho de la matriz, la diagonal cae fuera y el
resultado es todo ceros.

### `dtype` — tipo de los elementos
Por defecto `float` (los unos son `1.0`). Pasa `dtype=int` para una identidad entera o `dtype=bool`
para una **máscara** de la diagonal (`True`/`False`). Ver [[concepto_dtype]].

```python
np.eye(2, dtype=int)    # [[1, 0], [0, 1]]
np.eye(2, dtype=bool)   # [[True, False], [False, True]]
```

### `order` — disposición en memoria
`'C'` (filas contiguas, defecto) o `'F'` (columnas contiguas, estilo Fortran). Solo afecta al layout
interno, no a los valores; relevante si vas a pasar la matriz a una librería que espera orden Fortran.

### `like` — prototipo de backend
`array_like` (keyword-only). Crea el array con el mismo tipo que el prototipo, para soportar
sustitutos de NumPy (CuPy, Dask...). Rara vez se usa.

## Casos de uso

### Identidad para álgebra lineal
La identidad es el neutro del producto matricial: $A I = I A = A$.
```python
I = np.eye(4)
A @ I   # == A
```

### Codificación one-hot
Indexar las filas de la identidad por un vector de clases produce su one-hot encoding. Es el truco
idiomático:
```python
clases = np.array([0, 2, 1])
np.eye(3)[clases]
# array([[1., 0., 0.],
#        [0., 0., 1.],
#        [0., 1., 0.]])
```

### Matriz de desplazamiento (shift)
La superdiagonal de unos mueve cada componente una posición al multiplicar:
```python
S = np.eye(4, k=1)   # operador de shift hacia arriba
```

### Matriz rectangular o banda
```python
np.eye(3, 5)          # (3, 5) con diagonal de unos
np.eye(5) + np.eye(5, k=1) + np.eye(5, k=-1)   # matriz tridiagonal de unos
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `dtype` float donde querías int | por defecto es `float` (unos `1.0`) | `dtype=int` |
| Sale rectangular sin querer | se pasó `M` distinto de `N` | omitir `M` para cuadrada, o usar [[np.identity]] |
| Diagonal en el sitio equivocado | confundir el signo de `k` | `k>0` arriba, `k<0` abajo |
| Todo ceros | `|k|` mayor que el tamaño → la diagonal cae fuera | revisar `k` frente a `N`/`M` |
| Esperar 3D | `eye` solo genera matrices 2D | construir a mano o con [[np.diag]] por lotes |

## Notas relacionadas

- [[concepto_shape]] — la forma `(N, M)` se fija por parámetro
- [[concepto_dtype]] — tipo de los unos y ceros (`float`/`int`/`bool`)
- [[np.identity]] — el caso cuadrado de diagonal principal (`np.eye(n)`)
- [[np.diag]] · [[np.diagflat]] — construir diagonales a partir de un vector
- [[np.zeros]] · [[np.full]] — otras matrices constantes de partida
