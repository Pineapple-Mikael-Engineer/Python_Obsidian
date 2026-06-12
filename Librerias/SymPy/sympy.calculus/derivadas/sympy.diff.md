---
title: sympy.diff — derivar una expresion simbolica
aliases:
  - diff
  - sympy.diff
  - derivar
  - Expr.diff
tags:
  - sympy
  - api/funcion
  - calculus/derivadas
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Expr
  - symbols
draft: false
---

# sympy.diff — derivar una expresion simbolica

`diff(f, x)` calcula la **derivada** de la expresion `f` respecto del simbolo `x` y devuelve una **expresion nueva** (`Expr`), ya **evaluada** y auto-simplificada. Es la funcion estandar para diferenciar: maneja polinomios, funciones trigonometricas, exponenciales, productos, cocientes y composiciones aplicando las reglas del calculo (producto, cociente, cadena). Para **derivadas de orden superior** se repite el simbolo o se indica el orden (`diff(f, x, 2)`); para **derivadas parciales** se listan varios simbolos (`diff(f, x, y)`). Existe tambien como **metodo** de cualquier `Expr`: `f.diff(x)` es equivalente a `diff(f, x)`.

> Cuando SymPy **no sabe** calcular la derivada (p. ej. una funcion sin definir `f(x)`), `diff` devuelve un objeto [[Derivative]] **sin evaluar** en vez de fallar.

## Firma

```python
sympy.diff(
    f,            # Expr: expresion a derivar
    *symbols,     # simbolos y/o ordenes: x | x, y | x, 2 | x, x | x, 2, y
    **kwargs,
) -> Expr
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `Expr` | La derivada **evaluada** y simplificada |
| [[Derivative]] | Objeto sin evaluar si SymPy no puede resolver la derivada |

```python
from sympy import symbols, diff
x = symbols("x")
diff(x**3, x)     # 3*x**2   -> Expr nueva
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Primera derivada respecto a `x` | `diff(f, x)` |
| Segunda derivada (orden explicito) | `diff(f, x, 2)` |
| Segunda derivada (simbolo repetido) | `diff(f, x, x)` |
| Tercera derivada | `diff(f, x, 3)` |
| Parcial mixta `∂²/∂x∂y` | `diff(f, x, y)` |
| Parcial `∂³/∂x²∂y` | `diff(f, x, 2, y)` |
| Como metodo de la expresion | `f.diff(x)` |

```python
from sympy import symbols, diff
x, y = symbols("x y")
diff(x**4, x, 2)        # 12*x**2
diff(x**4, x, x)        # 12*x**2   -> equivale a x, 2
diff(x**2 * y**3, x, y) # 6*x*y**2  -> derivada cruzada
(x**3).diff(x)          # 3*x**2    -> forma metodo
```

## Parametros en detalle

### `f` (obligatorio)

La expresion a derivar. Cualquier `Expr` valida: el simbolo respecto al que **no** se deriva se trata como constante.

```python
from sympy import symbols, diff
x = symbols("x")
diff(x**2 + 3*x, x)     # 2*x + 3
```

### `*symbols` — simbolos y ordenes

Tras `f` se listan los simbolos de derivacion. Un **entero** despues de un simbolo indica el **orden** respecto a ese simbolo; repetir el simbolo equivale a aumentar el orden.

```python
from sympy import symbols, diff
x = symbols("x")
diff(x**4, x, 3)        # 24*x     -> tercera derivada
diff(x**4, x, x, x)     # 24*x     -> identico, repitiendo x
```

Con **varios simbolos distintos** se obtiene una **derivada parcial** (se deriva en cadena, de izquierda a derecha).

```python
from sympy import symbols, diff
x, y = symbols("x y")
diff(x**2 * y**3, x, 2, y)   # 6*y**2   -> ∂³/∂x²∂y
diff(x * y, x, y)            # 1
```

## Casos de uso

### Derivadas de funciones elementales

```python
from sympy import symbols, diff, sin, exp, cos
x = symbols("x")
diff(sin(x), x)              # cos(x)
diff(exp(x) * cos(x), x)     # -exp(x)*sin(x) + exp(x)*cos(x)
diff(sin(x) * cos(x), x)     # -sin(x)**2 + cos(x)**2
```

### Pendiente de una curva en un punto

Derivar y luego particularizar con [[Expr.subs]] (`diff` no evalua en un punto por si mismo).

```python
from sympy import symbols, diff
x = symbols("x")
f = x**3 - 2*x
m = diff(f, x)         # 3*x**2 - 2
m.subs(x, 1)           # 1   -> pendiente en x=1
```

### Gradiente de un campo escalar

```python
from sympy import symbols, diff
x, y = symbols("x y")
f = x**2 * y + y**3
[diff(f, v) for v in (x, y)]   # [2*x*y, x**2 + 3*y**2]
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `diff(f, x, 2)` confundido con `diff(f, x, y)` | El segundo argumento puede ser orden (int) o simbolo | Entero = orden; simbolo = otra variable parcial |
| El resultado "no se evalua" (sale `Derivative(...)`) | SymPy no sabe derivar (p. ej. `f(x)` sin definir) | Es lo esperado; ver [[Derivative]] y `.doit()` |
| Esperar un numero al derivar | `diff` devuelve una `Expr`, no un valor | Particularizar con `f.diff(x).subs(x, x0)` |
| Olvidar reasignar | Las `Expr` son inmutables | `df = diff(f, x)` |
| Derivar respecto a algo que no es simbolo | Pasar un numero o expresion compuesta | El argumento de derivacion debe ser un `Symbol` |

## Limitaciones

- `diff` **deriva**; no integra (para eso `integrate`) ni resuelve ecuaciones diferenciales (`dsolve`).
- Con funciones sin definir o casos no resolubles devuelve un [[Derivative]] sin evaluar, que se completa con `.doit()` cuando sea posible.
- El resultado no siempre queda en la forma mas compacta; encadenar con `simplify`/`expand`/`factor` si se busca otra forma.

## Notas relacionadas

- [[Derivative]]
- [[Expr.subs]]
- [[sympy.calculus/derivadas/index | derivadas]]
