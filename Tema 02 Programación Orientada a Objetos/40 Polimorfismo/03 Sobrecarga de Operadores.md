---
title: Sobrecarga de Operadores
tags:
  - python
  - teoria
  - polimorfismo
draft: false
aliases:
  - Operator overloading
  - Polimorfismo ad-hoc
---

# Sobrecarga de Operadores

> [!definicion]
> La **sobrecarga de operadores** consiste en dar significado a operadores (`+`, `==`, `<`, `*`, `[]`, `len()`…) para objetos de clases propias, implementando los **métodos especiales** (dunder) que Python asocia a cada operador. Es **polimorfismo ad-hoc**: el mismo símbolo realiza operaciones distintas según el tipo de sus operandos.

```python
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, otro):                       # da sentido a '+'
        return Vector(self.x + otro.x, self.y + otro.y)
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

Vector(1, 2) + Vector(3, 4)   # Vector(4, 6)  -> Python invoca __add__
```

`a + b` se traduce a `a.__add__(b)`: el operador `+` es solo azúcar sintáctico sobre una llamada a método. La definición completa de cada dunder y sus reglas (operadores reflejados, `NotImplemented`, contrato `__eq__`/`__hash__`) se desarrolla en [[50 Metodos Especiales (Dunder)/index | métodos especiales]].

## Operador → método especial

| Operador / sintaxis | Método dunder | Invocación equivalente |
| ------------------- | ------------- | ---------------------- |
| `a + b`             | `__add__`     | `a.__add__(b)`         |
| `a * b`             | `__mul__`     | `a.__mul__(b)`         |
| `a == b`            | `__eq__`      | `a.__eq__(b)`          |
| `a < b`             | `__lt__`      | `a.__lt__(b)`          |
| `len(a)`            | `__len__`     | `a.__len__()`          |
| `a[i]`              | `__getitem__` | `a.__getitem__(i)`     |

El detalle de los operadores aritméticos (`+ - * / // % **` y sus reflejados `__radd__`…) se trata en [[01 Operadores Aritmeticos]].

## Ejemplo: tipo Dinero

> [!ejemplo]
> Un tipo `Dinero` que sobrecarga la suma, la igualdad y el orden. Cada operador delega en su dunder; el operando aparece a la derecha del símbolo se pasa como argumento.

```python
class Dinero:
    def __init__(self, centavos): self.c = centavos
    def __add__(self, otro):  return Dinero(self.c + otro.c)   # '+'
    def __eq__(self, otro):   return self.c == otro.c          # '=='
    def __lt__(self, otro):   return self.c < otro.c           # '<'
    def __repr__(self):       return f"{self.c/100:.2f} €"

Dinero(150) + Dinero(50)    # 2.00 €
Dinero(150) == Dinero(150)  # True
Dinero(99) < Dinero(150)    # True
sorted([Dinero(300), Dinero(99), Dinero(150)])  # ordena gracias a __lt__
```

Definir `__lt__` basta para que `sorted` y `min`/`max` operen sobre el tipo: los algoritmos de la librería estándar son polimórficos sobre cualquier objeto que implemente la comparación requerida.

## Polimorfismo ad-hoc, no de subtipos

> [!info]
> La sobrecarga de operadores es polimorfismo **ad-hoc**: el comportamiento del símbolo se selecciona por el **tipo concreto** de los operandos, no por despacho dinámico sobre una jerarquía. Difiere así del [[02 Polimorfismo de Subtipos | polimorfismo de subtipos]], donde una base común y la sobrescritura determinan la versión ejecutada.

> [!warning]
> Implementar un operador no obliga a implementar sus relacionados: definir `__eq__` no genera `__ne__` coherente automáticamente en todos los casos, y `__lt__` por sí solo no provee `<=`, `>`, `>=`. Para el conjunto completo de comparaciones a partir de unas pocas se usa `functools.total_ordering`. Sobrecargar operadores solo cuando la semántica sea **natural** para el tipo; forzarla degrada la legibilidad.
