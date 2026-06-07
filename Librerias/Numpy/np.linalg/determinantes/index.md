---
title: np.linalg — determinantes
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — determinantes

Funciones para calcular el determinante de una matriz cuadrada. La eleccion entre las dos depende del tamano de la matriz y de la precision numerica requerida.

## Funciones

| Funcion | Que calcula | Limitacion |
|---|---|---|
| [[np.linalg.det]] | Determinante directo (valor escalar) | Puede sufrir overflow/underflow en matrices grandes |
| [[np.linalg.slogdet]] | Signo + logaritmo del determinante | Numericamente estable para cualquier tamano |

## Cuando usar cada una

| Situacion | Funcion recomendada |
|---|---|
| Matrices pequenas (< 10×10), valor exacto necesario | [[np.linalg.det]] |
| Matrices grandes o valores extremadamente pequenos/grandes | [[np.linalg.slogdet]] |
| Calculos de probabilidad (log-verosimilitud, log-det de covarianzas) | [[np.linalg.slogdet]] |
| Solo necesito saber si det ≠ 0 (invertibilidad) | [[np.linalg.det]] o `matrix_rank` |

## Relacion entre ambas

`slogdet` devuelve `(sign, logabsdet)` tal que `det = sign * exp(logabsdet)`. Usar `det` es equivalente a `np.exp(logabsdet) * sign`, pero `slogdet` evita el desbordamiento numerico intermedio.

```python
import numpy as np
A = np.array([[1., 2.], [3., 4.]])

np.linalg.det(A)           # -2.0
sign, logdet = np.linalg.slogdet(A)
sign * np.exp(logdet)      # -2.0  (mismo resultado, ruta estable)
```
