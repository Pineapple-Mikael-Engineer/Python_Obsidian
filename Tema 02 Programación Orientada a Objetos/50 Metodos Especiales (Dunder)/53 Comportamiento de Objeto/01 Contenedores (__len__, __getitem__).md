---
title: Contenedores (__len__, __getitem__)
order: 1
tags:
  - python
  - teoria
  - dunder
draft: false
aliases:
  - Protocolo de contenedor
  - Protocolo de secuencia
  - Container protocol
---

# Contenedores (__len__, __getitem__)

> [!definicion]
> El **protocolo de contenedor** es el conjunto de dunders que hacen que un objeto propio se comporte como una **colección**: medirse con `len()`, indexarse con `obj[clave]`, modificarse, recorrerse con `for` y consultarse con `in`. Implementando un par de ellos —`__len__` y `__getitem__`— la clase ya queda **secuenciable**: indexable e iterable.

```python
class Baraja:
    PALOS = "♠♥♦♣"
    def __init__(self):
        self._cartas = [f"{v}{p}" for p in self.PALOS for v in range(1, 4)]
    def __len__(self):                    # len(baraja)
        return len(self._cartas)
    def __getitem__(self, pos):           # baraja[pos], y de regalo: for, in, slicing
        return self._cartas[pos]

b = Baraja()
len(b)                                    # 12
b[0]                                      # "1♠"
b[-1]                                     # "3♣"   -> índices negativos heredados de la lista
b[:2]                                     # ["1♠", "2♠"]  -> slicing, pos es un slice
for carta in b: ...                       # itera vía __getitem__ (fallback)
"2♥" in b                                 # True   -> también vía __getitem__
```

`Baraja` no hereda de `list` ni declara `__iter__`/`__contains__`, y aun así es iterable e indexable: delega todo en `self._cartas` a través de `__getitem__`.

## Acceso por clave: lectura, escritura y borrado

> [!regla]
> Los tres dunders de acceso por clave reparten la sintaxis `obj[clave]` según el contexto: **leer** invoca `__getitem__`, **asignar** invoca `__setitem__`, **borrar con `del`** invoca `__delitem__`. La `clave` puede ser un entero, un `slice` o cualquier objeto (como en un diccionario).

```python
class Registro:
    def __init__(self):
        self._d = {}
    def __getitem__(self, k):             # r[k]
        return self._d[k]
    def __setitem__(self, k, v):          # r[k] = v
        self._d[k] = v
    def __delitem__(self, k):             # del r[k]
        del self._d[k]

r = Registro()
r["a"] = 1                                # __setitem__
r["a"]                                    # 1   -> __getitem__
del r["a"]                                # __delitem__
```

## Tamaño y pertenencia

`__len__` debe devolver un entero `>= 0`; lo usan `len()` y, además, el contexto booleano: un objeto sin `__bool__` se considera **falsy** cuando `len(obj) == 0`.

`__contains__(self, x)` define el operador `in`. Si no se implementa, Python lo simula recorriendo el objeto (vía `__iter__` o, en su defecto, `__getitem__`) y comparando con `==`. Definir `__contains__` permite una comprobación **más eficiente** (p. ej. delegando en un `set` o `dict` interno).

```python
class Catalogo:
    def __init__(self, items):
        self._s = set(items)
    def __len__(self):
        return len(self._s)
    def __contains__(self, x):            # x in catalogo  -> O(1), sin recorrer
        return x in self._s

c = Catalogo(["a", "b"])
bool(c)                                   # True   -> len != 0
len(Catalogo([]))                         # 0      -> y bool sería False
"a" in c                                  # True   -> __contains__
```

## Protocolo iterador: __iter__ y __next__

> [!info]
> La iteración tiene dos niveles. Un **iterable** define `__iter__`, que devuelve un **iterador**. Un **iterador** define `__next__`, que devuelve el siguiente elemento y lanza `StopIteration` al agotarse. El `for` llama a `iter(obj)` para obtener el iterador y luego a `next()` repetidamente.

```python
class Contador:                           # iterable + iterador a la vez
    def __init__(self, fin):
        self.fin, self.i = fin, 0
    def __iter__(self):                   # iter(c) -> el propio objeto
        return self
    def __next__(self):                   # next(c)
        if self.i >= self.fin:
            raise StopIteration
        self.i += 1
        return self.i

list(Contador(3))                         # [1, 2, 3]
```

> [!ejemplo]
> Implementar `__iter__` con un **generador** evita escribir `__next__` y mantener estado a mano: `yield` produce el iterador automáticamente.
> ```python
> class Rango:
>     def __init__(self, n): self.n = n
>     def __iter__(self):
>         for i in range(self.n):
>             yield i * i
> list(Rango(4))                          # [0, 1, 4, 9]
> ```

## Fallback de iteración por __getitem__

> [!warning]
> Si un objeto **no** define `__iter__`, Python recurre a un protocolo de iteración antiguo basado en `__getitem__`: lo invoca con `0, 1, 2, …` hasta que lanza `IndexError`. Por eso `Baraja`, con solo `__getitem__`, ya es iterable. Es un *fallback* cómodo, pero solo funciona con **claves enteras consecutivas**; para iterar sobre un mapa por clave hace falta `__iter__` explícito.

La iteración conecta con el [[02 For]] del control de flujo: todo `for x in obj` se apoya en este protocolo, y con `__getitem__` o `__iter__` una clase propia encaja en él sin esfuerzo. El resto de protocolos de comportamiento —[[02 Invocable (__call__) | invocable]] y [[03 Context Managers (__enter__, __exit__) | gestores de contexto]]— siguen la misma idea de implementar dunders para integrarse con la sintaxis nativa.
