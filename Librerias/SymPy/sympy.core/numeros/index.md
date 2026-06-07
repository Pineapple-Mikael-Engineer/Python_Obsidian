---
title: sympy.core/numeros — numeros
tags:
  - sympy
  - indice
draft: false
---

# numeros

Los **valores numericos** del mundo simbolico y, sobre todo, la **exactitud** que distingue a SymPy de los flotantes de Python. Aqui viven los enteros y fracciones exactos ([[Integer]], [[Rational]]), el flotante de precision arbitraria [[Float]] y las constantes matematicas simbolicas ([[sympy.constantes_simbolicas]]: `pi`, `E`, `oo`, `I`, junto al acceso `S`). Son los ladrillos numericos con los que se construye una `Expr`; la idea de fondo —cuando un calculo es exacto y cuando aproximado— esta en [[concepto_simbolico_vs_numerico]].

El punto que mas confunde: `1/3` en Python es un `float` (`0.333…`), mientras que `Rational(1, 3)` o `S(1)/3` conservan la fraccion intacta. Basta con que **un** operando sea SymPy para que toda la operacion sea exacta.

```python
from sympy import Rational, Integer, Float, pi, S

Rational(1, 3) + Rational(1, 6)   # 1/2                -> aritmetica exacta
S(1)/3                            # 1/3                -> atajo idiomatico
Float("0.1", 30)                  # 0.1 con 30 digitos -> precision arbitraria
pi.evalf(30)                      # 3.14159265358979...-> constante exacta evaluada
```

## Como se relacionan

Los tres tipos numericos se reparten segun **que precision necesitas**; las constantes son simbolos especiales que se quedan exactos hasta que los evaluas.

| Tipo | Exacto o aproximado | Cuando usarlo |
|------|---------------------|---------------|
| [[Integer]] | **Exacto** | Enteros; surge solo al operar `int` de Python con SymPy |
| [[Rational]] | **Exacto** | Fracciones `p/q`; la pieza con la que SymPy hace cuentas exactas |
| [[Float]] | **Aproximado** (precision arbitraria) | Un valor numerico con muchos digitos; salida de `evalf` |
| [[sympy.constantes_simbolicas]] | **Exacto** (simbolico) | `pi`, `E`, `oo`, `I`, `S`; permanecen simbolicos hasta `evalf` |

Relacion clave: `Integer` y `Rational` viven en el mundo **exacto** y se contagian entre si (`Integer(1)/3 → Rational`); en cuanto entra un `Float` (o un `float` de Python), todo el resultado **cae a flotante** y pierde exactitud. Por eso conviene mantenerse simbolico y pasar a `Float` solo al final, normalmente via `evalf`.

## Notas

- [[Integer]] — Entero exacto; el `int` de Python se sympifica a `Integer` al operar con expresiones, y su `/` da `Rational`, no `float`.
- [[Rational]] — Fraccion exacta `p/q`; se auto-simplifica al crearse y es el nucleo de la aritmetica exacta. Contrasta con el `1/3` flotante de Python.
- [[Float]] — Coma flotante de **precision arbitraria** (mpmath): no es exacto como `Rational`, pero lleva tantos digitos como pidas; es el tipo al que llega `evalf`.
- [[sympy.constantes_simbolicas]] — Las constantes (`pi`, `E`, `oo`, `I`, `nan`, `zoo`) como singletons exactos, mas el acceso `S` que tambien fuerza exactitud (`S(1)/3`).

## Notas relacionadas

- [[sympy.core/index | sympy.core]]
- [[concepto_simbolico_vs_numerico]]
- [[concepto_evalf_lambdify]]
- [[Tree SymPy]]
