---
title: np/reducciones — funciones que colapsan dimensiones
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones — funciones que colapsan dimensiones

Las reducciones toman un array de N elementos y producen un resultado de menor rango: colapsan uno o varios ejes, convirtiendo filas o columnas enteras en un solo valor. Son la herramienta central para pasar de datos crudos a estadisticas, totales o derivadas.

El parametro `axis` controla sobre que eje se colapsa: `axis=None` reduce todo el array a un escalar, `axis=0` colapsa a lo largo de las filas (resultado: una fila), `axis=1` colapsa a lo largo de las columnas (resultado: una columna). El parametro `keepdims=True` mantiene las dimensiones colapsadas como tamaño 1, lo que permite hacer broadcasting posterior sin necesidad de un `reshape` manual.

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])

np.sum(M)           # 21        — escalar (axis=None)
np.sum(M, axis=0)   # [5, 7, 9] — una suma por columna
np.sum(M, axis=1)   # [6, 15]   — una suma por fila

np.sum(M, axis=0, keepdims=True)  # [[5, 7, 9]] — shape (1,3), util para broadcast
```

## Subcarpetas

| Subcarpeta | Funciones | Concepto |
|---|---|---|
| [[Librerias/Numpy/np/reducciones/agregacion/index\|agregacion/]] | 4 | Suma y producto, en version reductora y acumulativa |
| [[Librerias/Numpy/np/reducciones/promedios/index\|promedios/]] | 5 | Estadistica de tendencia central y dispersion |
| [[Librerias/Numpy/np/reducciones/extremos/index\|extremos/]] | 5 | Valores minimos/maximos y sus posiciones en el array |
| [[Librerias/Numpy/np/reducciones/diferencial/index\|diferencial/]] | 3 | Calculo numerico discreto: derivadas e integrales aproximadas |
| [[Librerias/Numpy/np/reducciones/nan_safe/index\|nan_safe/]] | 12 | Gemelas de las anteriores que ignoran NaN en vez de propagarlo |

## Tabla de decision

| Quiero... | Subcarpeta |
|---|---|
| Sumar o multiplicar elementos (con o sin acumulacion) | [[Librerias/Numpy/np/reducciones/agregacion/index\|agregacion/]] |
| Media, mediana, desviacion estandar o varianza | [[Librerias/Numpy/np/reducciones/promedios/index\|promedios/]] |
| El minimo, el maximo o el indice donde se encuentran | [[Librerias/Numpy/np/reducciones/extremos/index\|extremos/]] |
| Derivadas o integrales numericas sobre datos muestreados | [[Librerias/Numpy/np/reducciones/diferencial/index\|diferencial/]] |
| Cualquiera de lo anterior pero mis datos pueden tener NaN | [[Librerias/Numpy/np/reducciones/nan_safe/index\|nan_safe/]] |
