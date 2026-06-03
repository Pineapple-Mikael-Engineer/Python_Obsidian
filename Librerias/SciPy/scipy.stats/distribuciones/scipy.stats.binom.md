---
title: scipy.stats.binom — distribucion binomial (discreta)
aliases:
  - binom
  - scipy.stats.binom
  - distribucion binomial
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

# scipy.stats.binom — distribucion binomial (discreta)

Objeto-distribucion **binomial**, instancia de `rv_discrete` (no de `rv_continuous`). Modela el numero de **exitos** en `n` ensayos independientes con probabilidad `p` de exito en cada uno. Por ser **discreta**, su funcion fundamental es la **masa de probabilidad `.pmf(k)`**, no la densidad `.pdf`: `pmf(k)` da la probabilidad exacta de obtener `k` exitos.

| Parametro | Significado | Notas |
|-----------|-------------|-------|
| `n` | numero de ensayos (parametro de forma) | entero `>= 0` |
| `p` | probabilidad de exito por ensayo | en `[0, 1]` |
| `loc` | desplazamiento del soporte | defecto `0`; rara vez se usa |

Comparte casi toda la API con el modelo continuo (`cdf`, `sf`, `ppf`, `rvs`, `mean`, `var`, ...), documentada en [[rv_continuous]], con dos diferencias por ser discreta: usa **`.pmf`** en vez de `.pdf`, y **no admite `scale`** ni el metodo `.fit`.

## pmf en vez de pdf (clave por ser discreta)

```python
from scipy.stats import binom

# Probabilidad de exactamente k=3 exitos en n=10 ensayos con p=0.5
binom.pmf(3, n=10, p=0.5)    # → 0.1172  (probabilidad EXACTA de k=3)

binom.pdf(3, n=10, p=0.5)    # AttributeError: las discretas no tienen pdf
```

> En distribuciones discretas `pmf(k)` es una **probabilidad real** (esta en `[0, 1]` y suma 1 sobre todos los `k`), a diferencia de la densidad `pdf` de las continuas.

## Probabilidad acumulada y de cola

```python
from scipy.stats import binom

binom.cdf(3, n=10, p=0.5)    # P(X <= 3) → 0.1719
binom.sf(7, n=10, p=0.5)     # P(X > 7) → 0.0547  (cola derecha)
binom.pmf([4, 5, 6], n=10, p=0.5)   # vectorizado → [0.205, 0.246, 0.205]
```

## Momentos

```python
from scipy.stats import binom

binom.mean(n=10, p=0.5)   # n*p → 5.0
binom.var(n=10, p=0.5)    # n*p*(1-p) → 2.5
binom.std(n=10, p=0.5)    # → 1.581
```

## Muestreo aleatorio

```python
from scipy.stats import binom

binom.rvs(n=10, p=0.5, size=8, random_state=0)
# → array de 8 enteros, cada uno entre 0 y 10 (numero de exitos)
```

## Distribucion congelada

```python
from scipy.stats import binom

B = binom(n=10, p=0.5)   # frozen: 10 ensayos, p=0.5
B.pmf(3)     # → 0.1172
B.cdf(3)     # → 0.1719
B.mean()     # → 5.0
B.rvs(size=1000, random_state=0)
```

## Buenas practicas

1. Usar siempre `.pmf(k)` para la probabilidad de un valor concreto; `.pdf` no existe en discretas.
2. Para "al menos k" usar `sf(k-1)` (o `1 - cdf(k-1)`); para "como mucho k", `cdf(k)`.
3. `k` debe ser entero dentro de `[0, n]`; valores fuera dan `pmf = 0`.
4. No esperar `scale` ni `.fit`: son exclusivos del modelo continuo `rv_continuous`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Llamar `binom.pdf(k, ...)` | es discreta | usar `binom.pmf(k, ...)` |
| Pasar `scale=` | discretas no tienen escala | reparametrizar con `n`, `p`, `loc` |
| `P(X >= k)` con `sf(k)` | `sf(k) = P(X > k)` excluye `k` | usar `sf(k-1)` para incluir `k` |
| `k` no entero | binomial vive en enteros | redondear o revisar el planteamiento |

## Notas relacionadas

- [[rv_continuous]]
- [[scipy.stats.norm]]
- [[scipy.stats.uniform]]
