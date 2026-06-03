---
title: Atributos Protegidos (_)
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - Protected attributes
  - Atributos protegidos
  - Guion bajo simple
---

# Atributos Protegidos (_)

> [!definicion]
> Un atributo con **un solo guion bajo inicial** (`_nombre`) señala, por **convención**, que es de **uso interno**: no forma parte de la API pública y no debería tocarse desde fuera de la clase (ni desde subclases salvo con cuidado). Python **no impide** el acceso; el guion bajo es únicamente una **señal de intención** dirigida a quien lee el código.

```python
class Cuenta:
    def __init__(self, saldo):
        self._saldo = saldo       # "protegido" por convención

c = Cuenta(100)
c._saldo                          # 100  -> accesible: Python NO lo bloquea
```

## Es convención, no barrera

A diferencia del doble guion bajo, `_nombre` **no sufre ningún renombrado**. El nombre queda literal en `__dict__` y se accede con normalidad. Lo único que cambia es el **mensaje al lector**: "esto es detalle de implementación, puede cambiar sin aviso, no dependas de ello".

```python
c.__dict__                        # {'_saldo': 100}  -> el nombre es literal
```

> [!regla]
> Marca con `_` lo que no quieres que el código cliente use directamente: atributos auxiliares, cachés, estado intermedio o el almacén real detrás de una [[22 Properties/index | property]] (el típico `self._x` que respalda a `x`).

## Efecto en `from modulo import *`

El guion bajo inicial sí tiene **un efecto técnico** a nivel de módulo: `from modulo import *` **no importa** los nombres que empiezan por `_` (salvo que el módulo defina `__all__` y los incluya explícitamente).

```python
# utilidades.py
def publica(): ...
def _interna(): ...

# otro_archivo.py
from utilidades import *
publica()                         # OK
_interna()                        # NameError: no se importó
```

> [!info]
> Este filtrado aplica a **funciones, variables y clases de nivel de módulo**, no a los atributos de instancia. Es el mismo guion bajo expresando la misma idea ("privado del módulo") en otro contexto.

## Uso en clases base pensadas para herencia

En una jerarquía, `_nombre` marca el estado que la clase base comparte **hacia abajo** (con sus subclases) pero **no hacia afuera** (con el código cliente). Las subclases pueden leer y escribir `_nombre` porque participan de la implementación; el usuario externo, no.

```python
class Vehiculo:
    def __init__(self, velocidad):
        self._velocidad = velocidad      # compartido con subclases

class Coche(Vehiculo):
    def acelerar(self):
        self._velocidad += 10            # la subclase lo usa con libertad
```

Por eso `_nombre` se prefiere al doble guion bajo en clases diseñadas para [[03 Privados y Name Mangling (__) | extenderse]]: el *name mangling* del `__nombre` complicaría que las subclases accedan al atributo. El nivel realmente sin restricción es el de los [[01 Atributos Publicos | atributos públicos]].
