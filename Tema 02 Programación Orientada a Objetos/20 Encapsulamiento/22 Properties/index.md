---
title: 22 Properties
draft: false
description: Acceso de atributo respaldado por métodos sin cambiar la sintaxis
tags:
  - Index
  - Tema
aliases:
  - Properties
  - Propiedades
  - property
---
# Properties

Una **property** convierte el acceso a un atributo en **llamadas a métodos** sin que la sintaxis del usuario cambie: `obj.x` se sigue leyendo y escribiendo igual, pero por detrás se ejecuta un *getter*, un *setter* o un *deleter*. Es el mecanismo con el que Python ofrece **acceso controlado** —validación, solo-lectura, valores calculados— manteniendo intacta la API pública.

```python
class Temperatura:
    def __init__(self, celsius):
        self.celsius = celsius        # invoca el setter, valida

    @property
    def celsius(self):                # getter
        return self._celsius
    @celsius.setter
    def celsius(self, valor):         # setter con validación
        if valor < -273.15:
            raise ValueError("bajo el cero absoluto")
        self._celsius = valor

t = Temperatura(20)
t.celsius          # 20      -> ejecuta el getter
t.celsius = 25     #         -> ejecuta el setter
```

La ventaja decisiva: un atributo público puede **promoverse** a property más tarde sin romper a quien ya usa `obj.x`. No hay que cambiar la sintaxis de acceso en ningún sitio.

## Subtemas

- [[01 property y getters-setters | property y getters/setters]] — definir getter, setter y deleter; el atributo de respaldo `_x`; por qué Python prefiere properties a getters/setters explícitos.
- [[02 Propiedades Solo-Lectura | Propiedades Solo-Lectura]] — solo getter: asignar lanza `AttributeError`. Para estado derivado inmutable.
- [[03 Propiedades Calculadas | Propiedades Calculadas]] — el getter computa el valor en cada acceso a partir de otros atributos; siempre consistente.

## Las tres operaciones de una property

| Operación | Decorador | Se dispara con | Sin ella |
| --------- | --------- | -------------- | -------- |
| Leer | `@property` | `obj.x` | no hay property |
| Escribir | `@x.setter` | `obj.x = v` | property de solo-lectura (`AttributeError` al asignar) |
| Borrar | `@x.deleter` | `del obj.x` | `del obj.x` lanza `AttributeError` |

El `@property` (getter) es obligatorio; `setter` y `deleter` son opcionales. Omitir el setter es justamente lo que produce una propiedad de [[02 Propiedades Solo-Lectura | solo-lectura]].

Las properties son la cara visible del [[20 Encapsulamiento/index | encapsulamiento]]: respaldan la interfaz controlada apoyándose en [[02 Atributos Protegidos (_)]] como almacenamiento interno.
