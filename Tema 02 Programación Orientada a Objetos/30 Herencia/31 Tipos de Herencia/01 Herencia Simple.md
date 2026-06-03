---
title: Herencia Simple
tags:
  - python
  - teoria
  - herencia
draft: false
aliases:
  - Single inheritance
  - Herencia única
---

# Herencia Simple

> [!definicion]
> La **herencia simple** define una subclase a partir de **una única clase base**: `class Hija(Base):`. La subclase **hereda** todos los atributos y métodos de la base, puede **añadir** miembros propios y **redefinir** (sobrescribir) los heredados. Modela la relación **"es un"**.

```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
    def hablar(self):
        return "..."
    def describir(self):
        return f"{self.nombre} dice {self.hablar()}"

class Perro(Animal):           # una sola base
    def hablar(self):          # redefine (override)
        return "Guau"
    def cobrar(self):          # añade método propio
        return f"{self.nombre} trae la pelota"

p = Perro("Toby")
p.hablar()                     # "Guau"     -> el redefinido
p.describir()                  # "Toby dice Guau"  -> heredado, usa el override
p.cobrar()                     # "Toby trae la pelota"  -> propio
```

`Perro` no declara `__init__`: hereda el de `Animal`, por lo que `Perro("Toby")` inicializa `self.nombre`. Si la subclase necesitara su propio constructor reutilizando el del padre, se invoca con [[01 super() y Constructor del Padre | super().__init__()]].

## Qué se hereda y qué se sombrea

Al resolver `p.metodo`, Python busca primero en la instancia, luego en `Perro.__dict__` y por último en `Animal.__dict__`. La subclase **sombrea** un miembro del padre cuando define uno con el mismo nombre; el original sigue accesible por la clase base.

```python
Perro.hablar is Animal.hablar  # False  -> sombreado
Animal.hablar(p)               # "..."  -> el del padre, accesible explícitamente
```

## Comprobación de tipo y de subclase

> [!regla]
> `isinstance(obj, Clase)` consulta toda la jerarquía: es `True` si `obj` es de `Clase` **o de cualquiera de sus bases**. `issubclass(A, B)` es `True` si `A` deriva de `B` (o es `B`). Ambas son **reflexivas** (una clase es subclase de sí misma).

```python
isinstance(p, Perro)           # True
isinstance(p, Animal)          # True   -> Perro ES un Animal
issubclass(Perro, Animal)      # True
issubclass(Animal, Perro)      # False
issubclass(Perro, Perro)       # True   -> reflexiva
```

## Todo hereda de object

> [!info]
> En Python 3 toda clase deriva **implícitamente** de `object`, aunque no se declare. `object` aporta el comportamiento por defecto: `__init__`, `__str__`, `__eq__`, `__hash__`, etc. Por eso `class Animal:` equivale a `class Animal(object):`.

```python
issubclass(Animal, object)     # True
isinstance(p, object)          # True  -> toda instancia es un object
Perro.__bases__                # (<class '__main__.Animal'>,)
Animal.__bases__               # (<class 'object'>,)
```

La cadena `Perro → Animal → object` es ya un caso de [[02 Herencia Multinivel | herencia multinivel]] implícita: `object` cierra siempre el linaje. Con un solo padre directo el orden de búsqueda es lineal y no presenta ambigüedad, a diferencia de la [[03 Herencia Multiple | herencia múltiple]].
