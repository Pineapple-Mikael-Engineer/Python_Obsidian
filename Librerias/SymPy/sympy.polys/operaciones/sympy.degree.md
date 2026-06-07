---
title: sympy.degree — grado de un polinomio
aliases:
  - degree
  - sympy.degree
  - grado de polinomio
tags:
  - sympy
  - api/funcion
  - polys/operaciones
lib: sympy
mod: sympy.polys
tipo: funcion
retorna: Integer
draft: false
---

# sympy.degree — grado de un polinomio

`degree(p, gen)` devuelve el **grado** de un polinomio: el mayor exponente de la variable indicada. Es una **consulta** de una sola cifra sobre la estructura del polinomio, util para decidir cuantas raices esperar, comprobar el grado de un cociente o validar entradas. En polinomios de una variable basta `degree(p)`; en multivariable hay que decir respecto a que variable con `gen=`.

> Convenios de borde: el grado de una **constante no nula** es `0`, y el grado del polinomio **cero** es `-oo` (menos infinito), el valor por convencion que hace consistentes las reglas del grado.

## Firma

```python
sympy.degree(
    f,           # Expr | Poly: el polinomio
    gen=0,       # Symbol | int: variable (o su indice) respecto a la cual medir
) -> Integer
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| Polinomio no nulo | `Integer` | Mayor exponente de `gen` |
| Constante no nula | `Integer` | `0` |
| Polinomio cero | `NegativeInfinity` | `-oo` |

```python
from sympy import symbols, degree
x = symbols("x")
degree(x**3 + 2*x + 1, x)     # 3
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Grado (una variable) | `degree(p)` o `degree(p, x)` |
| Grado respecto a una variable concreta | `degree(p, gen=x)` |

## Parametros en detalle

### `f` (el polinomio)

La expresion polinomica. Con una sola variable, `gen` es opcional.

```python
from sympy import symbols, degree
x = symbols("x")
degree(x**3 + 2*x + 1)        # 3
degree(x**3 + 2*x + 1, x)     # 3
```

### `gen` (variable en multivariable)

En polinomios de varias variables hay que indicar respecto a cual medir; cada variable da un grado distinto.

```python
from sympy import symbols, degree
x, y = symbols("x y")
degree(x**2*y**3 + x, x)        # 2   -> grado en x
degree(x**2*y**3 + x, gen=y)    # 3   -> grado en y
```

> Sin `gen` en una expresion multivariable, `degree` lanza un error pidiendo el generador: `degree(func, gen=x)`.

### Casos de borde

```python
from sympy import symbols, degree
x = symbols("x")
degree(5, x)     # 0     -> constante no nula
degree(0, x)     # -oo   -> polinomio cero (NegativeInfinity)
```

## Casos de uso

### Cuantas raices esperar

```python
from sympy import symbols, degree, real_roots
x = symbols("x")
p = x**3 - x
degree(p, x)            # 3   -> hasta 3 raices contando multiplicidad
len(real_roots(p))      # 3
```

### Verificar el grado tras una division

```python
from sympy import symbols, degree, div
x = symbols("x")
q, r = div(x**3 + 2*x + 1, x**2 + 1)
degree(r, x)     # 1   -> el resto siempre tiene grado menor que el divisor
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Error de generador requerido | Expresion multivariable sin `gen` | Pasar `gen=x` |
| Esperar `0` para el polinomio cero | El cero tiene grado `-oo` por convencion | Tratar `-oo` como caso especial |
| Pasar el indice y confundir variable | `gen=0` toma el primer generador interno | Usar la variable explicita `gen=x` |

## Limitaciones

- Mide el grado respecto a **una** variable a la vez; no da el grado total multivariable.
- Para el grado total existe `total_degree`; para el grado minimo, otras utilidades de `sympy.polys`.

## Notas relacionadas

- [[sympy.gcd]]
- [[sympy.div]]
- [[sympy.real_roots]]
- [[sympy.polys/operaciones/index | operaciones]]
