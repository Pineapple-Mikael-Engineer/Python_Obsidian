---
title: Derivative — derivada sin evaluar
aliases:
  - Derivative
  - derivada sin evaluar
  - derivada diferida
tags:
  - sympy
  - api/clase
  - calculus/derivadas
lib: sympy
mod: sympy
tipo: clase
retorna: Derivative
requiere:
  - Expr
  - Function
draft: false
---

# Derivative — derivada sin evaluar

`Derivative(f, x)` construye una derivada **sin calcularla**: representa la operacion "derivar `f` respecto de `x`" como un objeto simbolico (una `Expr`) que **no se evalua** hasta pedirlo con `.doit()`. Existe para poder **mostrar, manipular y razonar** sobre una derivada sin resolverla todavia: util al escribir formulas, ecuaciones diferenciales (`Eq` con derivadas) o cuando el calculo aun no se quiere disparar. Tambien es lo que devuelve [[sympy.diff]] cuando **no puede** resolver la derivada (p. ej. una funcion sin definir `f(x)`): en vez de fallar, deja la derivada pendiente.

> Diferencia clave con [[sympy.diff]]: `diff(f, x)` **evalua** y devuelve el resultado; `Derivative(f, x)` **no evalua** y devuelve la derivada diferida. Son las dos caras del mismo dato.

## Constructor

```python
sympy.Derivative(
    expr,         # Expr: expresion a derivar
    *variables,   # simbolos y/o ordenes: x | x, 2 | x, y
) -> Derivative
```

La misma sintaxis de simbolos y ordenes que [[sympy.diff]]: repetir el simbolo o pasar un entero indica el orden; varios simbolos distintos dan una parcial.

```python
from sympy import symbols, Derivative, sin
x = symbols("x")
Derivative(x**2, x)         # Derivative(x**2, x)        -> no evaluada
Derivative(sin(x), x, 2)    # Derivative(sin(x), (x, 2)) -> segunda derivada diferida
```

## Atributos utiles

| Atributo | Devuelve | Significado |
|----------|----------|-------------|
| `.expr` | `Expr` | La expresion que se deriva |
| `.variables` | `tuple` | Los simbolos de derivacion |
| `.args` | `tuple` | Componentes internas del nodo |

```python
from sympy import symbols, Derivative
x = symbols("x")
d = Derivative(x**2, x)
d.expr        # x**2
d.variables   # (x,)
```

## Evaluar con `.doit()`

`.doit()` **dispara** el calculo y devuelve la `Expr` resultante (cuando SymPy sabe resolverla).

```python
from sympy import symbols, Derivative, sin
x = symbols("x")
Derivative(x**2, x).doit()        # 2*x
Derivative(sin(x), x, 2).doit()   # -sin(x)
```

## Aparece cuando diff no puede resolver

Con una **funcion sin definir** (`Function`), `diff` no tiene regla que aplicar y devuelve un `Derivative` pendiente; al definir `f` mas tarde, `.doit()` lo completa.

```python
from sympy import symbols, diff, Function, Derivative
x = symbols("x")
f = Function("f")

diff(f(x), x)              # Derivative(f(x), x)   -> diff devuelve diferida
Derivative(f(x), x)        # Derivative(f(x), x)   -> identico, construida a mano

# Aparece dentro de un resultado mayor (regla del producto):
diff(x * f(x), x)          # x*Derivative(f(x), x) + f(x)
```

## Ejemplo: formula primero, calculo despues

```python
from sympy import symbols, Derivative, Eq, cos
x = symbols("x")

# Plantear la operacion sin resolverla (p. ej. para mostrarla)
expr = Derivative(cos(x), x)
expr            # Derivative(cos(x), x)

# Disparar el calculo cuando convenga
expr.doit()     # -sin(x)
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El resultado sale como `Derivative(...)` inesperado | SymPy no pudo evaluar (funcion sin definir) | Definir la funcion o llamar `.doit()` |
| `.doit()` "no hace nada" | La derivada de una funcion sin definir no se simplifica | Es correcto: queda diferida hasta tener `f` concreta |
| Esperar `Derivative` y obtener un valor | Se uso `diff`, que evalua | Usar `Derivative(...)` para la version sin evaluar |
| Olvidar reasignar tras `.doit()` | Las `Expr` son inmutables | `r = Derivative(f, x).doit()` |

## Limitaciones

- `Derivative` solo **representa** la derivada; el calculo real lo hace `.doit()` (o `diff` directamente).
- Si la expresion no es derivable simbolicamente, `.doit()` la deja igual (diferida).
- Para derivar y evaluar en un paso conviene [[sympy.diff]]; `Derivative` es para cuando se quiere la operacion **suspendida**.

## Notas relacionadas

- [[sympy.diff]]
- [[Expr.subs]]
- [[sympy.calculus/derivadas/index | derivadas]]
- [[Tree SymPy]]
