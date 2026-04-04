---
title: AbstractState.get_mole_fractions — Obtener fracciones molares
aliases:
  - get_mole_fractions
  - obtener_fracciones_molares
  - mole_fractions_get

tags:
  - coolprop
  - api/metodo
  - abstractstate
  - mezclas

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: metodo

# --- Comportamiento ---
retorna: List[float]
muta_estado: false

draft: false
---

# AbstractState.get_mole_fractions — Obtener fracciones molares

## Firma de la función

```python
AbstractState.get_mole_fractions() -> List[float]
```

## Valor de retorno

`List[float]` — Lista de fracciones molares de cada componente en el orden en que fueron especificados.

| Componentes | Retorno típico |
|-------------|----------------|
| 2 componentes | `[0.5, 0.5]` |
| 3 componentes | `[0.4, 0.4, 0.2]` |

## Uso básico

```python
import CoolProp.CoolProp as CP

# Crear y configurar mezcla
state = CP.AbstractState('HEOS', 'R32&R134a')
state.set_mole_fractions([0.6, 0.4])

# Obtener fracciones molares
fractions = state.get_mole_fractions()
print(f"Fracción molar R32: {fractions[0]}")    # 0.6
print(f"Fracción molar R134a: {fractions[1]}")  # 0.4
```

## Verificar composición actual

```python
fractions = state.get_mole_fractions()

for i, frac in enumerate(fractions):
    print(f"Componente {i}: {frac:.3f}")

print(f"Suma: {sum(fractions)}")  # Debe ser 1.0
```

## Diferencia entre get_mass y get_mole

```python
# Misma mezcla, diferentes fracciones
state.set_mass_fractions([0.5, 0.5])
mass_fracs = state.get_mass_fractions()   # [0.5, 0.5]
mole_fracs = state.get_mole_fractions()   # Diferente (depende de pesos moleculares)

# CoolProp mantiene ambas internamente
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.set_mole_fractions]]
- [[AbstractState.set_mass_fractions]]
- [[AbstractState.get_mass_fractions]]
