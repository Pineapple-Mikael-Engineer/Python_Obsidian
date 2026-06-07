---
title: sympy.satisfiable — verificar satisfacibilidad de una formula logica
aliases: [satisfiable, SAT]
tags: [sympy, api/funcion, logic]
lib: sympy
mod: sympy.logic
tipo: funcion
retorna: dict | False
requiere: []
draft: false
---

# sympy.satisfiable — verificar satisfacibilidad de una formula logica

`satisfiable(expr)` determina si una formula proposicional es **satisfacible**: existe al menos una asignacion de valores de verdad a sus variables que la hace verdadera. Devuelve un diccionario `{simbolo: True/False}` con **un** modelo satisfactorio si la formula es SAT, o `False` si es UNSAT (ninguna asignacion la satisface). Con `all_models=True` devuelve un generador de **todos** los modelos validos. Usa el algoritmo DPLL2 por defecto, apto para formulas con decenas de variables.

La entrada debe ser una formula construida con [[sympy.operadores_logicos]] (`And`, `Or`, `Not`, `Implies`, `Equivalent`).

## Firma

```python
sympy.logic.inference.satisfiable(
    expr,                     # formula booleana (BooleanExpr)
    algorithm='dpll2',        # 'dpll2' (default) | 'dpll' | 'pycosat'
    all_models=False,         # True -> generador de todos los modelos
) -> dict | False
```

## Valor de retorno

| Resultado | Tipo | Significado |
|-----------|------|-------------|
| Formula satisfacible | `dict` `{Symbol: bool, ...}` | Un modelo (asignacion) que la hace verdadera |
| Formula insatisfacible | `False` | Ninguna asignacion la satisface |
| `all_models=True` | generador de `dict` | Todos los modelos; se agota cuando no hay mas |

```python
from sympy import symbols
from sympy.logic.boolalg import And, Not
from sympy.logic.inference import satisfiable

p, q = symbols("p q")

satisfiable(And(p, q))       # {p: True, q: True}
satisfiable(And(p, Not(p)))  # False
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Un modelo (si existe) | `satisfiable(expr)` |
| Todos los modelos | `satisfiable(expr, all_models=True)` |
| Algoritmo alternativo | `satisfiable(expr, algorithm='dpll')` |

## Parametros en detalle

### `expr` (obligatorio)

Cualquier formula booleana de SymPy: puede ser un solo simbolo, una composicion con `And`/`Or`/`Not`/`Implies`, o una formula compleja. No acepta expresiones algebraicas (`x + 1 > 0`); solo proposicional puro.

```python
from sympy import symbols
from sympy.logic.boolalg import Or, Not
from sympy.logic.inference import satisfiable

p, q, r = symbols("p q r")

satisfiable(Or(p, q))              # {p: True, q: False} (un modelo posible)
satisfiable(Or(p, Not(p)))         # {p: True}           -> tautologia: siempre SAT
```

### `all_models`

Cuando `True`, devuelve un **generador** que produce todos los modelos uno a uno. Util para contar soluciones o filtrar las que cumplan condiciones adicionales.

```python
from sympy import symbols
from sympy.logic.boolalg import Or
from sympy.logic.inference import satisfiable

p, q = symbols("p q")

for modelo in satisfiable(Or(p, q), all_models=True):
    print(modelo)
# {p: False, q: True}
# {p: True, q: False}
# {p: True, q: True}
```

## Casos de uso

### Verificar contradiccion vs tautologia

```python
from sympy import symbols
from sympy.logic.boolalg import And, Or, Not
from sympy.logic.inference import satisfiable

p = symbols("p")

# Contradiccion: siempre False
satisfiable(And(p, Not(p)))          # False -> UNSAT

# Tautologia: siempre True (al menos un modelo existe con cualquier valor)
satisfiable(Or(p, Not(p)))           # {p: True}
```

### Verificacion de restricciones de planificacion

Codificar restricciones como formula y verificar si hay una asignacion que las satisfaga todas.

```python
from sympy import symbols
from sympy.logic.boolalg import And, Not, Implies
from sympy.logic.inference import satisfiable

tarea_a, tarea_b, tarea_c = symbols("tarea_a tarea_b tarea_c")

# Si A se hace, B no puede hacerse al mismo tiempo
# Si B se hace, C debe hacerse
restricciones = And(
    Implies(tarea_a, Not(tarea_b)),
    Implies(tarea_b, tarea_c),
    tarea_a,
)
satisfiable(restricciones)
# {tarea_a: True, tarea_b: False, tarea_c: True}
```

### Contar todos los modelos

```python
from sympy import symbols
from sympy.logic.boolalg import Or
from sympy.logic.inference import satisfiable

p, q = symbols("p q")

modelos = list(satisfiable(Or(p, q), all_models=True))
len(modelos)   # 3 -> (T,F), (F,T), (T,T)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `satisfiable` no importa desde `sympy` directamente | No esta en el namespace top-level | `from sympy.logic.inference import satisfiable` |
| Pasar una `Expr` algebraica (`x > 0`) | Solo acepta logica proposicional pura | Usar simbolos booleanos y operadores `And`/`Or`/`Not` |
| Confundir `False` (UNSAT) con `{...}` vacio | Un dict vacio no ocurre; UNSAT es el literal `False` | Comparar con `if resultado is False:` |
| Iterar `all_models=True` dos veces | El generador se agota tras la primera iteracion | Convertir a lista con `list(...)` si se necesita releer |

## Notas relacionadas

- [[sympy.operadores_logicos]]
- [[sympy.simplify_logic]]
- [[sympy.logic/index | sympy.logic]]
