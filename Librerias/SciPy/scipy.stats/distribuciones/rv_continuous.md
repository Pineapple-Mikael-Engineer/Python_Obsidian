---
title: rv_continuous — modelo de objeto de distribucion continua de scipy.stats
aliases:
  - rv_continuous
  - scipy.stats.rv_continuous
  - modelo de distribucion
  - distribucion congelada
tags:
  - scipy
  - api/clase
  - distribuciones
lib: scipy
tipo: clase
mod: scipy.stats
requiere:
  - numpy
draft: false
---

# rv_continuous — modelo de objeto de distribucion continua de scipy.stats

Clase base de todas las distribuciones **continuas** de `scipy.stats`. Cada distribucion concreta (`norm`, `t`, `chi2`, `uniform`, ...) es una **instancia** de `rv_continuous` que ya implementa su funcion de densidad; el usuario casi nunca crea una `rv_continuous` a mano, sino que usa esas instancias. Lo importante es que **todas comparten la misma API de metodos**: aprendido el modelo aqui, se aplica identico a cualquier distribucion. Su analogo discreto es `rv_discrete`, identico salvo que reemplaza la densidad `.pdf(x)` por la masa de probabilidad `.pmf(k)`.

Esta nota es la **gobernante** del submodulo de distribuciones: documenta el modelo de objeto comun. Las distribuciones concretas como [[scipy.stats.norm]] referencian este modelo y solo detallan sus parametros propios.

## Parametros: forma, loc y scale

Toda llamada a un metodo recibe primero los **parametros de forma** propios de la distribucion (p. ej. `df` en `t` y `chi2`; `n, p` en `binom`) y luego dos parametros universales:

| Parametro | Significado | Efecto |
|-----------|-------------|--------|
| `loc` | desplazamiento (location) | traslada la distribucion: `x -> x - loc` |
| `scale` | escala | estira/comprime: `x -> x / scale` |

Por defecto `loc=0`, `scale=1` (forma estandar). En muchas distribuciones `loc`/`scale` tienen lectura directa: en `norm` son media y desviacion tipica; en `uniform` definen el intervalo `[loc, loc+scale]`. Las distribuciones discretas (`rv_discrete`) admiten `loc` pero **no** `scale`.

## Metodos comunes (la API transversal)

| Metodo | Que devuelve | Nota |
|--------|--------------|------|
| `.pdf(x, *forma, loc, scale)` | densidad de probabilidad en `x` | en discretas no existe; se usa `.pmf(k)` |
| `.pmf(k, *forma, loc)` | masa de probabilidad en `k` | solo `rv_discrete` |
| `.logpdf(x, ...)` | `log(pdf)`, estable numericamente | util en verosimilitudes |
| `.cdf(x, ...)` | funcion de distribucion acumulada `P(X <= x)` | crece de 0 a 1 |
| `.sf(x, ...)` | funcion de supervivencia `1 - cdf = P(X > x)` | mas precisa que `1-cdf` en colas |
| `.ppf(q, ...)` | funcion cuantil: inversa de `cdf`; `x` tal que `cdf(x)=q` | da valores criticos |
| `.isf(q, ...)` | inversa de `sf`: `x` tal que `sf(x)=q` | cuantil por la cola derecha |
| `.rvs(*forma, loc, scale, size, random_state)` | muestras aleatorias | `size` controla la forma del array |
| `.fit(datos, ...)` | estima parametros por maxima verosimilitud (MLE) | **solo continuas**; devuelve tupla `(*forma, loc, scale)` |
| `.mean(...)` | media teorica | |
| `.var(...)` | varianza teorica | |
| `.std(...)` | desviacion tipica teorica | |
| `.median(...)` | mediana (`= ppf(0.5)`) | |
| `.stats(..., moments='mv')` | momentos pedidos: `m`edia, `v`arianza, `s`kew, `k`urtosis | devuelve tupla |
| `.interval(confidence, ...)` | intervalo central que acumula esa probabilidad | p. ej. `0.95` -> `(ppf(0.025), ppf(0.975))` |
| `.moment(order, ...)` | momento no central de orden `n` | |
| `.entropy(...)` | entropia diferencial | |

> Regla mental: `cdf` y `ppf` son inversas; `sf` es la cola derecha y `isf` su inversa. Para "valores criticos" se usa `ppf` (cola izquierda) o `isf` (cola derecha).

## Dos formas de pasar los parametros

Cada metodo acepta los parametros **en cada llamada**, o bien se crea una **distribucion congelada** (frozen) que los fija una vez.

### Llamada con parametros (parametros en cada metodo)

```python
from scipy.stats import norm

norm.pdf(0, loc=10, scale=2)   # densidad en x=0 de una N(10, 2)
norm.cdf(12, loc=10, scale=2)  # repetir loc/scale en CADA llamada
```

### Distribucion congelada (frozen)

`dist(*forma, loc=, scale=)` devuelve un **objeto frozen** con los parametros ya incrustados. Sus metodos se llaman sin volver a pasarlos: codigo mas limpio y reutilizable.

```python
from scipy.stats import norm

X = norm(loc=10, scale=2)   # objeto frozen: una N(10, 2) concreta
X.pdf(0)                    # ya no se repiten loc/scale
X.cdf(12)                   # → 0.8413
X.ppf(0.975)                # → 13.92
X.rvs(size=1000)            # 1000 muestras de esta N(10, 2)
```

> Preferir el objeto frozen cuando se hacen varias consultas sobre la misma distribucion; usar la llamada con parametros para una sola operacion puntual.

## Patron de uso tipico

```python
import numpy as np
from scipy.stats import norm

# 1) consulta directa
norm.cdf(1.96)              # → 0.975

# 2) valor critico (cuantil)
norm.ppf(0.975)            # → 1.959...

# 3) muestreo
muestra = norm.rvs(loc=0, scale=1, size=10_000, random_state=0)

# 4) ajuste de parametros a datos (MLE), solo continuas
mu, sigma = norm.fit(muestra)   # → ~0.0, ~1.0
```

## Buenas practicas

1. Aprender los metodos una vez aqui; son identicos en toda distribucion continua y casi identicos en las discretas (`pmf` en vez de `pdf`).
2. Usar `.sf`/`.isf` en lugar de `1 - cdf` cuando se trabaja en colas extremas: es numericamente mas preciso.
3. Para valores criticos de tests e intervalos usar `.ppf` (cola izquierda) o `.isf` (cola derecha), no calcularlos a mano.
4. Fijar `random_state` en `.rvs` para resultados reproducibles.
5. Congelar la distribucion (`X = dist(...)`) cuando se reutilice; evita repetir `loc`/`scale`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `AttributeError: 'rv_discrete' has no 'pdf'` | distribucion discreta | usar `.pmf(k)` |
| `.scale` no afecta a una discreta | `rv_discrete` no admite `scale` | reparametrizar; solo `loc` aplica |
| `.fit` falla o no existe | `fit` es solo de continuas | las discretas no tienen MLE generico |
| Confundir `ppf` con `pdf` | nombres parecidos | `ppf` = cuantil (inversa de cdf); `pdf` = densidad |
| Olvidar `loc`/`scale` en cada llamada | no se uso frozen | congelar: `X = dist(loc=, scale=)` |

## Limitaciones

- `rv_continuous` modela distribuciones de **una variable**; para multivariantes existen objetos aparte (`multivariate_normal`, etc.).
- `.fit` usa MLE generico y puede no converger bien en distribuciones con muchos parametros de forma; conviene fijar algunos con `floc`/`fscale`.
- La densidad `.pdf` puede superar 1 (es densidad, no probabilidad); la probabilidad se obtiene integrando, es decir via `.cdf`.

## Notas relacionadas

- [[scipy.stats.norm]]
- [[scipy.stats.t]]
- [[scipy.stats.chi2]]
- [[scipy.stats.uniform]]
- [[scipy.stats.binom]]
