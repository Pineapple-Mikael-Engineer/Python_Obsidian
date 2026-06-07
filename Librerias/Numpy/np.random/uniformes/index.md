---
title: uniformes — distribucion uniforme y sus alias
tags:
  - numpy
  - indice
draft: false
---

# uniformes — distribucion uniforme y sus alias

Funciones para generar muestras con distribucion uniforme. La mayoria son alias entre si; la diferencia principal esta en la interfaz de `size` y el rango de salida.

## Funciones

| Funcion | Rango | Interfaz de shape | Descripcion |
|---------|-------|-------------------|-------------|
| [[np.random.rand]] | `[0, 1)` | argumentos posicionales `rand(3, 4)` | Uniforme estandar con shape como args |
| [[np.random.random]] | `[0, 1)` | tupla `random((3, 4))` | Interfaz mas clara; alias de random_sample |
| [[np.random.random_sample]] | `[0, 1)` | tupla | Alias de `random` |
| [[np.random.ranf]] | `[0, 1)` | tupla | Alias de `random` |
| [[np.random.sample]] | `[0, 1)` | tupla | Alias de `random` |
| [[np.random.uniform]] | `[low, high)` | tupla o entero | Rango arbitrario con parametros explicitos |

## Alias: random = random_sample = ranf = sample

Las cuatro funciones son identicas en comportamiento. Se recomienda usar `np.random.random` por ser la mas legible.

```python
import numpy as np
np.random.seed(0)

np.random.rand(3)            # array([0.549, 0.715, 0.603])
np.random.random((3,))       # misma distribucion, interfaz de tupla
np.random.uniform(0, 1, 3)  # identico en resultado, con rango explicito
```

## Rango arbitrario con uniform

```python
# Uniforme en [-5, 5)
np.random.uniform(low=-5, high=5, size=(2, 3))
```
