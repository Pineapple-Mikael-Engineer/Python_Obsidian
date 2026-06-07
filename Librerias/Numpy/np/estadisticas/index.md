---
title: np/estadisticas — funciones de analisis estadistico avanzado
tags:
  - numpy
  - indice
draft: false
---

# np/estadisticas — funciones de analisis estadistico avanzado

`estadisticas/` agrupa funciones de analisis estadistico que van mas alla de las reducciones basicas (`sum`, `mean`, `std`, `var`) que viven en [[Numpy/np/reducciones/index|reducciones]]. Aqui encontraras correlacion, covarianza, histogramas en 1D/2D/ND, percentiles y herramientas de discretizacion.

## Tabla de decision

| Necesito… | Funcion |
|-----------|---------|
| Coeficiente de correlacion de Pearson entre variables | [[np.corrcoef]] |
| Matriz de covarianza entre variables | [[np.cov]] |
| Distribucion de frecuencias de un array 1D | [[np.histogram]] |
| Histograma bidimensional (densidad 2D) | [[np.histogram2d]] |
| Histograma N-dimensional | [[np.histogramdd]] |
| Conteo de enteros no negativos | [[np.bincount]] |
| Asignar cada valor a un intervalo (bin) | [[np.digitize]] |
| Percentil o cuantil de un array | [[np.percentile]] |

## Ejemplo: correlacion e histograma

```python
import numpy as np

# Correlacion entre dos variables
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
np.corrcoef(x, y)      # matriz 2x2, [0,1] es la correlacion cruzada

# Histograma 1D
datos = np.random.randn(1000)
conteos, bordes = np.histogram(datos, bins=20)
# conteos: frecuencias por intervalo
# bordes: los 21 limites de los 20 bins

# Percentil
np.percentile(datos, [25, 50, 75])   # Q1, mediana, Q3
```

## Relacion con reducciones

Las funciones de `reducciones/` como `np.mean`, `np.std` y `np.var` calculan estadisticos de resumen directamente sobre un array. Las funciones de `estadisticas/` analizan la **distribucion** o la **relacion entre variables**: necesitas mas de un numero para describir el resultado (matrices, arrays de conteos, bordes de bins).

## Notas de la carpeta

- [[np.corrcoef]] — coeficientes de correlacion de Pearson
- [[np.cov]] — matriz de covarianza
- [[np.histogram]] — histograma 1D (conteos y bordes de bins)
- [[np.histogram2d]] — histograma bidimensional
- [[np.histogramdd]] — histograma N-dimensional
- [[np.bincount]] — conteo de ocurrencias de enteros no negativos
- [[np.digitize]] — asignacion de valores a intervalos
- [[np.percentile]] — percentiles y cuantiles
