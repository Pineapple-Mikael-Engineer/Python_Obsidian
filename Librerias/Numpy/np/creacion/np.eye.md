---
title: np.eye — Matriz con unos en una diagonal
aliases:
  - eye
  - np.eye
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
  - concepto_dtype

draft: false
---

# np.eye — Matriz con unos en una diagonal

## Firma de la función

```python
np.eye(
    N,
    M=None,
    k=0,
    dtype=float,
    order='C',
    *,
    like=None
) -> ndarray
```

## Valor de retorno

Devuelve una matriz 2D con **unos en una diagonal** y ceros en el resto. Por defecto es la **matriz identidad** (cuadrada, diagonal principal). Es más flexible que [[np.identity]] porque permite matrices rectangulares y diagonales desplazadas.

| Llamada | Resultado |
|---------|-----------|
| `np.eye(3)` | identidad 3×3 |
| `np.eye(2, 3)` | `(2, 3)` con diagonal de unos |
| `np.eye(3, k=1)` | unos en la diagonal **superior** |
| `np.eye(3, k=-1)` | unos en la diagonal **inferior** |

```python
import numpy as np
np.eye(3)
# array([[1., 0., 0.],
#        [0., 1., 0.],
#        [0., 0., 1.]])
```

## Parámetros en detalle

### `N` — número de filas

Obligatorio. Define la altura.

### `M` — número de columnas

Si es `None`, se usa `N` (matriz cuadrada).

### `k` — diagonal a rellenar

`0` principal, `>0` diagonales superiores, `<0` inferiores.

```python
np.eye(3, k=1)
# array([[0., 1., 0.],
#        [0., 0., 1.],
#        [0., 0., 0.]])
```

### `dtype` — tipo

Por defecto `float`. Usa `int`/`bool` según necesidad (ver [[concepto_dtype]]).

## Casos de uso

### Matriz identidad para álgebra lineal

```python
I = np.eye(4)
A @ I   # == A
```

### Codificación one-hot

```python
clases = np.array([0, 2, 1])
onehot = np.eye(3)[clases]
# [[1,0,0], [0,0,1], [0,1,0]]
```

### Matriz de desplazamiento (shift)

```python
S = np.eye(4, k=1)   # mueve elementos una posición
```

## Buenas prácticas

1. Para la identidad cuadrada pura, [[np.identity]] es un alias más explícito.
2. El truco `np.eye(n)[indices]` es la forma idiomática de **one-hot encoding**.
3. Usa `k` para construir matrices banda o de desplazamiento.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| dtype float donde querías int | por defecto `float` | pasar `dtype=int` |
| Esperar cuadrada y obtener rectangular | se pasó `M` distinto de `N` | omitir `M` para cuadrada |

## Limitaciones

- Solo genera matrices 2D.
- Para identidad cuadrada simple, [[np.identity]] comunica mejor la intención.

## Notas relacionadas

- [[concepto_shape]]
- [[np.identity]]
- [[np.zeros]]
- [[np.full]]
