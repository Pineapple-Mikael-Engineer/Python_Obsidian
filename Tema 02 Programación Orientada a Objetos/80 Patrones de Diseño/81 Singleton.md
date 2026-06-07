---
title: Singleton
order: 81
tags:
  - python
  - teoria
  - patrones
draft: false
aliases:
  - Instancia única
  - Single instance
---

# Singleton

> [!definicion]
> El **Singleton** garantiza que una clase tenga **una sola instancia** y proporciona un punto de acceso global a ella. Toda construcción posterior devuelve **el mismo objeto** ya creado, en lugar de uno nuevo.

```python
class Config:
    _instancia = None

    def __new__(cls, *args, **kwargs):
        if cls._instancia is None:                 # primera vez: crea
            cls._instancia = super().__new__(cls)
        return cls._instancia                      # resto: la misma

a = Config()
b = Config()
a is b                                             # True  -> mismo objeto
```

`__new__` se ejecuta **antes** que `__init__` y es responsable de *crear* la instancia. Al cachearla en `cls._instancia` y devolverla siempre, todas las llamadas comparten estado.

## Cuidado con __init__

> [!warning]
> `__new__` controla la creación, pero **`__init__` se llama en cada construcción** sobre la instancia devuelta. Si `__init__` reasigna atributos, una segunda llamada **reinicializa** el objeto compartido y borra su estado.

```python
class Config:
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia
    def __init__(self):
        self.datos = []                            # se ejecuta cada vez

c = Config(); c.datos.append("x")
Config().datos                                     # []  -> reinicializado, no ["x"]
```

La solución es proteger `__init__` con una bandera (`if hasattr(self, "_init"): return`) o concentrar la lógica en `__new__`.

## Vía metaclase

> [!ejemplo]
> Una **metaclase** intercepta la llamada `Clase()` en su `__call__`, lo que permite reutilizar el mismo Singleton para varias clases sin tocar su `__new__`.

```python
class SingletonMeta(type):
    _instancias = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]

class Logger(metaclass=SingletonMeta):
    pass

Logger() is Logger()                               # True
```

Frente al [[02 Metodos de Clase (classmethod)]] u otras técnicas, la metaclase encapsula el control de instancia en un único lugar reutilizable.

## La forma idiomática: el módulo

> [!info]
> En Python un **módulo ya es un singleton**: se importa y ejecuta **una sola vez**, y sus variables globales quedan cacheadas en `sys.modules`. Por eso suele preferirse un módulo (o una instancia global creada al importar) antes que un Singleton clásico con `__new__` o metaclases, que añaden complejidad raramente justificada.

```python
# config.py
ajustes = {"debug": False}                         # estado compartido del módulo

# otro_modulo.py
from config import ajustes                          # misma referencia siempre
ajustes["debug"] = True                             # visible en todo el programa
```

El patrón sobrevive sobre todo en código portado de lenguajes estáticos; en Python su rol como contenedor de estado global lo cubre normalmente un módulo o un objeto creado una vez y reutilizado.
