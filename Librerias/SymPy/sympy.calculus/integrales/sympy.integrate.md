---
title: sympy.integrate — integral simbolica indefinida y definida
aliases:
  - integrate
  - sympy.integrate
  - integral simbolica
tags:
  - sympy
  - api/funcion
  - calculus/integrales
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Symbol
  - Integral
draft: false
---

# sympy.integrate — integral simbolica indefinida y definida

`integrate(f, x)` calcula la **integral indefinida** (antiderivada) de `f` respecto a `x`, e `integrate(f, (x, a, b))` la **integral definida** sobre `[a, b]`. Trabaja de forma **exacta y simbolica**: devuelve una `Expr` (no un flotante), aplicando reglas analiticas, el algoritmo de Risch y tablas de patrones. Soporta limites infinitos con `oo`, integrales **multiples** encadenando tuplas de limites, e integrandos con parametros simbolicos. Cuando **no encuentra primitiva en forma cerrada**, devuelve un objeto [[Integral]] sin evaluar en vez de fallar.

> La integral indefinida **NO incluye la constante `+C`**: `integrate(2*x, x)` da `x**2`, no `x**2 + C`. Si la necesitas, agregala a mano con un `Symbol("C")`.

## Firma

```python
sympy.integrate(
    f,                   # Expr: integrando
    *symbols,            # var indefinida: x   |   definida: (x, a, b)   |   multiple: (x, a, b), (y, c, d)
    meijerg=None,        # bool | None: forzar/evitar el metodo de G de Meijer
    conds="piecewise",   # str: como reportar condiciones de convergencia ('piecewise'|'separate'|'none')
    risch=None,          # bool | None: forzar el algoritmo de Risch
    manual=None,         # bool | None: integracion paso a paso estilo manual
    ...
) -> Expr
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Halla primitiva | `Expr` | La antiderivada (indefinida) o el numero/expresion del area (definida) |
| No halla primitiva | `Integral` | La integral **sin evaluar**; representa el planteamiento, ver [[Integral]] |

```python
from sympy import symbols, integrate
x = symbols("x")
integrate(2*x, x)          # x**2   -> Expr, sin +C
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Integral indefinida | `integrate(f, x)` |
| Integral definida | `integrate(f, (x, a, b))` |
| Limite superior infinito | `integrate(f, (x, 0, oo))` |
| Toda la recta real | `integrate(f, (x, -oo, oo))` |
| Integral doble | `integrate(f, (x, a, b), (y, c, d))` |
| Misma var, varias indefinidas | `integrate(f, x, y)` |

## Parametros en detalle

### `f` (obligatorio)

El integrando, una `Expr`. Puede llevar parametros simbolicos ademas de la variable de integracion; el resultado queda en funcion de ellos.

```python
from sympy import symbols, integrate
x, k = symbols("x k")
integrate(k*x, x)          # k*x**2/2   -> sigue simbolico en k
```

### Variable indefinida `x`

Con un **simbolo suelto** calcula la antiderivada. El resultado es otra `Expr` cuya derivada recupera `f`.

```python
from sympy import symbols, integrate, cos
x = symbols("x")
integrate(cos(x), x)       # sin(x)
integrate(1/x, x)          # log(x)
```

### Limites definidos `(x, a, b)`

Una **tupla** `(variable, inferior, superior)` produce la integral definida (un numero exacto o una expresion en los parametros). Aplica el teorema fundamental internamente.

```python
from sympy import symbols, integrate
x = symbols("x")
integrate(x**2, (x, 0, 1))     # 1/3   -> exacto, no 0.333...
```

### Limites infinitos con `oo`

Usa `oo` (y `-oo`) de SymPy, no `float('inf')`, para **integrales impropias**. SymPy evalua el limite de forma exacta.

```python
from sympy import symbols, integrate, exp, oo, sqrt, pi
x = symbols("x")
integrate(exp(-x), (x, 0, oo))         # 1
integrate(exp(-x**2), (x, -oo, oo))    # sqrt(pi)
```

### Integrales multiples (varias tuplas)

Encadena tuplas de limites: se integra de **dentro hacia afuera** (la primera tupla es la integral mas interna).

```python
from sympy import symbols, integrate
x, y = symbols("x y")
integrate(x*y, (x, 0, 1), (y, 0, 1))   # 1/4
```

### Cuando no hay primitiva elemental

Algunos integrandos no tienen antiderivada en funciones elementales; SymPy devuelve una **funcion especial** si la conoce, o un [[Integral]] sin evaluar si no.

```python
from sympy import symbols, integrate, sin, Function
x = symbols("x")
integrate(sin(x)/x, x)     # Si(x)   -> seno integral (funcion especial)

f = Function("f")
integrate(f(x), x)         # Integral(f(x), x)   -> sin evaluar
```

## Casos de uso

### Area bajo una curva

```python
from sympy import symbols, integrate, sin, pi
x = symbols("x")
integrate(sin(x), (x, 0, pi))      # 2
```

### Trabajo de una fuerza variable

```python
from sympy import symbols, integrate, exp
x = symbols("x")
F = 50 * exp(-x/2)                 # fuerza en funcion de la posicion
integrate(F, (x, 0, 2))            # 100 - 100*exp(-1)  -> exacto
```

### Formula parametrica reutilizable

```python
from sympy import symbols, integrate
x, n = symbols("x n")
integrate(x**n, x)                 # Piecewise((x**(n+1)/(n+1), Ne(n,-1)), (log(x), True))
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar `+C` en la indefinida | SymPy omite la constante de integracion | Agregar `+ Symbol("C")` a mano si hace falta |
| Resultado es un `Integral` sin evaluar | No hay primitiva cerrada conocida | Aceptarlo, usar `.doit()` numerico via `evalf`, o reformular |
| `inf` en lugar de `oo` | Usar `float('inf')` rompe el simbolico | Importar y usar `oo` de SymPy |
| Variable mal puesta en multiple | El orden de las tuplas invierte interna/externa | Recordar: la **primera** tupla es la integral mas interna |
| Olvidar la tupla en la definida | `integrate(f, x, a, b)` no es definida | Usar `integrate(f, (x, a, b))` |

## Limitaciones

- La indefinida **no** lleva constante de integracion; el usuario la añade si la necesita.
- No toda integral tiene primitiva elemental: puede devolver funciones especiales o un [[Integral]] sin evaluar.
- Para construir y mostrar la integral **sin** intentar resolverla, usar la clase [[Integral]] y luego `.doit()`.
- Para integracion **numerica** (datos o integrandos sin forma cerrada) usar `evalf` sobre el `Integral`, o SciPy (`scipy.integrate.quad`).

## Notas relacionadas

- [[Integral]]
- [[sympy.diff]]
- [[Expr.subs]]
- [[sympy.calculus/integrales/index | integrales]]
