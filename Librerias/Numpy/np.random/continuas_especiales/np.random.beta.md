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

Modela **proporciones y probabilidades**: variables continuas acotadas en el intervalo `[0, 1]`. Sus dos parámetros de forma `a` y `b` se interpretan, en el caso clásico, como "éxitos" y "fracasos" previos. Es la base de la inferencia bayesiana sobre tasas (CTR, conversión, fiabilidad) porque es la prior conjugada de la binomial.

## Firma de la función

```python
np.random.beta(
    a,
    b,
    size=None
) -> ndarray | float
```

## Valor de retorno

Devuelve reales en `[0, 1]` con densidad `f(x) ∝ x^(a−1)·(1−x)^(b−1)`. La media tiende a `a/(a+b)`; cuanto mayor es `a+b`, más concentrada está la masa alrededor de esa media.

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `beta(2, 5)` con `size=None` | `float` en `[0,1]` | `0.27` |
| `beta(2, 5, size=4)` | `ndarray (4,)` | `[0.31, 0.18, 0.44, 0.22]` |
| `beta(1, 1)` | uniforme en `[0,1]` | distribución plana |
| `beta(8, 2, size=(2,2))` | `ndarray (2,2)` | masa cerca de 1 |

```python
import numpy as np
np.random.seed(0)
np.random.beta(a=2, b=5, size=3)
# array([0.34, 0.19, 0.41])  → media tiende a 2/(2+5) ≈ 0.286
```

## Parámetros en detalle

### `a` — forma alfa (peso hacia 1)

Análogo a "éxitos + 1". A mayor `a`, la masa se desplaza hacia 1. Debe ser `> 0`.

```python
np.random.beta(0.5, 0.5)   # forma en U: masa en los extremos 0 y 1
np.random.beta(5, 1)       # sesgada hacia 1
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

## Casos de uso

### Posterior bayesiana de una tasa de conversión

```python
# Prior Beta(1,1) + 30 conversiones de 200 visitas → posterior
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

## Buenas prácticas

1. Interpreta la media como `a/(a+b)` y la "confianza" como `a+b` (mayor suma → menos dispersión).
2. `beta(1, 1)` es exactamente la uniforme en `[0,1]`; úsalo como prior no informativa.
3. Para proporciones que no toquen 0 ni 1 evita `a<1` o `b<1` (densidad infinita en los extremos).
4. Fija la semilla con [[np.random.seed]] para reproducir simulaciones.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Media al revés | Intercambiar `a` y `b` | `a` empuja hacia 1, `b` hacia 0 |
| `ValueError: a <= 0` | Parámetros no positivos | Garantizar `a > 0` y `b > 0` |
| Valores fuera de `[0,1]` esperados | La beta siempre vive en `[0,1]` | Reescalar si necesitas otro rango |
| Forma en U inesperada | Usar `a<1` y `b<1` | Subir ambos por encima de 1 |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.gamma]]
- [[np.random.rand]]
- [[np.random.seed]]
