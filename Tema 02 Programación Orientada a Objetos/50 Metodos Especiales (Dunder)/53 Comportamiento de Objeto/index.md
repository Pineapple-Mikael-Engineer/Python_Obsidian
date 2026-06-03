---
title: 53 Comportamiento de Objeto
draft: false
description: Dunders que hacen que un objeto propio se comporte como un tipo nativo - contenedor, función y gestor de contexto
tags:
  - Index
  - Tema
aliases:
  - Comportamiento de Objeto
  - Protocolos de Objeto
---
# Comportamiento de Objeto

Más allá de imprimirse o sumarse, un objeto puede **adoptar el comportamiento de un tipo nativo**: responder a `len()` y a `obj[clave]` como una lista, dejarse **llamar** como una función con `obj()`, o gobernar un bloque `with` como un archivo. Cada uno de esos comportamientos es un **protocolo**: un conjunto de dunders que Python invoca ante una sintaxis concreta. Implementarlos integra la clase con el lenguaje sin heredar de ningún tipo nativo.

```python
class Baraja:
    def __init__(self, cartas):
        self._cartas = list(cartas)
    def __len__(self):                    # len(baraja)
        return len(self._cartas)
    def __getitem__(self, i):             # baraja[i]  -> y además for, in, slicing
        return self._cartas[i]

b = Baraja(["AS", "2C", "3D"])
len(b)                                    # 3
b[0]                                      # "AS"
"2C" in b                                 # True   -> gratis, vía __getitem__
```

Con solo dos métodos `Baraja` ya es **secuenciable**: indexable, iterable y consultable con `in`. El catálogo completo está en [[Catalogo de Metodos Dunder | Catálogo de Métodos Dunder]]; aquí se desarrollan los tres protocolos de comportamiento.

## Subtemas

- [[01 Contenedores (__len__, __getitem__) | Contenedores]] — protocolo de contenedor y secuencia: `__len__`, `__getitem__`, `__setitem__`, `__delitem__`, `__contains__` y el protocolo iterador `__iter__`/`__next__`.
- [[02 Invocable (__call__) | Invocable]] — `__call__` convierte una **instancia** en algo llamable como función: functores, decoradores de clase y fábricas con estado.
- [[03 Context Managers (__enter__, __exit__) | Context Managers]] — `__enter__`/`__exit__` definen el protocolo del `with` para garantizar limpieza determinista de recursos.

## Protocolos y dunders

| Protocolo | Dunders | Sintaxis habilitada |
| --------- | ------- | ------------------- |
| Tamaño | `__len__` | `len(obj)` |
| Acceso por clave | `__getitem__`, `__setitem__`, `__delitem__` | `obj[k]`, `obj[k] = v`, `del obj[k]` |
| Pertenencia | `__contains__` (o *fallback* de `__getitem__`/`__iter__`) | `x in obj` |
| Iteración | `__iter__`, `__next__` (o *fallback* de `__getitem__`) | `for x in obj` |
| Invocable | `__call__` | `obj(...)` |
| Gestor de contexto | `__enter__`, `__exit__` | `with obj as r:` |

> [!info]
> Varios protocolos tienen *fallbacks*: definir `__getitem__` por sí solo ya da iteración y `in`, aunque no se declare `__iter__` ni `__contains__`. Python recurre al método más específico cuando existe y degrada al más general cuando no.

Estos protocolos son la cara del [[40 Polimorfismo/index | polimorfismo]] estructural de Python (*duck typing*): basta implementar los dunders del protocolo para que el objeto sirva donde se espera un contenedor, un callable o un gestor de contexto.
