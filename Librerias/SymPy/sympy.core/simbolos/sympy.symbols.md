---
title: sympy.symbols — crear uno o varios simbolos desde una cadena
aliases:
  - symbols
  - sympy.symbols
  - crear simbolos
tags:
  - sympy
  - api/funcion
  - core/simbolos
lib: sympy
mod: sympy
tipo: funcion
retorna: Symbol | tuple
requiere:
  - Symbol
  - concepto_symbols_assumptions
draft: false
---

# sympy.symbols — crear uno o varios simbolos desde una cadena

Es la forma **principal** de crear simbolos en SymPy. Recibe una **cadena** con los nombres y devuelve un [[Symbol]] (si pide uno solo) o una **tupla** de simbolos (si pide varios). Sobre esa cadena interpreta separadores (espacios y comas), **rangos** compactos (`x:5`, `a:d`) y **grupos**; ademas reparte a todos los simbolos creados los **supuestos** (*assumptions*) que se pasen por palabra clave. Es preferible a construir cada `Symbol("...")` a mano porque crea muchos de una vez y asigna nombres consistentes.

> Distincion clave: `symbols` es la **fabrica**; el objeto que devuelve es la clase [[Symbol]]. Para un unico simbolo ambos sirven, pero `symbols` es el camino idiomatico y el unico comodo para crear varios a la vez.

## Firma

```python
sympy.symbols(
    names,          # str | secuencia: nombres separados por espacio/coma, con rangos y grupos
    *,
    cls=Symbol,     # clase a instanciar (p.ej. Function, Wild)
    **assumptions,  # supuestos aplicados a TODOS los simbolos: real, positive, integer, ...
) -> Symbol | tuple
```

## Valor de retorno

| Entrada | Tipo devuelto | Significado |
|---------|---------------|-------------|
| Un solo nombre (`"x"`) | `Symbol` | El simbolo suelto, listo para usar |
| Varios nombres (`"x y z"`) | `tuple` de `Symbol` | Una tupla para desempaquetar |
| Un rango (`"x:5"`) | `tuple` de `Symbol` | Tupla con los simbolos generados |
| Un grupo entre parentesis | `tuple` de `tuple` | Tuplas anidadas, una por grupo |

```python
from sympy import symbols
x = symbols("x")            # Symbol  -> x
x, y, z = symbols("x y z")  # tuple   -> desempaquetado tipico
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Un simbolo | `symbols("x")` |
| Varios simbolos | `symbols("x y z")` |
| Separar con comas | `symbols("x, y, z")` |
| Rango numerico `x0..x4` | `symbols("x:5")` |
| Rango alfabetico `a..d` | `symbols("a:d")` |
| Varios grupos a la vez | `symbols("x:3 y:2")` |
| Con supuesto | `symbols("x", positive=True)` |

## Parametros en detalle

### `names` (obligatorio)

Cadena con los nombres. Los separadores son **espacios o comas**; ambos valen y se pueden mezclar.

```python
from sympy import symbols
symbols("x y z")     # (x, y, z)
symbols("x, y, z")   # (x, y, z)   -> identico
symbols("a b")       # (a, b)
```

Pedir **un solo** nombre devuelve el `Symbol` suelto, no una tupla de un elemento. Para forzar tupla de uno, añade una coma: `symbols("x,")`.

```python
symbols("x")    # x        -> Symbol
symbols("x,")   # (x,)     -> tuple de 1
```

#### Rangos numericos `nombre:N`

`x:5` genera `x0, x1, x2, x3, x4` (de 0 a N-1). Tambien admite extremos: `x1:4` da `x1, x2, x3`.

```python
symbols("x:5")     # (x0, x1, x2, x3, x4)
symbols("x1:4")    # (x1, x2, x3)
```

#### Rangos alfabeticos `a:letra`

`a:d` genera `a, b, c, d` (rango de letras, extremos incluidos).

```python
symbols("a:d")     # (a, b, c, d)
```

#### Varios grupos

Cada token separado produce su bloque; se pueden combinar nombres sueltos y rangos en la misma llamada.

```python
symbols("x:3 y:2")     # (x0, x1, x2, y0, y1)
symbols("p q r:3")     # (p, q, r0, r1, r2)
```

Con **parentesis** se agrupa en tuplas anidadas, util para desempaquetar por grupos:

```python
(a, b), (c, d) = symbols("a b, c d")   # dos grupos -> tuple de tuplas
```

### `**assumptions` (supuestos)

Todo supuesto pasado por palabra clave se aplica a **cada** simbolo creado en la llamada. Cambian lo que SymPy puede simplificar; ver [[concepto_symbols_assumptions]].

```python
from sympy import symbols, sqrt
x = symbols("x", positive=True)
sqrt(x**2)        # x        -> el supuesto habilita la simplificacion
n = symbols("n", integer=True)
n.is_integer      # True
a, b = symbols("a b", real=True)   # el supuesto va a los dos
```

### `cls`

Clase a instanciar en lugar de `Symbol`. Permite crear, por ejemplo, varias funciones de golpe.

```python
from sympy import symbols, Function
f, g = symbols("f g", cls=Function)   # (f, g) como funciones indefinidas
f(0)                                   # f(0)
```

## Casos de uso

### Variables de un problema con sus supuestos

```python
from sympy import symbols, solve
# longitudes fisicas: positivas
L, h = symbols("L h", positive=True)
# ecuacion en una incognita real
x = symbols("x", real=True)
solve(x**2 - L**2, x)     # [-L, L]
```

### Vector de incognitas con un rango

```python
from sympy import symbols, Matrix
xs = symbols("x:4")               # (x0, x1, x2, x3)
v = Matrix(xs)                    # vector columna de las 4 incognitas
```

### Coeficientes indexados para un polinomio generico

```python
from sympy import symbols
a = symbols("a:4")                       # (a0, a1, a2, a3)
x = symbols("x")
p = sum(a[i] * x**i for i in range(4))   # a3*x**3 + a2*x**2 + a1*x + a0
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Recibir un `Symbol` donde se esperaba tupla | Se pidio un solo nombre | Pedir varios o usar coma final `symbols("x,")` |
| `ValueError: ... cannot unpack` | Desempaquetar mas nombres de los creados | Igualar la cantidad de variables a los simbolos |
| Una simplificacion "obvia" no ocurre | Falto el supuesto que la habilita | Pasar `positive=True`/`real=True`/`integer=True` |
| Confundir `x:5` con `slice` | `:` es sintaxis de rango de la cadena | Es rango `x0..x4`, no un slice de Python |
| Crear el mismo simbolo con supuestos distintos | Mismo nombre + distintos supuestos = objetos distintos | Crear el simbolo una vez y reutilizarlo |

## Notas relacionadas

- [[Symbol]]
- [[sympy.sympify]]
- [[concepto_symbols_assumptions]]
- [[sympy.core/simbolos/index | simbolos]]
