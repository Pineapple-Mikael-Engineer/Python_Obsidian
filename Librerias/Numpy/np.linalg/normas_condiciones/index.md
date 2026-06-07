---
title: np.linalg — normas y condiciones
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — normas y condiciones

Funciones que miden **propiedades numericas** de matrices y vectores: su magnitud, su estabilidad numerica y su rango efectivo.

## Funciones

| Funcion | Que calcula | Caso tipico |
|---|---|---|
| [[np.linalg.norm]] | Norma vectorial o matricial (Frobenius, inf, L-p) | Magnitud de vectores, distancias, error residual |
| [[np.linalg.cond]] | Numero de condicion (estabilidad numerica) | Diagnosticar si un sistema es mal condicionado |
| [[np.linalg.matrix_rank]] | Rango de la matriz | Detectar dependencia lineal, dimension del espacio |

## Notas de uso

- **`norm`**: acepta vectores y matrices; el parametro `ord` controla el tipo de norma (`None` → Frobenius para matrices, L2 para vectores).
- **`cond`**: valores cercanos a 1 indican sistema bien condicionado; valores muy grandes (> 1e12) indican que la solucion puede ser numericamente inestable.
- **`matrix_rank`**: usa SVD internamente; el umbral de tolerancia `tol` puede ajustarse para matrices con ruido.

## Relacion con otras subcarpetas

Un numero de condicion alto (`cond`) es señal de que `solve` puede dar resultados poco fiables — en ese caso considerar `lstsq` o preprocesar la matriz.
