---
title: 60 Abstraccion
draft: false
description: Exponer qué hace un objeto y ocultar cómo — clases abstractas e interfaces
tags:
  - Index
  - Tema
aliases:
  - Abstracción
  - Abstraction
---
# Abstracción

La **abstracción** consiste en exponer *qué* hace un objeto y ocultar *cómo* lo hace. Una clase abstracta define un **contrato** —un conjunto de métodos que las subclases deben implementar— sin proporcionar (necesariamente) su implementación. Sirve para fijar una interfaz común y obligar a que todas las variantes la cumplan.

En Python la abstracción formal se construye con el módulo `abc` (*Abstract Base Classes*): una clase abstracta no puede instanciarse y declara métodos abstractos que las subclases concretas están obligadas a definir.

```python
from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self): ...        # contrato: toda figura calcula su área

class Circulo(Figura):
    def __init__(self, r): self.r = r
    def area(self): return 3.1416 * self.r**2

Figura()        # TypeError: no se puede instanciar una clase abstracta
Circulo(2).area()   # 12.5664
```

## Subtemas

- [[01 Clases Abstractas (ABC) | Clases Abstractas (ABC)]] — el módulo `abc`, la base `ABC` y por qué una clase abstracta no se instancia.
- [[02 abstractmethod | abstractmethod]] — el decorador `@abstractmethod` y cómo obliga a las subclases a implementar el método.
- [[03 Interfaces Informales vs Formales | Interfaces Informales vs Formales]] — *duck typing* y protocolos frente a la imposición explícita de las ABC.

## Mecanismos de abstracción

| Mecanismo | Garantía | Subtema |
| --------- | -------- | ------- |
| `ABC` + `@abstractmethod` | Imposición en tiempo de instanciación | [[01 Clases Abstractas (ABC) \| Clases Abstractas (ABC)]] |
| Interfaz informal (*duck typing*) | Convención, sin imposición | [[03 Interfaces Informales vs Formales \| Interfaces Informales vs Formales]] |
| `typing.Protocol` | Tipado estructural verificable | [[03 Interfaces Informales vs Formales \| Interfaces Informales vs Formales]] |

La abstracción se apoya en el [[40 Polimorfismo/index | polimorfismo]]: el contrato común permite tratar uniformemente a todas las implementaciones, y suele combinarse con [[30 Herencia/index | herencia]] para compartir lo común.
