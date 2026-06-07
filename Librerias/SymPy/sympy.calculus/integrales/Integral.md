---
title: Integral — integral simbolica sin evaluar
aliases:
  - Integral
  - integral sin evaluar
tags:
  - sympy
  - api/clase
  - calculus/integrales
lib: sympy
mod: sympy.integrals
tipo: clase
retorna: Integral
requiere:
  - Symbol
  - Expr
draft: false
---

# Integral — integral simbolica sin evaluar

`Integral(f, x)` o `Integral(f, (x, a, b))` construye una integral **sin evaluarla**: representa la **operacion** de integrar como un objeto simbolico, no su resultado. Es una `Expr` mas, asi que se puede mostrar, manipular y sustituir. Sirve para **plantear** una integral (mostrar el "∫ … dx" en el render), retrasar el calculo, o recibir lo que devuelve [[sympy.integrate]] cuando no halla primitiva. Para **evaluarla** se llama a `.doit()`, que intenta resolverla y devuelve la `Expr` del resultado (o el mismo `Integral` si no puede).

> `Integral(f, x)` **no integra**; solo guarda el planteamiento. Es `integrate(f, x)` (o `Integral(...).doit()`) lo que ejecuta el calculo.

## Constructor

```python
Integral(
    function,            # Expr: integrando
    *symbols,            # x (indefinida) | (x, a, b) (definida) | varias tuplas (multiple)
) -> Integral
```

Mismo lenguaje de limites que [[sympy.integrate]]: un simbolo suelto para la indefinida, una tupla `(x, a, b)` para la definida, varias tuplas para integrales multiples (la primera es la mas interna).

## Construir vs evaluar

| Accion | Llamada | Resultado |
|--------|---------|-----------|
| Plantear (sin evaluar) | `Integral(f, (x, a, b))` | `Integral` simbolico |
| Evaluar | `Integral(f, (x, a, b)).doit()` | `Expr` con el valor |
| Atajo directo | `integrate(f, (x, a, b))` | equivalente a construir + `.doit()` |

```python
from sympy import symbols, Integral, sin
x = symbols("x")

I = Integral(sin(x), x)        # Integral(sin(x), x)   -> sin evaluar
I.doit()                       # -cos(x)               -> ya evaluado
```

## .doit() — disparar el calculo

`.doit()` ejecuta la integracion y devuelve la `Expr` del resultado. Si la integral no tiene primitiva en forma cerrada, devuelve el **mismo `Integral` sin cambios**.

```python
from sympy import symbols, Integral, Function
x, a, b = symbols("x a b")

Integral(x**2, (x, 0, 1)).doit()          # 1/3
Integral(x, x).doit()                     # x**2/2   -> indefinida

f = Function("f")
Integral(f(x), (x, a, b)).doit()          # Integral(f(x), (x, a, b))  -> intacta
```

## Atributos utiles

Un `Integral` expone sus piezas para inspeccionarlo sin evaluarlo.

| Atributo | Devuelve | Ejemplo |
|----------|----------|---------|
| `.function` | el integrando | `x**2` |
| `.limits` | tupla de limites | `((x, 0, 1),)` |
| `.free_symbols` | simbolos libres | `set()` si esta acotada |

```python
from sympy import symbols, Integral
x = symbols("x")
I = Integral(x**2, (x, 0, 1))
I.function        # x**2
I.limits          # ((x, 0, 1),)
I.free_symbols    # set()   -> integral definida sin parametros
```

## Ejemplo: mostrar el planteamiento y luego resolver

Patron tipico en una nota o reporte: primero se **muestra** la integral, despues se **evalua**.

```python
from sympy import symbols, Integral, exp, oo
x = symbols("x")

planteo = Integral(exp(-x), (x, 0, oo))   # Integral(exp(-x), (x, 0, oo))
# ...se muestra/escribe el planteo...
planteo.doit()                            # 1   -> resultado exacto
```

Para el render bonito del simbolo "∫" usar `pprint(planteo)`, `latex(planteo)` o `init_printing()`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El `Integral` "no se resuelve solo" | Construirlo no evalua; es lo esperado | Llamar `.doit()` (o usar `integrate`) |
| `.doit()` devuelve el mismo `Integral` | No hay primitiva cerrada conocida | Aceptarlo, o evaluar numericamente con `.evalf()` |
| Confundir `Integral` con `integrate` | `Integral` plantea; `integrate` resuelve | Usar `integrate` si quieres el resultado directo |
| Pasar limite mal | Falta la tupla `(x, a, b)` | Construir con `Integral(f, (x, a, b))` |

## Notas relacionadas

- [[sympy.integrate]]
- [[sympy.diff]]
- [[Expr.subs]]
- [[sympy.calculus/integrales/index | integrales]]
