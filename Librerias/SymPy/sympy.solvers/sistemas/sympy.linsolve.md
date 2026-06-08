---
title: sympy.linsolve — resuelve sistemas de ecuaciones lineales
aliases:
  - linsolve
  - sympy.linsolve
  - sistemas lineales
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
  - Matrix
draft: false
---

# sympy.linsolve — resuelve sistemas de ecuaciones lineales

`linsolve` resuelve **sistemas de ecuaciones lineales** de forma exacta y simbolica. A diferencia de [[sympy.solve]], esta especializado en el caso lineal: usa eliminacion de Gauss y trata con un mismo lenguaje los sistemas con **solucion unica**, con **infinitas soluciones** (las parametriza) y **sin solucion** (devuelve `EmptySet`). Siempre devuelve un `FiniteSet` de tuplas, una tupla por solucion, en el orden de los simbolos que se le pasan.

> El resultado es un [[FiniteSet]] cuyos elementos son **tuplas** ordenadas segun los simbolos dados, no un `dict`. Para `linsolve([...], x, y)` cada solucion es `(valor_x, valor_y)`. El orden de las incognitas lo fijas tu en la llamada, no SymPy.

## Firma

```python
sympy.linsolve(
    system,        # lista de Eq/Expr  |  (A, b) matricial  |  Matrix aumentada [A|b]
    *symbols,      # las incognitas, en el orden deseado de la tupla de salida
) -> FiniteSet
```

## Valor de retorno

| Caso | Salida | Significado |
|------|--------|-------------|
| Solucion unica | `FiniteSet` con 1 tupla | `{(x0, y0, ...)}` valores concretos |
| Infinitas soluciones | `FiniteSet` con 1 tupla parametrica | tupla en funcion de las variables libres |
| Sin solucion | `EmptySet` | el sistema es inconsistente |

```python
from sympy import symbols, linsolve
x, y = symbols("x y")
linsolve([x + y - 2, x - y], x, y)     # {(1, 1)}
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Desde lista de ecuaciones | `linsolve([eq1, eq2], x, y)` |
| Forma matricial `A·x = b` | `linsolve((A, b), x, y)` |
| Desde matriz aumentada `[A\|b]` | `linsolve(Matrix([[..., ...]]), x, y)` |
| Con objetos `Eq` | `linsolve([Eq(x+y, 2), Eq(x-y, 0)], x, y)` |

## Parametros en detalle

### `system` (obligatorio)

Acepta tres representaciones equivalentes del mismo sistema. Una `Expr` suelta se interpreta como `= 0`; tambien puedes pasar objetos `Eq(lhs, rhs)`.

```python
from sympy import symbols, linsolve, Matrix, Eq
x, y = symbols("x y")

# 1) lista de expresiones (cada una igualada a 0)
linsolve([x + y - 2, x - y], x, y)              # {(1, 1)}

# 2) forma matricial (A, b)  ->  A·x = b
A = Matrix([[1, 1], [1, -1]])
b = Matrix([2, 0])
linsolve((A, b), x, y)                          # {(1, 1)}

# 3) matriz aumentada [A | b]
linsolve(Matrix([[1, 1, 2], [1, -1, 0]]), x, y) # {(1, 1)}
```

### `*symbols` (obligatorio)

Las incognitas, en el **orden** que tendran las tuplas de salida. Es obligatorio incluso en la forma matricial, porque la matriz por si sola no nombra las variables.

```python
from sympy import symbols, linsolve
x, y = symbols("x y")
linsolve([x + y - 2, x - y], y, x)     # {(1, 1)}  -> aqui la tupla es (y, x)
```

## Casos de uso

### Sistema con solucion unica

```python
from sympy import symbols, linsolve
x, y, z = symbols("x y z")
sistema = [x + y + z - 6,
           2*x - y + z - 3,
           x + 2*y - z - 2]
linsolve(sistema, x, y, z)             # {(1, 2, 3)}
```

### Infinitas soluciones (sistema indeterminado)

Cuando hay menos ecuaciones independientes que incognitas, `linsolve` **parametriza** la familia de soluciones dejando libres las variables sobrantes.

```python
from sympy import symbols, linsolve
x, y, z = symbols("x y z")
# una sola ecuacion independiente (la 2a es 2x la 1a)
linsolve([x + 2*y + 3*z - 6, 2*x + 4*y + 6*z - 12], x, y, z)
# {(-2*y - 3*z + 6, y, z)}   -> y, z libres; x depende de ellas
```

### Sistema sin solucion (inconsistente)

```python
from sympy import symbols, linsolve
x, y = symbols("x y")
linsolve([x + y - 1, x + y - 2], x, y)     # EmptySet
```

### Extraer una solucion del FiniteSet

El `FiniteSet` no se indexa como una lista; conviertelo a `list` o itera sobre el.

```python
from sympy import symbols, linsolve
x, y = symbols("x y")
sol = linsolve([x + y - 2, x - y], x, y)
list(sol)            # [(1, 1)]
list(sol)[0]         # (1, 1)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `sol[0]` falla con `TypeError` | un `FiniteSet` no es indexable | `list(sol)[0]` o iterar sobre `sol` |
| Tupla en orden inesperado | el orden lo fijan los `*symbols`, no el sistema | pasar los simbolos en el orden deseado |
| Resultado `EmptySet` no esperado | sistema inconsistente (rectas paralelas, etc.) | revisar el modelo; comprobar dependencias |
| Resultado con variables sueltas | sistema indeterminado (infinitas soluciones) | es correcto: las libres quedan como parametros |
| Sistema **no lineal** mal resuelto | `linsolve` asume linealidad | usar [[sympy.nonlinsolve]] para el caso no lineal |

## Limitaciones

- Solo para sistemas **lineales** en las incognitas; para ecuaciones no lineales usar [[sympy.nonlinsolve]].
- No acepta inecuaciones; modela igualdades.
- Las incognitas se dan siempre de forma explicita; no las infiere del sistema como hace a veces [[sympy.solve]].
- Para resolucion **numerica** de sistemas lineales grandes/densos, el mundo simbolico es lento: conviene `numpy.linalg.solve` o `scipy.linalg.solve`.

## Notas relacionadas

- [[sympy.nonlinsolve]]
- [[sympy.solve]]
- [[sympy.solveset]]
- [[Matrix]]
- [[FiniteSet]]
- [[sympy.solvers/sistemas/index | sistemas]]
