---
title: Limit — el limite sin evaluar como objeto simbolico
aliases:
  - Limit
  - limite sin evaluar
tags:
  - sympy
  - api/clase
  - calculus/limites
lib: sympy
mod: sympy.calculus
tipo: clase
retorna: Limit
requiere:
  - Symbol
  - Expr
draft: false
---

# Limit — el limite sin evaluar como objeto simbolico

`Limit(f, x, x0, dir)` construye el **limite sin evaluar**: un objeto [[Expr]] que *representa* `lim_{x->x0} f` pero no lo calcula. Es la forma "perezosa" de [[sympy.limit]]: sirve para **mostrar el planteamiento** (en pantalla, en LaTeX, en una deduccion paso a paso) y se evalua solo cuando lo pides con `.doit()`. La firma de argumentos es identica a la de la funcion `limit`; de hecho `limit(f, x, x0, dir)` equivale a `Limit(f, x, x0, dir).doit()`.

> Usa `Limit` cuando quieras **ver** o **manipular** el limite como expresion (renderizarlo, sustituir dentro, encadenar pasos); usa la funcion [[sympy.limit]] cuando solo quieras el **valor**.

## Constructor

```python
sympy.Limit(
    e,            # Expr: la expresion f
    z,            # Symbol: la variable
    z0,           # Expr: el punto destino (numero, simbolo, oo, -oo)
    dir="+",      # str: "+" derecha | "-" izquierda | "+-" bilateral
) -> Limit
```

Crear un `Limit` **no dispara ningun calculo**: queda planteado.

```python
from sympy import symbols, Limit, sin
x = symbols("x")
L = Limit(sin(x)/x, x, 0)
L          # Limit(sin(x)/x, x, 0, dir='+')   -> queda sin evaluar
```

## `.doit()` — evaluar el limite

`.doit()` resuelve el limite planteado y devuelve la [[Expr]] resultante (el mismo valor que daria la funcion `limit`).

```python
from sympy import symbols, Limit, sin
x = symbols("x")
Limit(sin(x)/x, x, 0).doit()    # 1
```

```python
from sympy import symbols, Limit
x = symbols("x")
Limit(1/x, x, 0, "-").doit()    # -oo   -> el dir se respeta al evaluar
```

## Atributos utiles

El objeto guarda sus componentes en `.args`, accesibles para inspeccionarlo o reconstruirlo.

| Acceso | Devuelve |
|--------|----------|
| `L.args` | tupla `(f, x, x0, dir)` |
| `L.args[0]` | la expresion `f` |
| `L.args[2]` | el punto `x0` |

```python
from sympy import symbols, Limit, sin
x = symbols("x")
L = Limit(sin(x)/x, x, 0)
L.args        # (sin(x)/x, x, 0, +)
L.args[0]     # sin(x)/x
```

## Mostrar el planteamiento

El uso tipico de `Limit` es **renderizar** el limite antes de resolverlo, en notebooks o documentos.

```python
from sympy import symbols, Limit, sin, latex, pprint
x = symbols("x")
L = Limit(sin(x)/x, x, 0)

latex(L)      # '\\lim_{x \\to 0^+}\\left(\\frac{\\sin{\\left(x \\right)}}{x}\\right)'
pprint(L)     # imprime el simbolo lim con la notacion matematica
L.doit()      # 1   -> y al final se evalua
```

## Casos de uso

### Plantear y luego resolver (deduccion en dos pasos)

```python
from sympy import symbols, Limit, oo
x = symbols("x")
L = Limit((1 + 1/x)**x, x, oo)   # planteamiento: queda Limit(...)
L.doit()                          # E   -> resultado
```

### Limite lateral mostrado explicitamente

```python
from sympy import symbols, Limit
x = symbols("x")
Lizq = Limit(1/x, x, 0, "-")
Lder = Limit(1/x, x, 0, "+")
Lizq.doit(), Lder.doit()    # (-oo, oo)   -> evidencia el salto de signo
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El `Limit` "no da el valor" | Crear `Limit` no evalua; solo plantea | Llamar `.doit()` para obtener el resultado |
| Se buscaba el valor y se uso la clase | `Limit` es la forma perezosa | Usar la funcion [[sympy.limit]] si solo quieres el numero |
| Se esperaba bilateral pero quedo `dir='+'` | El default del constructor es `"+"` | Pasar `dir="+-"` al construir el `Limit` |
| Pasar `float('inf')` como `z0` | SymPy usa su propio infinito | Importar y usar `oo` |

## Notas relacionadas

- [[sympy.limit]]
- [[Expr]]
- [[sympy.calculus/limites/index | limites]]
- [[sympy.calculus/index | sympy.calculus]]
