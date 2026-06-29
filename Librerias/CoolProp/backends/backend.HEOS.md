---
title: backend.HEOS — Helmholtz Equation of State (el backend por defecto)
aliases:
  - HEOS
  - Helmholtz Equation of State
  - backend por defecto
tags:
  - coolprop
  - backend
  - heos
lib: coolprop
tipo: concepto
draft: false
---

# backend.HEOS — Helmholtz Equation of State

`HEOS` es el **backend por defecto** de CoolProp y el más general y preciso de los que vienen incluidos. Es el [[concepto_backend|backend]] que se usa cuando no escribes ningún prefijo: `'Water'` y `'HEOS::Water'` son exactamente lo mismo. Si no tienes una razón concreta para elegir otro motor, este es el correcto.

## Qué modelo usa

HEOS implementa **ecuaciones de estado multiparamétricas de Helmholtz**: toma la energía libre de Helmholtz `a(T, ρ)` como función fundamental y deriva de ella **todas** las propiedades termodinámicas (presión, entalpía, entropía, calores específicos, velocidad del sonido…) por diferenciación analítica exacta. Como la función fundamental se ajusta a datos experimentales fluido a fluido, la precisión es la mejor que puede ofrecer CoolProp sin recurrir a [[backend.REFPROP|REFPROP]].

Cada fluido tiene su propia ecuación ajustada: la del agua es la formulación de referencia IAPWS-95, la del CO₂ es la de Span-Wagner, etc. Por eso HEOS es a la vez **general** (un mismo backend cubre cientos de fluidos) y **preciso** (cada uno con su correlación específica).

## Cobertura

HEOS cubre la inmensa mayoría de fluidos de CoolProp:

| Tipo de fluido | Ejemplo | Soportado |
|----------------|---------|-----------|
| Fluido puro | `'HEOS::Water'`, `'HEOS::CarbonDioxide'` | Sí |
| Pseudopuro | `'HEOS::Air'` | Sí (tratado como una sustancia) |
| Mezcla | `'HEOS::R32&R134a'` | Sí (con fracciones) |

## Sintaxis

```python
from CoolProp.CoolProp import PropsSI

# Las tres formas siguientes son equivalentes: HEOS es el default
rho1 = PropsSI('D', 'T', 300, 'P', 1e5, 'Water')         # -> 996.5563403889159
rho2 = PropsSI('D', 'T', 300, 'P', 1e5, 'HEOS::Water')   # -> 996.5563403889159
print(rho1 == rho2)                                       # -> True
```

Verificado: ambas llamadas devuelven `996.5563403889159` kg/m³, idénticas. Escribir `HEOS::` es redundante salvo que quieras documentar de forma explícita qué motor usas.

Como primer argumento del constructor de [[AbstractState]], es igual de explícito:

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')   # backend HEOS, fluido agua
state.update(CP.PT_INPUTS, 1e5, 300)
print(state.rhomass())                       # -> 996.5563403889159
```

## Cuándo usarlo

- **Por defecto, siempre que no tengas un motivo para cambiar.** Es la opción segura.
- Cuando necesitas **máxima precisión** y no tienes licencia de [[backend.REFPROP|REFPROP]].
- Para **cualquier fluido distinto del agua** donde quieras resultados fiables (refrigerantes, CO₂, hidrocarburos, nitrógeno…).
- Para **mezclas** con modelos de calidad.

## El coste

HEOS es el motor más completo, y eso se paga en velocidad. Las ecuaciones multiparamétricas y la resolución iterativa que requieren los pares de entrada que no son `(T, ρ)` lo hacen **más lento** que las alternativas especializadas:

- Frente a [[backend.IF97|IF97]] para agua, HEOS es del orden de **14 veces más lento** (medido en este entorno: 20 000 llamadas tardaron 1.50 s con HEOS frente a 0.105 s con IF97).
- Frente a las ecuaciones cúbicas como [[backend.SRK|SRK]], también es más caro por evaluación.

Por eso, en cálculos masivos de **ciclos de vapor** se prefiere IF97, y en estudios **cualitativos** de gases o mezclas se recurre a las cúbicas. Para todo lo demás, el coste de HEOS está más que justificado por su precisión.

> [!tip] Para muchas consultas del mismo estado, no es el backend lo que cambia, sino la interfaz
> Si llamas miles de veces, fija el estado una vez con [[AbstractState]] en lugar de repetir [[CoolProp.PropsSI|PropsSI]]. El backend sigue siendo HEOS; solo evitas recompilar el estado en cada llamada.

## Notas relacionadas

- [[concepto_backend]] — qué es un backend y la sintaxis `BACKEND::Fluido`
- [[backend.IF97]] — la alternativa rápida, solo para agua
- [[backend.REFPROP]] — la referencia de máxima precisión (requiere licencia)
- [[backend.SRK]] — la cúbica rápida para gases y mezclas cualitativas
- [[CoolProp.PropsSI]] — la función de alto nivel donde se escribe el prefijo
- [[AbstractState]] — el backend es el primer argumento del constructor
