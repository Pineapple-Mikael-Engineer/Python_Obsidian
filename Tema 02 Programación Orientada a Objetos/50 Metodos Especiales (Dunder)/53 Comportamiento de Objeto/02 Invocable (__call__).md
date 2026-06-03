---
title: Invocable (__call__)
tags:
  - python
  - teoria
  - dunder
draft: false
aliases:
  - Callable
  - Functor
  - Objeto invocable
---

# Invocable (__call__)

> [!definicion]
> `__call__(self, ...)` convierte una **instancia** en algo que se puede **llamar como una función**: tras definirlo, `obj(args)` ejecuta `obj.__call__(args)`. El objeto sigue siendo una instancia normal —con estado y otros métodos—, pero adquiere además la sintaxis de invocación. A un objeto así se le llama **invocable** o *functor*.

```python
class Multiplicador:
    def __init__(self, factor):
        self.factor = factor              # estado configurado al construir
    def __call__(self, x):                # habilita m(x)
        return x * self.factor

doble = Multiplicador(2)
triple = Multiplicador(3)
doble(5)                                  # 10   -> doble.__call__(5)
triple(5)                                 # 15
```

`doble` y `triple` comparten clase pero llevan **factores distintos**: cada instancia es una "función" parametrizada por su estado.

## Objeto-función con estado frente a función normal

> [!regla]
> Una función normal es **sin estado** entre llamadas (salvo trucos con variables libres o atributos). Un invocable **encapsula estado mutable** en `self` y lo conserva entre llamadas, manteniendo a la vez una interfaz de función. Es la opción natural cuando una "función" necesita **recordar** o **configurarse**.

```python
class Acumulador:
    def __init__(self):
        self.total = 0
    def __call__(self, x):                # cada llamada recuerda lo anterior
        self.total += x
        return self.total

acc = Acumulador()
acc(10)                                   # 10
acc(5)                                    # 15   -> el estado persiste en self.total
acc(1)                                    # 16
```

## Detección con callable()

`callable(obj)` indica si un objeto puede invocarse. Es `True` para funciones, métodos, clases (llamarlas construye una instancia) y para cualquier instancia cuya clase defina `__call__`.

```python
callable(doble)                           # True   -> su clase define __call__
callable(Multiplicador)                   # True   -> las clases son invocables
callable(42)                              # False
```

## Casos de uso

> [!ejemplo]
> **Decorador implementado como clase**: el estado vive en la instancia (aquí, el contador de llamadas) en lugar de en una clausura.
> ```python
> class CuentaLlamadas:
>     def __init__(self, fn):
>         self.fn, self.n = fn, 0
>     def __call__(self, *args, **kw):
>         self.n += 1
>         return self.fn(*args, **kw)
>
> @CuentaLlamadas
> def saludar(nombre):
>     return f"Hola {nombre}"
>
> saludar("Ana")                          # "Hola Ana"
> saludar("Leo")                          # "Hola Leo"
> saludar.n                               # 2   -> el decorador-objeto llevó la cuenta
> ```

> [!info]
> Otros usos típicos del invocable:
> - **Functores / fábricas con configuración**: se construye un objeto con parámetros (`Multiplicador(2)`) y luego se usa como función ligera muchas veces.
> - **Estrategias y *callbacks***: pasar un objeto con estado allí donde una API espera una función.
> - **Cierres con introspección**: a diferencia de una clausura, el estado vive en atributos visibles y depurables (`acc.total`).

Definir `__call__` es otro protocolo de [[53 Comportamiento de Objeto/index | comportamiento de objeto]]: igual que `__getitem__` hace que la instancia parezca una [[01 Contenedores (__len__, __getitem__) | secuencia]], `__call__` hace que parezca una función, integrándose con la sintaxis del lenguaje sin dejar de ser un objeto.
