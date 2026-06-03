---
title: np.intersect1d — Intersección de dos arrays
aliases:
  - intersect1d
  - np.intersect1d
  - interseccion
tags:
  - numpy
  - api/funcion
  - conjuntos

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.intersect1d — Intersección de dos arrays

## Firma de la función

```python
np.intersect1d(
    ar1,
    ar2,
    assume_unique=False,
    return_indices=False
) -> ndarray | tuple
```

## Valor de retorno

Devuelve los valores **comunes** a `ar1` y `ar2`, únicos y **ordenados**. Equivale a la intersección de conjuntos `A ∩ B`.

```python
import numpy as np
np.intersect1d([1, 2, 3, 4], [3, 4, 5, 6])   # array([3, 4])
```

## Parámetros en detalle

### `ar1`, `ar2` — arrays

Se aplanan; los duplicados se eliminan.

### `assume_unique` — optimización

Si garantizas que no hay duplicados, `True` acelera el cálculo (sin verificar).

### `return_indices` — posiciones

Devuelve también los índices de los comunes en cada array.

## Casos de uso

### Elementos presentes en ambos conjuntos

```python
clientes_comunes = np.intersect1d(lista_a, lista_b)
```

## Buenas prácticas

1. El resultado es único y ordenado (como [[np.unique]]).
2. Usa `assume_unique=True` solo si estás seguro (es más rápido).
3. Para más de 2 arrays, encadena: `reduce(np.intersect1d, [a, b, c])`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultados raros con `assume_unique=True` | había duplicados | dejarlo en `False` |

## Limitaciones

- Solo 1D (aplana la entrada); compara por igualdad de valor.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.unique]]
- [[np.union1d]]
- [[np.setdiff1d]]
