---
title: Herramientas Modernas
order: 90
draft: false
description: Utilidades del Python moderno para escribir clases — dataclasses, slots, new y Enum
tags:
  - Index
  - Tema
aliases:
  - Herramientas Modernas
---
# Herramientas Modernas

El Python moderno (3.7+) incorpora utilidades que reducen el código repetitivo de las clases y refinan su comportamiento: generar automáticamente `__init__`/`__repr__`/`__eq__`, fijar los atributos para ahorrar memoria, controlar la creación del objeto o definir conjuntos cerrados de constantes. No son nuevos paradigmas, sino herramientas que hacen las clases más concisas y seguras.

```python
from dataclasses import dataclass

@dataclass
class Punto:
    x: int
    y: int          # genera __init__, __repr__ y __eq__ automáticamente

Punto(1, 2) == Punto(1, 2)   # True
```

## Subtemas

- [[91 Dataclasses | Dataclasses]] — `@dataclass` genera los métodos de plantilla (`__init__`, `__repr__`, `__eq__`) a partir de los campos anotados.
- [[92 __slots__ | __slots__]] — declarar los atributos fijos de la clase para eliminar el `__dict__` y reducir memoria.
- [[93 __new__ vs __init__ | __new__ vs __init__]] — la creación del objeto (`__new__`) frente a su inicialización (`__init__`).
- [[94 Enumeraciones (Enum) | Enumeraciones (Enum)]] — conjuntos cerrados y nombrados de constantes con `Enum`.

## Para qué sirve cada una

| Herramienta | Resuelve | Subtema |
| ----------- | -------- | ------- |
| `@dataclass` | Clases de datos sin *boilerplate* | [[91 Dataclasses \| Dataclasses]] |
| `__slots__` | Memoria y atributos fijos | [[92 __slots__ \| __slots__]] |
| `__new__` | Control de la creación (inmutables, singletons) | [[93 __new__ vs __init__ \| __new__ vs __init__]] |
| `Enum` | Constantes nombradas y seguras | [[94 Enumeraciones (Enum) \| Enumeraciones (Enum)]] |

`@dataclass` se apoya en las [[12 Atributos/index | anotaciones de atributos]] y en `__slots__`; `__new__` precede al [[04 Constructor __init__ | constructor __init__]] visto en la definición de clases.
