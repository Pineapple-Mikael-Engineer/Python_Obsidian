---
title: 12 Atributos
draft: false
description: El estado del objeto — atributos de instancia frente a atributos de clase y su almacenamiento en __dict__
tags:
  - Index
  - Tema
aliases:
  - Atributos
---
# Atributos

Los **atributos** son las variables ligadas a un objeto: constituyen su **estado**, los datos que distinguen una instancia de otra y que sus [[13 Metodos/index | métodos]] consultan y modifican. Toda definición de clase declara, implícita o explícitamente, qué atributos tendrán sus objetos.

La distinción fundamental es **dónde vive** el atributo:

- **De instancia:** propio de cada objeto. Dos instancias tienen valores independientes.
- **De clase:** definido en el cuerpo de la clase y **compartido** por todas las instancias.

```python
class Circulo:
    PI = 3.14159          # atributo de CLASE - compartido
    def __init__(self, r):
        self.radio = r    # atributo de INSTANCIA - propio

a = Circulo(1)
b = Circulo(2)
a.radio, b.radio          # 1, 2  -> independientes
a.PI is b.PI              # True   -> mismo objeto compartido
```

## Subtemas

- [[01 Atributos de Instancia | Atributos de Instancia]] — propios de cada objeto; se crean con `self.x = ...` y viven en el `__dict__` de la instancia.
- [[02 Atributos de Clase | Atributos de Clase]] — definidos en el cuerpo de la clase; compartidos por todas las instancias; útiles para constantes y contadores.
- [[03 Atributos Dinamicos y __dict__ | Atributos Dinámicos y __dict__]] — añadir o quitar atributos en tiempo de ejecución; `getattr/setattr`, `vars()` y el rol de `__dict__`.

## Instancia, clase y dinámicos

| Tipo | Dónde se define | Alcance | Almacenamiento |
| ---- | --------------- | ------- | -------------- |
| De instancia | `self.x = v` (típicamente en [[01 Atributos de Instancia \| `__init__`]]) | Propio de cada objeto | `instancia.__dict__` |
| De clase | En el cuerpo de la clase | Compartido por todas las instancias | `Clase.__dict__` |
| Dinámico | `obj.x = v` en cualquier momento | El objeto donde se asigna | `obj.__dict__` |

## Resolución de atributos

> [!info]
> Al evaluar `obj.x`, Python busca **primero en el `__dict__` de la instancia** y, si no lo halla, en el `__dict__` de la **clase** (y luego en sus bases, según el MRO de [[30 Herencia/index | herencia]]). Por eso un atributo de instancia con el mismo nombre **sombrea** al de clase.

Esta jerarquía de búsqueda es la que vuelve transparente leer una constante de clase a través de cualquier instancia, y la que explica el efecto de sombreado al asignar `obj.x = v`. El detalle del sombreado y sus trampas se trata en [[02 Atributos de Clase | Atributos de Clase]].
