---
title: backend.IF97 — IAPWS-IF97 industrial para agua y vapor (rapido)
aliases:
  - IF97
  - IAPWS-IF97
  - backend de vapor
tags:
  - coolprop
  - backend
  - if97
lib: coolprop
tipo: concepto
draft: false
---

# backend.IF97 — IAPWS-IF97 para agua y vapor

`IF97` es el [[concepto_backend|backend]] que implementa la **formulación industrial IAPWS-IF97**, el estándar internacional para las propiedades del agua y el vapor en la industria de potencia (turbinas de vapor, calderas, centrales térmicas). Su gran virtud es la **velocidad**: está diseñado para evaluarse muchísimas veces por segundo. Su gran limitación es que **solo sirve para agua**.

## Qué modelo usa

A diferencia de [[backend.HEOS|HEOS]], que parte de una única función fundamental de Helmholtz y resuelve iterativamente, IF97 divide el diagrama del agua en **regiones** (líquido, vapor, supercrítica, saturación, alta temperatura) y da en cada una **correlaciones explícitas** ajustadas para que el cálculo sea directo, sin iterar. Por eso es tan rápido: no resuelve ecuaciones, las evalúa.

Es la formulación que usan los códigos comerciales de simulación de ciclos de vapor, así que elegir IF97 también significa **hablar el mismo idioma** que la industria de turbinas.

## Sintaxis

```python
from CoolProp.CoolProp import PropsSI

rho = PropsSI('D', 'T', 300, 'P', 1e5, 'IF97::Water')   # -> 996.5574824996613
```

Con [[AbstractState]], el backend es el primer argumento del constructor:

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('IF97', 'Water')
state.update(CP.PT_INPUTS, 1e5, 300)
print(state.rhomass())                                   # -> 996.557... kg/m3
```

## IF97 frente a HEOS: misma respuesta, mucho más rápido

Para agua, IF97 y [[backend.HEOS|HEOS]] dan prácticamente la **misma densidad** (la diferencia está muy por debajo de lo relevante en ingeniería), pero IF97 es **mucho más barato** de evaluar. Verificado en este entorno:

| Condición | `IF97::Water` | `HEOS::Water` | Diferencia |
|-----------|---------------|----------------|-----------|
| 300 K, 1 bar (líquido) | `996.5574824996613` | `996.5563403889159` | ~0.0001 % |
| 773.15 K, 10 MPa (vapor recalentado) | `30.475853366923843` | `30.477869948390932` | ~0.007 % |

```python
import time
from CoolProp.CoolProp import PropsSI

N = 20000
t = time.time()
for _ in range(N): PropsSI('D', 'T', 300, 'P', 1e5, 'IF97::Water')
print('IF97:', time.time() - t)    # -> ~0.105 s

t = time.time()
for _ in range(N): PropsSI('D', 'T', 300, 'P', 1e5, 'HEOS::Water')
print('HEOS:', time.time() - t)    # -> ~1.497 s  (≈ 14x mas lento)
```

Verificado: 20 000 llamadas tardaron **0.105 s con IF97** frente a **1.497 s con HEOS**, es decir IF97 fue del orden de **14 veces más rápido** dando esencialmente el mismo número.

## Cuándo preferirla

- **Cálculos masivos de ciclos de vapor**: barridos de miles de estados en un ciclo Rankine, mapas de turbina, optimización de calderas. Aquí los 14x de velocidad se notan.
- Cuando trabajas en un contexto **industrial de potencia** y quieres alinearte con el estándar IAPWS-IF97 que usan los demás códigos.

## Limitación: solo agua

IF97 es una formulación **exclusiva del agua**. No existe `'IF97::R134a'` ni `'IF97::CarbonDioxide'`: para cualquier otro fluido tienes que volver a [[backend.HEOS|HEOS]] (o la cúbica que corresponda). Si tu cálculo mezcla agua con otros fluidos, IF97 no es una opción para esos otros componentes.

> [!warning] No uses IF97 fuera del agua
> El backend solo está definido para `Water`. Pedirlo con otro fluido falla o no tiene sentido físico. Para todo lo que no sea agua, el default [[backend.HEOS|HEOS]] es el punto de partida.

## Notas relacionadas

- [[concepto_backend]] — qué es un backend y la sintaxis `BACKEND::Fluido`
- [[backend.HEOS]] — el motor general por defecto, la alternativa para agua de máxima generalidad
- [[CoolProp.PropsSI]] — donde se escribe el prefijo `IF97::`
- [[AbstractState]] — el backend es el primer argumento del constructor
