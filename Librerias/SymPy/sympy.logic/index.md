---
title: sympy.logic — logica proposicional simbolica
tags:
  - sympy
  - indice
draft: false
---

# sympy.logic

`sympy.logic` cubre la **logica proposicional simbolica**: formulas booleanas cuyos atomos son simbolos de SymPy, no valores Python. La distincion es fundamental — `p and q` en Python evalua de inmediato; `And(p, q)` en SymPy devuelve un objeto que se puede inspeccionar, simplificar y resolver. Este submodulo cierra el ciclo: construir formulas con operadores (`And`, `Or`, `Not`…), verificar si son satisfacibles (`satisfiable`) y minimizarlas (`simplify_logic`).

El flujo tipico de trabajo es lineal:

```python
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import And, Or, Not, Implies
from sympy.logic.inference import satisfiable

p, q, r = symbols("p q r")

# 1. Construir la formula con operadores simbolicos
formula = And(Implies(p, q), Implies(q, r), p)

# 2. Simplificar antes de analizar
compacta = simplify_logic(formula)   # And(p, q, r) -> simplificado

# 3. Verificar satisfacibilidad
satisfiable(compacta)                # {p: True, q: True, r: True}
```

## Como se relacionan

La decision clave: **que quieres hacer** con la formula.

| Herramienta | Entrada | Salida | Cuando usarla |
|-------------|---------|--------|---------------|
| [[sympy.operadores_logicos]] | simbolos SymPy | `BooleanExpr` | **Siempre primero**: construir la formula |
| [[sympy.simplify_logic]] | `BooleanExpr` | `BooleanExpr` simplificada | Minimizar redundancias o convertir a CNF/DNF |
| [[sympy.satisfiable]] | `BooleanExpr` | `dict` o `False` | Verificar si existe alguna asignacion que la satisfaga |

Arbol de decision:

- ¿Necesitas construir una formula? -> [[sympy.operadores_logicos]] (`And`, `Or`, `Not`, `Implies`, `Equivalent`, `Xor`).
- ¿Quieres saber si la formula puede ser verdadera (y con que valores)? -> [[sympy.satisfiable]].
- ¿Quieres una forma mas compacta, o necesitas CNF/DNF explicita? -> [[sympy.simplify_logic]].

> [!info] SymPy bool vs Python bool
> `p and q` en Python evalua `p`; si es falsy devuelve `p`, si no devuelve `q`. No crea ningun objeto simbolico. `And(p, q)` crea un objeto `BooleanExpr` que conserva la estructura de la formula, acepta `.subs()`, se puede simplificar y se puede pasar a `satisfiable`. Son herramientas distintas para propositos distintos.

## Notas

- [[sympy.operadores_logicos]] — `And`, `Or`, `Not`, `Implies`, `Equivalent`, `Xor`. Los constructores de formulas booleanas simbolicas; punto de entrada obligatorio de cualquier flujo en este modulo.
- [[sympy.satisfiable]] — determina si una formula es SAT o UNSAT. Devuelve un modelo (dict) o `False`; con `all_models=True` genera todos los modelos posibles.
- [[sympy.simplify_logic]] — minimiza una formula booleana o la convierte a CNF/DNF. Equivalente logica de `simplify` para el dominio proposicional.

## Notas relacionadas

- [[sympy.logic/index | sympy.logic]]
- [[SymPy/index | SymPy]]
- [[Tree SymPy]]
