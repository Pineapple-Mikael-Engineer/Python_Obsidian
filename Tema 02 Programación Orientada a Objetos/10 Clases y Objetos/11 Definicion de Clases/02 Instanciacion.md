---
title: Instanciación
tags:
  - python
  - teoria
  - clases
draft: false
aliases:
  - Instanciacion
  - Crear instancias
  - Instancia
---

# Instanciación

> [!definicion]
> **Instanciar** es crear un objeto concreto a partir de una clase. La sintaxis `obj = Clase(args)` invoca la clase como si fuera una función; el resultado es una **instancia**: un objeto con identidad propia y su propio estado.

```python
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Punto(1, 2)      # instanciación
p.x, p.y             # (1, 2)
```

## Qué ocurre al llamar a `Clase(args)`

Llamar a una clase dispara dos pasos internos en orden:

1. **`__new__(cls, ...)`** — *crea* el objeto vacío y lo reserva en memoria. Devuelve la instancia.
2. **`__init__(self, ...)`** — *inicializa* esa instancia recién creada, fijando su estado.

```python
obj = Clase(a, b)
# equivale, en esencia, a:
obj = Clase.__new__(Clase, a, b)
Clase.__init__(obj, a, b)
```

El detalle de este mecanismo —cuándo redefinir cada uno y por qué `__new__` es el constructor real— se trata en [[03 __new__ vs __init__ | __new__ vs __init__]]. Para el uso cotidiano basta con definir [[04 Constructor __init__ | `__init__`]].

## Cada instancia es independiente

Dos instancias de la misma clase son **objetos distintos**: tienen `id` diferente y estados separados. Modificar una no afecta a la otra.

```python
a = Punto(0, 0)
b = Punto(0, 0)

a is b           # False — objetos distintos
id(a) == id(b)   # False
a.x = 99
b.x              # 0 — b no se ve afectado
```

## Identificar el tipo: `type` e `isinstance`

```python
p = Punto(1, 2)

type(p)                  # <class '__main__.Punto'>
type(p) is Punto         # True

isinstance(p, Punto)     # True
isinstance(p, object)    # True — toda clase hereda de object
```

> [!info]
> `type(obj)` devuelve la clase **exacta**; `isinstance(obj, Clase)` devuelve `True` también si `obj` es de una subclase. Para comprobaciones polimórficas que respeten la [[30 Herencia/index | herencia]], se prefiere `isinstance`.

## Ciclo de vida básico

> [!info]
> 1. **Creación** — `__new__` reserva memoria, `__init__` fija el estado inicial.
> 2. **Uso** — la instancia vive mientras exista al menos una referencia a ella.
> 3. **Recolección** — al perder todas sus referencias, el *garbage collector* libera su memoria (y, si está definido, ejecuta `__del__`).

```python
p = Punto(1, 2)   # creación
p.x               # uso
p = None          # se pierde la referencia -> candidato a recolección
```
