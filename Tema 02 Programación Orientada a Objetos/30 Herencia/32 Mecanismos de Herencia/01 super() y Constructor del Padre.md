---
title: super() y Constructor del Padre
order: 1
tags:
  - python
  - teoria
  - herencia
draft: false
aliases:
  - super()
  - Constructor del Padre
  - Llamar al padre
---

# `super()` y el Constructor del Padre

> [!definicion]
> **`super()`** devuelve un objeto **proxy** a la(s) superclase(s) de la clase actual, siguiendo el orden de resolución de métodos ([[33 MRO y super() Cooperativo/index | MRO]]). A través de ese proxy se invoca cualquier método del padre **con `self` ya enlazado**. Su uso canónico es `super().__init__(...)` dentro del `__init__` de la subclase: inicializar primero la parte heredada y después añadir el estado propio.

```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre

class Perro(Animal):
    def __init__(self, nombre, raza):
        super().__init__(nombre)   # inicializa la parte heredada
        self.raza = raza           # añade lo propio

p = Perro("Toby", "Labrador")
p.nombre, p.raza                   # ('Toby', 'Labrador')
```

Sin la llamada a `super().__init__(nombre)`, el `__init__` de la subclase **reemplaza** al del padre por completo: `self.nombre` nunca se asignaría y el objeto quedaría a medio inicializar.

## Patrón canónico en `__init__`

La regla de orden es estricta: **primero el padre, después lo propio**. El estado del padre debe existir antes de que la subclase lo use o lo amplíe.

```python
class Cuenta:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

class CuentaAhorro(Cuenta):
    def __init__(self, titular, saldo=0, tasa=0.02):
        super().__init__(titular, saldo)   # 1. parte heredada
        self.tasa = tasa                   # 2. estado propio

CuentaAhorro("Ana", 1000, 0.03).saldo      # 1000
```

> [!regla]
> En el `__init__` de una subclase, llamar a `super().__init__(...)` **antes** de tocar atributos heredados. Pasar al padre solo los argumentos que él define; los específicos de la subclase se asignan después.

## Invocar cualquier método del padre

`super()` no se limita al constructor: da acceso a la versión del padre de **cualquier** método, incluso uno que la subclase sobrescribe. Esa es la base de la [[03 Extension de Metodos | extensión de métodos]].

```python
class Cuenta:
    def resumen(self):
        return f"{self.titular}: {self.saldo}"

class CuentaAhorro(Cuenta):
    def resumen(self):
        base = super().resumen()           # versión del padre
        return f"{base} (tasa {self.tasa})"
```

## Por qué `super()` sin argumentos

En Python 3, `super()` dentro de un método se equivale a `super(ClaseActual, self)`: el intérprete inyecta la clase y la instancia automáticamente. Frente a la forma explícita `Base.__init__(self, ...)`, `super()` es preferible por tres razones.

> [!info]
> - **No fija el nombre del padre.** Si la base cambia o se reordena la jerarquía, `super()` se adapta; `Base.__init__` queda obsoleto y hay que editarlo a mano.
> - **Respeta el MRO.** En [[31 Tipos de Herencia/index | herencia múltiple]], `Base.__init__(self, ...)` salta directamente a una base concreta y puede **omitir** o **duplicar** la inicialización de otras; `super()` recorre la cadena del [[33 MRO y super() Cooperativo/index | MRO]] una sola vez.
> - **Cooperación.** Solo `super()` permite el patrón [[02 super() Cooperativo]], donde cada clase delega en la siguiente del MRO sin conocerla.

```python
class Base:
    def __init__(self):
        self.x = 1

class Derivada(Base):
    def __init__(self):
        Base.__init__(self)   # frágil: nombre fijo, ignora el MRO
        super().__init__()    # robusto: sigue el MRO  (preferido)
```

> [!warning]
> `Base.__init__(self, ...)` solo es aceptable en herencia simple y trivial. En cuanto entra un segundo padre, mezclar la forma explícita con `super()` produce inicializaciones perdidas o repetidas. No combinarlas en una misma jerarquía.

## Relación con otras notas

`super()` es el mecanismo común a la [[02 Sobrescritura de Metodos (override) | sobrescritura]] (cuando se decide reaprovechar algo del padre) y a la [[03 Extension de Metodos | extensión]]. Su semántica completa en presencia de varios padres se desarrolla en [[33 MRO y super() Cooperativo/index | MRO y super() Cooperativo]]. El `__init__` que aquí se invoca se trata como concepto propio en [[04 Constructor __init__]].
