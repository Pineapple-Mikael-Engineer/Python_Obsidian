---
title: scipy.special.factorial — factorial n!, aproximado o exacto
aliases:
  - factorial
  - scipy.special.factorial
  - n factorial
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

# scipy.special.factorial — factorial n!, aproximado o exacto

Calcula el **factorial** n! = 1·2·…·n. A diferencia de `math.factorial` (escalar y siempre exacto), esta funcion **acepta arrays NumPy** y opera **elemento a elemento** (vectorizada) cuando `exact=False`, lo que la integra de forma natural con el resto del ecosistema cientifico. Su comportamiento cambia radicalmente segun el flag `exact`.

> Con `exact=False` (default) calcula n! via la funcion Gamma como `float`: rapido y vectorizable, pero **aproximado** para n grande (y desborda a `inf` desde n ≈ 171). Con `exact=True` devuelve el **entero exacto** de precision arbitraria (Python int), correcto siempre pero mas lento.

## Firma

```python
scipy.special.factorial(n, exact=False) -> ndarray | int
# n: array_like de enteros no negativos
# exact: False -> float via gamma (vectorizable) ; True -> entero exacto
```

## Valor de retorno

| `exact` | Entrada | Tipo retorno | Significado |
|---------|---------|--------------|-------------|
| `False` | escalar | `float` | n! aproximado (via gamma) |
| `False` | array | `ndarray` (float) | n! elemento a elemento |
| `True` | escalar | `int` (Python) | n! exacto, precision arbitraria |

Valores `n` negativos devuelven `0`. Con `exact=False`, `n` no entero se interpola via Gamma.

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Factorial rapido (float) | `factorial(10)` |
| Factorial exacto (int grande) | `factorial(25, exact=True)` |
| Vectorizado sobre array | `factorial(np.arange(6))` |
| Comparar con stdlib | `math.factorial(10)` |

## Parametros en detalle

### `n` (obligatorio)

Entero(s) no negativo(s), `array_like`. Con `exact=False` admite arrays y broadcasting; con `exact=True` se evalua por elementos pero produce objetos `int` de Python.

```python
import numpy as np
from scipy.special import factorial

factorial(5)                  # → 120.0   (float, aproximado pero exacto aqui)
factorial(np.arange(5))       # → array([ 1.,  1.,  2.,  6., 24.])
```

### `exact`

Controla el motor de calculo. `False`: rapido via Gamma, salida `float`, util para arrays y formulas. `True`: producto entero exacto, salida `int` ilimitada, imprescindible cuando n! debe ser exacto.

```python
factorial(25, exact=False)    # → 1.5511210043330986e+25   (aproximado)
factorial(25, exact=True)     # → 15511210043330985984000000   (exacto)
```

## Casos de uso

### Termino de una serie (vectorizado)

```python
import numpy as np
from scipy.special import factorial

# Suma de Taylor de e^x: sum x^n / n!
x, N = 1.0, np.arange(10)
np.sum(x**N / factorial(N))   # → 2.7182818...  (≈ e)
```

### Conteo combinatorio exacto

```python
# Permutaciones de 20 elementos: necesita exactitud entera
factorial(20, exact=True)     # → 2432902008176640000
```

## Buenas practicas

1. Usa `exact=False` (default) dentro de formulas numericas y arrays: es rapido y vectorizable.
2. Usa `exact=True` solo cuando necesites el entero exacto (combinatoria, criptografia, conteos).
3. Para un unico escalar exacto y maxima velocidad, `math.factorial` es la opcion ligera de la stdlib.
4. Para el **doble factorial** n!! (saltando de dos en dos) usa `factorial2`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Entero incorrecto en n grande | `exact=False` aproxima via gamma | Pasar `exact=True` |
| `inf` en factorial grande | Overflow float desde n ≈ 171 | Usar `exact=True` o trabajar en log con `gammaln` |
| Esperar `int` y recibir `float` | Default `exact=False` retorna float | Forzar `exact=True` |
| `math.factorial(array)` falla | stdlib solo acepta escalar | Usar `scipy.special.factorial` con array |

## Limitaciones

- Con `exact=False` desborda a `inf` para n ≳ 171 (float64) y pierde exactitud antes.
- Con `exact=True` es notablemente mas lento y, en arrays, devuelve objetos Python (no un dtype numerico denso).
- Para escalares puros sin NumPy, `math.factorial` suele ser preferible por simplicidad.

## Notas relacionadas

- [[scipy.special.factorial2]]
- [[scipy.special.gamma]]
- [[scipy.special.comb]]
