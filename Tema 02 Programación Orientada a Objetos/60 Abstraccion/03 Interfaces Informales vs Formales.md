---
title: Interfaces Informales vs Formales
tags:
  - python
  - teoria
  - abstraccion
draft: false
aliases:
  - Informal vs formal interfaces
  - Protocol
  - Interfaces en Python
---

# Interfaces Informales vs Formales

> [!definicion]
> Una **interfaz** es el conjunto de métodos que un objeto debe ofrecer para usarse en cierto contexto. Python admite dos formas de expresarla. La **informal** es una mera convención (*duck typing*): el objeto sirve si **tiene** los métodos, sin declaración ni verificación. La **formal** la impone una clase [[01 Clases Abstractas (ABC) | ABC]] con [[02 abstractmethod | @abstractmethod]]: el contrato se declara explícitamente y su incumplimiento **falla pronto**, al instanciar.

## Interfaz informal (duck typing)

> [!info]
> No existe declaración de interfaz: cualquier objeto con los métodos esperados es válido. El fallo, si falta un método, es un `AttributeError` **en el momento de usarlo**, no antes. Es flexible y sin acoplamiento por herencia, pero no documenta ni garantiza el contrato. Es la base del [[01 Duck Typing | duck typing]].

```python
class Pato:
    def hablar(self): return "Cuac"
class Perro:
    def hablar(self): return "Guau"

def coro(animales):
    return [a.hablar() for a in animales]   # solo exige el método hablar

coro([Pato(), Perro()])    # ['Cuac', 'Guau']  -> sin base común
coro([object()])           # AttributeError: 'object' has no attribute 'hablar'
                           #                  -> falla tarde, al ejecutarse
```

## Interfaz formal (ABC)

> [!info]
> Una ABC declara el contrato con `@abstractmethod` y lo **impone**: una subclase que no lo cumpla no se instancia (`TypeError`). El fallo ocurre **pronto** —al crear el objeto— y la jerarquía documenta explícitamente qué se exige. El coste es la herencia obligatoria de la ABC.

```python
from abc import ABC, abstractmethod

class Sonoro(ABC):
    @abstractmethod
    def hablar(self): ...

class Gato(Sonoro):
    def hablar(self): return "Miau"

class Mudo(Sonoro):
    pass

Gato().hablar()   # "Miau"
Mudo()            # TypeError: al instanciar  -> falla pronto, contrato incumplido
```

## Tercera vía: typing.Protocol

> [!info]
> `typing.Protocol` (PEP 544, Python 3.8+) ofrece **tipado estructural**: define un contrato como una clase, pero un objeto lo satisface por **tener los métodos**, sin heredar de él. Lo verifica `mypy` de forma **estática** (antes de ejecutar), no en tiempo de ejecución. Une la flexibilidad del *duck typing* con la verificación de las ABC.

```python
from typing import Protocol

class Sonoro(Protocol):
    def hablar(self) -> str: ...

class Vaca:                        # NO hereda de Sonoro
    def hablar(self) -> str: return "Muu"

def emitir(s: Sonoro) -> str:
    return s.hablar()

emitir(Vaca())   # "Muu"  -> Vaca cumple la estructura; mypy lo acepta sin herencia
```

Marcando el protocolo con `@runtime_checkable` se habilita `isinstance` (solo comprueba presencia de los métodos, no sus firmas).

## Tabla comparativa

| Criterio | Informal (*duck typing*) | Formal (ABC) | `typing.Protocol` |
|:---|:---|:---|:---|
| **Imposición** | Ninguna (convención) | En tiempo de ejecución | Estática (mypy) |
| **Momento del fallo** | Tarde (al usar el método) | Pronto (al instanciar) | En análisis estático |
| **Herencia requerida** | No | Sí (heredar de la ABC) | No (estructural) |
| **Excepción** | `AttributeError` | `TypeError` | Error de mypy (no en ejecución) |
| **Documenta el contrato** | No | Sí | Sí |

## Cuándo usar cada una

> [!regla]
> - **Informal:** código pequeño o muy dinámico donde el acoplamiento por herencia estorba y se confía en la convención.
> - **ABC:** cuando se quiere **garantizar** el contrato en ejecución y compartir además métodos concretos en la jerarquía; ideal para frameworks y APIs públicas.
> - **Protocol:** para fijar contratos **verificables** sin forzar herencia, especialmente con tipos de terceros que no se pueden modificar; la seguridad la da el chequeo estático.

## Relación con otras notas

La interfaz formal se apoya en [[01 Clases Abstractas (ABC) | ABC]] y [[02 abstractmethod | @abstractmethod]]; la informal es la cara estructural del [[01 Duck Typing | duck typing]]. Todas habilitan el [[40 Polimorfismo/index | polimorfismo]]: distintas implementaciones de un mismo contrato se tratan de forma uniforme.
