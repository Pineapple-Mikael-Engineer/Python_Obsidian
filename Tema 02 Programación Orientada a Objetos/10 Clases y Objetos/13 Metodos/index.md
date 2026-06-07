---
title: Métodos
draft: false
description: El comportamiento del objeto — métodos de instancia, de clase y estáticos según su primer parámetro
tags:
  - Index
  - Tema
aliases:
  - Métodos
  - Metodos
---
# Métodos

Los **métodos** son el **comportamiento** de un objeto: funciones definidas dentro del cuerpo de una clase. Python distingue **tres tipos** según qué reciben como **primer parámetro** —la instancia, la clase o nada— y según el decorador que los marca. Esa diferencia determina a qué estado pueden acceder.

```python
class Circulo:
    PI = 3.1416                          # atributo de clase
    def __init__(self, radio):
        self.radio = radio               # estado de instancia
    def area(self):                      # método de INSTANCIA (self)
        return Circulo.PI * self.radio ** 2
    @classmethod
    def unitario(cls):                   # método de CLASE (cls)
        return cls(1)
    @staticmethod
    def valido(radio):                   # método ESTÁTICO (nada)
        return radio > 0
```

El primer parámetro es lo único que cambia su naturaleza: `self` enlaza la instancia, `cls` enlaza la clase, y la ausencia de ambos convierte al método en una función ordinaria que solo vive dentro del *namespace* de la clase. La referencia explícita a la instancia se detalla en [[03 El parametro self | El parámetro self]].

## Subtemas

- [[01 Metodos de Instancia | Métodos de Instancia]] — el tipo por defecto; reciben `self` y operan sobre el estado de la instancia.
- [[02 Metodos de Clase (classmethod) | Métodos de Clase]] — decorados con `@classmethod`; reciben `cls`; su uso estrella son los **constructores alternativos**.
- [[03 Metodos Estaticos (staticmethod) | Métodos Estáticos]] — decorados con `@staticmethod`; no reciben `self` ni `cls`; funciones agrupadas por cohesión.

## Los tres tipos de un vistazo

| Tipo | Recibe | Decorador | Accede al estado | Uso típico |
| ---- | ------ | --------- | ---------------- | ---------- |
| Instancia | `self` (la instancia) | ninguno | Instancia **y** clase | Operar sobre los datos de un objeto concreto |
| Clase | `cls` (la clase) | `@classmethod` | Solo clase | Constructores alternativos / fábricas |
| Estático | nada | `@staticmethod` | Ninguno | Utilidad relacionada, sin tocar el estado |

## Categoría aparte: métodos especiales (dunder)

Los **métodos especiales** o *dunder* (`__init__`, `__str__`, `__eq__`, `__len__`...) son métodos de instancia con nombre reservado que Python invoca **implícitamente** ante ciertas operaciones del lenguaje (construcción, impresión, comparación, indexado). No constituyen un cuarto tipo: son métodos de instancia con un contrato especial. Se tratan en [[50 Metodos Especiales (Dunder)/index | Métodos Especiales]].

El comportamiento aquí descrito opera sobre el estado descrito en [[12 Atributos/index | Atributos]].
