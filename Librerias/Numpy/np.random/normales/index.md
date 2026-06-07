---
title: normales — distribuciones normales / gaussianas
tags:
  - numpy
  - indice
draft: false
---

# normales — distribuciones normales / gaussianas

La distribucion normal (gaussiana) es la mas importante en estadistica: aparece en errores de medida, fenomenos naturales, y es el resultado del teorema central del limite — la suma de muchas variables independientes converge a una normal sin importar su distribucion de origen. NumPy tiene tres funciones que generan la misma distribucion con interfaces diferentes; la eleccion es cuestion de legibilidad y consistencia.

## Funciones

| Funcion | Distribucion | Interfaz de shape | Descripcion |
|---------|--------------|-------------------|-------------|
| [[np.random.randn]] | N(0, 1) | argumentos posicionales `randn(3, 4)` | Normal estandar; interfaz estilo MATLAB |
| [[np.random.standard_normal]] | N(0, 1) | tupla `standard_normal((3, 4))` | Normal estandar con interfaz Pythonica |
| [[np.random.normal]] | N(loc, scale) | tupla o entero | Media y desviacion estandar especificadas directamente |

Para obtener N(mu, sigma) desde `randn`: `mu + sigma * np.random.randn(n)`. `normal` evita esa transformacion manual y hace los parametros explicitos en el codigo.

## Regla de eleccion

- Para N(0, 1) rapido y conciso → `randn`.
- Para N(0, 1) con interfaz de tupla consistente con el resto de `np.random` → `standard_normal`.
- Cuando se conocen media (`loc`) y desviacion (`scale`) y conviene hacerlos expliciots → `normal`.

```python
import numpy as np
np.random.seed(0)

np.random.randn(3, 4)                          # N(0,1), shape (3,4)
np.random.standard_normal((3, 4))              # idem, interfaz tupla

np.random.normal(loc=5, scale=2, size=(3, 4)) # N(5, 2)

# Equivalencia: las dos lineas producen la misma distribucion
np.random.normal(loc=50, scale=5, size=1000)
50 + 5 * np.random.randn(1000)
```
