---
title: np.identity — Matriz identidad cuadrada
aliases:
  - identity
  - np.identity
  - matriz identidad
tags:
  - numpy
  - api/funcion
  - creacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.identity — Matriz identidad cuadrada

## Firma de la función

```python
np.identity(
    n,
    dtype=float,
    *,
    like=None
) -> ndarray
```

## Valor de retorno

Devuelve la **matriz identidad** `n × n`: unos en la diagonal principal y ceros en el resto. Es un caso particular (y más explícito) de [[np.eye]] sin diagonales desplazadas ni forma rectangular.

| Llamada | Resultado |
|---------|-----------|
| `np.identity(2)` | `[[1, 0], [0, 1]]` |
| `np.identity(3)` | identidad 3×3 |

```python
import numpy as np
np.identity(3)
# array([[1., 0., 0.],
#        [0., 1., 0.],
#        [0., 0., 1.]])
```

## identity vs eye

| | `np.identity(n)` | [[np.eye]] |
|--|------------------|-----------|
| Forma | siempre cuadrada `n×n` | rectangular posible (`N, M`) |
| Diagonal | siempre la principal | desplazable con `k` |
| Intención | "quiero la identidad" | "quiero unos en *una* diagonal" |

`np.identity(n)` equivale exactamente a `np.eye(n)`.

## Parámetros en detalle

### `n` — tamaño

Número de filas y columnas (la matriz es `n × n`).

### `dtype` — tipo

Por defecto `float`. Para enteros, `dtype=int`.

## Casos de uso

### Elemento neutro en multiplicación matricial

```python
I = np.identity(3)
A @ I   # == A
```

### Punto de partida para construir matrices

```python
M = np.identity(4)
M[0, 3] = 5   # identidad modificada
```

## Buenas prácticas

1. Úsala cuando quieras dejar claro que es **la identidad**; usa [[np.eye]] si necesitas flexibilidad (rectangular, diagonal desplazada).
2. Fija `dtype=int` si trabajas con matrices enteras.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| dtype float inesperado | por defecto `float` | `dtype=int` |
| Querer rectangular | `identity` es cuadrada | usar [[np.eye]] |

## Limitaciones

- Solo cuadrada y diagonal principal: cualquier variación requiere [[np.eye]].

## Notas relacionadas

- [[concepto_shape]]
- [[np.eye]]
- [[np.zeros]]
