---
title: np/estadisticas — analisis estadistico avanzado
tags:
  - numpy
  - indice
draft: false
---

# np/estadisticas — analisis estadistico avanzado

Este grupo cubre el analisis estadistico que va mas alla de los estadisticos de resumen simples. Las funciones de [[Numpy/np/reducciones/index|reducciones]] (suma, media, desviacion estandar) colapsan un array a un solo numero. Las funciones de `estadisticas/` describen la **distribucion** de los datos o la **relacion entre variables**: el resultado es siempre una estructura — una matriz, un par de arrays (conteos + bordes), un vector de cuantiles.

El grupo se divide en dos ejes: relaciones entre variables (correlacion, covarianza) y distribucion de frecuencias (histogramas, bincount, digitize, percentiles).

## Notas de la carpeta

- [[np.corrcoef]] — matriz de correlacion de Pearson entre las filas de la entrada. Cada elemento (i,j) es la correlacion lineal normalizada entre las variables i y j, con valores en [-1, 1]. Rapida forma de detectar relaciones lineales entre multiples variables simultaneamente.
- [[np.cov]] — matriz de covarianza. Similar a `corrcoef` pero sin normalizar: los elementos diagonales son las varianzas de cada variable. Sensible a la escala de los datos; si las unidades son heterogeneas, preferir `corrcoef`.
- [[np.histogram]] — distribucion de frecuencias de un array 1D: cuenta cuantos valores caen en cada intervalo (bin). Devuelve el par `(conteos, bordes_de_bins)`. No dibuja nada; para visualizar, pasar el resultado a Matplotlib.
- [[np.histogram2d]] — histograma 2D de dos variables simultaneas. Devuelve una matriz de conteos y los bordes de ambos ejes. Base para generar mapas de calor o densidades conjuntas.
- [[np.histogramdd]] — generalizacion N-dimensional de `histogram`. El argumento `sample` tiene forma `(N, D)` donde D es la dimension. Util para analisis de datos multivariados.
- [[np.bincount]] — cuenta cuantas veces aparece cada entero no negativo en `x`. Mas rapido que `histogram` para datos enteros discretos porque no necesita definir bins: el indice del resultado es el valor contado.
- [[np.digitize]] — asigna cada valor de `x` al bin al que pertenece y devuelve el indice de ese bin. No cuenta; complementa a `histogram` cuando se necesita saber a que intervalo pertenece cada dato individual.
- [[np.percentile]] — calcula el percentil `q` del array: el valor por debajo del cual cae el `q%` de los datos. `q=50` es la mediana. Soporta multiples percentiles en una sola llamada pasando una lista a `q`.
