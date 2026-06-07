---
title: Operadores Aritméticos
order: 1
tags:
  - python
  - teoria
  - dunder
draft: false
aliases:
  - Arithmetic dunders
  - Operadores aritméticos sobrecargados
---

# Operadores Aritméticos

> [!definicion]
> Los **dunders aritméticos** son los métodos `__x__` que dan significado a los operadores aritméticos sobre instancias propias. Python traduce cada operador a una llamada de método: `a + b` invoca `a.__add__(b)`, `a * b` invoca `a.__mul__(b)`, y así con el resto. Definirlos hace que un objeto se comporte como un número en expresiones aritméticas.

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, otro):                  # +  -> suma componente a componente
        return Vector(self.x + otro.x, self.y + otro.y)
    def __mul__(self, k):                      # *  -> producto por escalar (vector a la izquierda)
        return Vector(self.x * k, self.y * k)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

Vector(1, 2) + Vector(3, 4)                    # Vector(4, 6)
Vector(1, 2) * 3                               # Vector(3, 6)   -> usa __mul__
```

## Operador a método

| Operador | Dunder | Operación |
| -------- | ------ | --------- |
| `a + b` | `__add__` | suma |
| `a - b` | `__sub__` | resta |
| `a * b` | `__mul__` | multiplicación |
| `a / b` | `__truediv__` | división real |
| `a // b` | `__floordiv__` | división entera |
| `a % b` | `__mod__` | módulo |
| `a ** b` | `__pow__` | potencia |
| `-a` | `__neg__` | negación unaria (un solo argumento) |

> [!info]
> Los binarios reciben `self` y el otro operando; `__neg__` es **unario** y recibe solo `self`. Existen otros unarios análogos: `__pos__` (`+a`) y `__abs__` (`abs(a)`).

## Operadores reflejados

> [!definicion]
> Los **operadores reflejados** (`__radd__`, `__rsub__`, `__rmul__`, …) se invocan sobre el operando **derecho** cuando el izquierdo no sabe operar con él. Para `x + y`, Python intenta primero `x.__add__(y)`; si devuelve `NotImplemented`, intenta `y.__radd__(x)`. Son necesarios cuando un tipo nativo aparece a la izquierda de un objeto propio.

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __mul__(self, k):                      # vector * escalar
        return Vector(self.x * k, self.y * k)
    def __rmul__(self, k):                     # escalar * vector  -> delega en __mul__
        return self.__mul__(k)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

3 * Vector(1, 2)                               # Vector(3, 6)
# int.__mul__(3, Vector) -> NotImplemented; Python prueba Vector.__rmul__(3) -> Vector(3, 6)
```

> [!regla]
> Cuando un dunder no sabe operar con el tipo del otro operando, **devuelve** `NotImplemented` (no lo lanza). Python lo interpreta como "delega": prueba el método reflejado del otro operando y, si tampoco resuelve, lanza `TypeError`. Devolver `NotImplemented` en vez de adivinar es lo que permite que dos tipos cooperen.

```python
def __add__(self, otro):
    if not isinstance(otro, Vector):
        return NotImplemented                  # deja que el otro operando lo intente
    return Vector(self.x + otro.x, self.y + otro.y)
```

## Operadores in-place

> [!definicion]
> Los **operadores in-place** (`__iadd__`, `__isub__`, `__imul__`, …) implementan las asignaciones aumentadas `+=`, `-=`, `*=`. Permiten **mutar** el objeto y devolver `self`, evitando crear uno nuevo. Si la clase no los define, `a += b` se reduce a `a = a + b`, que usa `__add__` y reasigna el nombre.

```python
class Carrito:
    def __init__(self, items=None):
        self.items = items or []
    def __iadd__(self, item):                  # +=  -> muta y devuelve self
        self.items.append(item)
        return self

c = Carrito()
antes = c
c += "libro"                                   # c.items == ["libro"]
antes is c                                      # True  -> mismo objeto, mutado
```

> [!warning]
> `__iadd__` **debe** devolver el objeto resultante (normalmente `self`); su valor de retorno es lo que se reasigna al nombre. Olvidar el `return` deja el nombre apuntando a `None`. En tipos **inmutables** no se define `__iadd__`: `+=` recae en `__add__` y produce un objeto nuevo, como ocurre con `int` o `str`.

## Relación con otras notas

La aritmética sobre objetos es polimórfica: el mismo `+` actúa según la clase que implementa `__add__`, conectando con el [[40 Polimorfismo/index | polimorfismo]]. El otro gran grupo de operadores sobrecargables, igualdad y orden, se trata en [[02 Operadores de Comparacion | Operadores de Comparación]].
