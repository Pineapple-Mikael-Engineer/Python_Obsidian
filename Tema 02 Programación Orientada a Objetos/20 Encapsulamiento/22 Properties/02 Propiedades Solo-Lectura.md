---
title: Propiedades Solo-Lectura
order: 2
tags:
  - python
  - teoria
  - properties
draft: false
aliases:
  - Propiedad de solo lectura
  - Read-only property
  - Propiedad inmutable
---

# Propiedades de solo-lectura

> [!definicion]
> Una **propiedad de solo-lectura** es una property que define **únicamente el getter** (`@property` sin `@x.setter`). Se puede **leer** (`obj.x`) pero **no asignar**: intentar `obj.x = v` lanza **`AttributeError`**. Sirve para exponer estado interno o valores derivados sin permitir que el usuario los modifique desde fuera.

```python
class Circulo:
    def __init__(self, radio):
        self._radio = radio

    @property
    def radio(self):                  # solo getter, sin setter
        return self._radio

c = Circulo(5)
c.radio            # 5
c.radio = 10       # AttributeError: property 'radio' of 'Circulo' object has no setter
```

Omitir el setter es lo único que se necesita: la property bloquea la escritura por sí sola. El valor sigue viviendo en el atributo de respaldo `_radio`, que la clase puede modificar internamente aunque el exterior no.

## Uso: exponer estado sin permitir su modificación

El patrón típico es **fijar el valor en `__init__`** sobre el atributo de respaldo y exponerlo de solo-lectura. El objeto controla cuándo cambia; el cliente solo observa.

```python
class Transaccion:
    def __init__(self, importe):
        self._importe = importe
        self._id = id(self)           # generado internamente

    @property
    def importe(self):
        return self._importe
    @property
    def id(self):                     # identidad inmutable
        return self._id

t = Transaccion(99)
t.id               # un entero fijo
t.id = 0           # AttributeError -> nadie reescribe la identidad
```

> [!regla]
> Si un atributo no debe cambiar tras la construcción (identificadores, configuración fija, estado derivado), exponlo como property **sin setter**. La inmutabilidad queda garantizada por la API, no por la disciplina del usuario.

> [!warning]
> Es solo-lectura **a través de la property**, no inmutabilidad absoluta: el atributo de respaldo `_radio` sigue siendo accesible y escribible (`c._radio = 10`). El guion bajo lo señala como [[02 Atributos Protegidos (_)]] interno; la barrera es convencional, coherente con la filosofía del [[20 Encapsulamiento/index | encapsulamiento]] en Python.

> [!info]
> El `AttributeError` por falta de setter es distinto del `__slots__` o de los descriptores de datos: aquí el mensaje es explícito —*"has no setter"*—, lo que documenta la intención de solo-lectura.

Cuando el getter, además de no tener setter, **deriva su valor de otros atributos**, estamos ante una [[03 Propiedades Calculadas | propiedad calculada]] (caso muy frecuente de solo-lectura).
