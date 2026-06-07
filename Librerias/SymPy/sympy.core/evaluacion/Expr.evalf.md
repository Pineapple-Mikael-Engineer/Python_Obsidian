---
title: Expr.evalf — evaluar una expresion a flotante de precision arbitraria
aliases:
  - evalf
  - Expr.evalf
  - N
tags:
  - sympy
  - api/metodo
  - core/evaluacion
lib: sympy
mod: sympy.core
tipo: metodo
obj: Expr
retorna: Float
requiere:
  - concepto_evalf_lambdify
draft: false
---

# Expr.evalf — evaluar una expresion a flotante de precision arbitraria

Metodo de cualquier `Expr` que la evalua numericamente a un **`Float` de precision arbitraria** de `n` digitos significativos (15 por defecto). Es el paso del mundo exacto al numerico para **un** valor: convierte constantes como `pi`, `sqrt(2)` o el resultado de una integral en un numero concreto con tantos digitos como pidas. Si en la expresion quedan **simbolos libres** sin valor, no puede dar un numero y los deja sin evaluar; para fijarlos se usa el argumento `subs`. Para evaluar la misma expresion sobre **muchos** datos (arrays, graficas) `evalf` en bucle es lento: ahi se usa [[sympy.lambdify]]. El flujo completo simbolico → numerico esta en [[concepto_evalf_lambdify]].

## Firma

```python
Expr.evalf(
    n=15,            # int: digitos significativos de precision
    subs=None,       # dict: {simbolo: valor} para fijar simbolos libres
    maxn=100,        # int: precision interna maxima al refinar
    chop=False,      # bool | float: anula colas numericas espurias (p. ej. ~1e-20)
    strict=False,    # bool: si True, lanza si no logra evaluar a numero
    ...
) -> Float
```

> `N(expr, n)` y `sympify(...).n(...)` son alias de `evalf`: `N(pi, 30)` equivale a `pi.evalf(30)`.

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Expresion sin simbolos libres | `Float` | Numero de `n` digitos (tipo SymPy, no `float` nativo) |
| Expresion con parte imaginaria | `Float`/`Add` | `re + im*I`, cada parte como `Float` |
| Quedan simbolos libres | `Expr` | Devuelve una expresion, **no** un numero |

```python
from sympy import pi
type(pi.evalf())    # <class 'sympy.core.numbers.Float'>
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Evaluar a 15 digitos | `expr.evalf()` |
| Evaluar a 30 digitos | `expr.evalf(30)` |
| Fijar simbolos y evaluar | `expr.evalf(subs={x: 2})` |
| Limpiar colas numericas | `expr.evalf(chop=True)` |
| Forma funcional | `N(expr, 30)` |

## Parametros en detalle

### `n` (digitos de precision)

Numero de **digitos significativos** del resultado (por defecto 15, similar a un `float` de doble precision). Subirlo da precision arbitraria real, no solo formato.

```python
from sympy import pi, sqrt
pi.evalf()          # 3.14159265358979
pi.evalf(30)        # 3.14159265358979311599796346854
sqrt(2).evalf(50)   # 1.4142135623730950488016887242096980785696718753769
```

### `subs`

Diccionario `{simbolo: valor}` que **fija los simbolos libres** justo antes de evaluar. Equivale a `expr.subs(...).evalf()` pero en un solo paso y mas estable numericamente.

```python
from sympy import symbols, sqrt
x, y = symbols("x y")
e = sqrt(x) + y

e.evalf(subs={x: 2, y: 1})   # 2.41421356237310
e.subs({x: 2, y: 1}).evalf() # 2.41421356237310   -> equivalente
```

### `chop`

Con `chop=True` reemplaza por cero las **colas numericas espurias** (residuos como `1e-21` por error de redondeo). Util cuando el resultado deberia ser real/entero pero arrastra ruido.

```python
from sympy import exp, I, pi
(exp(I*pi)).evalf()           # -1.0 + 1.22464679914735e-16*I
(exp(I*pi)).evalf(chop=True)  # -1.00000000000000   -> sin la cola imaginaria
```

## Casos de uso

### Numerar un resultado simbolico exacto

```python
from sympy import symbols, integrate, exp, oo
x = symbols("x")
I = integrate(exp(-x**2), (x, 0, oo))   # sqrt(pi)/2   -> exacto
I.evalf()                               # 0.886226925452758
```

### evalf vs float nativo

`float(expr)` hace lo mismo pero devuelve un `float` de Python (doble precision fija); `evalf(n)` permite **mas** digitos y devuelve un `Float` de SymPy.

```python
from sympy import sqrt
float(sqrt(2))     # 1.4142135623730951        -> float nativo de Python
sqrt(2).evalf()    # 1.41421356237310          -> Float de SymPy (15 digitos)
sqrt(2).evalf(40)  # 1.414213562373095048801688724209698078570  -> 40 digitos
```

## Errores comunes

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `evalf` devuelve una expresion, no un numero | quedan simbolos libres sin valor | pasar `subs={...}` o sustituirlos antes |
| El resultado arrastra una cola `1e-1x*I` | redondeo en partes que deberian ser 0 | `evalf(chop=True)` |
| `TypeError: can't convert expression to float` con `float()` | `float()` exige numero puro, no tolera simbolos | usar `evalf(subs=...)` o fijar simbolos primero |
| Mas digitos no cambian el valor mostrado | `init_printing`/repr recorta la salida, no el `Float` | el `Float` interno si tiene la precision; usar `print` o `str` |
| `evalf` en bucle sobre miles de puntos es lentisimo | `evalf` evalua un valor por llamada | compilar con `lambdify(..., "numpy")` una sola vez |

## Notas relacionadas

- [[sympy.lambdify]]
- [[concepto_evalf_lambdify]]
- [[sympy.core/evaluacion/index | evaluacion]]
