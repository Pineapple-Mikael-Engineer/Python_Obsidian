---
title: sympy.hiperbolicas — funciones hiperbolicas simbolicas
aliases:
  - sinh
  - cosh
  - tanh
  - funciones hiperbolicas
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

# sympy.hiperbolicas — funciones hiperbolicas simbolicas

SymPy incluye las funciones hiperbolicas directas e inversas como objetos simbolicos: `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`. Son las analogas a las trigonometricas pero definidas sobre la **hiperbola unitaria** `x^2 - y^2 = 1` en lugar del circulo unitario. Se relacionan con la exponencial natural: `sinh(x) = (e^x - e^(-x))/2`, `cosh(x) = (e^x + e^(-x))/2`. Esta conexion se expone directamente con `rewrite(exp)`.

La identidad fundamental es `cosh(x)**2 - sinh(x)**2 = 1`, analoga a la identidad pitagorica trigonometrica. Para simplificarla se necesita llamar a `simplify`.

## Firmas

```python
sympy.sinh(x)    -> Expr   # seno hiperbolico
sympy.cosh(x)    -> Expr   # coseno hiperbolico
sympy.tanh(x)    -> Expr   # tangente hiperbolica
sympy.asinh(x)   -> Expr   # arcoseno hiperbolico
sympy.acosh(x)   -> Expr   # arcocoseno hiperbolico
sympy.atanh(x)   -> Expr   # arcotangente hiperbolica
```

## Valor de retorno

Todas devuelven `Expr`. En puntos especiales evaluan a numeros exactos; en caso general devuelven la funcion sin evaluar.

| Llamada | Resultado |
|---------|-----------|
| `sinh(0)` | `0` |
| `cosh(0)` | `1` |
| `tanh(0)` | `0` |
| `sinh(1)` | `sinh(1)` — sin forma cerrada racional |
| `asinh(0)` | `0` |
| `acosh(1)` | `0` |

## Casos de uso

### Evaluacion en puntos especiales

```python
from sympy import sinh, cosh, tanh, asinh, acosh, atanh

sinh(0)         # 0
cosh(0)         # 1
tanh(0)         # 0
asinh(0)        # 0
acosh(1)        # 0
atanh(0)        # 0
```

### Identidad fundamental

```python
from sympy import sinh, cosh, symbols, simplify

x = symbols("x")
expr = cosh(x)**2 - sinh(x)**2
simplify(expr)          # 1    -> identidad cosh^2 - sinh^2 = 1
```

### Conversion a exponencial con rewrite

```python
from sympy import sinh, cosh, tanh, symbols, exp

x = symbols("x")
sinh(x).rewrite(exp)    # exp(x)/2 - exp(-x)/2
cosh(x).rewrite(exp)    # exp(x)/2 + exp(-x)/2
tanh(x).rewrite(exp)    # (exp(2*x) - 1)/(exp(2*x) + 1)
```

### Derivadas de funciones hiperbolicas

```python
from sympy import sinh, cosh, tanh, symbols, diff

x = symbols("x")
diff(sinh(x), x)    # cosh(x)
diff(cosh(x), x)    # sinh(x)
diff(tanh(x), x)    # 1 - tanh(x)**2    -> equivalente a sech^2(x)
```

### Funciones inversas

```python
from sympy import asinh, acosh, atanh, Rational

asinh(0)                    # 0
asinh(1)                    # asinh(1)   -> sin forma cerrada simple
acosh(1)                    # 0
atanh(Rational(1, 2))       # atanh(1/2) -> sin forma cerrada simple
```

### Evaluacion numerica

```python
from sympy import sinh, cosh

sinh(1).evalf()     # 1.17520119364380
cosh(1).evalf()     # 1.54308063481524
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `cosh(x)**2 - sinh(x)**2` no da `1` | La simplificacion no es automatica | Aplicar `simplify(expr)` |
| Confundir `sinh` con `sin` | Nombres similares, comportamiento distinto | `sinh` crece sin acotarse; `sin` oscila en `[-1,1]` |
| `acosh(x)` para `x < 1` da resultado complejo | El dominio real de `acosh` es `[1, +inf)` | Verificar el dominio o declarar supuestos |
| Esperar que `asinh(sinh(x))` sea `x` | Solo para `x` en el rango principal | Usar `simplify` o declarar supuestos |

## Limitaciones

- La simplificacion de `cosh(x)**2 - sinh(x)**2` a `1` requiere `simplify`; no ocurre de forma automatica.
- No existe una version "en grados" de las funciones hiperbolicas en SymPy.
- Para dominios complejos, las funciones inversas (`acosh`, `atanh`) pueden devolver partes imaginarias; verificar supuestos si se trabaja en reales.

## Notas relacionadas

- [[sympy.trigonometricas]]
- [[sympy.exp_log]]
- [[sympy.functions/elementales/index | elementales]]
- [[sympy.functions/index | sympy.functions]]
