---
title: sympy.solvers — sympy.solvers
tags:
  - sympy
  - indice
draft: false
---

# sympy.solvers

`sympy.solvers` es el submodulo que **resuelve ecuaciones** de todo tipo de forma exacta y simbolica: desde una ecuacion algebraica con una incognita hasta sistemas, ecuaciones diferenciales (EDOs) y relaciones de recurrencia. La idea comun es siempre la misma —plantear lo que se busca con `Eq(lhs, rhs)` (o una `Expr` suelta que se asume `= 0`) y pedir a SymPy que despeje la incognita—, pero la **naturaleza** de esa incognita cambia: un numero, una tupla de numeros, una funcion continua `f(x)` o una sucesion `y(n)`. Cada una de esas naturalezas tiene su carpeta y su resolutor especializado.

Una misma incognita, cuatro formas de plantearla:

```python
from sympy import symbols, solve, linsolve, dsolve, rsolve, Function, Eq

x, y = symbols("x y")
n = symbols("n", integer=True)
f = Function("f")
g = Function("g")

solve(x**2 - 4, x)                         # [-2, 2]              -> una incognita
linsolve([x + y - 3, x - y - 1], x, y)     # {(2, 1)}             -> sistema
dsolve(Eq(f(x).diff(x), f(x)), f(x))       # Eq(f(x), C1*exp(x))  -> EDO (funcion incognita)
rsolve(g(n) - 2*g(n-1), g(n))              # 2**n*C0              -> recurrencia (sucesion)
```

## Como se relacionan

Las cuatro subcarpetas se reparten el trabajo segun **que es** la incognita y como devuelven la solucion:

| Subcarpeta | Que resuelve | Incognita | Resolutor(es) |
|------------|--------------|-----------|---------------|
| [[sympy.solvers/algebraicas/index \| algebraicas]] | Ecuaciones de **una** incognita | un numero (o varios valores) | `solve`, `solveset`, `roots`, `nsolve` |
| [[sympy.solvers/sistemas/index \| sistemas]] | **Sistemas** de varias ecuaciones | una tupla de numeros | `linsolve`, `nonlinsolve` |
| [[sympy.solvers/diferenciales/index \| diferenciales]] | Ecuaciones **diferenciales** (EDOs) | una funcion continua `f(x)` | `dsolve` |
| [[sympy.solvers/recurrencias/index \| recurrencias]] | Relaciones de **recurrencia** | una sucesion `y(n)` | `rsolve` |

Arbol de decision — "¿que tengo que resolver?":

- **Una sola ecuacion con una incognita** (numero) -> [[sympy.solvers/algebraicas/index | algebraicas]]. Dentro, la eleccion fina (`solve` vs `solveset` vs `roots` vs `nsolve`) la decide ese index.
- **Varias ecuaciones con varias incognitas** (tupla) -> [[sympy.solvers/sistemas/index | sistemas]]: `linsolve` si es lineal, `nonlinsolve` si no lo es.
- **La incognita es una funcion** `f(x)` y aparecen sus **derivadas** -> [[sympy.solvers/diferenciales/index | diferenciales]] (`dsolve`).
- **La incognita es una sucesion** `y(n)` definida por sus terminos anteriores (`y(n-1)`, `y(n-2)`, …) -> [[sympy.solvers/recurrencias/index | recurrencias]] (`rsolve`).

> [!tip] Continuo vs discreto
> `dsolve` (diferenciales) y `rsolve` (recurrencias) son analogos: el primero despeja una funcion **continua** a partir de sus derivadas; el segundo, una sucesion **discreta** a partir de sus terminos previos. Ambos producen una solucion general con constantes (`C1`/`C0`) que se fijan con condiciones iniciales.

## Subtemas

- [[sympy.solvers/algebraicas/index | algebraicas]] — ecuaciones de una incognita; reune los cuatro resolutores de proposito general (clasico, moderno, polinomico y numerico) y explica cual usar.
- [[sympy.solvers/sistemas/index | sistemas]] — sistemas de ecuaciones; separa el caso lineal del no lineal, que tienen algoritmos distintos.
- [[sympy.solvers/diferenciales/index | diferenciales]] — EDOs; la incognita pasa a ser una funcion, lo que obliga a plantearla con `Function` y `Eq`.
- [[sympy.solvers/recurrencias/index | recurrencias]] — relaciones de recurrencia; el analogo discreto de las diferenciales.

## Notas relacionadas

- [[SymPy/index | SymPy]]
