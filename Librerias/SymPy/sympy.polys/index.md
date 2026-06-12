---
title: sympy.polys — manipulacion de polinomios
tags:
  - sympy
  - indice
draft: false
---

# sympy.polys

Este submodulo agrupa todo lo que SymPy ofrece para **trabajar con polinomios**: cambiar su
forma (expandir, factorizar), operar con ellos (division, mcd, grado) y hallar sus raices
exactas. Es la maquinaria que sostiene buena parte del algebra simbolica, y casi todas sus
funciones de uso diario son **top-level**: `expand`, `factor`, `gcd`, `degree`… aceptan una
`Expr` normal y devuelven otra `Expr`.

Hay **dos formas** de operar, y entenderlas es la clave de la carpeta:

- **Sobre la expresion directamente** (`Expr`): comodo, es lo que hacen las funciones top-level.
- **Sobre la representacion explicita** ([[Poly]]): un objeto denso de coeficientes por una
  variable generadora, mas rapido y exacto para trabajo polinomico intensivo, con acceso directo
  a grado y coeficientes.

```python
from sympy import symbols, factor, expand, Poly, div
x = symbols("x")

factor(x**2 - 1)            # (x - 1)*(x + 1)   -> funcion sobre Expr
expand((x - 1)*(x + 1))     # x**2 - 1          -> la inversa
Poly(x**2 - 1, x).all_coeffs()   # [1, 0, -1]   -> representacion explicita
div(x**2 - 1, x - 1)        # (x + 1, 0)        -> cociente y resto
```

## Como se relacionan

| Pieza | Que aporta | Cuando |
|-------|------------|--------|
| [[Poly]] | la **representacion** densa y explicita del polinomio | trabajo polinomico intensivo, acceso a coeficientes/grado |
| [[sympy.polys/expandir_factorizar/index \| expandir_factorizar]] | cambiar la **forma** (expand/factor, apart/together, collect) | reescribir un polinomio sin cambiar su valor |
| [[sympy.polys/operaciones/index \| operaciones]] | **aritmetica y raices** (gcd, lcm, div, degree, real_roots) | calcular con polinomios y extraer informacion |

La idea unificadora: `Poly` es el **dato** (como se guarda un polinomio), mientras que
*expandir_factorizar* y *operaciones* son los dos grupos de **verbos** (transformar la forma vs
calcular). Casi todas las funciones aceptan tanto `Expr` como `Poly`: usa `Poly` solo cuando la
velocidad o el acceso a coeficientes lo justifique.

## Subtemas

- [[Poly]] — la clase que representa un polinomio de forma explicita; base del resto del submodulo.
- [[sympy.polys/expandir_factorizar/index | expandir_factorizar]] — pares inversos `expand`/`factor` y `apart`/`together`, mas `collect`: cambian la forma, no el valor.
- [[sympy.polys/operaciones/index | operaciones]] — `gcd`, `lcm`, `div`, `degree`, `real_roots`: la aritmetica y las raices.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[sympy.simplify/general/index | simplify]]
