---
title: scipy.stats.uniform — distribucion uniforme continua
aliases:
  - uniform
  - scipy.stats.uniform
  - distribucion uniforme
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

# scipy.stats.uniform — distribucion uniforme continua

Objeto-distribucion **uniforme continua**, instancia de `rv_continuous`. Asigna densidad constante en un intervalo y cero fuera de el. El intervalo **no** se define con extremos `a, b` directos, sino con los parametros universales `loc` y `scale`: el soporte es `[loc, loc + scale]`.

| Parametro | Significado | Defecto |
|-----------|-------------|---------|
| `loc` | extremo inferior del intervalo | `0` |
| `scale` | **ancho** del intervalo (no el extremo superior) | `1` |

Por defecto (`loc=0`, `scale=1`) es la **uniforme estandar** en `[0, 1]`. Para un intervalo `[a, b]` se usa `loc=a`, `scale=b-a`. La API de metodos es la comun a las distribuciones continuas (ver [[rv_continuous]]).

## El intervalo es [loc, loc + scale]

```python
from scipy.stats import uniform

# Uniforme en [2, 5]:  a=2, b=5  ->  loc=2, scale=5-2=3
uniform.pdf(3, loc=2, scale=3)   # densidad constante 1/3 → 0.3333
uniform.pdf(6, loc=2, scale=3)   # fuera del intervalo → 0.0
```

> Error tipico: pasar `scale=5` pensando que es el extremo superior. `scale` es el **ancho**; para `[2, 5]` el ancho es `3`.

## Consultas basicas

```python
from scipy.stats import uniform

uniform.cdf(0.25)        # en [0,1]: P(X <= 0.25) → 0.25  (lineal)
uniform.cdf(4, loc=2, scale=3)   # en [2,5]: (4-2)/3 → 0.6667
uniform.ppf(0.5, loc=2, scale=3) # mediana = centro → 3.5
uniform.mean(loc=2, scale=3)     # (loc + loc+scale)/2 → 3.5
```

## Muestreo aleatorio

```python
from scipy.stats import uniform

uniform.rvs(size=5, random_state=0)            # 5 valores en [0, 1)
uniform.rvs(loc=2, scale=3, size=5, random_state=0)  # 5 valores en [2, 5)
```

## Distribucion congelada

```python
from scipy.stats import uniform

U = uniform(loc=2, scale=3)   # frozen: uniforme en [2, 5]
U.pdf(3)     # → 0.3333
U.cdf(4)     # → 0.6667
U.rvs(size=1000, random_state=0)
```

## Buenas practicas

1. Para un intervalo `[a, b]` usar siempre `loc=a`, `scale=b-a`; el `scale` es el ancho, no el limite superior.
2. La densidad en el soporte es constante `1/scale`; comprobacion rapida de que el intervalo es correcto.
3. Para muestreo simple en `[0,1]` basta `uniform.rvs(size=...)`; equivale a `numpy.random` pero con la API de distribuciones.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar `scale=b` en vez de `b-a` | `scale` es el ancho | `scale = b - a` |
| Esperar `pdf` distinta dentro del intervalo | la uniforme es plana | densidad constante `1/scale` |
| Creer que `loc`/`scale` son `a`/`b` | parametrizacion por desplazamiento+ancho | recordar `[loc, loc+scale]` |

## Notas relacionadas

- [[rv_continuous]]
- [[scipy.stats.norm]]
- [[scipy.stats.binom]]
