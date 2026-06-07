---
title: Glosario POO
order: 2
tags:
  - python
  - referencia
  - poo
draft: false
aliases:
  - Glosario de Programación Orientada a Objetos
  - Términos POO
---

# Glosario POO

Definiciones breves de los términos del paradigma orientado a objetos en Python. Entrada de consulta para fijar el significado preciso; el desarrollo de cada concepto se delega a su sección. El catálogo de métodos `__x__` referidos aquí está en [[Catalogo de Metodos Dunder | Catálogo de Métodos Dunder]].

## Entidades fundamentales

| Término | Definición breve |
| ------- | ---------------- |
| Clase | Plantilla que define atributos y métodos comunes a un conjunto de objetos. Definida con `class`. Ver [[10 Clases y Objetos/index | Clases y Objetos]] |
| Objeto / instancia | Entidad concreta creada a partir de una clase, con estado propio. Resultado de `Clase(...)` |
| Atributo de instancia | Dato ligado a una instancia concreta (`self.x`); independiente entre objetos |
| Atributo de clase | Dato compartido por todas las instancias, definido en el cuerpo de la clase |
| Método de instancia | Función definida en la clase que recibe `self`; opera sobre el estado del objeto |
| Método de clase | Recibe `cls` en lugar de `self`; decorado con `@classmethod`. Opera sobre la clase |
| Método estático | Sin `self` ni `cls`; decorado con `@staticmethod`. Función agrupada en la clase por contexto |
| `self` | Referencia convencional a la instancia sobre la que se invoca un método de instancia |
| `cls` | Referencia convencional a la clase en un método de clase |
| Constructor / inicializador | `__new__` crea la instancia (constructor); `__init__` la inicializa (inicializador) |

## Encapsulamiento

| Término | Definición breve |
| ------- | ---------------- |
| Encapsulamiento | Ocultar el estado interno y exponer una interfaz controlada de acceso. Ver [[20 Encapsulamiento/index | Encapsulamiento]] |
| Name mangling | Reescritura de `__attr` a `_Clase__attr` por el intérprete, para evitar colisiones en herencia |
| Property | Atributo gestionado por métodos *getter*/*setter*/*deleter* vía `@property`; acceso con sintaxis de atributo |

## Herencia y jerarquía

| Término | Definición breve |
| ------- | ---------------- |
| Herencia | Mecanismo por el que una subclase reutiliza y extiende atributos y métodos de una superclase. Ver [[30 Herencia/index | Herencia]] |
| Herencia simple | Una subclase deriva de una única superclase |
| Herencia multinivel | Cadena de herencia en varios niveles (A → B → C) |
| Herencia múltiple | Una subclase deriva de dos o más superclases a la vez |
| `super()` | Acceso cooperativo al siguiente método según el MRO; encadena las superclases |
| MRO | *Method Resolution Order*: orden lineal (algoritmo C3) en que se buscan atributos y métodos en la jerarquía |
| Sobrescritura (*override*) | Redefinir en la subclase un método heredado de la superclase |

## Polimorfismo

| Término | Definición breve |
| ------- | ---------------- |
| Polimorfismo | Capacidad de invocar la misma operación sobre objetos de tipos distintos con comportamiento específico. Ver [[40 Polimorfismo/index | Polimorfismo]] |
| Duck typing | El tipo se determina por los métodos/atributos que el objeto soporta, no por su clase declarada |
| Sobrecarga de operadores | Definir el comportamiento de operadores (`+`, `==`, ...) en una clase mediante métodos dunder |
| Método dunder | Método especial `__x__` invocado implícitamente por sintaxis o funciones incorporadas |

## Abstracción

| Término | Definición breve |
| ------- | ---------------- |
| Clase abstracta | Clase que no se instancia directamente; define una interfaz parcial. Base `ABC`. Ver [[60 Abstraccion/index | Abstracción]] |
| `abstractmethod` | Decorador que marca un método obligatorio de implementar en las subclases concretas |
| Interfaz | Contrato de métodos que una clase debe ofrecer; en Python, informal (duck typing) o vía clase abstracta |

## Relaciones entre objetos

| Término | Definición breve |
| ------- | ---------------- |
| Composición | Relación todo-parte fuerte: la parte no existe sin el todo y se destruye con él. Ver [[70 Relaciones entre Objetos/index | Relaciones entre Objetos]] |
| Agregación | Relación todo-parte débil: la parte existe independientemente del todo |
| Asociación | Relación de uso entre objetos con ciclos de vida independientes |
| Dependencia | Relación transitoria: un objeto usa otro de forma puntual (parámetro, variable local) |
| Mixin | Clase que aporta funcionalidad concreta por herencia múltiple, sin instanciarse por sí sola |

## Herramientas modernas

| Término | Definición breve |
| ------- | ---------------- |
| Dataclass | Clase decorada con `@dataclass` que autogenera `__init__`, `__repr__`, `__eq__`, etc. Ver [[90 Herramientas Modernas/index | Herramientas Modernas]] |
| `__slots__` | Declaración que fija los atributos permitidos, elimina el `__dict__` por instancia y reduce memoria |
