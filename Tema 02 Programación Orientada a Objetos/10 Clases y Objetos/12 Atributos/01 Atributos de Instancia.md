---
title: Atributos de Instancia
order: 1
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - Instance attributes
  - Atributos de objeto
---

# Atributos de Instancia

> [!definicion]
> Un **atributo de instancia** pertenece a **un objeto concreto**, no a la clase. Cada instancia mantiene su propia copia, independiente de las demás. Se crean asignando a `self.nombre` dentro de un método —normalmente el constructor [[04 Constructor __init__ | `__init__`]]— y se almacenan en el `__dict__` de esa instancia.

```python
class Punto:
    def __init__(self, x, y):
        self.x = x        # atributo de instancia
        self.y = y

p = Punto(3, 4)
p.x, p.y                  # 3, 4
```

Cada llamada a `Punto(...)` produce un objeto con su propio `x` y su propio `y`. Modificar el de uno no afecta al otro.

## Independencia entre instancias

El estado de cada objeto es **aislado**: dos instancias de la misma clase pueden tener valores totalmente distintos para los mismos atributos.

```python
a = Punto(1, 1)
b = Punto(9, 9)
a.x = 100                 # solo cambia 'a'
a.x, b.x                  # 100, 9  -> 'b' intacto
```

Esta independencia es justo lo que distingue a un atributo de instancia de uno [[02 Atributos de Clase | de clase]], que sí es compartido.

## Creación: `__init__` no es obligatorio

Aunque lo habitual es fijar el estado en el constructor, un atributo de instancia se crea en el momento de la **primera asignación a `self.x`**, ocurra en el método que ocurra.

```python
class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo

    def aplicar_interes(self, tasa):
        self.interes = self.saldo * tasa   # se crea aquí, no en __init__

c = Cuenta(1000)
# c.interes  ->  AttributeError: aún no existe
c.aplicar_interes(0.05)
c.interes                                  # 50.0  -> ya existe
```

> [!warning]
> Crear atributos fuera de `__init__` provoca que una instancia tenga o no cierto atributo según qué métodos se hayan llamado, lo que rompe la uniformidad y dispara `AttributeError`. Conviene declarar **todos** los atributos esperados en `__init__` (con un valor inicial, p. ej. `None`) y reservar otras asignaciones para mutar lo ya existente.

## Almacenamiento en `__dict__`

Los atributos de instancia viven en un diccionario propio del objeto, accesible como `obj.__dict__`. Asignar `self.x = v` equivale a `obj.__dict__['x'] = v`.

```python
p = Punto(3, 4)
p.__dict__                # {'x': 3, 'y': 4}
```

Como es un `dict` editable, el conjunto de atributos de una instancia no es fijo: puede ampliarse o reducirse en ejecución. Ese carácter dinámico, junto con `getattr`/`setattr`/`vars()`, se desarrolla en [[03 Atributos Dinamicos y __dict__ | Atributos Dinámicos y __dict__]].
