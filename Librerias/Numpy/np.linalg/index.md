---
title: np.linalg — algebra lineal
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — algebra lineal

`numpy.linalg` es el submodulo de algebra lineal de NumPy. Resuelve los problemas centrales del algebra lineal numerica: sistemas de ecuaciones, descomposicion de matrices, autovalores, normas e inversas. Internamente usa LAPACK (la biblioteca de referencia en Fortran para algebra lineal numerica), por lo que su rendimiento es comparable a MATLAB.

La diferencia con `scipy.linalg`: NumPy tiene el conjunto esencial; SciPy lo extiende (descomposicion LU, funciones de matrices, solucion de Sylvester, etc.). Para trabajo serio en algebra lineal numerica, SciPy es mas completo; NumPy es suficiente para la mayoria de casos en ciencia de datos y machine learning.

## Subcarpetas

| Subcarpeta | Funciones | Que contiene |
|---|---|---|
| [[Librerias/Numpy/np.linalg/normas_condiciones/index\|normas_condiciones/]] | 3 | norm, cond, matrix_rank |
| [[Librerias/Numpy/np.linalg/determinantes/index\|determinantes/]] | 2 | det, slogdet |
| [[Librerias/Numpy/np.linalg/inversas/index\|inversas/]] | 2 | inv, pinv |
| [[Librerias/Numpy/np.linalg/eigen/index\|eigen/]] | 4 | eig, eigvals, eigh, eigvalsh |
| [[Librerias/Numpy/np.linalg/descomposiciones/index\|descomposiciones/]] | 4 | svd, qr, cholesky, (lu → scipy) |
| [[Librerias/Numpy/np.linalg/sistemas_ecuaciones/index\|sistemas_ecuaciones/]] | 3 | solve, tensorsolve, lstsq |
| [[Librerias/Numpy/np.linalg/productos/index\|productos/]] | 4 | dot, multi_dot, matrix_power, matrix_transpose |

## Tabla de decision por caso de uso

| Necesito... | Funcion |
|---|---|
| Resolver `Ax = b` (sistema cuadrado) | [[np.linalg.solve]] |
| Resolver sistema sobredeterminado | [[np.linalg.lstsq]] |
| Autovalores de matriz general | [[np.linalg.eig]] / [[np.linalg.eigvals]] |
| Autovalores de matriz simetrica | [[np.linalg.eigh]] / [[np.linalg.eigvalsh]] |
| Descomponer en valores singulares | [[np.linalg.svd]] |
| Factorizar A = QR | [[np.linalg.qr]] |
| Factorizar A = LL^T (positiva definida) | [[np.linalg.cholesky]] |
| Inversa de una matriz cuadrada | [[np.linalg.inv]] |
| Pseudoinversa (rectangular o singular) | [[np.linalg.pinv]] |
| Determinante | [[np.linalg.det]] / [[np.linalg.slogdet]] |
| Norma vectorial o matricial | [[np.linalg.norm]] |
| Numero de condicion | [[np.linalg.cond]] |
| Rango de la matriz | [[np.linalg.matrix_rank]] |
| Producto matricial multiple | [[np.linalg.multi_dot]] |
| Potencia de una matriz | [[np.linalg.matrix_power]] |

## NumPy vs scipy.linalg

`np.linalg` cubre el conjunto basico de algebra lineal. `scipy.linalg` lo extiende con:

- Factorizacion LU (`scipy.linalg.lu`) — no existe en `np.linalg`
- Funciones de matrices especiales: `expm`, `logm`, `sqrtm`
- Solucionadores mas especializados (banda, triangular, simetrico)
- Descomposicion de Schur, funciones de Lyapunov, etc.

Regla practica: si `np.linalg` tiene la funcion, usarla; solo migrar a `scipy.linalg` cuando se necesite algo que NumPy no ofrece.
