---
title: np/reducciones/extremos — minimo, maximo y posicion
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/extremos — minimo, maximo y posicion

Las 5 funciones de esta subcarpeta localizan los valores extremos de un array y, opcionalmente, sus indices. Todas aceptan `axis=`.

## Notas de esta subcarpeta

| Funcion | Que devuelve |
|---|---|
| [[np.min]] | Valor del elemento minimo |
| [[np.max]] | Valor del elemento maximo |
| [[np.argmin]] | Indice plano (o a lo largo del eje) del elemento minimo |
| [[np.argmax]] | Indice plano (o a lo largo del eje) del elemento maximo |
| [[np.ptp]] | Rango = max - min (peak to peak) |

## Valor vs indice

```python
import numpy as np
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])

np.min(a)     # 1   — valor minimo
np.argmin(a)  # 1   — posicion del minimo (indice 1)

np.max(a)     # 9
np.argmax(a)  # 5   — posicion del maximo (indice 5)

np.ptp(a)     # 8   — rango: 9 - 1
```

Con arrays 2-D:

```python
M = np.array([[3, 1],
              [4, 2]])

np.argmin(M, axis=0)  # [0, 0] — fila del minimo por columna
np.argmin(M, axis=1)  # [1, 1] — columna del minimo por fila
```

> [!tip] Datos con NaN
> Si el array puede contener NaN, usa [[np.nanmin]], [[np.nanmax]], [[np.nanargmin]] y [[np.nanargmax]] de [[Librerias/Numpy/np/reducciones/nan_safe/index|nan_safe/]].
