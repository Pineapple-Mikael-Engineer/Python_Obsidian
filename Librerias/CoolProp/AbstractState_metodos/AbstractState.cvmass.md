---
title: AbstractState.cvmass — Calor específico a volumen constante
aliases:
  - cvmass
  - cv
  - calor_especifico_volumen_constante

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

# AbstractState.cvmass — Calor específico a volumen constante

## Firma de la función

```python
AbstractState.cvmass() -> float
```

## Valor de retorno

`float` — Calor específico a volumen constante Cv en **J/(kg·K)**.

| Fluido | Condiciones | Valor típico |
|--------|-------------|--------------|
| Agua | 25°C, 1 atm (líquido) | ~4,180 J/(kg·K) |
| Agua | 100°C, 1 atm (vapor) | ~1,550 J/(kg·K) |
| Aire | 25°C, 1 atm | ~718 J/(kg·K) |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.PT_INPUTS, 101325, 298.15)

cv = state.cvmass()
print(f"Cv: {cv:.1f} J/(kg·K)")  # Cv: 4180.0 J/(kg·K) (líquido)
```

## Proceso isocórico (calor a volumen constante)

```python
# Estado inicial
state.update(CP.PT_INPUTS, 101325, 300)
cv = state.cvmass()
u1 = state.umass()

# Calor añadido a volumen constante
# q = ∫ cv dT ≈ cv * ΔT (aproximación)
# Mejor: q = Δu
state.update(CP.DP_INPUTS, state.rho(), 101325)
u2 = state.umass()
q = u2 - u1
```

## Relación Cp - Cv (gas ideal)

```python
cp = state.cpmass()
cv = state.cvmass()
R = cp - cv  # Constante específica del gas (J/(kg·K))

print(f"R específica: {R:.1f} J/(kg·K)")
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.cpmass]]
- [[AbstractState.umass]]
- [[CoolProp.PropsSI]]
