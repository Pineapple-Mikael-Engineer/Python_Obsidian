---
title: Agregación
tags:
  - python
  - teoria
  - relaciones
draft: false
aliases:
  - Aggregation
  - Agregación de objetos
---

# Agregación

> [!definicion]
> La **agregación** es una relación **"tiene un" débil**: el **todo agrupa partes que existen de forma independiente** y que **pueden compartirse** con otros todos. Las partes **no las crea el todo**: se **inyectan desde fuera** (típicamente por el constructor). El **ciclo de vida es independiente**: si el todo desaparece, las partes **siguen vivas**.

```python
class Profesor:
    def __init__(self, nombre):
        self.nombre = nombre

class Universidad:
    def __init__(self, profesores):
        self.profesores = profesores      # las RECIBE: agregación

ana = Profesor("Ana")
luis = Profesor("Luis")
u = Universidad([ana, luis])              # los profesores ya existían
u.profesores[0].nombre                    # "Ana"
```

`ana` y `luis` se construyen **antes** que la `Universidad` y se le pasan ya hechos. La universidad los **agrupa**, pero no los **posee** en exclusiva.

## Las partes sobreviven al todo

> [!regla]
> En agregación las partes tienen **referencias externas**, por lo que **no mueren con el todo**. Eliminar el todo no afecta a las partes: otros objetos (o el propio programa) las siguen referenciando.

```python
u = Universidad([ana, luis])
del u               # cierra la Universidad...
ana.nombre          # "Ana"  -> el Profesor sigue vivo
```

Esto es exactamente lo contrario al ciclo de vida ligado de la [[01 Composicion | composición]], donde la parte muere con el todo.

## Partes compartidas

> [!ejemplo]
> Como las partes existen por su cuenta, **un mismo objeto puede pertenecer a varios todos** a la vez. Ambos comparten la **misma instancia** (no copias): mutarla desde uno se ve desde el otro.

```python
ana = Profesor("Ana")
uni_a = Universidad([ana])
uni_b = Universidad([ana])          # la MISMA Ana en dos universidades

uni_a.profesores[0] is uni_b.profesores[0]   # True -> instancia compartida
```

La compartición es imposible en composición (parte exclusiva) y natural en agregación.

## Composición vs Agregación

> [!info]
> Las dos modelan **"tiene un"**; el contraste está en el **origen** y la **exclusividad** de la parte:
>
> | Aspecto | Composición | Agregación |
> | ------- | ----------- | ---------- |
> | Quién crea la parte | el **todo** (en `__init__`) | **fuera**, se inyecta |
> | Exclusividad | parte **exclusiva** | parte **compartible** |
> | Ciclo de vida | muere **con** el todo | **sobrevive** al todo |
> | UML | rombo lleno ◆ | rombo vacío ◇ |

```python
# Composición: crea dentro -> exclusiva, muere con el todo
class Coche:
    def __init__(self):
        self.motor = Motor(2000)

# Agregación: recibe fuera -> compartible, sobrevive al todo
class Universidad:
    def __init__(self, profesores):
        self.profesores = profesores
```

La agregación es **más débil** que la composición pero sigue expresando "parte de"; cuando la relación ni siquiera es de contención sino de mero uso, se trata de una [[03 Asociacion | asociación]]. Para elegir entre contener y heredar, ver [[06 Composicion vs Herencia | Composición vs Herencia]].
