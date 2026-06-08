---
title: np.linalg — descomposiciones matriciales
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — descomposiciones matriciales

Factorizar una matriz en el producto de matrices con propiedades especiales permite resolver sistemas de forma mas eficiente, analizar los datos que contiene (SVD para PCA), o verificar propiedades (Cholesky solo funciona en matrices positivas definidas). Las descomposiciones son el nucleo del algebra lineal numerica moderna.

## Funciones

| Funcion | Factorizacion | Requisito de la matriz |
|---|---|---|
| [[np.linalg.svd]] | A = U Σ V^T (valores singulares) | Cualquier forma (M×N) |
| [[np.linalg.qr]] | A = QR | Cualquier forma (M×N) |
| [[np.linalg.cholesky]] | A = LL^T | Cuadrada, simetrica y positiva definida |
| `scipy.linalg.lu` | A = PLU | Cuadrada — **no existe en np.linalg** |

> [!warning] np.linalg.lu no existe
> La factorizacion LU no esta en NumPy. Usar `scipy.linalg.lu` o `scipy.linalg.lu_factor` + `scipy.linalg.lu_solve`.

## Descripcion de cada funcion

**`np.linalg.svd(a, full_matrices)`** — Descomposicion en Valores Singulares: A = U S V^T. U y V son matrices ortonormales; S contiene los valores singulares en orden descendente. Es la factorizacion mas general y numericamente estable. Base de PCA, compresion de imagenes, regresion ridge y muchos algoritmos de ML.

**`np.linalg.qr(a, mode)`** — Descomposicion QR: A = Q R donde Q es ortogonal y R es triangular superior. Util para resolver sistemas sobredeterminados (minimos cuadrados) y para el algoritmo QR de calculo de autovalores. El parametro `mode='reduced'` da la forma compacta.

**`np.linalg.cholesky(a)`** — Descomposicion de Cholesky: A = L L^T donde L es triangular inferior. Solo funciona si A es simetrica positiva definida (todas las matrices de covarianza bien condicionadas). Es el doble de rapido que LU para este tipo de matrices. Util en simulacion de variables gaussianas correlacionadas.

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
