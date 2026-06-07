---
title: Definición de Clases
order: 11
draft: false
description: Definir una clase es declarar un tipo nuevo — la sentencia class, la instanciación, self y __init__
tags:
  - Index
  - Tema
aliases:
  - Definición de Clases
  - Definicion de Clases
---
# Definición de Clases

**Definir una clase es declarar un tipo nuevo** en el programa: un molde a partir del cual se fabrican objetos que comparten estructura (atributos) y comportamiento (métodos). La sentencia `class` ejecuta un bloque de código que produce un objeto-clase; ese objeto, al ser invocado como `Clase(...)`, fabrica **instancias**.

```python
class CuentaBancaria:           # se declara un tipo nuevo
    def __init__(self, saldo):  # inicializa cada instancia
        self.saldo = saldo      # estado propio vía self

c = CuentaBancaria(100)         # instanciación
type(c)                         # <class '__main__.CuentaBancaria'>
```

Esta sección descompone los cuatro elementos mínimos de toda definición. Su resultado —el estado y el comportamiento— se detalla en [[12 Atributos/index | Atributos]] y [[13 Metodos/index | Métodos]].

## Subtemas

- [[01 Sentencia class | Sentencia class]] — `class Nombre:` ejecuta un cuerpo que crea un namespace; la clase es un objeto, instancia de `type`.
- [[02 Instanciacion | Instanciación]] — `obj = Clase(args)` crea una instancia independiente; `__new__` la crea y `__init__` la inicializa.
- [[03 El parametro self | El parámetro self]] — referencia explícita a la instancia; `obj.metodo()` equivale a `Clase.metodo(obj)`.
- [[04 Constructor __init__ | Constructor __init__]] — el inicializador que fija el estado inicial; no devuelve nada.

## Los cuatro elementos

| Elemento | Qué hace | Subtema |
| -------- | -------- | ------- |
| `class Nombre:` | Declara el tipo y crea su namespace | [[01 Sentencia class \| Sentencia class]] |
| `Nombre(args)` | Fabrica una instancia | [[02 Instanciacion \| Instanciación]] |
| `self` | Referencia a la instancia dentro del método | [[03 El parametro self \| El parámetro self]] |
| `__init__(self, ...)` | Inicializa el estado de la instancia | [[04 Constructor __init__ \| Constructor __init__]] |
