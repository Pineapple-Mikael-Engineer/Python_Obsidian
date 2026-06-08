---
title: introduccion — que es SymPy y como empezar
aliases: [introduccion sympy, sympy intro]
tags: [sympy, api/concepto, introduccion]
lib: sympy
mod: sympy
tipo: concepto
draft: false
---

# introduccion — que es SymPy y como empezar

SymPy es una biblioteca de **matematica simbolica** para Python, de codigo abierto y sin dependencias externas (solo Python puro). Nacio en 2006 como alternativa libre a Mathematica y Maple: permite derivar, integrar, factorizar, resolver ecuaciones y simplificar expresiones de forma **exacta**, conservando la estructura algebraica en lugar de aproximarla con flotantes. La diferencia clave frente a NumPy es de naturaleza: NumPy opera sobre arrays de numeros de punto flotante (rapido, aproximado); SymPy opera sobre **expresiones simbolicas exactas** (lento para calculo masivo, exacto para matematica formal). El puente entre ambos mundos es `lambdify`.

## Instalacion

```
pip install sympy
```

Import estandar para sesiones interactivas (trae todo el namespace al frente):

```python
from sympy import *
```

En produccion o scripts, preferir imports especificos para evitar colisiones de nombres:

```python
from sympy import symbols, diff, integrate, solve, lambdify, sqrt, Rational
```

## La idea central

Todo en SymPy es una instancia de [[concepto_expr_arbol|Expr]], un arbol de expresion inmutable. Los simbolos no son variables de Python con valor: son objetos algebraicos que hay que declarar explicitamente con `symbols`. SymPy **no evalua** mas alla de lo trivial; conserva la forma exacta hasta que se le pida un valor numerico.

```python
from sympy import symbols, sqrt, Rational

x = symbols("x")

sqrt(8)        # 2*sqrt(2)   — exacto, no 2.828...
Rational(1,3)  # 1/3         — no 0.333...
x + x          # 2*x         — auto-simplifica lo obvio, nada mas
```

Los tres ejemplos ilustran el contrato: SymPy simplifica cuando la simplificacion es obvia e inequivoca, pero no colapsa a flotante ni expande ni factoriza sin pedirlo. La exactitud es la norma, la aproximacion numerica es opt-in.

## Cuando usar SymPy

| Necesidad | Herramienta |
|-----------|-------------|
| Resultado exacto (radicales, pi, fracciones) | SymPy |
| Derivar \| integrar \| resolver en forma cerrada | SymPy |
| Calculo numerico masivo (arrays grandes) | NumPy / SciPy |
| Simulacion, optimizacion numerica | SciPy |
| Generar codigo a partir de expresiones | SymPy -> `lambdify` / `ccode` |

La regla practica: **trabaja simbolico el mayor tiempo posible** y pasa a numerico solo al final, cuando necesites un valor concreto o graficar sobre datos. Mezclar flotantes de Python con expresiones SymPy contamina la precision y suele dar resultados inesperados.

## Flujo tipico

El patron mas comun en ingenieria: obtener la formula simbolica, verificarla con SymPy, y compilarla a NumPy para evaluacion masiva.

```python
from sympy import symbols, diff, integrate, solve, lambdify
import numpy as np

x = symbols("x")

f = x**3 - 3*x + 2
diff(f, x)           # 3*x**2 - 3
solve(f, x)          # [-2, 1]              — exacto

f_num = lambdify(x, f, "numpy")
f_num(np.linspace(-2, 2, 5))   # array([ 0., 3.375, 2., 0.625, 0.])
```

`diff` devuelve una `Expr`; `solve` devuelve una lista de soluciones exactas; `lambdify` convierte la `Expr` en una funcion Python/NumPy evaluable sobre arrays.

## Como navegar este modulo

El vault esta organizado por submodulo funcional. Ruta recomendada de entrada:

- Empezar por `[[conceptos_transversales/index | conceptos_transversales]]` — el modelo mental: que es una `Expr`, como funcionan los supuestos, diferencia exacto vs flotante, `evalf` y `lambdify`.
- Luego `[[sympy.core/index | sympy.core]]` — simbolos, numeros exactos (`Rational`, `Integer`), expresiones y sustitucion (`subs`).
- Calculo: `[[sympy.calculus/index | sympy.calculus]]` — derivadas, integrales, limites, series.
- Ecuaciones: `[[sympy.solvers/index | sympy.solvers]]` — `solve`, `solveset`, `dsolve`, sistemas.
- Ver el roadmap completo (todos los submodulos y estado de cobertura) en `[[Tree SymPy]]`.

## Notas relacionadas

- [[concepto_simbolico_vs_numerico]]
- [[concepto_expr_arbol]]
- [[Tree SymPy]]
- [[SymPy/index | SymPy]]
