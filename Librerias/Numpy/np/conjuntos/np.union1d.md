---
title: np.union1d — unión, elementos en cualquiera de los dos
aliases:
  - union1d
  - np.union1d
  - unión
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

# np.union1d — unión, elementos en cualquiera de los dos

`np.union1d` devuelve todos los valores que aparecen en `ar1` **o** en `ar2` (o en ambos): la unión
de conjuntos $A \cup B$. Como el resto de operaciones binarias de conjunto, **aplana** las dos
entradas a 1D, combina y devuelve el resultado **único y ordenado**. Es la versión vectorizada de
`set(a) | set(b)`. Internamente equivale a `np.unique(np.concatenate((ar1, ar2)))`.

## La idea

La operación es la **unión**: un valor sobrevive si está en al menos uno de los dos arrays.

$$ A \cup B \;=\; \{\, x : x \in A \ \vee\ x \in B \,\} $$

La salida es **siempre 1D**, ordenada de menor a mayor y sin repetidos. Da igual el shape de las
entradas: ambas se aplanan. No hay caso N-D. La unión es **simétrica**: el orden de los argumentos
no cambia el resultado.

```python
import numpy as np
np.union1d([1, 2, 3], [3, 4, 5])   # array([1, 2, 3, 4, 5])
```

## Firma

```python
np.union1d(
    ar1,   # array_like: primer array (se aplana)
    ar2,   # array_like: segundo array (se aplana)
) -> ndarray
```

## Los parámetros en detalle

### `ar1`, `ar2` — los dos arrays
`array_like`. Se **aplanan a 1D**, se concatenan y se deduplican con [[np.unique]]. No hay
`assume_unique` ni flags de índices: `union1d` siempre pasa por `unique`, así que cualquier
duplicado en la entrada se elimina de todos modos.

## El caso N-D

No aplica: `union1d` **aplana** ambas entradas y devuelve siempre un vector 1D ordenado. Para
combinar más de dos arrays, encadena con `functools.reduce` o concatena y deduplica directamente:

```python
from functools import reduce
reduce(np.union1d, [a, b, c, d])        # unión de los cuatro
np.unique(np.concatenate([a, b, c]))    # equivalente explícito
```

## Casos de uso

### Combinar dos conjuntos sin repetir
```python
set_train = np.array([0, 1, 2])
set_test  = np.array([2, 3, 4])
todas = np.union1d(set_train, set_test)   # [0, 1, 2, 3, 4]
```

### Vocabulario común de varias fuentes
```python
from functools import reduce
vocabulario = reduce(np.union1d, [tokens_doc1, tokens_doc2, tokens_doc3])
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar el orden de inserción | `union1d` siempre **ordena** | reordenar aparte si hace falta el orden original |
| Esperar conservar el shape | `union1d` aplana siempre | la salida es 1D por diseño |
| Querer unir N arrays de golpe | la firma solo admite 2 | `reduce(np.union1d, lista)` |

## Notas relacionadas

- [[concepto_indexing]] — la salida es un índice ordenado de valores
- [[np.unique]] — `union1d` es `unique` sobre la concatenación
- [[Librerias/Numpy/np/conjuntos/index|operaciones de conjunto]] — la nota madre
- [[np.intersect1d]] · [[np.setdiff1d]] · [[np.setxor1d]]
