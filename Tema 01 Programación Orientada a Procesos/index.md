---
title: Programación Orientada a Procesos
order: 0
draft: false
tags:
  - Index
  - Capitulo
aliases:
  - Programación Procedimental
  - Programación Procedural
---
# Programación Orientada a Procesos

Paradigma en el que un programa se expresa como una **secuencia de instrucciones** que transforman datos paso a paso. El flujo es **secuencial por defecto** (de arriba hacia abajo) y se altera únicamente mediante estructuras de control y llamadas a funciones. No hay objetos ni estado encapsulado: hay **datos** que viven en memoria y **procedimientos** que los manipulan.

Este capítulo cubre los fundamentos del lenguaje sobre los que se apoya todo lo demás —incluida la [[Python POO | Programación Orientada a Objetos]]—: el sistema de tipos, las colecciones, el control de flujo, la modularización en funciones y el manejo de errores.

## Modelo de ejecución

```mermaid
flowchart LR
    classDef etapa fill:#3b4252,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    D[Datos en memoria]:::etapa --> C[Estructuras de Control]:::etapa
    C --> F[Funciones]:::etapa
    F --> E[Manejo de Excepciones]:::etapa
    E --> R[Resultado]:::etapa
```

Un dato se declara, se opera mediante operadores y funciones, su flujo se decide con condicionales y bucles, y las situaciones anómalas se interceptan con excepciones. Cada módulo de este capítulo aísla una de esas piezas.

## Mapa del capítulo

| Módulo | Contenido | Nota madre |
| ------ | --------- | ---------- |
| 00 | Tablas de operadores y reglas de verdad transversales | [[00 Referencias/index \| Referencias]] |
| 10 | El sistema de tipos: primitivos, mutabilidad, conversión | [[10 Variables y Tipos de Datos/index \| Variables y Tipos de Datos]] |
| 20 | Colecciones: secuencias, mapas y conjuntos | [[20 Estructura de Datos/index \| Estructura de Datos]] |
| 30 | Decisión, repetición e interrupción del flujo | [[30 Estructuras de Control/index \| Estructuras de Control]] |
| 40 | Abstracción y reutilización mediante funciones | [[40 Funciones/index \| Funciones]] |
| 50 | Errores controlados: jerarquía, captura y lanzamiento | [[50 Manejo de Excepciones/index \| Manejo de Excepciones]] |

## Dependencias entre módulos

- **00 Referencias** y **10 Tipos** son la base: ningún otro módulo se entiende sin tipos y operadores.
- **20 Estructura de Datos** depende de la mutabilidad definida en 10.
- **30 Control** depende de los [[Valores Truthy y Falsy | valores de verdad]] (00) y de los iterables (20).
- **40 Funciones** integra todo lo anterior y agrega ámbitos propios.
- **50 Excepciones** es transversal: cualquier operación puede fallar y propagar un error por la pila de llamadas.
