---
title: permutaciones — mezcla y permutacion de arrays
tags:
  - numpy
  - indice
draft: false
---

# permutaciones — mezcla y permutacion de arrays

Dos funciones para reordenar arrays aleatoriamente. Difieren en si modifican el array original o devuelven una copia.

## Funciones

| Funcion | Modifica el original | Devuelve | Descripcion |
|---------|---------------------|----------|-------------|
| [[np.random.permutation]] | No | Copia mezclada | Permutacion sin tocar el original |
| [[np.random.shuffle]] | Si (in-place) | `None` | Mezcla el array en su lugar |

## Regla de eleccion

- Si necesitas el array original intacto → `permutation`.
- Si quieres modificar in-place y ahorrar memoria → `shuffle`.

```python
import numpy as np
np.random.seed(0)

arr = np.array([1, 2, 3, 4, 5])

# permutation: el original no cambia
mezclado = np.random.permutation(arr)
# arr  -> [1, 2, 3, 4, 5]  (intacto)
# mezclado -> [2, 5, 4, 3, 1]  (copia nueva)

# shuffle: modifica arr directamente
np.random.shuffle(arr)
# arr  -> [2, 5, 4, 3, 1]  (modificado)
# devuelve None
```

## permutation con entero

`permutation(n)` con un entero genera una permutacion de `np.arange(n)`:

```python
np.random.permutation(5)   # array([1, 4, 0, 2, 3])
```
