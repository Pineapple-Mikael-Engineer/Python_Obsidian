---
title: sympy.simplify_logic — simplificar expresiones logicas booleanas
aliases: [simplify_logic, CNF, DNF, forma normal]
tags: [sympy, api/funcion, logic]
lib: sympy
mod: sympy.logic
tipo: funcion
retorna: BooleanExpr
requiere: []
draft: false
---

# sympy.simplify_logic — simplificar expresiones logicas booleanas

`simplify_logic(expr)` reduce una formula booleana a su forma mas compacta, o la convierte a una forma canonica especifica: **CNF** (Forma Normal Conjuntiva, conjuncion de disyunciones) o **DNF** (Forma Normal Disyuntiva, disyuncion de conjunciones). Si no se especifica `form`, SymPy elige la representacion mas simple. Acepta formulas construidas con [[sympy.operadores_logicos]] y devuelve una nueva `BooleanExpr` equivalente logicamente a la original.

Es la contraparte logica de `simplify` para expresiones algebraicas: misma idea, dominio diferente.

## Firma

```python
sympy.simplify_logic(
    expr,           # BooleanExpr a simplificar
    form=None,      # None | 'cnf' | 'dnf'
    deep=True,      # si simplificar subexpresiones
) -> BooleanExpr
```

## Valor de retorno

| Tipo | Descripcion |
|------|-------------|
| `BooleanExpr` | Formula equivalente simplificada o en la forma pedida |
| `True` / `False` | Si la formula es tautologia o contradiccion |

```python
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import And, Or, Not

p, q = symbols("p q")

simplify_logic(Or(And(p, q), And(p, Not(q))))  # p
simplify_logic(And(Or(p, q), Or(p, Not(q))))   # p
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Simplificar al minimo | `simplify_logic(expr)` |
| Forzar CNF | `simplify_logic(expr, form='cnf')` |
| Forzar DNF | `simplify_logic(expr, form='dnf')` |
| Sin simplificar subexpresiones | `simplify_logic(expr, deep=False)` |

## Parametros en detalle

### `form`

Controla la forma canonica de salida.

| Valor | Forma | Estructura | Uso tipico |
|-------|-------|------------|------------|
| `None` | Libre | La mas compacta | Minimizar antes de comparar o exportar |
| `'cnf'` | Conjuntiva | `(a \| b) & (c \| d) & ...` | Preparar para SAT solvers externos |
| `'dnf'` | Disyuntiva | `(a & b) \| (c & d) \| ...` | Tablas de verdad, circuitos logicos |

```python
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import And, Or, Not, Implies

p, q = symbols("p q")

# Implicacion -> forma CNF
simplify_logic(Implies(p, q), form='cnf')   # ~p | q
simplify_logic(Implies(p, q), form='dnf')   # ~p | q  (ya es minima)

# Formula mas compleja
f = Or(And(p, q), And(Not(p), Not(q)))
simplify_logic(f)               # Equivalent(p, q) o ~p ^ ~q segun version
simplify_logic(f, form='cnf')   # (~p | q) & (p | ~q)
simplify_logic(f, form='dnf')   # (p & q) | (~p & ~q)
```

### `deep`

Cuando `True` (por defecto), la simplificacion desciende a subexpresiones. Con `False` solo actua en el nivel raiz, util para formulas muy grandes donde el tiempo importa.

## Casos de uso

### Minimizar antes de pasar a satisfiable

Simplificar primero reduce el espacio de busqueda de [[sympy.satisfiable]] en formulas redundantes.

```python
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import And, Or, Not
from sympy.logic.inference import satisfiable

p, q = symbols("p q")

formula = Or(And(p, q), And(p, Not(q)), And(Not(p), q))
compacta = simplify_logic(formula)   # p | q
satisfiable(compacta)                # {p: False, q: True}
```

### Convertir implicaciones a CNF para un SAT solver

Los SAT solvers externos esperan CNF. `simplify_logic` elimina `Implies` y `Equivalent` y agrupa en conjunciones.

```python
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import Implies, And

p, q, r = symbols("p q r")

f = And(Implies(p, q), Implies(q, r))
simplify_logic(f, form='cnf')   # (~p | q) & (~q | r)
```

### Detectar tautologias y contradicciones

```python
from sympy import symbols, simplify_logic
from sympy.logic.boolalg import Or, And, Not

p = symbols("p")

simplify_logic(Or(p, Not(p)))    # True   -> tautologia
simplify_logic(And(p, Not(p)))   # False  -> contradiccion
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| La salida no es la esperada en `form='cnf'` | SymPy puede reordenar o fusionar clausulas equivalentes | Verificar equivalencia logica, no igualdad textual |
| `simplify_logic` sobre una `Expr` algebraica | Solo opera en logica proposicional | Usar `simplify` para expresiones algebraicas |
| Resultado mas largo que la entrada | CNF/DNF canonicas pueden expandirse antes de simplificar | Usar `form=None` si solo interesa la forma mas corta |
| Lentitud en formulas grandes | `deep=True` con muchas variables | Probar `deep=False` o simplificar por partes |

## Notas relacionadas

- [[sympy.operadores_logicos]]
- [[sympy.satisfiable]]
- [[sympy.logic/index | sympy.logic]]
