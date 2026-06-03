---
title: Enumeraciones (Enum)
tags:
  - python
  - teoria
  - poo
draft: false
aliases:
  - Enum
  - Enumeraciones
---

# Enumeraciones (Enum)

> [!definicion]
> Una **enumeración** (clase que hereda de `Enum`, módulo `enum`) define un **conjunto cerrado y nombrado de constantes**. Cada miembro asocia un **nombre** (`.name`) a un **valor** (`.value`) y es un **singleton**: existe una sola instancia por miembro, comparable por **identidad** (`is`). Sustituye a las constantes sueltas (`ROJO = 1; VERDE = 2; ...`) por una agrupación con tipo propio.

```python
from enum import Enum

class Color(Enum):
    ROJO = 1
    VERDE = 2
    AZUL = 3

Color.ROJO              # <Color.ROJO: 1>
Color.ROJO.name         # 'ROJO'
Color.ROJO.value        # 1
Color.ROJO is Color.ROJO    # True   -> singleton, comparar por identidad
```

## Operaciones fundamentales

```python
list(Color)                 # [<Color.ROJO: 1>, <Color.VERDE: 2>, <Color.AZUL: 3>]  -> iterable
Color(2)                    # <Color.VERDE: 2>   -> búsqueda por valor
Color['AZUL']               # <Color.AZUL: 3>    -> búsqueda por nombre
len(Color)                  # 3
Color.ROJO in Color         # True
```

> [!warning]
> Los valores **no se comparan por igualdad de valor** con un literal: `Color.ROJO == 1` es `False`, porque el miembro es un objeto `Color`, no el entero. La comparación correcta es `Color.ROJO is Color(1)`. La excepción es `IntEnum` (abajo). Además, los miembros son **inmutables y únicos**: dos miembros no pueden compartir el mismo valor sin que el segundo se vuelva un **alias** del primero.

## Variantes

### `auto()` — valores automáticos

Cuando el valor concreto es irrelevante y solo importa la distinción:

```python
from enum import Enum, auto

class Estado(Enum):
    PENDIENTE = auto()      # 1
    ACTIVO = auto()         # 2
    CERRADO = auto()        # 3
```

### `IntEnum` — compatible con `int`

Sus miembros **son** enteros: comparables y operables con `int` directamente. Útil para interoperar con APIs que esperan números (códigos HTTP, niveles de log), a costa de perder la separación estricta de tipo.

```python
from enum import IntEnum

class Prioridad(IntEnum):
    BAJA = 1
    ALTA = 3

Prioridad.ALTA > Prioridad.BAJA     # True
Prioridad.ALTA == 3                 # True   -> a diferencia de Enum puro
```

### `Flag` — combinables con bits

Para conjuntos de opciones que se **combinan** mediante operadores bit a bit (`|`, `&`, `~`); los valores deben ser potencias de 2.

```python
from enum import Flag, auto

class Permiso(Flag):
    LEER = auto()           # 1
    ESCRIBIR = auto()       # 2
    EJECUTAR = auto()       # 4

p = Permiso.LEER | Permiso.ESCRIBIR
Permiso.ESCRIBIR in p       # True
p                           # <Permiso.LEER|ESCRIBIR: 3>
```

## Métodos y miembros propios

Una `Enum` es una clase: admite métodos que operan sobre `self.value`/`self.name`, encapsulando lógica junto a las constantes.

```python
class Planeta(Enum):
    TIERRA = (5.97e24, 6.37e6)
    MARTE  = (6.42e23, 3.39e6)

    def __init__(self, masa, radio):
        self.masa = masa
        self.radio = radio

    def gravedad(self):
        return 6.67e-11 * self.masa / self.radio**2

Planeta.TIERRA.gravedad()   # 9.81...
```

## Ventaja sobre constantes sueltas

> [!regla]
> Frente a `ROJO = 1; VERDE = 2` a nivel de módulo, una `Enum` aporta: **agrupación** bajo un tipo común (`Color`), **legibilidad** en *repr* y mensajes (`<Color.ROJO: 1>` en vez de `1`), **seguridad** (el conjunto es cerrado: `Color(99)` lanza `ValueError`, mientras un entero suelto admitiría cualquier valor), e **iteración/búsqueda** integradas. Para un agregado de datos con identidad por valor la herramienta es [[01 Dataclasses | el dataclass]]; para un conjunto cerrado de constantes nombradas, la `Enum`.
