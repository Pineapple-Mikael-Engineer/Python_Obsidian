---
title: AbstractState.smass — Entropía específica
aliases:
  - smass
  - entropia
  - entropy

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

# AbstractState.smass — Entropía específica

## Firma de la función

```python
AbstractState.smass() -> float
```

## Valor de retorno

`float` — Entropía específica en **J/(kg·K)**.

| Fluido | Condiciones | Valor típico |
|--------|-------------|--------------|
| Agua | 25°C, 1 atm (líquido) | ~367 J/(kg·K) |
| Agua | 100°C, 1 atm (vapor saturado) | ~7,354 J/(kg·K) |
| R134a | 20°C, vapor saturado | ~1,730 J/(kg·K) |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.PT_INPUTS, 101325, 298.15)

s = state.smass()
print(f"Entropía: {s:.1f} J/(kg·K)")  # Entropía: 367.0 J/(kg·K)
```

## Proceso isentrópico (entropía constante)

```python
# Guardar entropía del estado inicial
state.update(CP.TQ_INPUTS, 263.15, 1)  # -10°C, vapor saturado
s1 = state.smass()

# Forzar misma entropía con nueva presión
state.update(CP.PSmass_INPUTS, 1e6, s1)  # Compresión isentrópica
h2 = state.hmass()
```

## Variación de entropía en procesos

```python
# Estado inicial
state.update(CP.PT_INPUTS, 101325, 300)
s1 = state.smass()

# Estado final
state.update(CP.PT_INPUTS, 101325, 350)
s2 = state.smass()

# Cambio de entropía
delta_s = s2 - s1
print(f"Δs: {delta_s:.1f} J/(kg·K)")
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.hmass]]
- [[AbstractState.rho]]
- [[CoolProp.PropsSI]]
