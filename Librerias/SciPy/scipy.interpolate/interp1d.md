---
title: interp1d — interpolador 1D legacy (callable)
aliases:
  - interp1d
  - scipy.interpolate.interp1d
  - interpolacion 1D
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

# interp1d — interpolador 1D legacy (callable)

Clase que construye un **interpolador unidimensional** a partir de puntos muestreados `(x, y)`. El constructor no devuelve valores: devuelve una **funcion** que luego se evalua sobre nuevos abscisas, `f(xnew)`. Soporta varios esquemas (`kind`) desde vecino mas cercano hasta splines cubicos, y controla el comportamiento fuera del rango muestreado mediante `bounds_error` y `fill_value`.

> [!warning] Considerada legacy (SciPy >= 1.14)
> `interp1d` esta marcada como **legacy**: se mantiene por compatibilidad pero no se recomienda para codigo nuevo. Segun el caso, prefiere `numpy.interp` (lineal simple), `make_interp_spline` o `CubicSpline` (splines), o `PchipInterpolator` (monotono sin oscilacion). Se documenta aqui porque **abunda en codigo existente** y conviene saber leerla y portarla.

## Constructor

```python
scipy.interpolate.interp1d(
    x,                      # array_like (n,): abscisas muestreadas
    y,                      # array_like: ordenadas; el eje `axis` debe medir n
    kind='linear',         # str | int: esquema de interpolacion (ver tabla)
    axis=-1,               # int: eje de `y` sobre el que interpolar
    copy=True,             # bool: copia x,y internamente
    bounds_error=True,     # bool: error si xnew sale de [x.min, x.max]
    fill_value=nan,        # valor/tupla/'extrapolate': que devolver fuera de rango
    assume_sorted=False,   # bool: True si x ya viene ordenado ascendente
)                          # -> callable f(xnew) -> ndarray
```

## Parametro `kind`

| `kind` | Esquema | Continuidad |
|--------|---------|-------------|
| `'linear'` (default) | Recta entre puntos | C0 |
| `'nearest'` | Valor del punto mas cercano | escalonada |
| `'nearest-up'` | Como nearest, redondea .5 hacia arriba | escalonada |
| `'zero'` | Spline orden 0 (constante a trozos) | escalonada |
| `'previous'` | Valor del punto anterior | escalonada |
| `'next'` | Valor del punto siguiente | escalonada |
| `'slinear'` | Spline orden 1 (lineal via B-spline) | C0 |
| `'quadratic'` | Spline orden 2 | C1 |
| `'cubic'` | Spline orden 3 | C2 |
| `int n` | Spline B de orden `n` | C(n-1) |

> `kind='cubic'` es el caso que conviene migrar a `CubicSpline` o `make_interp_spline`, que ofrecen derivadas e integracion ademas de la evaluacion.

## Parametros en detalle

### `bounds_error` y `fill_value`

Gobiernan juntos el comportamiento **fuera** de `[x.min(), x.max()]`:

- `bounds_error=True` (default): lanza `ValueError` si algun `xnew` cae fuera del rango.
- `bounds_error=False`: no lanza error; rellena con `fill_value`.
- `fill_value=valor`: usa ese escalar fuera de rango (implica `bounds_error=False`).
- `fill_value=(abajo, arriba)`: valor distinto por debajo de `x.min` y por encima de `x.max`.
- `fill_value='extrapolate'`: **extrapola** con el mismo esquema; desactiva `bounds_error`.

```python
import numpy as np
from scipy.interpolate import interp1d

x = np.array([0., 1., 2., 3.])
y = np.array([0., 1., 4., 9.])

f = interp1d(x, y, kind='linear')      # bounds_error=True por defecto
f(1.5)                                  # → 2.5
# f(5.0)                                # ValueError: x fuera de rango

g = interp1d(x, y, fill_value='extrapolate')
g(5.0)                                   # → extrapolacion lineal (15.0)

h = interp1d(x, y, bounds_error=False, fill_value=(-1.0, 99.0))
h([-2.0, 10.0])                          # → array([-1., 99.])
```

### `assume_sorted`

Si `x` ya esta ordenado de forma ascendente, `assume_sorted=True` evita el reordenamiento interno (ahorra una ordenacion). Con `False` (default) SciPy ordena por seguridad.

### `axis`

Permite interpolar arrays `y` multidimensionales a lo largo de un eje concreto: con `y` de forma `(n, m)` y `axis=0`, se obtienen `m` interpoladores en paralelo evaluables a la vez.

## Casos de uso

### Resamplear una serie a una rejilla nueva

```python
x  = np.linspace(0, 10, 11)
y  = np.sin(x)
f  = interp1d(x, y, kind='cubic')        # se construye el interpolador
xn = np.linspace(0, 10, 200)
yn = f(xn)                                # se EVALUA como funcion -> ndarray (200,)
```

### Lookup de tabla con escalon (previous)

```python
# tarifa por tramos: el precio vigente es el del ultimo umbral alcanzado
umbral = np.array([0, 100, 500, 1000])
precio = np.array([0.20, 0.18, 0.15, 0.12])
tarifa = interp1d(umbral, precio, kind='previous',
                  bounds_error=False, fill_value=(0.20, 0.12))
tarifa([50, 250, 1500])                   # → array([0.2 , 0.18, 0.12])
```

### Interpolar varias senales a la vez (axis)

```python
t   = np.linspace(0, 1, 5)
Y   = np.vstack([t**2, np.cos(t)])        # forma (2, 5): dos senales en filas
f   = interp1d(t, Y, axis=1)              # interpola a lo largo del tiempo
f(0.5).shape                              # → (2,) un valor por senal
```

## Buenas practicas

1. Para **codigo nuevo** prefiere las alternativas modernas; reserva `interp1d` para mantener codigo legado.
2. Decide explicitamente el comportamiento fuera de rango: deja `bounds_error=True` para detectar abscisas invalidas, o fija `fill_value` a conciencia.
3. Pasa `assume_sorted=True` solo si garantizas `x` ordenado; un `x` desordenado con ese flag da resultados erroneos sin avisar.
4. Construye el interpolador **una vez** y reutilizalo para muchos `xnew`; el coste esta en el constructor, no en la llamada.
5. Evita `kind` de orden alto con pocos puntos: los splines cubicos oscilan (Runge); si necesitas monotonia usa un interpolador PCHIP.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: A value in x_new is below/above the interpolation range` | `xnew` fuera de `[x.min,x.max]` con `bounds_error=True` | Fijar `fill_value` o `'extrapolate'`, o filtrar `xnew` |
| Resultado escalonado inesperado | `kind='previous'/'next'/'nearest'` en vez de continuo | Usar `'linear'` o `'cubic'` |
| Oscilaciones grandes entre puntos | Spline cubico con datos ruidosos/pocos puntos | Bajar el orden o usar PCHIP/monotono |
| Salida desordenada o incorrecta | `assume_sorted=True` con `x` no ordenado | Ordenar `x,y` o dejar `assume_sorted=False` |
| `ValueError: x and y arrays must be equal in length along interpolation axis` | `y` no mide `n` en el eje `axis` | Ajustar `axis` o las formas de `x,y` |

## Limitaciones

- Solo **una dimension** de entrada; para mallas N-D usa otra herramienta.
- Considerada **legacy**: no expone derivadas ni integracion como los splines modernos.
- La extrapolacion (`'extrapolate'`) es **poco fiable** lejos del rango muestreado.
- No filtra ruido: **pasa exactamente** por todos los puntos dados.

## Notas relacionadas

- [[CubicSpline]]
- [[RegularGridInterpolator]]
- [[make_interp_spline]]
- [[numpy.interp]]
