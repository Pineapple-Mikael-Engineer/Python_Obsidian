---
title: 10 Clases y Objetos
draft: false
description: El molde y la instancia — definición de clases, atributos y métodos
tags:
  - Index
  - Tema
aliases:
  - Clases y Objetos
---
# Clases y Objetos

Una **clase** es la plantilla que describe una categoría de objetos: declara qué **atributos** (estado) y qué **métodos** (comportamiento) tendrán sus instancias. Un **objeto** —o **instancia**— es una materialización concreta de esa plantilla, con valores propios para sus atributos. La clase se define una vez; de ella se crean tantos objetos como se necesite.

```python
class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular     # atributo de instancia
        self.saldo = saldo
    def depositar(self, monto):    # método de instancia
        self.saldo += monto

c = CuentaBancaria("Ana", 100)     # instancia
c.depositar(50)                    # invocación del comportamiento
c.saldo                            # 150
```

## Subtemas

- [[11 Definicion de Clases/index | Definición de Clases]] — la sentencia `class`, cómo se crean instancias, el papel de `self` y el constructor `__init__`.
- [[12 Atributos/index | Atributos]] — el estado del objeto: atributos de instancia frente a atributos de clase y su almacenamiento en `__dict__`.
- [[13 Metodos/index | Métodos]] — el comportamiento: métodos de instancia, de clase (`@classmethod`) y estáticos (`@staticmethod`).

## Anatomía de una clase

| Elemento | Qué define | Subtema |
| -------- | ---------- | ------- |
| `class Nombre:` | El molde | [[11 Definicion de Clases/index \| Definición de Clases]] |
| `__init__` | Inicialización del estado | [[11 Definicion de Clases/index \| Definición de Clases]] |
| `self.x` | Atributo de instancia | [[12 Atributos/index \| Atributos]] |
| atributo en el cuerpo | Atributo de clase (compartido) | [[12 Atributos/index \| Atributos]] |
| `def metodo(self):` | Comportamiento | [[13 Metodos/index \| Métodos]] |

El acceso a esos atributos puede protegerse mediante [[20 Encapsulamiento/index | encapsulamiento]], y el comportamiento puede extenderse por [[30 Herencia/index | herencia]].
