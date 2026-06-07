---
title: sympy.core/evaluacion — evaluacion
tags:
  - sympy
  - indice
draft: false
---

# evaluacion

El **final del flujo** de [[sympy.core/index | sympy.core]]: el puente que saca una expresion del mundo simbolico exacto y la convierte en numeros. Una `Expr` como `sqrt(2)` o `sin(x)` se mantiene simbolica todo el tiempo que quieras, pero tarde o temprano hace falta un valor concreto: para imprimir un resultado, para graficar, para alimentar codigo numerico. Esta carpeta cubre las dos formas de cruzar ese puente —[[Expr.evalf]] para **un** valor y [[sympy.lambdify]] para **muchos**— y vive sobre la idea de [[concepto_evalf_lambdify]].

La eleccion entre ambas es la pregunta central: **un valor de alta precision** o **muchos datos vectorizados**. `evalf` evalua una expresion a un `Float` de precision arbitraria; `lambdify` la **compila** a una funcion Python (tipicamente con backend NumPy) que evalua arrays enteros de golpe.

```python
import numpy as np
from sympy import symbols, sqrt, lambdify

x = symbols("x")
sqrt(2).evalf(30)                 # 1.41421356237309504880168872421 -> un valor exacto
f = lambdify(x, x**2 + 1, "numpy")
f(np.array([1.0, 2.0, 3.0]))      # array([ 2.,  5., 10.]) -> muchos a la vez
```

## Como se relacionan

Las dos notas hacen la misma transicion simbolico → numerico, pero a escalas opuestas: una llamada da un numero; la otra fabrica una funcion reutilizable.

| Nota | Para cuantos datos | Salida | Cuando usarla |
|------|--------------------|--------|---------------|
| [[Expr.evalf]] | **Un** valor (escalar) | `Float` de SymPy de `n` digitos | Un numero concreto, precision arbitraria, fijar simbolos con `subs` |
| [[sympy.lambdify]] | **Muchos** (arrays) | funcion Python (`callable`); `ndarray` con backend NumPy | Graficar/simular sobre miles de puntos; puente a NumPy/SciPy |

Regla de decision: `evalf` en bucle sobre miles de puntos es **lentisimo** (evalua un valor por llamada); para eso se **compila una sola vez** con `lambdify(..., "numpy")` y se evalua vectorizado. A cambio, `evalf` ofrece precision arbitraria real que `lambdify` (atado a la doble precision de NumPy) no da. Resumen: pocos valores y mucha precision → `evalf`; muchos valores y velocidad → `lambdify`.

## Notas

- [[Expr.evalf]] — Evalua **una** `Expr` a un `Float` de `n` digitos significativos; con `subs={...}` fija los simbolos libres. La via para un valor exacto de alta precision.
- [[sympy.lambdify]] — **Compila** la expresion a una funcion numerica rapida y vectorizable (backend `"numpy"`, `"math"`, `"mpmath"`); el puente correcto para evaluar masivo sobre arrays.

## Notas relacionadas

- [[sympy.core/index | sympy.core]]
- [[concepto_evalf_lambdify]]
- [[Float]]
- [[Tree SymPy]]
