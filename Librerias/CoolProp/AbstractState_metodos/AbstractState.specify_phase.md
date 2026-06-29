---
title: AbstractState.specify_phase — Forzar la fase del fluido
aliases:
  - specify_phase
  - forzar fase
  - unspecify_phase

tags:
  - coolprop
  - api/metodo
  - abstractstate

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: true

draft: false
---

# AbstractState.specify_phase — Forzar la fase del fluido

`specify_phase` le dice al solver de [[AbstractState]] **en qué región termodinámica buscar** ANTES de llamar a `update`. No cambia las propiedades del fluido: cambia la rama de la solución que el solver elige cuando un par de entrada es ambiguo (sobre la línea de saturación) o costoso de resolver (cerca del punto crítico). Es una pista, no un cálculo: por eso `muta_estado` es `true` en el sentido de que altera el comportamiento del próximo `update`, pero por sí mismo no fija ningún estado.

## Firma de la función

```python
AbstractState.specify_phase(phase: int) -> None
```

Y su contraparte para deshacer la pista:

```python
AbstractState.unspecify_phase() -> None
```

## Valor de retorno

`None` — ambos métodos modifican el estado interno del objeto [[AbstractState]] (la fase que se asumirá en los `update` siguientes) pero no retornan ningún valor.

## Parámetros en detalle

### `phase` — identificador de fase

Entero (`int`) que indica la fase forzada. Se usan las constantes `CP.iphase_*` definidas en [[Constants]]; nunca un string ni el número literal.

| Constante | Valor | Fase forzada |
|-----------|-------|--------------|
| `CP.iphase_liquid` | 0 | Líquido subenfriado |
| `CP.iphase_gas` | 1 | Gas / vapor |
| `CP.iphase_supercritical` | 2 | Supercrítico |
| `CP.iphase_supercritical_gas` | 3 | Gas supercrítico |
| `CP.iphase_supercritical_liquid` | 4 | Líquido supercrítico |
| `CP.iphase_critical_point` | 5 | Punto crítico |
| `CP.iphase_twophase` | 6 | Mezcla saturada (dos fases) |

`unspecify_phase()` no recibe parámetros: devuelve el solver a la detección automática de fase.

## Casos de uso

### Desambiguar un estado sobre la línea de saturación

Sobre la curva de saturación, un mismo par `(P, T)` describe **dos estados distintos** (líquido saturado y vapor saturado): el par P-T no los distingue. `specify_phase` elige la rama.

```python
import CoolProp.CoolProp as CP

# Presión de saturación del agua a 150 °C
sat = CP.AbstractState('HEOS', 'Water')
T = 150 + 273.15                       # 423.15 K (convertir °C -> K)
sat.update(CP.QT_INPUTS, 0.0, T)       # líquido saturado: (Q, T)
Psat = sat.p()                         # -> ~476164.5 Pa

# En (Psat, T) el par P-T es ambiguo: forzamos cada rama
liq = CP.AbstractState('HEOS', 'Water')
liq.specify_phase(CP.iphase_liquid)    # forzar rama líquida
liq.update(CP.PT_INPUTS, Psat, T)
print(liq.rhomass())                   # -> ~917.01 kg/m3 (líquido)

gas = CP.AbstractState('HEOS', 'Water')
gas.specify_phase(CP.iphase_gas)       # forzar rama vapor
gas.update(CP.PT_INPUTS, Psat, T)
print(gas.rhomass())                   # -> ~2.5481 kg/m3 (vapor)
```

### Acelerar un bucle cuya fase ya conoces

Cuando recorres muchos estados que sabes que están en la misma región (p. ej. vapor sobrecalentado), forzar la fase ahorra al solver la búsqueda de en qué región cae cada punto.

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.specify_phase(CP.iphase_gas)     # todo el barrido es vapor a 1 bar

for T in [400.0, 450.0, 500.0]:
    state.update(CP.PT_INPUTS, 1e5, T)
    print(T, state.rhomass())          # -> 400 0.5476 / 450 0.4846 / 500 0.4351
```

### Estado cerca del punto crítico

Cerca del punto crítico (agua: 647.096 K, 22.064 MPa) el solver puede no converger o elegir la rama equivocada; una pista de fase lo estabiliza.

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.specify_phase(CP.iphase_gas)     # pista: buscar en la región gaseosa
state.update(CP.PT_INPUTS, 2.2e7, 660.0)
print(state.rhomass())                 # -> ~141.94 kg/m3
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Estados siguientes con densidad/propiedades absurdas | Olvidar `unspecify_phase()`: la fase forzada se arrastra a todos los `update` posteriores del mismo objeto | Llamar `state.unspecify_phase()` al terminar la región forzada, o usar un objeto distinto por región |
| `ValueError` al hacer `update` | Forzar una fase imposible para ese `(P, T)` (p. ej. exigir gas a 300 K y 1 bar, donde el agua es líquida) | No forzar una fase incompatible; si dudas, deja la detección automática |
| `Expected int, got str` | Pasar `'iphase_gas'` (string) en vez de la constante | Usar `CP.iphase_gas` (entero) |

El siguiente fragmento ilustra el segundo error y su recuperación:

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.specify_phase(CP.iphase_gas)     # forzamos gas...
try:
    state.update(CP.PT_INPUTS, 1e5, 300.0)   # ...pero a 300 K, 1 bar el agua es líquida
except ValueError:
    print("Fase imposible para este estado")  # -> se imprime esto

state.unspecify_phase()                # deshacer la pista
state.update(CP.PT_INPUTS, 1e5, 300.0)
print(state.rhomass())                 # -> ~996.556 kg/m3 (líquido, correcto)
```

## Limitaciones

`specify_phase` solo tiene sentido con el objeto de bajo nivel [[AbstractState]]; [[CoolProp.PropsSI]] no expone control de fase. Y recuerda que es una **pista al solver**, no una conversión: no fuerza al fluido a estar en esa fase, solo orienta la búsqueda de la solución; si la fase pedida es físicamente imposible en ese punto, el `update` falla.

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[Constants]]
- [[concepto_estado_termodinamico]]
