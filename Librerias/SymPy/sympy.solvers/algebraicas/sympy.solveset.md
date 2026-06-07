---
title: sympy.solveset — resolutor moderno que devuelve conjuntos
aliases:
  - solveset
  - sympy.solveset
  - resolver en conjunto
tags:
  - sympy
  - api/funcion
  - solvers/algebraicas
lib: sympy
mod: sympy.solvers
tipo: funcion
retorna: Set
requiere:
  - Symbol
  - Eq
draft: false
---

# sympy.solveset — resolutor moderno que devuelve conjuntos

`solveset(eq, x, domain=S.Reals)` resuelve una ecuacion de **una** incognita y devuelve un **conjunto** (`Set`) con todas las soluciones, en vez de una lista. Es el resolutor **moderno** de SymPy: representa de forma natural soluciones **infinitas** (`ImageSet`), intervalos (`Interval`), conjuntos finitos (`FiniteSet`) y la ausencia de solucion (`EmptySet`), y deja **explicito el dominio** de busqueda. Por eso su salida es siempre un objeto consistente y bien definido, frente a la lista heterogenea de [[sympy.solve]].

> Ventaja clave frente a `solve`: `solveset(sin(x), x)` devuelve el conjunto **infinito** completo de raices, no una muestra finita. Y `domain=S.Reals` vs `S.Complexes` controla con precision donde buscar.

## Firma

```python
sympy.solveset(
    f,                   # Expr | Eq: ecuacion (Expr suelta -> se asume = 0)
    symbol=None,         # Symbol: la unica incognita (recomendado indicarla)
    domain=S.Complexes,  # Set: dominio de busqueda; tipicamente S.Reals
) -> Set
```

## Valor de retorno

Siempre un **conjunto** (`Set`). Segun el caso:

| Tipo de conjunto | Cuando aparece | Ejemplo |
|------------------|----------------|---------|
| `FiniteSet` | Numero finito de soluciones | `{-2, 2}`, ver [[FiniteSet]] |
| `Interval` | Soluciones en un rango continuo (inecuaciones) | `Interval.open(0, oo)`, ver [[Interval]] |
| `ImageSet` | Familia **infinita** parametrizada por un entero | raices de `sin(x)` |
| `EmptySet` | **No** hay solucion en el dominio | `solveset(x**2 + 1, x, S.Reals)` |
| `ConditionSet` | SymPy no pudo despejar; queda la condicion | conjunto definido por la ecuacion |

```python
from sympy import symbols, solveset
x = symbols("x")
solveset(x**2 - 4, x)      # {-2, 2}   -> FiniteSet
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Resolver en los complejos (por defecto) | `solveset(f, x)` |
| Resolver solo en los reales | `solveset(f, x, domain=S.Reals)` |
| Resolver `lhs = rhs` | `solveset(Eq(lhs, rhs), x)` |
| Resolver una inecuacion | `solveset(x > 0, x, domain=S.Reals)` |

## Parametros en detalle

### `f` (obligatorio)

La ecuacion. Una `Expr` suelta se asume `= 0`; una igualdad explicita se construye con `Eq(lhs, rhs)`. Tambien admite inecuaciones (`<`, `>`, …), cuyo resultado suele ser un [[Interval]].

```python
from sympy import symbols, solveset, Eq, S
x = symbols("x")
solveset(x**2 - 4, x)              # {-2, 2}
solveset(Eq(x**2, 4), x, S.Reals)  # {-2, 2}
```

### `symbol`

La unica incognita. `solveset` resuelve para **un solo** simbolo (no sistemas); conviene indicarlo siempre que haya parametros.

```python
from sympy import symbols, solveset
x, a = symbols("x a")
solveset(a*x - 1, x)       # {1/a}   -> deja a simbolico
```

### `domain`

Conjunto donde buscar soluciones. Por defecto `S.Complexes`; lo habitual en ingenieria es restringir a `S.Reals`. El dominio cambia el resultado: una ecuacion sin raices reales devuelve `EmptySet` en `S.Reals` pero un `FiniteSet` complejo en `S.Complexes`.

```python
from sympy import symbols, solveset, S
x = symbols("x")
solveset(x**2 + 1, x, domain=S.Reals)       # EmptySet
solveset(x**2 + 1, x, domain=S.Complexes)   # {-I, I}
```

### Soluciones infinitas (`ImageSet`)

Las ecuaciones periodicas tienen **infinitas** soluciones; `solveset` las representa exactas con un `ImageSet` parametrizado por un entero `_n`. Esto es lo que `solve` no puede expresar.

```python
from sympy import symbols, solveset, sin
x = symbols("x")
solveset(sin(x), x)
# Union(ImageSet(Lambda(_n, 2*_n*pi), Integers),
#       ImageSet(Lambda(_n, 2*_n*pi + pi), Integers))   -> todos los multiplos de pi
```

## Casos de uso

### Restringir la busqueda a los reales

```python
from sympy import symbols, solveset, S
x = symbols("x")
solveset(x**2 - 2, x, domain=S.Reals)   # {-sqrt(2), sqrt(2)}
```

### Resolver una inecuacion

```python
from sympy import symbols, solveset, S
x = symbols("x")
solveset(x > 0, x, domain=S.Reals)      # Interval.open(0, oo)
```

### Detectar ausencia de solucion sin ambiguedad

```python
from sympy import symbols, solveset, exp, S
x = symbols("x")
solveset(exp(x), x, domain=S.Reals)     # EmptySet   -> e**x nunca es 0
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar una lista y hacer `[0]` | `solveset` devuelve un `Set`, no una lista | Convertir con `list(resultado)` si es finito, o iterar |
| `EmptySet` inesperado | El dominio por defecto o `S.Reals` no contiene la raiz | Ajustar `domain` (p. ej. `S.Complexes`) |
| Pasar varias incognitas | `solveset` es de **una** incognita | Usar `linsolve` / `nonlinsolve` o [[sympy.solve]] |
| Resultado `ConditionSet` | SymPy no supo despejar la ecuacion | Reformular, o usar [[sympy.nsolve]] para una raiz numerica |
| Usar `=` para la ecuacion | `=` es asignacion en Python | Usar `Eq(lhs, rhs)` o `lhs - rhs` |

## Limitaciones

- Resuelve **una sola** incognita: para sistemas se usan `linsolve` / `nonlinsolve`, o [[sympy.solve]].
- Su salida es un `Set`, no una lista: hay que convertirla (`list(...)`) cuando se quiere indexar, y solo si es finita.
- Para raices de **polinomios** con multiplicidad, [[sympy.roots]]; para una raiz **numerica**, [[sympy.nsolve]].

## Notas relacionadas

- [[sympy.solve]]
- [[FiniteSet]]
- [[Interval]]
- [[sympy.roots]]
- [[sympy.solvers/algebraicas/index | algebraicas]]
