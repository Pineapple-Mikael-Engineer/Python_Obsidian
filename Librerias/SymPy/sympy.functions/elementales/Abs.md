---
title: Abs — valor absoluto simbolico
aliases:
  - Abs
  - valor absoluto
tags:
  - sympy
  - api/clase
  - functions/elementales
lib: sympy
mod: sympy.functions
tipo: clase
retorna: Expr
requiere:
  - Symbol
  - concepto_symbols_assumptions
draft: false
---

# Abs — valor absoluto simbolico

`Abs(x)` es la clase de SymPy que representa el **valor absoluto** de una expresion simbolica. No es una funcion pura: es una subclase de `Expr` que SymPy reconoce y puede simplificar usando los **supuestos** del simbolo. Cuando `x` no tiene supuestos, `Abs(x)` permanece sin evaluar (lo que es correcto, pues no se conoce el signo). Con `positive=True`, SymPy sabe que `x > 0` y simplifica `Abs(x)` a `x`.

Diferencia clave con el built-in `abs()` de Python: `abs(expr)` llama a `Abs` internamente sobre objetos SymPy, por lo que el resultado es equivalente, pero se recomienda importar y usar `Abs` explicitamente para dejar clara la intencion simbolica.

## Firma

```python
sympy.Abs(x) -> Expr
```

`x` puede ser un numero, un `Symbol`, o cualquier `Expr`.

## Valor de retorno

| Caso | Resultado | Ejemplo |
|------|-----------|---------|
| `x` es un numero negativo | `Integer` positivo | `Abs(-3)` → `3` |
| `x` es un numero positivo | El mismo numero | `Abs(5)` → `5` |
| `x` simbolo sin supuestos | `Abs(x)` sin evaluar | `Abs(x)` → `Abs(x)` |
| `x` con `positive=True` | `x` directamente | `Abs(xp)` → `xp` |
| `x` con `negative=True` | `-x` | `Abs(xn)` → `-xn` |

## Casos de uso

### Evaluacion sobre numeros

```python
from sympy import Abs

Abs(-3)         # 3
Abs(5)          # 5
Abs(0)          # 0
Abs(-Rational(3, 4))   # 3/4
```

### Comportamiento con simbolos y supuestos

```python
from sympy import Abs, symbols

x  = symbols("x")
xp = symbols("x", positive=True)
xn = symbols("x", negative=True)
xr = symbols("x", real=True)

Abs(x)          # Abs(x)    -> sin supuestos no simplifica
Abs(xp)         # x         -> positive=True: el valor absoluto es x mismo
Abs(xn)         # -x        -> negative=True: el valor absoluto es -x
Abs(xr)         # Abs(x)    -> real pero sin signo conocido, queda sin evaluar
```

### Rewrite a Piecewise

```python
from sympy import Abs, symbols, Piecewise

x = symbols("x")
Abs(x).rewrite(Piecewise)
# Piecewise((x, x >= 0), (-x, True))
```

Esta forma es util para integrar por tramos o analizar la funcion segun el signo de `x`.

### Derivada de Abs

```python
from sympy import Abs, symbols, diff

x = symbols("x", real=True)
diff(Abs(x), x)     # sign(x)    -> derivada es la funcion signo
```

### Comparacion con abs() de Python

```python
from sympy import Abs, symbols

x = symbols("x")
abs(x)          # Abs(x)   -> Python llama a __abs__ que delega en Abs
Abs(x)          # Abs(x)   -> forma explicita recomendada
```

Ambas dan el mismo resultado sobre `Expr` de SymPy. Se prefiere `Abs` para claridad.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `Abs(x)` no simplifica | El simbolo no tiene supuestos de signo | Declarar `positive=True` o `negative=True` |
| Confundir con `abs()` de Python sobre floats | `abs(-3.0)` es el built-in de Python, no SymPy | Sobre `Expr` el resultado es el mismo; sobre floats Python devuelve float, no `Expr` |
| Esperar que `Abs(-x)` de `x` | Sin supuestos, SymPy no sabe si `-x` es positivo | Declarar supuestos en el simbolo original |
| `Abs(x**2)` no se simplifica | `x**2 >= 0` pero SymPy no siempre lo detecta | Usar `simplify` o declarar supuestos |

## Limitaciones

- `Abs(x)` no es diferenciable en `x = 0`; `diff(Abs(x), x)` devuelve `sign(x)`, que es la derivada para `x != 0`.
- Para comparaciones numericas, `Abs` devuelve una `Expr`; convertir con `.evalf()` si se necesita un `float`.
- La simplificacion de `Abs(x**2)` a `x**2` requiere saber que `x**2 >= 0`, lo cual SymPy no siempre infiere automaticamente sin supuestos explicitos.

## Notas relacionadas

- [[sympy.sqrt]]
- [[sympy.trigonometricas]]
- [[sympy.functions/elementales/index | elementales]]
- [[sympy.functions/index | sympy.functions]]
