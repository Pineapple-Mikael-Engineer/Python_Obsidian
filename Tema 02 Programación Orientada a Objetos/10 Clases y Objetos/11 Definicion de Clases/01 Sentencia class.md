---
title: Sentencia class
order: 1
tags:
  - python
  - teoria
  - clases
draft: false
aliases:
  - class statement
  - Definir una clase
  - CapWords
---

# Sentencia class

> [!definicion]
> La sentencia `class Nombre:` **declara un tipo nuevo**. Al ejecutarse, Python recorre el cuerpo del bloque como código normal, recoge los nombres definidos en él en un **namespace** propio y construye con ellos un **objeto-clase**, que queda enlazado al nombre `Nombre`.

```python
class Punto:
    """Representa un punto en el plano."""   # docstring de la clase
    dimension = 2                            # atributo de clase

    def modulo(self):                        # método
        ...

Punto                # <class '__main__.Punto'>
Punto.dimension      # 2
Punto.__doc__        # 'Representa un punto en el plano.'
```

## El cuerpo se ejecuta y crea un namespace

El bloque indentado tras `class` **no es declarativo**: se ejecuta de arriba a abajo una sola vez, en el momento de la definición. Los nombres que queden ligados en ese ámbito —asignaciones y `def`— pasan a ser los **atributos de clase** y **métodos** del tipo.

```python
class Config:
    print("ejecutando el cuerpo")   # se imprime al definir la clase
    base = 10
    doble = base * 2                # 'base' ya existe en este namespace

Config.doble                        # 20
```

Esto significa que el cuerpo puede contener cualquier sentencia (condicionales, bucles), aunque lo habitual es solo asignaciones y `def`. Lo que define el cuerpo es el **estado compartido** y el **comportamiento**; el detalle se trata en [[12 Atributos/index | Atributos]] y [[13 Metodos/index | Métodos]].

## La clase ES un objeto

> [!info]
> Una clase es un objeto en tiempo de ejecución, instancia del tipo `type`. Puede asignarse a variables, pasarse como argumento o devolverse desde una función.

```python
class Animal:
    pass

type(Animal)            # <class 'type'>
isinstance(Animal, type)  # True

Alias = Animal          # la clase es un valor más
Alias is Animal         # True
```

Como toda clase es instancia de `type`, `type` es la **metaclase** por defecto: el "molde de los moldes". Crear una clase con la sentencia `class` equivale a una llamada implícita a `type(nombre, bases, namespace)`.

## Convención de nombres: CapWords

> [!regla]
> Por **PEP 8**, los nombres de clase usan `CapWords` (también llamado `PascalCase`): cada palabra capitalizada, sin guiones bajos. `CuentaBancaria`, `HTTPServer`, `Punto`. Esto las distingue visualmente de funciones y variables, que van en `snake_case`.

## Clase vacía con `pass`

Una clase sin cuerpo útil necesita `pass` para satisfacer la sintaxis de bloque. Sirve como marcador, base para extender luego, o como contenedor al que añadir atributos dinámicamente.

```python
class Vacia:
    pass

v = Vacia()
v.x = 10          # se le añade un atributo de instancia tras crearla
v.x               # 10
```

El siguiente paso es fabricar instancias del tipo recién declarado, en [[02 Instanciacion | Instanciación]].
