---
title: abstractmethod
order: 62
tags:
  - python
  - teoria
  - abstraccion
draft: false
aliases:
  - "@abstractmethod"
  - Método abstracto
  - abstractmethod
---

# abstractmethod

> [!definicion]
> El decorador `@abstractmethod` marca un método como de **implementación obligatoria**: declara el contrato pero (normalmente) no aporta cuerpo. Una subclase es **concreta** —e instanciable— solo si implementa **todos** los métodos abstractos heredados. Mientras quede alguno sin implementar, la clase permanece abstracta. Solo tiene efecto dentro de una clase cuya metaclase sea `ABCMeta` (es decir, que herede de [[61 Clases Abstractas (ABC) | ABC]]).

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self): ...
    @abstractmethod
    def perimetro(self): ...

class Cuadrado(Figura):
    def __init__(self, l): self.l = l
    def area(self): return self.l ** 2
    def perimetro(self): return 4 * self.l   # implementa los DOS -> concreta

Cuadrado(3).area()    # 9
```

## TypeError al instanciar incompleta

> [!ejemplo]
> Si la subclase deja un método abstracto sin implementar, **sigue siendo abstracta** y al instanciarla se produce `TypeError`, indicando exactamente qué métodos faltan.

```python
class Rectangulo(Figura):
    def __init__(self, b, h): self.b, self.h = b, h
    def area(self): return self.b * self.h
    # falta perimetro

Rectangulo(2, 3)
# TypeError: Can't instantiate abstract class Rectangulo
#            with abstract method perimetro
```

> [!warning]
> La comprobación ocurre **al instanciar**, no al definir la clase. Definir `Rectangulo` con un método abstracto pendiente **no lanza ningún error**; el `TypeError` salta solo cuando se intenta crear un objeto. La clase incompleta es válida como base intermedia de otras subclases.

## Combinación con otros decoradores

> [!regla]
> `@abstractmethod` se combina con `@property`, `@classmethod` y `@staticmethod`. El orden es fijo: **`@abstractmethod` debe ser el decorador más interno** (el más cercano al `def`), con el otro decorador encima.

```python
from abc import ABC, abstractmethod

class Recurso(ABC):
    @property
    @abstractmethod
    def nombre(self): ...          # propiedad abstracta

    @classmethod
    @abstractmethod
    def desde_id(cls, i): ...      # método de clase abstracto

    @staticmethod
    @abstractmethod
    def validar(x): ...            # método estático abstracto

class Archivo(Recurso):
    @property
    def nombre(self): return "a.txt"
    @classmethod
    def desde_id(cls, i): return cls()
    @staticmethod
    def validar(x): return x is not None
```

## Cuerpo opcional y super()

> [!info]
> Un método abstracto **puede** tener cuerpo. No exime a la subclase de redefinirlo, pero permite ofrecer una implementación base reutilizable invocable con `super()`. El convenio habitual es dejarlo vacío (`...`, `pass`) o lanzar `NotImplementedError` como documentación del contrato.

```python
class Base(ABC):
    @abstractmethod
    def cargar(self):
        return "recurso base"     # cuerpo aprovechable

class Hija(Base):
    def cargar(self):
        return super().cargar() + " extendido"   # "recurso base extendido"
```

## Relación con otras notas

`@abstractmethod` es el mecanismo que convierte una clase [[61 Clases Abstractas (ABC) | ABC]] en un contrato exigible. Esta imposición explícita distingue la interfaz **formal** de la informal por *duck typing*; ver [[63 Interfaces Informales vs Formales | Interfaces Informales vs Formales]].
