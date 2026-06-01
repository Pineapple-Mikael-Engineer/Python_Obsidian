---
title: np.nonzero — Índices de los elementos no nulos
aliases:
  - nonzero
  - np.nonzero
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.nonzero — Índices de los elementos no nulos

## Firma de la función

```python
np.nonzero(a) -> tuple[ndarray, ...]
```

## Valor de retorno

Devuelve una **tupla de arrays** con las posiciones de los elementos distintos de cero (un array por dimensión). Es la base del modo-índices de [[np.where]].

| Entrada | Retorno |
|---------|---------|
| `[0, 3, 0, 5]` | `(array([1, 3]),)` |
| `[[0, 2], [1, 0]]` | `(array([0, 1]), array([1, 0]))` |

```python
import numpy as np
np.nonzero([0, 3, 0, 5])   # (array([1, 3]),)
```

## Uso con máscaras booleanas

Como `True` cuenta como no-cero, `nonzero` sobre una condición da las posiciones que la cumplen:

```python
arr = np.array([5, -2, 8, -1])
np.nonzero(arr > 0)        # (array([0, 2]),)
arr[np.nonzero(arr > 0)]   # [5, 8]
```

## Reconstruir coordenadas

En 2D, la tupla se desempaqueta en (filas, columnas):

```python
M = np.array([[0, 5], [3, 0]])
filas, cols = np.nonzero(M)
list(zip(filas, cols))     # [(0, 1), (1, 0)]
```

## Parámetros en detalle

### `a` — array de entrada

Cualquier array; los elementos `0`, `False` o vacíos se consideran "cero".

## Casos de uso

### Contar elementos no nulos

```python
len(np.nonzero(arr)[0])    # o np.count_nonzero(arr) (más directo)
```

### Índices de una condición (alternativa a where)

```python
idx = np.nonzero(señal > umbral)[0]
```

## Buenas prácticas

1. Para solo **contar**, usa `np.count_nonzero` (no necesitas los índices).
2. `np.where(cond)` y `np.nonzero(cond)` son equivalentes; elige por legibilidad.
3. El método `arr.nonzero()` es idéntico.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar un array y recibir tupla | siempre devuelve tupla | indexar `[0]` en 1D |
| NaN cuenta como no-cero | `nan != 0` es True | filtrar NaN antes si molesta |

## Limitaciones

- Devuelve siempre una tupla (un eje por dimensión), no un array de coordenadas.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.where]]
- [[np.take]]
