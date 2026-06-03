---
title: 32 Mecanismos de Herencia
draft: false
description: Cómo una subclase reutiliza, reemplaza o amplía lo heredado
tags:
  - Index
  - Tema
aliases:
  - Mecanismos de Herencia
  - Inheritance Mechanisms
---
# Mecanismos de Herencia

Heredar no es solo recibir atributos y métodos del padre: es decidir, miembro a miembro, **qué hacer con cada uno**. Una subclase dispone de tres operaciones sobre lo heredado: **reutilizarlo** tal cual (no escribir nada), **reemplazarlo** por una versión propia (*override*) o **ampliarlo** llamando primero al padre y añadiendo comportamiento (extensión). El pivote de las dos últimas es `super()`, el proxy que da acceso a la implementación de la superclase.

```python
class Animal:
    def __init__(self, nombre):
        self.nombre = nombre
    def hablar(self):
        return "..."

class Perro(Animal):
    def __init__(self, nombre, raza):
        super().__init__(nombre)   # REUTILIZA la inicialización del padre
        self.raza = raza           # AMPLÍA con estado propio
    def hablar(self):              # REEMPLAZA el método del padre
        return "Guau"

Perro("Toby", "Labrador").hablar()  # "Guau"
```

## Subtemas

- [[01 super() y Constructor del Padre | super() y Constructor del Padre]] — `super()` como proxy a la superclase; uso canónico en `__init__` para inicializar la parte heredada antes de añadir lo propio.
- [[02 Sobrescritura de Metodos (override) | Sobrescritura de Métodos (override)]] — redefinir un método del padre con la misma firma; base del polimorfismo de subtipos.
- [[03 Extension de Metodos | Extensión de Métodos]] — caso de *override* que no reemplaza por completo: llama a `super()` y añade comportamiento.

## Las tres operaciones

| Operación | Qué escribe la subclase | Resultado al llamar sobre la subclase | Nota |
| --------- | ----------------------- | ------------------------------------- | ---- |
| Reutilizar | nada | corre la versión heredada del padre | herencia pura |
| Reemplazar (*override*) | método nuevo, misma firma, **sin** `super()` | corre solo la versión de la subclase | [[02 Sobrescritura de Metodos (override) \| override]] |
| Ampliar (extensión) | método nuevo que **llama** a `super().metodo()` | corre el del padre **más** lo añadido | [[03 Extension de Metodos \| extensión]] |

`super()` es transversal a las dos últimas: sin él no hay forma limpia de invocar la implementación del padre desde la subclase. Su comportamiento exacto en herencia múltiple lo fija el [[33 MRO y super() Cooperativo/index | MRO]].

El *override* es lo que vuelve útil la herencia para el [[40 Polimorfismo/index | polimorfismo]]: una misma llamada se resuelve a la implementación de la clase real del objeto. La distinción entre reemplazar y ampliar es la decisión de diseño central de este apartado.
