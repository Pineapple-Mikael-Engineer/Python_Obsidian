---
title: sympy.dsolve — resolver ecuaciones diferenciales ordinarias
aliases:
  - dsolve
  - sympy.dsolve
  - resolver EDO
tags:
  - sympy
  - api/funcion
  - solvers/diferenciales
lib: sympy
mod: sympy.solvers
tipo: funcion
retorna: Eq | list
requiere:
  - Function
  - sympy.Eq
  - Derivative
draft: false
---

# sympy.dsolve — resolver ecuaciones diferenciales ordinarias

`dsolve(eq, f(x))` resuelve de forma **exacta y simbolica** una **ecuacion diferencial ordinaria** (EDO) para la funcion incognita `f(x)`. Devuelve una `Eq` de la forma `Eq(f(x), <solucion>)`, donde la solucion general lleva **constantes de integracion** `C1`, `C2`, ... (una por cada orden de derivacion). Reconoce decenas de patrones (separable, lineal de primer orden, exacta, coeficientes constantes, etc.), elige automaticamente el metodo aplicable y admite **condiciones iniciales** via `ics=` para fijar las constantes. Es el equivalente simbolico de [[scipy.integrate.solve_ivp]], que integra EDOs de forma numerica.

> La funcion incognita se declara con `Function("f")` y se usa **aplicada** a su variable, `f(x)`. La derivada se escribe `f(x).diff(x)` (un objeto [[Derivative]]). La ecuacion se plantea con `Eq(lhs, rhs)`; una `Expr` suelta se asume **igualada a cero**.

## Firma

```python
sympy.dsolve(
    eq,                  # Eq | Expr: la EDO (Expr suelta = 0)
    func=None,           # f(x): funcion incognita aplicada (deducida si es unica)
    hint="default",      # str: metodo de resolucion a usar
    ics=None,            # dict: condiciones iniciales/de contorno {f(0): 1, ...}
    simplify=True,       # bool: simplificar la solucion
    ...
) -> Eq | list
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| EDO unica | `Eq` | `Eq(f(x), <solucion>)`; la solucion general lleva `C1`, `C2`, ... |
| Solucion no unica | `list` de `Eq` | Varias ramas/familias de solucion (p. ej. implicitas) |
| Sistema de EDOs | `list` de `Eq` | Una `Eq` por cada funcion incognita |

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")
dsolve(Eq(f(x).diff(x), f(x)), f(x))     # Eq(f(x), C1*exp(x))
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| EDO de primer orden | `dsolve(Eq(f(x).diff(x), ...), f(x))` |
| EDO planteada como `Expr` (= 0) | `dsolve(f(x).diff(x) - f(x), f(x))` |
| EDO de segundo orden | `dsolve(Eq(f(x).diff(x, 2) + f(x), 0), f(x))` |
| Con condiciones iniciales | `dsolve(eq, f(x), ics={f(0): 1})` |
| Forzar un metodo | `dsolve(eq, f(x), hint="1st_linear")` |
| Sistema de EDOs | `dsolve([eq1, eq2])` |

## Parametros en detalle

### `eq` (obligatorio)

La ecuacion diferencial, como `Eq(lhs, rhs)` o como `Expr` suelta (interpretada `= 0`). Las derivadas se construyen con `.diff()` sobre la funcion **aplicada** `f(x)`; `f(x).diff(x, 2)` es la segunda derivada.

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")

# Las dos formas son equivalentes:
dsolve(Eq(f(x).diff(x), f(x)), f(x))     # Eq(f(x), C1*exp(x))
dsolve(f(x).diff(x) - f(x), f(x))        # Eq(f(x), C1*exp(x))
```

### `func`

La funcion incognita aplicada, `f(x)`. Se puede **omitir** cuando la ecuacion contiene una sola funcion desconocida (SymPy la deduce), pero conviene pasarla siempre para evitar ambiguedad. **No** se pasa el simbolo `x` suelto: debe ser `f(x)`.

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")
dsolve(f(x).diff(x) - x)                 # Eq(f(x), C1 + x**2/2)  -> func deducida
```

### `ics` (condiciones iniciales)

Diccionario que fija el valor de la funcion y/o de sus derivadas en puntos concretos, eliminando las constantes `C1`, `C2`, .... Las claves son **expresiones evaluadas**: `f(0)` para la funcion, `f(x).diff(x).subs(x, 0)` para la derivada en `x = 0`. Hacen falta tantas condiciones como el orden de la EDO.

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")

# Primer orden: una condicion fija C1
dsolve(Eq(f(x).diff(x), f(x)), f(x), ics={f(0): 1})    # Eq(f(x), exp(x))

# Segundo orden: dos condiciones (valor y derivada)
dsolve(Eq(f(x).diff(x, 2) + f(x), 0), f(x),
       ics={f(0): 1, f(x).diff(x).subs(x, 0): 0})       # Eq(f(x), cos(x))
```

### `hint`

Nombre del **metodo** a emplear. Por defecto SymPy clasifica la EDO y elige el primero aplicable; `classify_ode(eq, f(x))` lista los disponibles. Util cuando quieres una forma de solucion concreta o el metodo automatico no satisface.

```python
from sympy import Function, Eq, dsolve, classify_ode, symbols
x = symbols("x")
f = Function("f")

classify_ode(Eq(f(x).diff(x), f(x)), f(x))[:3]   # ('separable', '1st_exact', '1st_linear')
dsolve(Eq(f(x).diff(x), f(x)), f(x), hint="1st_linear")   # Eq(f(x), C1*exp(x))
```

## Casos de uso

### EDO de primer orden separable

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")
# f' = x*f   ->  crecimiento gaussiano
dsolve(Eq(f(x).diff(x), x*f(x)), f(x))           # Eq(f(x), C1*exp(x**2/2))
```

### EDO lineal de primer orden no homogenea

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")
# f' + f = x
dsolve(Eq(f(x).diff(x) + f(x), x), f(x))         # Eq(f(x), C1*exp(-x) + x - 1)
```

### Oscilador armonico (segundo orden)

La ecuacion `f'' + f = 0` describe un oscilador no amortiguado; su solucion general combina seno y coseno con dos constantes.

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f = Function("f")
dsolve(Eq(f(x).diff(x, 2) + f(x), 0), f(x))      # Eq(f(x), C1*sin(x) + C2*cos(x))
```

### Sistema de EDOs acopladas

Pasa una **lista** de ecuaciones; `dsolve` devuelve una `Eq` por cada funcion incognita.

```python
from sympy import Function, Eq, dsolve, symbols
x = symbols("x")
f, g = Function("f"), Function("g")
dsolve([Eq(f(x).diff(x), g(x)),
        Eq(g(x).diff(x), -f(x))])
# [Eq(f(x), C1*sin(x) + C2*cos(x)), Eq(g(x), C1*cos(x) - C2*sin(x))]
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: dsolve() ... only work with functions of one variable` | Se paso `x` en lugar de `f(x)` como incognita | Pasar la funcion **aplicada** `f(x)`, no el simbolo |
| Constantes `C1`, `C2` sin fijar | No se dieron condiciones iniciales | Pasar `ics={...}` con tantas condiciones como el orden |
| `ics` no elimina las constantes | Clave mal escrita (p. ej. `f` sin aplicar) | Usar `f(0)` y `f(x).diff(x).subs(x, 0)` como claves |
| Plantear `f.diff(x)` (sin aplicar) | Se derivo la funcion no aplicada | Derivar `f(x).diff(x)`, siempre sobre `f(x)` |
| Olvidar `Eq` y restar mal los lados | `eq` suelta se asume `= 0` | Usar `Eq(lhs, rhs)` o mover todo a un lado: `lhs - rhs` |

## Limitaciones

- Solo resuelve EDOs que encajen en sus **patrones conocidos**; ecuaciones no lineales arbitrarias pueden quedar sin solucion cerrada o devolver formas implicitas.
- La solucion es **simbolica y exacta**; para EDOs sin forma cerrada o con datos numericos, usar [[scipy.integrate.solve_ivp]].
- Resuelve EDOs (una variable independiente), no ecuaciones en **derivadas parciales** (para eso existe `pdsolve`).
- Las claves de `ics` deben ser expresiones evaluadas en el punto, no la funcion generica.

## Notas relacionadas

- [[Derivative]]
- [[sympy.integrate]]
- [[scipy.integrate.solve_ivp]]
- [[sympy.solvers/diferenciales/index | diferenciales]]
