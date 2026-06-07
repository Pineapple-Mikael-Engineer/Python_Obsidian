---
title: sympy.solve — resolutor algebraico clasico de proposito general
aliases:
  - solve
  - sympy.solve
  - resolver ecuaciones
tags:
  - sympy
  - api/funcion
  - solvers/algebraicas
lib: sympy
mod: sympy.solvers
tipo: funcion
retorna: list | dict
requiere:
  - Symbol
  - Eq
draft: false
---

# sympy.solve — resolutor algebraico clasico de proposito general

`solve(f, x)` resuelve **algebraicamente** la ecuacion `f = 0` para la incognita `x`, de forma exacta y simbolica. Es el resolutor **clasico** y mas flexible de SymPy: acepta una `Expr` suelta (que se asume igualada a cero), una ecuacion explicita `Eq(lhs, rhs)`, o **sistemas** de varias ecuaciones con varias incognitas. Devuelve normalmente una **lista** de soluciones (o una **lista de diccionarios** con `dict=True`). Cuando no encuentra ninguna solucion, devuelve una **lista vacia** `[]`.

> Para muchos casos, [[sympy.solveset]] es la alternativa **moderna**: devuelve un conjunto en vez de una lista y representa soluciones infinitas y dominios de forma explicita. `solve` sigue siendo el mas comodo para sistemas y para obtener listas/diccionarios directos.

## Firma

```python
sympy.solve(
    f,                   # Expr | Eq | lista de ellas: ecuacion(es) a resolver (Expr -> se asume = 0)
    *symbols,            # Symbol(s): incognita(s); si se omiten, SymPy las deduce
    dict=False,          # bool: True -> lista de dicts {simbolo: valor}
    set=False,           # bool: True -> (symbols, {tuplas de solucion})
    check=True,          # bool: descartar soluciones que invaliden denominadores/logaritmos
    rational=None,       # bool: convertir floats a Rational antes de resolver
    ...
) -> list | dict
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Una incognita | `list` | Lista de soluciones: `[-2, 2]` |
| Una incognita, `dict=True` | `list[dict]` | `[{x: -2}, {x: 2}]` |
| Sistema, solucion unica | `dict` | `{x: 2, y: 1}` (mapea cada incognita a su valor) |
| Sistema, varias soluciones | `list[dict]` | Lista de diccionarios, uno por solucion |
| Sin solucion | `list` | Lista **vacia** `[]` |

```python
from sympy import symbols, solve
x = symbols("x")
solve(x**2 - 4, x)         # [-2, 2]   -> Expr suelta, se asume = 0
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Resolver `f = 0` | `solve(f, x)` |
| Resolver `lhs = rhs` | `solve(Eq(lhs, rhs), x)` |
| Devolver lista de diccionarios | `solve(f, x, dict=True)` |
| Sistema de ecuaciones | `solve([eq1, eq2], [x, y])` |
| Deducir las incognitas | `solve(f)` |

## Parametros en detalle

### `f` (obligatorio)

La ecuacion. Una `Expr` suelta se interpreta como `f = 0`; una ecuacion explicita se construye con `Eq(lhs, rhs)`. Una **lista** de ellas plantea un sistema.

```python
from sympy import symbols, solve, Eq
x = symbols("x")
solve(x**2 - 4, x)         # [-2, 2]      -> x**2 - 4 = 0
solve(Eq(x**2, 4), x)      # [-2, 2]      -> x**2 = 4, mismo resultado
```

### `*symbols`

La(s) incognita(s) a despejar. Si se omiten, SymPy resuelve para todos los simbolos libres; conviene indicarlas siempre que haya parametros para no despejar el simbolo equivocado.

```python
from sympy import symbols, solve
x, a, b = symbols("x a b")
solve(a*x + b, x)          # [-b/a]   -> despeja x, deja a y b simbolicos
```

### Soluciones multiples

`solve` devuelve **todas** las raices que encuentra, incluidas las **complejas** (con la unidad imaginaria `I`).

```python
from sympy import symbols, solve
x = symbols("x")
solve(x**2 + 1, x)         # [-I, I]                              -> raices complejas
solve(x**3 - 1, x)         # [1, -1/2 - sqrt(3)*I/2, -1/2 + sqrt(3)*I/2]
```

### `dict=True`

Devuelve una **lista de diccionarios** `{simbolo: valor}` en vez de una lista plana. Util para mapear cada solucion a su incognita de forma inequivoca, sobre todo con varias incognitas.

```python
from sympy import symbols, solve
x = symbols("x")
solve(x**2 - 4, x, dict=True)   # [{x: -2}, {x: 2}]
```

### Sistemas (varias incognitas)

Con una **lista de ecuaciones** y una **lista de incognitas** resuelve el sistema. Con solucion unica devuelve un `dict`; con varias, una lista de `dict`.

```python
from sympy import symbols, solve
x, y = symbols("x y")
solve([x + y - 3, x - y - 1], [x, y])   # {x: 2, y: 1}
```

### Cuando devuelve lista vacia

Si la ecuacion **no tiene solucion** (o SymPy no logra hallarla en forma cerrada), el resultado es `[]`. No es un error: hay que comprobar la lista antes de indexarla.

```python
from sympy import symbols, solve
x = symbols("x")
solve(x - x, x)            # []   -> 0 = 0 no restringe x (identidad)
```

## Casos de uso

### Despejar una variable de una formula

```python
from sympy import symbols, solve, Eq
v, v0, a, t = symbols("v v0 a t")
solve(Eq(v, v0 + a*t), t)      # [(-v0 + v)/a]   -> t despejado
```

### Puntos de corte de dos curvas

```python
from sympy import symbols, solve
x = symbols("x")
solve(x**2 - (x + 2), x)       # [-1, 2]   -> donde x**2 = x + 2
```

### Sistema lineal de equilibrio

```python
from sympy import symbols, solve
F1, F2 = symbols("F1 F2")
solve([F1 + F2 - 100, F1 - 2*F2], [F1, F2])   # {F1: 200/3, F2: 100/3}
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar `lhs = rhs` con `=` | `=` es asignacion en Python, no ecuacion | Usar `Eq(lhs, rhs)` o reescribir como `lhs - rhs` |
| Indexar `[0]` y fallar | El resultado fue `[]` (sin solucion) | Comprobar si la lista esta vacia antes de indexar |
| No saber a que incognita corresponde cada valor | Lista plana ambigua | Usar `dict=True` o resolver con la lista de incognitas |
| Esperar el conjunto de **todas** las soluciones de `sin(x)=0` | `solve` da representantes finitos, no el conjunto infinito | Usar [[sympy.solveset]] para soluciones infinitas |
| Olvidar la incognita en sistemas | Sin lista de incognitas, el resultado es ambiguo | Pasar `solve([...], [x, y])` |

## Limitaciones

- Devuelve una **lista** o **dict**, no un conjunto: no representa de forma natural soluciones **infinitas** (p. ej. todas las de `sin(x) = 0`). Para eso, [[sympy.solveset]].
- No fija el **dominio** de busqueda de forma explicita; `solveset` permite `domain=S.Reals`.
- Para raices de **polinomios** con su multiplicidad, [[sympy.roots]] es mas directo.
- Cuando no hay solucion cerrada, conviene una **raiz numerica** con [[sympy.nsolve]].

## Notas relacionadas

- [[sympy.solveset]]
- [[sympy.roots]]
- [[sympy.nsolve]]
- [[sympy.solvers/algebraicas/index | algebraicas]]
