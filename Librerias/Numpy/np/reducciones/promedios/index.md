---
title: np/reducciones/promedios — estadistica descriptiva
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/promedios — estadistica descriptiva

Las 5 funciones de esta subcarpeta cubren las medidas clasicas de tendencia central y dispersion. Responden dos preguntas sobre un conjunto de datos: "donde estan concentrados" (mean, median, average) y "cuanto se dispersan alrededor de ese centro" (std, var). Todas aceptan `axis=` para operar por filas o columnas en matrices.

La diferencia mas importante entre las tres medidas de tendencia central: `mean` es la mas eficiente pero sensible a valores extremos; `median` es robusta a outliers pero mas lenta porque requiere ordenar el array internamente; `average` permite asignar pesos distintos a cada elemento cuando no todos contribuyen por igual.

```python
import numpy as np
a = np.array([1.0, 2.0, 3.0, 100.0])  # 100 es un outlier

np.mean(a)    # 26.5  — arrastrado por el outlier
np.median(a)  # 2.5   — robusta, no se ve afectada

np.std(a, ddof=1)  # desviacion muestral (ddof=1 es la convencion estadistica)
np.var(a, ddof=1)  # np.std(a, ddof=1)**2
```

## Notas de esta subcarpeta

| Funcion | Que hace |
|---|---|
| [[np.mean]] | Media aritmetica (suma dividida entre n). Sensible a outliers. Con `axis=0` da la media de cada columna; con `axis=1` la media de cada fila. |
| [[np.median]] | Valor central cuando los datos se ordenan. Robusta a outliers a diferencia de la media. Mas lenta que `mean` en arrays grandes por el paso de ordenamiento interno. |
| [[np.average]] | Media ponderada: igual que `mean` cuando no se pasan pesos, pero acepta `weights=` para dar distinta importancia a cada elemento. Util para promedios de notas o medias moviles ponderadas. |
| [[np.std]] | Desviacion estandar. `ddof=0` (por defecto) es la desviacion poblacional; `ddof=1` es la muestral, que usa la mayoria de paquetes estadisticos y lenguajes de programacion. |
| [[np.var]] | Varianza: igual que `std` pero sin la raiz cuadrada. `np.var(a, ddof=k) == np.std(a, ddof=k)**2`. Se usa como paso intermedio en calculos donde la raiz se cancela o es innecesaria. |

## Cuando usar cada una

| Situacion | Funcion |
|---|---|
| Distribucion simetrica sin valores extremos | [[np.mean]] |
| Distribucion sesgada o con outliers | [[np.median]] |
| Cada elemento tiene un peso distinto | [[np.average]] |
| Medir dispersion en las unidades originales | [[np.std]] |
| Medir dispersion en unidades cuadradas (calculo intermedio) | [[np.var]] |

> [!tip] Datos con NaN
> Si el array puede contener NaN, usa las variantes de [[Librerias/Numpy/np/reducciones/nan_safe/index|nan_safe/]]: [[np.nanmean]], [[np.nanmedian]], [[np.nanstd]], [[np.nanvar]].
