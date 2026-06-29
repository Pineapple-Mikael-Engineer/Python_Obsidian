---
title: Estado termodinámico — dos propiedades lo definen todo
aliases:
  - estado termodinamico
  - regla de las dos propiedades
  - grados de libertad
tags:
  - coolprop
  - concepto
  - estado
lib: coolprop
tipo: concepto
draft: false
---

# Estado termodinámico — dos propiedades lo definen todo

## Definicion

El **estado termodinámico** de un fluido puro queda **completamente definido por DOS propiedades intensivas independientes**. Fijadas esas dos (presión y temperatura, presión y calidad, temperatura y densidad...), **todas** las demás propiedades —densidad, entalpía, entropía, energía interna, calidad de vapor, calores específicos, viscosidad...— quedan unívocamente determinadas.

## Por que existe

Esta es la **regla de estado** de Gibbs para una sustancia pura, compresible y simple: tiene exactamente **dos grados de libertad**. No es una limitación de CoolProp, es física: por eso toda función de CoolProp pide *dos* pares `(clave, valor)` y ni uno más. Si pidieras una sola propiedad el estado quedaría indeterminado (infinitos estados con esa misma densidad); si dieras tres correrías el riesgo de sobredeterminarlo con datos contradictorios. Dos, exactamente dos.

## La regla central

> [!regla] Dos propiedades independientes definen el estado de un fluido puro
> Da dos → obtienes cualquier otra. El truco está en que sean **independientes**: dentro de la campana de saturación (mezcla líquido-vapor) **P y T NO lo son** y hay que sustituir una por la calidad `Q`.

Pares de entrada habituales (todos válidos para [[CoolProp.PropsSI]] y [[AbstractState.update]]):

| Par | Cuándo se usa |
|-----|---------------|
| `P`, `T` | Estado general: líquido subenfriado, vapor sobrecalentado, gas, supercrítico |
| `P`, `Q` | Saturación a presión conocida (calderas, condensadores) |
| `T`, `Q` | Saturación a temperatura conocida (evaporadores) |
| `P`, `H` | Procesos reales con balance de energía (turbinas, compresores) |
| `P`, `S` | Procesos isentrópicos (compresión/expansión ideal) |
| `T`, `D` | Estado denso definido por densidad |

> [!warning] Dentro de la campana, P y T están ligadas
> A saturación la presión determina la temperatura (y viceversa): a 1 atm el agua hierve a una sola temperatura. El par `(P, T)` deja de ser independiente y no distingue *cuánto* vapor hay. Para fijar el punto exacto en la zona bifásica usa la **calidad** `Q` (`P,Q` o `T,Q`).

## Nivel 1 — dos propiedades dan una tercera

```python
from CoolProp.CoolProp import PropsSI

# Fijo P=101325 Pa y T=300 K -> obtengo densidad
D = PropsSI('D', 'T', 300, 'P', 101325, 'Water')  # -> 996.557 kg/m3

# El MISMO estado (P,T) determina tambien H y S, sin ambiguedad
H = PropsSI('H', 'T', 300, 'P', 101325, 'Water')  # -> 112654.9 J/kg
S = PropsSI('S', 'T', 300, 'P', 101325, 'Water')  # -> 393.062 J/(kg K)
```

Una vez fijado el par `(T, P)`, pedir `D`, `H` o `S` es solo leer del mismo estado: no hay grados de libertad sueltos.

## Nivel 2 — saturación: usa la calidad en lugar del par P,T

```python
from CoolProp.CoolProp import PropsSI

# A 1 atm el agua satura a una sola temperatura: P fija ya determina T
Tsat = PropsSI('T', 'P', 101325, 'Q', 0, 'Water')  # -> 373.124 K

# Dentro de la campana, la densidad depende de CUANTO vapor hay (Q):
D_liq = PropsSI('D', 'P', 101325, 'Q', 0, 'Water')  # liquido sat. -> 958.367 kg/m3
D_vap = PropsSI('D', 'P', 101325, 'Q', 1, 'Water')  # vapor sat.   ->   0.598 kg/m3
```

Aquí `(P, Q)` sí es un par independiente: `P` fija la línea de saturación y `Q` dice en qué punto de la campana estás. Por eso `D` salta de 958 a 0.6 kg/m³ sin cambiar `P`.

## Nivel 3 — el par adecuado para un proceso isentrópico

```python
from CoolProp.CoolProp import PropsSI

# Entrada del compresor: R134a, vapor saturado a -10 C (263.15 K)
s1 = PropsSI('S', 'T', 263.15, 'Q', 1, 'R134a')   # -> 1733.35 J/(kg K)
h1 = PropsSI('H', 'T', 263.15, 'Q', 1, 'R134a')   # -> 392664.9 J/kg

# Salida ideal (isentropica) hasta 10 bar: el par (P, S) define el estado
h2 = PropsSI('H', 'P', 1e6, 'S', s1, 'R134a')     # -> 426130.7 J/kg
w_ideal = h2 - h1                                 # trabajo especifico ideal -> 33465.8 J/kg
```

El proceso ideal conserva la entropía, así que el estado de salida se define con `(P, S)`: otro par independiente más.

## Casos que fallan

| Intento | Por qué falla |
|---------|---------------|
| Dar `(P, T)` dentro de la zona bifásica | A saturación `P` y `T` no son independientes: el par no distingue la calidad y CoolProp no puede ubicar el punto. Usa `(P, Q)` o `(T, Q)` |
| Dar una sola propiedad | Un grado de libertad sin fijar: el estado queda indeterminado (infinitas soluciones) |
| `(H, S)` cerca de saturación | Existe físicamente, pero la relación puede no ser monótona y el solver puede no converger; prefiere `(P, H)` o `(P, S)` |
| Esperar que `Q` tenga sentido fuera de la campana | `Q` solo está definida entre 0 y 1 (mezcla L-V); como líquido subenfriado o vapor sobrecalentado no aplica |

```python
from CoolProp.CoolProp import PropsSI

# FALLA: (T, P) a la temperatura de saturacion no fija el estado bifasico
# PropsSI('D', 'T', 373.124, 'P', 101325, 'Water')  # ambiguo dentro de la campana
# Correcto: anade la calidad
D = PropsSI('D', 'T', 373.124, 'Q', 0.5, 'Water')  # 50% vapor -> ~1.195 kg/m3
```

## Relacion con otros conceptos

- [[concepto_propiedades_SI]] — las claves (`'T'`, `'P'`, `'Q'`...) y unidades de cada propiedad del estado
- [[concepto_backend]] — el motor que resuelve la ecuación de estado a partir del par
- [[CoolProp.PropsSI]] — recibe el par como `input1/value1`, `input2/value2`
- [[AbstractState.update]] — fija el estado con un par de entrada (`PT_INPUTS`, `PQ_INPUTS`...)
