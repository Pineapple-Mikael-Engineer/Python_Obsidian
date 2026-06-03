---
title: scipy.special.comb — coeficiente binomial C(N, k)
aliases:
  - comb
  - scipy.special.comb
  - coeficiente binomial
tags:
  - scipy
  - api/funcion
  - funciones-especiales
lib: scipy
tipo: funcion
mod: scipy.special
retorna: ndarray | float | int
requiere:
  - numpy
draft: false
---

# scipy.special.comb — coeficiente binomial C(N, k)

Calcula el **coeficiente binomial** C(N, k) = N! / (k!(N−k)!): el numero de maneras de elegir `k` elementos entre `N` **sin importar el orden**. Como `factorial`, **acepta arrays NumPy** y opera **elemento a elemento** (vectorizada) cuando `exact=False`. Su comportamiento depende de los flags `exact` y `repetition`.

> Con `exact=False` (default) calcula via Gamma como `float`: rapido y vectorizable, pero aproximado para valores grandes. Con `exact=True` devuelve el **entero exacto** (Python int), correcto siempre pero mas lento y solo escalar.

## Firma

```python
scipy.special.comb(N, k, *, exact=False, repetition=False) -> ndarray | int
# N, k: array_like de enteros no negativos
# exact: False -> float via gamma (vectorizable) ; True -> entero exacto
# repetition: True -> combinaciones con repeticion
```

## Valor de retorno

| `exact` | Entrada | Tipo retorno | Significado |
|---------|---------|--------------|-------------|
| `False` | escalar | `float` | C(N,k) aproximado (via gamma) |
| `False` | array | `ndarray` (float) | C(N,k) elemento a elemento |
| `True` | escalar | `int` (Python) | C(N,k) exacto, precision arbitraria |

Devuelve `0` cuando `k > N` (sin repeticion) o ante argumentos invalidos.

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Binomial rapido (float) | `comb(10, 3)` |
| Binomial exacto (int) | `comb(50, 25, exact=True)` |
| Vectorizado sobre array | `comb(10, np.arange(11))` |
| Con repeticion | `comb(5, 3, repetition=True)` |

## Parametros en detalle

### `N`, `k` (obligatorios)

Enteros no negativos, `array_like`. Con `exact=False` admiten arrays y broadcasting (`N` y `k` se combinan por broadcasting).

```python
import numpy as np
from scipy.special import comb

comb(10, 3)                 # → 120.0
comb(10, np.arange(4))      # → array([  1.,  10.,  45., 120.])
```

### `exact`

`False`: float via Gamma, vectorizable, rapido pero aproximado para N grande. `True`: entero exacto de precision arbitraria, solo para entradas escalares.

```python
comb(50, 25, exact=False)   # → 1.2641060643880958e+14   (aproximado)
comb(50, 25, exact=True)    # → 126410606437752          (exacto)
```

### `repetition`

Con `repetition=True` cuenta **combinaciones con repeticion**: C(N+k−1, k), o sea elegir `k` de `N` tipos permitiendo repetir.

```python
# Cuantas formas de elegir 3 bolas de 5 colores, con repeticion
comb(5, 3, repetition=True)   # → 35.0
```

## Casos de uso

### Probabilidad binomial

```python
import numpy as np
from scipy.special import comb

# P(X = k) en Binomial(n, p): C(n,k) p^k (1-p)^(n-k)
n, k, p = 10, 3, 0.4
prob = comb(n, k) * p**k * (1 - p)**(n - k)
prob    # → 0.2149908...
```

### Conteo combinatorio exacto

```python
# Manos de poker: C(52, 5) exacto
comb(52, 5, exact=True)   # → 2598960
```

## Buenas practicas

1. Usa `exact=False` (default) en formulas y arrays de probabilidad: rapido y vectorizable.
2. Usa `exact=True` cuando necesites el entero exacto (conteos, combinatoria pura).
3. Para combinaciones con repeticion activa `repetition=True` en vez de reescribir la formula.
4. Para **permutaciones** (donde el orden si importa) usa `perm`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Resultado no entero | `exact=False` retorna float aproximado | Usar `exact=True` |
| Imprecision en N grande | Cociente de Gammas enormes | Usar `exact=True` |
| Contar permutaciones con `comb` | `comb` ignora el orden | Usar `perm` |
| `exact=True` con arrays | Modo exacto es escalar | Iterar o usar `exact=False` |
| Olvidar repeticion | Default `repetition=False` | Pasar `repetition=True` |

## Limitaciones

- Con `exact=False` pierde exactitud y puede desbordar para N muy grande.
- `exact=True` opera sobre escalares, no vectoriza sobre arrays.
- Cuenta combinaciones (sin orden); para ordenado usar `perm`.

## Notas relacionadas

- [[scipy.special.perm]]
- [[scipy.special.factorial]]
- [[scipy.special.gamma]]
