---
title: Piecewise — funcion definida a trozos
aliases: [Piecewise, funcion a trozos]
tags: [sympy, api/clase, functions/especiales]
lib: sympy
mod: sympy.functions
tipo: clase
retorna: Expr
requiere: [Symbol]
draft: false
---

# Piecewise — funcion definida a trozos

`Piecewise` construye una **funcion definida a trozos** como objeto simbolico de SymPy. Cada argumento es una tupla `(expresion, condicion)`; SymPy evalua los trozos **en orden** y usa el primero cuya condicion se cumpla. La ultima condicion suele ser `True` para capturar el caso por defecto. El objeto resultante soporta `subs`, `diff` e `integrate` simbolicos de forma directa: SymPy aplica cada operacion a cada trozo sobre su dominio correspondiente. Es la herramienta natural para representar funciones absolutas, funciones por ramos en EDOs y condiciones de frontera.

## Firma

```python
sympy.Piecewise(
    (expr_1, condicion_1),
    (expr_2, condicion_2),
    ...
    (expr_n, True),        # caso por defecto (obligatorio si hay gaps)
) -> Expr
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `(expr, cond)` | `tuple[Expr, BooleanExpr]` | Par expresion-condicion; se evaluan en orden |
| `True` como condicion | `bool` | Captura cualquier valor no cubierto por condiciones anteriores |

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `Expr` evaluada | Si la condicion se puede determinar con los datos (p.ej. `x` numerica via `subs`) |
| `Piecewise(...)` | Si `x` es simbolica y no se puede determinar el trozo activo |

## Casos de uso

### Construccion basica y evaluacion

```python
from sympy import symbols, Piecewise

x = symbols("x")
f = Piecewise((x**2, x >= 0), (-x, True))

f.subs(x, 2)    # 4    (x=2 >= 0, usa x**2)
f.subs(x, -3)   # 3    (x=-3 < 0, usa -x = -(-3) = 3)
f.subs(x, 0)    # 0    (x=0 >= 0, usa x**2 = 0)
```

### Derivacion simbolica

`diff` aplica la derivada a cada trozo dentro de su dominio.

```python
from sympy import symbols, Piecewise, diff

x = symbols("x")
f = Piecewise((x**2, x >= 0), (-x, True))

diff(f, x)
# Piecewise((2*x, x >= 0), (-1, True))
```

### Integracion simbolica

```python
from sympy import symbols, Piecewise, integrate

x = symbols("x")
f = Piecewise((x**2, x >= 0), (0, True))

integrate(f, (x, -1, 2))   # 8/3    (solo el trozo x>=0 contribuye: int_0^2 x^2 dx)
```

### Reescribir Abs como Piecewise (manual)

`Abs(x).rewrite(Piecewise)` no simplifica en algunas versiones; la forma manual es mas robusta.

```python
from sympy import symbols, Piecewise

x = symbols("x")
# Equivalente manual de Abs(x):
abs_manual = Piecewise((x, x > 0), (-x, True))
abs_manual.subs(x, 3)    # 3
abs_manual.subs(x, -5)   # 5
abs_manual.subs(x, 0)    # 0
```

### Funcion signo

```python
from sympy import symbols, Piecewise

x = symbols("x")
signo = Piecewise((1, x > 0), (-1, x < 0), (0, True))
signo.subs(x, 5)    # 1
signo.subs(x, -2)   # -1
signo.subs(x, 0)    # 0
```

### Ecuaciones diferenciales con condicion por tramos

`Piecewise` puede usarse como termino forzante en `dsolve` para representar funciones de entrada discontinuas.

```python
from sympy import symbols, Piecewise, Function, dsolve, Eq, diff

t = symbols("t")
y = Function("y")

# Entrada escalon: 0 para t<1, 1 para t>=1
entrada = Piecewise((0, t < 1), (1, True))
ode = Eq(diff(y(t), t) + y(t), entrada)
# dsolve(ode, y(t))  -> solucion por tramos (requiere condicion inicial)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El ultimo trozo no tiene condicion `True` | Si ningun trozo cubre un punto, `subs` devuelve `nan` | Agregar siempre `(expr, True)` como ultimo par |
| Condiciones solapadas | SymPy evalua en **orden**; el primero que se cumple gana | Ordenar de mas restrictivo a mas general |
| `diff` da resultado inesperado en la frontera | Las derivadas en puntos de discontinuidad son distribucionales | Usar [[sympy.Heaviside_DiracDelta]] para el tratamiento distribucional |
| `Abs(x).rewrite(Piecewise)` no simplifica | Comportamiento dependiente de la version | Construir el `Piecewise` manualmente |

## Limitaciones

- En algunos contextos, `lambdify` con `Piecewise` requiere el modulo `"numpy"` para vectorizar correctamente.
- La integracion de `Piecewise` puede producir resultados complicados si las condiciones involucran mas de una variable.
- SymPy no siempre simplifica automaticamente dos `Piecewise` con trozos complementarios; usar `piecewise_fold` de `sympy.functions.elementary.piecewise`.

## Notas relacionadas

- [[sympy.Heaviside_DiracDelta]]
- [[sympy.functions/especiales/index | especiales]]
- [[sympy.functions/index | sympy.functions]]
