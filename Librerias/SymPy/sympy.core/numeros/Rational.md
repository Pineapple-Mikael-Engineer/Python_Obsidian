---
title: Rational — fraccion exacta p/q de SymPy
aliases:
  - Rational
  - fraccion exacta
  - numero racional
tags:
  - sympy
  - api/clase
  - core/numeros
lib: sympy
mod: sympy.core.numbers
tipo: clase
retorna: Rational
requiere:
  - Integer
draft: false
---

# Rational — fraccion exacta p/q de SymPy

Representa un **numero racional exacto** `p/q` (un cociente de enteros) sin perdida de precision. A diferencia del `1/3` de Python —que es un `float` y vale `0.333...`—, `Rational(1, 3)` conserva la fraccion intacta y opera con aritmetica exacta de fracciones. Es la pieza con la que SymPy hace cuentas exactas; ver [[concepto_simbolico_vs_numerico]]. Se **auto-simplifica** al crearse: `Rational(2, 4)` se guarda ya como `1/2`.

## Constructor

```python
sympy.Rational(
    p,            # int | str | float: numerador, o la fraccion completa como str
    q=1,          # int: denominador (por defecto 1)
)                 # -> Rational  (o Integer si q divide a p)
```

## Formas basicas de construccion

| Objetivo | Llamada | Resultado |
|----------|---------|-----------|
| Fraccion desde enteros | `Rational(1, 3)` | `1/3` |
| Fraccion desde cadena | `Rational("1/3")` | `1/3` |
| Se reduce sola | `Rational(2, 4)` | `1/2` |
| Signo en denominador | `Rational(1, -2)` | `-1/2` |
| Denominador 1 -> `Integer` | `Rational(6, 3)` | `2` (tipo `Integer`) |

## Atributos clave

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `.p` | `int` | Numerador (ya reducido, signo incluido) |
| `.q` | `int` | Denominador (siempre positivo, `>= 1`) |

```python
from sympy import Rational

r = Rational(3, 7)
r.p        # 3
r.q        # 7

Rational(6, 8).p   # 3   -> se redujo: 6/8 = 3/4
Rational(6, 8).q   # 4
```

## Aritmetica exacta

Las operaciones entre `Rational` devuelven otro `Rational` exacto, sin error de redondeo:

```python
from sympy import Rational

Rational(1, 3) + Rational(1, 6)   # 1/2
Rational(2, 3) ** 2               # 4/9
Rational(1, 3) * 6                # 2   (Integer)
Rational(3, 4) - Rational(1, 4)   # 1/2
```

## Comparacion con el `1/3` de Python

El punto que mas confunde: `1/3` en Python es un **flotante**, no una fraccion. Por eso `Rational(1, 3)` y `1/3` **no** son iguales.

```python
from sympy import Rational

1 / 3                       # 0.3333333333333333   -> float de Python, inexacto
Rational(1, 3)              # 1/3                   -> fraccion exacta
Rational(1, 3) == 1/3       # False  -> 1/3 (float) no es exactamente 1/3
float(Rational(1, 3))       # 0.3333333333333333   -> al pedir float SI coincide
```

> [!regla]
> Para obtener un `Rational` a partir de enteros de Python, **no uses `/`**: `1/3` ya es float. Usa `Rational(1, 3)` o sympifica con `S(1)/3`. Ver [[concepto_simbolico_vs_numerico]].

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `Rational(1, 3) == 1/3` da `False` | `1/3` es un `float` inexacto, no la fraccion | Comparar contra otro `Rational` o usar `float(...)` |
| `Rational(0.1)` da una fraccion enorme | El `float` `0.1` ya es inexacto en binario | Pasar la cadena: `Rational("1/10")` |
| Esperabas `Rational` y sale `Integer` | El denominador divide al numerador | Es correcto: `6/3` es entero exacto `2` |
| `.q` negativo | No ocurre: el signo va siempre en `.p` | `Rational(1, -2).q` es `2`, `.p` es `-1` |

## Notas relacionadas

- [[Integer]]
- [[Float]]
- [[sympy.constantes_simbolicas]]
- [[concepto_simbolico_vs_numerico]]
- [[sympy.core/numeros/index | numeros]]
