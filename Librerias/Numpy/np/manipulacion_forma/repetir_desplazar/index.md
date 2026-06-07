---
title: np/manipulacion_forma/repetir_desplazar — duplicar y rotar elementos
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/repetir_desplazar — duplicar y rotar elementos

`repetir_desplazar/` agrupa las funciones que duplican o mueven elementos dentro del array. A diferencia de `combinar/`, estas operaciones trabajan sobre un solo array y pueden ampliar su tamano o simplemente reposicionar su contenido.

La distincion principal: `np.tile` y `np.repeat` aumentan el tamano del array duplicando datos, mientras que `np.roll` lo mantiene igual y desplaza los elementos de forma circular.

## Funciones

| Funcion | Que hace | Tamano del resultado |
|---------|----------|----------------------|
| [[np.tile]] | Repite el array completo N veces como un mosaico | Mayor |
| [[np.repeat]] | Repite cada elemento N veces individualmente | Mayor |
| [[np.roll]] | Desplaza elementos circularmente a lo largo de un eje | Igual |

## Diferencia entre tile y repeat

```python
import numpy as np
a = np.array([1, 2, 3])

np.tile(a, 2)    # [1, 2, 3, 1, 2, 3]  — el array completo se repite
np.repeat(a, 2)  # [1, 1, 2, 2, 3, 3]  — cada elemento se repite
```

## Notas relacionadas

- [[np.tile]]
- [[np.repeat]]
- [[np.roll]]
