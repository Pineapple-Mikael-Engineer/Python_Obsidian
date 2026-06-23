---
title: np.random.beta — Muestras de la distribución beta
aliases: [beta, random.beta, np.random.beta]
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

# np.random.beta — Muestras de la distribución beta

Genera muestras de una distribución **Beta(a, b)**, una variable continua acotada en el intervalo `[0, 1]`. Por vivir siempre entre 0 y 1, es la herramienta natural para modelar **proporciones, tasas y probabilidades** (CTR, conversión, fiabilidad). En inferencia bayesiana es la *prior conjugada* de la binomial: si partes de una Beta y observas éxitos/fracasos, la posterior vuelve a ser una Beta, lo que la convierte en el ladrillo clásico de los modelos sobre tasas.

## La idea

La densidad de la Beta sobre `x ∈ [0, 1]` depende de los dos **parámetros de forma** `a` y `b`:

$$ f(x;a,b) \;=\; \frac{x^{\,a-1}\,(1-x)^{\,b-1}}{B(a,b)} \;\propto\; x^{\,a-1}\,(1-x)^{\,b-1}, \qquad 0 \le x \le 1 $$

donde $B(a,b)$ es la función beta, que solo normaliza el área a 1. La intuición de los exponentes:

- `a` tira de la masa **hacia 1** (cuantos más "éxitos", más cerca del 1).
- `b` tira de la masa **hacia 0** (cuantos más "fracasos", más cerca del 0).
- La media es $\mathbb{E}[X] = \dfrac{a}{a+b}$ y la "confianza" (concentración) crece con $a+b$.

Casos notables: `Beta(1, 1)` es la **uniforme** en `[0,1]`; `Beta(a, a)` es simétrica en torno a `0.5`; con `a, b < 1` la densidad tiene forma de **U** (masa en los extremos).

> [!tip] Versión moderna
> La API recomendada desde NumPy 1.17 usa un generador explícito en vez del estado global. Ver [[np.random.default_rng]].
> ```python
> rng = np.random.default_rng()
> rng.beta(a=2, b=5, size=1000)
> ```

## Firma

```python
np.random.beta(a, b, size=None) -> ndarray | float
```

## Los parámetros en detalle

### `a` — forma alfa (peso hacia 1)

Análogo a "éxitos + 1" en la interpretación bayesiana. A mayor `a`, la masa se desplaza hacia 1. Debe ser estrictamente `> 0`. Acepta escalar o array (se combina por [[concepto_broadcasting|broadcasting]] con `b` y `size`).

```python
np.random.beta(0.5, 0.5)   # forma en U: masa en los extremos 0 y 1
np.random.beta(5, 1)       # fuertemente sesgada hacia 1
```

### `b` — forma beta (peso hacia 0)

Análogo a "fracasos + 1". A mayor `b`, la masa se desplaza hacia 0. Debe ser `> 0`.

```python
np.random.beta(1, 5)       # sesgada hacia 0
np.random.beta(2, 2)       # simétrica acampanada centrada en 0.5
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del array; `None` devuelve un escalar.

```python
np.random.beta(2, 2, size=1000)    # vector (1000,)
np.random.beta(2, 2, size=(3, 3))  # matriz (3, 3)
```

## size y la forma de salida

Devuelve reales en `[0, 1]` con la densidad anterior. La media tiende a `a/(a+b)` y la masa se concentra a medida que crece `a+b`.

| Llamada | Distribución | Shape | dtype |
|---------|--------------|-------|-------|
| `np.random.beta(2, 5)` | Beta(2, 5) | `()` escalar | `float` |
| `np.random.beta(2, 5, 4)` | Beta(2, 5) | `(4,)` | `float64` |
| `np.random.beta(1, 1, 10)` | uniforme `[0,1]` | `(10,)` | `float64` |
| `np.random.beta(8, 2, (2, 2))` | Beta(8, 2), masa cerca de 1 | `(2, 2)` | `float64` |

```python
import numpy as np
np.random.seed(0)
np.random.beta(a=2, b=5, size=3)
# array([0.34, 0.19, 0.41])  → media tiende a 2/(2+5) ≈ 0.286
```

Si `a` o `b` son arrays, su forma se combina por broadcasting con `size`.

## Casos de uso

### Posterior bayesiana de una tasa de conversión

```python
# Prior Beta(1,1) + 30 conversiones de 200 visitas → posterior Beta(31, 171)
a_post, b_post = 1 + 30, 1 + (200 - 30)
muestras = np.random.beta(a_post, b_post, size=10000)
muestras.mean()                       # ≈ 0.153, estimación de la tasa
np.percentile(muestras, [2.5, 97.5])  # intervalo creíble del 95%
```

### Generar pesos aleatorios acotados

```python
# Fracciones de mezcla entre 0 y 1, sesgadas hacia valores bajos
pesos = np.random.beta(2, 5, size=100)
```

### Prior no informativa

```python
# Beta(1,1) es exactamente la uniforme: punto de partida neutro
np.random.beta(1, 1, size=1000)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Media al revés | Intercambiar `a` y `b` | `a` empuja hacia 1, `b` hacia 0 |
| `ValueError: a <= 0` | Parámetros no positivos | Garantizar `a > 0` y `b > 0` |
| Esperar valores fuera de `[0,1]` | La beta siempre vive en `[0,1]` | Reescalar si necesitas otro rango |
| Forma en U inesperada | Usar `a < 1` y `b < 1` | Subir ambos por encima de 1 |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.default_rng]]
- [[np.random.gamma]]
- [[np.random.rand]]
- [[np.random.seed]]
