---
title: permutaciones — barajar y permutar arrays
tags:
  - numpy
  - indice
draft: false
---

# permutaciones — barajar y permutar arrays

Dos funciones para **reordenar un array al azar**. La distinción clave es **copia vs. in-place**, y es justo la que produce bugs sutiles: [[np.random.shuffle]] devuelve `None` y muta el original, así que quien espere el array barajado en el valor de retorno obtiene `None` en silencio, sin error. [[np.random.permutation]], en cambio, devuelve una **copia nueva** y deja el original intacto.

Ambas comparten una regla de eje importante: en arrays N-D **solo reordenan el primer eje** (las filas); el contenido de cada fila se mueve entero, sin mezclarse por dentro. Para una permutación de la forma $(n_0, n_1, \dots, n_{k-1})$, solo se permuta $n_0$:

$$ (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{permutar eje 0}\ }\; (n_0, n_1, \dots, n_{k-1}) $$

## Funciones

| Función | ¿Modifica el original? | Devuelve | Acepta entero | Eje |
|---------|------------------------|----------|---------------|-----|
| [[np.random.permutation]] | No | copia barajada | Sí (`n` → `arange(n)`) | primer eje |
| [[np.random.shuffle]] | Sí (in-place) | `None` | No (`TypeError`) | primer eje |

`permutation(n)` con un entero genera directamente una permutación de `np.arange(n)`: el modo idiomático de crear índices aleatorios sin construir el array antes. `shuffle` solo acepta un array existente que mutar.

## Regla de elección

- ¿Necesitas el original intacto (bootstrapping, splits de validación)? → `permutation`.
- ¿Quieres modificar in-place y ahorrar la copia en memoria? → `shuffle`.
- ¿Quieres barajar índices para reordenar varios arrays a la vez? → `permutation(len(x))`.

```python
import numpy as np
np.random.seed(0)

arr = np.array([1, 2, 3, 4, 5])

# permutation: el original NO cambia
mezclado = np.random.permutation(arr)
# arr      -> [1, 2, 3, 4, 5]  (intacto)
# mezclado -> [3, 5, 2, 1, 4]  (copia nueva)

# shuffle: modifica arr directamente, devuelve None
np.random.shuffle(arr)
# arr -> [4, 1, 5, 3, 2]  (modificado in-place)

# permutation con entero: permutación de arange(n)
np.random.permutation(5)   # array([0, 3, 1, 2, 4])
```

## Forma moderna

En código nuevo, prefiere el [[np.random.default_rng|Generator]] explícito, que además permite barajar por **cualquier eje** (no solo el primero):

```python
rng = np.random.default_rng(0)
rng.permutation(arr)          # copia
rng.shuffle(arr)              # in-place
rng.permuted(M, axis=1)       # permuta dentro de cada fila
```
