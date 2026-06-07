---
title: sympy.div — division polinomica con cociente y resto
aliases:
  - div
  - sympy.div
  - division polinomica
tags:
  - sympy
  - api/funcion
  - polys/operaciones
lib: sympy
mod: sympy.polys
tipo: funcion
retorna: tuple (Expr, Expr)
draft: false
---

# sympy.div — division polinomica con cociente y resto

`div(p, q)` realiza la **division con resto** de un polinomio `p` (dividendo) entre `q` (divisor), devolviendo la **tupla** `(cociente, resto)` tal que `p = q*cociente + resto`, con el grado del resto menor que el de `q`. Es el algoritmo de Euclides polinomico y la operacion base sobre la que se construye el resto de la aritmetica de polinomios: [[sympy.gcd]] y [[sympy.lcm]] se apoyan en divisiones sucesivas.

> El resto vale `0` exactamente cuando `q` **divide** a `p`. Asi `div` sirve a la vez para dividir y para comprobar divisibilidad.

## Firma

```python
sympy.div(
    f,        # Expr | Poly: dividendo
    g,        # Expr | Poly: divisor
    *gens,    # Symbol(s): variable(s), normalmente inferidas
    **args    # opciones de dominio
) -> tuple   # (cociente, resto)
```

## Valor de retorno

| Posicion | Tipo | Significado |
|----------|------|-------------|
| `[0]` | `Expr` | Cociente `q` de la division |
| `[1]` | `Expr` | Resto `r`, con `grado(r) < grado(divisor)` |

Se cumple siempre la identidad `f = g * cociente + resto`.

```python
from sympy import symbols, div
x = symbols("x")
div(x**2 + 1, x + 1)     # (x - 1, 2)   -> x**2+1 = (x+1)(x-1) + 2
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Cociente y resto | `div(p, q)` |
| Solo el cociente | `div(p, q)[0]` |
| Solo el resto | `div(p, q)[1]` |

## Parametros en detalle

### `f`, `g` (dividendo y divisor)

`f` se divide entre `g`. La salida es siempre una tupla `(cociente, resto)`.

```python
from sympy import symbols, div
x = symbols("x")
div(x**2 + 2*x + 1, x + 1)    # (x + 1, 0)   -> division exacta, resto 0
div(x**2 + 1, x + 1)          # (x - 1, 2)   -> resto no nulo
```

### Division exacta (resto 0)

Cuando `g` divide a `f`, el resto es `0` y el cociente es el otro factor.

```python
from sympy import symbols, div
x = symbols("x")
div(x**3 - 1, x - 1)     # (x**2 + x + 1, 0)   -> (x-1) divide a x**3-1
```

### Cociente y resto no triviales

```python
from sympy import symbols, div
x = symbols("x")
div(x**3 + 2*x + 1, x**2 + 1)    # (x, x + 1)   -> grado del resto < 2
```

## Casos de uso

### Comprobar si un polinomio divide a otro

```python
from sympy import symbols, div
x = symbols("x")
div(x**3 - 1, x - 1)[1] == 0     # True  -> (x-1) | (x**3-1)
div(x**3 - 1, x + 1)[1] == 0     # False
```

### Verificar la identidad de la division

```python
from sympy import symbols, div, expand
x = symbols("x")
f, g = x**3 + 2*x + 1, x**2 + 1
q, r = div(f, g)                 # (x, x + 1)
expand(g*q + r)                  # x**3 + 2*x + 1   -> reconstruye f
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tratar el retorno como un solo polinomio | `div` devuelve `(cociente, resto)` | Desempaquetar: `q, r = div(f, g)` |
| Esperar resto siempre 0 | Solo es 0 si `g` divide a `f` | Revisar `div(f, g)[1]` |
| Olvidar el divisor como factor | `cociente` no es el resultado de simplificar `f/g` si hay resto | Usar `cancel` para fracciones que se simplifican |

## Limitaciones

- Trabaja con polinomios; el resto tiene grado **estrictamente menor** que el divisor.
- Para solo el cociente exacto existe `quo`, y para solo el resto `rem`; `div` los devuelve juntos.

## Notas relacionadas

- [[sympy.gcd]]
- [[sympy.lcm]]
- [[sympy.degree]]
- [[sympy.polys/operaciones/index | operaciones]]
