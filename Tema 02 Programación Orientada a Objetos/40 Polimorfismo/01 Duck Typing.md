---
title: Duck Typing
tags:
  - python
  - teoria
  - polimorfismo
draft: false
aliases:
  - Duck typing
  - Tipado de pato
---

# Duck Typing

> [!definicion]
> El **duck typing** es la política de Python por la que la compatibilidad de un objeto se juzga por los **métodos y atributos que posee**, no por su tipo ni por su posición en una jerarquía de herencia. Si un objeto implementa la **interfaz** que el código va a usar, sirve. *"Si grazna como un pato y camina como un pato, es un pato."*

```python
def total_lineas(fuente):
    return sum(1 for _ in fuente)   # solo exige que 'fuente' sea iterable

total_lineas(open("datos.txt"))     # archivo
total_lineas(["a", "b", "c"])       # lista       -> 3
total_lineas(("x", "y"))            # tupla        -> 2
```

`total_lineas` no comprueba el tipo de `fuente`: cualquier objeto iterable encaja. No hay base común que los tres argumentos compartan; basta con que respondan al protocolo de iteración.

## La interfaz manda, no el tipo

> [!regla]
> Una función que invoca `obj.metodo()` funciona con **cualquier** objeto que defina `metodo`, sin importar su clase. No se requiere herencia común ni declaración de interfaz. El contrato es implícito: lo fija el conjunto de métodos efectivamente llamados.

```python
import io

def volcar(stream):
    return stream.read()            # solo necesita .read()

volcar(open("datos.txt"))           # archivo en disco
volcar(io.StringIO("en memoria"))   # "en memoria"  -> buffer de texto
# también: respuestas HTTP, sockets, pipes... ninguno comparte clase base
```

`open(...)` y `StringIO` no derivan de un mismo tipo orientado a `read`, pero ambos cumplen el protocolo de lectura, así que son intercambiables para `volcar`. Esto contrasta con el [[02 Polimorfismo de Subtipos | polimorfismo de subtipos]], que sí exige una clase base compartida.

## EAFP frente a comprobar el tipo

> [!info]
> El duck typing se expresa en el estilo **EAFP** (*Easier to Ask Forgiveness than Permission*): se **intenta** usar el objeto y se captura el fallo, en lugar de inspeccionar su tipo de antemano (estilo LBYL, *Look Before You Leap*). Comprobar con `isinstance` cierra la puerta a objetos válidos que no heredan del tipo esperado.

```python
# EAFP — pythónico: intentar y capturar
def primero(obj):
    try:
        return obj[0]               # asume protocolo de indexado
    except (TypeError, KeyError, IndexError):
        return None

# LBYL — frágil: rechaza dict, str, tuple y tipos propios con __getitem__
def primero_rigido(obj):
    if isinstance(obj, list):       # demasiado restrictivo
        return obj[0]
    return None
```

`primero` acepta listas, cadenas, tuplas y cualquier objeto con `__getitem__`; `primero_rigido` solo admite `list` y descarta colecciones perfectamente válidas. La comprobación explícita de tipo rompe la sustituibilidad que el duck typing concede.

> [!warning]
> El precio del duck typing es que los errores de interfaz afloran en **tiempo de ejecución**: si el objeto carece del método esperado, se lanza `AttributeError` al invocarlo, no antes. La fiabilidad descansa en pruebas y en documentar el protocolo exigido.

## Formalización: typing.Protocol

> [!info]
> `typing.Protocol` (PEP 544, Python 3.8+) da nombre a un protocolo sin obligar a heredarlo: cualquier clase que implemente los métodos declarados es aceptada por el verificador estático como conforme. Es **duck typing comprobable estáticamente** (*structural subtyping*), sin tocar el comportamiento en ejecución.

```python
from typing import Protocol

class Legible(Protocol):
    def read(self) -> str: ...       # solo describe la firma

def volcar(s: Legible) -> str:       # mypy acepta cualquier objeto con read()
    return s.read()
```

La conformidad es **estructural**: una clase satisface `Legible` por tener `read`, sin declarar `class X(Legible)`. Esto conserva el espíritu del duck typing y añade verificación en herramientas como `mypy`. Cuando lo deseable es **exigir** la implementación de una interfaz vía herencia, se recurre a la [[60 Abstraccion/index | abstracción]] con clases base abstractas.
