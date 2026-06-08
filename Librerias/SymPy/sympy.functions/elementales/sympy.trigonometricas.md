---
title: sympy.trigonometricas — funciones trigonometricas simbolicas
aliases:
  - sin
  - cos
  - tan
  - atan2
  - funciones trigonometricas
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

# sympy.trigonometricas — funciones trigonometricas simbolicas

SymPy provee las funciones trigonometricas directas e inversas como objetos simbolicos exactos: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`. Evaluan **exactamente** en angulos especiales (multiplos de `pi/6`, `pi/4`, `pi/3`, `pi/2`) y devuelven fracciones, raices o cero cuando el valor es conocido. En cualquier otro caso devuelven la expresion sin evaluar, lista para derivar, integrar o simplificar.

Los argumentos siempre se expresan en **radianes**. Para simplificar identidades trigonometricas entre `sin`, `cos`, `tan` y sus potencias, la herramienta principal es `trigsimp`.

## Firmas

```python
sympy.sin(x)           -> Expr
sympy.cos(x)           -> Expr
sympy.tan(x)           -> Expr
sympy.asin(x)          -> Expr   # arcoseno,   rango [-pi/2, pi/2]
sympy.acos(x)          -> Expr   # arcocoseno, rango [0, pi]
sympy.atan(x)          -> Expr   # arcotangente, rango (-pi/2, pi/2)
sympy.atan2(y, x)      -> Expr   # angulo en el plano, rango (-pi, pi]
```

## Valor de retorno

Todas devuelven `Expr`. Pueden ser un numero racional, una expresion con `sqrt`, o la funcion aplicada sin evaluar.

| Llamada | Resultado |
|---------|-----------|
| `sin(pi/6)` | `1/2` |
| `cos(pi/4)` | `sqrt(2)/2` |
| `cos(pi)` | `-1` |
| `tan(pi/4)` | `1` |
| `sin(pi/2)` | `1` |
| `asin(Rational(1,2))` | `pi/6` |
| `atan(1)` | `pi/4` |
| `atan2(1, 1)` | `pi/4` |
| `sin(x)` (x simbolo) | `sin(x)` sin evaluar |

## Casos de uso

### Evaluacion exacta en angulos especiales

```python
from sympy import sin, cos, tan, pi, Rational

sin(pi/6)           # 1/2
sin(pi/4)           # sqrt(2)/2
cos(pi/3)           # 1/2
cos(pi)             # -1
tan(pi/4)           # 1
tan(pi/3)           # sqrt(3)
sin(0)              # 0
cos(0)              # 1
```

### Funciones inversas

```python
from sympy import asin, acos, atan, atan2, Rational, pi

asin(Rational(1, 2))    # pi/6
acos(Rational(1, 2))    # pi/3
atan(1)                 # pi/4
atan2(1, 1)             # pi/4    -> angulo de (1,1) respecto al eje x
atan2(1, -1)            # 3*pi/4  -> segundo cuadrante
atan2(-1, 0)            # -pi/2   -> abajo del eje x
```

> La funcion `atan2(y, x)` calcula el angulo del vector `(x, y)` en el plano con rango `(-pi, pi]`, a diferencia de `atan(y/x)` que pierde informacion del cuadrante y falla en `x=0`.

### Simplificacion de identidades con trigsimp

```python
from sympy import sin, cos, symbols, trigsimp

x = symbols("x")
expr = sin(x)**2 + cos(x)**2
trigsimp(expr)          # 1    -> identidad pitagorica

expr2 = sin(2*x) - 2*sin(x)*cos(x)
trigsimp(expr2)         # 0    -> sin(2x) = 2*sin(x)*cos(x)
```

### Derivada de funciones trigonometricas

```python
from sympy import sin, cos, tan, symbols, diff

x = symbols("x")
diff(sin(x), x)     # cos(x)
diff(cos(x), x)     # -sin(x)
diff(tan(x), x)     # tan(x)**2 + 1    -> equivalente a sec^2(x)
```

### Expresion no evaluada y sustitucion

```python
from sympy import sin, symbols

x = symbols("x")
expr = sin(x) + sin(x)**2
expr.subs(x, 0)         # 0
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Pasar grados en vez de radianes | `sin(90)` no da `1` | Convertir: `sin(pi/2)` o `sin(rad(90))` |
| `atan(y/x)` en vez de `atan2(y, x)` | Pierde cuadrante y falla si `x=0` | Usar `atan2(y, x)` para angulos en el plano |
| `sin(x)**2 + cos(x)**2` no da `1` | Auto-simplificacion no ocurre aqui | Aplicar `trigsimp(expr)` |
| Esperar que `asin(sin(x))` sea `x` | Solo vale para `x` en el rango `[-pi/2, pi/2]` | Declarar supuestos o usar `simplify` |

## Limitaciones

- SymPy no simplifica `sin(x)**2 + cos(x)**2` a `1` de forma automatica; es necesario llamar a `trigsimp` o `simplify`.
- `asin(sin(x))` solo simplifica a `x` si SymPy puede verificar que `x` esta en el rango principal; en general puede devolver la expresion sin evaluar.
- Para angulos en grados, no hay una funcion `sind` nativa; convertir manualmente multiplicando por `pi/180`.

## Notas relacionadas

- [[sympy.hiperbolicas]]
- [[sympy.exp_log]]
- [[sympy.functions/elementales/index | elementales]]
- [[sympy.functions/index | sympy.functions]]
