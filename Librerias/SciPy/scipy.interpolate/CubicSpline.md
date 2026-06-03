---
title: CubicSpline — spline cubico C2 interpolante (callable)
aliases:
  - CubicSpline
  - scipy.interpolate.CubicSpline
  - spline cubico
tags:
  - scipy
  - api/clase
  - interpolacion
lib: scipy
tipo: clase
mod: scipy.interpolate
requiere:
  - numpy
draft: false
---

# CubicSpline — spline cubico C2 interpolante (callable)

Clase que construye un **spline cubico** que pasa por todos los puntos `(x, y)` y es **C2-continuo** (curva, pendiente y curvatura continuas en los nudos). Se evalua como funcion `cs(xnew)` y, ademas, permite obtener **derivadas** `cs(xnew, nu)`, asi como **derivar, integrar y hallar raices** del propio spline. Es la alternativa moderna recomendada frente a un interpolador 1D legacy con `kind='cubic'`.

## Constructor

```python
scipy.interpolate.CubicSpline(
    x,                       # array_like (n,): abscisas, estrictamente crecientes
    y,                       # array_like: ordenadas; eje `axis` mide n
    axis=0,                 # int: eje de `y` sobre el que interpolar
    bc_type='not-a-knot',   # str | (par_izq, par_der): condiciones de contorno
    extrapolate=None,       # bool | 'periodic' | None: extrapolar fuera de rango
)                            # -> callable cs(xnew, nu=0) -> ndarray
```

## Metodos y atributos principales

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `cs(xnew, nu=0)` | call | Evalua el spline (o su derivada `nu`) en `xnew` |
| `cs.derivative(nu=1)` | metodo | Devuelve **otro** spline: la derivada `nu`-esima |
| `cs.antiderivative(nu=1)` | metodo | Devuelve la primitiva (spline integrado) |
| `cs.integrate(a, b)` | metodo | Integral definida en `[a, b]` |
| `cs.roots(extrapolate=...)` | metodo | Raices reales del spline (donde `cs(x)=0`) |
| `cs.solve(y=0)` | metodo | Abscisas donde `cs(x) = y` |
| `cs.c` | `ndarray` | Coeficientes polinomicos por tramo, forma `(4, n-1, ...)` |
| `cs.x` | `ndarray` | Nudos (los `x` de entrada) |

## Parametros en detalle

### `bc_type` (condiciones de contorno)

Define el comportamiento en los **extremos**, donde un spline cubico tiene grados de libertad sin fijar:

| `bc_type` | Condicion | Cuando |
|-----------|-----------|--------|
| `'not-a-knot'` (default) | 3a derivada continua en el 2o y penultimo nudo | Uso general, sin info de bordes |
| `'natural'` | 2a derivada = 0 en los extremos (curvatura nula) | Bordes "relajados", sin pendiente impuesta |
| `'clamped'` | 1a derivada = 0 en los extremos | Tangente horizontal en los bordes |
| `'periodic'` | Curva ciclica: `y[0]==y[-1]` y derivadas casan | Senales periodicas |
| `(izq, der)` | Tupla de condiciones por extremo, p.ej. `(1, m)` fija 1a deriv = `m` | Pendiente/curvatura conocida en un borde |

Cada elemento de la tupla es `(orden_derivada, valor)`: `(1, 0.0)` fija pendiente 0; `(2, 0.0)` fija curvatura 0.

### `extrapolate`

- `None` (default): extrapola con el polinomio del tramo extremo (equivale a `True`), salvo que `bc_type='periodic'`, donde pasa a periodico.
- `True` / `False`: forzar extrapolacion polinomica o devolver `nan` fuera de rango.
- `'periodic'`: extiende la curva de forma ciclica.

## Casos de uso

### Interpolar, derivar e integrar una curva suave

```python
import numpy as np
from scipy.interpolate import CubicSpline

x = np.linspace(0, 2*np.pi, 9)
y = np.sin(x)
cs = CubicSpline(x, y)                  # se construye el spline

xn = np.linspace(0, 2*np.pi, 200)
cs(xn)                                   # se EVALUA: valores interpolados
cs(xn, 1)                                # 1a derivada -> aproxima cos(x)
cs(xn, 2)                                # 2a derivada -> aproxima -sin(x)
cs.integrate(0, np.pi)                   # → ~2.0 (integral de sin en [0, pi])
```

### Splines derivados como objetos

```python
d1 = cs.derivative(1)                    # spline de la 1a derivada
prim = cs.antiderivative()               # spline primitiva
d1(np.pi)                                # evaluar la derivada como callable
```

### Hallar raices de la curva interpolada

```python
cs.roots()                               # abscisas donde el spline cruza 0
cs.solve(0.5)                            # abscisas donde cs(x) == 0.5
```

### Spline periodico

```python
ang = np.linspace(0, 2*np.pi, 13)        # ang[0] y ang[-1] cierran el ciclo
r   = np.cos(ang)                         # r[0] == r[-1]
csp = CubicSpline(ang, r, bc_type='periodic')
```

## Buenas practicas

1. Asegura `x` **estrictamente creciente y sin duplicados**; ordena antes si hace falta.
2. Elige `bc_type` segun lo que sepas del borde: `'natural'` si no impones pendiente, `'clamped'` si conoces la tangente, `'periodic'` para ciclos.
3. Aprovecha los splines derivados (`derivative`/`antiderivative`) en vez de derivar numericamente a mano.
4. Para datos **monotonos** que no deben oscilar, usa un interpolador PCHIP en lugar de `CubicSpline`.
5. No abuses de la **extrapolacion**: un cubico crece rapido fuera del rango y diverge.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: x must be strictly increasing` | `x` desordenado o con duplicados | Ordenar `x,y`; eliminar abscisas repetidas |
| `ValueError: The first and last y must be equal` (periodic) | `y[0] != y[-1]` con `bc_type='periodic'` | Igualar extremos o usar otro `bc_type` |
| Oscilaciones (Runge) entre puntos | Datos con saltos bruscos o ruido | Usar PCHIP/monotono o suavizar antes |
| Extrapolacion absurda lejos del rango | Cubico extrapolado | `extrapolate=False` o limitar `xnew` |
| `bc_type` ignorado / forma inesperada | Tupla mal formada `(orden, valor)` | Revisar el formato de las condiciones por extremo |

## Limitaciones

- **Interpola exactamente**: pasa por todos los puntos, no suaviza ruido (para eso, splines suavizantes).
- Solo entrada **1D**; para mallas N-D usa otra herramienta.
- No garantiza **monotonia** ni ausencia de overshoot entre nudos.
- La extrapolacion polinomica es fiable solo muy cerca de los extremos.

## Notas relacionadas

- [[interp1d]]
- [[RegularGridInterpolator]]
- [[make_interp_spline]]
- [[PchipInterpolator]]
