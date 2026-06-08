---
title: simbolico vs numerico — por que SymPy trabaja con expresiones exactas
aliases:
  - simbolico vs numerico
  - exacto vs flotante
  - por que sympy
tags:
  - sympy
  - concepto
  - fundamentos
lib: sympy
mod: sympy
tipo: concepto
requiere:
  - concepto_expr_arbol
draft: false
---

# simbolico vs numerico — por que SymPy trabaja con expresiones exactas

## Definicion fundamental

Una libreria **numerica** (NumPy, SciPy, el `float` de Python) representa los numeros como **aproximaciones** de punto flotante y opera evaluando: `1/3` es `0.333...`. SymPy es **simbolico**: representa los objetos matematicos de forma **exacta** y los manipula como lo haria un humano con lapiz y papel. `sqrt(2)` no se evalua a `1.414...`, se conserva como la raiz exacta; `1/3` sigue siendo el numero racional `1/3`.

La consecuencia practica: SymPy puede **simplificar, derivar, integrar, factorizar y resolver** de forma exacta, mientras que una libreria numerica solo puede dar valores aproximados.

```python
import math
from sympy import Rational, sqrt

math.sqrt(2)        # 1.4142135623730951   -> flotante, ya perdio exactitud
sqrt(2)             # sqrt(2)               -> simbolico, exacto
sqrt(2) ** 2        # 2                     -> exacto, sin error de redondeo
Rational(1, 3) + Rational(1, 6)   # 1/2     -> aritmetica exacta de fracciones
```

## Por que existe esta division

El punto flotante es rapido pero **inexacto**: arrastra error de redondeo y no sabe que `sqrt(2)**2` es exactamente `2`. Para ingenieria numerica (simular, medir, graficar) eso basta y conviene por velocidad. Pero para **matematica exacta** —obtener la formula de una derivada, demostrar una identidad, resolver una ecuacion en forma cerrada— necesitas conservar la estructura simbolica. Son dos mundos con propositos distintos, no uno mejor que el otro.

```python
from sympy import symbols, integrate, cos

x = symbols("x")
integrate(cos(x), x)   # sin(x)   -> SymPy da la primitiva EXACTA, no un numero
```

## La regla central: exacto o aproximado

| Necesitas… | Usa | Tipo |
|------------|-----|------|
| la **formula** (derivada, integral, solucion en simbolos) | **SymPy** | simbolico |
| demostrar/simplificar una identidad | **SymPy** | simbolico |
| aritmetica exacta (fracciones, raices) | **SymPy** (`Rational`, `sqrt`) | simbolico |
| evaluar rapido sobre millones de datos | **NumPy/SciPy** | numerico |
| un **valor** numerico final | `evalf()` o `lambdify` sobre el resultado | puente |

> [!regla]
> Trabaja **simbolico el mayor tiempo posible** y pasa a numerico **solo al final**, cuando necesites un valor o graficar. El puente es [[concepto_evalf_lambdify|evalf / lambdify]].

## Exactitud: el detalle que mas sorprende

El mayor cambio mental frente a Python normal es que en SymPy **`/` entre enteros de Python da flotante**: hay que sympificar para obtener un `Rational`.

```python
from sympy import Rational, S, sqrt

1/3                 # 0.333...      -> Python puro: flotante (NO simbolico)
Rational(1, 3)      # 1/3           -> exacto
S(1)/3              # 1/3           -> exacto (S sympifica el 1)
sqrt(8)             # 2*sqrt(2)     -> simplificado exacto, no 2.828...
```

## Casos que confunden

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `1/3` da `0.333...` dentro de SymPy | division de enteros de Python, no simbolica | `Rational(1,3)` o `S(1)/3` |
| Aparece `1.4142...` en vez de `sqrt(2)` | algun operando ya era `float` | mantener todo simbolico; no mezclar `float` |
| Quieres un numero y queda `sqrt(2)` | SymPy no evalua salvo que se lo pidas | `.evalf()` o `float(...)` al final |
| Es lento sobre arrays grandes | SymPy no es para calculo masivo | compilar con `lambdify` a NumPy |

## Relacion con otros conceptos

- [[concepto_expr_arbol]]
- [[concepto_evalf_lambdify]]
- [[concepto_simplificacion_automatica]]
