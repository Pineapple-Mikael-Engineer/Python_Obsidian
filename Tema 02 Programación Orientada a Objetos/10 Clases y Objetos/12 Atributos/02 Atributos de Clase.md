---
title: Atributos de Clase
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - Class attributes
  - Atributos compartidos
---

# Atributos de Clase

> [!definicion]
> Un **atributo de clase** se define en el **cuerpo de la clase**, fuera de cualquier método. Existe **una sola copia compartida** por todas las instancias y por la propia clase. Vive en `Clase.__dict__`, no en el de cada objeto. Sirve para **constantes** comunes y para **contadores** o estado global de la clase.

```python
class Perro:
    especie = "Canis familiaris"   # atributo de CLASE - compartido
    def __init__(self, nombre):
        self.nombre = nombre       # atributo de INSTANCIA - propio

a = Perro("Bobi")
b = Perro("Laika")
a.especie, b.especie               # mismo valor para ambos
Perro.especie                      # accesible desde la clase
```

## Resolución y sombreado

Al leer `obj.x`, Python busca primero en la instancia y, si no lo encuentra, en la clase. Por eso una instancia puede **leer** un atributo de clase sin tener uno propio.

```python
a = Perro("Bobi")
a.__dict__                # {'nombre': 'Bobi'}  -> 'especie' NO está aquí
a.especie                 # se resuelve en Perro.__dict__
```

Asignar a través de la instancia **no** modifica el atributo de clase: crea uno **de instancia** con el mismo nombre que lo **sombrea** localmente.

```python
a.especie = "lobo"        # crea a.__dict__['especie'] - sombrea
a.especie                 # "lobo"   (instancia)
b.especie                 # "Canis familiaris"  (clase, intacto)
Perro.especie             # "Canis familiaris"  (clase, intacto)
del a.especie             # se elimina el de instancia
a.especie                 # "Canis familiaris"  -> vuelve a verse el de clase
```

> [!regla]
> Para modificar el atributo **compartido** hay que asignarlo en la clase: `Perro.especie = ...`. Asignarlo vía instancia siempre crea un atributo de instancia que sombrea.

## Caso de uso: contador de instancias

```python
class Usuario:
    total = 0                 # contador compartido
    def __init__(self, nombre):
        self.nombre = nombre
        Usuario.total += 1    # se modifica EN LA CLASE

Usuario("Ana"); Usuario("Luis")
Usuario.total                 # 2
```

Si dentro de `__init__` se escribiera `self.total += 1`, en la primera lectura tomaría el valor de clase pero la asignación crearía un atributo de instancia, y el contador global nunca avanzaría.

## El error clásico: atributo de clase mutable

> [!warning]
> Un atributo de clase **mutable** (lista, dict, set) es **un único objeto compartido por todas las instancias**. Mutarlo desde una instancia afecta a **todas**, porque no hay sombreado: `self.lista.append(x)` no asigna a `self`, sino que muta el objeto común de la clase.

```python
class Carrito:
    items = []                    # MAL: lista compartida por todos
    def agregar(self, x):
        self.items.append(x)      # muta el objeto de clase, no crea uno propio

c1 = Carrito()
c2 = Carrito()
c1.agregar("pan")
c2.items                          # ['pan']  -> ¡fuga de estado entre instancias!
c1.items is c2.items              # True  -> es el MISMO objeto
```

**Solución:** inicializar el atributo mutable en `__init__`, de modo que cada instancia reciba su propio objeto.

```python
class Carrito:
    def __init__(self):
        self.items = []           # BIEN: una lista NUEVA por instancia

c1 = Carrito(); c2 = Carrito()
c1.items.append("pan")
c2.items                          # []  -> estado aislado
c1.items is c2.items              # False
```

La regla práctica: las **constantes inmutables** (números, cadenas, tuplas) pueden ir como atributos de clase sin riesgo; el **estado mutable propio** de cada objeto debe inicializarse en `__init__`. La distinción entre objetos mutables e inmutables se detalla en [[01 Objetos Inmutables | Objetos Inmutables]].
