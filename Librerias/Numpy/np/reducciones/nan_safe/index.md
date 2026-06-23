---
title: np/reducciones/nan_safe — variantes que ignoran NaN
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/nan_safe — variantes que ignoran NaN

Esta subcarpeta agrupa las **variantes NaN-safe** de las reducciones: cada una es la **gemela** de
una reducción de [[Librerias/Numpy/np/reducciones/agregacion/index|agregación]], [[Librerias/Numpy/np/reducciones/promedios/index|promedios]]
o [[Librerias/Numpy/np/reducciones/extremos/index|extremos]], con una sola diferencia: en vez de **propagar** el
`NaN` (un solo `NaN` contamina todo el resultado), lo **ignoran**. Sin ellas, un hueco en los datos
arruina el cálculo completo:

```python
import numpy as np
a = np.array([1.0, 2.0, np.nan, 4.0])

np.sum(a)     # nan   — un NaN contamina el resultado
np.nansum(a)  # 7.0   — el NaN se descarta, se suma el resto

np.mean(a)    # nan
np.nanmean(a) # 2.333...
```

## El patrón

La idea unificadora es tratar el `NaN` como **ausencia de dato**, lo que se traduce de forma distinta
según la operación:

- **Suma / producto**: el `NaN` se sustituye por el **elemento neutro** de la operación — `0` en la
  suma (no cambia el total), `1` en el producto (no cambia el resultado).
- **Medias / desviaciones**: el `NaN` se **omite del cálculo** y, crucialmente, el **divisor pasa a
  ser el conteo de no-NaN** (no el tamaño total del eje), para que la media sea la de los datos reales.
- **Extremos / argumentos**: el máximo/mínimo (o su índice) se toma solo entre los elementos no-NaN
  del eje.

El coste: internamente hay que **localizar y enmascarar** los NaN antes de calcular, un recorrido
extra sobre el array. Si se garantiza que los datos no tienen NaN, las versiones normales son más
eficientes.

## Tabla gemela ↔ nan-safe

| Función normal | Variante nan-safe | Categoría |
|---|---|---|
| [[np.sum]] | [[np.nansum]] | agregación |
| [[np.prod]] | [[np.nanprod]] | agregación |
| [[np.cumsum]] | [[np.nancumsum]] | agregación |
| [[np.cumprod]] | [[np.nancumprod]] | agregación |
| [[np.mean]] | [[np.nanmean]] | promedios |
| [[np.std]] | [[np.nanstd]] | promedios |
| [[np.var]] | [[np.nanvar]] | promedios |
| [[np.median]] | [[np.nanmedian]] | promedios |
| [[np.max]] | [[np.nanmax]] | extremos |
| [[np.min]] | [[np.nanmin]] | extremos |
| [[np.argmax]] | [[np.nanargmax]] | extremos |
| [[np.argmin]] | [[np.nanargmin]] | extremos |

> [!warning] Slice todo-NaN: la trampa depende de la función
> Cuando **todos** los elementos del eje reducido son `NaN`, el comportamiento no es uniforme:
> - **`nansum` / `nanprod`** → devuelven el elemento neutro: `0` (suma) o `1` (producto). Silencioso.
> - **`nanmean` / `nanstd` / `nanvar` / `nanmax` / `nanmin`** → devuelven `NaN` con un
>   `RuntimeWarning: All-NaN slice encountered` (o `Mean of empty slice`). Recuperable.
> - **`nanargmax` / `nanargmin`** → lanzan un **`ValueError`** (no hay índice válido que devolver).
>   No es un warning: es un **error** que aborta la llamada. En N-D basta con un slice todo-NaN.

## Notas relacionadas

- [[Librerias/Numpy/np/reducciones/agregacion/index|reducciones · agregación]] — las gemelas de suma y producto
- [[Librerias/Numpy/np/reducciones/promedios/index|reducciones · promedios]] — las gemelas de media y dispersión
- [[Librerias/Numpy/np/reducciones/extremos/index|reducciones · extremos]] — las gemelas de máximo, mínimo y argumentos
- [[concepto_axis_parametro]] — el eje que toda reducción colapsa
