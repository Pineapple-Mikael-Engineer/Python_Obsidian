---
title: sympy.srepr — representacion exacta del arbol de una expresion como str
aliases:
  - srepr
  - sympy.srepr
  - representacion del arbol
tags:
  - sympy
  - api/funcion
  - core/expresiones
lib: sympy
mod: sympy.printing
tipo: funcion
retorna: str
requiere:
  - Expr
  - concepto_expr_arbol
draft: false
---

# sympy.srepr — representacion exacta del arbol de una expresion como str

`srepr(expr)` devuelve un **string** con la representacion **exacta y sin ambiguedad** del arbol interno de una expresion: muestra cada nodo con su constructor real y sus hijos, p.ej. `Add(Symbol('x'), Integer(1))`. A diferencia de `str()`/`print`, que dan la forma matematica legible (`x + 1`), `srepr` revela como SymPy guarda la expresion: tipos de los numeros, orden de `args`, supuestos de los simbolos. Es la herramienta para **depurar** y entender la estructura de una `Expr`; ver [[concepto_expr_arbol]].

> Distincion clave: `str(x + 1)` da `"x + 1"` (legible). `srepr(x + 1)` da `"Add(Symbol('x'), Integer(1))"` (estructura). El string de `srepr` es ademas **valido como codigo Python**: pegado en un interprete con los nombres importados, reconstruye la expresion.

## Firma

```python
sympy.srepr(
    expr,            # Expr | cualquier objeto sympificable
    **settings,      # opciones del printer (rara vez necesarias)
) -> str
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `str` | Arbol completo nodo a nodo: `Func(arg1, arg2, ...)`, con los tipos exactos de cada hoja (`Symbol`, `Integer`, `Rational`, `Float`…) |

```python
from sympy import symbols, srepr
x = symbols("x")
srepr(x**2 + 1)     # "Add(Pow(Symbol('x'), Integer(2)), Integer(1))"
```

## srepr frente a str/print

| Forma | Salida para `x**2 + 1` | Para que sirve |
|-------|------------------------|----------------|
| `print(x**2 + 1)` / `str(...)` | `x**2 + 1` | Lectura matematica, salida final |
| `srepr(x**2 + 1)` | `Add(Pow(Symbol('x'), Integer(2)), Integer(1))` | Depurar la estructura interna |
| `pprint(x**2 + 1)` | render en 2D (potencias arriba) | Presentacion bonita en consola |

```python
from sympy import symbols, srepr, Rational
x = symbols("x")
str(x**2 + 1)        # 'x**2 + 1'
srepr(x**2 + 1)      # "Add(Pow(Symbol('x'), Integer(2)), Integer(1))"

# srepr distingue tipos que str oculta:
str(Rational(1, 2))    # '1/2'
srepr(Rational(1, 2))  # 'Rational(1, 2)'   -> NO un Float
```

## Casos de uso

### Entender por que dos expresiones no son `==`

`==` es estructural; cuando dos expresiones "deberian" ser iguales pero dan `False`, `srepr` muestra la diferencia real de arboles.

```python
from sympy import symbols, srepr
x = symbols("x")
srepr((x + 1)**2)         # "Pow(Add(Symbol('x'), Integer(1)), Integer(2))"
srepr(x**2 + 2*x + 1)     # "Add(Pow(Symbol('x'), Integer(2)), Mul(Integer(2), Symbol('x')), Integer(1))"
# -> arboles distintos, por eso == da False
```

### Revelar los supuestos de un simbolo

Los `assumptions` viajan dentro del nodo `Symbol` y solo se ven con `srepr`.

```python
from sympy import symbols, srepr
p = symbols("p", positive=True)
srepr(p)      # "Symbol('p', positive=True)"
```

### Distinguir entero exacto de flotante

```python
from sympy import srepr, Integer, Float, S
srepr(S(2))        # 'Integer(2)'      -> entero exacto
srepr(Float(2.0))  # "Float('2.0', precision=53)"   -> flotante
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar salida "bonita" de `srepr` | `srepr` es para estructura, no presentacion | Usar `pprint` o `print` para legibilidad |
| `srepr` de un float da `Float('...', precision=...)` "feo" | Es la representacion exacta, a proposito | Normal; usar `str`/`evalf` para mostrar el numero |
| Pegar la salida y que falle | Faltan imports (`Add`, `Symbol`, `Integer`…) | Importar los constructores que aparecen en el string |

## Notas relacionadas

- [[concepto_expr_arbol]]
- [[Expr]]
- [[Expr.subs]]
- [[sympy.core/expresiones/index | expresiones]]
