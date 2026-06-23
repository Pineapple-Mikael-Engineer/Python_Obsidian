---
title: np/estadísticas — distribución de frecuencias y relación entre variables
tags:
  - numpy
  - indice
draft: false
---

# np/estadísticas — distribución de frecuencias y relación entre variables

Este grupo cubre el análisis estadístico que va más allá de los estadísticos de resumen. Las funciones de [[Numpy/np/reducciones/index|reducciones]] (suma, media, desviación estándar) colapsan un array a un solo número; las de `estadísticas/` describen la **estructura** de los datos: cómo se **distribuyen** (cuántos valores caen dónde) o cómo se **relacionan** las variables entre sí. El resultado nunca es un escalar — es una estructura: una matriz de correlación, un par `(conteos, bordes)`, un tensor de conteos N-dimensional, un vector de etiquetas de bin.

El grupo se ordena en dos ejes.

## Contar y agrupar datos (distribución de frecuencias)

Cuántos valores caen en cada intervalo o categoría. El eje central es el **histograma**, que escala de 1D a N-D, más dos primitivas de apoyo (`digitize` etiqueta, `bincount` cuenta enteros):

| Función | Qué hace | Entrada → salida |
|---|---|---|
| [[np.histogram]] | cuenta valores por bin en **1D** | `(N,)` → `(hist (bins,), edges (bins+1,))` |
| [[np.histogram2d]] | histograma **2D** de dos variables `x, y` | dos `(N,)` → `(H (nx, ny), xe, ye)` |
| [[np.histogramdd]] | histograma en **D dimensiones** (el caso N-D natural) | `(N, D)` → `(H (n_0,…,n_{D-1}), edges)` |
| [[np.digitize]] | **a qué bin** pertenece cada valor (índice, no conteo) | `x` → índices con shape de `x` |
| [[np.bincount]] | cuenta ocurrencias de **enteros no negativos** | `(N,)` → `(max(x)+1,)` |

La familia de histogramas comparte un retorno que conviene **desambiguar**: varias devuelven una tupla `(conteos, bordes)`, donde los **bordes tienen un elemento más** que los conteos en cada eje (`bins` conteos, `bins+1` bordes). `histogramdd` es la forma general — `histogram` (D=1) y `histogram2d` (D=2) son atajos cómodos —, y `histogram2d(x, y)` no es más que `histogramdd(np.column_stack([x, y]))`. `digitize` se apoya en la búsqueda binaria de [[np.searchsorted]]; `bincount` evita los bins porque el valor entero **es** su propio índice.

## Relación entre variables

Cómo covarían dos o más variables. Lo lleva otro agente; se listan para completar el mapa de la carpeta:

| Función | Qué hace |
|---|---|
| [[np.corrcoef]] | matriz de **correlación** de Pearson (normalizada, en `[-1, 1]`) |
| [[np.cov]] | matriz de **covarianza** (sin normalizar; diagonal = varianzas) |
| [[np.percentile]] | el percentil `q` de los datos (`q=50` es la mediana) |

## Cómo se conectan

- Para **contar** por intervalo continuo → [[np.histogram]]; para **etiquetar** cada dato con su bin → [[np.digitize]]; ambos sobre los mismos bordes son complementarios.
- Para datos **enteros pequeños** evita definir bins: [[np.bincount]] es más directo que `histogram`.
- Más de una variable → sube de dimensión: [[np.histogram2d]] (2 variables) o [[np.histogramdd]] (D variables, con marginales vía [[np.sum]] sobre sus ejes).
- Ninguna de estas funciones **dibuja**: calculan; la visualización se delega a Matplotlib.

## Notas relacionadas

- [[Numpy/np/reducciones/index|reducciones]] — los estadísticos de resumen (media, std) que sí colapsan a escalar
- [[np.searchsorted]] — la búsqueda binaria que sostiene a `digitize`
- [[concepto_shape]] — por qué conteos y bordes difieren en longitud
