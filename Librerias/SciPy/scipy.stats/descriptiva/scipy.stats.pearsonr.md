---
title: scipy.stats.pearsonr — correlacion lineal de Pearson r y p-valor
aliases:
  - pearsonr
  - scipy.stats.pearsonr
  - correlacion de Pearson
tags:
  - scipy
  - api/funcion
  - estadistica
lib: scipy
tipo: funcion
mod: scipy.stats
retorna: PearsonRResult
requiere:
  - numpy
draft: false
---

# scipy.stats.pearsonr — correlacion lineal de Pearson r y p-valor

Calcula el **coeficiente de correlacion lineal de Pearson** `r` entre dos vectores `x` e `y` de igual longitud, junto con un **p-valor** que contrasta la hipotesis nula de **no correlacion lineal**. El valor `r ∈ [-1, 1]`: `+1` relacion lineal positiva perfecta, `-1` negativa perfecta, `0` ausencia de relacion **lineal**. Mide solo la componente **lineal** de la asociacion, es **sensible a outliers** y el p-valor asume **normalidad bivariada** de los datos. Devuelve un objeto-resultado con `statistic` y `pvalue`, tambien **desempaquetable** como `(r, p)`.

> `r = 0` no significa independencia: una relacion fuerte pero **no lineal** (p. ej. parabolica) puede dar `r` cercano a 0. Para relaciones monotonas no lineales o datos con outliers, contrastar con la correlacion de Spearman.

## Firma

```python
scipy.stats.pearsonr(
    x,                       # array_like 1D: primera variable
    y,                       # array_like 1D: segunda variable (misma longitud que x)
    *,
    alternative='two-sided', # str: 'two-sided' | 'greater' | 'less'
    method=None,             # objeto de remuestreo opcional (permutaciones/bootstrap)
) -> PearsonRResult
```

## Valor de retorno

Objeto **PearsonRResult**. Acceso por atributo o desempaquetado posicional `(r, p)`.

| Campo | Tipo | Significado |
|-------|------|-------------|
| `statistic` | `float` | Coeficiente de Pearson `r ∈ [-1, 1]` |
| `pvalue` | `float` | p-valor del contraste (H0: no hay correlacion lineal) |

Ademas, el objeto ofrece el metodo `confidence_interval(confidence_level=0.95)` para el intervalo de confianza de `r`.

```python
res = pearsonr(x, y)
res.statistic, res.pvalue        # acceso por atributo
r, p = pearsonr(x, y)            # desempaquetado (r, p)
res.confidence_interval()        # IC del coeficiente
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Correlacion y p-valor | `r, p = pearsonr(x, y)` |
| Objeto completo | `res = pearsonr(x, y)` |
| Contraste unilateral (r>0) | `pearsonr(x, y, alternative='greater')` |
| Contraste unilateral (r<0) | `pearsonr(x, y, alternative='less')` |
| Intervalo de confianza de r | `pearsonr(x, y).confidence_interval()` |

## Parametros en detalle

### `x`, `y` (obligatorios)

Dos secuencias 1D de **igual longitud** (minimo 2 elementos). Son las dos variables cuya asociacion lineal se mide. El orden no afecta a `r` (es simetrico).

```python
import numpy as np
from scipy.stats import pearsonr

x = np.array([10, 20, 30, 40, 50])
y = np.array([12, 19, 33, 38, 51])      # crece junto con x
r, p = pearsonr(x, y)
r    # → 0.997...   (relacion lineal positiva casi perfecta)
p    # → muy pequeño  (se rechaza H0: hay correlacion)
```

### `alternative`

Define la hipotesis alternativa del p-valor: `'two-sided'` (defecto, `r != 0`), `'greater'` (`r > 0`) o `'less'` (`r < 0`). Solo cambia el p-valor, no el valor de `r`.

### `method`

Permite estimar el p-valor por **remuestreo** (permutaciones o bootstrap) en vez de la formula parametrica, util cuando no se cumple la normalidad. Si es `None`, se usa la aproximacion analitica clasica.

## Casos de uso

### Asociacion lineal entre dos magnitudes fisicas

```python
import numpy as np
from scipy.stats import pearsonr

temperatura = np.array([15, 18, 21, 24, 27, 30])
resistencia = np.array([100, 104, 109, 112, 118, 121])
r, p = pearsonr(temperatura, resistencia)
r    # → ~0.998   (la resistencia sube linealmente con la temperatura)
```

### Detectar que r=0 no implica independencia

```python
x = np.linspace(-3, 3, 50)
y = x**2                         # relacion fuerte, pero NO lineal
r, p = pearsonr(x, y)
r    # → ~0.0   (Pearson no ve la parabola)
```

Aqui la asociacion es total pero simetrica; Pearson la cuantifica como nula porque solo mide linealidad.

### Reportar r junto a su intervalo de confianza

```python
res = pearsonr(x, y)
res.statistic                    # estimacion puntual de r
res.confidence_interval(0.95)    # rango plausible de r al 95%
```

## Buenas practicas

1. Inspecciona un diagrama de dispersion antes de fiarte de `r`: detecta no linealidad y outliers que el numero no revela.
2. Reporta siempre `r` **y** `pvalue` juntos; un `r` alto con `n` pequeño puede no ser significativo.
3. Acompaña `r` de su `confidence_interval()` para comunicar incertidumbre.
4. Si hay outliers o la relacion es monotona no lineal, compara con la correlacion de Spearman.
5. Si los datos no son aproximadamente normales, usa `method` con permutaciones para un p-valor mas robusto.
6. Recuerda: correlacion no implica causalidad.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Interpretar `r=0` como independencia | Pearson solo mide linealidad | Graficar; usar `spearmanr` para relacion monotona |
| Confiar en `r` con outliers | Pearson es muy sensible a valores extremos | Inspeccionar dispersion; usar Spearman |
| `ValueError` por longitudes distintas | `x` e `y` deben tener igual tamaño | Alinear/recortar los arrays |
| Tomar p-valor pequeño como prueba de causa | Significancia no es causalidad | Interpretar con cautela el diseño |
| Esperar una tupla y solo una tupla | Hoy devuelve un objeto (tambien desempaquetable) | Usar `r, p = pearsonr(...)` o `res.statistic`/`res.pvalue` |
| p-valor poco fiable con n muy pequeño o no normal | Asume normalidad bivariada | Usar `method` de permutaciones |

## Limitaciones

- Mide **solo** asociacion lineal; ignora relaciones curvas o monotonas no lineales.
- **Sensible a outliers**: un punto extremo puede inflar o anular `r`.
- El p-valor parametrico **asume normalidad bivariada**; poco fiable fuera de ese supuesto.
- Opera sobre **dos vectores 1D**; no produce directamente una matriz de correlaciones (para eso, `numpy.corrcoef` o `spearmanr`).
- Requiere varianza no nula en ambas variables; un vector constante da resultado indefinido.

## Notas relacionadas

- [[scipy.stats.spearmanr]]
- [[scipy.stats.linregress]]
- [[scipy.stats.describe]]
