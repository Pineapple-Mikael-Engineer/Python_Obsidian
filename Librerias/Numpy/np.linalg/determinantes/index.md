---
title: np.linalg — determinantes
tags:
  - numpy
  - indice
draft: false
---

# np.linalg — determinantes

El determinante es un escalar que caracteriza si una matriz cuadrada es invertible (det != 0) y como transforma volumenes. En la practica, el determinante directo rara vez se necesita; lo que se necesita es saber si el sistema tiene solucion unica, y para eso el rango es mas util.

## Funciones

| Funcion | Que calcula | Limitacion |
|---|---|---|
| [[np.linalg.det]] | Determinante directo (valor escalar) | Puede sufrir overflow/underflow en matrices grandes |
| [[np.linalg.slogdet]] | Signo + logaritmo del determinante | Numericamente estable para cualquier tamano |

## Descripcion de cada funcion

**`np.linalg.det(a)`** — determinante exacto. Para matrices grandes puede sufrir overflow o underflow porque el calculo implica productos de muchos numeros. Usar con precaucion para matrices de dimension > 20.

**`np.linalg.slogdet(a)`** — devuelve el signo y el logaritmo del valor absoluto del determinante: `(sign, logabsdet)`. Numericamente estable para matrices grandes porque trabaja en escala logaritmica. Para verificar si la matriz es singular: `sign == 0`.

## Cuando usar cada una

| Situacion | Funcion recomendada |
|---|---|
| Matrices pequenas (< 10x10), valor exacto necesario | [[np.linalg.det]] |
| Matrices grandes o valores extremadamente pequenos/grandes | [[np.linalg.slogdet]] |
| Calculos de probabilidad (log-verosimilitud, log-det de covarianzas) | [[np.linalg.slogdet]] |
| Solo necesito saber si det != 0 (invertibilidad) | [[np.linalg.det]] o `matrix_rank` |

## Relacion entre ambas

`slogdet` devuelve `(sign, logabsdet)` tal que `det = sign * exp(logabsdet)`. Usar `det` es equivalente a `np.exp(logabsdet) * sign`, pero `slogdet` evita el desbordamiento numerico intermedio.

```python
import numpy as np
A = np.array([[1., 2.], [3., 4.]])

np.linalg.det(A)           # -2.0
sign, logdet = np.linalg.slogdet(A)
sign * np.exp(logdet)      # -2.0  (mismo resultado, ruta estable)
```
