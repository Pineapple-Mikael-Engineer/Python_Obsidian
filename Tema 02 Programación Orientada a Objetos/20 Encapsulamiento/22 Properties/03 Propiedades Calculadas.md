---
title: Propiedades Calculadas
order: 3
tags:
  - python
  - teoria
  - properties
draft: false
aliases:
  - Propiedad calculada
  - Propiedad derivada
  - Computed property
  - cached_property
---

# Propiedades calculadas

> [!definicion]
> Una **propiedad calculada** es una property cuyo getter **computa el valor en cada acceso** a partir de otros atributos del objeto, en vez de almacenarlo. No tiene atributo de respaldo propio: su resultado es siempre función del estado actual, por lo que **nunca queda desincronizado**.

```python
import math

class Circulo:
    def __init__(self, radio):
        self.radio = radio            # único dato almacenado

    @property
    def area(self):                   # se calcula al pedirla
        return math.pi * self.radio ** 2

c = Circulo(2)
c.area             # 12.566...
c.radio = 3
c.area             # 28.274...  -> coherente sin tocar nada más
```

`area` no se guarda: se deriva de `radio` cada vez que se lee. Cambiar `radio` actualiza `area` automáticamente. Suele ser de [[02 Propiedades Solo-Lectura | solo-lectura]] (sin setter), porque su valor no es un dato propio sino el reflejo de otros.

## Ventaja: consistencia garantizada

La alternativa —guardar `area` como atributo y recalcularla a mano cada vez que cambia `radio`— es frágil: cualquier camino que modifique `radio` y olvide actualizar `area` deja el objeto en un estado **incoherente**. La propiedad calculada elimina ese riesgo de raíz porque no hay nada que sincronizar.

```python
class Persona:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

p = Persona("Ada", "Lovelace")
p.nombre_completo          # 'Ada Lovelace'
p.apellido = "Byron"
p.nombre_completo          # 'Ada Byron'  -> siempre al día
```

> [!regla]
> Si un valor **se puede deducir** de otros atributos, expónlo como propiedad calculada en lugar de almacenarlo. Una sola fuente de verdad (los atributos base) evita estados contradictorios.

## Coste: se recalcula en cada acceso

El precio es que el cálculo se repite **en cada lectura**. Para fórmulas baratas es irrelevante; si el cómputo es caro (consultas, sumas sobre colecciones grandes) y el resultado **no cambia mientras vivan sus dependencias**, conviene **cachear** con `functools.cached_property`: calcula una vez, guarda el resultado en el `__dict__` de la instancia y lo reutiliza.

```python
from functools import cached_property

class Dataset:
    def __init__(self, datos):
        self.datos = datos

    @cached_property
    def media(self):                  # se calcula UNA vez por instancia
        print("calculando...")
        return sum(self.datos) / len(self.datos)

d = Dataset([1, 2, 3])
d.media            # 'calculando...' -> 2.0
d.media            # 2.0  (sin recalcular: viene de la caché)
```

> [!warning]
> `cached_property` **no se invalida solo**: si cambian las dependencias (`d.datos`), el valor cacheado queda obsoleto. Hay que borrarlo a mano (`del d.media`) para forzar el recálculo. Úsalo solo cuando las dependencias sean estables tras la construcción. Además requiere que la instancia tenga `__dict__` (incompatible con `__slots__` sin entrada extra).

> [!info]
> `@property` y `@cached_property` se eligen según el balance coste/frescura: `property` cuando el cálculo es barato o las dependencias mutan; `cached_property` cuando es caro y las dependencias quedan fijas.
