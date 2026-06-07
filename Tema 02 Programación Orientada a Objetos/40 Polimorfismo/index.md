---
title: Polimorfismo
order: 40
draft: false
description: Una misma interfaz, comportamientos distintos según el objeto
tags:
  - Index
  - Tema
aliases:
  - Polimorfismo
  - Polymorphism
---
# Polimorfismo

El **polimorfismo** es la capacidad de que una misma operación o interfaz produzca comportamientos distintos según el tipo del objeto sobre el que actúa. El código cliente invoca un método sin conocer la clase concreta; cada objeto responde a su manera. Es lo que permite escribir funciones genéricas que operan sobre familias enteras de objetos.

```python
def imprimir_sonido(animal):
    print(animal.hablar())     # no le importa la clase concreta

for a in [Perro(), Gato(), Vaca()]:
    imprimir_sonido(a)         # Guau / Miau / Muu
```

En Python el polimorfismo no exige una jerarquía de herencia común: basta con que los objetos **compartan la interfaz** (los métodos que se van a usar). Esto es el *duck typing*.

## Subtemas

- [[41 Duck Typing | Duck Typing]] — *"si camina como un pato y grazna como un pato, es un pato"*: la compatibilidad se juzga por comportamiento, no por tipo.
- [[42 Polimorfismo de Subtipos | Polimorfismo de Subtipos]] — el polimorfismo clásico vía herencia y [[32 Mecanismos de Herencia/index | sobrescritura]] de métodos.
- [[43 Sobrecarga de Operadores | Sobrecarga de Operadores]] — dar significado a `+`, `==`, `<`… para objetos propios mediante [[50 Metodos Especiales (Dunder)/index | métodos especiales]].

## Formas de polimorfismo en Python

| Forma | Mecanismo | Subtema |
| ----- | --------- | ------- |
| *Duck typing* | Interfaz compartida, sin herencia | [[41 Duck Typing \| Duck Typing]] |
| De subtipos | Herencia + sobrescritura | [[42 Polimorfismo de Subtipos \| Polimorfismo de Subtipos]] |
| De operadores | Métodos dunder (`__add__`, `__eq__`…) | [[43 Sobrecarga de Operadores \| Sobrecarga de Operadores]] |

Python **no** ofrece *overloading* por firma (varias funciones con el mismo nombre y distintos parámetros) como C++/Java; ese papel lo cubren los argumentos por defecto, `*args`/`**kwargs` y `functools.singledispatch`.
