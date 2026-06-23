---
title: np.tril — parte triangular inferior (ceros por encima de la diagonal k)
aliases:
  - tril
  - np.tril
  - triangular inferior
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

# np.tril — parte triangular inferior (ceros por encima de la diagonal k)

`np.tril` devuelve la **parte triangular inferior** de una matriz: conserva los elementos en y por
debajo de la diagonal `k`, y pone a **cero** todo lo que está por encima. No fabrica una matriz desde
cero como [[np.eye]]; **transforma** una matriz existente anulando su triángulo superior. Soporta
lotes N-D: aplica la máscara sobre los **dos últimos ejes** de cada matriz del tensor.

## La idea

El elemento se conserva si su columna no supera a su fila más el desplazamiento `k`, y se anula en
caso contrario:

$$
\text{tril}(A)_{ij} = \begin{cases} A_{ij} & \text{si } j \le i + k \\ 0 & \text{si } j > i + k \end{cases}
$$

Con $k = 0$ se mantiene la diagonal principal y todo lo de debajo; el triángulo superior estricto se
pone a cero:

$$
\text{tril}\!\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
= \begin{bmatrix} a & 0 & 0 \\ d & e & 0 \\ g & h & i \end{bmatrix}
$$

`k` mueve la frontera diagonal: $k > 0$ conserva además superdiagonales (deja pasar más), $k < 0$ corta
también parte del triángulo inferior (deja pasar menos):

$$
\text{tril}(A,\, k=-1) = \begin{bmatrix} 0 & 0 & 0 \\ d & 0 & 0 \\ g & h & 0 \end{bmatrix}
\qquad
\text{tril}(A,\, k=1) = \begin{bmatrix} a & b & 0 \\ d & e & f \\ g & h & i \end{bmatrix}
$$

El **mapa de shapes** es la identidad: `tril` **no cambia la forma**, solo anula entradas. Ver
[[concepto_shape]].

$$
(n_0,\dots,n_{k-2},\, m,\, n) \xrightarrow{\ \text{tril}\ } (n_0,\dots,n_{k-2},\, m,\, n)
$$

## Firma

```python
np.tril(
    m,      # array_like: matriz (o lote N-D); se opera en los 2 últimos ejes
    k=0,    # int: diagonal frontera (0 principal, >0 conserva más, <0 conserva menos)
) -> ndarray
```

## Los parámetros en detalle

### `m` — la matriz (o lote) de entrada
`array_like` con `ndim >= 2`. Si tiene más de 2 ejes, los **dos últimos** forman la matriz y los
demás son ejes de lote: la máscara triangular se aplica de forma independiente a cada matriz. No
necesita ser cuadrada.

```python
A = np.arange(1, 10).reshape(3, 3)
np.tril(A)
# array([[1, 0, 0],
#        [4, 5, 0],
#        [7, 8, 9]])
```

### `k` — diagonal frontera
`int` (defecto `0`). Marca hasta qué diagonal se conserva: `0` incluye la principal; `k > 0` conserva
además `k` superdiagonales (el triángulo retenido crece); `k < 0` excluye también `|k|` diagonales por
debajo de la principal (el triángulo retenido se encoge).

```python
np.tril(A, k=-1)   # también borra la diagonal principal
np.tril(A, k=1)    # conserva además la primera superdiagonal
```

## El caso N-D

Sobre un tensor de más de 2 ejes, `np.tril` opera sobre los **dos últimos ejes** y trata el resto como
lote. La forma se conserva intacta; cada matriz del lote recibe la misma máscara triangular inferior.

| `m.shape` | salida | lectura |
|-----------|--------|---------|
| `(n, n)` | `(n, n)` | una matriz triangular inferior |
| `(m, n)` | `(m, n)` | rectangular: misma regla $j \le i + k$ |
| `(b, n, n)` | `(b, n, n)` | una triangular inferior por matriz del lote |
| `(b, c, n, n)` | `(b, c, n, n)` | máscara aplicada a cada matriz de la rejilla |

```python
P = np.arange(2*3*3).reshape(2, 3, 3)
np.tril(P).shape   # (2, 3, 3) → la triangular inferior de cada una de las 2 matrices
```

## Casos de uso

### Factorizaciones y sistemas triangulares
La parte inferior $L$ de una factorización LU o de Cholesky se aísla con `tril`:
```python
L = np.tril(A)            # candidata a matriz triangular inferior
```

### Máscara causal (atención, series temporales)
Una matriz booleana triangular impide "mirar al futuro": cada fila solo ve hasta su propia posición.
```python
mascara = np.tril(np.ones((n, n), dtype=bool))   # True en/bajo la diagonal
```

### Quedarse solo con el triángulo estricto
```python
np.tril(A, k=-1)   # inferior sin la diagonal principal
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Confundir inferior con superior | `tril` conserva **abajo**; arriba está [[np.triu]] | recuerda: triangular **lower** |
| Se borró la diagonal sin querer | se pasó `k=-1` (excluye la principal) | usar `k=0` para incluirla |
| Esperar una matriz nueva | `tril` **transforma**, no crea de cero | para crear usa [[np.eye]] / [[np.diag]] |
| `ndim < 2` falla | la entrada es 1D | `tril` exige al menos 2 ejes |

## Notas relacionadas

- [[concepto_shape]] — la forma se conserva; opera en los 2 últimos ejes en N-D
- [[np.triu]] — la parte triangular **superior** (complementaria)
- [[np.diag]] · [[np.diagonal]] — la diagonal en sí
- [[np.eye]] — matriz de unos en una diagonal (a menudo base de la máscara)
