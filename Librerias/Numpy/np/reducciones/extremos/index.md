---
title: np/reducciones/extremos — minimo, maximo y posicion
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/extremos — minimo, maximo y posicion

Las 5 funciones de esta subcarpeta localizan los valores extremos de un array. La distincion central: `min`/`max` devuelven el **valor** del extremo; `argmin`/`argmax` devuelven el **indice** (la posicion) donde se encuentra ese valor. `ptp` calcula el rango completo como una sola operacion.

```python
import numpy as np
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])

np.min(a)     # 1  — valor minimo
np.argmin(a)  # 1  — indice del minimo (primera ocurrencia)

np.max(a)     # 9
np.argmax(a)  # 5  — indice del maximo

np.ptp(a)     # 8  — rango: 9 - 1
```

Con arrays 2-D, `axis` cambia el significado del resultado: `axis=0` busca el extremo entre filas (resultado por columna); `axis=1` busca el extremo entre columnas (resultado por fila).

```python
M = np.array([[3, 1],
              [4, 2]])

np.argmin(M, axis=0)  # [0, 0] — fila donde esta el minimo de cada columna
np.argmin(M, axis=1)  # [1, 1] — columna donde esta el minimo de cada fila
```

Sin `axis`, `argmin`/`argmax` devuelven el indice plano sobre el array aplanado. Para recuperar el valor: `a.flat[np.argmin(a)]`.

## Notas de esta subcarpeta

| Funcion | Que devuelve |
|---|---|
| [[np.min]] | Valor del elemento minimo. Equivalente a `a.min()`. |
| [[np.max]] | Valor del elemento maximo. Equivalente a `a.max()`. |
| [[np.argmin]] | Indice del elemento minimo. Sin `axis` es el indice plano; con `axis` es el indice a lo largo del eje indicado. |
| [[np.argmax]] | Indice del elemento maximo. Mismo comportamiento que `argmin`. |
| [[np.ptp]] | Rango peak-to-peak: `max - min`. Util para normalizar al intervalo [0,1] con `(a - a.min()) / a.ptp()`. Deprecada en versiones recientes de NumPy. |

> [!tip] Datos con NaN
> Si el array puede contener NaN, usa [[np.nanmin]], [[np.nanmax]], [[np.nanargmin]] y [[np.nanargmax]] de [[Librerias/Numpy/np/reducciones/nan_safe/index|nan_safe/]].
