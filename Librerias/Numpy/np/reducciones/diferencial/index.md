---
title: np/reducciones/diferencial — cálculo numérico discreto
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/diferencial — cálculo numérico discreto

Esta subcarpeta agrupa las funciones que hacen de puente entre el **análisis matemático continuo**
(derivadas e integrales) y los **datos discretos** del mundo real: solo se tiene una tabla de
valores muestreados, no la función analítica. Son las tres operaciones del cálculo numérico básico
sobre una serie: **diferencia** (cambio entre vecinos), **derivada/gradiente** (pendiente) e
**integral** (área).

La clave para elegir entre ellas no es solo "qué calculan", sino **qué le hacen al eje**: las tres
parten del mismo array pero devuelven shapes distintos.

## El contraste de mapas de shapes

Tres comportamientos distintos sobre el eje operado `axis=p`:

| Función | Qué le hace al eje | Mapa de shapes |
|---|---|---|
| [[np.diff]] | lo **acorta** en `n` | $(\dots,n_p,\dots)\to(\dots,n_p-n,\dots)$ |
| [[np.gradient]] | lo **conserva** | $(\dots,n_p,\dots)\to(\dots,n_p,\dots)$ |
| [[np.trapz]] | lo **reduce** (desaparece) | $(\dots,n_p,\dots)\to(\dots,\widehat{n_p},\dots)$ |

`diff` deja un elemento menos por orden; `gradient` da una derivada por punto (y en N-D una **lista**
de arrays, uno por eje); `trapz` colapsa el eje a un único valor, como cualquier reducción (ver
[[np.sum]]).

```python
import numpy as np
x = np.array([0., 1., 2., 3.])
y = x**2          # y = x²; derivada analítica = 2x; ∫ en [0,3] = 9

np.diff(y)        # [1., 3., 5.]     → shape (3,): el eje se acorta
np.gradient(y, x) # [1., 2., 4., 6.] → shape (4,): mismo shape, centrado
np.trapz(y, x)    # 9.0              → escalar: el eje desaparece
```

## Tabla de decisión

| Quieres… | Función | Por qué |
|---|---|---|
| el **cambio** entre muestras consecutivas (saltos, deltas) | [[np.diff]] | resta vecinos; `n>1` para órdenes superiores |
| la **derivada / pendiente** alineada con cada punto | [[np.gradient]] | diferencias centradas, conserva el shape, acepta espaciado real |
| la **integral / área** bajo la curva | [[np.trapz]] | regla del trapecio, reduce el eje a un valor |

Regla práctica: si necesitas **mantener la longitud** del array para seguir operando con él, usa
`gradient`; si solo quieres los incrementos crudos, `diff`; si quieres acumular el área total,
`trapz`.

> [!note] diff vs gradient
> [[np.diff]] es más simple y rápido pero **acorta** el array y no usa el espaciado (asume paso 1).
> [[np.gradient]] **conserva** el shape, usa diferencias centradas (más preciso en el interior) y
> admite coordenadas no uniformes. Elige según si necesitas conservar la longitud y la escala física.

> [!note] np.trapz → np.trapezoid
> Desde NumPy 2.0 `np.trapz` está **deprecada** y se renombró a `np.trapezoid` (mismo comportamiento).
> En código nuevo usa `np.trapezoid`.

## Notas relacionadas

- [[np.diff]] — diferencia discreta (acorta el eje)
- [[np.gradient]] — derivada por diferencias centradas (conserva el shape)
- [[np.trapz]] — integral por la regla del trapecio (reduce el eje)
- [[concepto_axis_parametro]] — qué significa operar a lo largo de un eje
- [[np.cumsum]] — suma acumulada (integral discreta sin promediar)
