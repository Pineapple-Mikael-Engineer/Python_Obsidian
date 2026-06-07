---
title: sympy.expand — distribuir productos y potencias de una expresion
aliases:
  - expand
  - sympy.expand
  - distribuir
tags:
  - sympy
  - api/funcion
  - polys/expandir_factorizar
lib: sympy
mod: sympy
tipo: funcion
retorna: Expr
requiere:
  - Symbol
draft: false
---

# sympy.expand — distribuir productos y potencias de una expresion

`expand(expr)` reescribe una expresion **distribuyendo** productos sobre sumas y desarrollando potencias enteras, hasta dejar un polinomio (o suma de terminos) plano. Convierte `(x + 1)**2` en `x**2 + 2*x + 1`: rompe parentesis y agrupa. Es la operacion **inversa** de [[sympy.factor]] y la forma canonica para comparar dos expresiones polinomicas o para extraer coeficientes termino a termino. Por defecto expande solo la parte algebraica; mediante banderas (`trig=True`, `log=True`, `power_exp=True`...) extiende el desarrollo a funciones trigonometricas, logaritmos o exponenciales.

> `expand` produce la forma **desarrollada** y `factor` la forma **factorizada**; aplicadas en cadena se cancelan: `factor(expand(p)) == p` para un polinomio factorizable.

## Firma

```python
sympy.expand(
    expr,                # Expr: expresion a desarrollar
    deep=True,           # bool: expandir tambien subexpresiones anidadas
    mul=True,            # bool: distribuir multiplicaciones sobre sumas
    power_exp=True,      # bool: expandir exponentes (e^(a+b) -> e^a*e^b)
    power_base=True,     # bool: expandir bases ((x*y)^n -> x^n*y^n) con supuestos
    log=False,           # bool: expandir logaritmos (log(x*y) -> log(x)+log(y))
    trig=False,          # bool: expandir funciones trigonometricas
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | suma de terminos | La expresion desarrollada (parentesis distribuidos, potencias resueltas) |

Si nada se puede desarrollar, devuelve la expresion **sin cambios** (no falla).

```python
from sympy import symbols, expand
x = symbols("x")
expand((x + 1)**2)        # x**2 + 2*x + 1
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Desarrollar potencia/producto | `expand((x + 1)**2)` |
| Multiplicar dos factores | `expand((x + 1)*(x - 1))` |
| Expandir trigonometricas | `expand(sin(x + y), trig=True)` |
| Expandir logaritmos | `expand(log(x*y), log=True, force=True)` |
| Solo distribuir, no potencias | `expand(expr, power_exp=False)` |

## Parametros en detalle

### `expr` (obligatorio)

La expresion a desarrollar. Distribuye productos sobre sumas y desarrolla las potencias de exponente entero positivo.

```python
from sympy import symbols, expand
x = symbols("x")
expand((x + 1)**2)        # x**2 + 2*x + 1
expand((x + 1)*(x - 1))   # x**2 - 1        -> diferencia de cuadrados
expand((x + 1)**3)        # x**3 + 3*x**2 + 3*x + 1
```

Funciona igual con varias variables:

```python
from sympy import symbols, expand
x, y = symbols("x y")
expand((x + y)**2)        # x**2 + 2*x*y + y**2
```

### `trig=True`

Activa el desarrollo de **identidades trigonometricas** (sumas de angulos, multiplos). Sin esta bandera, `expand` deja `sin(x + y)` intacto.

```python
from sympy import symbols, expand, sin
x, y = symbols("x y")
expand(sin(x + y), trig=True)   # sin(x)*cos(y) + sin(y)*cos(x)
```

### `log=True`

Expande logaritmos de productos y potencias (`log(x*y) -> log(x) + log(y)`). Requiere supuestos de positividad sobre los simbolos, o `force=True` para forzarlo. Existe el atajo `expand_log` equivalente a este modo.

```python
from sympy import symbols, expand
x, y = symbols("x y")
expand(log(x*y), log=True, force=True)   # log(x) + log(y)
```

### `deep`, `mul`, `power_exp`

Banderas de grano fino para limitar el desarrollo: `mul=False` no distribuye productos, `power_exp=False` no separa exponenciales, `deep=False` solo expande el nivel superior. Por defecto todas las algebraicas estan activas.

## Casos de uso

### Comparar dos expresiones polinomicas

Dos polinomios son iguales si su forma **desarrollada** coincide; `expand` da la forma canonica para compararlos.

```python
from sympy import symbols, expand
x = symbols("x")
expand((x + 2)**2) == expand(x**2 + 4*x + 4)   # True
```

### Preparar una expresion para extraer coeficientes

Tras desarrollar, cada termino queda explicito y se puede leer el coeficiente de cada potencia (a menudo combinado con [[sympy.collect]]).

```python
from sympy import symbols, expand
x = symbols("x")
p = expand((2*x + 1)*(x - 3))   # 2*x**2 - 5*x - 3
p.coeff(x, 1)                   # -5
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `expand(sin(x+y))` no cambia nada | Sin `trig=True` no toca trigonometricas | Pasar `expand(..., trig=True)` |
| `expand(log(x*y))` no separa el log | Falta `log=True` y/o supuestos de signo | `expand(..., log=True, force=True)` o `symbols(..., positive=True)` |
| Esperar que factorice | `expand` desarrolla, no factoriza | Usar [[sympy.factor]] |
| Expresion enorme tras expandir | Desarrollar potencias altas explota terminos | Mantenerla factorizada con [[sympy.factor]] hasta el final |

## Notas relacionadas

- [[sympy.factor]]
- [[sympy.collect]]
- [[sympy.together]]
- [[sympy.polys/expandir_factorizar/index | expandir_factorizar]]
