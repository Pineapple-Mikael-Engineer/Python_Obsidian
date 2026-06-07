---
title: sympy.operadores_logicos — And, Or, Not, Implies, Equivalent
aliases: [And, Or, Not, Implies, operadores logicos]
tags: [sympy, api/concepto, logic]
lib: sympy
mod: sympy.logic
tipo: concepto
draft: false
---

# sympy.operadores_logicos — And, Or, Not, Implies, Equivalent

SymPy ofrece operadores de logica proposicional simbolica: `And`, `Or`, `Not`, `Implies`, `Equivalent` y `Xor`. A diferencia de los operadores nativos de Python (`and`, `or`, `not`), estos **no evaluan inmediatamente**: crean objetos `Expr` booleanos que se pueden simplificar, sustituir con `.subs()` o pasar a [[sympy.satisfiable]] y [[sympy.simplify_logic]]. Son la materia prima de la logica proposicional en SymPy.

La diferencia central: `p and q` en Python evalua `p` y devuelve uno de los dos valores; `And(p, q)` en SymPy devuelve el objeto simbolico `p & q` sin resolver, igual que `sin(x)` deja la funcion sin calcular hasta tener un valor concreto.

## Operadores

| Operador | Llamada SymPy | Notacion simbolica | Significado |
|----------|---------------|--------------------|-------------|
| Conjuncion | `And(p, q)` | `p & q` | `p` y `q` ambos verdaderos |
| Disyuncion | `Or(p, q)` | `p \| q` | al menos uno verdadero |
| Negacion | `Not(p)` | `~p` | contrario de `p` |
| Implicacion | `Implies(p, q)` | `Implies(p, q)` | si `p` entonces `q` |
| Equivalencia | `Equivalent(p, q)` | `Equivalent(p, q)` | `p` sii `q` |
| O exclusivo | `Xor(p, q)` | `Xor(p, q)` | exactamente uno verdadero |

```python
from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies, Equivalent, Xor

p, q = symbols("p q")

And(p, q)              # p & q
Or(p, Not(q))          # p | ~q
Implies(p, q)          # Implies(p, q)
Equivalent(p, q)       # Equivalent(p, q)
Xor(p, q)              # Xor(p, q)
```

## Casos de uso

### Construir formulas para satisfiable

El uso principal es componer la formula y pasarla a [[sympy.satisfiable]] para verificar si existe alguna asignacion de verdad que la satisfaga.

```python
from sympy import symbols
from sympy.logic.boolalg import And, Or, Not, Implies
from sympy.logic.inference import satisfiable

p, q = symbols("p q")

formula = And(Implies(p, q), p)
satisfiable(formula)         # {p: True, q: True}

contradiccion = And(p, Not(p))
satisfiable(contradiccion)   # False
```

### Sustituir valores con .subs()

Los objetos booleanos son `Expr` y aceptan `.subs()`. Util para evaluar una formula en una asignacion parcial.

```python
from sympy import symbols
from sympy.logic.boolalg import And, Or, Not

p, q = symbols("p q")

f = And(p, Or(q, Not(p)))
f.subs(p, True)              # q  -> se simplifica con p=True
f.subs([(p, True), (q, False)])  # False
```

### Simplificar formulas

Las formulas construidas con estos operadores se pueden minimizar con [[sympy.simplify_logic]].

```python
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import And, Or, Not

p, q = symbols("p q")

simplify_logic(Or(And(p, q), And(p, Not(q))))  # p
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Usar `and`/`or`/`not` de Python | Evaluan a Python `bool`, no crean objetos simbolicos | Usar `And`, `Or`, `Not` de `sympy.logic.boolalg` |
| `And(True, False)` devuelve `False` directo | Con literales Python la formula se evalua | Usar simbolos `symbols("p q")` para mantener el objeto |
| `Implies` no esta en `sympy` top-level | No se exporta directamente desde `sympy` | Importar desde `sympy.logic.boolalg` |
| Confundir `Xor` con `Or` | `Xor` es verdadero solo si exactamente uno es verdadero | Revisar la tabla de verdad antes de elegir |

## Notas relacionadas

- [[sympy.satisfiable]]
- [[sympy.simplify_logic]]
- [[sympy.logic/index | sympy.logic]]
