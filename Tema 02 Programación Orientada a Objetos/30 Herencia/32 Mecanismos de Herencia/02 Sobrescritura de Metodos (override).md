---
title: Sobrescritura de Métodos (override)
tags:
  - python
  - teoria
  - herencia
draft: false
aliases:
  - Override
  - Sobrescritura
  - Method Overriding
---

# Sobrescritura de Métodos (*override*)

> [!definicion]
> La **sobrescritura** (*override*) ocurre cuando una subclase **redefine** un método heredado con el **mismo nombre y la misma firma**. Al invocar el método sobre una instancia de la subclase, gana la versión de la subclase: la del padre queda **eclipsada** (aunque sigue accesible vía [[01 super() y Constructor del Padre | super()]]). Es el mecanismo que sustenta el [[40 Polimorfismo/index | polimorfismo]] de subtipos.

```python
class Animal:
    def hablar(self):
        return "..."

class Perro(Animal):
    def hablar(self):          # sobrescribe Animal.hablar
        return "Guau"

class Gato(Animal):
    def hablar(self):          # sobrescribe Animal.hablar
        return "Miau"

Perro().hablar()               # "Guau"
Gato().hablar()                # "Miau"
Animal().hablar()              # "..."
```

La resolución es por **clase real** del objeto: Python busca `hablar` empezando en la clase de la instancia y subiendo por la cadena de herencia hasta el primer acierto. Si la subclase lo define, nunca se llega al del padre.

## Base del polimorfismo

Una función que opera sobre el tipo base funciona sin cambios para cualquier subclase que sobrescriba el método: cada objeto responde con su propia versión.

```python
def coro(animales):
    return [a.hablar() for a in animales]

coro([Perro(), Gato(), Animal()])   # ['Guau', 'Miau', '...']
```

> [!info]
> El emisor (`coro`) no conoce las subclases concretas; solo el contrato `hablar()`. Añadir un nuevo `Animal` con su propio `hablar` no obliga a tocar `coro`. Este desacople es el núcleo del [[40 Polimorfismo/index | polimorfismo]] y de la sustituibilidad de Liskov.

## Firma compatible

El *override* exige conservar la **firma** del método (mismo nombre, parámetros compatibles) para que el código que llama al tipo base siga siendo válido sobre la subclase. Cambiar el nombre no es sobrescribir: crea un método **nuevo** que no participa del despacho polimórfico.

> [!regla]
> Sobrescribir = mismo nombre + firma compatible. Si la subclase necesita parámetros extra obligatorios, está rompiendo el contrato del padre y probablemente la relación no es **"es un"**, sino [[70 Relaciones entre Objetos/index | composición]].

## Override total vs. extensión

Sobrescribir **sin** llamar a `super()` reemplaza el comportamiento por completo. Sobrescribir **llamando** a `super().metodo()` y añadiendo código es la [[03 Extension de Metodos | extensión]]: un *override* parcial que reutiliza al padre en lugar de descartarlo.

```python
class Perro(Animal):
    def hablar(self):
        return super().hablar() + " Guau"   # extensión, no reemplazo total
```

## Override no es overloading

Python **no tiene sobrecarga** (*overloading*) en el sentido clásico de C++/Java: no se pueden declarar varias versiones de un método distinguidas por el número o tipo de argumentos. Definir dos métodos con el mismo nombre en una clase no crea variantes; el segundo **reemplaza** al primero en el espacio de nombres de la clase.

> [!warning]
> *Override* (subclase redefine método del padre) y *overloading* (varias firmas del mismo nombre) son cosas distintas. Lo que Python ofrece es solo lo primero. La "sobrecarga" se emula con argumentos por defecto, `*args`/`**kwargs`, despacho manual por tipo o `functools.singledispatch`.

```python
class C:
    def f(self, a): return a
    def f(self, a, b): return a + b   # NO es overloading

C().f(1, 2)   # 3
C().f(1)      # TypeError: falta el argumento 'b'  -> el primer f se perdió
```

## Relación con otras notas

El *override* presupone [[31 Tipos de Herencia/index | herencia]] y se apoya en [[01 super() y Constructor del Padre | super()]] cuando se quiere reaprovechar al padre. Su variante no destructiva es la [[03 Extension de Metodos | extensión de métodos]]; su consecuencia de diseño es el [[40 Polimorfismo/index | polimorfismo]] de subtipos.
