---
title: np/reducciones — funciones que reducen dimension
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones — funciones que reducen dimension

Las funciones de `reducciones/` toman N elementos de un array y producen un escalar o un array de menor rango. En total son **29 funciones** organizadas en 5 subcarpetas.

El parametro clave es `axis`: controla sobre que eje se colapsa el array. Con `axis=None` (defecto) se reduce todo el array a un escalar; con `axis=0` se colapsa a lo largo de las filas, etc.

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])

np.sum(M)           # 21         — escalar (axis=None)
np.sum(M, axis=0)   # [5, 7, 9]  — una suma por columna
np.sum(M, axis=1)   # [6, 15]    — una suma por fila
```

## Subcarpetas

| Subcarpeta | Funciones | Que hace |
|---|---|---|
| [[Librerias/Numpy/np/reducciones/agregacion/index\|agregacion/]] | 4 | Suma y producto, simple y acumulativo |
| [[Librerias/Numpy/np/reducciones/promedios/index\|promedios/]] | 5 | Estadistica descriptiva: media, mediana, dispersion |
| [[Librerias/Numpy/np/reducciones/extremos/index\|extremos/]] | 5 | Valor minimo/maximo y sus indices |
| [[Librerias/Numpy/np/reducciones/diferencial/index\|diferencial/]] | 3 | Calculo numerico: derivadas e integrales discretas |
| [[Librerias/Numpy/np/reducciones/nan_safe/index\|nan_safe/]] | 12 | Variantes nan* que ignoran NaN en el calculo |

## Tabla de decision

| Quiero... | Subcarpeta |
|---|---|
| Sumar o multiplicar elementos | [[Librerias/Numpy/np/reducciones/agregacion/index\|agregacion/]] |
| Estadistica descriptiva (media, varianza...) | [[Librerias/Numpy/np/reducciones/promedios/index\|promedios/]] |
| Encontrar el minimo, maximo o su posicion | [[Librerias/Numpy/np/reducciones/extremos/index\|extremos/]] |
| Derivadas o integrales numericas | [[Librerias/Numpy/np/reducciones/diferencial/index\|diferencial/]] |
| Mis datos tienen NaN y no quiero propagar el error | [[Librerias/Numpy/np/reducciones/nan_safe/index\|nan_safe/]] |
