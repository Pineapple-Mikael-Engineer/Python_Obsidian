---
title: 80 Patrones de Diseño
draft: false
description: Soluciones reutilizables a problemas recurrentes de diseño orientado a objetos
tags:
  - Index
  - Tema
aliases:
  - Patrones de Diseño
  - Design Patterns
---
# Patrones de Diseño

Un **patrón de diseño** es una solución probada y reutilizable a un problema recurrente en el diseño orientado a objetos. No es código que se copia, sino una **plantilla de organización** de clases y objetos que resuelve un tipo de problema (crear objetos, asignar responsabilidades, coordinar colaboraciones). Conocerlos da un vocabulario común y evita reinventar soluciones frágiles.

Python, por ser dinámico y tener funciones de primera clase, a menudo **simplifica** patrones que en lenguajes estáticos requieren mucha infraestructura: una función ya es una *strategy*, un módulo ya es un *singleton*.

## Subtemas

- [[01 Singleton | Singleton]] — garantizar una **única instancia** global de una clase.
- [[02 Factory Method | Factory Method]] — delegar la **creación** de objetos a un método, desacoplando del tipo concreto.
- [[03 Strategy | Strategy]] — encapsular **algoritmos intercambiables** y seleccionarlos en tiempo de ejecución.
- [[04 Observer | Observer]] — notificar automáticamente a múltiples objetos cuando **cambia el estado** de otro.

## Clasificación

| Patrón | Tipo | Problema que resuelve | Subtema |
| ------ | ---- | --------------------- | ------- |
| Singleton | Creacional | Una sola instancia compartida | [[01 Singleton \| Singleton]] |
| Factory Method | Creacional | Crear sin acoplar al tipo concreto | [[02 Factory Method \| Factory Method]] |
| Strategy | De comportamiento | Intercambiar algoritmos | [[03 Strategy \| Strategy]] |
| Observer | De comportamiento | Propagar cambios de estado | [[04 Observer \| Observer]] |

Estos patrones se construyen sobre los pilares del tema: la [[30 Herencia/index | herencia]] y el [[40 Polimorfismo/index | polimorfismo]] para variar comportamiento, y la [[70 Relaciones entre Objetos/index | composición]] para vincular objetos colaboradores.
