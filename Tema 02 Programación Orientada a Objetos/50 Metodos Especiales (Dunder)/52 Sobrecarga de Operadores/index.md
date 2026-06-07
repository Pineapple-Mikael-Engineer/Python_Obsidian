---
title: Sobrecarga de Operadores
order: 52
draft: false
description: Implementar los dunders de operadores para que un objeto propio responda a + - * == < y demás
tags:
  - Index
  - Tema
aliases:
  - Sobrecarga de Operadores
  - Operator Overloading
---
# Sobrecarga de Operadores

La **sobrecarga de operadores** consiste en implementar los métodos *dunder* asociados a cada operador para que un objeto propio responda a la sintaxis de operadores nativa: `+`, `-`, `*`, `==`, `<`, etc. Cuando Python evalúa `a + b`, no busca una función global: invoca `a.__add__(b)`. Definir ese método en la clase es lo que da significado al operador sobre instancias propias.

```python
class Dinero:
    def __init__(self, centavos):
        self.centavos = centavos
    def __add__(self, otro):                  # habilita +
        return Dinero(self.centavos + otro.centavos)
    def __eq__(self, otro):                   # habilita ==
        return self.centavos == otro.centavos
    def __repr__(self):
        return f"Dinero({self.centavos})"

Dinero(150) + Dinero(50)                      # Dinero(200)
Dinero(100) == Dinero(100)                    # True
```

## Subtemas

- [[01 Operadores Aritmeticos | Operadores Aritméticos]] — `__add__`, `__sub__`, `__mul__`, `__truediv__`, `__neg__`…: aritmética sobre objetos, con las variantes **reflejadas** (`__radd__`) e **in-place** (`__iadd__`).
- [[02 Operadores de Comparacion | Operadores de Comparación]] — `__eq__`, `__lt__`, `__le__`…: igualdad y orden, su efecto sobre `__hash__` y la derivación automática con `functools.total_ordering`.

## Operador a método

| Operador | Dunder | Operador | Dunder |
| -------- | ------ | -------- | ------ |
| `a + b` | `__add__` | `a == b` | `__eq__` |
| `a - b` | `__sub__` | `a != b` | `__ne__` |
| `a * b` | `__mul__` | `a < b` | `__lt__` |
| `a / b` | `__truediv__` | `a <= b` | `__le__` |
| `a // b` | `__floordiv__` | `a > b` | `__gt__` |
| `a % b` | `__mod__` | `a >= b` | `__ge__` |
| `a ** b` | `__pow__` | `-a` | `__neg__` |

## Reflejados e in-place

> [!info]
> Cada operador binario admite dos variantes además de la forma directa:
>
> - **Reflejados** (`__radd__`, `__rmul__`, …): se invocan sobre el operando **derecho** cuando el izquierdo no sabe operar con él. En `3 * vector`, `int.__mul__` no conoce `Vector` y devuelve `NotImplemented`, así que Python recurre a `vector.__rmul__(3)`. Imprescindibles cuando el otro operando es un tipo nativo a la izquierda.
> - **In-place** (`__iadd__`, `__imul__`, …): implementan `+=`, `*=`, etc. Permiten **mutar** el objeto en lugar de crear uno nuevo. Si no existen, `a += b` se reduce a `a = a + b` usando `__add__`.

> [!regla]
> Un dunder de operador devuelve `NotImplemented` (no lo lanza) cuando no sabe operar con el otro tipo. Python interpreta ese valor como "delega": prueba el método reflejado del otro operando, y si tampoco, lanza `TypeError`. Devolver `NotImplemented` es lo que mantiene la sobrecarga **cooperativa** entre tipos.

La sobrecarga es la cara de los dunders que conecta con el [[40 Polimorfismo/index | polimorfismo]]: un mismo `+` actúa distinto según la clase, y el caso extremo —un operador con varias firmas según el tipo del otro operando— se trata en [[43 Sobrecarga de Operadores | sobrecarga dentro de polimorfismo]].
