---
title: np.setxor1d — Diferencia simétrica de conjuntos
aliases:
  - setxor1d
  - np.setxor1d
  - diferencia simetrica
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

# np.setxor1d — Diferencia simétrica de conjuntos

## Firma de la función

```python
np.setxor1d(
    ar1,
    ar2,
    assume_unique=False
) -> ndarray
```

## Valor de retorno

Devuelve los valores que están en `ar1` **o** en `ar2`, pero **no en ambos** (diferencia simétrica, `A △ B`). Únicos y **ordenados**. A diferencia de [[np.setdiff1d]], **sí es simétrica**.

```python
import numpy as np
np.setxor1d([1, 2, 3, 4], [3, 4, 5, 6])   # array([1, 2, 5, 6])
```

## Relación con las otras operaciones

```
A △ B = (A ∪ B) − (A ∩ B)
      = setdiff1d(union1d(A,B), intersect1d(A,B))
```

## Parámetros en detalle

### `ar1`, `ar2` — arrays

Se aplanan y deduplican.

### `assume_unique` — optimización

`True` si garantizas ausencia de duplicados.

## Casos de uso

### Detectar elementos que cambiaron entre dos conjuntos

```python
cambios = np.setxor1d(estado_antes, estado_despues)
```

## Buenas prácticas

1. Es **simétrica**: el orden de los argumentos no afecta al resultado.
2. Úsala para encontrar diferencias en ambos sentidos a la vez.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar solo lo nuevo | incluye lo que se fue **y** lo que llegó | usar [[np.setdiff1d]] para un solo sentido |

## Limitaciones

- Solo 1D; siempre ordena.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.setdiff1d]]
- [[np.intersect1d]]
- [[np.union1d]]
