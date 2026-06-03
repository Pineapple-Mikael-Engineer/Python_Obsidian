---
title: Operadores de Comparacion
tags:
  - python
  - teoria
  - dunder
draft: false
aliases:
  - Comparison dunders
  - Operadores de comparación sobrecargados
  - Rich comparison methods
---

# Operadores de Comparación

> [!definicion]
> Los **dunders de comparación** dan significado a los operadores de igualdad y orden sobre instancias propias. Python traduce cada uno a una llamada de método: `a == b` invoca `a.__eq__(b)`, `a < b` invoca `a.__lt__(b)`, etc. Definirlos permite comparar objetos por su **contenido** y ordenarlos con `sorted`, `min`, `max`.

```python
class Version:
    def __init__(self, mayor, menor):
        self.mayor, self.menor = mayor, menor
    def __eq__(self, otro):                    # ==
        return (self.mayor, self.menor) == (otro.mayor, otro.menor)
    def __lt__(self, otro):                    # <
        return (self.mayor, self.menor) < (otro.mayor, otro.menor)
    def __repr__(self):
        return f"Version({self.mayor}, {self.menor})"

Version(1, 4) == Version(1, 4)                 # True
Version(1, 4) < Version(2, 0)                  # True
```

## Operador a método

| Operador | Dunder | Significado |
| -------- | ------ | ----------- |
| `a == b` | `__eq__` | igualdad |
| `a != b` | `__ne__` | desigualdad |
| `a < b` | `__lt__` | menor que |
| `a <= b` | `__le__` | menor o igual |
| `a > b` | `__gt__` | mayor que |
| `a >= b` | `__ge__` | mayor o igual |

> [!info]
> Los operadores de orden son **reflejos** entre sí: `a < b` recurre a `b.__gt__(a)` si `a.__lt__(b)` devuelve `NotImplemented`. Por eso basta implementar `__lt__` para que `>` funcione entre instancias de la misma clase. `__ne__` se deriva automáticamente de `__eq__` en Python 3 (devuelve su negación).

## Igualdad por defecto vs. definida

> [!definicion]
> Sin `__eq__` propio, un objeto hereda `object.__eq__`, que compara **identidad**: `a == b` equivale a `a is b`. Dos instancias distintas con el mismo contenido resultan **desiguales**. Definir `__eq__` reemplaza esa identidad por una igualdad **estructural**, basada en los atributos.

```python
class P:
    def __init__(self, v): self.v = v

P(1) == P(1)                                    # False  -> identidad: son objetos distintos

class Q:
    def __init__(self, v): self.v = v
    def __eq__(self, otro): return self.v == otro.v

Q(1) == Q(1)                                    # True   -> igualdad estructural
```

## Igualdad y hashabilidad

> [!warning]
> Definir `__eq__` **anula** el `__hash__` heredado: la clase pasa a ser **no hashable** y no puede usarse como clave de diccionario ni elemento de `set`. Python lo hace por seguridad, pues dos objetos iguales **deben** tener el mismo hash. Si el objeto es inmutable y debe ser hashable, hay que definir `__hash__` explícitamente, coherente con `__eq__`.

```python
class Punto:
    def __init__(self, x, y): self.x, self.y = x, y
    def __eq__(self, otro):
        return (self.x, self.y) == (otro.x, otro.y)
    def __hash__(self):                         # coherente con __eq__
        return hash((self.x, self.y))

{Punto(1, 2)}                                   # OK  -> hashable porque se definió __hash__
# Sin __hash__: TypeError: unhashable type: 'Punto'
```

La regla "objetos iguales comparten hash" y la necesidad de inmutabilidad para ser clave se desarrollan en [[01 Objetos Inmutables | objetos inmutables]].

## Derivar el orden con total_ordering

> [!regla]
> `functools.total_ordering` es un decorador de clase que **deriva** los cuatro operadores de orden (`<`, `<=`, `>`, `>=`) a partir de `__eq__` y **uno** de ellos —habitualmente `__lt__`—. Evita escribir seis métodos a mano manteniendo la coherencia entre ellos.

```python
from functools import total_ordering

@total_ordering
class Temperatura:
    def __init__(self, grados): self.grados = grados
    def __eq__(self, otro): return self.grados == otro.grados
    def __lt__(self, otro): return self.grados < otro.grados
    # __le__, __gt__, __ge__ los genera total_ordering

Temperatura(20) <= Temperatura(25)             # True   -> derivado de __lt__ y __eq__
Temperatura(30) > Temperatura(25)              # True   -> derivado
sorted([Temperatura(30), Temperatura(10)])     # ordena por __lt__
```

> [!info]
> `total_ordering` genera operadores correctos pero **menos eficientes** que los escritos a mano (cada uno se compone de varias llamadas). Para clases con comparaciones intensivas conviene definir los seis explícitamente.

## Relación con otras notas

La comparación es polimórfica: `==` y `<` actúan según la clase que implementa el dunder, en línea con el [[40 Polimorfismo/index | polimorfismo]]. El otro gran grupo de operadores sobrecargables, la aritmética, se trata en [[01 Operadores Aritmeticos | Operadores Aritméticos]].
