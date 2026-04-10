---
title: AbstractState.umass — Energía interna específica
aliases:
  - umass
  - energia_interna
  - internal_energy

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

# AbstractState.umass — Energía interna específica

## Firma de la función

```python
AbstractState.umass() -> float
```

## Valor de retorno

`float` — Energía interna específica en **J/kg**.

| Fluido | Condiciones | Valor típico |
|--------|-------------|--------------|
| Agua | 25°C, 1 atm (líquido) | ~104,700 J/kg |
| Agua | 100°C, 1 atm (vapor) | ~2,504,000 J/kg |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.PT_INPUTS, 101325, 298.15)

u = state.umass()
print(f"Energía interna: {u:.0f} J/kg")
```

## Relación con entalpía

```python
h = state.hmass()      # h = u + P*v
rho = state.rho()
P = state.p()

# Calcular u desde h
v = 1.0 / rho
u_calc = h - P * v
u_direct = state.umass()

print(f"Desde h: {u_calc:.0f} J/kg")
print(f"Directo: {u_direct:.0f} J/kg")
```

## Proceso isocórico (volumen constante)

```python
# Estado inicial
state.update(CP.PT_INPUTS, 101325, 300)
u1 = state.umass()
v1 = 1.0 / state.rho()

# Volumen constante -> misma densidad
state.update(CP.DP_INPUTS, state.rho(), 101325)
u2 = state.umass()

# Calor a volumen constante = Δu
q_v = u2 - u1
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.hmass]]
- [[AbstractState.rho]]
- [[CoolProp.PropsSI]]
