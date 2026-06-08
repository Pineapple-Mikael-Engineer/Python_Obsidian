---
title: Symbol — la clase del simbolo matematico (nombre + supuestos)
aliases:
  - Symbol
  - sympy.Symbol
  - clase Symbol
tags:
  - sympy
  - api/clase
  - core/simbolos
lib: sympy
mod: sympy
tipo: clase
requiere:
  - concepto_symbols_assumptions
draft: false
---

# Symbol — la clase del simbolo matematico (nombre + supuestos)

Clase que representa una **incognita** o variable matematica: el atomo sobre el que se construyen todas las expresiones de SymPy. Un `Symbol` queda definido por **dos cosas**: su **nombre** (`.name`, lo que se imprime) y sus **supuestos** (*assumptions*: `real`, `positive`, `integer`…), que son los que rigen el algebra. La forma idiomatica de crearlos es [[sympy.symbols]]; el constructor `Symbol("x")` existe y es equivalente para un unico simbolo. Su identidad (igualdad y hashing) depende del **par (nombre, supuestos)**: dos simbolos con el mismo nombre pero distintos supuestos son objetos **distintos**.

> Distincion clave: la **variable Python** y el **simbolo** son cosas separadas. `x = Symbol("y")` crea un simbolo llamado "y" guardado en la variable `x`; lo que SymPy imprime y compara es "y".

## Constructor

```python
sympy.Symbol(
    name,            # str: el nombre del simbolo (lo que se imprime)
    **assumptions,   # supuestos: real, positive, negative, integer, nonzero, complex, ...
) -> Symbol
```

```python
from sympy import Symbol
x = Symbol("x")                 # simbolo general (posiblemente complejo)
p = Symbol("p", positive=True)  # simbolo con supuesto
```

## Atributos principales

| Miembro | Tipo | Significado |
|---------|------|-------------|
| `.name` | `str` | El nombre del simbolo (cadena que se imprime) |
| `.assumptions0` | `dict` | Supuestos declarados explicitamente al crearlo |
| `.is_real` | `bool \| None` | `True`/`False`/`None` segun se sepa que es real |
| `.is_positive` | `bool \| None` | Si es real y > 0 (o `None` si se desconoce) |
| `.is_integer` | `bool \| None` | Si es entero |
| `.is_nonzero` | `bool \| None` | Si se sabe distinto de cero |
| `.is_commutative` | `bool` | Si conmuta en productos (por defecto `True`) |
| `.free_symbols` | `set` | El propio simbolo (`{x}`); coherencia con las `Expr` |

## Atributos en detalle

### `.name`

El nombre es una **cadena cualquiera**, no tiene por que coincidir con la variable Python. Es lo que se muestra al imprimir.

```python
from sympy import Symbol
s = Symbol("alpha")
s.name        # 'alpha'
s             # alpha
```

### Los supuestos `.is_*`

Cada simbolo expone sus propiedades como atributos `.is_*` con **logica de tres valores**: `True`, `False` o `None` (desconocido). Sin supuestos, casi todo es `None`. Ver [[concepto_symbols_assumptions]].

```python
from sympy import Symbol
p = Symbol("p", positive=True)
p.is_positive    # True
p.is_real        # True    -> positivo implica real
p.is_integer     # None    -> no se sabe
x = Symbol("x")
x.is_positive    # None    -> sin supuestos, desconocido
```

El `None` es clave: "no se sabe" **no** es "falso". No conviene escribir `if x.is_positive:` esperando que `None` se comporte como `False` sin tenerlo presente.

## Igualdad e identidad

Dos simbolos son **iguales** solo si coinciden **nombre y supuestos**. El mismo nombre con distintos supuestos da objetos distintos (y eso rompe simplificaciones si se mezclan sin querer).

```python
from sympy import Symbol
Symbol("x") == Symbol("x")                   # True
Symbol("x") == Symbol("x", positive=True)    # False  -> distintos supuestos
Symbol("x") == Symbol("y")                   # False  -> distinto nombre
```

> [!regla]
> Crea cada simbolo **una sola vez** (con sus supuestos) y reutilizalo. Volver a crearlo con supuestos distintos produce un objeto que SymPy considera diferente y las expresiones dejaran de casar.

## `Symbol("x")` frente a `symbols`

| Aspecto | `Symbol("x")` | `symbols("x y z")` |
|---------|---------------|--------------------|
| Crea | Un unico simbolo | Uno o varios (tupla) |
| Rangos / grupos | No | Si (`x:5`, `a:d`) |
| Uso idiomatico | Puntual, un simbolo | Recomendado en general |
| Supuestos | `**assumptions` | `**assumptions` a todos |

```python
from sympy import Symbol, symbols
x = Symbol("x")            # un simbolo
a, b, c = symbols("a b c") # varios de una vez (preferido)
```

## Casos de uso

### Construir y manipular una expresion

```python
from sympy import Symbol
x = Symbol("x")
expr = x**2 + 2*x + 1
expr.free_symbols     # {x}
expr.subs(x, 3)       # 16
```

### Supuestos que cambian el resultado

```python
from sympy import Symbol, sqrt, simplify
x = Symbol("x")
simplify(sqrt(x**2))            # sqrt(x**2)   -> sin supuesto, no simplifica
a = Symbol("a", positive=True)
simplify(sqrt(a**2))           # a
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Dos simbolos "iguales" no son iguales | Mismo nombre, distintos supuestos -> objetos distintos | Crear el simbolo una vez y reutilizarlo |
| `if x.is_positive:` se comporta raro | `None` (desconocido) no es `False` | Comparar explicitamente con `is True`/`is None` |
| Una simplificacion no ocurre | Falta el supuesto que la habilita | Crear con `real`/`positive`/`integer` |
| Confundir variable Python y nombre | `x = Symbol("y")` imprime "y" | Hacer coincidir nombre y variable salvo intencion |
| Crear muchos simbolos a mano | `Symbol` es de a uno | Usar [[sympy.symbols]] con rangos/grupos |

## Notas relacionadas

- [[sympy.symbols]]
- [[sympy.sympify]]
- [[concepto_symbols_assumptions]]
- [[sympy.core/simbolos/index | simbolos]]
