---
title: scipy.special.gamma — funcion Gamma, generalizacion del factorial
aliases:
  - gamma
  - scipy.special.gamma
  - funcion Gamma
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

# scipy.special.gamma — funcion Gamma, generalizacion del factorial

Evalua la **funcion Gamma** Γ(z), la extension del factorial a numeros reales y complejos. Para enteros positivos cumple Γ(n+1) = n!, de modo que interpola "factoriales" en valores no enteros. Es una **ufunc**: acepta escalares, arrays NumPy y complejos, y opera **elemento a elemento** (vectorizada), por lo que se aplica directamente a un `ndarray` sin bucles.

> Crece muy rapido (mas que exponencial): Γ(171) ya desborda el rango de `float64` y devuelve `inf`. Para magnitudes grandes trabaja con el logaritmo via `gammaln` y opera en escala log.

## Firma

```python
scipy.special.gamma(z, /, out=None) -> ndarray
# z: array_like (real o complejo)
# out: ndarray opcional donde escribir el resultado
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `float` | Γ(z) si `z` es escalar real |
| `complex` | Γ(z) si `z` es complejo |
| `ndarray` | Γ aplicada elemento a elemento si `z` es array |

Devuelve `inf` por overflow para `z` grande, y `±inf`/`nan` en los polos (enteros ≤ 0).

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Factorial de un entero | `gamma(n + 1)` |
| Gamma en un real | `gamma(0.5)` |
| Vectorizada sobre array | `gamma(np.array([1, 2, 3, 4]))` |
| Gamma compleja | `gamma(1 + 1j)` |

## Parametros en detalle

### `z` (obligatorio)

Argumento `array_like`. Puede ser escalar, `ndarray` o complejo. Al ser ufunc se evalua elemento a elemento y respeta broadcasting.

```python
import numpy as np
from scipy.special import gamma

gamma(5)              # → 24.0          (= 4!)
gamma(0.5)            # → 1.7724539...  (= sqrt(pi))
gamma(np.arange(1, 6))  # → array([ 1.,  1.,  2.,  6., 24.])
```

### `out`

`ndarray` opcional preasignado donde depositar el resultado, util para reusar memoria en bucles de calculo intensivo.

## Casos de uso

### Factorial continuo en valores no enteros

```python
# "factorial" de 2.5 = Gamma(3.5)
gamma(3.5)    # → 3.3233509...
```

### Normalizacion de distribuciones estadisticas

```python
import numpy as np
from scipy.special import gamma

# Constante de la densidad chi-cuadrado con k grados de libertad
k = 4
const = 1.0 / (2**(k/2) * gamma(k/2))
const    # → 0.25
```

### Combinatoria continua / coeficientes

```python
# Coeficiente binomial generalizado via Gamma: C(n, k) = Γ(n+1)/(Γ(k+1)Γ(n-k+1))
n, k = 6, 2
gamma(n+1) / (gamma(k+1) * gamma(n-k+1))   # → 15.0
```

## Buenas practicas

1. Para enteros usa `gamma(n+1)` recordando el desplazamiento +1 respecto a `n!`.
2. Si el argumento puede ser grande, calcula en log con `gammaln` y exponencia solo al final para evitar overflow.
3. Aprovecha la vectorizacion: pasa un `ndarray` completo en vez de iterar elemento a elemento.
4. Para derivadas logaritmicas de Gamma (psi) usa `digamma`, que aparece a menudo junto a `gamma`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `gamma(n)` en vez de `n!` | Olvidar el desfase Γ(n+1)=n! | Usar `gamma(n + 1)` |
| Resultado `inf` | Overflow para `z` grande (> ~171) | Trabajar con `gammaln` en escala log |
| `inf`/`nan` inesperado | Polo en entero ≤ 0 | Evitar 0 y enteros negativos como argumento |
| Perdida de precision en cocientes | Dividir Gammas enormes | Restar logaritmos con `gammaln` |

## Limitaciones

- Indefinida (polos) en `z = 0, -1, -2, ...`; alli devuelve `±inf` o `nan`.
- Desborda a `inf` en `float64` aproximadamente desde `z > 171`.
- Para precision en magnitudes extremas conviene el logaritmo `gammaln`, no `log(gamma(z))`.

## Notas relacionadas

- [[scipy.special.gammaln]]
- [[scipy.special.digamma]]
- [[scipy.special.factorial]]
