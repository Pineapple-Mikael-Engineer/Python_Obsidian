---
title: sympy.solvers/recurrencias — recurrencias
tags:
  - sympy
  - indice
draft: false
---

# recurrencias

Esta carpeta cubre la resolucion de **relaciones de recurrencia** lineales con `rsolve`: dada una sucesion definida por sus terminos anteriores (como Fibonacci, `y(n) = y(n-1) + y(n-2)`), encontrar su **forma cerrada** `y(n)`, una expresion en funcion del indice `n` que evita iterar. Es el **analogo discreto** de [[sympy.dsolve]]: donde `dsolve` despeja una funcion continua a partir de sus derivadas, `rsolve` despeja una sucesion a partir de sus terminos previos. La recurrencia se plantea como una `Expr` igualada a `0` sobre una `Function` sin definir `y(n)`; sin condiciones iniciales devuelve la solucion general con constantes `C0, C1, …`, y con un diccionario `init` la solucion particular.

De la recurrencia a la formula cerrada de Fibonacci (Binet):

```python
from sympy import Function, symbols, rsolve
y = Function("y")
n = symbols("n", integer=True)

eq = y(n) - y(n-1) - y(n-2)                # F(n) = F(n-1) + F(n-2), igualada a 0
rsolve(eq, y(n))                           # C0*(1/2 - sqrt(5)/2)**n + C1*(1/2 + sqrt(5)/2)**n
rsolve(eq, y(n), {y(0): 0, y(1): 1})       # formula de Binet (constantes ya resueltas)
```

## Como se relacionan

Carpeta de un solo resolutor; el index fija el **paralelismo discreto-continuo** y el patron de planteamiento:

| Concepto | Recurrencias (`rsolve`) | Diferenciales (`dsolve`) |
|----------|-------------------------|--------------------------|
| Incognita | sucesion `y(n)` (`Function` aplicada al indice) | funcion `f(x)` (`Function` aplicada a la variable) |
| Se define por | terminos anteriores `y(n-1)`, `y(n-2)` | derivadas `f(x).diff(x)` |
| Solucion | forma cerrada `y(n)` (`Expr` en `n`) | `Eq(f(x), <expr>)` |
| Constantes | `C0, C1, …` | `C1, C2, …` |
| Condiciones | `init={y(0): a, y(1): b}` | `ics={f(0): a, …}` |

Claves para acertar:

- Plantea los indices **hacia atras** (`y(n)`, `y(n-1)`, `y(n-2)`) y pasa `y(n)`; la forma adelantada con `y(n+2)` puede fallar con `PolynomialError`.
- Declara el indice como entero: `symbols("n", integer=True)`.
- Hacen falta tantas condiciones en `init` como el **orden** de la recurrencia (orden 2 -> dos condiciones) para fijar todas las constantes.
- `rsolve` solo resuelve recurrencias **lineales**; si no halla solucion hipergeometrica cerrada devuelve `None`.

> [!info] Por que la forma cerrada
> Iterar `y(n)` cuesta `n` pasos; la forma cerrada que da `rsolve` evalua el termino `n`-esimo de golpe (`fib.subs(n, 10)` -> `55`) y permite analizar el crecimiento de la sucesion simbolicamente.

## Notas

- [[sympy.rsolve]] — resuelve relaciones de recurrencia lineales a forma cerrada; el analogo discreto de `dsolve`, con `init` jugando el papel de las condiciones iniciales.

## Notas relacionadas

- [[sympy.solvers/index | sympy.solvers]]
