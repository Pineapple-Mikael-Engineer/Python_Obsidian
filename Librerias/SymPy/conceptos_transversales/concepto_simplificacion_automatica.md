---
title: simplificacion automatica — lo que SymPy simplifica solo y lo que no
aliases:
  - simplificacion automatica
  - auto simplify
  - simplify vs automatico
tags:
  - sympy
  - concepto
  - fundamentos
lib: sympy
tipo: concepto
requiere:
  - concepto_expr_arbol
draft: false
---

# simplificacion automatica — lo que SymPy simplifica solo y lo que no

## Definicion fundamental

SymPy aplica una **simplificacion automatica** ligera al **construir** cada expresion: ciertas reescrituras baratas y siempre validas se hacen solas, sin que las pidas. Pero la mayoria de las transformaciones (factorizar, simplificar identidades, combinar trigonometria) **no** son automaticas: hay que invocarlas explicitamente con `simplify`, `expand`, `factor`, etc.

```python
from sympy import symbols
x = symbols("x")
x + x          # 2*x        -> automatico
x * x          # x**2       -> automatico
x - x          # 0          -> automatico
2*x + 3*x      # 5*x        -> automatico (combina coeficientes)
```

## Que se hace solo (automatico)

| Entrada | Resultado | Por que |
|---------|-----------|---------|
| `x + x` | `2*x` | combina terminos iguales |
| `x*x*x` | `x**3` | junta potencias de la misma base |
| `0*x`, `x - x` | `0` | identidades triviales |
| `1*x`, `x**1` | `x` | elementos neutros |
| `Rational(2,4)` | `1/2` | normaliza racionales |
| `b + a` | `a + b` | orden canonico |

La auto-simplificacion es **barata y conservadora**: solo lo que es siempre cierto y rapido. Reordenar a una **forma canonica** permite que `x + y` y `y + x` sean el mismo arbol.

## Que NO se hace solo (hay que pedirlo)

| Quieres | Funcion | Ejemplo |
|---------|---------|---------|
| desarrollar productos | `expand` | `(x+1)**2 -> x**2+2*x+1` |
| factorizar | `factor` | `x**2-1 -> (x-1)*(x+1)` |
| identidades trigonometricas | `trigsimp` | `sin(x)**2+cos(x)**2 -> 1` |
| simplificar en general | `simplify` | heuristica que prueba varias |
| cancelar fraccion racional | `cancel` | `(x**2-1)/(x-1) -> x+1` |

```python
from sympy import sin, cos, simplify, expand, factor
sin(x)**2 + cos(x)**2            # sin(x)**2 + cos(x)**2   -> NO automatico
simplify(sin(x)**2 + cos(x)**2)  # 1
expand((x + 1)**2)               # x**2 + 2*x + 1
factor(x**2 - 1)                 # (x - 1)*(x + 1)
```

> [!regla]
> No esperes que SymPy "adivine" la forma que quieres. La auto-simplificacion solo hace lo trivial; para todo lo demas **elige la herramienta concreta** (`expand`, `factor`, `trigsimp`…). `simplify` es el comodin, pero es lento y no siempre da la forma deseada.

## Exactitud: cuidado con mezclar flotantes

La auto-simplificacion mantiene la exactitud **si todo es simbolico**. En cuanto entra un `float`, SymPy lo propaga y pierdes la forma exacta. Manten [[concepto_simbolico_vs_numerico|todo simbolico]] hasta el final.

```python
from sympy import Rational, sqrt
sqrt(8)              # 2*sqrt(2)    -> simplificacion exacta automatica
x + 1.0*x            # 2.0*x        -> el float contamina (no 2*x)
Rational(1,2) + 0.5  # 1.00000000000000   -> el float gana, deja de ser 1/2
```

## Casos que confunden

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| una identidad "obvia" no se simplifica sola | no es automatica | llamar `simplify`/`trigsimp`/`factor` |
| `simplify` no da la forma que quiero | es heuristica, no canonica | usar la funcion especifica (`factor`, `expand`…) |
| aparecen `2.0*x` en vez de `2*x` | se colo un `float` | usar `Rational`/`Integer`, no literales con punto |
| dos formas "iguales" no son `==` | `==` es estructural, no simplifica | comparar `simplify(a-b) == 0` |

## Relacion con otros conceptos

- [[concepto_expr_arbol]]
- [[concepto_simbolico_vs_numerico]]
- [[concepto_symbols_assumptions]]
