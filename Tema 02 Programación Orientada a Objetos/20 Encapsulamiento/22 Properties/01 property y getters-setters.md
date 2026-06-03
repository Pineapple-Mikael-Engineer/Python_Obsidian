---
title: property y getters-setters
tags:
  - python
  - teoria
  - properties
draft: false
aliases:
  - property
  - getter
  - setter
  - deleter
  - "@property"
---

# `property`: getters y setters

> [!definicion]
> **`@property`** transforma un método en el **getter** de un atributo: a partir de ahí `obj.x` ejecuta ese método en lugar de leer un dato. **`@x.setter`** define qué ocurre al **escribir** (`obj.x = v`), el lugar natural para **validar**; **`@x.deleter`** define el borrado (`del obj.x`). El valor real se guarda en un **atributo de respaldo** distinto, por convención `_x`.

```python
class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo            # pasa por el setter -> valida

    @property
    def saldo(self):                  # getter: obj.saldo
        return self._saldo
    @saldo.setter
    def saldo(self, valor):           # setter: obj.saldo = valor
        if valor < 0:
            raise ValueError("saldo negativo")
        self._saldo = valor

c = Cuenta(100)
c.saldo            # 100
c.saldo = 50       # ok
c.saldo = -10      # ValueError: saldo negativo
```

El nombre público es `saldo`; el dato vive en `_saldo`. El getter y el setter **deben** usar el atributo de respaldo `_saldo`, nunca `self.saldo`: escribir `self.saldo = valor` dentro del setter se llamaría a sí mismo y produciría una recursión infinita.

> [!warning]
> Dentro del getter/setter usa siempre el atributo de respaldo (`self._saldo`), **no** el nombre de la property (`self.saldo`). Lo segundo reentra en la property y desemboca en `RecursionError`.

## El patrón del atributo de respaldo `_x`

La property `x` es un **descriptor** a nivel de clase: no almacena nada por instancia. El valor concreto de cada objeto se guarda en un atributo de instancia aparte —`_x`— marcado como [[02 Atributos Protegidos (_)]] para señalar que es uso interno.

```python
class Persona:
    @property
    def edad(self):
        return self._edad            # lee el respaldo
    @edad.setter
    def edad(self, v):
        if v < 0:
            raise ValueError("edad negativa")
        self._edad = v               # escribe el respaldo
```

El `_edad` no se declara en ningún sitio especial: nace la primera vez que el setter le asigna. Por eso `__init__` debe asignar `self.edad = ...` (pasando por el setter y su validación), no `self._edad = ...` directo, salvo que se quiera saltar la validación a propósito.

## Por qué Python prefiere properties a getters/setters explícitos

En Java se escribe desde el principio `getX()` / `setX()` por miedo a tener que añadir validación más tarde sin poder cambiar `obj.x` por `obj.getX()` en todo el código. Python no sufre ese problema:

> [!regla]
> Empieza con un **atributo público normal** (`self.x = x`). Si algún día necesitas validación, cálculo o solo-lectura, **promuévelo a property** con el mismo nombre. `obj.x` y `obj.x = v` siguen funcionando idénticos: la API no se rompe.

```python
# Versión 1: atributo público corriente
class Circulo:
    def __init__(self, radio):
        self.radio = radio

# Versión 2: se promueve a property SIN cambiar cómo se usa
class Circulo:
    def __init__(self, radio):
        self.radio = radio           # mismo __init__
    @property
    def radio(self):
        return self._radio
    @radio.setter
    def radio(self, v):
        if v <= 0:
            raise ValueError("radio positivo")
        self._radio = v
```

El código cliente `c = Circulo(5); c.radio = 8` no cambia ni una letra entre ambas versiones. Por eso en Python se considera **mala práctica** escribir `get_*`/`set_*` por defecto: solo se introduce una property cuando hace falta lógica real.

## `@x.deleter` y forma funcional

El **deleter** controla `del obj.x` (poco frecuente: liberar recursos, invalidar caché):

```python
class Recurso:
    @property
    def datos(self):
        return self._datos
    @datos.deleter
    def datos(self):
        del self._datos              # del r.datos
```

Los decoradores son azúcar sobre el constructor `property(fget, fset, fdel, doc)`. La **forma funcional** es equivalente y útil cuando los métodos ya existen con otro nombre:

```python
class Persona:
    def _get_nombre(self):
        return self._nombre
    def _set_nombre(self, v):
        self._nombre = v.strip().title()

    nombre = property(_get_nombre, _set_nombre)   # getter, setter
```

> [!info]
> `@property` sobre `def x` equivale a `x = property(x)`; cada `@x.setter`/`@x.deleter` devuelve una **copia nueva** de la property con ese accesor añadido y la reasigna a `x`. Por eso los tres métodos deben llamarse igual que la property.

Una property sin setter es de [[02 Propiedades Solo-Lectura | solo-lectura]]; un getter que deriva su valor de otros atributos es una [[03 Propiedades Calculadas | propiedad calculada]].
