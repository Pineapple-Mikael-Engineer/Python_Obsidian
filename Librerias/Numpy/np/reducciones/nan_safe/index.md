---
title: np/reducciones/nan_safe — variantes nan* que ignoran NaN
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/nan_safe — variantes nan* que ignoran NaN

Las 12 funciones de esta subcarpeta son gemelas exactas de sus contrapartes normales, con una sola diferencia: ignoran los valores NaN en vez de propagarlos. Sin ellas, un solo NaN en el array contamina el resultado completo:

```python
import numpy as np
a = np.array([1.0, 2.0, np.nan, 4.0])

np.sum(a)     # nan  — un NaN contamina el resultado
np.nansum(a)  # 7.0  — el NaN se descarta, se suma el resto

np.mean(a)    # nan
np.nanmean(a) # 2.333...
```

El coste de usar estas variantes: internamente deben localizar y enmascarar los NaN antes de calcular, lo que implica un recorrido adicional sobre el array. Si se sabe con certeza que los datos no tienen NaN, usar las versiones normales es mas eficiente.

Caso extremo: si **todos** los elementos del eje son NaN, las variantes `nanmin`, `nanmax`, `nanargmin` y `nanargmax` lanzan `ValueError`. Las variantes de suma y promedio devuelven 0 o NaN segun la funcion.

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

> [!warning] Slice completamente NaN
> `np.nanmin`, `np.nanmax`, `np.nanargmin` y `np.nanargmax` lanzan `ValueError` si el slice evaluado esta compuesto enteramente por NaN. Las variantes de suma y promedio devuelven 0 o NaN segun la funcion.
