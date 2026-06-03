---
title: scipy.special.erf — funcion error, ligada a la CDF de la normal
aliases:
  - erf
  - scipy.special.erf
  - funcion error
tags:
  - scipy
  - api/funcion
  - funciones-especiales
lib: scipy
tipo: funcion
mod: scipy.special
retorna: ndarray | float
requiere:
  - numpy
draft: false
---

# scipy.special.erf — funcion error, ligada a la CDF de la normal

Evalua la **funcion error** erf(x) = (2/√π) ∫₀ˣ e^(−t²) dt. Es una funcion sigmoide impar que crece monotonamente de −1 a 1, intimamente ligada a la **distribucion normal**: la CDF gaussiana se expresa como Φ(x) = ½[1 + erf(x/√2)]. Es una **ufunc**: acepta escalares y arrays NumPy y opera **elemento a elemento** (vectorizada), aplicandose directamente sobre un `ndarray`.

> Rango de salida acotado a (−1, 1). En las **colas** (|x| grande) erf(x) se satura a ±1 y `1 - erf(x)` pierde precision por cancelacion: para eso existe `erfc` (complementaria), que calcula 1 − erf(x) de forma estable.

## Firma

```python
scipy.special.erf(x, /, out=None) -> ndarray
# x: array_like (real o complejo)
# out: ndarray opcional donde escribir el resultado
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `float` | erf(x) si `x` es escalar |
| `ndarray` | erf aplicada elemento a elemento si `x` es array |

Valores en (−1, 1); erf(0) = 0, erf(±∞) = ±1, funcion impar erf(−x) = −erf(x).

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Funcion error escalar | `erf(1.0)` |
| Vectorizada sobre array | `erf(np.linspace(-3, 3, 7))` |
| CDF de la normal estandar | `0.5 * (1 + erf(x / np.sqrt(2)))` |
| Cola estable | `erfc(x)` en vez de `1 - erf(x)` |

## Parametros en detalle

### `x` (obligatorio)

Argumento `array_like`. Escalar o `ndarray`. Por ser ufunc respeta broadcasting y se evalua elemento a elemento.

```python
import numpy as np
from scipy.special import erf

erf(0.0)    # → 0.0
erf(1.0)    # → 0.8427007...
erf(np.array([-1.0, 0.0, 1.0]))   # → array([-0.8427,  0.    ,  0.8427])
```

### `out`

`ndarray` opcional preasignado donde depositar el resultado.

## Casos de uso

### Probabilidad gaussiana (CDF de la normal)

```python
import numpy as np
from scipy.special import erf

# P(Z <= 1) para una normal estandar
x = 1.0
Phi = 0.5 * (1 + erf(x / np.sqrt(2)))
Phi    # → 0.8413447...
```

### Difusion (solucion de la ecuacion del calor)

```python
# Perfil de concentracion en difusion 1D: c(x,t) = c0 * erfc(x / (2*sqrt(D t)))
# (erf describe la transicion del frente difusivo)
D, t = 1e-9, 100.0
x = np.array([0.0, 1e-4, 2e-4])
frente = erf(x / (2 * np.sqrt(D * t)))
frente    # → array([0.   , 0.520..., 0.843...])
```

## Buenas practicas

1. Para la CDF normal usa Φ(x) = ½[1 + erf(x/√2)]; el factor 1/√2 es imprescindible.
2. En las colas (`1 - erf`) usa `erfc` para evitar la cancelacion catastrofica de precision.
3. Vectoriza pasando un `ndarray` completo en lugar de iterar.
4. Para invertir (de probabilidad a cuantil) usa `erfinv`, la funcion error inversa.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Olvidar `/√2` en la CDF normal | erf usa escala distinta de Φ | Usar `0.5*(1 + erf(x/np.sqrt(2)))` |
| Precision pobre en la cola | `1 - erf(x)` cancela cifras | Usar `erfc(x)` |
| Esperar rango (0, 1) | erf va de −1 a 1, no de 0 a 1 | Mapear con `0.5*(1+erf(...))` si se quiere prob. |
| Invertir mal | No usar la inversa correcta | Usar `erfinv` / `erfcinv` |

## Limitaciones

- Salida acotada a (−1, 1): se satura numericamente a ±1 para |x| ≳ 6.
- Para colas extremas la version estable es `erfc`, no `1 - erf`.
- La inversion requiere `erfinv`; no existe formula elemental cerrada.

## Notas relacionadas

- [[scipy.special.erfc]]
- [[scipy.special.erfinv]]
- [[scipy.special.gamma]]
