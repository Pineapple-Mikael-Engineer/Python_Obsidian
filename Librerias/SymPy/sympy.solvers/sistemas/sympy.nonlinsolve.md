---
title: sympy.nonlinsolve — resuelve sistemas de ecuaciones no lineales
aliases:
  - nonlinsolve
  - sympy.nonlinsolve
  - sistemas no lineales
tags:
  - sympy
  - api/funcion
  - solvers/sistemas
lib: sympy
mod: sympy.solvers
tipo: funcion
retorna: FiniteSet
requiere:
  - Symbol
  - sympy.linsolve
draft: false
---

# sympy.nonlinsolve — resuelve sistemas de ecuaciones no lineales

`nonlinsolve` resuelve **sistemas de ecuaciones no lineales** (con potencias, productos de incognitas, trigonometricas, exponenciales) de forma exacta y simbolica. Es la contraparte de [[sympy.linsolve]] para el caso no lineal y devuelve **todas** las soluciones que encuentra, incluidas las **complejas**, como un `FiniteSet` de tuplas. El orden dentro de cada tupla sigue el de los simbolos que se le pasan.

> El resultado es un [[FiniteSet]] de **tuplas** ordenadas segun los simbolos dados. A diferencia de `solve`, `nonlinsolve` siempre intenta el conjunto **completo** de soluciones (reales y complejas) y nunca devuelve un `dict`.

## Firma

```python
sympy.nonlinsolve(
    system,        # lista de Eq/Expr no lineales
    *symbols,      # las incognitas (o una lista), en el orden de la tupla de salida
) -> FiniteSet
```

## Valor de retorno

| Caso | Salida | Significado |
|------|--------|-------------|
| Soluciones discretas | `FiniteSet` de tuplas | una tupla por solucion (real o compleja) |
| Sin solucion | `EmptySet` | el sistema no tiene solucion |
| No resuelve del todo | `FiniteSet` con formas implicitas | deja una expresion sin despejar (ver Limitaciones) |

```python
from sympy import symbols, nonlinsolve
x, y = symbols("x y")
nonlinsolve([x**2 - y, y - x - 2], [x, y])     # {(-1, 1), (2, 4)}
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Simbolos en lista | `nonlinsolve([eq1, eq2], [x, y])` |
| Simbolos sueltos | `nonlinsolve([eq1, eq2], x, y)` |
| Con objetos `Eq` | `nonlinsolve([Eq(x**2+y**2, 1), Eq(x, y)], x, y)` |

## Parametros en detalle

### `system` (obligatorio)

La lista de ecuaciones. Una `Expr` suelta se interpreta como `= 0`; tambien se aceptan objetos `Eq(lhs, rhs)`. Las ecuaciones pueden ser polinomicas o trascendentes.

```python
from sympy import symbols, nonlinsolve, Eq
x, y = symbols("x y")

# circunferencia x^2 + y^2 = 1 cortada con la recta x = y
nonlinsolve([Eq(x**2 + y**2, 1), Eq(x, y)], x, y)
# {(-sqrt(2)/2, -sqrt(2)/2), (sqrt(2)/2, sqrt(2)/2)}
```

### `*symbols` (obligatorio)

Las incognitas, sueltas o en una lista, en el **orden** de la tupla de salida. Es habitual pasarlas como lista `[x, y]`.

```python
from sympy import symbols, nonlinsolve
x, y = symbols("x y")
# soluciones complejas incluidas
nonlinsolve([x**2 - y, x**3 - 1], [x, y])
# {(1, 1),
#  (-1/2 - sqrt(3)*I/2, -1/2 + sqrt(3)*I/2),
#  (-1/2 + sqrt(3)*I/2, -1/2 - sqrt(3)*I/2)}
```

## Casos de uso

### Interseccion de dos curvas

```python
from sympy import symbols, nonlinsolve
x, y = symbols("x y")
# parabola y = x^2  con la recta y = x + 2
nonlinsolve([x**2 - y, y - x - 2], [x, y])     # {(-1, 1), (2, 4)}
```

### Circunferencia y recta (raices irracionales exactas)

```python
from sympy import symbols, nonlinsolve
x, y = symbols("x y")
nonlinsolve([x**2 + y**2 - 1, x - y], [x, y])
# {(-sqrt(2)/2, -sqrt(2)/2), (sqrt(2)/2, sqrt(2)/2)}
```

### Relacion con `solve` para sistemas

Para sistemas, [[sympy.solve]] tambien funciona y devuelve una **lista de tuplas** (o de dicts con `dict=True`); `nonlinsolve` devuelve un `FiniteSet` y apunta a entregar el conjunto completo de soluciones. Si solo interesan las soluciones discretas y un formato de lista, `solve` suele bastar.

```python
from sympy import symbols, solve, nonlinsolve
x, y = symbols("x y")
solve([x**2 + y**2 - 1, x - y], [x, y])
# [(-sqrt(2)/2, -sqrt(2)/2), (sqrt(2)/2, sqrt(2)/2)]   -> lista de tuplas

nonlinsolve([x**2 + y**2 - 1, x - y], [x, y])
# {(-sqrt(2)/2, -sqrt(2)/2), (sqrt(2)/2, sqrt(2)/2)}   -> FiniteSet
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `sol[0]` falla con `TypeError` | un `FiniteSet` no es indexable | `list(sol)[0]` o iterar sobre `sol` |
| Aparecen soluciones complejas inesperadas | `nonlinsolve` da el conjunto completo | filtrar con `.is_real`, o declarar `symbols(..., real=True)` |
| Resultado con `_n`/parametros raros | familia infinita (p. ej. trascendentes) | aceptar la forma parametrica o reformular |
| Sistema **lineal** resuelto de mas | overhead innecesario | usar [[sympy.linsolve]] para el caso lineal |
| Cuelgue o resultado sin despejar | sistema trascendente dificil | simplificar, dar supuestos, o usar `nsolve` numerico |

## Limitaciones

- Puede dejar soluciones en **forma implicita** o solo parcialmente despejadas cuando el sistema es trascendente y no admite solucion cerrada.
- Para familias **infinitas** (ecuaciones trigonometricas/exponenciales) la salida puede incluir parametros enteros (`_n`) en vez de un conjunto finito limpio.
- No resuelve inecuaciones.
- Para una raiz **numerica** concreta de un sistema dificil, usar `nsolve` (requiere una estimacion inicial); el mundo simbolico no siempre converge.

## Notas relacionadas

- [[sympy.linsolve]]
- [[sympy.solve]]
- [[sympy.solveset]]
- [[FiniteSet]]
- [[sympy.solvers/sistemas/index | sistemas]]
