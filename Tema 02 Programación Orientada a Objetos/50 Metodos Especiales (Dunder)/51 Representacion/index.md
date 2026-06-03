---
title: 51 Representacion
draft: false
description: Cómo se muestra un objeto a humanos y a desarrolladores con __str__, __repr__ y __format__
tags:
  - Index
  - Tema
aliases:
  - Representación
  - Representación de Objetos
---
# Representación

Un objeto necesita **convertirse en texto** en muchos contextos: al imprimirlo, al mostrarlo en la consola interactiva, al interpolarlo en una f-string o al pasarlo a `str()`. Los dunders de **representación** controlan ese texto y permiten distinguir dos audiencias: el **usuario final**, que quiere algo legible, y el **desarrollador**, que quiere algo **no ambiguo** y orientado a la depuración.

```python
class Punto:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):                       # para el desarrollador
        return f"Punto({self.x}, {self.y})"
    def __str__(self):                        # para el usuario
        return f"({self.x}, {self.y})"

p = Punto(1, 2)
print(p)                                      # (1, 2)      -> __str__
p                                             # Punto(1, 2) -> __repr__ en consola
```

Sin estos métodos, un objeto se muestra con el formato por defecto de `object`: `<__main__.Punto object at 0x7f...>`, inútil para identificar su contenido.

## Subtemas

- [[01 __str__ y __repr__ | __str__ y __repr__]] — las dos representaciones canónicas: legible para el usuario frente a no ambigua para el desarrollador, y la regla de delegación entre ambas.
- [[02 __format__ | __format__]] — respuesta del objeto a `format()` y a las f-strings con especificador `f"{obj:spec}"`, interpretando el mini-lenguaje de formato.

## Quién invoca a cada dunder

| Dunder | Invocado por | Audiencia | Si falta |
| ------ | ------------ | --------- | -------- |
| `__repr__` | `repr()`, consola interactiva, *fallback* de `__str__`, `repr` dentro de contenedores | desarrollador | `object.__repr__` (dirección de memoria) |
| `__str__` | `print()`, `str()`, f-strings sin especificador | usuario final | delega en `__repr__` |
| `__format__` | `format()`, `f"{obj:spec}"`, `"{}".format(obj)` | según el `format_spec` | `object.__format__`, que delega en `str()` |

> [!regla]
> `__repr__` es el cimiento: es el *fallback* tanto de `__str__` como de `__format__` con especificador vacío. Una clase que define **solo** `__repr__` ya queda razonablemente representada en todos los contextos.

La representación se relaciona con la [[52 Sobrecarga de Operadores/index | sobrecarga de operadores]] —en especial con `__eq__`— por el ideal de `__repr__`: que `eval(repr(obj))` reconstruya un objeto **igual** al original.
