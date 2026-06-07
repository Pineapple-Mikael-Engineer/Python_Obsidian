---
title: np.linalg — descomposiciones matriciales
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — descomposiciones matriciales

Factorizaciones que expresan una matriz como producto de matrices con propiedades especiales. Cada una esta optimizada para un tipo de problema distinto.

## Funciones

| Funcion | Factorizacion | Requisito de la matriz |
|---|---|---|
| [[np.linalg.svd]] | A = U Σ V^T (valores singulares) | Cualquier forma (M×N) |
| [[np.linalg.qr]] | A = QR | Cualquier forma (M×N) |
| [[np.linalg.cholesky]] | A = LL^T | Cuadrada, simetrica y positiva definida |
| `scipy.linalg.lu` | A = PLU | Cuadrada — **no existe en np.linalg** |

> [!warning] np.linalg.lu no existe
> La factorizacion LU **no esta en NumPy**. Usar `scipy.linalg.lu` o `scipy.linalg.lu_factor` + `scipy.linalg.lu_solve`.

## Cuando usar cada una

| Aplicacion | Descomposicion recomendada |
|---|---|
| Analisis de datos, PCA, reduccion de dimension | [[np.linalg.svd]] |
| Sistemas sobredeterminados (minimos cuadrados) | [[np.linalg.qr]] |
| Matrices de covarianza, simulacion de multivariada normal | [[np.linalg.cholesky]] |
| Resolver sistemas cuadrados eficientemente (alternativa a solve) | `scipy.linalg.lu` |
| Pseudoinversa numericamente estable | [[np.linalg.svd]] (base de `pinv`) |

## Notas rapidas

- **SVD**: la mas universal; `full_matrices=False` da la forma economica (recomendada para matrices grandes).
- **QR**: `Q` es ortogonal, `R` es triangular superior; util para sistemas de ecuaciones con estructura rectangular.
- **Cholesky**: la factorizacion mas rapida cuando aplica; falla con `LinAlgError` si la matriz no es positiva definida.
