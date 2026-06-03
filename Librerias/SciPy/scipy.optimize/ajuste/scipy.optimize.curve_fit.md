---
title: scipy.optimize.curve_fit — ajuste no lineal por minimos cuadrados
aliases:
  - curve_fit
  - ajuste de curvas scipy
  - fit no lineal
tags:
  - scipy
  - api/funcion
  - optimize/ajuste
lib: scipy
tipo: funcion
mod: scipy.optimize
retorna: tuple (popt, pcov)
requiere:
  - numpy
  - scipy.optimize.least_squares
draft: false
---

# scipy.optimize.curve_fit — ajuste no lineal por minimos cuadrados

Ajusta un modelo parametrico `f(x, *params)` a datos experimentales `(xdata, ydata)` minimizando la suma de cuadrados de los residuos. Es la herramienta directa para "encontrar los parametros de mi ecuacion que mejor explican mis mediciones". Internamente delega en `least_squares` (o en `leastsq` para el metodo `lm`).

> **No devuelve un OptimizeResult.** Devuelve una **tupla** `(popt, pcov)`. Es el error de lectura mas comun: no tiene `.x` ni `.success`.

## Firma

```python
scipy.optimize.curve_fit(
    f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False,
    check_finite=True, bounds=(-inf, inf), method=None, jac=None,
    *, full_output=False, nan_policy=None, **kwargs
)
```

## Valor de retorno

| Elemento | Tipo | Significado |
|----------|------|-------------|
| `popt` | `ndarray` (n_params,) | Parametros optimos que minimizan `sum((f(xdata,*popt)-ydata)**2)` |
| `pcov` | `ndarray` (n_params, n_params) | Matriz de covarianza estimada de `popt` |
| `infodict` | `dict` | Solo si `full_output=True`: diagnostico interno (`nfev`, residuos, etc.) |
| `mesg`, `ier` | `str`, `int` | Solo si `full_output=True`: mensaje y codigo de salida |

Errores estandar (1σ) de cada parametro a partir de la diagonal de `pcov`:

```python
errores = np.sqrt(np.diag(pcov))   # desviacion estandar de cada parametro en popt
```

Si `pcov` contiene `inf` o `NaN`, el ajuste no pudo estimar bien la incertidumbre (modelo sobreparametrizado, datos insuficientes o no convergio).

## Formas basicas de llamada

```python
import numpy as np
from scipy.optimize import curve_fit

def modelo(x, a, b):
    return a * np.exp(-b * x)

x = np.linspace(0, 4, 50)
y = modelo(x, 2.5, 1.3) + 0.05 * np.random.default_rng(0).normal(size=x.size)

# 1) ajuste basico
popt, pcov = curve_fit(modelo, x, y)
# popt ≈ [2.50, 1.30]

# 2) con semilla inicial (recomendado)
popt, pcov = curve_fit(modelo, x, y, p0=[2.0, 1.0])

# 3) con cotas en los parametros (fuerza a>0, 0<b<5)
popt, pcov = curve_fit(modelo, x, y, p0=[2.0, 1.0], bounds=([0, 0], [np.inf, 5]))
```

## Parametros en detalle

### `f`
La funcion modelo. Su firma es `f(x, a, b, ...)`: el **primer argumento es la variable independiente** y el resto son los parametros a ajustar. El numero de parametros se infiere de la firma (o de `p0` si pasas `**kwargs`/`*args`). Debe estar **vectorizada en `x`**: recibe el array `xdata` completo y devuelve un array del mismo tamaño que `ydata`. Si dentro usas bucles Python o devuelves un escalar, el ajuste falla o es lentisimo.

### `xdata`, `ydata`
Datos observados. `xdata` puede ser un array 1D, o un array `(k, m)` para modelos con `k` variables independientes (ej. `f((x1, x2), a, b)`). `ydata` debe ser 1D y su longitud debe coincidir con la salida de `f(xdata, ...)`.

### `p0`
Semilla inicial de los parametros (array o lista). **Es el parametro mas determinante para la convergencia.** Si es `None`, se asume `1.0` para todos, lo que suele fallar en modelos exponenciales/sigmoides con escalas reales. Dar un `p0` con el orden de magnitud correcto evita minimos locales y divergencias.

### `sigma`
Incertidumbre de cada punto de `ydata`. Pondera el ajuste: puntos con menor `sigma` pesan mas. Si es 1D, son las desviaciones estandar `σ_i` (residuos ponderados `r_i = (f-y)/σ_i`). Si es 2D, se interpreta como matriz de covarianza de los datos. Sin `sigma`, todos los puntos pesan igual.

### `absolute_sigma`
Controla la interpretacion de `sigma` en el calculo de `pcov`:
- `False` (default): `sigma` es **relativa**; `pcov` se reescala con la varianza residual estimada. Apropiado cuando solo conoces pesos relativos.
- `True`: `sigma` son incertidumbres **absolutas** en unidades reales; `pcov` refleja directamente esas incertidumbres. Usalo cuando tus barras de error son fisicamente reales.

### `bounds`
Cotas `(low, high)` para los parametros, como dos arrays (o escalares). Activa automaticamente un metodo con region de confianza (`trf` por defecto). Restringir el espacio mejora la robustez cuando conoces rangos fisicos (constantes positivas, fracciones en `[0,1]`).

### `method`
Algoritmo: `'lm'` (Levenberg-Marquardt, default sin bounds, rapido), `'trf'` (Trust Region Reflective, default con bounds), `'dogbox'`. Solo `trf` y `dogbox` soportan `bounds`.

### `jac`
Jacobiano de `f` respecto a los parametros. Si lo provees (callable), acelera y estabiliza; si no, se estima por diferencias finitas.

### `nan_policy`
Que hacer con `NaN`/`inf` en los datos: `'raise'`, `'omit'`, o `None` (delega en `check_finite`).

## Casos de uso

### Decaimiento exponencial con errores estandar reportados

```python
import numpy as np
from scipy.optimize import curve_fit

def decaimiento(t, A, tau, c):
    return A * np.exp(-t / tau) + c

t = np.linspace(0, 10, 80)
rng = np.random.default_rng(1)
y = decaimiento(t, 5.0, 2.5, 0.4) + 0.1 * rng.normal(size=t.size)

popt, pcov = curve_fit(decaimiento, t, y, p0=[4, 2, 0])
perr = np.sqrt(np.diag(pcov))
# popt   ≈ [5.0, 2.5, 0.4]  -> A, tau, c
# perr   ≈ [0.04, 0.05, 0.02]  -> incertidumbre 1σ de cada parametro
```

### Sigmoide (curva de saturacion) con cotas fisicas

```python
def sigmoide(x, L, x0, k):
    return L / (1 + np.exp(-k * (x - x0)))

x = np.linspace(0, 20, 60)
rng = np.random.default_rng(2)
y = sigmoide(x, 100, 10, 0.8) + 2 * rng.normal(size=x.size)

# L>0, x0 en el rango de x, k>0
popt, pcov = curve_fit(
    sigmoide, x, y, p0=[90, 9, 1],
    bounds=([0, 0, 0], [200, 20, 5]),
)
# popt ≈ [100, 10, 0.8]
```

### Ajuste ponderado con incertidumbres absolutas

```python
yerr = np.full_like(y, 2.0)   # barra de error fisica de cada medida
popt, pcov = curve_fit(
    sigmoide, x, y, p0=[90, 9, 1],
    sigma=yerr, absolute_sigma=True,
)
# pcov ya esta en unidades reales: np.sqrt(np.diag(pcov)) son las σ de los parametros
```

### Bondad del ajuste (R^2)

```python
residuos = y - sigmoide(x, *popt)
ss_res = np.sum(residuos**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res / ss_tot          # ej. 0.987
```

## Buenas practicas

- Da siempre un `p0` razonable; estima los parametros a ojo desde la grafica antes de ajustar.
- Vectoriza el modelo con operaciones de NumPy, nunca con bucles sobre `x`.
- Usa `absolute_sigma=True` solo si tus `sigma` son incertidumbres reales; de lo contrario las barras de error de los parametros estaran mal escaladas.
- Reporta `popt` junto con `np.sqrt(np.diag(pcov))`; un parametro sin su incertidumbre no es un resultado completo.
- Para modelos con escalas muy dispares entre parametros, normaliza variables o usa `bounds` para acotar.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `RuntimeError: Optimal parameters not found` | No convergio (`p0` malo, modelo mal escalado) | Mejora `p0`, normaliza datos, añade `bounds` |
| `popt` absurdo y `pcov` con `inf` | Modelo sobreparametrizado o datos insuficientes | Reduce parametros o aporta mas datos / mejor `p0` |
| `TypeError: f() takes ...` | Firma incorrecta: variable independiente no va primero | Define `f(x, a, b, ...)` con `x` primero |
| Ajuste lento o `ValueError` de shapes | Modelo no vectorizado o devuelve escalar | Devuelve `array` con ops NumPy, igual tamaño que `ydata` |
| `ValueError: array must not contain infs or NaNs` | `NaN`/`inf` en datos | Limpia datos o usa `nan_policy='omit'` |
| Cotas ignoradas | `method='lm'` con `bounds` | Usa `method='trf'` o `'dogbox'` |

## Limitaciones

- Solo minimiza suma de cuadrados (`loss` lineal): **no es robusto a outliers**. Para eso, usa `least_squares` con `loss='soft_l1'`/`'huber'`/`'cauchy'`.
- Asume errores gaussianos para que `pcov` tenga interpretacion estadistica.
- Es optimizacion **local**: el resultado depende de `p0` y puede caer en un minimo local.
- No expone directamente `cost`, residuos ni `jac`; si necesitas esos diagnosticos o control fino de `loss`/`jac`, baja a `least_squares`.

## Notas relacionadas

- [[scipy.optimize.least_squares]]
- [[concepto_callbacks_vectorizados]]
- [[concepto_objetos_resultado]]
- [[concepto_relacion_numpy]]
