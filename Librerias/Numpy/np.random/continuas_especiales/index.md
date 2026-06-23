---
title: continuas_especiales — distribuciones continuas más allá de uniforme y normal
tags:
  - numpy
  - indice
draft: false
---

# continuas_especiales — distribuciones continuas especiales

Distribuciones continuas para **modelado estadístico**: cuando los datos no se distribuyen normalmente y hace falta capturar **asimetría**, **colas pesadas**, **soporte positivo** o **proporciones acotadas**. Cada una tiene un contexto de uso típico en estadística o simulación. Todas comparten el parámetro [[concepto_shape|`size`]] para fijar la forma de salida y conviven con la API moderna del [[np.random.default_rng|Generator]].

## Distribuciones

| Distribución | Parámetros | PDF / uso |
|---|---|---|
| [[np.random.beta]] | `a`, `b` | $\propto x^{a-1}(1-x)^{b-1}$ en $(0,1)$ · proporciones, tasas de conversión, priors bayesianos |
| [[np.random.chisquare]] | `df` | suma de `df` normales al cuadrado · bondad de ajuste, varianzas |
| [[np.random.exponential]] | `scale` | $\frac{1}{b}e^{-x/b}$, $x\ge0$ · tiempo entre eventos de Poisson, sin memoria |
| [[np.random.f]] | `dfnum`, `dfden` | cociente de dos chi-cuadrados · ANOVA, igualdad de varianzas |
| [[np.random.gamma]] | `shape`, `scale` | $\propto x^{k-1}e^{-x/\theta}$, $x>0$ · suma de exponenciales, duraciones |
| [[np.random.laplace]] | `loc`, `scale` | $\frac{1}{2b}e^{-\lvert x-\mu\rvert/b}$ · pico agudo, regularización L1 (LASSO) |
| [[np.random.logistic]] | `loc`, `scale` | $\frac{e^{-z}}{s(1+e^{-z})^2}$ · campana con colas pesadas, regresión logística |
| [[np.random.lognormal]] | `mean`, `sigma` | $\ln X \sim \mathcal{N}(\mu,\sigma^2)$, $x>0$ · datos multiplicativos: precios, tamaños |
| [[np.random.t]] | `df` | $\propto (1+t^2/\nu)^{-(\nu+1)/2}$ · colas pesadas, tests con muestras pequeñas |

La **exponencial** es sin memoria: la espera no depende del tiempo ya transcurrido. La **beta** con `a=b=1` es uniforme y con `a,b>1` es acampanada en $0.5$. La **t de Student** tiende a la normal cuando `df → ∞` y es Cauchy cuando `df=1`. La **log-normal** modela datos cuyo logaritmo es normal. **Laplace** y **logística** comparten colas pesadas, pero Laplace tiene pico agudo y la logística pico redondeado.

> [!tip] Versión moderna (API recomendada)
> Estas funciones usan el **estado global** de `np.random` (*legacy*). En código nuevo, crea un generador propio con [[np.random.default_rng]] y llama a los métodos homónimos:
> ```python
> rng = np.random.default_rng(seed=42)
> rng.laplace(0, 1, size=5)
> rng.lognormal(0, 1, size=5)
> rng.standard_t(df=10, size=5)   # ojo: 't' se llama 'standard_t' en Generator
> ```
> El `Generator` no comparte estado global, permite múltiples flujos independientes y es más rápido.

## Ejemplos rápidos

```python
import numpy as np
np.random.seed(0)

np.random.exponential(scale=2.0, size=5)      # tiempo entre eventos (tasa=0.5)
np.random.gamma(shape=2, scale=1.0, size=5)   # suma de 2 exponenciales
np.random.beta(a=0.5, b=0.5, size=5)          # distribución en (0, 1)
np.random.chisquare(df=4, size=5)             # 4 grados de libertad
np.random.f(dfnum=5, dfden=2, size=5)         # cociente chi2(5)/chi2(2)
np.random.t(df=10, size=5)                    # t de Student, df=10
np.random.laplace(loc=0, scale=1, size=5)     # colas pesadas, pico agudo
np.random.logistic(loc=0, scale=1, size=5)    # campana con colas pesadas
np.random.lognormal(mean=0, sigma=1, size=5)  # log(X) ~ N(0, 1)
```

## Relaciones entre distribuciones

- `gamma(shape=1, scale=b)` equivale a `exponential(scale=b)`.
- `chisquare(df=k)` equivale a `gamma(shape=k/2, scale=2)`.
- Si `X ~ lognormal(μ, σ)` entonces `log(X) ~ N(μ, σ²)`.
- La `t(df)` tiende a la normal estándar cuando `df → ∞`; con `df=1` es Cauchy.
- El cuadrado de una `t(df)` es una `f(dfnum=1, dfden=df)`.

## Notas relacionadas

- [[np.random.normal]] · [[np.random.standard_normal]] — el contraste sin colas pesadas
- [[np.random.default_rng]] — la API moderna basada en `Generator`
- [[np.random.seed]] · [[concepto_shape]]
