---
title: AbstractState.hmass — Entalpía específica
aliases:
  - hmass
  - entalpia
  - enthalpy

tags:
  - coolprop
  - api/metodo
  - abstractstate
  - propiedades

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: metodo

# --- Comportamiento ---
retorna: float
muta_estado: false

draft: false
---

# AbstractState.hmass — Entalpía específica

## Firma de la función

```python
AbstractState.hmass() -> float
```

## Valor de retorno

`float` — Entalpía específica en **J/kg**.

| Fluido | Condiciones | Valor típico |
|--------|-------------|--------------|
| Agua | 25°C, 1 atm (líquido) | ~104,900 J/kg |
| Agua | 100°C, 1 atm (vapor saturado) | ~2,676,000 J/kg |
| R134a | 20°C, vapor saturado | ~410,000 J/kg |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.PT_INPUTS, 101325, 298.15)

h = state.hmass()
print(f"Entalpía: {h:.0f} J/kg")  # Entalpía: 104900 J/kg
```

## Calor latente (diferencia de entalpía)

```python
# Líquido saturado
state.update(CP.PQ_INPUTS, 101325, 0)
h_f = state.hmass()

# Vapor saturado
state.update(CP.PQ_INPUTS, 101325, 1)
h_g = state.hmass()

# Calor latente de vaporización
h_fg = h_g - h_f
print(f"Calor latente: {h_fg:.0f} J/kg")  # ~2,257,000 J/kg
```

## Proceso isentrópico (compresor)

```python
# Estado 1: entrada (vapor saturado a -10°C)
state.update(CP.TQ_INPUTS, 263.15, 1)
h1 = state.hmass()
s1 = state.smass()

# Estado 2: compresión isentrópica hasta 10 bar
state.update(CP.PSmass_INPUTS, 1e6, s1)
h2 = state.hmass()

# Trabajo del compresor
w_comp = h2 - h1
print(f"Trabajo: {w_comp:.0f} J/kg")
```

## Proceso isobárico (caldera)

```python
# Entrada: líquido saturado
state.update(CP.PQ_INPUTS, 1e6, 0)
h_in = state.hmass()

# Salida: vapor sobrecalentado
state.update(CP.PT_INPUTS, 1e6, 573.15)  # 300°C
h_out = state.hmass()

# Calor añadido
q = h_out - h_in
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.smass]]
- [[AbstractState.rho]]
- [[CoolProp.PropsSI]]
