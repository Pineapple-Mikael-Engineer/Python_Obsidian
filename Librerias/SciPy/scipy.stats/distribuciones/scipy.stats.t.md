---
title: scipy.stats.t — distribucion t de Student
aliases:
  - t de Student
  - scipy.stats.t
  - distribucion t
tags:
  - scipy
  - api/objeto
  - estadistica
lib: scipy
tipo: objeto
mod: scipy.stats
requiere:
  - numpy
draft: false
---

# scipy.stats.t — distribucion t de Student

Objeto-distribucion de la **t de Student**, instancia de `rv_continuous`. Simetrica y centrada en 0 como la normal, pero con **colas mas pesadas**: asigna mas probabilidad a valores extremos. Esa anchura extra modela la incertidumbre de estimar la varianza con **muestras pequeñas**. Cuando los grados de libertad crecen, `t` **tiende a la normal** (`df -> inf`).

| Parametro | Significado | Notas |
|-----------|-------------|-------|
| `df` | grados de libertad (parametro de forma) | en un t-test suele ser `n - 1` |
| `loc` | desplazamiento | defecto `0` |
| `scale` | escala | defecto `1` |

La API de metodos es la comun a las distribuciones continuas (ver [[rv_continuous]]); el parametro de forma `df` va **primero** en cada llamada.

## Colas mas pesadas que la normal

```python
from scipy.stats import t, norm

t.pdf(3, df=3)     # densidad en x=3 con pocos df → ~0.0114
norm.pdf(3)        # la normal asigna menos → ~0.0044  (t tiene mas cola)
```

## Valor critico para intervalos de confianza

El uso estrella: el cuantil `t.ppf(1 - alpha/2, df=n-1)` da el multiplicador del intervalo de confianza de la media con varianza desconocida.

```python
from scipy.stats import t

n = 10
t.ppf(0.975, df=n - 1)   # valor critico al 95% con 9 df → 2.262
# IC 95% de la media:  media +- t_crit * (s / sqrt(n))
```

```python
from scipy.stats import t

t.interval(0.95, df=9)   # intervalo central al 95% → (-2.262, 2.262)
t.sf(2.0, df=9)          # cola derecha (p-valor de una cola) → 0.0385
```

## Convergencia a la normal

```python
from scipy.stats import t, norm

t.ppf(0.975, df=5)      # → 2.571   (cola ancha, pocos df)
t.ppf(0.975, df=100)    # → 1.984   (ya casi normal)
norm.ppf(0.975)         # → 1.960   (limite df -> inf)
```

## Distribucion congelada y muestreo

```python
from scipy.stats import t

T = t(df=9)             # frozen: t con 9 grados de libertad
T.ppf(0.975)            # → 2.262
T.rvs(size=1000, random_state=0)   # 1000 muestras
```

## Buenas practicas

1. En t-tests de una muestra y en IC de la media, usar `df = n - 1`.
2. Para p-valores de una cola usar `sf`; para dos colas, `2 * sf(|t_obs|, df)`.
3. Con `df` grande (> ~30) la diferencia con la normal es minima; aun asi `t` es la eleccion correcta cuando la varianza poblacional es desconocida.
4. El parametro `df` es de forma: va antes que `loc`/`scale` en cada llamada.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usar la normal con n pequeño | colas demasiado finas | usar `t` con `df=n-1` |
| Olvidar `df` | es obligatorio (parametro de forma) | `t.ppf(0.975, df=n-1)` |
| p-valor de dos colas a medias | usar solo `sf` da una cola | `2 * t.sf(abs(t_obs), df)` |

## Notas relacionadas

- [[rv_continuous]]
- [[scipy.stats.norm]]
- [[scipy.stats.chi2]]
