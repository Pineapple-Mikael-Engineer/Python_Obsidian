---
title: np.setdiff1d — Diferencia de conjuntos (A − B)
aliases:
  - setdiff1d
  - np.setdiff1d
  - diferencia
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

# np.setdiff1d — Diferencia de conjuntos (A − B)

## Firma de la función

```python
np.setdiff1d(
    ar1,
    ar2,
    assume_unique=False
) -> ndarray
```

## Valor de retorno

Devuelve los valores de `ar1` que **no** están en `ar2`, únicos y **ordenados**. Equivale a la diferencia de conjuntos `A − B`. **No es simétrica**: `setdiff1d(A, B) ≠ setdiff1d(B, A)`.

```python
import numpy as np
np.setdiff1d([1, 2, 3, 4], [3, 4, 5])   # array([1, 2])
np.setdiff1d([3, 4, 5], [1, 2, 3, 4])   # array([5])  → distinto
```

## Parámetros en detalle

### `ar1`, `ar2` — arrays

`ar1` es el conjunto base; se quitan los elementos que aparezcan en `ar2`.

### `assume_unique` — optimización

`True` acelera si garantizas que no hay duplicados.

## Casos de uso

### Elementos exclusivos del primer conjunto

```python
solo_en_train = np.setdiff1d(ids_train, ids_test)
```

### Filtrar valores prohibidos

```python
validos = np.setdiff1d(candidatos, lista_negra)
```

## Buenas prácticas

1. Recuerda que es **direccional**: el orden de los argumentos importa.
2. Para la diferencia simétrica (en uno u otro pero no ambos), usa [[np.setxor1d]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado vacío inesperado | argumentos invertidos | revisar cuál es el conjunto base |

## Limitaciones

- Solo 1D; no simétrica; siempre ordena.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.intersect1d]]
- [[np.union1d]]
- [[np.setxor1d]]
