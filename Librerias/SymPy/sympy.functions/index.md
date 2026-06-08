---
title: sympy.functions — funciones matematicas simbolicas
tags:
  - sympy
  - indice
draft: false
---

# sympy.functions

Este submodulo agrupa las **funciones matematicas simbolicas** de SymPy: desde las elementales de calculo (raiz cuadrada, exponencial, logaritmo, trigonometricas, hiperbolicas, valor absoluto) hasta las funciones especiales de matematica avanzada (gamma, factorial, funciones a trozos, escalon de Heaviside, delta de Dirac). La diferencia con Python puro es que estas funciones operan sobre **expresiones exactas**: `sin(pi/6)` devuelve `Rational(1, 2)`, no `0.4999...`.

El punto de partida: en SymPy las funciones matematicas son **objetos simbolicos** (nodos del arbol de expresion), no rutinas numericas. Esto permite derivarlas, integrarlas, sustituirles valores y simplificarlas con exactitud.

```python
from sympy import symbols, sin, cos, exp, log, sqrt, gamma, pi, Rational

x = symbols("x")

# Evaluacion exacta en valores especiales
sin(pi/6)                     # 1/2
cos(pi)                       # -1
sqrt(8)                       # 2*sqrt(2)
exp(log(x))                   # x

# Las funciones se derivan e integran simbolicamente
from sympy import diff, integrate
diff(sin(x), x)               # cos(x)
integrate(cos(x), x)          # sin(x)

# Funciones especiales: exactitud mas alla del calculo
gamma(Rational(1, 2))         # sqrt(pi)
```

## Como se relacionan

| Carpeta | Que contiene | Cuando |
|---------|-------------|--------|
| [[sympy.functions/elementales/index \| elementales]] | `sqrt`, `exp`/`log`, trigonometricas, hiperbolicas, `Abs` | Calculo estandar: derivar, integrar, resolver ecuaciones con estas funciones |
| [[sympy.functions/especiales/index \| especiales]] | `gamma`, `factorial`/`binomial`, `Piecewise`, `Heaviside`/`DiracDelta` | Combinatoria, probabilidad, funciones a trozos, sistemas de control y senales |

La frontera es la frecuencia de uso: las `elementales` aparecen en casi cualquier problema de matematica; las `especiales` son esenciales en dominios concretos (estadistica, control, teoria de numeros) pero menos ubicuas.

> [!info] Supuestos como palanca
> Muchas funciones se simplifican solo si los simbolos llevan supuestos. `sqrt(x**2)` permanece como `sqrt(x**2)` sin supuestos; con `symbols("x", positive=True)` devuelve `x`. Definir bien los supuestos en [[concepto_symbols_assumptions]] es mas barato que forzar simplificaciones a posteriori.

## Subtemas

- [[sympy.functions/elementales/index | elementales]] — `sqrt`, `exp`, `log`, `sin`/`cos`/`tan`, `sinh`/`cosh`/`tanh`, `Abs`: las funciones del calculo basico.
- [[sympy.functions/especiales/index | especiales]] — `gamma`, `factorial`, `binomial`, `Piecewise`, `Heaviside`, `DiracDelta`: matematica avanzada y funciones a trozos.

## Notas relacionadas

- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
- [[concepto_symbols_assumptions]]
- [[sympy.simplify/trig_y_radicales/index | trig_y_radicales]]
