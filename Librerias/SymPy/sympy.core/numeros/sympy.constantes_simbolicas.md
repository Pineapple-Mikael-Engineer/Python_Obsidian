---
title: sympy.constantes_simbolicas — pi, E, oo, I, nan, zoo y el acceso S
aliases:
  - constantes simbolicas
  - singletons de sympy
  - pi E oo I
tags:
  - sympy
  - concepto
  - core/numeros
lib: sympy
tipo: concepto
requiere:
  - Integer
  - Rational
draft: false
---

# sympy.constantes_simbolicas — pi, E, oo, I, nan, zoo y el acceso S

SymPy ofrece las constantes matematicas fundamentales como objetos **simbolicos exactos**, no como flotantes aproximados. `pi` no es `3.14159...`: es el simbolo exacto que se conserva en las expresiones y solo se evalua a numero cuando lo pides con `evalf()`. Lo mismo vale para `E`, el infinito `oo`, la unidad imaginaria `I` y los valores especiales `nan` y `zoo`. Todas estas constantes son **singletons** (un unico objeto compartido) y se pueden alcanzar tambien via `S`. Ver [[concepto_simbolico_vs_numerico]].

## Tabla de constantes

| Constante | Significado | Ejemplo |
|-----------|-------------|---------|
| `pi` | El numero pi, exacto | `pi.evalf()` -> `3.14159265358979` |
| `E` | Base del logaritmo natural (e) | `E.evalf()` -> `2.71828182845905` |
| `oo` | Infinito positivo (`+inf`) | `1/oo` -> `0`; `oo + 1` -> `oo` |
| `-oo` | Infinito negativo | `(-oo) < 0` -> `True` |
| `I` | Unidad imaginaria, `sqrt(-1)` | `I**2` -> `-1` |
| `nan` | "Not a number" (resultado indeterminado) | `nan` (se propaga en operaciones) |
| `zoo` | Infinito **complejo** (de modulo infinito, fase indefinida) | `1/0` simbolico -> `zoo` |
| `S` | Acceso a los singletons y atajo para sympificar | `S.Half`, `S.One`, `S(1)/3` |

## pi y E: exactos hasta que los evaluas

Permanecen simbolicos en las expresiones; con `evalf(n)` obtienes tantos digitos como quieras (precision arbitraria, ver [[Float]]).

```python
from sympy import pi, E, sin, cos

sin(pi)          # 0        -> SymPy lo simplifica exacto
cos(pi)          # -1
pi.evalf()       # 3.14159265358979
pi.evalf(30)     # 3.14159265358979323846264338328
E.evalf()        # 2.71828182845905
```

## oo y -oo: el infinito

`oo` (dos letras `o`) es `+infinito`; `-oo` es `-infinito`. Se comportan como en analisis matematico.

```python
from sympy import oo, limit, symbols

oo + 1           # oo
1 / oo           # 0
oo - oo          # nan      -> indeterminacion

x = symbols("x")
limit(1/x, x, 0, "+")   # oo
```

## I: la unidad imaginaria

`I` es `sqrt(-1)`. Permite trabajar con numeros complejos de forma exacta.

```python
from sympy import I, sqrt, simplify

I**2             # -1
(1 + I) * (1 - I)   # 2
sqrt(-1)         # I
```

## nan y zoo: valores especiales

- `nan` es el resultado indeterminado (como `0/0` o `oo - oo`); se **propaga** por las operaciones.
- `zoo` es el **infinito complejo**: modulo infinito con fase indefinida, lo que SymPy devuelve para `1/0` simbolico.

```python
from sympy import nan, zoo, S

nan == nan       # True   -> en SymPy si (a diferencia del nan de float)
S(1) / S(0)      # zoo    -> division por cero simbolica
zoo + 1          # zoo
```

> [!aviso]
> No confundir `oo` (infinito real con signo) con `zoo` (infinito complejo, sin direccion definida). `1/0` simbolico da `zoo`, no `oo`.

## S: el acceso a singletons

`S` es el **registro de singletons**. Sirve para dos cosas: alcanzar constantes con nombre y **sympificar** numeros de Python al vuelo para no caer en flotantes.

| Acceso | Es | Equivale a |
|--------|-----|-----------|
| `S.One` | `1` exacto | `Integer(1)` |
| `S.Zero` | `0` exacto | `Integer(0)` |
| `S.Half` | `1/2` exacto | `Rational(1, 2)` |
| `S.Pi` | `pi` | `pi` |
| `S.Infinity` | `oo` | `oo` |
| `S.NaN` | `nan` | `nan` |
| `S(1)` | sympifica el `int` 1 | `Integer(1)` |

```python
from sympy import S

S.Half           # 1/2
S.One            # 1
S(1) / 3         # 1/3    -> S sympifica el 1, asi la division es exacta (Rational)
1 / 3            # 0.333...   -> sin S, es float de Python
```

> [!regla]
> `S(1)/3` es el atajo idiomatico para forzar aritmetica **exacta** desde enteros de Python, equivalente a `Rational(1, 3)`. Ver [[concepto_simbolico_vs_numerico]].

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `pi` se trata como `3.14...` | `pi` es simbolico, no float | Usar `pi.evalf(n)` solo al final |
| Esperabas `oo` y sale `zoo` | `1/0` simbolico es infinito complejo | Es correcto: usar limites para el caso con signo |
| `nan` "contamina" todo el resultado | `nan` se propaga por diseño | Revisar la indeterminacion de origen (`0/0`, `oo-oo`) |
| `1/3` sigue dando float | No se sympifico | `S(1)/3` o `Rational(1, 3)` |
| Confundir `I` (imaginaria) con una variable | `I` es constante reservada | No nombrar simbolos `I`; usar otro nombre |

## Notas relacionadas

- [[Integer]]
- [[Rational]]
- [[Float]]
- [[concepto_simbolico_vs_numerico]]
- [[concepto_evalf_lambdify]]
- [[sympy.core/numeros/index | numeros]]
