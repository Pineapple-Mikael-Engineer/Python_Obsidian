---
title: np.linalg — inversas
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — inversas

Funciones para invertir matrices. La eleccion depende de si la matriz es cuadrada y no singular, o si puede ser rectangular o singular.

## Funciones

| Funcion | Que calcula | Requisito |
|---|---|---|
| [[np.linalg.inv]] | Inversa exacta A^-1 | Matriz cuadrada y no singular |
| [[np.linalg.pinv]] | Pseudoinversa de Moore-Penrose A^+ | Funciona con rectangulares y singulares |

## Regla de decision

```
¿La matriz es cuadrada y garantizadamente no singular?
  Si  → np.linalg.inv
  No  → np.linalg.pinv
```

| Caso | Funcion |
|---|---|
| Matriz cuadrada, det ≠ 0 | [[np.linalg.inv]] |
| Matriz rectangular (mas filas que columnas) | [[np.linalg.pinv]] |
| Matriz singular o casi singular | [[np.linalg.pinv]] |
| Resolver `Ax = b` (no solo invertir) | [[np.linalg.solve]] — preferido sobre `inv` |

## Advertencia

En la mayoria de los casos en que se calcula `inv(A) @ b`, es preferible usar directamente `solve(A, b)`: misma solucion pero mas rapido y numericamente mas estable (evita el calculo explicito de la inversa).
