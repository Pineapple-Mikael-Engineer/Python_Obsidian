---
title: np/reducciones/promedios — estadistica descriptiva
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/promedios — estadistica descriptiva

Las 5 funciones de esta subcarpeta cubren las medidas clasicas de tendencia central y dispersion. Todas aceptan `axis=` para operar por eje.

## Notas de esta subcarpeta

| Funcion | Que hace |
|---|---|
| [[np.mean]] | Media aritmetica (suma / n) |
| [[np.median]] | Valor central (el elemento que queda en el medio al ordenar) |
| [[np.average]] | Media ponderada; acepta `weights=` para dar distinto peso a cada elemento |
| [[np.std]] | Desviacion estandar (raiz cuadrada de la varianza) |
| [[np.var]] | Varianza (promedio de las desviaciones al cuadrado) |

## Cuando usar cada una

- Distribucion simetrica sin outliers → [[np.mean]]
- Distribucion sesgada o con outliers → [[np.median]]
- Cada elemento tiene un peso distinto → [[np.average]]
- Medir dispersion en unidades originales → [[np.std]]
- Medir dispersion en unidades al cuadrado (para calculos intermedios) → [[np.var]]

> [!tip] Datos con NaN
> Si el array puede contener NaN, usa las variantes de [[Librerias/Numpy/np/reducciones/nan_safe/index|nan_safe/]]: [[np.nanmean]], [[np.nanmedian]], [[np.nanstd]], [[np.nanvar]].
