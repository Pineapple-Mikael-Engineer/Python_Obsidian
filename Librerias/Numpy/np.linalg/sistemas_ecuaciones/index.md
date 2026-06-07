---
title: np.linalg — sistemas de ecuaciones
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — sistemas de ecuaciones

Funciones para resolver `Ax = b`. La eleccion depende de la forma de `A` y de si el sistema tiene solucion exacta o aproximada.

## Funciones

| Funcion | Sistema que resuelve | Requisito de A |
|---|---|---|
| [[np.linalg.solve]] | Exacto: `Ax = b` | Cuadrada (M×M) y no singular |
| [[np.linalg.tensorsolve]] | Tensorial: `A x = b` con indices multiples | Forma compatible para contraccion tensorial |
| [[np.linalg.lstsq]] | Minimos cuadrados: `min \|\|Ax - b\|\|` | Cualquier forma (M×N), incluido sobredeterminado |

## Regla de decision

```
¿A es cuadrada y no singular?
  Si  → solve (mas rapido, solucion exacta)
  No  → lstsq (minimos cuadrados, tolera sobredeterminado/subdeterminado)
¿Trabajo con tensores de orden superior?
  Si  → tensorsolve
```

| Caso | Funcion |
|---|---|
| Sistema cuadrado `Ax = b`, A invertible | [[np.linalg.solve]] |
| Sistema sobredeterminado (mas ecuaciones que incognitas) | [[np.linalg.lstsq]] |
| Sistema subdeterminado (mas incognitas que ecuaciones) | [[np.linalg.lstsq]] |
| A singular o casi singular | [[np.linalg.lstsq]] |
| Ecuacion tensorial `A[i,j,k,l] x[k,l] = b[i,j]` | [[np.linalg.tensorsolve]] |

## Buenas practicas

- Nunca usar `inv(A) @ b` para resolver sistemas: `solve` es mas rapido y estable.
- `lstsq` devuelve ademas el rango efectivo y los valores singulares, utiles para diagnostico.
- Para multiples terminos independientes con la misma `A`, pasar todos en `b` como columnas: una sola factorizacion para todos.
