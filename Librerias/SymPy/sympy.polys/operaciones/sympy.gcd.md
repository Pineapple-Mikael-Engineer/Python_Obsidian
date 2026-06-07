---
title: sympy.gcd — maximo comun divisor de polinomios y enteros
aliases:
  - gcd
  - sympy.gcd
  - maximo comun divisor
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

# sympy.gcd — maximo comun divisor de polinomios y enteros

`gcd(f, g)` calcula el **maximo comun divisor** de dos polinomios: el polinomio de mayor grado que divide a ambos sin resto. Es el analogo polinomico del MCD de enteros y, de hecho, la misma funcion sirve para enteros (`gcd(12, 18)`). Su uso tipico es **simplificar fracciones de polinomios** (dividir numerador y denominador por su `gcd`) y detectar **factores comunes**. El resultado se normaliza a un polinomio monico (coeficiente lider 1) cuando es posible.

> El `gcd` de dos polinomios captura su parte factorizable comun: si `f = (x-1)(x+1)` y `g = (x-1)(x-2)`, su factor compartido es `x - 1`, y eso es exactamente lo que devuelve `gcd`.

## Firma

```python
sympy.gcd(
    f,        # Expr | Poly | int: primer polinomio (o entero)
    g=None,   # Expr | Poly | int: segundo polinomio (o entero)
    *gens,    # Symbol(s): variable(s), normalmente inferidas
    **args    # opciones de dominio (p.ej. polys=True)
) -> Expr
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Polinomios | `Expr` | El polinomio comun de mayor grado, normalizado monico |
| Enteros | `Integer` | El MCD entero clasico |
| Sin factor comun | `Expr` | `1` (son coprimos) |

```python
from sympy import symbols, gcd
x = symbols("x")
gcd(x**2 - 1, x**2 - 3*x + 2)   # x - 1
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| MCD de dos polinomios | `gcd(p1, p2)` |
| MCD de dos enteros | `gcd(12, 18)` |
| Indicando la variable | `gcd(p1, p2, x)` |

## Parametros en detalle

### `f`, `g` (los dos polinomios)

Los dos operandos. SymPy infiere la variable a partir de las expresiones; con polinomios de una sola variable no hace falta pasarla.

```python
from sympy import symbols, gcd
x = symbols("x")
gcd(x**2 - 1, x**2 - 3*x + 2)        # x - 1   -> factor comun (x-1)
gcd(x**2 + 2*x + 1, x**2 - 1)        # x + 1   -> (x+1)^2 y (x-1)(x+1) comparten x+1
```

### Funciona tambien con enteros

La misma funcion sirve para el MCD numerico; devuelve un `Integer`.

```python
from sympy import gcd
gcd(12, 18)        # 6
gcd(7, 5)          # 1   -> coprimos
```

### `*gens` (la variable, cuando hace falta)

Si la expresion es multivariable conviene indicar respecto a que generador trabajar.

```python
from sympy import symbols, gcd
x, y = symbols("x y")
gcd(x**2*y - y, x*y - y)        # y*(x - 1)   -> factor comun en ambas variables
```

## Casos de uso

### Simplificar una fraccion de polinomios a mano

```python
from sympy import symbols, gcd, div
x = symbols("x")
num = x**2 - 1
den = x**2 - 3*x + 2
g = gcd(num, den)                    # x - 1
div(num, g)[0], div(den, g)[0]       # (x + 1, x - 2)  -> (x+1)/(x-2)
```

### Comprobar si dos polinomios son coprimos

```python
from sympy import symbols, gcd
x = symbols("x")
gcd(x**2 + 1, x - 5) == 1     # True  -> no comparten raices
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Esperar la factorizacion completa | `gcd` da el factor **comun**, no factoriza cada polinomio | Usar `factor` para descomponer uno solo |
| Resultado no monico esperado | `gcd` normaliza el coeficiente lider a 1 | Multiplicar por la constante deseada si se requiere otra forma |
| Variable ambigua en multivariable | No se indico el generador | Pasar la variable: `gcd(f, g, x)` |

## Limitaciones

- Devuelve un resultado **exacto** y normalizado monico; no preserva un factor constante particular.
- Para fracciones, combinarlo con [[sympy.div]] o usar directamente `cancel`/`simplify`, que ya aplican el `gcd` internamente.

## Notas relacionadas

- [[sympy.lcm]]
- [[sympy.div]]
- [[sympy.degree]]
- [[sympy.polys/operaciones/index | operaciones]]
