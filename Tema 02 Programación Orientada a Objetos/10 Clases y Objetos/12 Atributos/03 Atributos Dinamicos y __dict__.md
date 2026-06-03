---
title: Atributos Dinámicos y __dict__
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - Atributos Dinamicos
  - __dict__
  - getattr setattr hasattr delattr
---

# Atributos Dinámicos y `__dict__`

> [!definicion]
> Los objetos de Python son **dinámicos**: se pueden **añadir** y **quitar** atributos en tiempo de ejecución, sin que la clase los haya declarado. Todo el estado de instancia se guarda en `obj.__dict__`, un **diccionario editable** cuyas claves son los nombres de atributo. Manipular ese `dict` —directa o indirectamente— equivale a manipular los atributos.

```python
class Vacia:
    pass

o = Vacia()
o.color = "rojo"          # se crea un atributo nuevo en ejecución
o.__dict__                # {'color': 'rojo'}
del o.color               # se elimina
o.__dict__                # {}
```

## `__dict__` y `vars()`

`obj.__dict__` es el almacén real de los atributos de instancia. `vars(obj)` devuelve ese mismo diccionario y es la forma idiomática de inspeccionarlo.

```python
class P:
    def __init__(self, x, y):
        self.x, self.y = x, y

p = P(1, 2)
vars(p)                   # {'x': 1, 'y': 2}
vars(p) is p.__dict__     # True

p.__dict__['z'] = 3       # asignar por el dict equivale a p.z = 3
p.z                       # 3
```

## Acceso por nombre: `getattr / setattr / hasattr / delattr`

Cuando el nombre del atributo está en una variable (no escrito literalmente), se usan las funciones integradas. Reciben el nombre como **cadena**.

| Función | Acción | Equivale a |
| ------- | ------ | ---------- |
| `getattr(obj, "x")` | Lee el atributo | `obj.x` |
| `getattr(obj, "x", def)` | Lee con valor por defecto si no existe | — |
| `setattr(obj, "x", v)` | Asigna el atributo | `obj.x = v` |
| `hasattr(obj, "x")` | ¿Existe el atributo? | — |
| `delattr(obj, "x")` | Elimina el atributo | `del obj.x` |

```python
p = P(1, 2)
campo = "x"
getattr(p, campo)              # 1
setattr(p, "w", 9)             # p.w = 9
hasattr(p, "w")                # True
getattr(p, "falta", None)      # None  -> sin error gracias al default
delattr(p, "w")                # elimina p.w
```

> [!info]
> `getattr` con tercer argumento es la vía segura para leer un atributo que puede no existir, evitando el `AttributeError`. Es preferible a comprobar con `hasattr` y luego leer, porque hace una sola búsqueda.

## Relación con la resolución de atributos

`__dict__` solo contiene los atributos **de instancia**. Un atributo [[02 Atributos de Clase | de clase]] no aparece en `obj.__dict__` aunque `obj.x` lo lea correctamente, porque la búsqueda continúa en `Clase.__dict__`.

```python
class C:
    cls_attr = "compartido"

o = C()
o.inst_attr = "propio"
o.__dict__                 # {'inst_attr': 'propio'}  -> sin 'cls_attr'
o.cls_attr                 # "compartido"  -> resuelto en C.__dict__
```

## `__slots__`: fijar atributos y eliminar `__dict__`

> [!warning]
> Definir `__slots__` en la clase **elimina el `__dict__` por instancia** y prohíbe crear atributos no declarados: aporta velocidad y ahorra memoria a costa de perder el dinamismo.

```python
class Punto:
    __slots__ = ("x", "y")     # solo estos atributos permitidos
    def __init__(self, x, y):
        self.x, self.y = x, y

p = Punto(1, 2)
# p.z = 3   ->  AttributeError: 'Punto' object has no attribute 'z'
# p.__dict__ ->  AttributeError: no existe __dict__
```

El detalle de `__slots__` —sintaxis, herencia y limitaciones— se trata en [[90 Herramientas Modernas/index | Herramientas Modernas]].
