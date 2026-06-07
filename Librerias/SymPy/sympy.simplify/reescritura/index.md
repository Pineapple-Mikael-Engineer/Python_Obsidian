---
title: sympy.simplify/reescritura — reescritura
tags:
  - sympy
  - indice
draft: false
---

# reescritura

Esta carpeta trata de **reescribir** una expresion: reexpresarla en terminos de **otra familia de funciones equivalente**, sin pretender simplificarla. La idea clave es cambiar de **base de representacion** —pasar de trigonometricas a exponenciales, de un factorial a la funcion gamma, de un valor absoluto a una definicion por tramos— manteniendo el valor matematico exacto. No es buscar "lo mas corto" (eso es `simplify`) ni sustituir simbolos concretos (eso es [[Expr.subs]]): es traducir la expresion al lenguaje de otra funcion para que un solver, un integrador o una identidad la acepten en una misma base.

El metodo unico de esta carpeta es [[Expr.rewrite]], y su uso es siempre el mismo patron: `expr.rewrite(funcion_destino)`.

```python
from sympy import symbols, cos, exp, I, factorial, gamma, Abs, Piecewise
x = symbols("x"); n = symbols("n"); xr = symbols("x", real=True)

cos(x).rewrite(exp)            # exp(I*x)/2 + exp(-I*x)/2     -> forma de Euler
exp(I*x).rewrite(cos)          # I*sin(x) + cos(x)            -> camino inverso
factorial(n).rewrite(gamma)    # gamma(n + 1)                 -> base comun
Abs(xr).rewrite(Piecewise)     # Piecewise((x, x >= 0), (-x, True))
```

## rewrite vs simplify vs subs

Los tres devuelven una `Expr` nueva, pero responden a preguntas distintas. Hay que situar `rewrite` frente a sus vecinos para no confundirlos:

| Operacion | Que hace | Cuando usarla |
|-----------|----------|---------------|
| `rewrite(f)` | Cambia la **base de funciones** (misma cosa, otro lenguaje) | Llevar todo a `exp`, `sin`/`cos`, `gamma`, `Piecewise`… |
| `simplify` | Busca una forma **mas corta/canonica** (no fija la base) | Reducir y limpiar el resultado |
| `subs` | Sustituye **simbolos o subexpresiones** concretos | Evaluar parametros, particularizar |

> [!info] No simplifica
> `rewrite` puede dar una expresion mas larga que la original: `tan(x).rewrite(cos)` -> `cos(x - pi/2)/cos(x)`. Si quieres reducir despues, encadena con `simplify`/`trigsimp`.

## Notas

- [[Expr.rewrite]] — reexpresa una expresion en terminos de **otra funcion** (Euler `exp`<->trig, `factorial`->`gamma`, `Abs`->`Piecewise`); cambia la base, no la simplifica.

## Notas relacionadas

- [[sympy.simplify/index | sympy.simplify]]
- [[Tree SymPy]]
