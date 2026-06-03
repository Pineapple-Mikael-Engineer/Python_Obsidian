---
title: scipy.stats.norm — distribucion normal (gaussiana)
aliases:
  - norm
  - scipy.stats.norm
  - distribucion normal
  - gaussiana
tags:
  - scipy
  - api/objeto
  - distribuciones
lib: scipy
tipo: objeto
mod: scipy.stats
requiere:
  - numpy
draft: false
---

# scipy.stats.norm — distribucion normal (gaussiana)

Objeto-distribucion de la **normal** (gaussiana), instancia de `rv_continuous`. Es la distribucion en forma de campana, base del teorema central del limite y de la inferencia clasica. No tiene parametros de forma propios: se controla solo con los universales `loc` y `scale`.

| Parametro | Simbolo | Significado | Defecto |
|-----------|---------|-------------|---------|
| `loc` | mu | media (centro de la campana) | `0` |
| `scale` | sigma | desviacion tipica (anchura) | `1` |

Con `loc=0`, `scale=1` es la **normal estandar** `N(0, 1)`. Toda la API de metodos (`pdf`, `cdf`, `sf`, `ppf`, `rvs`, `fit`, ...) es la comun a las distribuciones continuas, documentada en [[rv_continuous]]; aqui solo se ilustra con la normal.

## Consultas basicas

```python
from scipy.stats import norm

norm.pdf(0)        # densidad en 0 de la N(0,1) → 0.3989  (= 1/sqrt(2*pi))
norm.cdf(0)        # P(X <= 0) → 0.5  (simetrica respecto a la media)
norm.cdf(1.96)     # → 0.975
norm.sf(1.96)      # cola derecha P(X > 1.96) → 0.025
```

## Cuantiles y valores criticos

`ppf` (inversa de `cdf`) da los valores criticos clasicos de la normal estandar:

```python
from scipy.stats import norm

norm.ppf(0.975)    # cuantil 0.975 → 1.959...  (el famoso 1.96)
norm.ppf(0.5)      # mediana → 0.0
norm.isf(0.025)    # mismo 1.96 por la cola derecha → 1.96
norm.interval(0.95)   # intervalo central al 95% → (-1.96, 1.96)
```

## Con media y desviacion (loc, scale)

```python
from scipy.stats import norm

norm.pdf(10, loc=10, scale=2)   # densidad en la media de una N(10,2)
norm.cdf(12, loc=10, scale=2)   # P(X <= 12) → 0.8413  (una sigma)
norm.ppf(0.975, loc=10, scale=2)  # → 13.92
```

## Distribucion congelada

```python
from scipy.stats import norm

X = norm(loc=10, scale=2)   # frozen: una N(10, 2) reutilizable
X.mean()    # → 10.0
X.std()     # → 2.0
X.cdf(12)   # → 0.8413
X.ppf(0.975)  # → 13.92
```

## Muestreo aleatorio

```python
from scipy.stats import norm

datos = norm.rvs(loc=0, scale=1, size=10_000, random_state=0)
datos.shape    # → (10000,)
```

## Ajuste a datos (MLE)

`fit` estima `loc` y `scale` por maxima verosimilitud; para la normal coinciden con la media y la desviacion tipica muestrales.

```python
import numpy as np
from scipy.stats import norm

muestra = norm.rvs(loc=5, scale=3, size=5000, random_state=1)
mu, sigma = norm.fit(muestra)   # → ~5.0, ~3.0
```

## Buenas practicas

1. Recordar que `loc`/`scale` son media y desviacion tipica: leen directos, sin parametros de forma.
2. Para colas (p. ej. p-valores) usar `sf`/`isf` en vez de `1 - cdf`.
3. Para intervalos centrales usar `interval(confidence)` en lugar de calcular ambos cuantiles a mano.
4. Fijar `random_state` en `rvs` para reproducibilidad.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar varianza a `scale` | `scale` es sigma, no sigma^2 | usar la desviacion tipica |
| Esperar que `pdf` sea una probabilidad | es densidad; puede pasar de 1 al estrechar | integrar via `cdf` |
| Confundir `ppf` con `pdf` | nombres similares | `ppf` = cuantil; `pdf` = densidad |

## Notas relacionadas

- [[rv_continuous]]
- [[scipy.stats.t]]
- [[scipy.stats.chi2]]
