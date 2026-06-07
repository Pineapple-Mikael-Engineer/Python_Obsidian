---
title: Expr y el arbol de expresiones — toda expresion es un arbol inmutable
aliases:
  - Expr
  - arbol de expresiones
  - func y args
tags:
  - sympy
  - concepto
  - fundamentos
lib: sympy
mod: sympy
tipo: concepto
requiere:
  - concepto_symbols_assumptions
draft: false
---

# Expr y el arbol de expresiones — toda expresion es un arbol inmutable

## Definicion fundamental

Toda expresion de SymPy es una instancia de **`Expr`** representada internamente como un **arbol**: un nodo raiz (la operacion: suma, producto, potencia, funcion) con **hijos** (sus operandos), que a su vez son expresiones. `x**2 + 1` no es texto ni un numero: es el arbol `Add(Pow(Symbol('x'), Integer(2)), Integer(1))`.

Dos atributos describen cualquier nodo:

- **`.func`** — el constructor/tipo del nodo (`Add`, `Mul`, `Pow`, `sin`, `Symbol`…).
- **`.args`** — la tupla de hijos (sus subexpresiones).

```python
from sympy import symbols, srepr
x = symbols("x")
e = x**2 + 1
e.func        # <class 'sympy.core.add.Add'>
e.args        # (1, x**2)
(x**2).func   # <class 'sympy.core.power.Pow'>
(x**2).args   # (x, 2)
srepr(e)      # "Add(Pow(Symbol('x'), Integer(2)), Integer(1))"
```

## La invariante: func + args reconstruye el nodo

Para **cualquier** expresion se cumple `expr.func(*expr.args) == expr`. Esa es la base de recorrer y transformar arboles: puedes descomponer un nodo y reconstruirlo.

```python
from sympy import sin
e = sin(x) + 1
e.func(*e.args) == e    # True
```

> [!regla]
> Los **atomos** (hojas del arbol) tienen `.args == ()`: simbolos (`x`), enteros (`Integer(2)`), racionales, constantes (`pi`). Todo lo demas es un nodo compuesto con hijos.

## Inmutabilidad: nada se modifica in-place

Las expresiones de SymPy son **inmutables**. Ningun metodo cambia la expresion original; todos **devuelven una nueva**. No existe el equivalente a modificar una lista en su sitio.

```python
e = x + 1
e.subs(x, 5)   # 6     -> devuelve una expresion NUEVA
e              # x + 1 -> la original intacta
```

Esto hace que las expresiones sean **hashables** (sirven de clave en `dict`/`set`) y seguras de compartir, pero obliga a **reasignar**: `e = e.subs(...)`, nunca esperar que `e` cambie solo.

## Recorrer el arbol

```python
from sympy import preorder_traversal
e = x**2 + 2*x + 1
list(preorder_traversal(e))
# [x**2 + 2*x + 1, x**2, x, 2, 2*x, 2, x, 1]   -> todos los subnodos
e.atoms()              # {1, 2, x}              -> hojas unicas
list(e.free_symbols)   # [x]                    -> simbolos libres
```

## Igualdad estructural, no matematica

`==` compara la **estructura** del arbol, no la equivalencia matematica. `(x+1)**2` y `x**2+2*x+1` son matematicamente iguales pero arboles distintos: `==` da `False`.

```python
from sympy import expand, simplify
(x + 1)**2 == x**2 + 2*x + 1            # False  -> distinta forma
expand((x + 1)**2) == x**2 + 2*x + 1    # True   -> misma forma tras expandir
simplify((x+1)**2 - (x**2+2*x+1)) == 0  # True   -> equivalencia via simplify
```

## Casos que confunden

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `e.subs(...)` no cambia `e` | las expresiones son inmutables | reasignar: `e = e.subs(...)` |
| `a == b` da `False` y "deberian ser iguales" | `==` es estructural, no matematico | comparar `simplify(a-b) == 0` |
| `TypeError: unhashable` al usar de clave | el objeto no era una `Expr` (p.ej. lista) | sympificar con `S(...)` |

## Relacion con otros conceptos

- [[concepto_symbols_assumptions]]
- [[concepto_simplificacion_automatica]]
- [[concepto_simbolico_vs_numerico]]
