---
title: Transformación de Tipos
order: 13
draft: false
tags:
  - python
  - teoria
  - transformacion-tipos
  - Index
aliases:
  - Conversión de Tipos
  - Type Conversion
---
# Transformación de Tipos

Cambio del tipo de un valor en Python. Se distinguen dos mecanismos: la **coerción**, que el intérprete aplica de forma automática siguiendo una jerarquía de promoción numérica, y el **casting**, que el programador fuerza mediante funciones constructoras. La diferencia operativa es quién decide y quién asume el riesgo: la coerción nunca pierde información ni falla; el casting puede **truncar** (`int(3.9) → 3`) o lanzar `ValueError` ante un dato mal formado.

```mermaid
flowchart LR
    classDef principal fill:#3b4252,stroke:#88c0d0,stroke-width:3px,color:#eceff4,font-weight:bold;
    classDef categoria fill:#434c5e,stroke:#81a1c1,stroke-width:2px,color:#eceff4;
    classDef subcategoria fill:#4c566a,stroke:#5e81ac,stroke-width:1.6px,color:#eceff4;
    classDef ejemplo fill:#2e3440,stroke:#5e81ac,stroke-width:1.2px,stroke-dasharray:3 3,color:#eceff4,font-size:12px;

    Title((Transformación de Tipos)):::principal

    Title --> Coercion["Conversión Implícita (Coerción)"]:::categoria
    Title --> Explicita["Conversión Explícita (Casting)"]:::categoria

    Coercion --> Coer1["Int → Float"]:::subcategoria
    Coercion --> Coer2["Bool → Int"]:::subcategoria
    Coercion --> Coer3["Promoción Numérica"]:::subcategoria

    Coer1 --> EjCoer1["`5 + 2.0 → 7.0`"]:::ejemplo
    Coer2 --> EjCoer2["`True + 5 → 6`"]:::ejemplo
    Coer3 --> EjCoer3["`int + complex → complex`"]:::ejemplo

    Explicita --> Constructores["Constructores: int() float() str() bool()"]:::subcategoria
    Explicita --> Colecciones["Colecciones: list() tuple() set() dict()"]:::subcategoria
    Explicita --> Caracteres["Caracteres: chr() ord()"]:::subcategoria
    Explicita --> Sistemas["Sistemas: bin() hex() oct()"]:::subcategoria

    linkStyle default stroke:#81a1c1,stroke-width:1.6px

```

## Mecanismos

- [[01 Conversion Implicita | Conversión implícita (coerción)]] — promoción automática `bool → int → float → complex` en operaciones aritméticas; `str` queda fuera de la cadena.
- [[02 Conversion Explicita | Conversión explícita (casting)]] — constructores `int()`, `float()`, `str()`, `bool()`, `list()`, `tuple()`, `set()`, `dict()`, `chr()`, `ord()`, más conversiones seguras con manejo de `ValueError`.

## Coerción vs casting

| Aspecto | Coerción (implícita) | Casting (explícito) |
|---------|----------------------|---------------------|
| **Quién la dispara** | El intérprete | El programador |
| **Dominio** | Solo tipos numéricos | Cualquier par de tipos compatibles |
| **Pérdida de información** | Nunca (promueve a mayor capacidad) | Posible (`int()` trunca decimales) |
| **Puede fallar** | No | Sí (`ValueError`, `TypeError`) |
| **Sintaxis** | Implícita en el operador | Función constructora `tipo(valor)` |
| **Ejemplo** | `5 + 2.0 → 7.0` | `int("100") → 100` |
