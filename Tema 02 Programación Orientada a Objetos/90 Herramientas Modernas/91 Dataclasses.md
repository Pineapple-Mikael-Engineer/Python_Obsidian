---
title: Dataclasses
order: 91
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - dataclass
  - Clases de datos
---

# Dataclasses

> [!definicion]
> El decorador `@dataclass` del módulo `dataclasses` (Python 3.7+) **genera automáticamente** los métodos de plantilla de una clase —`__init__`, `__repr__` y `__eq__`— a partir de los **campos anotados con tipo** en el cuerpo. Cada anotación `nombre: tipo` se convierte en un parámetro del constructor y en un atributo de instancia, en el mismo orden de declaración.

```python
from dataclasses import dataclass

@dataclass
class Punto:
    x: int
    y: int

p = Punto(1, 2)
p                       # Punto(x=1, y=2)   -> __repr__ generado
Punto(1, 2) == Punto(1, 2)   # True          -> __eq__ por campos
p.x, p.y                # (1, 2)
```

Solo las variables **anotadas** son campos. `x = 0` sin anotación es un atributo de clase normal, **no** un campo del dataclass.

## Contraste con la clase manual

La clase equivalente escrita a mano requiere repetir cada nombre tres veces:

```python
class Punto:                          # equivale al dataclass de arriba
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Punto(x={self.x!r}, y={self.y!r})"
    def __eq__(self, otro):
        if not isinstance(otro, Punto):
            return NotImplemented
        return (self.x, self.y) == (otro.x, otro.y)
```

El dataclass elimina ese *boilerplate*. La generación de `__repr__` y `__eq__` corresponde a lo que en su forma manual se detalla en [[01 __str__ y __repr__ | __str__ y __repr__]] y [[02 Operadores de Comparacion | los operadores de comparación]].

## Parámetros del decorador

| Parámetro | Efecto |
| --------- | ------ |
| `eq=True` (defecto) | genera `__eq__` (igualdad por tupla de campos) |
| `repr=True` (defecto) | genera `__repr__` |
| `frozen=True` | instancias **inmutables**; asignar atributos lanza `FrozenInstanceError`. Al ser inmutable, genera `__hash__` → la instancia es **hashable** (usable en `set`/`dict`) |
| `order=True` | genera `__lt__`, `__le__`, `__gt__`, `__ge__` comparando la tupla de campos en orden |
| `slots=True` (3.10+) | genera `__slots__` con los campos (ver [[92 __slots__ \| __slots__]]) |

```python
@dataclass(frozen=True, order=True)
class Version:
    mayor: int
    menor: int

Version(2, 1) < Version(2, 5)   # True   -> compara (2,1) < (2,5)
{Version(1, 0)}                 # OK: frozen -> hashable
```

## Defaults y el trap del mutable compartido

Un campo con valor por defecto debe ir **después** de los campos sin defecto (misma regla que los parámetros de función).

> [!warning]
> Un default **mutable** literal (`items: list = []`) está **prohibido**: ese único objeto se compartiría entre todas las instancias, el mismo error clásico del [[02 Atributos de Clase | atributo de clase mutable]]. El dataclass lo detecta y lanza `ValueError` en la definición. La solución es `field(default_factory=list)`: la fábrica se invoca **por instancia**, produciendo un objeto nuevo cada vez.

```python
from dataclasses import dataclass, field

@dataclass
class Cesta:
    dueno: str
    items: list = field(default_factory=list)   # lista NUEVA por instancia

a = Cesta("Ana"); b = Cesta("Luis")
a.items.append("pan")
b.items                 # []        -> estado aislado
a.items is b.items      # False
```

`field()` también controla campos individuales: `field(repr=False)` lo excluye del `__repr__`, `field(compare=False)` del `__eq__`/orden, `field(init=False)` lo retira del constructor.

## Post-inicialización

Si se define `__post_init__(self)`, el `__init__` generado lo invoca tras asignar los campos. Sirve para validación o para derivar campos calculados.

```python
@dataclass
class Rect:
    ancho: float
    alto: float
    area: float = field(init=False)     # no es parámetro del constructor

    def __post_init__(self):
        self.area = self.ancho * self.alto

Rect(3, 4).area         # 12
```

## Cuándo NO usar dataclass

> [!regla]
> `@dataclass` encaja cuando la clase es esencialmente un **agregado de datos** con identidad por valor. **No** aporta —y estorba— cuando: la clase es sobre todo **comportamiento** (muchos métodos, pocos campos); la igualdad debe ser por **identidad** y no por campos (entidades con estado mutable); el `__init__` necesita lógica compleja que no cabe en `field`/`__post_init__`; o se requiere control fino de invariantes. Para conjuntos cerrados de constantes nombradas, la herramienta es [[94 Enumeraciones (Enum) \| Enum]], no un dataclass.
