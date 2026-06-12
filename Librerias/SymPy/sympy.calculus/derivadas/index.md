---
title: sympy.calculus/derivadas — derivadas
tags:
  - sympy
  - indice
draft: false
---

# derivadas

La **diferenciacion simbolica** en SymPy: calcular la derivada exacta de una expresion aplicando las reglas del calculo (producto, cociente, cadena), con soporte para ordenes superiores y derivadas parciales. El resultado es otra `Expr`, exacta y manipulable, no un valor numerico.

Esta carpeta es el ejemplo mas limpio del patron transversal de `sympy.calculus`: la **funcion** [[sympy.diff]] (en minuscula) *deriva ya* y devuelve el resultado; la **clase** [[Derivative]] (en mayuscula) *plantea* la derivada sin evaluarla y la deja diferida hasta `.doit()`. Misma sintaxis de simbolos y ordenes en ambas; lo unico que cambia es si el calculo se dispara o no.

```python
from sympy import symbols, diff, Derivative
x = symbols("x")

diff(x**2, x)              # 2*x   -> la funcion evalua ya
Derivative(x**2, x)        # Derivative(x**2, x)   -> la clase plantea sin evaluar
Derivative(x**2, x).doit() # 2*x   -> .doit() dispara el calculo
```

## Como se relacionan

| Aspecto | `diff` (funcion) | `Derivative` (clase) |
|---------|------------------|----------------------|
| Que hace al llamarla | **evalua** y devuelve la derivada | **no evalua**: deja la operacion diferida |
| Tipo de salida | `Expr` ya calculada | objeto `Derivative` (una `Expr` inerte) |
| Como obtener el valor | directo | con `.doit()` |
| Caso de uso | quiero el resultado | quiero **mostrar** o manipular la derivada |
| Funcion sin definir `f(x)` | devuelve un `Derivative` sin evaluar | lo construye explicitamente |

Hay un puente entre ambas: cuando `diff` **no sabe** derivar (p. ej. una `Function` sin definir), no falla — devuelve un `Derivative` sin evaluar, exactamente lo que `Derivative(...)` construye a mano. Son las dos caras del mismo dato.

## Notas

- [[sympy.diff | sympy.diff]] — la funcion que deriva y devuelve el resultado ya evaluado; tambien como metodo `f.diff(x)`.
- [[Derivative | Derivative]] — la clase que representa la derivada sin evaluar, para plantearla/mostrarla; se evalua con `.doit()`.

## Notas relacionadas

- [[sympy.calculus/index | sympy.calculus]]
