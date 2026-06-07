---
title: normales — distribuciones normales / gaussianas
tags:
  - numpy
  - indice
draft: false
---

# normales — distribuciones normales / gaussianas

Tres funciones para muestrear distribuciones normales. Difieren en interfaz y flexibilidad; la distribucion subyacente es siempre gaussiana.

## Funciones

| Funcion | Distribucion | Interfaz de shape | Descripcion |
|---------|--------------|-------------------|-------------|
| [[np.random.randn]] | N(0, 1) | argumentos posicionales `randn(3, 4)` | Normal estandar rapida |
| [[np.random.standard_normal]] | N(0, 1) | tupla `standard_normal((3, 4))` | Normal estandar con interfaz de tupla |
| [[np.random.normal]] | N(loc, scale) | tupla o entero | Normal con media y desviacion arbitrarias |

## Regla de eleccion

- Para N(0, 1) rapido y conciso → `randn`.
- Para N(0, 1) con interfaz de tupla consistente → `standard_normal`.
- Para media (`loc`) y desviacion (`scale`) controlados → `normal`.

```python
import numpy as np
np.random.seed(0)

np.random.randn(3, 4)                      # N(0,1), shape (3,4)
np.random.standard_normal((3, 4))          # idem, interfaz tupla
np.random.normal(loc=5, scale=2, size=(3, 4))  # N(5, 4)

# Equivalencia: estas dos lineas producen la misma distribucion
np.random.normal(loc=50, scale=5, size=1000)
50 + 5 * np.random.randn(1000)
```
