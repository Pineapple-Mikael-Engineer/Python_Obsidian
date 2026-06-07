---
title: Expr — clase base de toda expresion simbolica (nodo de un arbol inmutable)
aliases:
  - Expr
  - expresion simbolica
  - clase base de expresiones
tags:
  - sympy
  - api/clase
  - core/expresiones
lib: sympy
mod: sympy.core
tipo: clase
retorna: Expr
requiere:
  - Symbol
  - concepto_expr_arbol
draft: false
---

# Expr — clase base de toda expresion simbolica (nodo de un arbol inmutable)

`Expr` es la **clase base** de la que hereda toda expresion matematica de SymPy: simbolos, numeros, sumas, productos, potencias, funciones (`sin`, `exp`…) y ecuaciones. No se instancia directamente con `Expr(...)`: se obtiene **construyendo** expresiones a partir de simbolos y operaciones aritmeticas (`x**2 + 1`), que SymPy representa internamente como un **arbol** de nodos `func`/`args`. Toda `Expr` es **inmutable**: ningun metodo la modifica en su sitio, todos devuelven una expresion **nueva**. Ver [[concepto_expr_arbol]] para el modelo mental completo del arbol.

> Distincion clave: una `Expr` no es texto ni un float. `x**2 + 1` es el arbol `Add(Pow(Symbol('x'), Integer(2)), Integer(1))`. La igualdad `==` compara **estructura** del arbol, no equivalencia matematica.

## Atributos estructurales

Todo nodo del arbol se describe con dos atributos; ver [[sympy.srepr]] para imprimir el arbol completo.

| Atributo | Tipo | Significado |
|----------|------|-------------|
| `.func` | clase | Constructor/tipo del nodo (`Add`, `Mul`, `Pow`, `sin`, `Symbol`…) |
| `.args` | `tuple` | Hijos (subexpresiones) del nodo; `()` si es un atomo |
| `.free_symbols` | `set` | Simbolos libres que aparecen en la expresion |

Se cumple la invariante `expr.func(*expr.args) == expr` para cualquier expresion.

```python
from sympy import symbols
x = symbols("x")
e = x**2 + 1
e.func              # <class 'sympy.core.add.Add'>
e.args              # (1, x**2)
e.free_symbols      # {x}
e.func(*e.args) == e   # True   -> reconstruye el nodo
```

## Metodos clave

| Metodo | Devuelve | Para que |
|--------|----------|----------|
| `.subs(old, new)` | `Expr` | Sustituir subexpresiones; ver [[Expr.subs]] |
| `.evalf(n)` | `Float` / `Expr` | Evaluar numericamente con `n` digitos; ver [[Expr.evalf]] |
| `.rewrite(f)` | `Expr` | Reescribir en terminos de otra funcion; ver [[Expr.rewrite]] |
| `.atoms(*tipos)` | `set` | Hojas del arbol (o atomos de un tipo dado) |
| `.xreplace(dict)` | `Expr` | Reemplazo estructural exacto, mas rapido que `subs` |

```python
from sympy import symbols, sin, cos, Symbol
x = symbols("x")
(x + 1).subs(x, 5)            # 6        -> expresion nueva
(x**2 + 1).atoms()           # {1, 2, x}
(x**2 + 1).atoms(Symbol)     # {x}      -> solo simbolos
sin(x).rewrite(cos)          # cos(x - pi/2)
(x + 1).evalf(subs={x: 2})   # 3.00000000000000
```

## Operaciones aritmeticas: construyen el arbol

Las operaciones `+ - * / **` sobre expresiones **no calculan un numero**: construyen un nuevo nodo del arbol (con auto-simplificacion ligera, como `x + x -> 2*x`).

| Operacion | Nodo resultante | `srepr` |
|-----------|-----------------|---------|
| `x + y` | `Add` | `Add(Symbol('x'), Symbol('y'))` |
| `x * y` | `Mul` | `Mul(Symbol('x'), Symbol('y'))` |
| `x**2` | `Pow` | `Pow(Symbol('x'), Integer(2))` |

```python
from sympy import symbols
x, y = symbols("x y")
(x + x)          # 2*x          -> auto-simplificacion
(x + y).func     # <class 'sympy.core.add.Add'>
(x * y).args     # (x, y)
```

## Inmutabilidad e igualdad estructural

`Expr` es inmutable y **hashable**: sirve de clave en `dict`/`set` y es segura de compartir, pero obliga a **reasignar** el resultado. La igualdad `==` es **estructural**, no matematica.

```python
from sympy import symbols, expand, simplify
x = symbols("x")
e = x + 1
e.subs(x, 5)            # 6        -> NUEVA expresion
e                       # x + 1    -> la original intacta (reasignar: e = e.subs(...))

(x + 1)**2 == x**2 + 2*x + 1            # False  -> arboles distintos
expand((x + 1)**2) == x**2 + 2*x + 1    # True   -> misma forma tras expandir
simplify((x + 1)**2 - (x**2 + 2*x + 1)) == 0   # True   -> equivalencia matematica
```

## Casos de uso

### Inspeccionar la estructura de una expresion

```python
from sympy import symbols
x = symbols("x")
e = x**2 + 2*x + 1
e.func                  # Add
e.args                  # (1, 2*x, x**2)
[a.func for a in e.args]  # [Integer, Mul, Pow]
```

### Extraer los simbolos de un modelo

```python
from sympy import symbols
a, b, t = symbols("a b t")
modelo = a * t + b
modelo.free_symbols     # {a, b, t}   -> que parametros/variables hay
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `e.subs(...)` no cambia `e` | `Expr` es inmutable | Reasignar: `e = e.subs(...)` |
| `a == b` da `False` "y deberian ser iguales" | `==` es estructural, no matematico | Comparar `simplify(a - b) == 0` |
| `TypeError: unhashable` al usar de clave | El objeto no era una `Expr` (p.ej. una lista) | Sympificar con `S(...)` o `sympify(...)` |
| `Expr(...)` falla o da algo raro | No se instancia la clase base directamente | Construir con `symbols(...)` y operadores |

## Limitaciones

- `Expr` modela expresiones **escalares**; las matrices son `Matrix` (no subclase de `Expr` en general).
- `==` nunca decide equivalencia matematica; usa `simplify`/`equals`.
- La auto-simplificacion al construir es minima: para transformar de verdad hay que llamar `expand`, `simplify`, `factor`, etc.

## Notas relacionadas

- [[concepto_expr_arbol]]
- [[Expr.subs]]
- [[Expr.evalf]]
- [[Expr.rewrite]]
- [[sympy.srepr]]
- [[Symbol]]
- [[sympy.core/expresiones/index | expresiones]]
