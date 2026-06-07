---
title: continuas_especiales — distribuciones continuas mas alla de uniforme y normal
tags:
  - numpy
  - indice
draft: false
---

# continuas_especiales — distribuciones continuas mas alla de uniforme y normal

Nueve distribuciones continuas para simulacion estadistica, modelado de fenomenos fisicos y analisis de datos.

## Funciones

| Funcion | Cuando usarla |
|---------|---------------|
| [[np.random.exponential]] | Tiempo entre eventos en un proceso de Poisson |
| [[np.random.gamma]] | Suma de variables exponenciales; modelado de duraciones |
| [[np.random.beta]] | Proporciones en (0, 1); modelado bayesiano |
| [[np.random.chisquare]] | Suma de normales al cuadrado; pruebas de bondad de ajuste |
| [[np.random.f]] | Ratio de chi-cuadradas; ANOVA y pruebas F |
| [[np.random.t]] | t de Student; intervalos de confianza con muestras pequenas |
| [[np.random.laplace]] | Datos con colas pesadas; regularizacion LASSO |
| [[np.random.logistic]] | Curvas sigmoide; regresion logistica |
| [[np.random.lognormal]] | Datos multiplicativos; precios financieros; tamanos de archivo |

## Ejemplos rapidos

```python
import numpy as np
np.random.seed(0)

np.random.exponential(scale=2.0, size=5)     # tiempo entre eventos (tasa=0.5)
np.random.gamma(shape=2, scale=1.0, size=5)  # suma de 2 exponenciales
np.random.beta(a=0.5, b=0.5, size=5)        # distribucion en (0,1)
np.random.chisquare(df=4, size=5)            # 4 grados de libertad
np.random.f(dfnum=5, dfden=2, size=5)        # ratio chi2(5)/chi2(2)
np.random.t(df=10, size=5)                   # t de Student, df=10
np.random.laplace(loc=0, scale=1, size=5)    # colas mas pesadas que normal
np.random.logistic(loc=0, scale=1, size=5)   # forma similar a normal, colas mas gordas
np.random.lognormal(mean=0, sigma=1, size=5) # log(X) ~ N(0,1)
```

## Relaciones entre distribuciones

- `gamma(shape=1, scale=b)` es equivalente a `exponential(scale=b)`.
- `chisquare(df=k)` es equivalente a `gamma(shape=k/2, scale=2)`.
- Si `X ~ lognormal(mu, sigma)` entonces `log(X) ~ N(mu, sigma)`.
