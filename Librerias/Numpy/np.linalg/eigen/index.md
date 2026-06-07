---
title: np.linalg — autovalores y autovectores
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — autovalores y autovectores

Los autovalores y autovectores de una matriz A son los escalares λ y vectores v tales que Av = λv: A "estira" v por un factor λ sin cambiar su direccion. Son fundamentales en PCA, analisis de estabilidad, vibraciones mecanicas, algoritmos de grafos (PageRank) y cualquier problema donde la dinamica de un sistema se describe por una matriz.

NumPy ofrece 4 variantes segun si la matriz es general o simetrica, y si se necesitan solo autovalores o tambien autovectores.

## Funciones

| Funcion | Autovalores | Autovectores | Tipo de matriz |
|---|---|---|---|
| [[np.linalg.eig]] | Si | Si | General (cualquier cuadrada) |
| [[np.linalg.eigvals]] | Si | No | General (mas rapido sin vectores) |
| [[np.linalg.eigh]] | Si | Si | Simetrica / hermitiana |
| [[np.linalg.eigvalsh]] | Si | No | Simetrica / hermitiana |

## Descripcion de cada funcion

**`np.linalg.eig(a)`** — autovalores y autovectores para matrices cuadradas generales. Los autovalores pueden ser complejos incluso para matrices reales. Los autovectores estan en las columnas de la matriz devuelta (no en las filas).

**`np.linalg.eigvals(a)`** — solo autovalores (sin autovectores). Mas rapido cuando no se necesitan los vectores.

**`np.linalg.eigh(a)`** — autovalores y autovectores para matrices simetricas reales o hermitanas complejas. Garantiza autovalores reales y autovectores ortonormales. Numericamente mas estable y rapido que `eig` para estas matrices. Los autovalores se devuelven en orden ascendente.

**`np.linalg.eigvalsh(a)`** — solo autovalores de matrices simetricas/hermitanas. La opcion mas rapida cuando la matriz es simetrica y solo se necesitan los valores.

## Regla de decision

```
¿La matriz es simetrica o hermitiana?
  Si  → eigh (con vectores) o eigvalsh (sin vectores)
  No  → eig  (con vectores) o eigvals  (sin vectores)
```

| Necesito... | Funcion |
|---|---|
| Autovalores + autovectores, matriz general | [[np.linalg.eig]] |
| Solo autovalores, matriz general | [[np.linalg.eigvals]] |
| Autovalores + autovectores, matriz de covarianza / simetrica | [[np.linalg.eigh]] |
| Solo autovalores, matriz simetrica (PCA, vibraciones) | [[np.linalg.eigvalsh]] |

Regla practica: si la matriz es de covarianza, de correlacion, o cualquier A^T A, usar `eigh`/`eigvalsh`.

## Nota sobre matrices simetricas

`eigh` y `eigvalsh` solo leen la mitad triangular de la matriz (inferior por defecto, controlado con `UPLO`). Los autovalores devueltos estan ordenados de menor a mayor, lo cual es conveniente para analisis espectral.
