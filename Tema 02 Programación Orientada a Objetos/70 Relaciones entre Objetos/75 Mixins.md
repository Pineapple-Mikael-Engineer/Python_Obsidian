---
title: Mixins
order: 75
tags:
  - python
  - teoria
  - relaciones
draft: false
aliases:
  - Mixins
  - Mixin
  - Clase mixin
---

# Mixins

> [!definicion]
> Un **mixin** es una clase **pequeña** que aporta **métodos reutilizables** a otras clases mediante **herencia múltiple**, sin pretender ser una clase base **"es un"** completa. No se **instancia sola**, no representa una entidad del dominio y normalmente **no aporta estado propio** (no define `__init__` ni atributos de instancia): solo **comportamiento** que se "mezcla" en la clase principal.

```python
class JSONSerializableMixin:
    def to_json(self):                       # comportamiento, sin estado
        import json
        return json.dumps(self.__dict__)

class Usuario(JSONSerializableMixin):        # se mezcla en la clase real
    def __init__(self, nombre):
        self.nombre = nombre

Usuario("Ana").to_json()                     # '{"nombre": "Ana"}'
```

`JSONSerializableMixin` no tiene sentido por sí solo —no hay un "JSONSerializable" en el dominio—; existe para **dotar de `to_json()`** a cualquier clase que lo necesite.

## Convención de nombre y diseño

> [!regla]
> - Nombre con sufijo **`XxxMixin`** (`LoggingMixin`, `ComparableMixin`), señalando que **no se instancia**.
> - **Ortogonal y acotado**: aporta **una** capacidad concreta (serializar, comparar, registrar).
> - **No define estado propio** ni `__init__`; asume que la clase anfitriona provee los atributos que sus métodos consultan (aquí, `self.__dict__`).
> - Se coloca **a la izquierda** de las bases (`class C(Mixin, Base)`) para que sus métodos precedan en el MRO.

## Reutilización en varias clases

> [!ejemplo]
> El mismo mixin se mezcla en clases sin relación jerárquica entre sí: ahí está su valor frente a una jerarquía rígida.
>
> ```python
> class JSONSerializableMixin:
>     def to_json(self):
>         import json
>         return json.dumps(self.__dict__)
>
> class Producto(JSONSerializableMixin):
>     def __init__(self, sku): self.sku = sku
>
> class Pedido(JSONSerializableMixin):
>     def __init__(self, n): self.n = n
>
> Producto("A1").to_json()      # '{"sku": "A1"}'
> Pedido(7).to_json()           # '{"n": 7}'
> # Producto y Pedido no comparten linaje, solo la capacidad inyectada
> ```

## Dependencia del MRO y `super()` cooperativo

> [!info]
> Como el mixin entra por **herencia múltiple**, su posición en el orden de resolución decide qué método gana ante colisiones —ver [[03 Herencia Multiple | herencia múltiple]]—. Si el mixin **extiende** comportamiento (en vez de solo añadirlo), debe llamar a `super()` para encadenar al siguiente eslabón del MRO, según el [[02 super() Cooperativo | super() cooperativo]].

```python
class LoggingMixin:
    def guardar(self):
        print("log: guardando")
        return super().guardar()      # delega al siguiente en el MRO

class Repositorio:
    def guardar(self): return "ok"

class RepoLog(LoggingMixin, Repositorio):
    pass

RepoLog().guardar()    # imprime "log: guardando" -> "ok"
[c.__name__ for c in RepoLog.__mro__]
# ['RepoLog', 'LoggingMixin', 'Repositorio', 'object']
```

## Frontera: mixin vs herencia normal vs composición

> [!warning]
> Distinguir el mecanismo según la intención:
> - **Herencia normal ("es un")** — la base es una **entidad completa** del dominio y la subclase **es** un caso suyo (`Perro(Animal)`).
> - **Mixin** — la base **no es** una entidad: solo **inyecta una capacidad** transversal vía herencia múltiple, sin estado.
> - **Composición ("tiene un")** — si la capacidad necesita **estado propio** o configuración, conviene **contener** un colaborador en `self` antes que mezclar una clase. La composición evita la fragilidad del MRO.
>
> Regla práctica: un mixin debe ser **sin estado, ortogonal y opcional**. En cuanto pide guardar datos propios o crece, replantear hacia [[71 Composicion | composición]].
