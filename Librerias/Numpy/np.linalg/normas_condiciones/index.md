---
title: np.linalg — normas y condiciones
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — normas y condiciones

Antes de resolver un sistema lineal, conviene entender si la matriz es "bien condicionada" (solucion estable frente a perturbaciones) o "mal condicionada" (pequenos errores en los datos causan grandes errores en la solucion). Este directorio agrupa las funciones que miden esas propiedades.

## Funciones

| Funcion | Que calcula | Caso tipico |
|---|---|---|
| [[np.linalg.norm]] | Norma vectorial o matricial (Frobenius, inf, L-p) | Magnitud de vectores, distancias, error residual |
| [[np.linalg.cond]] | Numero de condicion (estabilidad numerica) | Diagnosticar si un sistema es mal condicionado |
| [[np.linalg.matrix_rank]] | Rango de la matriz | Detectar dependencia lineal, dimension del espacio |

## Descripcion de cada funcion

**`np.linalg.norm(x, ord, axis)`** — norma de un vector o matriz. Para vectores: norm-1 (suma de abs), norm-2 (norma euclidea, la por defecto), norm-inf (maximo de abs). Para matrices: norma de Frobenius (por defecto), norma espectral (mayor valor singular). Es la funcion de medida de "tamano" de NumPy.

**`np.linalg.cond(x, p)`** — numero de condicion de la matriz: ratio entre el mayor y el menor valor singular. Un numero de condicion de 1 es perfecto; 1e12 indica que se pierden ~12 digitos de precision al resolver el sistema. Regla practica: si `cond(A) > 1/eps` (donde eps es la precision de maquina), el sistema es numericamente singular.

**`np.linalg.matrix_rank(M, tol)`** — rango de la matriz: numero de valores singulares por encima de una tolerancia. El rango dice cuantas ecuaciones son "realmente independientes" en el sistema.

## Notas de uso

- **`norm`**: acepta vectores y matrices; el parametro `ord` controla el tipo de norma (`None` → Frobenius para matrices, L2 para vectores).
- **`cond`**: valores cercanos a 1 indican sistema bien condicionado; valores muy grandes (> 1e12) indican que la solucion puede ser numericamente inestable.
- **`matrix_rank`**: usa SVD internamente; el umbral de tolerancia `tol` puede ajustarse para matrices con ruido.

## Relacion con otras subcarpetas

Un numero de condicion alto (`cond`) es senal de que `solve` puede dar resultados poco fiables — en ese caso considerar `lstsq` o preprocesar la matriz.
