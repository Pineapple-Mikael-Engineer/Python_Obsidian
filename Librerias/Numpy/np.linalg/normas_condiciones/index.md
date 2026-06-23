---
title: normas y condiciones — tamaño, sensibilidad numérica y rango de matrices
tags:
  - numpy
  - indice
draft: false
---

# normas y condiciones — tamaño, sensibilidad numérica y rango de matrices

Esta carpeta reúne las funciones que **miden propiedades** de un vector o una matriz antes de
operar con ellos: su **tamaño** (norma), su **sensibilidad numérica** (número de condición) y su
**independencia lineal** (rango). No transforman la matriz: la *diagnostican*. La pregunta que
responden, en conjunto, es la que conviene hacerse antes de resolver un sistema lineal: *¿cuán
grande es?, ¿cuán fiable será la solución?, ¿cuántas ecuaciones son realmente independientes?*.

- **Norma** ([[np.linalg.norm]]): el **tamaño** de un vector o una matriz. Magnitudes, distancias,
  errores residuales, normalización.
- **Condición** ([[np.linalg.cond]]): la **sensibilidad numérica**. Un número de condición $\kappa$
  grande avisa de que la solución de $Ax=b$ amplificará los errores de los datos.
- **Rango** ([[np.linalg.matrix_rank]]): la **independencia lineal**. Cuántas filas/columnas no son
  combinación de las otras; detecta deficiencia de rango y sistemas sin solución única.

## Funciones

| Función | Qué mide | Mapa de shapes | Caso típico |
|---|---|---|---|
| [[np.linalg.norm]] | tamaño (vector o matriz) | $(\dots,n)\to(\dots)$ o $(\dots,m,n)\to(\dots)$ | distancias, error residual, normalizar |
| [[np.linalg.cond]] | sensibilidad numérica | $(\dots,m,n)\to(\dots)$ | diagnosticar si un sistema es mal condicionado |
| [[np.linalg.matrix_rank]] | independencia lineal | $(\dots,m,n)\to(\dots)$ entero | detectar dependencia, deficiencia de rango |

## La tabla de `ord` de `norm`

`np.linalg.norm` es la pieza central: **un mismo `ord` significa cosas distintas** según se norme
un vector (un eje) o una matriz (dos ejes). Con $\sigma_i$ los valores singulares de la
[[np.linalg.svd|SVD]]:

| `ord` | Vector (1 eje) | Matriz (2 ejes) |
|-------|----------------|-----------------|
| `None` | euclídea $\sqrt{\sum_i x_i^2}$ | Frobenius $\sqrt{\sum_{ij} A_{ij}^2}$ |
| `2` | euclídea | espectral $\sigma_{\max}$ |
| `1` | $\sum_i |x_i|$ | máx. suma de columna |
| `np.inf` | $\max_i |x_i|$ | máx. suma de fila |
| `-np.inf` | $\min_i |x_i|$ | mín. suma de fila |
| `0` | nº de no nulos | — |
| `p` (float) | $(\sum_i |x_i|^p)^{1/p}$ | — |
| `'fro'` | — | Frobenius |
| `'nuc'` | — | nuclear $\sum_i \sigma_i$ |

## Cómo se conectan

Las tres funciones están atadas por la [[np.linalg.svd|descomposición en valores singulares]]: la
SVD es el motor común que las hace coherentes entre sí.

- La **norma espectral** ($\lVert A\rVert_2$) es el **mayor** valor singular, $\sigma_{\max}$; la
  **nuclear** es su **suma**, $\sum_i \sigma_i$; la **Frobenius**, $\sqrt{\sum_i \sigma_i^2}$.
- El **número de condición** con `p=2` es el **cociente** $\kappa_2 = \sigma_{\max}/\sigma_{\min}$:
  reutiliza los extremos del espectro singular.
- El **rango** es el **número** de valores singulares por encima de un umbral, $\#\{\sigma_i > \tau\}$.

Así, `cond` y `matrix_rank` son dos lecturas distintas del mismo espectro de valores singulares:
$\kappa$ mira su **rango dinámico** (lo grande frente a lo pequeño) y el rango cuenta **cuántos son
significativos**. Una $\sigma_{\min}$ casi nula dispara $\kappa$ hacia $\infty$ y baja el rango: las
dos señalan la misma patología (matriz casi singular) desde ángulos complementarios.

## Notas relacionadas

- [[np.linalg.svd]] — el motor común (valores singulares) detrás de norma, condición y rango
- [[np.linalg.norm]] — la función central de la carpeta
- [[np.linalg.solve]] · [[np.linalg.lstsq]] — a quién avisa un `cond` alto
- [[Librerias/Numpy/np.linalg/index|np.linalg]] · [[Librerias/Numpy/index|NumPy raíz]]
