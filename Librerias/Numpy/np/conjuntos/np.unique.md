---
title: np.unique — Elementos únicos (ordenados)
aliases:
  - unique
  - np.unique
  - únicos
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

# np.unique — Elementos únicos (ordenados)

## Firma de la función

```python
np.unique(
    ar,
    return_index=False,
    return_inverse=False,
    return_counts=False,
    axis=None
) -> ndarray | tuple
```

## Valor de retorno

Devuelve los valores **únicos** de `ar`, **ordenados** ascendentemente. Con los flags `return_*` devuelve una tupla con información adicional.

| Flag | Añade al retorno |
|------|------------------|
| (ninguno) | array de únicos |
| `return_index` | índices de la primera aparición en `ar` |
| `return_inverse` | índices para **reconstruir** `ar` desde los únicos |
| `return_counts` | nº de apariciones de cada único |

```python
import numpy as np
np.unique([3, 1, 2, 1, 3, 3])              # array([1, 2, 3])
np.unique([3, 1, 2, 1, 3, 3], return_counts=True)
# (array([1, 2, 3]), array([2, 1, 3]))      → 1×2, 2×1, 3×3
```

## Parámetros en detalle

### `ar` — array de entrada

Se aplana salvo que se indique `axis`.

### `return_counts` — frecuencias

Muy útil para tablas de frecuencia (alternativa a [[np.bincount]] que funciona con cualquier valor, no solo enteros).

### `return_inverse` — reconstrucción

```python
u, inv = np.unique(['a','b','a','c'], return_inverse=True)
# u = ['a','b','c'], inv = [0,1,0,2]
u[inv]   # reconstruye el array original
```

### `axis` — filas/columnas únicas

Con `axis=0`, encuentra **filas** únicas (no elementos):

```python
M = np.array([[1, 2], [1, 2], [3, 4]])
np.unique(M, axis=0)   # [[1, 2], [3, 4]]
```

## Casos de uso

### Tabla de frecuencias

```python
valores, conteos = np.unique(etiquetas, return_counts=True)
```

### Codificar categorías a enteros (label encoding)

```python
categorias, codigos = np.unique(textos, return_inverse=True)
```

## Buenas prácticas

1. `return_counts=True` es la forma general de contar (funciona con strings, floats, etc.).
2. `return_inverse` permite label-encoding en una línea.
3. Usa `axis=0` para filas únicas (deduplicar registros).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar orden original | `unique` **ordena** | usar `return_index` y reordenar |
| Esperar array y recibir tupla | algún `return_*=True` | desempaquetar la tupla |

## Limitaciones

- Siempre ordena (no conserva el orden de aparición).

## Notas relacionadas

- [[concepto_indexing]]
- [[np.bincount]]
- [[np.intersect1d]]
- [[np.union1d]]
