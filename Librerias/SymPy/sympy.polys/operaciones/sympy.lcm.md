---
title: sympy.lcm — minimo comun multiplo de polinomios y enteros
aliases:
  - lcm
  - sympy.lcm
  - minimo comun multiplo
tags:
  - sympy
  - api/funcion
  - polys/operaciones
lib: sympy
mod: sympy.polys
tipo: funcion
retorna: Expr
draft: false
---

# sympy.lcm — minimo comun multiplo de polinomios y enteros

`lcm(f, g)` calcula el **minimo comun multiplo** de dos polinomios: el polinomio de menor grado que es divisible por ambos. Es la operacion pareja de [[sympy.gcd]] y, como aquella, sirve igual para enteros (`lcm(4, 6)`). Su uso clasico es hallar el **denominador comun** al sumar fracciones de polinomios. Se relaciona con `gcd` por la identidad `gcd(f, g) * lcm(f, g) = f * g` (salvo signo/constante).

> Pareja de `gcd`: mientras `gcd` extrae los factores **compartidos**, `lcm` reune **todos** los factores de ambos sin repetir los comunes. Para `(x-1)(x+1)` y `(x-1)(x-2)`, el `lcm` es `(x-1)(x+1)(x-2)`.

## Firma

```python
sympy.lcm(
    f,        # Expr | Poly | int: primer polinomio (o entero)
    g=None,   # Expr | Poly | int: segundo polinomio (o entero)
    *gens,    # Symbol(s): variable(s), normalmente inferidas
    **args    # opciones de dominio
) -> Expr
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Polinomios | `Expr` | El multiplo comun de menor grado, normalizado monico |
| Enteros | `Integer` | El MCM entero clasico |
| Coprimos | `Expr` | El producto `f * g` (no comparten factores) |

```python
from sympy import symbols, lcm
x = symbols("x")
lcm(x**2 - 1, x**2 - 3*x + 2)   # x**3 - 2*x**2 - x + 2
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| MCM de dos polinomios | `lcm(p1, p2)` |
| MCM de dos enteros | `lcm(4, 6)` |
| Indicando la variable | `lcm(p1, p2, x)` |

## Parametros en detalle

### `f`, `g` (los dos polinomios)

Los dos operandos. El resultado se expande y se normaliza monico.

```python
from sympy import symbols, lcm, factor
x = symbols("x")
lcm(x**2 - 1, x**2 - 3*x + 2)        # x**3 - 2*x**2 - x + 2
factor(lcm(x**2 - 1, x**2 - 3*x + 2))  # (x - 2)*(x - 1)*(x + 1)
```

### Funciona tambien con enteros

```python
from sympy import lcm
lcm(4, 6)          # 12
lcm(7, 5)          # 35   -> coprimos: producto directo
```

### Relacion con `gcd`

El producto de `gcd` y `lcm` reproduce el producto de los polinomios.

```python
from sympy import symbols, gcd, lcm, expand
x = symbols("x")
f, g = x**2 - 1, x**2 - 3*x + 2
expand(gcd(f, g) * lcm(f, g))   # x**4 - 3*x**3 + x**2 + 3*x - 2
expand(f * g)                   # x**4 - 3*x**3 + x**2 + 3*x - 2   -> coinciden
```

## Casos de uso

### Denominador comun al sumar fracciones

```python
from sympy import symbols, lcm, div, together
x = symbols("x")
d1, d2 = x**2 - 1, x**2 - 3*x + 2
lcm(d1, d2)        # x**3 - 2*x**2 - x + 2  -> denominador comun de 1/d1 + 1/d2
together(1/d1 + 1/d2)   # forma compacta usando ese denominador
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar el producto siempre | Si comparten factores, `lcm < f*g` | Solo coincide con `f*g` cuando son coprimos |
| Resultado no monico esperado | `lcm` normaliza monico | Reescalar por una constante si se necesita otra forma |
| Confundir con `gcd` | `lcm` reune factores; `gcd` los comparte | Recordar `gcd*lcm = f*g` |

## Limitaciones

- Resultado **exacto** y monico; igual que [[sympy.gcd]].
- Para sumas de fracciones suele bastar `together`/`cancel`, que aplican `lcm`/`gcd` internamente.

## Notas relacionadas

- [[sympy.gcd]]
- [[sympy.div]]
- [[sympy.degree]]
- [[sympy.polys/operaciones/index | operaciones]]
