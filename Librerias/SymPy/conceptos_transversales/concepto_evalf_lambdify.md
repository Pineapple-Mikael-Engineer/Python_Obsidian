---
title: de simbolico a numerico — subs, evalf y lambdify
aliases:
  - evalf
  - lambdify
  - simbolico a numerico
tags:
  - sympy
  - concepto
  - fundamentos
lib: sympy
tipo: concepto
requiere:
  - concepto_simbolico_vs_numerico
draft: false
---

# de simbolico a numerico — subs, evalf y lambdify

## Definicion fundamental

El flujo tipico es: **manipular simbolico** y, al final, **obtener numeros**. Tres herramientas cubren ese puente, de menos a mas escala:

- **`subs`** — sustituye simbolos por valores (numericos o simbolicos). Sigue siendo exacto.
- **`evalf`** — evalua a un **flotante de precision arbitraria** (un valor).
- **`lambdify`** — **compila** la expresion a una funcion Python/NumPy rapida, para evaluar sobre **muchos** datos.

```python
from sympy import symbols, sqrt, lambdify
x = symbols("x")
e = sqrt(x) + 1

e.subs(x, 2)          # sqrt(2) + 1     -> exacto, aun simbolico
e.subs(x, 2).evalf()  # 2.41421356...   -> un numero
f = lambdify(x, e, "numpy")
f(2)                  # 2.41421356...   -> funcion numerica rapida
```

## subs: sustituir manteniendo exactitud

`subs` reemplaza un simbolo (o subexpresion) por otro valor y **devuelve una nueva expresion** (las expresiones son inmutables). El resultado puede seguir siendo simbolico.

```python
from sympy import symbols
x, y = symbols("x y")
e = x**2 + y
e.subs(x, 3)             # y + 9
e.subs({x: 3, y: 2})     # 11             -> varias a la vez (dict)
e.subs(x, y + 1)         # y + (y + 1)**2 -> sustitucion simbolica
```

## evalf: un numero con la precision que pidas

`evalf(n)` evalua a `n` digitos significativos (por defecto 15). `float(expr)` hace lo mismo y devuelve un `float` nativo. Si quedan simbolos libres, no puede dar un numero.

```python
from sympy import pi, sqrt
pi.evalf()        # 3.14159265358979
pi.evalf(30)      # 3.14159265358979311599796346854   -> 30 digitos
sqrt(2).evalf()   # 1.41421356237310
float(sqrt(2))    # 1.4142135623730951                -> float nativo
```

> [!warning]
> `evalf` evalua **un** valor. Para evaluar la misma expresion en miles de puntos (graficar, simular), `evalf` en bucle es **lento**: usa `lambdify`.

## lambdify: el puente a NumPy para datos masivos

`lambdify(vars, expr, "numpy")` genera una **funcion vectorizada** que opera sobre arrays de NumPy, traduciendo `sin`, `exp`, etc. a sus equivalentes numericos. Es como se conecta SymPy con [[concepto_simbolico_vs_numerico|el mundo numerico]] de NumPy/SciPy.

```python
import numpy as np
from sympy import symbols, sin, lambdify
x = symbols("x")
f = lambdify(x, sin(x)/x, "numpy")
xs = np.linspace(0.1, 10, 1000)
ys = f(xs)            # array de 1000 valores, rapido
```

## Que herramienta usar

| Objetivo | Herramienta | Resultado |
|----------|-------------|-----------|
| fijar el valor de un simbolo | `subs` | expresion (puede seguir simbolica) |
| un unico numero, alta precision | `evalf` / `float` | flotante |
| evaluar sobre un array / graficar | `lambdify(..., "numpy")` | funcion vectorizada |
| derivar/integrar y LUEGO numerar | simbolico primero, `lambdify` al final | lo mejor de ambos |

## Casos que confunden

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `evalf` deja simbolos, no da numero | quedan simbolos libres sin valor | `subs` esos simbolos antes de `evalf` |
| graficar con SymPy es lentisimo | `evalf`/`subs` en bucle sobre miles de puntos | compilar con `lambdify` una sola vez |
| `lambdify` falla con una funcion rara | sin equivalente en el backend numpy | usar `"mpmath"`/`"sympy"` o `modules=` propio |
| `TypeError` al pasar un array a `subs` | `subs` es sustitucion simbolica, no vectorizada | usar `lambdify` |

## Relacion con otros conceptos

- [[concepto_simbolico_vs_numerico]]
- [[concepto_expr_arbol]]
- [[concepto_simplificacion_automatica]]
