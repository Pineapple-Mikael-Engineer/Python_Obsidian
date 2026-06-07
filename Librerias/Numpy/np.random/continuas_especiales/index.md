---
title: continuas_especiales — distribuciones continuas mas alla de uniforme y normal
tags:
  - numpy
  - indice
draft: false
---

# continuas_especiales — distribuciones continuas mas alla de uniforme y normal

Distribuciones continuas para modelado estadistico: cuando los datos no se distribuyen normalmente y se necesita una distribucion que capture asimetria, colas pesadas u otras caracteristicas. Cada una tiene un contexto de uso tipico en estadistica o simulacion.

## Funciones

| Funcion | Cuando usarla |
|---------|---------------|
| [[np.random.exponential]] | Tiempo entre eventos en un proceso de Poisson; `scale = 1/lambda` |
| [[np.random.gamma]] | Suma de exponenciales independientes; modelado de duraciones |
| [[np.random.beta]] | Proporciones en (0, 1); modelado bayesiano de tasas de conversion |
| [[np.random.chisquare]] | Suma de normales al cuadrado; pruebas de bondad de ajuste |
| [[np.random.f]] | Ratio de chi-cuadradas; ANOVA y pruebas de igualdad de varianzas |
| [[np.random.t]] | t de Student; intervalos de confianza con muestras pequenas |
| [[np.random.laplace]] | Colas mas pesadas que la normal; regularizacion LASSO (prior Laplace) |
| [[np.random.logistic]] | Similar a la normal con colas mas pesadas; regresion logistica bayesiana |
| [[np.random.lognormal]] | Datos multiplicativos siempre positivos: precios de activos, tamanos de archivo |

La exponencial es sin memoria: la distribucion de espera no depende de cuanto tiempo ya paso. La beta para a=b=1 es uniforme; para a,b > 1 es campaniforme centrada en 0.5. La t de Student tiene colas mas pesadas que la normal para df bajos; a medida que df → inf se aproxima a la normal. La lognormal modela datos donde el logaritmo es normal: si X ~ lognormal(mu, sigma), entonces log(X) ~ N(mu, sigma).

## Ejemplos rapidos

```python
import numpy as np
np.random.seed(0)

np.random.exponential(scale=2.0, size=5)      # tiempo entre eventos (tasa=0.5)
np.random.gamma(shape=2, scale=1.0, size=5)   # suma de 2 exponenciales
np.random.beta(a=0.5, b=0.5, size=5)          # distribucion en (0, 1)
np.random.chisquare(df=4, size=5)             # 4 grados de libertad
np.random.f(dfnum=5, dfden=2, size=5)         # ratio chi2(5)/chi2(2)
np.random.t(df=10, size=5)                    # t de Student, df=10
np.random.laplace(loc=0, scale=1, size=5)     # colas mas pesadas que normal
np.random.logistic(loc=0, scale=1, size=5)    # forma similar a normal, colas mas gordas
np.random.lognormal(mean=0, sigma=1, size=5)  # log(X) ~ N(0, 1)
```

## Relaciones entre distribuciones

- `gamma(shape=1, scale=b)` es equivalente a `exponential(scale=b)`.
- `chisquare(df=k)` es equivalente a `gamma(shape=k/2, scale=2)`.
- Si `X ~ lognormal(mu, sigma)` entonces `log(X) ~ N(mu, sigma)`.
