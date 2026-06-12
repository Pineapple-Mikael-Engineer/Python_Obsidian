---
title: CoolProp — propiedades termodinámicas de fluidos
aliases: [CoolProp, introduccion]
tags: [coolprop, indice]
draft: false
---

# CoolProp — propiedades termodinámicas de fluidos

CoolProp calcula **propiedades termodinámicas y de transporte** de fluidos puros, pseudopuros y mezclas (agua, aire húmedo, refrigerantes, CO₂…). La idea de fondo es un principio de la termodinámica: el **estado** de un fluido puro queda **definido por dos propiedades independientes** (p. ej. presión y temperatura); fijadas esas dos, CoolProp deriva todas las demás —densidad, entalpía, entropía, calidad de vapor, calores específicos, etc.—.

Ofrece dos interfaces para lo mismo, según cuántas propiedades necesites del mismo estado:

## En acción

```python
from CoolProp.CoolProp import PropsSI, AbstractState
import CoolProp

# Alto nivel: una propiedad por llamada (rapido de escribir)
h = PropsSI("H", "T", 300, "P", 101325, "Water")   # entalpia masica [J/kg]
Tsat = PropsSI("T", "P", 101325, "Q", 0, "Water")  # temperatura de saturacion [K]

# Bajo nivel: un objeto de estado, mucho mas rapido para muchas consultas
state = AbstractState("HEOS", "Water")
state.update(CoolProp.PT_INPUTS, 101325, 300)      # fija el estado (P, T)
state.hmass(), state.rhomass(), state.smass()      # todas las propiedades de ese estado
```

## Las dos interfaces

```mermaid
flowchart TD
    Q{{"¿Cuántas propiedades del mismo estado necesito?"}}
    Q -->|"una consulta puntual"| PS(["CoolProp.PropsSI"])
    Q -->|"muchas del mismo estado o en bucles"| AS["AbstractState"]
    AS --> U["update(par, v1, v2) — fija el estado"]
    U --> P(["T() · p() · rhomass() · hmass() · smass()..."])

    classDef pregunta fill:#5e81ac,stroke:#88c0d0,stroke-width:2px,color:#eceff4;
    classDef grupo fill:#3b4252,stroke:#81a1c1,stroke-width:1.5px,color:#88c0d0;
    classDef hoja fill:#2e3440,stroke:#a3be8c,color:#d8dee9;
    class Q pregunta;
    class AS,U grupo;
    class PS,P hoja;
```

`PropsSI` recompila el estado en cada llamada; `AbstractState` lo fija una vez y reutiliza, por lo que es mucho más eficiente cuando pides varias propiedades o iteras sobre miles de estados.

## Qué contiene el vault

| Nota / carpeta | Qué aporta |
|----------------|-----------|
| [[CoolProp.PropsSI]] | La función de **alto nivel**: una propiedad por llamada. El punto de entrada habitual |
| [[AbstractState]] | El objeto de **bajo nivel**: fija un estado y consulta muchas propiedades; soporta mezclas |
| [[CoolProp/AbstractState_metodos/index\|AbstractState_metodos]] | Los métodos del objeto: `update`, propiedades (`T`, `p`, `hmass`…), saturación, derivadas |
| [[Constants]] | Los pares de entrada (`PT_INPUTS`, `QT_INPUTS`…) y las claves de propiedad |
| [[CoolProp/Plots/index\|Plots]] | Diagramas termodinámicos (P-h, T-s…) con isolíneas vía `PropertyPlot` |

## Notas relacionadas

- [[CoolProp.PropsSI]] — el primer paso para la mayoría de cálculos
- [[AbstractState]] — la vía eficiente y para mezclas
- [[Tree CoolProp]] — mapa completo del vault
