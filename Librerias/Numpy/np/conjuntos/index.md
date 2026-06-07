---
title: np/conjuntos — operaciones de conjuntos sobre arrays 1D
tags:
  - numpy
  - indice
draft: false
---

# np/conjuntos — operaciones de conjuntos sobre arrays 1D

`conjuntos/` agrupa las funciones que tratan arrays 1D como conjuntos matematicos. Las operaciones son las clasicas de teoria de conjuntos (union, interseccion, diferencia, diferencia simetrica) mas la obtencion de elementos unicos. A diferencia de los `set` de Python, estas funciones retornan `ndarray` ordenados y soportan tipos numericos de forma eficiente.

## Comparacion con sets de Python

| Operacion | Python nativo | NumPy |
|-----------|--------------|-------|
| Elementos unicos | `set(a)` | [[np.unique]] |
| Interseccion | `a & b` | [[np.intersect1d]] |
| Union | `a \| b` | [[np.union1d]] |
| Diferencia (a - b) | `a - b` | [[np.setdiff1d]] |
| Diferencia simetrica | `a ^ b` | [[np.setxor1d]] |
| Tipo de retorno | `set` (desordenado) | `ndarray` (ordenado) |
| Broadcasting | No | Si (sobre arrays) |

## Tabla de decision

| Necesito… | Funcion |
|-----------|---------|
| Elementos sin repeticion de un array | [[np.unique]] |
| Elementos que estan en ambos arrays | [[np.intersect1d]] |
| Todos los elementos de ambos arrays sin repetir | [[np.union1d]] |
| Elementos de A que no estan en B | [[np.setdiff1d]] |
| Elementos que estan en uno solo de los dos arrays | [[np.setxor1d]] |

## Ejemplo

```python
import numpy as np

a = np.array([1, 2, 2, 3, 4])
b = np.array([2, 3, 3, 5])

np.unique(a)            # [1, 2, 3, 4]
np.intersect1d(a, b)    # [2, 3]
np.union1d(a, b)        # [1, 2, 3, 4, 5]
np.setdiff1d(a, b)      # [1, 4]
np.setxor1d(a, b)       # [1, 4, 5]
```

> Todas las funciones trabajan sobre los valores unicos internamente, por lo que duplicados en la entrada no afectan el resultado de las operaciones de conjunto.

## Notas de la carpeta

- [[np.unique]] — elementos unicos ordenados (con opciones para indices e inverso)
- [[np.intersect1d]] — interseccion de dos arrays
- [[np.union1d]] — union de dos arrays
- [[np.setdiff1d]] — diferencia de conjuntos (elementos de a que no estan en b)
- [[np.setxor1d]] — diferencia simetrica (elementos en uno pero no en ambos)
