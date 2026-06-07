---
title: sympy.exp_log — exponencial y logaritmo simbolicos
aliases:
  - exp
  - log
  - exponencial simbolica
  - logaritmo simbolico
tags:
  - sympy
  - api/funcion
  - functions/elementales
lib: sympy
mod: sympy.functions
tipo: concepto
requiere:
  - Symbol
  - concepto_symbols_assumptions
draft: false
---

# sympy.exp_log — exponencial y logaritmo simbolicos

`exp(x)` y `log(x)` son las funciones exponencial y logaritmica naturales de SymPy. Trabajan de forma **exacta**: no aproximan, sino que devuelven `Expr` que pueden simplificarse o evaluarse segun sea necesario. `exp(x)` representa `e^x`; `log(x)` es el logaritmo natural (base `E`); `log(x, b)` es el logaritmo en base `b`. Son funciones simbolicas inversas entre si, aunque la simplificacion de `log(exp(x))` no ocurre automaticamente sin supuestos.

Usa este par como base para construir expresiones exponenciales y logaritmicas exactas antes de simplificar, integrar o derivar.

## Firmas

```python
sympy.exp(x)           -> Expr   # e^x
sympy.log(x)           -> Expr   # ln(x), logaritmo natural
sympy.log(x, b)        -> Expr   # log_b(x) = log(x)/log(b)
```

`x` y `b` pueden ser numeros, `Symbol`, o cualquier `Expr`.

## Valor de retorno

| Funcion | Tipo de salida | Cuando |
|---------|---------------|--------|
| `exp(x)` | `E` | `x = 1` |
| `exp(x)` | `Integer(1)` | `x = 0` |
| `exp(x)` | `exp(Expr)` | Caso general no evaluable |
| `log(x)` | `Integer(0)` | `x = 1` |
| `log(x)` | `Integer(1)` | `x = E` |
| `log(x)` | `log(Expr)` | Caso general |
| `log(x, b)` | `log(x)/log(b)` | Internamente siempre se convierte a razon de logs naturales |

## Casos de uso

### Evaluacion exacta de casos especiales

```python
from sympy import exp, log, E, symbols

exp(0)          # 1
exp(1)          # E
log(1)          # 0
log(E)          # 1
log(E**3)       # 3
log(100, 10)    # 2    -> log base 10 de 100
```

### Inversa mutua — simplificacion con supuestos

```python
from sympy import exp, log, symbols

x = symbols("x")
xr = symbols("x", real=True)

exp(log(x))         # x                -> simplifica siempre
log(exp(x))         # x                -> simplifica (x complejo en general)
log(exp(xr))        # x                -> real, simplifica
```

> [!note] Comportamiento de `log(exp(x))`
> SymPy simplifica `log(exp(x))` a `x` para `x` simbolico general (asume complejo). Si el resultado sorprende, verificar los supuestos del simbolo.

### Expansion de logaritmos — expand_log

`log(x*y)` no simplifica automaticamente a `log(x) + log(y)`. Es necesario usar `expand_log` con `force=True` si los simbolos no tienen supuesto positivo.

```python
from sympy import log, symbols, expand_log

x, y = symbols("x y")
xp, yp = symbols("x y", positive=True)

log(x*y)                        # log(x*y)        -> no simplifica
expand_log(log(x*y))            # log(x*y)        -> sin supuestos tampoco
expand_log(log(xp*yp))          # log(x) + log(y) -> con positive=True si simplifica
expand_log(log(x*y), force=True)  # log(x) + log(y) -> forzando la expansion
log(x**3)                       # log(x**3)
expand_log(log(xp**3))          # 3*log(x)
```

### Derivada e integral de exp y log

```python
from sympy import exp, log, symbols, diff, integrate

x = symbols("x")
diff(exp(x), x)         # exp(x)
diff(log(x), x)         # 1/x
integrate(exp(x), x)    # exp(x)
integrate(1/x, x)       # log(x)    -> SymPy devuelve log (= ln)
```

### Conversion a base arbitraria

```python
from sympy import log, E, symbols

x = symbols("x", positive=True)
log(x, 2)           # log(x)/log(2)    -> base 2
log(x, 10)          # log(x)/log(10)   -> base 10
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `log(x*y)` no se expande | SymPy no puede asumir que `x`, `y > 0` | Usar `expand_log(..., force=True)` o declarar `positive=True` |
| `log` sin especificar base asumido base 10 | En matematica escolar `log` puede ser base 10 | En SymPy `log` siempre es ln; usar `log(x, 10)` para base 10 |
| `exp(x).evalf()` sin valor de `x` | `x` es un simbolo, no un numero | Sustituir primero: `exp(x).subs(x, 2).evalf()` |
| Esperar que `log(exp(x))` sea siempre `x` | Depende de supuestos de rama compleja | Para garantizarlo, declarar `x` real o usar `simplify` |

## Limitaciones

- `log` en SymPy es siempre el **logaritmo natural**; no existe `ln` como alias por defecto en el namespace de SymPy (aunque se puede importar como `from sympy import ln`).
- La expansion de `log(x*y)` no es valida en general para complejos (multivaluado); por eso no ocurre automaticamente.
- Para evaluacion numerica de alta precision: `log(2).evalf(50)`.

## Notas relacionadas

- [[sympy.sqrt]]
- [[sympy.trigonometricas]]
- [[sympy.functions/elementales/index | elementales]]
- [[sympy.functions/index | sympy.functions]]
