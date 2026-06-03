---
title: scipy.stats.chi2 — distribucion chi-cuadrado
aliases:
  - chi2
  - scipy.stats.chi2
  - chi-cuadrado
  - ji-cuadrado
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

# scipy.stats.chi2 — distribucion chi-cuadrado

Objeto-distribucion **chi-cuadrado** (ji-cuadrado), instancia de `rv_continuous`. Es la distribucion de la **suma de cuadrados de variables normales estandar independientes**. Tiene **soporte no negativo** (solo `x >= 0`) y es **asimetrica a la derecha**; al crecer `df` se vuelve mas simetrica y se aproxima a una normal.

| Parametro | Significado | Notas |
|-----------|-------------|-------|
| `df` | grados de libertad (parametro de forma) | suma de `df` cuadrados normales |
| `loc` | desplazamiento | defecto `0` (normalmente no se toca) |
| `scale` | escala | defecto `1` |

Usos tipicos: **tests de bondad de ajuste** y de independencia (tablas de contingencia), e **inferencia sobre varianzas**. La API de metodos es la comun a las distribuciones continuas (ver [[rv_continuous]]).

## Soporte no negativo

```python
from scipy.stats import chi2

chi2.pdf(-1, df=4)   # fuera del soporte → 0.0
chi2.pdf(3, df=4)    # densidad valida → ~0.168
chi2.mean(df=4)      # media = df → 4.0  (la media de chi2 es df)
chi2.var(df=4)       # varianza = 2*df → 8.0
```

## Valor critico (cola derecha)

En tests chi-cuadrado se rechaza la hipotesis nula cuando el estadistico supera un valor critico de la **cola derecha**. Se obtiene con `ppf(1 - alpha)` o, mas directo, con `isf(alpha)`.

```python
from scipy.stats import chi2

chi2.ppf(0.95, df=4)   # valor critico al 5% con 4 df → 9.488
chi2.isf(0.05, df=4)   # mismo valor por la cola derecha → 9.488
```

## p-valor de un test

El p-valor es la probabilidad en la cola derecha del estadistico observado:

```python
from scipy.stats import chi2

estadistico = 11.2
p = chi2.sf(estadistico, df=4)   # P(X > 11.2) → 0.0244  (cola derecha = p-valor)
```

## Distribucion congelada y muestreo

```python
from scipy.stats import chi2

C = chi2(df=4)          # frozen: chi2 con 4 grados de libertad
C.ppf(0.95)             # → 9.488
C.rvs(size=1000, random_state=0)   # 1000 muestras (todas >= 0)
```

## Buenas practicas

1. Para valores criticos de un test usar la cola derecha: `isf(alpha)` o `ppf(1 - alpha)`.
2. El p-valor de un test chi-cuadrado es `sf(estadistico, df)`, no `cdf`.
3. Recordar `mean = df` y `var = 2*df`: util como comprobacion rapida.
4. Normalmente no se toca `loc`/`scale`; el `df` correcto depende del test (bondad de ajuste: `categorias - 1 - parametros estimados`).

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usar `cdf` como p-valor | el p-valor es la cola derecha | usar `sf(estadistico, df)` |
| Evaluar en valores negativos | soporte es `x >= 0` | la densidad ahi es 0 por definicion |
| `df` equivocado en bondad de ajuste | no se descontaron parametros estimados | `df = k - 1 - m` |

## Notas relacionadas

- [[rv_continuous]]
- [[scipy.stats.norm]]
- [[scipy.stats.t]]
