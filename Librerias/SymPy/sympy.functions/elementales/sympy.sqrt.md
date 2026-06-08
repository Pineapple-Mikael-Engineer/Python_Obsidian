---
title: sympy.sqrt — raiz cuadrada simbolica exacta
aliases:
  - sqrt
  - raiz cuadrada
tags:
  - sympy
  - api/funcion
  - functions/elementales
lib: sympy
mod: sympy.functions
tipo: funcion
retorna: Expr
requiere:
  - Symbol
  - concepto_symbols_assumptions
draft: false
---

# sympy.sqrt — raiz cuadrada simbolica exacta

`sqrt(x)` calcula la **raiz cuadrada exacta** de una expresion simbolica. No devuelve un flotante: devuelve una `Expr` que puede ser un numero exacto (`2`), una forma simplificada (`2*sqrt(2)`) o una forma no evaluada (`sqrt(x)`) cuando no hay una simplificacion posible. SymPy reconoce `sqrt` como una funcion propia (distinta de `x**Rational(1,2)`) y aplica reglas de simplificacion adicionales: extrae factores cuadrados perfectos, evalua sobre numeros racionales, y usa los **supuestos** del simbolo para simplificar expresiones como `sqrt(x**2)`.

Usala como punto de entrada por defecto cuando el objetivo sea trabajar con raices cuadradas de forma exacta. Para raices de otro indice usa `x**Rational(1, n)` o `root(x, n)`.

## Firma

```python
sympy.sqrt(x) -> Expr
```

`x` puede ser un numero, un `Symbol`, o cualquier `Expr`.

## Valor de retorno

| Tipo de salida | Cuando ocurre | Ejemplo |
|----------------|---------------|---------|
| `Integer` | `x` es un cuadrado perfecto | `sqrt(4)` → `2` |
| `Mul` con `sqrt` | `x` tiene factores cuadrados | `sqrt(8)` → `2*sqrt(2)` |
| `sqrt(Expr)` | No simplificable sin supuestos | `sqrt(x**2)` → `sqrt(x**2)` |
| `Symbol` / `Expr` | Supuesto `positive=True` activo | `sqrt(xp**2)` → `xp` |
| `Abs(x)` | Supuesto `real=True` (sin `positive`) | `sqrt(xr**2)` → `Abs(xr)` |

## Casos de uso

### Evaluacion exacta de numeros

```python
from sympy import sqrt

sqrt(4)     # 2
sqrt(9)     # 3
sqrt(2)     # sqrt(2)       -> irracional, se deja simbolico
sqrt(8)     # 2*sqrt(2)     -> extrae el factor cuadrado perfectoo
sqrt(12)    # 2*sqrt(3)
sqrt(Rational(1, 4))  # 1/2
```

### sqrt de una expresion con simbolo (sin supuestos)

```python
from sympy import sqrt, symbols

x = symbols("x")
sqrt(x**2)          # sqrt(x**2)   -> sin supuestos no simplifica
sqrt(x**2 + 2*x + 1)  # sqrt((x + 1)**2)  -> puede quedar sin evaluar
```

### Efecto de los supuestos sobre la simplificacion

```python
from sympy import sqrt, symbols

xr = symbols("x", real=True)
xp = symbols("x", positive=True)

sqrt(xr**2)         # Abs(x)   -> real pero puede ser negativo
sqrt(xp**2)         # x        -> positivo, por lo que sqrt(x**2) = x
```

### Simplificacion adicional con powsimp / nsimplify

```python
from sympy import sqrt, symbols, powsimp, nsimplify

x = symbols("x", positive=True)
expr = sqrt(x) * sqrt(x)
powsimp(expr)       # x

nsimplify(1.4142135623730951)  # sqrt(2)   -> recupera forma exacta desde float
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `sqrt(x**2)` no da `x` | Falta el supuesto `positive=True` | Declarar `symbols("x", positive=True)` |
| Confundir con `x**0.5` | El float `0.5` fuerza evaluacion numerica en ciertos contextos | Usar `sqrt(x)` o `x**Rational(1,2)` |
| Esperar simplificacion automatica de productos | `sqrt(x)*sqrt(y)` no da `sqrt(x*y)` sin supuestos | Usar `powsimp` o declarar supuestos positivos |
| `sqrt` de numero negativo da `I*sqrt(...)` | SymPy trabaja en los complejos por defecto | Es el comportamiento correcto; si se quiere forzar real, usar supuesto |

## Limitaciones

- `sqrt(x**2)` no simplifica a `x` a menos que `x` tenga el supuesto `positive=True`; con `real=True` devuelve `Abs(x)`.
- La simplificacion de `sqrt(a)*sqrt(b)` en `sqrt(a*b)` requiere `powsimp` o supuestos positivos; no ocurre de forma automatica.
- Para evaluar numericamente: `sqrt(2).evalf()` → `1.41421356237310`.

## Notas relacionadas

- [[sympy.exp_log]]
- [[Abs]]
- [[sympy.functions/elementales/index | elementales]]
- [[sympy.functions/index | sympy.functions]]
