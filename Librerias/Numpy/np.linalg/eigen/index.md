---
title: np.linalg — autovalores y autovectores
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — autovalores y autovectores

Los **autovalores** $\lambda$ y **autovectores** $\mathbf{v}$ de una matriz $A$ son los escalares y
vectores no nulos que cumplen la ecuación central:

$$
A\,\mathbf{v} = \lambda\,\mathbf{v}
$$

$A$ solo **estira** a $\mathbf{v}$ por un factor $\lambda$ sin cambiar su dirección. Son la base del
PCA, el análisis de estabilidad de sistemas lineales, las vibraciones mecánicas (modos y frecuencias
propias), los algoritmos de grafos (PageRank) y, en general, de cualquier problema cuya dinámica se
describe con una matriz. Apilando los autovectores como **columnas** de $V$ y los autovalores en una
diagonal $\Lambda$, la ecuación se vuelve la diagonalización $A = V\,\Lambda\,V^{-1}$.

NumPy ofrece **cuatro** variantes según dos ejes de decisión: si la matriz es **general** o
**simétrica/Hermítica**, y si necesitas **solo los autovalores** o **también los autovectores**.

## Las cuatro funciones

| Función | Matriz | Devuelve |
|---|---|---|
| [[np.linalg.eig]] | general (cualquier cuadrada) | autovalores **y** autovectores |
| [[np.linalg.eigvals]] | general | solo autovalores |
| [[np.linalg.eigh]] | simétrica / Hermítica | autovalores **y** autovectores |
| [[np.linalg.eigvalsh]] | simétrica / Hermítica | solo autovalores |

Las que llevan **vectores** ([[np.linalg.eig]], [[np.linalg.eigh]]) devuelven un namedtuple
`(autovalores, autovectores)` con campos `eigenvalues` / `eigenvectors`; los autovectores son las
**columnas** de la matriz `v` (`v[:, i]` es el autovector de `w[i]`). Las que **no** llevan vectores
devuelven un solo `ndarray` de autovalores.

## Cuándo usar cada una: simétrica → `eigh` siempre

```text
¿La matriz es simétrica o Hermítica?
  Sí  → eigh      (con vectores)   /  eigvalsh  (solo valores)
  No  → eig       (con vectores)   /  eigvals   (solo valores)
```

| Necesito… | Función |
|---|---|
| autovalores + autovectores, matriz general | [[np.linalg.eig]] |
| solo autovalores, matriz general | [[np.linalg.eigvals]] |
| autovalores + autovectores, matriz simétrica (covarianza, PCA) | [[np.linalg.eigh]] |
| solo autovalores, matriz simétrica | [[np.linalg.eigvalsh]] |

**Regla práctica:** si la matriz es de covarianza, de correlación, de Gram o cualquier
$A^{\mathsf{T}}A$, es simétrica → usa **siempre** la familia `eigh`/`eigvalsh`. Frente a `eig`/`eigvals`,
la variante simétrica es **más rápida y estable**, devuelve autovalores **reales** (nunca complejos
espurios) y en **orden ascendente**, y autovectores **ortonormales**. La familia general `eig`/`eigvals`
no ordena y puede devolver autovalores **complejos** aunque la matriz sea real.

## Nota sobre `UPLO` y el lote N-D

`eigh` y `eigvalsh` solo leen la **mitad triangular** de la matriz (`UPLO='L'` inferior por defecto,
`'U'` superior); el otro triángulo se ignora asumiendo simetría. Las cuatro funciones operan sobre los
**dos últimos ejes** `(n, n)` y tratan los ejes anteriores como un **lote**: con shape `(..., n, n)`
descomponen todas las matrices del lote de una sola llamada (ver [[concepto_shape]]).
