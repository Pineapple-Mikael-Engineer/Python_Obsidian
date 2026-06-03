---
title: scipy.special.jv — funcion de Bessel de primera especie J_v(z)
aliases:
  - jv
  - scipy.special.jv
  - Bessel primera especie
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

# scipy.special.jv — funcion de Bessel de primera especie J_v(z)

Evalua la **funcion de Bessel de primera especie** J_v(z) de **orden real** `v` y argumento `z`. Son las soluciones acotadas en el origen de la ecuacion de Bessel, que aparece al separar variables del Laplaciano en **geometria cilindrica**. Es una **ufunc**: acepta escalares y arrays NumPy tanto en `v` como en `z`, y opera **elemento a elemento** (vectorizada) con broadcasting entre ambos argumentos.

> El orden `v` puede ser cualquier real (incluso fraccionario). Cuando el orden es entero existe la variante optimizada `jn`. Las funciones J_v(z) oscilan y decaen lentamente (∼ z^(−1/2)) para z grande, como ondas amortiguadas.

## Firma

```python
scipy.special.jv(v, z, /, out=None) -> ndarray
# v: array_like, orden real de la funcion de Bessel
# z: array_like, argumento (real o complejo)
# out: ndarray opcional donde escribir el resultado
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `float` | J_v(z) si `v` y `z` son escalares reales |
| `complex` | J_v(z) si `z` es complejo |
| `ndarray` | J_v(z) elemento a elemento, con broadcasting de `v` y `z` |

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Bessel de orden 0 | `jv(0, 2.5)` |
| Bessel de orden entero | `jv(1, z)` (o `jn(1, z)`) |
| Orden fraccionario | `jv(0.5, z)` |
| Vectorizada en z | `jv(0, np.linspace(0, 10, 50))` |

## Parametros en detalle

### `v` (obligatorio)

Orden real de la funcion de Bessel. Puede ser entero o fraccionario, escalar o `ndarray`. Para orden entero puro, `jn` es equivalente y algo mas rapida.

```python
import numpy as np
from scipy.special import jv

jv(0, 0.0)    # → 1.0     (J_0(0) = 1)
jv(1, 0.0)    # → 0.0     (J_v(0) = 0 para v > 0)
```

### `z` (obligatorio)

Argumento de la funcion, `array_like` real o complejo. Por ser ufunc se evalua elemento a elemento y hace broadcasting con `v`.

```python
z = np.linspace(0, 10, 5)
jv(0, z)      # → array([ 1.   ,  0.177..., -0.397..., -0.090...,  0.245...])
```

### `out`

`ndarray` opcional preasignado donde depositar el resultado.

## Casos de uso

### Modos de vibracion de una membrana circular (tambor)

```python
import numpy as np
from scipy.special import jv, jn_zeros

# Amplitud radial del modo fundamental: J_0(k r), con k del primer cero de J_0
r = np.linspace(0, 1, 100)
k = jn_zeros(0, 1)[0]          # primer cero de J_0 ≈ 2.4048
modo = jv(0, k * r)            # perfil radial, nulo en el borde r=1
modo[-1]                       # → ~0.0   (condicion de contorno)
```

### Patron de difraccion (optica, disco de Airy)

```python
# Intensidad de difraccion por una apertura circular ∝ (2 J_1(x) / x)^2
x = np.linspace(0.1, 12, 6)
I = (2 * jv(1, x) / x)**2
I[0]    # → ~0.997   (cerca del maximo central)
```

## Buenas practicas

1. Para ordenes enteros puros usa `jn`; reserva `jv` para ordenes reales/fraccionarios.
2. Aprovecha la vectorizacion: pasa un `ndarray` de `z` para barrer el perfil de una sola llamada.
3. Para condiciones de contorno (membranas, guias de onda) obten los ceros con `jn_zeros` en vez de buscarlos a mano.
4. La segunda solucion independiente (singular en el origen) es `yv`; usala cuando el dominio excluya r = 0.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Intercambiar argumentos | La firma es `jv(v, z)`, orden primero | Respetar el orden `(orden, argumento)` |
| Esperar valor finito singular en 0 | J_v(0)=0 para v>0; la singular es Y_v | Usar `yv` si se requiere la 2a solucion |
| Buscar ceros manualmente | Imprecision al tantear raices | Usar `jn_zeros(v, n)` |
| Usar `jv` con orden entero grande en bucle | Mas lento que la variante entera | Usar `jn` para orden entero |

## Limitaciones

- Solo cubre la primera especie (acotada en el origen); para la segunda usar `yv`.
- Para argumentos `z` muy grandes el coste y la cancelacion aumentan; considerar formas asintoticas.
- Los ceros no son analiticos: requieren `jn_zeros` u otra rutina numerica.

## Notas relacionadas

- [[scipy.special.yv]]
- [[scipy.special.jn_zeros]]
- [[scipy.special.gamma]]
