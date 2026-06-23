---
title: np.random.t — Distribución t de Student
aliases:
  - t
  - random.t
  - np.random.t
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray | float
inplace: false
draft: false
---

# np.random.t — Distribución t de Student

`np.random.t` muestrea de la distribución **t de Student** con `df` grados de libertad. Es simétrica y acampanada como la normal, pero con **colas más pesadas**: aparece al estimar **medias con muestras pequeñas** y varianza poblacional desconocida. Cuando `df` crece converge a la normal estándar (ver [[np.random.standard_normal]]); con `df=1` es la distribución de Cauchy.

> [!tip] Versión moderna
> Esta función usa el **estado global** de `np.random` (el que fija [[np.random.seed]]), hoy considerado *legacy*. La API recomendada crea un generador propio y aislado con [[np.random.default_rng]]:
> ```python
> rng = np.random.default_rng()
> rng.standard_t(df=10, size=(3, 2))   # equivalente moderno
> ```
> Ojo al nombre: en `Generator` el método se llama **`standard_t`**, no `t`. La firma es la misma.

## La idea

Una t con $\nu$ grados de libertad es el cociente de una normal estándar entre la raíz de una chi-cuadrado independiente, escalada por sus grados de libertad. El resultado está **centrado en 0** y simétrico, con colas tanto más gruesas cuanto **menor** es $\nu$.

$$ T = \frac{Z}{\sqrt{V/\nu}}, \qquad Z \sim \mathcal{N}(0,1),\ \ V \sim \chi^2_\nu,\ \ \nu = \texttt{df} $$

$$ f(t) = \frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi}\,\Gamma\!\left(\frac{\nu}{2}\right)} \left(1 + \frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}} \quad\xrightarrow[\nu\to\infty]{}\quad \mathcal{N}(0,1) $$

A más grados de libertad, más se parece a la normal; a menos, más probabilidad de valores extremos.

## Firma

```python
np.random.t(
    df,          # float | array_like: grados de libertad > 0
    size=None,   # int | tuple[int] | None: shape de salida; None → escalar
) -> ndarray | float
```

## Los parámetros en detalle

### `df` — grados de libertad (ν)

Número de grados de libertad, debe ser `> 0`. Controla el grosor de las colas y, con ello, cuántos valores extremos aparecen:

| `df` | Comportamiento |
|------|----------------|
| `1` | Distribución de Cauchy: colas muy pesadas, **sin media ni varianza** definidas |
| `2` | Varianza infinita (media ya definida = 0) |
| `5`–`30` | Colas notablemente más pesadas que la normal |
| `> 100` | Prácticamente indistinguible de la normal estándar |

```python
np.random.t(1, size=3)    # colas extremas (Cauchy)
np.random.t(30, size=3)   # casi normal
```

Acepta escalar o array (broadcasting con `size`).

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un único `float`.

```python
np.random.t(8, size=(3, 2))   # array 3x2 de valores t
```

## size y la forma de salida

La forma del array generado es exactamente `size`; cada muestra es i.i.d. y está centrada en 0. Sin `size`, el retorno es un `float` escalar (no un array `0-d`).

| Llamada | `size` | retorno | shape |
|---|---|---|---|
| `np.random.t(10)` | `None` | `float` | — |
| `np.random.t(10, size=4)` | `int` | `ndarray` | `(4,)` |
| `np.random.t(8, size=(3, 2))` | `tuple` | `ndarray` | `(3, 2)` |

```python
import numpy as np
np.random.seed(0)
np.random.t(10, size=4)   # array([ 1.85,  0.62, -0.40,  0.49])  centradas en 0
```

## Casos de uso

### Distribución nula de un estadístico t

```python
# Contraste de una media con n=10 → df = n-1 = 9
nulo = np.random.t(9, size=10000)
critico = np.percentile(nulo, [2.5, 97.5])   # límites bilaterales al 5%
```

### Simular datos con valores atípicos (colas pesadas)

```python
# Ruido más realista que la normal para outliers ocasionales
ruido = np.random.t(3, size=1000)
```

### Convergencia a la normal con df alto

```python
m = np.random.t(200, size=100000)
m.std()   # ≈ 1, casi indistinguible de la normal estándar
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: df <= 0` | grados de libertad no positivos | usar `df > 0` |
| Media muestral inestable | `df` muy bajo (colas pesadas) | aumentar `df` o usar la mediana |
| Esperar valores acotados | la t no tiene cota; produce extremos | no asumir un rango fijo |
| `AttributeError` con `Generator` | usar `rng.t(...)` | el método moderno es `rng.standard_t(...)` |

## Notas relacionadas

- [[np.random.standard_normal]] — el límite de la t cuando `df → ∞`
- [[np.random.chisquare]] — la chi-cuadrado del denominador de la t
- [[np.random.f]] — cociente de chi-cuadrados (la t² es una F)
- [[np.random.default_rng]] · [[np.random.seed]] · [[concepto_shape]]
