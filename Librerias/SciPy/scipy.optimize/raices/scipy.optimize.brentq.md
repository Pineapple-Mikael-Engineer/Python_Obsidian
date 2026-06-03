---
title: brentq — raiz escalar robusta en un intervalo con cambio de signo
aliases:
  - brentq
  - metodo de brent
  - raiz acotada
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

# brentq — raiz escalar en un intervalo

Encuentra la raiz de una funcion **escalar** `f` dentro de un intervalo `[a, b]`. **Requiere** que `f(a)` y `f(b)` tengan **signo opuesto** (cambio de signo), garantizando por Bolzano que existe al menos una raiz en el intervalo. Usa el metodo de Brent (biseccion + secante + interpolacion cuadratica inversa): **robusto y de convergencia garantizada**. Es la opcion **mas recomendada** para una raiz escalar acotada.

## Firma

```python
scipy.optimize.brentq(f, a, b, args=(), xtol=2e-12, rtol=8.88e-16,
                      maxiter=100, full_output=False, disp=True)
```

## Valor de retorno

| `full_output` | Devuelve | Contenido |
|---------------|----------|-----------|
| `False` (default) | `float` | La raiz `x0` |
| `True` | `(x0, RootResults)` | Raiz + objeto con diagnostico |

| Atributo (RootResults) | Significado |
|------------------------|-------------|
| `.root` | Raiz hallada |
| `.converged` | `True` si convergio |
| `.iterations` | Numero de iteraciones |
| `.function_calls` | Numero de evaluaciones de `f` |

## Formas basicas de llamada

```python
from scipy.optimize import brentq

# Raiz de x^2 - 2 en [0, 2]: f(0)=-2 < 0, f(2)=2 > 0 (cambio de signo OK)
r = brentq(lambda x: x**2 - 2, 0, 2)
r   # → 1.4142135623730951
```

## Parametros en detalle

### f

`callable` escalar: recibe un `float` y devuelve un `float`. Se evalua repetidamente, escribela de forma eficiente segun [[concepto_callbacks_vectorizados]]. Debe ser **continua** en `[a, b]`.

### a, b

Extremos del intervalo (el **bracket**). Condicion **obligatoria**: `f(a) * f(b) < 0`. Si no hay cambio de signo, lanza `ValueError: f(a) and f(b) must have different signs`.

### args

`tuple` de parametros extra inyectados a `f` en cada llamada.

### xtol / rtol

Tolerancias absoluta y relativa de terminacion sobre `x`. `xtol` debe ser positivo; `rtol` no puede bajar de un minimo dependiente de la maquina.

### maxiter

Numero maximo de iteraciones (default `100`). Si se supera sin converger, lanza error (o lo refleja en `RootResults` si `disp=False`).

### full_output / disp

`full_output=True` devuelve tambien el objeto `RootResults`. `disp=True` lanza excepcion si no converge; `disp=False` la suprime.

## Casos de uso

### Diagnostico con full_output

```python
raiz, res = brentq(lambda x: x**3 - x - 2, 1, 2, full_output=True)
raiz           # → 1.5213797068045676
res.converged  # → True
res.iterations # → 8
```

### Parametros con args

```python
def f(x, c):
    return x**2 - c

brentq(f, 0, 5, args=(9.0,))   # → 3.0
```

### Verificar el bracket antes de llamar

```python
import numpy as np
a, b = 0.0, 3.0
g = lambda x: np.cos(x) - x
assert g(a) * g(b) < 0          # confirma cambio de signo
brentq(g, a, b)                 # → 0.7390851332151607
```

## Buenas practicas

- **Comprueba el cambio de signo** (`f(a)*f(b) < 0`) antes de llamar, idealmente graficando o muestreando la funcion.
- Para una raiz acotada, prefiere `brentq` sobre `newton`: converge siempre dentro del bracket.
- Si la funcion tiene **varias raices** en `[a, b]`, acota el intervalo a cada cambio de signo por separado.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: f(a) and f(b) must have different signs` | No hay cambio de signo en el bracket | Elige `a, b` que encierren la raiz |
| Devuelve una raiz, hay otras | Multiples raices en el intervalo | Subdivide en sub-intervalos con un solo cambio de signo |
| Resultado erroneo en discontinuidad | `f` no continua (cruza un polo) | El cambio de signo es de un polo, no de una raiz; valida `f(r)~0` |
| `RuntimeError` por no converger | `maxiter` insuficiente | Aumenta `maxiter` o ajusta tolerancias |

## Limitaciones

- Solo funciones **escalares** de una variable; para sistemas usa `root`.
- Necesita un **bracket** con cambio de signo: no sirve para raices donde `f` toca el eje sin cruzarlo (raices dobles).
- No vectorizado: una raiz por llamada (a diferencia de `newton` con `x0` array).

## Notas relacionadas

- [[scipy.optimize.newton]]
- [[concepto_callbacks_vectorizados]]
