---
title: np/reducciones/diferencial — calculo numerico discreto
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/diferencial — calculo numerico discreto

Las 3 funciones de esta subcarpeta implementan operaciones de calculo diferencial e integral sobre datos discretos (arrays). Son utiles cuando se tiene una senal muestreada o una tabla de valores y se quiere estimar derivadas o integrales.

## Notas de esta subcarpeta

| Funcion | Que hace |
|---|---|
| [[np.diff]] | Diferencias finitas hacia adelante: `a[i+1] - a[i]`. Aproxima la derivada discreta. Reduce la longitud del array en 1. |
| [[np.gradient]] | Gradiente numerico con diferencias centradas. Estima la derivada en cada punto; la salida tiene el **mismo shape** que la entrada. |
| [[np.trapz]] | Integracion numerica por la regla del trapecio. Devuelve un escalar (o array si `axis=` en 2-D). |

## Ejemplo rapido

```python
import numpy as np
x = np.array([0.0, 1.0, 2.0, 3.0])
y = x**2          # funcion y = x^2; derivada = 2x

# Diferencias finitas (aproximacion cruda de la derivada)
np.diff(y)        # [1., 3., 5.]  — longitud n-1

# Gradiente numerico (derivada en cada punto)
np.gradient(y, x) # [1., 2., 4., 6.] — mismo shape, usa dif. centradas

# Integral de y sobre x (debe ser ~ x^3/3 = 9)
np.trapz(y, x)    # 9.0
```

> [!note] diff vs gradient
> [[np.diff]] es mas simple y rapido pero acorta el array; [[np.gradient]] conserva el shape y usa diferencias centradas (mas preciso en el interior).
