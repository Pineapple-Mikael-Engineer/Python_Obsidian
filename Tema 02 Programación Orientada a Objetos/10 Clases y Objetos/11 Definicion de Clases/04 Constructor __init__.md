---
title: Constructor __init__
tags:
  - python
  - teoria
  - clases
draft: false
aliases:
  - __init__
  - Inicializador
  - Constructor
---

# Constructor `__init__`

> [!definicion]
> `__init__(self, ...)` es el **inicializador** de una clase: el método que Python ejecuta automáticamente **tras crear** una instancia para fijar su estado inicial. No es el constructor estricto —el objeto ya existe cuando se llama—; el constructor real es `__new__`.

```python
class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular     # estado inicial de la instancia
        self.saldo = saldo

c = CuentaBancaria("Ana", 100)
c.titular, c.saldo                 # ('Ana', 100)
```

## Inicializa, no construye

Cuando se ejecuta `Clase(args)`, primero `__new__` **crea** el objeto vacío y solo después `__init__` lo **inicializa**. Por eso `self` ya existe dentro de `__init__`: el método recibe un objeto ya construido y se limita a poblar sus atributos. La separación de roles se detalla en [[03 __new__ vs __init__ | __new__ vs __init__]].

## No debe devolver nada

> [!warning]
> `__init__` debe devolver `None`. Si retorna cualquier otro valor, Python lanza `TypeError: __init__() should return None`. Su trabajo es mutar `self`, no producir un resultado.

```python
class Mal:
    def __init__(self):
        return 42          # TypeError al instanciar

# Mal()  -> TypeError: __init__() should return None
```

## Argumentos por defecto y validación

`__init__` admite parámetros con valor por defecto y puede ejecutar lógica de validación antes de fijar el estado, levantando una excepción si los datos son inválidos.

```python
class Temperatura:
    def __init__(self, celsius=0):
        if celsius < -273.15:
            raise ValueError("temperatura bajo el cero absoluto")
        self.celsius = celsius

Temperatura(25).celsius     # 25
# Temperatura(-300)         # ValueError
```

## Diferencia con un método normal

`__init__` es un método de instancia ordinario en su firma (recibe `self`), pero se distingue en que **Python lo invoca solo**, una única vez, durante la instanciación. No se suele llamar a mano; un método normal se invoca explícitamente cuando se necesita.

```python
c = CuentaBancaria("Ana")   # __init__ se ejecuta aquí, automáticamente
c.__init__("Beto")          # posible, pero re-inicializa: rara vez deseable
```

## El default mutable

> [!warning]
> Un valor por defecto **mutable** (lista, dict, set) se crea **una sola vez** al definir la función y se comparte entre todas las instancias que no pasen ese argumento. Resultado: estado compartido accidental.

```python
class Carrito:
    def __init__(self, items=[]):    # MAL: lista compartida
        self.items = items

a = Carrito(); a.items.append("pan")
b = Carrito()
b.items                              # ['pan'] -> contaminado por 'a'
```

El patrón correcto usa `None` como centinela y crea un objeto nuevo dentro del cuerpo:

```python
class Carrito:
    def __init__(self, items=None):
        self.items = items if items is not None else []   # nuevo por instancia
```

El estado que `__init__` fija se almacena en `self.__dict__`; su naturaleza (instancia frente a clase) se trata en [[12 Atributos/index | Atributos]].
