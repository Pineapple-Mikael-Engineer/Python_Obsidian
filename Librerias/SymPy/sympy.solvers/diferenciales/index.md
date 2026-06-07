---
title: sympy.solvers/diferenciales — diferenciales
tags:
  - sympy
  - indice
draft: false
---

# diferenciales

Esta carpeta cubre la resolucion **exacta y simbolica** de **ecuaciones diferenciales ordinarias** (EDOs) con `dsolve`. Aqui la incognita ya no es un numero sino una **funcion** continua `f(x)`, y la ecuacion relaciona esa funcion con sus **derivadas**. Por eso el planteamiento cambia respecto a las algebraicas: la incognita se declara con `Function("f")` y se usa **aplicada** a su variable, `f(x)`; las derivadas se escriben `f(x).diff(x)`; y la ecuacion se arma con `Eq(lhs, rhs)`. La solucion general que devuelve `dsolve` lleva **constantes de integracion** (`C1`, `C2`, …, una por orden de derivacion) que se fijan con condiciones iniciales via `ics=`.

El patron de planteamiento, de la solucion general a la particular:

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")                              # 1) declarar la funcion incognita

dsolve(Eq(f(x).diff(x), f(x)), f(x))           # Eq(f(x), C1*exp(x))   -> general, con C1
dsolve(Eq(f(x).diff(x), f(x)), f(x),
       ics={f(0): 1})                          # Eq(f(x), exp(x))      -> particular (C1 fijada)
```

## Como se relacionan

Esta carpeta tiene un unico resolutor, `dsolve`, pero el index aporta el **modelo mental** de como se plantea una EDO en SymPy:

| Pieza | Como se escribe | Papel |
|-------|-----------------|-------|
| Funcion incognita | `f = Function("f")`, usada como `f(x)` | la incognita; se pasa **aplicada**, nunca el simbolo `x` suelto |
| Derivada | `f(x).diff(x)`, `f(x).diff(x, 2)` | relaciona la funcion con su variacion (objeto [[Derivative]]) |
| Ecuacion | `Eq(lhs, rhs)` (una `Expr` suelta se asume `= 0`) | la EDO en si |
| Condiciones iniciales | `ics={f(0): 1, f(x).diff(x).subs(x, 0): 0}` | fijan las constantes `C1`, `C2`, … |

Reglas para acertar:

- El **orden** de la EDO marca cuantas constantes salen y cuantas condiciones hacen falta: una EDO de orden 2 da `C1`, `C2` y necesita **dos** condiciones (valor y derivada) en `ics`.
- Las claves de `ics` son **expresiones evaluadas**: `f(0)` para el valor, `f(x).diff(x).subs(x, 0)` para la derivada en un punto; nunca la funcion generica `f` sin aplicar.
- Sin `ics`, `dsolve` devuelve la **solucion general** con constantes libres; con `ics` completas, la **particular**.

> [!tip] Simbolico vs numerico
> `dsolve` es el equivalente exacto de [[scipy.integrate.solve_ivp]], que integra EDOs de forma **numerica**. Si la ecuacion no encaja en los patrones conocidos de SymPy (no lineal arbitraria) o trabajas con datos numericos, usa `solve_ivp`. Para derivadas **parciales** existe `pdsolve`, fuera de esta carpeta.

`dsolve` es, ademas, el analogo continuo de [[sympy.rsolve]] (recurrencias): ambos despejan una incognita definida por su relacion con versiones previas de si misma —derivadas en lo continuo, terminos anteriores en lo discreto— y ambos producen constantes que las condiciones iniciales determinan.

## Notas

- [[sympy.dsolve]] — resuelve EDOs; reconoce decenas de patrones (separable, lineal, coeficientes constantes, …), elige el metodo automaticamente y admite `ics=` para fijar las constantes.

## Notas relacionadas

- [[sympy.solvers/index | sympy.solvers]]
- [[Tree SymPy]]
