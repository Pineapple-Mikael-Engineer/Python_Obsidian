---
title: np.random.permutation — Copia permutada aleatoriamente
aliases:
  - permutation
  - random.permutation
  - np.random.permutation
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray
inplace: false
draft: false
---

# np.random.permutation — Permuta devolviendo una copia

## Firma de la función

```python
np.random.permutation(
    x
) -> ndarray
```

## Valor de retorno

Devuelve un **nuevo** `ndarray` con los elementos permutados al azar; **no modifica** `x`. El comportamiento depende del tipo de `x`:

| `x` | Resultado | Eje permutado |
|-----|-----------|---------------|
| entero `n` | copia de `np.arange(n)` barajada | — |
| array 1D | copia barajada | único eje |
| array nD | copia barajada por el **primer eje** | eje 0 (filas) |

```python
import numpy as np
np.random.seed(0)

np.random.permutation(5)
# array([2, 0, 1, 3, 4])   → permuta arange(5)

original = np.array([10, 20, 30, 40])
np.random.permutation(original)
# array([20, 40, 10, 30])
original
# array([10, 20, 30, 40])   → intacto (copia)
```

## Parámetros en detalle

### `x` — entero o array a permutar

Si es un `int`, equivale a permutar `np.arange(x)`. Si es un array de cualquier [[concepto_shape|shape]], se baraja a lo largo del **primer eje**; el contenido de cada fila se mantiene unido.

```python
M = np.arange(9).reshape(3, 3)
np.random.permutation(M)
# reordena filas completas; las columnas internas no se mezclan
```

## Casos de uso

### Barajar índices para muestreo sin alterar los datos

```python
idx = np.random.permutation(len(datos))
datos_barajados = datos[idx]       # datos original intacto
```

### Dividir en train/test

```python
perm = np.random.permutation(n)
train, test = perm[:800], perm[800:]
```

## Buenas prácticas

1. Úsala cuando necesites **conservar el original**; si quieres barajar in-place usa [[np.random.shuffle]].
2. Para nD recuerda que solo se permuta el **primer eje** (filas).
3. Combínala con `seed` o `default_rng` para reproducibilidad.
4. En código nuevo prefiere `rng = np.random.default_rng(); rng.permutation(x)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperabas mezclar todos los elementos de una matriz | Solo permuta el eje 0 | Aplanar con `ravel()` antes, o `rng.permuted` |
| Creías que modificaba `x` | `permutation` devuelve **copia** | Usar [[np.random.shuffle]] para in-place |
| Resultado no reproducible | Sin semilla fijada | Llamar antes a [[np.random.seed]] |

## Notas relacionadas

- [[np.random.shuffle]]
- [[np.random.seed]]
- [[np.random.default_rng]]
- [[concepto_shape]]
- [[concepto_views_vs_copias]]
