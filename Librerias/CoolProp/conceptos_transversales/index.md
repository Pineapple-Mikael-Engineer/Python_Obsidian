---
title: Conceptos transversales — el modelo mental de CoolProp
aliases:
  - conceptos CoolProp
  - modelo mental CoolProp
tags:
  - coolprop
  - indice
draft: false
---

# Conceptos transversales — el modelo mental de CoolProp

Antes de llamar a una sola función conviene entender los **tres conceptos** sobre los que se apoya todo CoolProp. No son secundarios: son el modelo mental que explica *por qué* las funciones piden lo que piden. Quien los tiene claros lee cualquier ejemplo de [[CoolProp.PropsSI]] o [[AbstractState]] sin sorpresas.

## La idea en tres piezas

```mermaid
flowchart LR
    E["1 · Estado termodinamico — defino el fluido con DOS propiedades"]
    B["2 · Backend — el motor que calcula esas propiedades"]
    S["3 · Propiedades SI — claves y unidades de entrada/salida"]
    E -->|"dame T,P (o P,Q...)"| B
    B -->|"devuelve D,H,S... en SI"| S

    classDef pregunta fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class E pregunta;
    class B grupo;
    class S hoja;
```

| Concepto | Idea |
|----------|------|
| [[concepto_estado_termodinamico]] | El estado de un fluido puro queda **completamente definido por DOS propiedades independientes**; fijadas dos, todas las demás quedan determinadas |
| [[concepto_backend]] | CoolProp separa *qué* propiedad quieres de *con qué modelo* se calcula; el **backend** (`HEOS`, `IF97`, `REFPROP`...) es ese motor intercambiable |
| [[concepto_propiedades_SI]] | Cada propiedad tiene una **clave string** (`'T'`, `'P'`, `'D'`, `'H'`...) y CoolProp trabaja **siempre en SI estricto** (Pa, K, J/kg) |

## Cómo encajan

El flujo de cualquier cálculo es siempre el mismo: **defines el estado con dos propiedades** independientes (por ejemplo presión y temperatura), **el backend resuelve** la ecuación de estado del fluido a partir de ese par, y **el resultado sale en unidades SI** identificado por su clave. Las tres piezas son inseparables: sin dos propiedades el estado no existe, sin backend nadie las relaciona, y sin la convención SI los números no significan nada. Las funciones de alto y bajo nivel ([[CoolProp.PropsSI]] y [[AbstractState]]) son solo dos formas de recorrer este mismo flujo.

## Notas relacionadas

- [[concepto_estado_termodinamico]] — la regla de las dos propiedades
- [[concepto_backend]] — el motor de cálculo intercambiable
- [[concepto_propiedades_SI]] — claves y unidades
- [[CoolProp.PropsSI]] — la interfaz de alto nivel que aplica estos conceptos
- [[AbstractState]] — la interfaz de bajo nivel
