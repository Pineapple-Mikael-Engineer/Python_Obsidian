---
title: Catálogo de Métodos Dunder
tags:
  - python
  - referencia
  - poo
draft: false
aliases:
  - Catálogo de Métodos Especiales
  - Dunder Methods
  - Magic Methods
---

# Catálogo de Métodos Dunder

Tabla de consulta de los **métodos especiales** (`__x__`, *double underscore*) que Python invoca implícitamente ante una sintaxis o función incorporada. Implementarlos integra una clase propia con el protocolo del lenguaje. El desarrollo de cada protocolo vive en [[50 Metodos Especiales (Dunder)/index | Métodos Especiales]]; el mapeo operador → método, en [[52 Sobrecarga de Operadores/index | Sobrecarga de Operadores]].

> [!info] Convención
> El intérprete busca los dunder en la **clase**, no en la instancia (`type(obj).__x__`, salta `__getattr__`/`__getattribute__`). Un dunder no implementado delega en el de la superclase, en última instancia `object`.

## Creación e inicialización

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__new__` | `Clase(...)` (antes de `__init__`) | Crea y devuelve la instancia; método estático implícito. Se sobrescribe para inmutables o *singletons* |
| `__init__` | `Clase(...)` (tras `__new__`) | Inicializa la instancia ya creada; no retorna valor |
| `__del__` | `del obj` / recolección de basura | Finalizador; se ejecuta al destruirse el objeto. Sin garantía de momento exacto |

## Representación y conversión

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__repr__` | `repr(obj)`, eco en consola, *debug* | Representación inequívoca, idealmente reconstruible. *Fallback* de `__str__` |
| `__str__` | `str(obj)`, `print(obj)`, `f"{obj}"` | Representación legible para usuario final |
| `__format__` | `format(obj, spec)`, `f"{obj:spec}"` | Formato según *mini-lenguaje* de especificación |
| `__bytes__` | `bytes(obj)` | Representación en bytes del objeto |

## Comparación y hash

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__eq__` | `a == b` | Igualdad. Definirlo sin `__hash__` vuelve la clase no *hashable* |
| `__ne__` | `a != b` | Desigualdad; por defecto niega `__eq__` |
| `__lt__` | `a < b` | Menor que |
| `__le__` | `a <= b` | Menor o igual que |
| `__gt__` | `a > b` | Mayor que; reflejo de `__lt__` |
| `__ge__` | `a >= b` | Mayor o igual que; reflejo de `__le__` |
| `__hash__` | `hash(obj)`, claves de `dict`, elementos de `set` | Valor *hash* entero. Objetos iguales deben compartir *hash* |

> [!info] total_ordering
> `functools.total_ordering` deriva los seis comparadores a partir de `__eq__` y uno de orden (`__lt__`, `__le__`, `__gt__` o `__ge__`).

## Operadores aritméticos

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__add__` | `a + b` | Suma |
| `__sub__` | `a - b` | Resta |
| `__mul__` | `a * b` | Multiplicación |
| `__truediv__` | `a / b` | División real |
| `__floordiv__` | `a // b` | División entera |
| `__mod__` | `a % b` | Módulo |
| `__pow__` | `a ** b`, `pow(a, b)` | Potencia |
| `__neg__` | `-a` | Negación unaria |

### Reflejados (operando derecho)

Se invocan cuando el operando izquierdo no implementa la operación o devuelve `NotImplemented`.

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__radd__` | `a + b` (vía `b`) | Suma reflejada |
| `__rsub__` | `a - b` (vía `b`) | Resta reflejada |
| `__rmul__` | `a * b` (vía `b`) | Multiplicación reflejada |
| `__rtruediv__` | `a / b` (vía `b`) | División reflejada |

### In-place (asignación aumentada)

Modifican el objeto en sitio cuando es posible; si no existen, Python recurre al operador no reflejado y reasigna.

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__iadd__` | `a += b` | Suma en sitio |
| `__isub__` | `a -= b` | Resta en sitio |
| `__imul__` | `a *= b` | Multiplicación en sitio |
| `__itruediv__` | `a /= b` | División en sitio |

## Contenedores y secuencias

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__len__` | `len(obj)`, contexto booleano (*fallback*) | Número de elementos |
| `__getitem__` | `obj[k]`, `obj[i:j]` | Lectura por clave/índice/*slice* |
| `__setitem__` | `obj[k] = v` | Asignación por clave/índice |
| `__delitem__` | `del obj[k]` | Eliminación por clave/índice |
| `__contains__` | `x in obj` | Pertenencia; *fallback* recorre con `__iter__`/`__getitem__` |
| `__iter__` | `iter(obj)`, `for x in obj` | Devuelve un iterador |
| `__next__` | `next(it)` | Siguiente elemento; lanza `StopIteration` al agotarse |

## Invocable y acceso a atributos

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__call__` | `obj(...)` | Hace la instancia invocable como una función |
| `__getattr__` | `obj.x` (solo si falla la búsqueda normal) | Resuelve atributos inexistentes |
| `__setattr__` | `obj.x = v` | Intercepta **toda** asignación de atributo |
| `__getattribute__` | `obj.x` (siempre) | Intercepta **todo** acceso de atributo; precaución con la recursión |
| `__dir__` | `dir(obj)` | Lista de atributos expuestos |

## Gestión de contexto

| Método | Invocado por | Propósito |
| ------ | ------------ | --------- |
| `__enter__` | entrada a `with obj as x:` | Prepara el recurso; su retorno se liga a `x` |
| `__exit__` | salida de `with` (normal o por excepción) | Libera el recurso; retornar `True` suprime la excepción |

> [!warning] NotImplemented vs NotImplementedError
> Un dunder aritmético/de comparación debe **retornar** `NotImplemented` (singleton) para ceder al operando reflejado; `raise NotImplementedError` es para métodos abstractos pendientes y aborta la operación.
