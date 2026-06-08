---
title: uniformes — distribucion uniforme y sus alias
tags:
  - numpy
  - indice
draft: false
---

# uniformes — distribucion uniforme y sus alias

La distribucion uniforme es el punto de partida de toda aleatoriedad numerica: todos los valores en un rango son igualmente probables. NumPy tiene 6 funciones para esto, aunque 4 de ellas son aliases identicos — una decision de diseño historica confusa que sobrevive por compatibilidad. La diferencia practica entre las funciones que no son alias esta en la interfaz de `size` y en si el rango es fijo `[0, 1)` o configurable.

## Funciones

| Funcion | Rango | Interfaz de shape | Descripcion |
|---------|-------|-------------------|-------------|
| [[np.random.rand]] | `[0, 1)` | argumentos posicionales `rand(3, 4)` | Uniforme estandar con shape como args; interfaz estilo MATLAB |
| [[np.random.random]] | `[0, 1)` | tupla `random((3, 4))` | Interfaz Pythonica; forma preferida sobre `rand` |
| [[np.random.random_sample]] | `[0, 1)` | tupla | Alias exacto de `random` |
| [[np.random.ranf]] | `[0, 1)` | tupla | Alias exacto de `random`; existe por compatibilidad historica |
| [[np.random.sample]] | `[0, 1)` | tupla | Alias exacto de `random`; cuatro nombres para la misma funcion |
| [[np.random.uniform]] | `[low, high)` | tupla o entero | Rango arbitrario con parametros explicitos; semanticamente la mas clara |

## Alias: random = random_sample = ranf = sample

Las cuatro funciones son identicas en comportamiento. Se recomienda usar `np.random.random` por ser la mas legible. `rand` queda para codigo que privilegia la brevedad; `uniform` cuando el rango importa y conviene hacerlo explicito.

```python
import numpy as np
np.random.seed(0)

np.random.rand(3)             # array([0.549, 0.715, 0.603]) — shape como args
np.random.random((3,))        # misma distribucion, interfaz de tupla
np.random.uniform(0, 1, 3)   # identico en resultado, con rango explicito

# Uniforme en rango arbitrario
np.random.uniform(low=-5, high=5, size=(2, 3))
```
