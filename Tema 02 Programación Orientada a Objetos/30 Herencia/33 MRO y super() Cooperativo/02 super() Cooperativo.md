---
title: super() Cooperativo
tags:
  - python
  - teoria
  - herencia
draft: false
aliases:
  - Cooperative super
  - Herencia cooperativa
  - Mixins cooperativos
---

# super() Cooperativo

> [!definicion]
> En herencia múltiple, `super()` **no** llama "al padre" sino al **siguiente en el MRO** del objeto real. Si cada clase de una cadena delega con `super().metodo(...)`, la llamada **recorre todo el MRO** y cada clase ejecuta su parte **exactamente una vez**. A esto se le llama **herencia cooperativa**: las clases colaboran sin saber quién va después de ellas.

```python
class A:
    def saludar(self): return "A"
class B(A):
    def saludar(self): return "B+" + super().saludar()
class C(A):
    def saludar(self): return "C+" + super().saludar()
class D(B, C):
    def saludar(self): return "D+" + super().saludar()

D().saludar()     # "D+B+C+A"  -> recorre el MRO (D, B, C, A)
```

En `B`, `super()` se resuelve **dinámicamente** según el MRO de la instancia: para un `D()`, el siguiente de `B` no es `A` sino `C`. Por eso `B` cede a `C` aunque `B` herede directamente de `A`.

## La regla de la cadena

Para que la cooperación funcione, **todas** las clases de la cadena deben:

- **Llamar a `super().metodo(...)`** para no cortar el recorrido.
- Usar **firmas compatibles**. Como cada clase no sabe qué clase la sigue, lo idiomático es propagar argumentos con `**kwargs` y que la cima de la jerarquía (`object` o una base común) los consuma.

```python
class Base:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   # llega a object con kwargs vacíos

class ConLog(Base):
    def __init__(self, *, log=True, **kwargs):
        self.log = log
        super().__init__(**kwargs)   # pasa el resto al SIGUIENTE del MRO

class ConCache(Base):
    def __init__(self, *, cache=10, **kwargs):
        self.cache = cache
        super().__init__(**kwargs)

class Servicio(ConLog, ConCache):
    pass

s = Servicio(log=False, cache=50)    # cada mixin toma SU kwarg y reenvía el resto
s.log, s.cache                        # (False, 50)
[k.__name__ for k in Servicio.__mro__]
# ['Servicio', 'ConLog', 'ConCache', 'Base', 'object']
```

Cada *mixin* extrae su propio parámetro por nombre y reenvía el resto; el MRO garantiza que `ConLog` y `ConCache` se inicialicen **una sola vez** cada uno, sin que ninguno conozca al otro.

## Romper la cadena

> [!warning]
> Si una clase intermedia **no llama a `super()`** (por ejemplo, invoca directamente `Base.__init__(self)` o simplemente no delega), corta el recorrido del MRO: las clases que vendrían **después** de ella nunca se ejecutan y se **pierde su comportamiento** de forma silenciosa.

```python
class ConCacheRoto(Base):
    def __init__(self, *, cache=10, **kwargs):
        self.cache = cache
        # falta super().__init__(**kwargs)  -> corta la cadena

class Servicio(ConLog, ConCacheRoto):
    pass

# El MRO sería [Servicio, ConLog, ConCacheRoto, Base, object],
# pero como ConCacheRoto no delega, Base.__init__ no se invoca a través suyo.
```

Esta es la diferencia clave con [[01 super() y Constructor del Padre | super() en constructor]]: en herencia simple basta llamar al padre, pero en una cadena cooperativa **toda** clase debe delegar, porque "el padre" lo decide el MRO completo y no la relación directa. El orden exacto que recorre `super()` es el [[01 MRO (Method Resolution Order) | MRO]], y este patrón es el que sostiene los [[05 Mixins | Mixins]].
</content>
