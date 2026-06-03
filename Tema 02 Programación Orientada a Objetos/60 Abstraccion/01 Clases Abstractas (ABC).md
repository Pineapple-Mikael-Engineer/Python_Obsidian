---
title: Clases Abstractas (ABC)
tags:
  - python
  - teoria
  - abstraccion
draft: false
aliases:
  - Abstract Base Classes
  - ABC
  - Clase abstracta
---

# Clases Abstractas (ABC)

> [!definicion]
> Una **clase abstracta** es una clase que define un **contrato** —una interfaz común— y que **no puede instanciarse** mientras tenga métodos abstractos sin implementar. Sirve de **plantilla** para subclases concretas, que sí se instancian solo después de implementar todo el contrato. En Python se construye con el módulo `abc` (*Abstract Base Classes*): se hereda de `ABC` o se declara con `metaclass=ABCMeta`.

```python
from abc import ABC, abstractmethod

class Figura(ABC):                 # clase abstracta
    @abstractmethod
    def area(self): ...            # contrato: toda figura calcula su área
    def describir(self):           # método concreto, ya implementado
        return f"Figura de área {self.area()}"

class Circulo(Figura):             # subclase concreta
    def __init__(self, r): self.r = r
    def area(self): return 3.1416 * self.r ** 2

Figura()              # TypeError: Can't instantiate abstract class Figura
                      #            with abstract method area
Circulo(2).area()     # 12.5664
Circulo(2).describir()  # "Figura de área 12.5664"  -> usa el método concreto heredado
```

`Figura` fija *qué* debe ofrecer toda figura (`area`) sin decidir *cómo*; cada subclase aporta la implementación. La obligación se delega al decorador [[02 abstractmethod | @abstractmethod]].

## Dos formas de declararla

> [!regla]
> Heredar de `ABC` y declarar `metaclass=ABCMeta` son **equivalentes**: `ABC` es solo una clase base de conveniencia que ya usa `ABCMeta` como metaclase. La maquinaria abstracta vive en `ABCMeta`; `ABC` evita escribir la metaclase a mano.

```python
from abc import ABC, ABCMeta, abstractmethod

class A(ABC):                      # forma habitual
    @abstractmethod
    def m(self): ...

class B(metaclass=ABCMeta):        # equivalente, útil si ya hay otra metaclase
    @abstractmethod
    def m(self): ...

type(ABC)             # <class 'abc.ABCMeta'>
```

## No se instancia, pero sí se hereda

> [!info]
> La prohibición de instanciar **solo afecta a la clase con métodos abstractos pendientes**. Una clase abstracta puede mezclar métodos abstractos (contrato) y concretos (comportamiento compartido). Las subclases heredan los concretos y deben implementar los abstractos; una subclase que no los implemente **todos** sigue siendo abstracta.

```python
class FiguraColor(Figura):         # no implementa area
    def __init__(self, color): self.color = color

FiguraColor("rojo")   # TypeError: sigue abstracta (area sin implementar)
```

## Subclases virtuales con register()

> [!info]
> `register()` declara una clase como **subclase virtual** de una ABC sin herencia real: `isinstance`/`issubclass` la reconocen, pero la ABC **no impone** ni hereda nada en ella. Es un mecanismo para "afiliar" tipos preexistentes a una jerarquía abstracta (lo usan las ABC de `collections.abc`).

```python
class MiLista:
    def area(self): return 0

Figura.register(MiLista)
issubclass(MiLista, Figura)   # True   -> reconocida como subtipo
isinstance(MiLista(), Figura) # True
                              # pero NO se comprueba que implemente area: sin imposición
```

## Relación con otras notas

El contrato se expresa con [[02 abstractmethod | @abstractmethod]]; sin ningún método abstracto, una clase que herede de `ABC` se instancia con normalidad (deja de ser abstracta en la práctica). Las ABC son la versión **formal** de una interfaz, frente al *duck typing*; el contraste se desarrolla en [[03 Interfaces Informales vs Formales | Interfaces Informales vs Formales]].
