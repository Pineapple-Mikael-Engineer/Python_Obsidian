---
title: np/reducciones/nan_safe — variantes nan* que ignoran NaN
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/nan_safe — variantes nan* que ignoran NaN

Las 12 funciones de esta subcarpeta son equivalentes a sus contrapartes normales pero con `skipnan=True` implicito: detectan y excluyen los NaN antes de calcular. Tienen un coste adicional respecto a la version base (un recorrido extra para localizar los NaN), pero evitan que un solo NaN contamine todo el resultado.

## Tabla normal vs nan-safe

| Funcion normal | Variante nan-safe | Categoria |
|---|---|---|
| [[np.sum]] | [[np.nansum]] | agregacion |
| [[np.prod]] | [[np.nanprod]] | agregacion |
| [[np.cumsum]] | [[np.nancumsum]] | agregacion |
| [[np.cumprod]] | [[np.nancumprod]] | agregacion |
| [[np.mean]] | [[np.nanmean]] | promedios |
| [[np.median]] | [[np.nanmedian]] | promedios |
| [[np.std]] | [[np.nanstd]] | promedios |
| [[np.var]] | [[np.nanvar]] | promedios |
| [[np.min]] | [[np.nanmin]] | extremos |
| [[np.max]] | [[np.nanmax]] | extremos |
| [[np.argmin]] | [[np.nanargmin]] | extremos |
| [[np.argmax]] | [[np.nanargmax]] | extremos |

## Comportamiento clave

```python
import numpy as np
a = np.array([1.0, 2.0, np.nan, 4.0])

np.sum(a)     # nan    — un NaN contamina el resultado
np.nansum(a)  # 7.0    — ignora el NaN

np.mean(a)    # nan
np.nanmean(a) # 2.333...
```

> [!warning] Si todos los elementos son NaN
> `np.nanmin`, `np.nanmax`, `np.nanargmin` y `np.nanargmax` lanzan `ValueError` si el slice esta compuesto enteramente por NaN. Las variantes de suma/promedio devuelven 0 o NaN segun la funcion.
