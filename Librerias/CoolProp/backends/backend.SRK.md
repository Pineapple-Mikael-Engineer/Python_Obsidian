---
title: backend.SRK — ecuacion cubica Soave-Redlich-Kwong (rapida, cualitativa)
aliases:
  - SRK
  - Soave-Redlich-Kwong
  - backend cubico
tags:
  - coolprop
  - backend
  - srk
lib: coolprop
tipo: concepto
draft: false
---

# backend.SRK — ecuación cúbica Soave-Redlich-Kwong

`SRK` es el [[concepto_backend|backend]] que usa la **ecuación de estado cúbica de Soave-Redlich-Kwong**. Es **rápida y sencilla** pero **menos precisa** que [[backend.HEOS|HEOS]]: a cambio de un cálculo ligero, acepta una pérdida de exactitud. Es la elección típica para **gases, mezclas y cálculos cualitativos o educativos**, donde lo que importa es la tendencia y no el tercer decimal.

## Qué modelo usa

Las ecuaciones cúbicas describen el fluido con un polinomio de tercer grado en el volumen, parametrizado solo con propiedades básicas del fluido (temperatura crítica, presión crítica y factor acéntrico). Tienen **muy pocos parámetros** comparadas con las ecuaciones multiparamétricas de Helmholtz de HEOS, así que se evalúan rápido y se extienden con facilidad a mezclas y a fluidos poco caracterizados, pero **reproducen peor** las propiedades, sobre todo la densidad de la fase líquida y la zona cercana al punto crítico.

## El pariente: Peng-Robinson (`PR`)

SRK no está sola: CoolProp también incluye la otra gran cúbica clásica, **Peng-Robinson**, con el prefijo `'PR::...'`. Son alternativas del mismo tipo (cúbicas, rápidas, cualitativas) que difieren en el ajuste; PR suele dar mejores densidades de líquido. Se intercambian igual que cualquier backend:

```python
from CoolProp.CoolProp import PropsSI

rho_srk = PropsSI('D', 'T', 300, 'P', 1e6, 'SRK::Methane')   # -> 6.5389603054482155
rho_pr  = PropsSI('D', 'T', 300, 'P', 1e6, 'PR::Methane')    # -> 6.572326327085937
```

Verificado: para metano a 300 K y 10 bar, SRK da `6.539` kg/m³ y PR da `6.572` kg/m³.

## Sintaxis

```python
from CoolProp.CoolProp import PropsSI

rho = PropsSI('D', 'T', 300, 'P', 1e6, 'SRK::Methane')   # -> 6.5389603054482155
```

Con [[AbstractState]], el backend es el primer argumento del constructor: `CP.AbstractState('SRK', 'Methane')`.

## SRK frente a HEOS: la diferencia de precisión

Comparando la misma densidad con el motor de referencia [[backend.HEOS|HEOS]] se ve el coste en exactitud. Verificado en este entorno:

| Condición (metano) | `SRK::Methane` | `HEOS::Methane` | Diferencia |
|--------------------|----------------|------------------|-----------|
| 300 K, 10 bar (gas) | `6.5389603054482155` | `6.54154365368275` | ~0.04 % |
| 200 K, 50 bar (gas denso) | `87.15496864863769` | `87.76399754661693` | ~0.7 % |

```python
from CoolProp.CoolProp import PropsSI

srk  = PropsSI('D', 'T', 200, 'P', 5e6, 'SRK::Methane')   # -> 87.15496864863769
heos = PropsSI('D', 'T', 200, 'P', 5e6, 'HEOS::Methane')  # -> 87.76399754661693
print(100 * abs(srk - heos) / heos)                        # -> 0.69... %
```

Como gas a baja presión la diferencia es pequeña (~0.04 %), pero al acercarse a la región densa crece (~0.7 %): exactamente donde las cúbicas flojean. Para cálculos finos esa desviación no es aceptable; para una estimación cualitativa, sí.

## Cuándo usarla y cuándo no

**Úsala cuando:**
- Trabajas con **gases o mezclas** y necesitas una respuesta **rápida**.
- El objetivo es **cualitativo o educativo**: entender tendencias, hacer un primer dimensionamiento, enseñar el comportamiento de una cúbica.
- El fluido está poco caracterizado y solo dispones de sus propiedades críticas.

**No la uses cuando:**
- Necesitas **precisión** en densidad de líquido o cerca del punto crítico → usa [[backend.HEOS|HEOS]].
- Calculas **agua/vapor** de forma intensiva → usa [[backend.IF97|IF97]].
- Requieres trazabilidad a la **referencia** del NIST → usa [[backend.REFPROP|REFPROP]] si tienes licencia.

## Notas relacionadas

- [[concepto_backend]] — qué es un backend y la sintaxis `BACKEND::Fluido`
- [[backend.HEOS]] — el motor preciso por defecto contra el que se compara
- [[CoolProp.PropsSI]] — donde se escribe el prefijo `SRK::` o `PR::`
- [[AbstractState]] — el backend es el primer argumento del constructor
