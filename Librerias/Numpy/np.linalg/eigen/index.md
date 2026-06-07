---
title: np.linalg — autovalores y autovectores
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — autovalores y autovectores

Cuatro variantes segun la necesidad: si se necesitan solo autovalores o tambien autovectores, y si la matriz es general o simetrica/hermitiana.

## Funciones

| Funcion | Autovalores | Autovectores | Tipo de matriz |
|---|---|---|---|
| [[np.linalg.eig]] | Si | Si | General (cualquier cuadrada) |
| [[np.linalg.eigvals]] | Si | No | General (mas rapido sin vectores) |
| [[np.linalg.eigh]] | Si | Si | Simetrica / hermitiana |
| [[np.linalg.eigvalsh]] | Si | No | Simetrica / hermitiana |

## Regla de decision

```
¿La matriz es simetrica o hermitiana?
  Si  → eigh (con vectores) o eigvalsh (sin vectores)
  No  → eig  (con vectores) o eigvals  (sin vectores)
```

Preferir `eigh`/`eigvalsh` para matrices simetricas: garantizan autovalores **reales** y son mas rapidos y numericamente mas estables que sus equivalentes generales.

## Cuando usar cada variante

| Necesito... | Funcion |
|---|---|
| Autovalores + autovectores, matriz general | [[np.linalg.eig]] |
| Solo autovalores, matriz general | [[np.linalg.eigvals]] |
| Autovalores + autovectores, matriz de covarianza / simetrica | [[np.linalg.eigh]] |
| Solo autovalores, matriz simetrica (PCA, vibraciones) | [[np.linalg.eigvalsh]] |

## Nota sobre matrices simetricas

`eigh` y `eigvalsh` solo leen la mitad triangular de la matriz (inferior por defecto, controlado con `UPLO`). Los autovalores devueltos estan **ordenados de menor a mayor**, lo cual es conveniente para analisis espectral.
