---
title: Privados y Name Mangling (__)
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - Name mangling
  - Atributos privados
  - Doble guion bajo
---

# Privados y Name Mangling (__)

> [!definicion]
> Un atributo con **dos guiones bajos iniciales** y que **no termina** en dos guiones bajos (`__nombre`) activa el **name mangling**: dentro de una clase `Clase`, Python renombra `__nombre` a `_Clase__nombre`. El objetivo **no es la seguridad**, sino **evitar colisiones de nombres** entre una clase base y sus subclases. El atributo sigue siendo accesible si se usa el nombre renombrado.

```python
class Cuenta:
    def __init__(self):
        self.__pin = 1234         # se almacena como _Cuenta__pin

c = Cuenta()
c.__pin                           # AttributeError: 'Cuenta' object has no attribute '__pin'
c._Cuenta__pin                    # 1234   -> el nombre real
```

## Demostración con `__dict__`

El renombrado ocurre al definir la clase. En el diccionario de la instancia el nombre aparece ya transformado, lo que delata que **no hay ocultación real**, solo un nombre distinto.

```python
c.__dict__                        # {'_Cuenta__pin': 1234}
```

## Para qué sirve: evitar colisiones en herencia

El caso de uso real es proteger un atributo de la clase base frente a que una **subclase** defina, sin saberlo, otro con el mismo nombre. Como cada `__nombre` se decora con el nombre de **su** clase, base y subclase obtienen entradas **separadas** en `__dict__`.

```python
class Base:
    def __init__(self):
        self.__dato = "base"      # -> _Base__dato
    def ver_base(self):
        return self.__dato        # resuelve a _Base__dato

class Sub(Base):
    def __init__(self):
        super().__init__()
        self.__dato = "sub"       # -> _Sub__dato  (NO pisa al de Base)
    def ver_sub(self):
        return self.__dato        # resuelve a _Sub__dato

s = Sub()
s.ver_base()                      # "base"   intacto
s.ver_sub()                       # "sub"
s.__dict__                        # {'_Base__dato': 'base', '_Sub__dato': 'sub'}
```

Sin *name mangling*, ambos `__init__` escribirían el mismo `self.__dato` y la subclase **machacaría** el dato de la base.

> [!warning]
> El *name mangling* **no es privacidad real**: el atributo sigue siendo accesible desde fuera como `obj._Clase__nombre`. No lo uses esperando seguridad ni para ocultar secretos; su único propósito legítimo es evitar choques de nombres en jerarquías. Para un acceso controlado de verdad, usa [[22 Properties/index | Properties]].

## No confundir con los dunder `__x__`

Los nombres que **empiezan y terminan** en dos guiones bajos (los *dunder*: `__init__`, `__str__`, `__dict__`) **no sufren mangling**. El renombrado solo aplica a nombres con **dos guiones bajos al inicio y como mucho uno al final**.

```python
class C:
    def __init__(self):
        self.__x = 1              # mangled  -> _C__x
        self.__y__ = 2            # dunder    -> queda como __y__ (sin tocar)

C().__dict__                      # {'_C__x': 1, '__y__': 2}
```

> [!regla]
> `__nombre` (sin cierre dunder) -> *name mangling*, para colisiones en herencia. `__nombre__` -> protocolo del lenguaje, sin mangling, **no inventes** los tuyos. Si solo quieres marcar "uso interno", basta con [[02 Atributos Protegidos (_) | un guion bajo]].
