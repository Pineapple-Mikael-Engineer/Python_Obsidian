---
title: __slots__
order: 92
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - slots
  - Atributos fijos
---

# __slots__

> [!definicion]
> Declarar `__slots__` en el cuerpo de la clase fija el **conjunto cerrado de atributos de instancia** permitidos. Las instancias dejan de tener `__dict__`: cada atributo se almacena en una ranura (*slot*) de tamaño fijo, como los campos de una estructura en C. Consecuencias: **no se pueden añadir atributos** fuera de la lista, y se **ahorra memoria** de forma significativa al eliminar el diccionario por instancia.

```python
class Punto:
    __slots__ = ('x', 'y')      # solo estos dos atributos
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punto(1, 2)
p.x                 # 1
p.__dict__          # AttributeError: 'Punto' object has no attribute '__dict__'
```

## Atributos fijos: el error de asignación

Asignar un atributo no declarado **falla** en vez de crearse silenciosamente. Sin `__slots__`, el [[03 Atributos Dinamicos y __dict__ | almacenamiento dinámico en __dict__]] aceptaría cualquier nombre.

```python
p.z = 3             # AttributeError: 'Punto' object has no attribute 'z'
```

> [!info]
> Este rechazo es un beneficio colateral: convierte un *typo* (`p.nombre` en vez de `p.nombre_`) en un error inmediato en lugar de crear un atributo basura que pasa desapercibido.

## Ahorro de memoria

El `__dict__` por instancia es un objeto pesado (decenas de bytes más su carga de tabla hash). Con `__slots__` los valores se guardan directamente en el objeto, contiguos.

```python
import sys

class ConDict:                  # instancia normal: tiene __dict__
    def __init__(self, x, y):
        self.x, self.y = x, y

class ConSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x, self.y = x, y

sys.getsizeof(ConDict(1, 2).__dict__)   # ~104 bytes SOLO el dict
# ConSlots no tiene __dict__: las dos ranuras viven en el objeto
```

> [!ejemplo]
> Con **millones** de instancias pequeñas (puntos, nodos de grafo, registros) el ahorro acumulado del `__dict__` eliminado es del orden de **40-50 %** de memoria por instancia. Es la motivación principal de `__slots__`: no la velocidad, sino la huella en memoria a gran escala.

## Costes y restricciones

> [!warning]
> `__slots__` introduce limitaciones que lo hacen inadecuado por defecto:
> - **Sin atributos dinámicos:** se pierde la flexibilidad de añadir atributos en caliente (ver [[03 Atributos Dinamicos y __dict__ \| Atributos Dinámicos y __dict__]]). Código que dependa de inyectar atributos arbitrarios se rompe.
> - **Herencia:** si una subclase **no** declara `__slots__`, sus instancias **recuperan** el `__dict__` y se anula el ahorro. Para conservarlo, cada clase de la jerarquía debe declarar sus propios slots (solo los nuevos, no repetir los heredados).
> - **Herencia múltiple:** combinar dos clases base que definen `__slots__` no vacíos lanza `TypeError` (conflicto de *layout*). Es la restricción más espinosa.
> - Sin `__weakref__` en los slots, las instancias **no** admiten referencias débiles; hay que añadirlo explícitamente: `__slots__ = ('x', '__weakref__')`.

## Slots vacíos y dataclasses

`__slots__ = ()` (tupla vacía) no añade atributos pero **sigue eliminando** el `__dict__`: útil en clases puramente de comportamiento o mixins sin estado, para que no acepten atributos accidentales.

Un dataclass genera sus slots automáticamente con `@dataclass(slots=True)` (Python 3.10+), evitando escribir a mano la tupla y mantenerla sincronizada con los campos (ver [[91 Dataclasses | Dataclasses]]).

> [!regla]
> Activar `__slots__` solo cuando el perfilado muestre que las instancias dominan la memoria del programa. En clases ordinarias, el coste en flexibilidad y la fragilidad ante la herencia no compensan el ahorro.
