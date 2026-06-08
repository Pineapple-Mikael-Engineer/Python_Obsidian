---
title: permutaciones — mezcla y permutacion de arrays
tags:
  - numpy
  - indice
draft: false
---

# permutaciones — mezcla y permutacion de arrays

Dos funciones para reordenar arrays aleatoriamente. La diferencia es en-lugar vs. copia — una distincion que puede causar bugs sutiles: `shuffle` devuelve `None` y quien espere el array mezclado en el valor de retorno obtendra silenciosamente `None` en lugar de un error.

## Funciones

| Funcion | Modifica el original | Devuelve | Descripcion |
|---------|---------------------|----------|-------------|
| [[np.random.permutation]] | No | Copia mezclada | Permutacion sin tocar el original; acepta array o entero |
| [[np.random.shuffle]] | Si (in-place) | `None` | Mezcla el array en su lugar; solo mezcla a lo largo del primer eje |

`permutation` con un entero `n` genera directamente una permutacion de `np.arange(n)`, util para crear indices aleatorios sin crear el array previo. `shuffle` en arrays 2D mezcla las filas pero no los elementos dentro de cada fila — mezcla a lo largo del eje 0 unicamente.

## Regla de eleccion

- Si necesitas el array original intacto (bootstrapping, splits de validacion) → `permutation`.
- Si quieres modificar in-place y ahorrar la copia en memoria → `shuffle`.

```python
import numpy as np
np.random.seed(0)

arr = np.array([1, 2, 3, 4, 5])

# permutation: el original no cambia
mezclado = np.random.permutation(arr)
# arr      -> [1, 2, 3, 4, 5]  (intacto)
# mezclado -> [2, 5, 4, 3, 1]  (copia nueva)

# shuffle: modifica arr directamente, devuelve None
np.random.shuffle(arr)
# arr -> [2, 5, 4, 3, 1]  (modificado)

# permutation con entero: permutacion de arange(n)
np.random.permutation(5)   # array([1, 4, 0, 2, 3])
```
