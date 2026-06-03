---
title: 33 MRO y super() Cooperativo
draft: false
description: El orden de resolución de métodos (C3) y cómo super() coopera en herencia múltiple
tags:
  - Index
  - Tema
aliases:
  - MRO y super Cooperativo
  - Method Resolution Order
---
# MRO y super() Cooperativo

Con [[03 Herencia Multiple | herencia múltiple]] aparece la ambigüedad: si dos bases definen el mismo método o atributo, Python necesita un **orden determinista** para decidir cuál gana. Ese orden es el **MRO** (*Method Resolution Order*), una secuencia lineal calculada por el algoritmo **C3**. La función `super()` no salta "al padre", sino al **siguiente en ese MRO**, lo que permite que una cadena de clases coopere y cada una ejecute su parte **una sola vez** (herencia cooperativa).

```python
class A: ...
class B(A): ...
class C(A): ...
class D(B, C): ...        # diamante

D.__mro__                 # (D, B, C, A, object)  -> orden lineal y único
```

## Subtemas

- [[01 MRO (Method Resolution Order) | MRO (Method Resolution Order)]] — la secuencia lineal de búsqueda; algoritmo C3, propiedades, `__mro__` y el problema del diamante.
- [[02 super() Cooperativo | super() Cooperativo]] — `super()` recorre el MRO, no la jerarquía; cómo encadenar mixins con firmas compatibles.

## Mapa del subtema

| Concepto | Pregunta que responde | Hoja |
| -------- | --------------------- | ---- |
| MRO / C3 | Con varios padres, ¿en qué orden se busca? | [[01 MRO (Method Resolution Order) \| MRO]] |
| `super()` cooperativo | ¿Cómo llamo al *siguiente* y encadeno mixins? | [[02 super() Cooperativo \| super() Cooperativo]] |

```mermaid
flowchart TD
    classDef base fill:#2e3440,stroke:#5e81ac,stroke-width:2px,color:#eceff4,font-weight:bold;
    classDef der fill:#3b4252,stroke:#88c0d0,color:#eceff4;
    A[A]:::base --> B[B]:::der
    A --> C[C]:::der
    B --> D[D]:::der
    C --> D
```

El MRO es la pieza que cierra los [[32 Mecanismos de Herencia/index | Mecanismos de Herencia]]: define exactamente qué resuelve cada llamada cuando el grafo deja de ser una simple cadena.
</content>
</invoke>
