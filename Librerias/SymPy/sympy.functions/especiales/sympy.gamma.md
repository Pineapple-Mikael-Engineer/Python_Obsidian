---
title: sympy.gamma — funcion gamma simbolica
aliases: [gamma, funcion gamma]
tags: [sympy, api/funcion, functions/especiales]
lib: sympy
mod: sympy.functions
tipo: funcion
retorna: Expr
requiere: [Symbol, Rational]
draft: false
---

# sympy.gamma — funcion gamma simbolica

`gamma(x)` evalua la **funcion gamma** de Euler, la generalizacion del factorial a los numeros reales y complejos. Para enteros positivos `n`, cumple `gamma(n) == (n-1)!`; para semienteros como `Rational(1,2)`, devuelve expresiones exactas en terminos de `sqrt(pi)`. Cuando el argumento es simbolico, `gamma` permanece **sin evaluar** como objeto `Expr`, listo para simplificar o reescribir. Es la funcion de referencia en probabilidad (distribucion Gamma), integrales de Euler, series de Taylor y funciones hipergeometricas.

## Firma

```python
sympy.gamma(x) -> Expr
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `x` | `Expr \| Number \| Rational` | Argumento de la funcion gamma |

## Valor de retorno

| Tipo | Cuando ocurre |
|------|---------------|
| `Integer` | `x` es un entero positivo: devuelve `(x-1)!` exacto |
| `Expr` con `sqrt(pi)` | `x` es un semientero positivo: forma exacta en pi |
| `gamma(x)` sin evaluar | `x` es simbolico o un valor no simplificable |

```python
from sympy import symbols, gamma, Rational, sqrt, pi

x = symbols("x")
gamma(5)               # 24           (= 4!)
gamma(Rational(1, 2))  # sqrt(pi)
gamma(Rational(3, 2))  # sqrt(pi)/2
gamma(Rational(5, 2))  # 3*sqrt(pi)/4
gamma(x + 1)           # gamma(x + 1) -> sin evaluar
```

## Formas basicas de llamada

| Objetivo | Llamada | Resultado |
|----------|---------|-----------|
| Factorial de entero via gamma | `gamma(n + 1)` | `factorial(n)` si `n` entero |
| Valor en semientero | `gamma(Rational(1, 2))` | `sqrt(pi)` |
| Reescribir como factorial | `gamma(x + 1).rewrite(factorial)` | `factorial(x)` |
| Evaluar numericamente | `gamma(x).evalf(subs={x: 0.5})` | `1.77245385090552` |

## Casos de uso

### Relacion con factorial

`gamma(n+1) == factorial(n)` para enteros no negativos. Son la misma funcion en dominios distintos.

```python
from sympy import symbols, gamma, factorial, Rational

n = symbols("n", positive=True, integer=True)
gamma(5)                          # 24    (= 4!)
factorial(4)                      # 24
gamma(n + 1).rewrite(factorial)   # factorial(n)
```

### Semienteros y sqrt(pi)

```python
from sympy import Rational, gamma

gamma(Rational(1, 2))   # sqrt(pi)
gamma(Rational(3, 2))   # sqrt(pi)/2
gamma(Rational(5, 2))   # 3*sqrt(pi)/4
```

### Integral de Euler (segunda clase)

La funcion gamma es la integral `int_0^inf t^(x-1) * exp(-t) dt`. SymPy puede trabajar con ella simbolicamente en integrales especiales.

```python
from sympy import symbols, gamma, integrate, exp, oo

t, x = symbols("t x", positive=True)
# Propiedad: gamma(x) = integral de Euler (referencia analitica)
# Para valores concretos:
gamma(4)   # 6   (= 3!)
gamma(1)   # 1
gamma(2)   # 1
gamma(3)   # 2
```

### Evaluacion numerica

```python
from sympy import gamma, Rational

gamma(Rational(1, 2)).evalf()   # 1.77245385090552  (= sqrt(pi))
gamma(Rational(3, 2)).evalf()   # 0.886226925452758
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `gamma(0)` o `gamma(-n)` | La gamma tiene polos en 0 y enteros negativos | Verificar dominio antes de evaluar |
| Confundir `gamma(n)` con `factorial(n)` | `gamma(n) = (n-1)!`, no `n!` | Usar `gamma(n+1)` para emular `factorial(n)` |
| Esperar simplificacion automatica | `gamma(x+1)` no se reduce automaticamente a `x*gamma(x)` | Usar `.rewrite(factorial)` o `simplify` |

## Limitaciones

- Los **polos** de `gamma` estan en `0, -1, -2, ...`: `gamma(0)` produce `zoo` (complejo infinito).
- La **relacion de recurrencia** `gamma(x+1) = x * gamma(x)` no se aplica automaticamente para `x` simbolico; hay que llamar a `simplify` o `gammasimp`.
- Para integraciones que generan factores gamma, SymPy puede devolver expresiones con `meijerg`; `simplify` suele resolverlas.

## Notas relacionadas

- [[sympy.factorial_binomial]]
- [[sympy.functions/especiales/index | especiales]]
- [[sympy.functions/index | sympy.functions]]
