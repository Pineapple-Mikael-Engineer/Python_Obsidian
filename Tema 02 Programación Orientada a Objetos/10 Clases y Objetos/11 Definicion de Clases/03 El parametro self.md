---
title: El parámetro self
order: 3
tags:
  - python
  - teoria
  - clases
draft: false
aliases:
  - self
  - Parametro self
  - Método ligado
---

# El parámetro self

> [!definicion]
> `self` es el **primer parámetro** de todo método de instancia y recibe, de forma automática, la **referencia a la instancia** sobre la que se invocó el método. A través de `self` el método lee y escribe el estado del objeto concreto que lo llamó.

```python
class Contador:
    def __init__(self):
        self.n = 0
    def incrementar(self):
        self.n += 1        # self -> la instancia que llamó al método

c = Contador()
c.incrementar()
c.n                        # 1
```

## `self` no es una palabra clave

> [!regla]
> `self` es solo una **convención** de nombre, no una palabra reservada. Python pasa la instancia como primer argumento sin importar cómo se llame; usar `self` es universal y PEP 8 lo recomienda. Renombrarlo funciona pero confunde y debe evitarse.

```python
class Punto:
    def mostrar(esto):     # funciona, pero NO es idiomático
        print(esto.x)
```

## `obj.metodo()` equivale a `Clase.metodo(obj)`

Acceder a un método desde una instancia produce un **método ligado** (*bound method*): la instancia queda "pegada" como primer argumento. Por eso no se pasa `self` explícitamente al llamar.

```python
c = Contador()

c.incrementar()              # forma habitual (método ligado)
Contador.incrementar(c)      # equivalente explícito (método no ligado)

type(c.incrementar)          # <class 'method'>      -> ligado
type(Contador.incrementar)   # <class 'function'>    -> función pura
```

`c.incrementar` es un método **ligado**: ya conoce su `self`. `Contador.incrementar` es la función subyacente, **no ligada**, que exige pasar la instancia a mano.

## Por qué Python lo hace explícito

> [!info]
> Otros lenguajes inyectan un `this` implícito. Python prefiere lo explícito: `self` deja claro en la firma que el método opera sobre una instancia, distingue sin ambigüedad un atributo de instancia (`self.x`) de una variable local (`x`), y hace que `Clase.metodo(obj)` sea coherente con el modelo de descriptores.

## Errores comunes

> [!warning]
> Olvidar `self` en la firma de un método provoca `TypeError` al llamarlo, porque Python ya pasa la instancia como primer argumento posicional.

```python
class Mal:
    def saludar():          # falta self
        print("hola")

Mal().saludar()
# TypeError: saludar() takes 0 positional arguments but 1 was given
```

Olvidar `self.` al acceder a un atributo crea o lee una variable local en su lugar, no el atributo de la instancia:

```python
class Caja:
    def __init__(self):
        valor = 10          # variable LOCAL, se pierde al terminar __init__
        # correcto: self.valor = 10
```

## Contraste con `cls`

En los métodos de clase (`@classmethod`), el primer parámetro por convención es `cls` y recibe **la clase**, no la instancia. La distinción método de instancia / método de clase / método estático se desarrolla en [[13 Metodos/index | Métodos]].

```python
class Registro:
    total = 0
    @classmethod
    def reset(cls):         # cls -> la clase Registro
        cls.total = 0
```
