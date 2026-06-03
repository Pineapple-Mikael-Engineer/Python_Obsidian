---
title: Objetos Inmutables
tags:
  - python
  - teoria
  - mutabilidad
draft: false
aliases:
  - Immutable objects
  - Tipos inmutables
  - Hashables
---

# Objetos Inmutables

> [!definicion]
> Un objeto **inmutable** es aquel cuyo contenido **no puede cambiar** tras su creación. Toda operación que aparente "modificarlo" produce en realidad un objeto nuevo en una dirección de memoria distinta, dejando el original intacto. La inmutabilidad es propiedad del **tipo**, no del valor.

Tipos inmutables del núcleo de Python:

- **Numéricos:** `int`, `float`, `complex`, `bool`.
- **Secuencias:** `str`, `tuple`, `bytes`.
- **Conjuntos:** `frozenset` (la versión inmutable de `set`).
- **Constante:** `None`.

Todos los inmutables son **hashables**: poseen un `__hash__` estable durante su vida, por lo que pueden usarse como claves en [[01 Diccionarios | diccionarios]] o elementos de un `set`.

## Identidad: cada "cambio" crea un objeto nuevo

La función `id(objeto)` devuelve la dirección de memoria. Si el `id` cambia tras una operación, el dato es inmutable: no se mutó, se reasignó la variable a un objeto recién creado (*rebinding*).

```python
a = (1, 2, 3)            # Tupla - inmutable
print(f"id(a) antes: {id(a)}")   # Ej: 140245...
a = a + (4,)             # Crea NUEVA tupla, no modifica la original
print(f"id(a) después: {id(a)}")  # DIFERENTE id
```

El nombre `a` apunta primero a `(1, 2, 3)` y luego a `(1, 2, 3, 4)`, que es un objeto distinto. El operador `+` sobre tuplas, las concatenaciones de `str` y la aritmética sobre `int`/`float` siguen este patrón: construyen y devuelven un objeto nuevo.

```python
s = "hola"
print(id(s))
s += " mundo"            # NO modifica "hola"; crea "hola mundo"
print(id(s))             # id distinto
```

## Rebinding vs. mutación

*Rebinding* es asignar un nombre a otro objeto; **no** altera el objeto previo. Con inmutables es la única vía de "cambio", y por ello otros nombres que aún apunten al objeto original no se ven afectados.

```python
x = 10
y = x          # y apunta al mismo int 10
x = x + 1      # x se reenlaza a un nuevo int 11; y sigue en 10
print(x, y)    # 11 10
```

Esta propiedad hace a los inmutables seguros frente al *aliasing*: compartir referencias nunca produce efectos colaterales sorpresivos (a diferencia de los [[02 Objetos Mutables | objetos mutables]]).

## Inmutabilidad estricta vs. relativa

> [!warning]
> La inmutabilidad de un contenedor es **superficial**: garantiza que la estructura externa no cambie, no que su contenido sea inmutable.

- **Estricta:** `int`, `float`, `str`, `bytes`, `tuple` con elementos inmutables. Nada en su interior puede cambiar.
- **Relativa:** [[03 Tuplas | `tuple`]] que contiene objetos mutables. La tupla conserva su `id` y sus referencias, pero los objetos referenciados sí pueden mutar.

```python
# Tupla con lista - inmutabilidad "superficial"
t = ([1, 2], 3)
print(f"id(t): {id(t)}")  # Constante
t[0].append(3)            # PERMITIDO: la lista interna cambia
print(f"t después: {t}")  # ([1, 2, 3], 3)
```

La tupla `t` nunca cambia sus dos referencias; lo que muta es el objeto `list` al que apunta su primer elemento. Una tupla con un elemento mutable **deja de ser hashable**.

## `frozenset`: el conjunto inmutable

```python
fs = frozenset([1, 2, 3])
# fs.add(4)  # Error: 'frozenset' object has no attribute 'add'

# Al ser hashable, puede contener otros frozensets o ser clave de dict
fs2 = frozenset([fs, frozenset([4, 5])])
print(fs2)  # frozenset({frozenset({1, 2, 3}), frozenset({4, 5})})
```

`frozenset` ofrece las operaciones de conjunto (`union`, `intersection`, `difference`) pero ninguna que mute (`add`, `discard`, `update`). Es el único tipo de conjunto admisible como clave de diccionario o elemento de otro conjunto.

## Optimizaciones de CPython sobre inmutables

Al no poder cambiar, los inmutables permiten que el intérprete **comparta** una sola instancia entre múltiples referencias.

### Pool de enteros pequeños

```python
# Python cachea enteros pequeños (-5 a 256)
a = 100
b = 100
print(a is b)  # True - MISMO objeto

c = 1000
d = 1000
print(c is d)  # False (en modo interactivo) o True (en scripts)
```

### Interning de strings

```python
s1 = "hello"
s2 = "hello"
print(s1 is s2)  # True - mismo objeto por interning

# No todos los strings se internan automáticamente
s3 = "hello world!"
s4 = "hello world!"
print(s3 is s4)  # False (depende del contexto)
```

> [!info]
> `is` compara **identidad** (mismo objeto), `==` compara **valor**. El caché de enteros y el interning de strings explican por qué `is` a veces devuelve `True` para inmutables que se escribieron por separado. No debe usarse `is` para comparar valores numéricos o de texto; solo para `None`, `True`, `False`.

## Ventajas operativas

> [!info]
> - **Thread-safe:** al no mutar, no requieren bloqueos entre hilos.
> - **Cacheables:** su hash es estable, permitiendo memoización y uso como clave.
> - **Claves de diccionario:** acceso $O(1)$ garantizado por hash invariante.
> - **Compartición de memoria:** múltiples referencias a un mismo objeto sin riesgo.

## Construcciones inmutables avanzadas

> [!warning]
> Estos casos requieren temas que aún no se tratan; se incluyen como referencia.

`namedtuple` y `dataclass(frozen=True)` construyen registros inmutables con atributos nombrados:

```python
from collections import namedtuple
from dataclasses import dataclass

Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
# p.x = 3  # Error: can't set attribute

@dataclass(frozen=True)
class InmutableData:
    name: str
    value: int

data = InmutableData("test", 42)
# data.value = 99  # Error: frozen instance
```

### Patrón funcional: no modificar, devolver nuevo

```python
def procesar_datos(datos_inmutables):
    # En lugar de modificar, crear nuevo
    return tuple(x * 2 for x in datos_inmutables)

original = (1, 2, 3)
procesado = procesar_datos(original)
# 'original' permanece sin cambios
```

### Construcción eficiente de texto

Como cada concatenación de `str` crea un objeto nuevo, acumular en una `list` y unir una sola vez con `join` evita objetos intermedios:

```python
parts = []
for i in range(1000):
    parts.append(f"item_{i}")
result = "".join(parts)  # Una sola asignación final
```
