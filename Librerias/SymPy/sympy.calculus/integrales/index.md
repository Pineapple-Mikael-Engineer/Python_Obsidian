---
title: sympy.calculus/integrales — integrales
tags:
  - sympy
  - indice
draft: false
---

# integrales

La **integracion simbolica** en SymPy: hallar la antiderivada (integral **indefinida**) o el area exacta sobre un intervalo (integral **definida**), trabajando de forma exacta con reglas analiticas, el algoritmo de Risch y tablas de patrones. Soporta limites infinitos con `oo`, integrales multiples e integrandos con parametros simbolicos. Es la operacion inversa de la derivacion ([[sympy.diff]]).

Como toda la seccion, sigue el patron **funcion-vs-clase-sin-evaluar**: la **funcion** [[sympy.integrate]] (en minuscula) *integra ya* y devuelve el resultado; la **clase** [[Integral]] (en mayuscula) *plantea* la integral sin resolverla y la deja diferida hasta `.doit()`. La distincion indefinida/definida la marca el segundo argumento: un **simbolo suelto** `x` da la antiderivada; una **tupla** `(x, a, b)` da la definida.

```python
from sympy import symbols, integrate, Integral
x = symbols("x")

integrate(x**2, x)              # x**3/3   -> indefinida (sin +C)
integrate(x**2, (x, 0, 1))     # 1/3      -> definida, exacta
Integral(x**2, (x, 0, 1))      # Integral(x**2, (x, 0, 1))   -> planteada, sin evaluar
Integral(x**2, (x, 0, 1)).doit() # 1/3
```

> La integral indefinida **no incluye `+C`**: `integrate(2*x, x)` da `x**2`, no `x**2 + C`.

## Como se relacionan

| Aspecto | `integrate` (funcion) | `Integral` (clase) |
|---------|-----------------------|--------------------|
| Que hace al llamarla | **evalua** y devuelve la primitiva/area | **no evalua**: deja la operacion planteada |
| Tipo de salida | `Expr` ya calculada | objeto `Integral` (una `Expr` inerte) |
| Como obtener el valor | directo | con `.doit()` |
| Caso de uso | quiero el resultado | quiero **mostrar** el simbolo ∫ o manipularlo |
| Sin primitiva elemental | devuelve un `Integral` sin evaluar | lo construye explicitamente |

Indefinida (simbolo `x`) y definida (tupla `(x, a, b)`) conviven en ambas formas. Y hay el mismo puente que en derivadas: cuando `integrate` no halla primitiva en forma cerrada devuelve un `Integral` sin evaluar — lo que `Integral(...)` construye a mano. De hecho `integrate(f, x)` equivale a `Integral(f, x).doit()`.

## Notas

- [[sympy.integrate | sympy.integrate]] — la funcion que integra ya; indefinida con `x`, definida con `(x, a, b)`, multiples con varias tuplas.
- [[Integral | Integral]] — la clase que plantea la integral sin resolverla, para mostrarla o retrasar el calculo; se evalua con `.doit()`.

## Notas relacionadas

- [[sympy.calculus/index | sympy.calculus]]
- [[Tree SymPy]]
