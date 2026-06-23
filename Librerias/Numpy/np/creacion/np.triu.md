---
title: np.triu — parte triangular superior (ceros por debajo de la diagonal k)
aliases:
  - triu
  - np.triu
  - triangular superior
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

# np.triu — parte triangular superior (ceros por debajo de la diagonal k)

`np.triu` devuelve la **parte triangular superior** de una matriz: conserva los elementos en y por
encima de la diagonal `k`, y pone a **cero** todo lo que está por debajo. Es la complementaria de
[[np.tril]]: donde una guarda el triángulo de abajo, esta guarda el de arriba. **Transforma** una
matriz existente (no la crea de cero) y soporta lotes N-D operando sobre los **dos últimos ejes**.

## La idea

El elemento se conserva si su columna es al menos su fila más el desplazamiento `k`, y se anula en
caso contrario:

$$
\text{triu}(A)_{ij} = \begin{cases} A_{ij} & \text{si } j \ge i + k \\ 0 & \text{si } j < i + k \end{cases}
$$

Con $k = 0$ se mantiene la diagonal principal y todo lo de encima; el triángulo inferior estricto se
pone a cero:

$$
\text{triu}\!\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}
= \begin{bmatrix} a & b & c \\ 0 & e & f \\ 0 & 0 & i \end{bmatrix}
$$

`k` mueve la frontera: $k > 0$ recorta también superdiagonales (conserva menos), $k < 0$ deja pasar
parte del triángulo inferior (conserva más):

$$
\text{triu}(A,\, k=1) = \begin{bmatrix} 0 & b & c \\ 0 & 0 & f \\ 0 & 0 & 0 \end{bmatrix}
\qquad
\text{triu}(A,\, k=-1) = \begin{bmatrix} a & b & c \\ d & e & f \\ 0 & h & i \end{bmatrix}
$$

El **mapa de shapes** es la identidad: `triu` **no cambia la forma**, solo anula entradas. Ver
[[concepto_shape]].

$$
(n_0,\dots,n_{k-2},\, m,\, n) \xrightarrow{\ \text{triu}\ } (n_0,\dots,n_{k-2},\, m,\, n)
$$

## Firma

```python
np.triu(
    m,      # array_like: matriz (o lote N-D); se opera en los 2 últimos ejes
    k=0,    # int: diagonal frontera (0 principal, >0 conserva menos, <0 conserva más)
) -> ndarray
```

## Los parámetros en detalle

### `m` — la matriz (o lote) de entrada
`array_like` con `ndim >= 2`. Con más de 2 ejes, los **dos últimos** forman la matriz y los demás son
lote; la máscara se aplica a cada matriz por separado. No necesita ser cuadrada.

```python
A = np.arange(1, 10).reshape(3, 3)
np.triu(A)
# array([[1, 2, 3],
#        [0, 5, 6],
#        [0, 0, 9]])
```

### `k` — diagonal frontera
`int` (defecto `0`). `0` incluye la diagonal principal; `k > 0` excluye además `k` superdiagonales (el
triángulo retenido se encoge); `k < 0` conserva también `|k|` subdiagonales (el triángulo retenido
crece). Es el signo **opuesto** al efecto en [[np.tril]].

```python
np.triu(A, k=1)    # también borra la diagonal principal (estrictamente superior)
np.triu(A, k=-1)   # conserva además la primera subdiagonal
```

## El caso N-D

Sobre un tensor de más de 2 ejes, `np.triu` opera sobre los **dos últimos ejes** y trata el resto como
lote. La forma se conserva; cada matriz del lote recibe la misma máscara triangular superior.

| `m.shape` | salida | lectura |
|-----------|--------|---------|
| `(n, n)` | `(n, n)` | una matriz triangular superior |
| `(m, n)` | `(m, n)` | rectangular: misma regla $j \ge i + k$ |
| `(b, n, n)` | `(b, n, n)` | una triangular superior por matriz del lote |
| `(b, c, n, n)` | `(b, c, n, n)` | máscara aplicada a cada matriz de la rejilla |

```python
P = np.arange(2*3*3).reshape(2, 3, 3)
np.triu(P).shape   # (2, 3, 3) → la triangular superior de cada matriz del lote
```

## Casos de uso

### Factor $U$ de una factorización LU
```python
U = np.triu(A)   # candidata a matriz triangular superior
```

### Pares sin repetir (índices i < j)
La triangular superior estricta selecciona cada par una sola vez (matrices de distancias, correlación):
```python
sup = np.triu(D, k=1)   # solo el triángulo estricto, sin la diagonal
```

### Quedarse con la diagonal y lo de arriba
```python
np.triu(A)   # incluye la diagonal principal
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Confundir superior con inferior | `triu` conserva **arriba**; abajo está [[np.tril]] | recuerda: triangular **upper** |
| Se conservó la diagonal sin quererlo | `k=0` la incluye | usar `k=1` para el triángulo estricto |
| Esperar una matriz nueva | `triu` **transforma**, no crea de cero | para crear usa [[np.eye]] / [[np.diag]] |
| `ndim < 2` falla | la entrada es 1D | `triu` exige al menos 2 ejes |

## Notas relacionadas

- [[concepto_shape]] — la forma se conserva; opera en los 2 últimos ejes en N-D
- [[np.tril]] — la parte triangular **inferior** (complementaria)
- [[np.diag]] · [[np.diagonal]] — la diagonal en sí
- [[np.eye]] — matriz de unos en una diagonal
