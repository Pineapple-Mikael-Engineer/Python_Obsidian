---
title: np.linalg — sistemas de ecuaciones
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — sistemas de ecuaciones

Resolver Ax = b es el problema fundamental del algebra lineal aplicada. Las tres funciones de este directorio cubren los tres casos principales: sistema cuadrado exacto, sistema tensorial, y sistema sobredeterminado (minimos cuadrados).

## Funciones

| Funcion | Sistema que resuelve | Requisito de A |
|---|---|---|
| [[np.linalg.solve]] | Exacto: `Ax = b` | Cuadrada (M×M) y no singular |
| [[np.linalg.tensorsolve]] | Tensorial: `A x = b` con indices multiples | Forma compatible para contraccion tensorial |
| [[np.linalg.lstsq]] | Minimos cuadrados: `min \|\|Ax - b\|\|` | Cualquier forma (M×N), incluido sobredeterminado |

## Descripcion de cada funcion

**`np.linalg.solve(a, b)`** — resuelve Ax = b cuando A es cuadrada y no singular. Usa factorizacion LU internamente. Es mas rapido y numericamente mas estable que `inv(A) @ b`. Acepta multiples vectores `b` simultaneamente (b puede ser una matriz).

**`np.linalg.lstsq(a, b, rcond)`** — resuelve Ax ≈ b en el sentido de minimos cuadrados: encuentra x que minimiza ||Ax - b||. Funciona con sistemas sobredeterminados (mas ecuaciones que incognitas) y subdeterminados. Usa SVD internamente. Devuelve (solucion, residuales, rango, valores singulares).

**`np.linalg.tensorsolve(a, b, axes)`** — generaliza `solve` a tensores de orden superior: resuelve la ecuacion tensorial sum_j A[...,j] x[j] = b. Para la mayoria de casos `solve` es suficiente.

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
