---
title: newton — raiz escalar por Newton-Raphson o secante (vectorizable)
aliases:
  - newton
  - newton-raphson
  - metodo de la secante
tags:
  - scipy
  - api/funcion
  - optimize/raices
lib: scipy
tipo: funcion
mod: scipy.optimize
retorna: float
requiere:
  - concepto_callbacks_vectorizados
draft: false
---

# newton — raiz escalar por Newton-Raphson o secante

Encuentra la raiz de una funcion **escalar** partiendo de una semilla `x0`. Si das la derivada `fprime`, usa **Newton-Raphson**; si no, cae al metodo de la **secante**; si das tambien `fprime2`, usa el metodo de **Halley**. Es **rapido** pero **no garantiza convergencia** (puede diverger con mala semilla). Admite `x0` como array para resolver muchas raices a la vez (modo vectorizado).

## Firma

```python
scipy.optimize.newton(func, x0, fprime=None, args=(), tol=1.48e-08,
                      maxiter=50, fprime2=None, x1=None,
                      rtol=0.0, full_output=False, disp=True)
```

## Valor de retorno

| Modo | Devuelve | Contenido |
|------|----------|-----------|
| Escalar (default) | `float` | La raiz |
| Escalar, `full_output=True` | `(root, RootResults)` | Raiz + diagnostico |
| `x0` array | `ndarray` | Una raiz por cada componente |

| Atributo (RootResults) | Significado |
|------------------------|-------------|
| `.root` | Raiz hallada |
| `.converged` | `True` si convergio |
| `.iterations` | Iteraciones realizadas |

## Formas basicas de llamada

```python
from scipy.optimize import newton

# Secante (sin derivada): raiz de x^2 - 2 cerca de 1.5
newton(lambda x: x**2 - 2, x0=1.5)              # → 1.4142135623730951

# Newton-Raphson (con derivada)
newton(lambda x: x**2 - 2, x0=1.5, fprime=lambda x: 2*x)   # → 1.4142135623730951
```

## Parametros en detalle

### func

`callable` escalar `f(x)` (o `f(x, *args)`). Se evalua repetidamente; escribela eficiente segun [[concepto_callbacks_vectorizados]]. En modo vectorizado debe aceptar arrays.

### x0

Semilla inicial. Si es un **array**, activa el modo vectorizado y devuelve un array de raices. La calidad de la semilla determina si converge.

### fprime

Derivada `f'(x)`. Si se aporta, usa **Newton-Raphson** (convergencia cuadratica). Si es `None`, usa **secante** (convergencia superlineal, sin derivada).

### args

`tuple` de parametros extra para `func`, `fprime` y `fprime2`.

### tol / rtol / maxiter

`tol` es la tolerancia absoluta sobre `x` (default `1.48e-08`); `maxiter` el tope de iteraciones (default `50`). Si no converge, lanza `RuntimeError` (con `disp=True`).

### fprime2

Segunda derivada `f''(x)`. Si se aporta junto con `fprime`, usa el metodo de **Halley** (convergencia cubica).

### x1

Segundo punto inicial para el metodo de la secante (opcional; si no, se genera internamente).

## Casos de uso

### Modo vectorizado (x0 array)

```python
import numpy as np

# Resuelve la misma ecuacion desde varias semillas de golpe
raices = newton(lambda x: x**2 - 2, x0=np.array([1.0, -1.0, 1.5]))
raices   # → array([ 1.41421356, -1.41421356,  1.41421356])
```

### Halley con segunda derivada

```python
newton(lambda x: x**3 - 2, x0=1.0,
       fprime=lambda x: 3*x**2,
       fprime2=lambda x: 6*x)        # → 1.2599210498948732
```

### Diagnostico con full_output

```python
r, res = newton(lambda x: np.cos(x) - x, x0=0.5, full_output=True)
res.converged   # → True
res.iterations  # → 4
```

## Buenas practicas

- Aporta `fprime` cuando puedas: pasa de secante a Newton (cuadratico) y reduce evaluaciones.
- Da una semilla `x0` **cercana** a la raiz; lejos del optimo Newton puede oscilar o diverger.
- Si tienes un intervalo con cambio de signo y necesitas robustez, prefiere `brentq` sobre `newton`.
- En modo vectorizado, comprueba que **todas** las componentes convergieron (`full_output`).

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `RuntimeError: Failed to converge` | Mala semilla o divergencia | Acerca `x0`, baja a secante, o usa `brentq` |
| Salta a otra raiz | `fprime` se anula cerca de `x0` | Cambia la semilla; evita puntos con `f'(x)≈0` |
| Resultado `nan` (vectorizado) | Alguna componente diverge | Usa `full_output`, filtra `.converged` |
| Lento o ciclico | Punto de inflexion / derivada mal calculada | Verifica `fprime`; prueba Halley o `brentq` |

## Limitaciones

- **No garantiza convergencia**: a diferencia de `brentq`, puede diverger o saltar a otra raiz.
- Newton requiere `f'(x) ≠ 0` cerca de la raiz; en raices multiples la convergencia se degrada.
- Solo funciones escalares; para sistemas multivariable usa `root`.

## Notas relacionadas

- [[scipy.optimize.brentq]]
- [[scipy.optimize.root]]
- [[concepto_callbacks_vectorizados]]
