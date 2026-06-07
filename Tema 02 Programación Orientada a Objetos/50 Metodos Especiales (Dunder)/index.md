---
title: Métodos Especiales (Dunder)
order: 50
draft: false
description: Los métodos __x__ que integran un objeto con la sintaxis del lenguaje
tags:
  - Index
  - Tema
aliases:
  - Métodos Especiales
  - Métodos Mágicos
  - Dunder Methods
---
# Métodos Especiales (Dunder)

Los **métodos especiales** —o *dunder*, por *double underscore*— son métodos con nombre `__x__` que Python invoca **automáticamente** ante ciertas sintaxis y funciones del lenguaje. Definir `__len__` hace que `len(obj)` funcione; definir `__add__` hace que `obj + otro` funcione. Son el mecanismo por el que un objeto propio se comporta como uno nativo y se integra con operadores, *built-ins* y construcciones del lenguaje.

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, otro):              # habilita el operador +
        return Vector(self.x + otro.x, self.y + otro.y)
    def __repr__(self):                   # habilita repr() y la consola
        return f"Vector({self.x}, {self.y})"

Vector(1, 2) + Vector(3, 4)               # Vector(4, 6)
```

El catálogo completo está en [[Catalogo de Metodos Dunder | Catálogo de Métodos Dunder]]; aquí se desarrollan los grupos principales.

## Subtemas

- [[51 Representacion/index | Representación]] — `__str__`, `__repr__` y `__format__`: cómo se muestra un objeto.
- [[52 Sobrecarga de Operadores/index | Sobrecarga de Operadores]] — `__add__`, `__eq__`, `__lt__`…: dar significado a los operadores aritméticos y de comparación.
- [[53 Comportamiento de Objeto/index | Comportamiento de Objeto]] — `__len__`/`__getitem__` (contenedor), `__call__` (invocable) y `__enter__`/`__exit__` (gestor de contexto).

## Categorías de dunders

| Categoría | Métodos clave | Habilita | Subtema |
| --------- | ------------- | -------- | ------- |
| Representación | `__str__`, `__repr__` | `print`, `repr`, consola | [[51 Representacion/index \| Representación]] |
| Operadores | `__add__`, `__eq__`, `__lt__` | `+`, `==`, `<` | [[52 Sobrecarga de Operadores/index \| Sobrecarga de Operadores]] |
| Contenedor | `__len__`, `__getitem__`, `__iter__` | `len`, `obj[i]`, `for` | [[53 Comportamiento de Objeto/index \| Comportamiento de Objeto]] |
| Invocable | `__call__` | `obj()` | [[53 Comportamiento de Objeto/index \| Comportamiento de Objeto]] |
| Contexto | `__enter__`, `__exit__` | `with` | [[53 Comportamiento de Objeto/index \| Comportamiento de Objeto]] |

La sobrecarga de operadores es la cara de los dunders que conecta con el [[40 Polimorfismo/index | polimorfismo]]: un mismo operador `+` actúa distinto según la clase que lo implementa.
