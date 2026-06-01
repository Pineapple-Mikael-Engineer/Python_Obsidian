---
title: np.union1d — Unión de dos arrays
aliases:
  - union1d
  - np.union1d
  - union
tags:
  - numpy
  - api/funcion
  - conjuntos

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.union1d — Unión de dos arrays

## Firma de la función

```python
np.union1d(ar1, ar2) -> ndarray
```

## Valor de retorno

Devuelve **todos** los valores presentes en `ar1` **o** `ar2`, únicos y **ordenados**. Equivale a la unión de conjuntos `A ∪ B`.

```python
import numpy as np
np.union1d([1, 2, 3], [3, 4, 5])   # array([1, 2, 3, 4, 5])
```

## Parámetros en detalle

### `ar1`, `ar2` — arrays

Se aplanan y deduplican.

## Casos de uso

### Combinar dos conjuntos sin repetir

```python
todas_las_etiquetas = np.union1d(set_train, set_test)
```

### Unir varios arrays

```python
from functools import reduce
reduce(np.union1d, [a, b, c, d])
```

## Buenas prácticas

1. Resultado único y ordenado.
2. Para más de 2 arrays, encadena con `functools.reduce` o usa `np.unique(np.concatenate([...]))`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar orden de inserción | `union1d` ordena | reordenar aparte si hace falta |

## Limitaciones

- Solo 1D; siempre ordena.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.unique]]
- [[np.intersect1d]]
- [[np.setdiff1d]]
