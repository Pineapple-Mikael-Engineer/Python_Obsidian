---
title: np.identity — matriz identidad cuadrada
aliases:
  - identity
  - np.identity
  - matriz identidad
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
draft: false
---

# np.identity — matriz identidad cuadrada

`np.identity` devuelve la **matriz identidad** $I$ de orden $n$: una matriz cuadrada $(n, n)$ con unos
en la diagonal principal y ceros en el resto. Es el caso simple y explícito de [[np.eye]]: sin forma
rectangular ni diagonal desplazada. Cuando lo que quieres es justo "la identidad", esta función lo
comunica mejor que `np.eye(n)`.

## La idea

El elemento vale $1$ solo donde coinciden fila y columna ($i = j$), y $0$ en todo lo demás (la delta
de Kronecker $\delta_{ij}$):

$$
I_{ij} = \delta_{ij} = \begin{cases} 1 & \text{si } i = j \\ 0 & \text{si } i \neq j \end{cases}
$$

Para $n = 3$ eso es:

$$
I = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix}
$$

La forma de salida está fijada por el único parámetro: siempre $(n, n)$, cuadrada. Ver
[[concepto_shape]].

## Firma

```python
np.identity(
    n,            # int: orden de la matriz (filas = columnas = n)
    dtype=float,  # tipo de los elementos
    *,
    like=None,    # array_like: prototipo de backend
) -> ndarray
```

## Los parámetros en detalle

### `n` — orden de la matriz
`int` obligatorio. La matriz resultante es $n \times n$. Es el único grado de libertad: no hay forma
de pedir una identidad rectangular ni desplazada por aquí (para eso, [[np.eye]]).

### `dtype` — tipo de los elementos
Por defecto `float` (unos `1.0`). Pasa `dtype=int` para una identidad entera o `dtype=bool` para una
máscara diagonal.

```python
np.identity(2, dtype=int)   # [[1, 0], [0, 1]]
```

### `like` — prototipo de backend
`array_like` keyword-only para crear el array en un sustituto de NumPy (CuPy, Dask...). Rara vez se usa.

## `identity` vs `eye`

`np.identity(n)` equivale **exactamente** a `np.eye(n)`. La diferencia es de intención y de
flexibilidad:

| | `np.identity(n)` | [[np.eye]] |
|--|------------------|------------|
| Forma | siempre cuadrada $(n, n)$ | rectangular posible `(N, M)` |
| Diagonal | siempre la principal | desplazable con `k` |
| Intención | "quiero **la** identidad" | "quiero unos en *una* diagonal" |

## Casos de uso

### Neutro del producto matricial
```python
I = np.identity(3)
A @ I   # == A
```

### Punto de partida para construir matrices
```python
M = np.identity(4)
M[0, 3] = 5   # identidad con una entrada modificada
```

### Término de regularización
Sumar $\lambda I$ a una matriz es un patrón común (ridge, estabilizar una inversión):
```python
A_reg = A + 1e-3 * np.identity(A.shape[0])
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `dtype` float inesperado | por defecto es `float` | `dtype=int` |
| Querer una matriz rectangular | `identity` es siempre cuadrada | usar [[np.eye]] con `M` |
| Querer la diagonal desplazada | `identity` solo da la principal | usar [[np.eye]] con `k` |

## Notas relacionadas

- [[concepto_shape]] — la forma de salida es siempre `(n, n)`
- [[np.eye]] — la versión general (rectangular y diagonal `k`)
- [[np.diag]] — construir una diagonal a partir de un vector
- [[np.zeros]] · [[np.ones]] — otras matrices constantes
