---
title: np.intersect1d — intersección, elementos en ambos arrays
aliases:
  - intersect1d
  - np.intersect1d
  - intersección
tags:
  - numpy
  - api/funcion
  - conjuntos

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.intersect1d — intersección, elementos en ambos arrays

`np.intersect1d` devuelve los valores que aparecen **en los dos** arrays a la vez: la intersección
de conjuntos $A \cap B$. Como todas las operaciones binarias de conjunto en NumPy, **aplana** ambas
entradas a 1D, elimina duplicados y devuelve el resultado **único y ordenado**. Es la forma
vectorizada de `set(a) & set(b)`, pero sobre arrays contiguos y mucho más rápida para grandes
volúmenes numéricos.

## La idea

La operación es la **intersección**: un valor sobrevive solo si está presente en `ar1` **y** en
`ar2`.

$$ A \cap B \;=\; \{\, x : x \in A \ \wedge\ x \in B \,\} $$

La salida es **siempre 1D**, ordenada de menor a mayor y sin repetidos, sea cual sea el shape de la
entrada (ambos arrays se aplanan primero). No hay caso N-D: el shape de las entradas no se conserva.

```python
import numpy as np
np.intersect1d([1, 2, 3, 4], [3, 4, 5, 6])   # array([3, 4])
np.intersect1d([[1, 2], [3, 4]], [4, 4, 9])  # array([4])  → se aplana el 2D
```

## Firma

```python
np.intersect1d(
    ar1,                    # array_like: primer array (se aplana)
    ar2,                    # array_like: segundo array (se aplana)
    assume_unique=False,    # bool: True salta la deduplicación interna (más rápido)
    return_indices=False,   # bool: añade los índices de los comunes en cada array
) -> ndarray | tuple
```

## Los parámetros en detalle

### `ar1`, `ar2` — los dos arrays
`array_like`. Se **aplanan a 1D** y se deduplican internamente. La intersección es **simétrica**:
`intersect1d(a, b)` y `intersect1d(b, a)` dan el mismo conjunto.

### `assume_unique` — saltarse la deduplicación
`bool`. Si garantizas que **ninguna** entrada tiene duplicados, `True` evita el paso interno de
`unique` y acelera. Si lo activas con duplicados presentes, el resultado puede ser **incorrecto** —
úsalo solo cuando estés seguro.

### `return_indices` — dónde están los comunes
`bool`. Si `True`, el retorno pasa a ser la tupla `(comun, idx1, idx2)`, donde `ar1[idx1]` y
`ar2[idx2]` reproducen los valores comunes. Útil para recuperar datos asociados a cada coincidencia.

```python
comun, i1, i2 = np.intersect1d([10, 20, 30], [30, 40, 10], return_indices=True)
# comun = [10, 30], i1 = [0, 2], i2 = [2, 0]
```

## El caso N-D

No aplica: `intersect1d` **aplana** ambas entradas y devuelve siempre un vector 1D ordenado. Un array
de cualquier shape se trata como su lista plana de valores. Si necesitas razonar sobre la forma
original, usa [[np.isin]], que sí conserva el shape de su primer argumento.

## Casos de uso

### Elementos presentes en ambos conjuntos
```python
clientes_a = np.array([1, 2, 3, 4])
clientes_b = np.array([3, 4, 5, 6])
np.intersect1d(clientes_a, clientes_b)   # [3, 4]  → clientes comunes
```

### Intersección de más de dos arrays
```python
from functools import reduce
reduce(np.intersect1d, [a, b, c])   # valores presentes en los tres
```

### Recuperar datos alineados con la coincidencia
```python
ids, i_a, i_b = np.intersect1d(ids_a, ids_b, return_indices=True)
precios_comunes = precios_a[i_a]   # precio de cada id común desde la tabla A
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultados raros con `assume_unique=True` | había duplicados en alguna entrada | dejar `assume_unique=False` |
| Esperar conservar el shape 2D | `intersect1d` aplana siempre | usar [[np.isin]] si necesitas la forma |
| Esperar un array y recibir tupla | `return_indices=True` | desempaquetar `c, i1, i2 = ...` |

## Notas relacionadas

- [[concepto_indexing]] — `return_indices` reindexa los arrays originales
- [[np.unique]] — la base: deduplicar y ordenar
- [[Librerias/Numpy/np/conjuntos/index|operaciones de conjunto]] — la nota madre
- [[np.union1d]] · [[np.setdiff1d]] · [[np.isin]]
