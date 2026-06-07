---
title: __new__ vs __init__
order: 93
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - __new__
  - Creacion vs inicializacion
---

# __new__ vs __init__

> [!definicion]
> `__new__(cls, ...)` es el **constructor real**: recibe la **clase** (`cls`), **crea** la instancia y la **devuelve**. `__init__(self, ...)` es el **inicializador**: recibe la instancia **ya creada** (`self`) y le asigna su estado, sin devolver nada. La creación y la inicialización son pasos separados.

```python
class Demo:
    def __new__(cls, *args):
        print("1) __new__  -> crea")
        return super().__new__(cls)     # delega la creación real a object
    def __init__(self, x):
        print("2) __init__ -> inicializa")
        self.x = x

Demo(5)
# 1) __new__  -> crea
# 2) __init__ -> inicializa
```

## Secuencia de instanciación

`Clase(args)` no llama a `__init__` directamente: el protocolo es

```text
Clase(args)
   └─► type.__call__:
          inst = Clase.__new__(Clase, args)     # crea
          if isinstance(inst, Clase):
              inst.__init__(args)                # inicializa
          return inst
```

La forma habitual de instanciar y el rol de `__init__` se tratan en [[02 Instanciacion | Instanciación]] y [[04 Constructor __init__ | el constructor __init__]]; `__new__` es la fase previa que normalmente no se sobrescribe.

> [!warning]
> `__new__` **debe devolver una instancia de `cls`** (normalmente vía `super().__new__(cls)`). Si devuelve otra cosa —u olvida el `return`, devolviendo `None`— Python **no llama a `__init__`** y el objeto queda sin inicializar. Esta es la causa de error más común al sobrescribir `__new__`.

## Cuándo sobrescribir `__new__`

La mayoría de las clases solo necesitan `__init__`. Sobrescribir `__new__` se justifica en casos donde hay que intervenir **antes** de que el objeto exista:

### Subclasear tipos inmutables

En `int`, `str`, `tuple`, `float` el valor se fija en la **creación**; al llegar a `__init__` el objeto ya es inmutable y no se puede modificar. La personalización debe ocurrir en `__new__`.

```python
class Positivo(int):
    def __new__(cls, valor):
        if valor < 0:
            raise ValueError("debe ser >= 0")
        return super().__new__(cls, valor)   # fija el valor inmutable

Positivo(5) + 1     # 6   (se comporta como int)
Positivo(-1)        # ValueError
```

### Singleton

`__new__` puede devolver **siempre la misma** instancia almacenada en la clase:

```python
class Config:
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

Config() is Config()    # True   -> una única instancia
```

> [!info]
> Con el singleton, `__init__` se ejecuta **en cada llamada** a `Config()`, sobre la misma instancia ya existente. Si reinicializa estado, hay que protegerlo (p. ej. con una bandera) para no sobrescribir lo anterior.

### Fábrica que devuelve otra clase

`__new__` puede devolver una instancia de una **subclase distinta** según los argumentos, centralizando la elección del tipo concreto.

```python
class Figura:
    def __new__(cls, lados):
        if cls is Figura:
            objetivo = Triangulo if lados == 3 else Cuadrado
            return super().__new__(objetivo)
        return super().__new__(cls)

class Triangulo(Figura): pass
class Cuadrado(Figura): pass

type(Figura(3))     # <class 'Triangulo'>
```

> [!regla]
> Inicializar estado normal → `__init__`. Intervenir en la **identidad o el tipo** del objeto (inmutables, singletons, fábricas, *caching* de instancias) → `__new__`, y siempre devolviendo una instancia válida.
