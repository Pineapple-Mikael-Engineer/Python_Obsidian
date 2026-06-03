---
title: fsolve — raices de sistemas no lineales (interfaz legacy)
aliases:
  - fsolve
  - scipy fsolve
  - raices legacy
tags:
  - scipy
  - api/funcion
  - optimize/raices
lib: scipy
tipo: funcion
mod: scipy.optimize
retorna: ndarray
requiere:
  - concepto_callbacks_vectorizados
draft: false
---

# fsolve — raices de sistemas no lineales

> [!warning] Interfaz LEGACY
> `fsolve` es el wrapper **antiguo** sobre el metodo `'hybr'` de MINPACK. La interfaz moderna y recomendada es [[scipy.optimize.root]], que unifica varios metodos y devuelve un objeto-resultado. Documenta `fsolve` porque abunda en codigo viejo; **para codigo nuevo, migra a `root`**.

Resuelve `func(x) = 0` para un **sistema** de ecuaciones no lineales. A diferencia de `root`, por defecto devuelve **directamente el array solucion**, no un `OptimizeResult`.

## Firma

```python
scipy.optimize.fsolve(func, x0, args=(), fprime=None, full_output=0,
                      col_deriv=0, xtol=1.49012e-08, maxfev=0,
                      band=None, epsfcn=None, factor=100, diag=None)
```

## Valor de retorno

El retorno depende de `full_output`:

| `full_output` | Devuelve | Contenido |
|---------------|----------|-----------|
| `0` (default) | `ndarray` | Solo el vector solucion `x` |
| `1` | `(x, infodict, ier, mesg)` | Solucion + diagnostico detallado |

| Elemento (full_output) | Significado |
|------------------------|-------------|
| `x` | Vector solucion |
| `infodict['fvec']` | Residuos `func(x)` en la solucion |
| `infodict['nfev']` | Numero de evaluaciones |
| `ier` | `1` si convergio; otro valor indica fallo |
| `mesg` | Mensaje de estado |

## Formas basicas de llamada

```python
import numpy as np
from scipy.optimize import fsolve

def sistema(v):
    x0, x1 = v
    return [x0 * np.cos(x1) - 4,
            x0 * x1 - x1 - 5]

x = fsolve(sistema, x0=[1.0, 1.0])
x   # → array([6.50409711, 0.90841421])  (array directo, NO OptimizeResult)
```

## Parametros en detalle

### func

`callable` que recibe `x` y devuelve los **residuos** (mismo tamaño que `x`). Se evalua muchas veces; escribela vectorizada con NumPy segun [[concepto_callbacks_vectorizados]].

### x0

Semilla inicial; su longitud fija la dimension del sistema.

### args

`tuple` de parametros extra inyectados a `func` (y a `fprime`) en cada llamada.

### fprime

`callable` que devuelve la Jacobiana de `func`. Si es `None`, se estima por diferencias finitas. Equivale al `jac` de `root`.

### full_output

Si es `1`, devuelve la tupla `(x, infodict, ier, mesg)` con diagnostico. Es la **unica** forma de obtener informacion de convergencia, ya que `fsolve` no expone un objeto-resultado.

### xtol / maxfev

Tolerancia de paso relativa y numero maximo de evaluaciones. Equivalen a opciones que en `root` se pasan via `options`.

## Casos de uso

### Recuperar diagnostico de convergencia

```python
x, info, ier, msg = fsolve(sistema, [1.0, 1.0], full_output=1)
ier            # → 1  (convergio)
info['fvec']   # → array([~0, ~0])  residuos en la solucion
```

### Con Jacobiana analitica

```python
def f(v):
    x, y = v
    return [x**2 + y**2 - 1, x - y]

def jac(v):
    x, y = v
    return np.array([[2*x, 2*y], [1.0, -1.0]])

fsolve(f, [1.0, 1.0], fprime=jac)   # → array([0.70710678, 0.70710678])
```

### Contraste con root (equivalencia)

```python
# fsolve(func, x0) ≡ root(func, x0, method='hybr').x
from scipy.optimize import root
root(sistema, [1.0, 1.0], method='hybr').x   # → mismo resultado que fsolve
```

## Buenas practicas

- En codigo **nuevo**, prefiere `root`: misma potencia, mas metodos y resultado estructurado.
- Si usas `fsolve`, activa `full_output=1` y comprueba `ier == 1` antes de confiar en `x`.
- Aporta `fprime` cuando puedas para acelerar y estabilizar.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Se asume que devuelve `.x` | `fsolve` devuelve el array directo, no un objeto | Usa `x = fsolve(...)`, sin `.x` |
| No se detecta fallo de convergencia | Por defecto no informa estado | Usa `full_output=1` y revisa `ier` |
| `func` con tamaño incorrecto | Devuelve mas/menos residuos que `x` | Asegura `len(func(x)) == len(x)` |
| Raiz inesperada | Semilla lejana a la deseada | Ajusta `x0` |

## Limitaciones

- Solo expone el metodo `'hybr'` (Powell hibrido); ninguna alternativa como `krylov` o `lm`.
- No devuelve objeto-resultado salvo con `full_output=1`.
- Encuentra una sola raiz cercana a la semilla; no es global.

## Notas relacionadas

- [[scipy.optimize.root]]
- [[concepto_callbacks_vectorizados]]
