---
title: AbstractState.cpmass — Calor específico a presión constante
aliases:
  - cpmass
  - cp
  - calor_especifico_presion_constante

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

# AbstractState.cpmass — Calor específico a presión constante

## Firma de la función

```python
AbstractState.cpmass() -> float
```

## Valor de retorno

`float` — Calor específico a presión constante Cp en **J/(kg·K)**.

| Fluido | Condiciones | Valor típico |
|--------|-------------|--------------|
| Agua | 25°C, 1 atm (líquido) | ~4,180 J/(kg·K) |
| Agua | 100°C, 1 atm (vapor) | ~2,080 J/(kg·K) |
| Aire | 25°C, 1 atm | ~1,005 J/(kg·K) |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.iT, 298.15, CP.iP, 101325)

cp = state.cpmass()
print(f"Cp: {cp:.1f} J/(kg·K)")  # Cp: 4180.0 J/(kg·K)
```

## Variación con temperatura (gas ideal)

```python
state = CP.AbstractState('HEOS', 'Air')

for T in [300, 500, 1000]:
    state.update(CP.iT, T, CP.iP, 101325)
    cp = state.cpmass()
    print(f"T={T}K, Cp={cp:.1f} J/(kg·K)")
```

## Relación con Cv

```python
cp = state.cpmass()
cv = state.cvmass()
gamma = cp / cv  # Relación de calores específicos
print(f"γ = cp/cv = {gamma:.3f}")
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.cvmass]]
- [[CoolProp.PropsSI]]
