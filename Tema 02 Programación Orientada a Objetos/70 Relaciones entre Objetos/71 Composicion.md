---
title: Composición
order: 71
tags:
  - python
  - teoria
  - relaciones
draft: false
aliases:
  - Composition
  - Composición de objetos
---

# Composición

> [!definicion]
> La **composición** es una relación **"tiene un" fuerte**: el objeto **compuesto (el todo) crea y posee** sus **partes**, normalmente dentro de su `__init__`. El **ciclo de vida de la parte está ligado al del todo**: cuando el todo deja de existir, sus partes mueren con él. Las partes **no se comparten** con otros objetos; pertenecen en exclusiva al compuesto.

```python
class Motor:
    def __init__(self, cilindrada):
        self.cilindrada = cilindrada
    def arrancar(self):
        return "Brum"

class Coche:
    def __init__(self, cilindrada):
        self.motor = Motor(cilindrada)   # el Coche CREA su Motor: composición
    def encender(self):
        return self.motor.arrancar()     # delega en la parte

c = Coche(2000)
c.encender()        # "Brum"  -> el todo usa a su parte
c.motor.cilindrada  # 2000    -> la parte vive dentro del todo
```

El `Motor` no llega desde fuera: lo **construye el propio `Coche`**. No existe antes que el coche ni se entrega a otro coche distinto. Esa propiedad exclusiva y la creación interna son la firma de la composición.

## Ciclo de vida ligado

> [!regla]
> En composición la parte **no tiene vida propia fuera del todo**. Conceptualmente, al destruir el todo se destruyen sus partes. En Python esto se refleja en el conteo de referencias: si el único objeto que referencia a la parte es el todo, cuando el todo se recolecta su parte queda sin referencias y también se recolecta.

```python
c = Coche(2000)
del c               # se va el Coche... y con él la única referencia a su Motor
```

Como la parte se crea dentro y no se expone para ser reutilizada, ningún otro objeto la conserva viva. Esto es lo opuesto a la [[72 Agregacion | agregación]], donde la parte sobrevive al todo.

## Composición vs Agregación

> [!info]
> Ambas son relaciones **"tiene un"**; se diferencian en **quién crea la parte** y **si se comparte**:
> - **Composición** (◆ rombo lleno en UML): el todo **crea** la parte; es **exclusiva**; muere con el todo.
> - **Agregación** (◇ rombo vacío en UML): la parte **se inyecta** desde fuera; es **compartible**; **sobrevive** al todo.

```python
# Composición: la parte nace dentro
class Coche:
    def __init__(self):
        self.motor = Motor(2000)        # creada y poseída

# Agregación: la parte llega ya construida
class Universidad:
    def __init__(self, profesores):
        self.profesores = profesores    # inyectada, vive fuera
```

El detalle a fijar: en composición el constructor **instancia** la parte; en agregación el constructor **recibe** la parte ya existente como parámetro.

## Base de "composición sobre herencia"

> [!ejemplo]
> Para reutilizar comportamiento, **contener** un objeto que sepa hacer algo suele ser más flexible que **heredar** de él: se delega en la parte en vez de acoplarse a una jerarquía. El `Coche` no *es un* `Motor`, *tiene un* `Motor` y le delega `arrancar()`.

```python
class Coche:
    def __init__(self):
        self.motor = Motor(2000)
    def encender(self):
        return self.motor.arrancar()   # delegación, no herencia
```

Cambiar la implementación del `Motor` no obliga a tocar la jerarquía del `Coche`, y se puede sustituir la parte sin reescribir el todo. Este criterio se desarrolla en [[76 Composicion vs Herencia | Composición vs Herencia]] y contrasta con la [[30 Herencia/index | herencia]] ("es un").
