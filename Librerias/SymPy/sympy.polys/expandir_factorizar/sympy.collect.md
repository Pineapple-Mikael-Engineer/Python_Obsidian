---
title: sympy.collect — agrupar terminos por potencias de una variable
aliases:
  - collect
  - sympy.collect
  - agrupar
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

# sympy.collect — agrupar terminos por potencias de una variable

`collect(expr, x)` reordena una expresion **agrupando** sus terminos por las potencias de la variable `x`, factorizando el coeficiente de cada potencia. Convierte `a*x**2 + b*x**2 + a*x + x + 5` en `x**2*(a + b) + x*(a + 1) + 5`: deja la expresion como un polinomio en `x` con coeficientes (posiblemente simbolicos) recogidos por grado. No expande ni factoriza globalmente como [[sympy.expand]] o [[sympy.factor]]; **reordena** para ver la expresion como polinomio en una variable elegida, lo que facilita leer o extraer cada coeficiente.

> A diferencia de los pares inversos (`expand`/`factor`, `apart`/`together`), `collect` no tiene inversa: es un **reordenador**. Su trabajo previo habitual es `expand`, para que todos los terminos esten sueltos antes de agruparlos.

## Firma

```python
sympy.collect(
    expr,                # Expr: expresion a agrupar (conviene expandirla antes)
    syms,                # Symbol | lista: variable(s) por cuyas potencias agrupar
    func=None,           # callable: aplicar a cada coeficiente recogido
    evaluate=True,       # bool: False -> devuelve dict {potencia: coeficiente}
    exact=False,         # bool: emparejado exacto de potencias
    ...
) -> Expr
```

## Valor de retorno

| Tipo | Forma | Significado |
|------|-------|-------------|
| `Expr` | polinomio en `x` | La expresion reescrita con coeficientes agrupados por potencia de `x` |
| `dict` | `{potencia: coef}` | Solo con `evaluate=False`: mapea cada potencia de `x` a su coeficiente |

```python
from sympy import symbols, collect
x, a, b = symbols("x a b")
collect(a*x**2 + b*x**2 + a*x + x + 5, x)   # x**2*(a + b) + x*(a + 1) + 5
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Agrupar por potencias de `x` | `collect(expr, x)` |
| Agrupar por varias variables | `collect(expr, [x, y])` |
| Aplicar algo a cada coeficiente | `collect(expr, x, func=factor)` |
| Obtener dict potencia->coef | `collect(expr, x, evaluate=False)` |

## Parametros en detalle

### `expr` (obligatorio)

La expresion a reordenar. Para que `collect` agrupe bien conviene que los terminos esten **desarrollados** (sin parentesis sin distribuir); de lo contrario puede no reconocer terminos equivalentes.

```python
from sympy import symbols, collect
x, a, b = symbols("x a b")
collect(a*x**2 + b*x**2 + a*x + x + 5, x)   # x**2*(a + b) + x*(a + 1) + 5
```

### `syms` (obligatorio)

La variable (o lista de variables) por cuyas potencias agrupar. Es la decision clave: el **mismo** polinomio se ve distinto segun la variable elegida.

```python
from sympy import symbols, collect
x = symbols("x")
collect(a*x + a, a)        # a*(x + 1)   -> agrupado por a, no por x
```

### `func`

Funcion que se aplica a **cada coeficiente** recogido, util para factorizar o simplificar los coeficientes sobre la marcha (p. ej. `func=factor`).

### `evaluate=False`

Devuelve un **diccionario** `{potencia_de_x: coeficiente}` en vez de la expresion reescrita, comodo para acceder programaticamente a cada coeficiente.

```python
from sympy import symbols, collect
x, a, b = symbols("x a b")
collect(a*x**2 + b*x**2 + x, x, evaluate=False)   # {x: 1, x**2: a + b}
```

## Casos de uso

### Ordenar un polinomio en una variable

Tras manipular una expresion con parametros, `collect` la deja como polinomio limpio en la variable de interes, lista para leer.

```python
from sympy import symbols, collect, expand
x, k = symbols("x k")
e = expand((x + k)*(x - 1))     # k*x - k + x**2 - x
collect(e, x)                   # x**2 + x*(k - 1) - k
```

### Extraer el coeficiente de una potencia concreta

Una vez agrupado, `coeff` lee el coeficiente de cada grado de forma fiable.

```python
from sympy import symbols, collect
x, a, b = symbols("x a b")
collect(a*x**2 + b*x**2 + x, x).coeff(x, 2)   # a + b
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `collect` no agrupa lo esperado | La expresion no estaba desarrollada | Aplicar [[sympy.expand]] antes de `collect` |
| Agrupar por la variable equivocada | El segundo argumento define el criterio | Elegir bien `syms` (la variable de interes) |
| Esperar factorizacion completa | `collect` solo agrupa por potencias, no factoriza | Usar [[sympy.factor]] si se busca el producto de irreducibles |
| Querer un coeficiente y recibir la expresion | Forma por defecto reescribe, no devuelve dict | Usar `evaluate=False` o `.coeff(x, n)` |

## Notas relacionadas

- [[sympy.expand]]
- [[sympy.factor]]
- [[sympy.together]]
- [[sympy.polys/expandir_factorizar/index | expandir_factorizar]]
