---
title: simbolos y supuestos — Symbol y las assumptions que cambian el resultado
aliases:
  - simbolos y supuestos
  - assumptions
  - symbol real positive
tags:
  - sympy
  - concepto
  - fundamentos
lib: sympy
mod: sympy
tipo: concepto
requiere:
  - concepto_expr_arbol
draft: false
---

# simbolos y supuestos — Symbol y las assumptions que cambian el resultado

## Definicion fundamental

Un **`Symbol`** es una incognita matematica: un nombre sobre el que se construyen las expresiones, creado con `symbols(...)`. Por defecto un simbolo es **lo mas general posible** (podria ser complejo), y eso limita lo que SymPy puede simplificar. Los **supuestos** (*assumptions*) son banderas que declaran propiedades del simbolo —real, positivo, entero…— y **cambian el resultado** de simplificaciones, raices y resoluciones.

```python
from sympy import symbols, sqrt

x = symbols("x")                       # general (posiblemente complejo)
sqrt(x**2)                             # sqrt(x**2)   -> no puede simplificar
p = symbols("p", positive=True)        # supuesto: positivo
sqrt(p**2)                             # p            -> ahora si
```

## Por que el nombre de la variable no basta

`x = symbols("x")` crea un simbolo **llamado** "x"; la variable Python `x` es solo una etiqueta. El nombre es lo que se imprime; los **supuestos** son los que rigen el algebra. Dos simbolos con el mismo nombre pero distintos supuestos son **objetos distintos**.

```python
a = symbols("a")
b = symbols("a", positive=True)
a == b          # False   -> mismo nombre, distintos supuestos
```

> [!regla]
> Declara los supuestos que **son ciertos en tu problema** (una longitud es `positive`, un indice `integer`, una variable fisica `real`). Cuantos mas supuestos correctos, mas puede simplificar y resolver SymPy. Declarar supuestos **falsos** da resultados incorrectos.

## Supuestos mas usados

| Supuesto | Significado | Efecto tipico |
|----------|-------------|---------------|
| `real=True` | numero real | habilita comparaciones, evita ramas complejas |
| `positive=True` | real > 0 | `sqrt(x**2) -> x`, `log(exp(x)) -> x` |
| `negative=True` | real < 0 | signo conocido en valores absolutos |
| `integer=True` | entero | `(-1)**(2*n) -> 1`, indices de sumatorios |
| `nonzero=True` | distinto de cero | permite dividir sin ambiguedad |
| `complex=True` | complejo (por defecto) | el mas general |

```python
from sympy import symbols, cos, pi
n = symbols("n", integer=True)
cos(2*pi*n)        # 1   -> usa que n es entero
```

## Consultar lo que SymPy sabe

Cada simbolo (y cada expresion) expone los supuestos como atributos `.is_*`, que devuelven `True`, `False` o **`None`** (desconocido).

```python
p = symbols("p", positive=True)
p.is_positive      # True
p.is_real          # True    -> positivo implica real
p.is_integer       # None    -> no se sabe
x = symbols("x")
x.is_positive      # None    -> sin supuestos, desconocido
```

El **`None`** es clave: SymPy razona con logica de tres valores. "No se sabe" no es "falso".

## Caso que mas falla: el supuesto olvidado

```python
from sympy import symbols, sqrt, simplify
x = symbols("x")
simplify(sqrt(x**2))           # sqrt(x**2)   -> sin supuesto no simplifica
# correcto: sqrt(x**2) = |x|; solo es x si x >= 0
a = symbols("a", positive=True)
simplify(sqrt(a**2))           # a
```

## Casos que confunden

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| una simplificacion "obvia" no ocurre | falta el supuesto que la habilita | crear el simbolo con `real`/`positive`/`integer` |
| dos simbolos "iguales" no son iguales | distintos supuestos -> distintos objetos | crear el simbolo una vez y reutilizarlo |
| `x.is_positive` es `None`, esperaba `False` | logica de 3 valores: None = desconocido | declarar el supuesto; no asumir |

## Relacion con otros conceptos

- [[concepto_expr_arbol]]
- [[concepto_simplificacion_automatica]]
- [[concepto_simbolico_vs_numerico]]
