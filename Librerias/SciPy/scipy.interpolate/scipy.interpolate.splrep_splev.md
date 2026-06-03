---
title: splrep / splev — ajustar y evaluar B-splines con la API procedural FITPACK
aliases:
  - splrep
  - splev
  - scipy.interpolate.splrep
  - scipy.interpolate.splev
  - tck
tags:
  - scipy
  - api/funcion
  - interpolacion
lib: scipy
tipo: funcion
mod: scipy.interpolate
retorna: tuple tck / ndarray
requiere:
  - numpy
draft: false
---

# splrep / splev — ajustar y evaluar B-splines con la API procedural FITPACK

Par de funciones de la **interfaz procedural FITPACK** (Fortran) para trabajar con B-splines en dos pasos: `splrep` **ajusta** un spline a datos 1D `(x, y)` y devuelve una tupla `tck = (t, c, k)` —knots `t`, coeficientes `c` y grado `k`—; `splev` **evalua** ese spline (o su derivada) en puntos nuevos a partir de `tck`. La representacion `tck` es el objeto intermedio que conecta ambas etapas.

> Flujo de dos pasos: `tck = splrep(x, y)` (ajustar una vez) y luego `ynew = splev(xnew, tck)` (evaluar cuantas veces haga falta). El parametro `s` de `splrep` controla el equilibrio entre interpolar exactamente (`s=0`) y suavizar datos ruidosos (`s>0`).

> Es la interfaz **procedural antigua**. La alternativa moderna, orientada a objetos, es `make_interp_spline` / `BSpline` (devuelve un objeto evaluable como `spl(xnew)` y derivable con `spl.derivative()`). Para codigo nuevo se recomienda esa via; `splrep/splev` siguen vigentes y son muy comunes en codigo existente. La relacion con los arrays de NumPy es la habitual: todo entra y sale como `ndarray`, ver [[concepto_relacion_numpy]].

## Firma

```python
scipy.interpolate.splrep(
    x, y,          # ndarray 1D: datos a ajustar, x estrictamente creciente
    w=None,        # ndarray: pesos por punto (1/sigma tipicamente)
    k=3,           # int: grado del spline (3 = cubico; 1..5)
    s=None,        # float: factor de suavizado (s=0 interpola; s>0 ajusta)
    t=None,        # ndarray: knots interiores si task=-1
    ...
) -> tuple        # tck = (t, c, k)

scipy.interpolate.splev(
    x,             # ndarray: puntos donde evaluar
    tck,           # tuple (t, c, k) devuelta por splrep
    der=0,         # int: orden de la derivada a evaluar
    ext=0,         # int: comportamiento fuera del rango de los knots
) -> ndarray
```

## Valor de retorno

| Funcion | Tipo | Significado |
|---------|------|-------------|
| `splrep` | `tuple (t, c, k)` | `t`: knots; `c`: coeficientes B-spline; `k`: grado |
| `splev` | `ndarray` | Valores del spline (o derivada `der`) en los `x` dados |

```python
tck = splrep(x, y)          # tupla (t, c, k)
ynew = splev(xnew, tck)     # array con los valores interpolados
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Ajustar spline interpolante (pasa por todos los puntos) | `splrep(x, y, s=0)` |
| Ajustar spline suavizado | `splrep(x, y, s=len(x))` |
| Cambiar el grado (p. ej. lineal) | `splrep(x, y, k=1)` |
| Evaluar el spline | `splev(xnew, tck)` |
| Evaluar la 1a derivada | `splev(xnew, tck, der=1)` |
| Evaluar la 2a derivada | `splev(xnew, tck, der=2)` |

## Parametros en detalle

### `x`, `y` (obligatorios de splrep)

Datos a ajustar. `x` debe ser **estrictamente creciente** (ordenar antes si hace falta). `y` son los valores observados.

```python
import numpy as np
from scipy.interpolate import splrep, splev

x = np.linspace(0, 10, 11)
y = np.sin(x)
tck = splrep(x, y, s=0)        # spline interpolante exacto
```

### `k` (grado)

Grado del polinomio por tramo, entre 1 y 5. `k=3` (cubico) es el habitual: equilibra suavidad y estabilidad. `k=1` da una poligonal lineal. Requiere al menos `k+1` puntos.

### `s` (factor de suavizado)

Controla el ajuste vs. suavidad. El spline cumple `sum(w*(y - spline(x))**2) <= s`.

| Valor de `s` | Comportamiento |
|--------------|----------------|
| `s=0` | Interpolacion exacta: pasa por todos los puntos |
| `s>0` | Ajuste suavizado: no pasa exacto, atenua ruido |
| `s=None` (default) | Heuristica: `s ~ len(x)` si hay pesos, suaviza por defecto |

Una guia comun para datos con ruido de desviacion `sigma` es `s ~ len(x)` (con pesos `w=1/sigma`).

```python
# datos ruidosos: s>0 suaviza, s=0 seguiria el ruido
rng = np.random.default_rng(0)
xr = np.linspace(0, 10, 60)
yr = np.sin(xr) + rng.normal(0, 0.15, xr.size)
tck_suave = splrep(xr, yr, s=len(xr))   # suaviza el ruido
```

### `w` (pesos)

Peso por punto; tipicamente `1/sigma_i`. Da mas influencia a las mediciones mas fiables y entra en el criterio de suavizado junto con `s`.

### `der` (de splev)

Orden de la derivada a evaluar. `der=0` (default) evalua el spline; `der=1` su primera derivada; `der=2` la segunda, etc. Debe cumplirse `der <= k`.

```python
xnew = np.linspace(0, 10, 200)
y_eval = splev(xnew, tck)            # spline
dy     = splev(xnew, tck, der=1)     # derivada primera
```

### `ext` (de splev)

Comportamiento fuera del intervalo de los knots: `0` extrapola, `1` devuelve `0`, `2` lanza `ValueError`, `3` mantiene el valor del borde. Evita extrapolaciones silenciosas inadvertidas.

## Casos de uso

### Interpolar una curva 1D y remuestrear fino

```python
import numpy as np
from scipy.interpolate import splrep, splev

x = np.linspace(0, 2*np.pi, 12)
y = np.sin(x)
tck = splrep(x, y, s=0)                 # interpolante exacto, cubico
xnew = np.linspace(0, 2*np.pi, 400)
ynew = splev(xnew, tck)                 # curva suave densa
```

### Suavizar datos ruidosos y evaluar su derivada

```python
# Señal experimental con ruido: ajustar suave y derivar
rng = np.random.default_rng(7)
xs = np.linspace(0, 10, 80)
ys = np.exp(-0.2*xs) * np.cos(xs) + rng.normal(0, 0.05, xs.size)

tck = splrep(xs, ys, s=0.5)             # s>0: filtra el ruido
xf  = np.linspace(0, 10, 400)
yf  = splev(xf, tck)                    # señal suavizada
dyf = splev(xf, tck, der=1)             # derivada de la señal suave
```

La derivada de un ajuste suavizado es mucho mas estable que diferenciar numericamente los datos crudos, donde el ruido se amplifica.

### Cambiar el grado para un ajuste lineal por tramos

```python
tck_lin = splrep(xs, ys, k=1, s=0)      # poligonal interpolante
y_lin   = splev(xf, tck_lin)
```

## Buenas practicas

1. Ajusta una sola vez (`splrep`) y reutiliza el `tck` en cada `splev`; no re-ajustes para reevaluar.
2. Asegura `x` estrictamente creciente y sin duplicados antes de `splrep`.
3. Para datos limpios usa `s=0`; para datos ruidosos sube `s` gradualmente (guia: `s ~ len(x)`) hasta lograr la suavidad deseada.
4. Para derivar datos ruidosos, suaviza con `s>0` y luego `splev(..., der=1)`; es mas estable que el diferenciado finito directo.
5. Controla la extrapolacion con `ext` (p. ej. `ext=2` para fallar si te sales del rango) en vez de confiar en la extrapolacion por defecto.
6. En codigo nuevo evalua usar `make_interp_spline`/`BSpline` (API orientada a objetos), mas legible y con metodos `.derivative()`/`.integrate()`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: x must be strictly increasing` | `x` desordenado o con duplicados | Ordenar y deduplicar antes de `splrep` |
| Spline interpolante "ondulado" sobre datos ruidosos | `s=0` fuerza pasar por todo el ruido | Usar `s>0` para suavizar |
| Spline demasiado plano / no sigue los datos | `s` demasiado grande | Reducir `s` hacia 0 |
| `der > k` falla o da ceros | Derivada de orden mayor que el grado | Subir `k` o reducir `der` |
| Resultados raros fuera del rango | Extrapolacion silenciosa (`ext=0`) | Fijar `ext=1/2/3` segun convenga |
| Menos de `k+1` puntos | Datos insuficientes para el grado | Bajar `k` o aportar mas puntos |

## Limitaciones

- Solo 1D: para superficies usar `bisplrep`/`bisplev` o `griddata`.
- API procedural heredada: el `tck` es una tupla opaca; la via moderna `BSpline`/`make_interp_spline` es mas explicita.
- El `tck` es especifico de FITPACK; no es intercambiable directamente con objetos `BSpline` sin conversion.
- El suavizado por `s` es global; no controla finamente el suavizado por region.
- No estima por si solo el `s` optimo: requiere criterio/iteracion del usuario.

## Notas relacionadas

- [[scipy.interpolate.make_interp_spline]]
- [[scipy.interpolate.BSpline]]
- [[scipy.interpolate.griddata]]
- [[concepto_relacion_numpy]]
