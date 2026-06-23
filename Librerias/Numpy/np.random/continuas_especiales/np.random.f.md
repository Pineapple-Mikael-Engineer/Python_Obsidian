---
title: np.random.f — Distribución F de Snedecor (cociente de chi-cuadrado)
aliases:
  - f
  - random.f
  - np.random.f
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.f — Distribución F de Snedecor

Genera muestras de la distribución **F de Snedecor**, definida como el **cociente de dos chi-cuadrado independientes**, cada una dividida por sus grados de libertad. Es siempre no negativa y asimétrica a la derecha. Es la distribución de referencia en **ANOVA** y en los contrastes de **comparación de varianzas** entre dos poblaciones. Está construida a partir de la [[np.random.chisquare|distribución chi-cuadrado]].

## La idea

Si $U \sim \chi^2(d_1)$ y $V \sim \chi^2(d_2)$ son chi-cuadrado independientes, con $d_1 = $ `dfnum` y $d_2 = $ `dfden`, entonces:

$$ F \;=\; \frac{U/d_1}{V/d_2} \;\sim\; F(d_1, d_2) $$

Su densidad sobre `x ≥ 0` depende de los **dos parámetros de forma** `dfnum` y `dfden`:

$$ f(x;d_1,d_2) \;\propto\; \frac{x^{\,d_1/2-1}}{\left(d_1\,x + d_2\right)^{(d_1+d_2)/2}}, \qquad x \ge 0 $$

Propiedades clave:

- Los valores son siempre **no negativos** y la cola superior es larga (asimetría a la derecha).
- La media (para $d_2 > 2$) es $\dfrac{d_2}{d_2-2}$, cercana a 1 cuando `dfden` es grande.
- A mayor `dfden`, la masa se **concentra alrededor de 1**; a `dfden` bajo, colas pesadas.

> [!tip] Versión moderna
> La API recomendada desde NumPy 1.17 usa un generador explícito en vez del estado global. Ver [[np.random.default_rng]].
> ```python
> rng = np.random.default_rng()
> rng.f(dfnum=5, dfden=20, size=1000)
> ```

## Firma

```python
np.random.f(dfnum, dfden, size=None) -> ndarray | float
```

## Los parámetros en detalle

### `dfnum` — grados de libertad del numerador

Grados de libertad de la chi-cuadrado del numerador (`> 0`). En ANOVA corresponde a los grados de libertad **entre grupos**. Acepta escalar o array (broadcasting con `dfden` y `size`).

```python
np.random.f(1, 30)    # numerador con 1 g.l.
np.random.f(10, 30)   # numerador con 10 g.l.
```

### `dfden` — grados de libertad del denominador

Grados de libertad de la chi-cuadrado del denominador (`> 0`). En ANOVA corresponde a los grados de libertad **dentro de los grupos** (residual). A mayor `dfden`, la distribución se concentra alrededor de 1.

```python
np.random.f(5, 5)     # colas pesadas, mucha dispersión
np.random.f(5, 100)   # más concentrada cerca de 1
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un escalar.

```python
np.random.f(5, 20, size=(2, 3))   # array 2×3 de valores F
```

## size y la forma de salida

Devuelve reales no negativos, asimétricos a la derecha.

| Llamada | Distribución | Shape | dtype |
|---------|--------------|-------|-------|
| `np.random.f(5, 20)` | F(5, 20) | `()` escalar | `float` |
| `np.random.f(5, 20, 4)` | F(5, 20) | `(4,)` | `float64` |
| `np.random.f(2, 27, 10000)` | F(2, 27) | `(10000,)` | `float64` |
| `np.random.f(5, 20, (2, 3))` | F(5, 20) | `(2, 3)` | `float64` |

```python
import numpy as np
np.random.seed(0)
np.random.f(dfnum=5, dfden=20, size=4)
# array([1.21, 0.44, 2.07, 0.68])
```

## Casos de uso

### Estadístico F simulado para ANOVA

```python
# Distribución nula de F con 3 grupos (dfnum=2) y 27 observaciones residuales
nulo = np.random.f(2, 27, size=10000)
umbral = np.percentile(nulo, 95)   # valor crítico al 5%
```

### Comparación de dos varianzas muestrales

```python
# Bajo H0 (varianzas iguales), el cociente s1^2 / s2^2 sigue una F
ratios = np.random.f(9, 9, size=5000)   # dos muestras de n=10
```

### Construirla a mano desde dos chi-cuadrado

```python
# F(d1, d2) = (U/d1) / (V/d2) con U, V chi-cuadrado independientes
d1, d2 = 5, 20
U = np.random.chisquare(d1, size=10000)
V = np.random.chisquare(d2, size=10000)
F = (U / d1) / (V / d2)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: dfnum <= 0` | grados de libertad no positivos | usar `dfnum > 0` y `dfden > 0` |
| Valores enormes inesperados | `dfden` muy bajo (cola pesada) | aumentar `dfden` o revisar el modelo |
| Esperar valores negativos | la F siempre es `>= 0` | no aplicar a datos con signo |
| `TypeError` con `size` | pasar float como tamaño | usar `int` o `tuple` de enteros |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.default_rng]]
- [[np.random.chisquare]]
- [[np.random.t]]
- [[np.random.seed]]
