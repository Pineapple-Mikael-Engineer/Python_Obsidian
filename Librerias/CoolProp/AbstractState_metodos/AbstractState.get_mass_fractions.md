---
title: AbstractState.get_mass_fractions — Obtener fracciones másicas
aliases:
  - get_mass_fractions
  - obtener_fracciones_masicas
  - mass_fractions_get

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

# AbstractState.get_mass_fractions — Obtener fracciones másicas

## Firma de la función

```python
AbstractState.get_mass_fractions() -> List[float]
```

## Valor de retorno

`List[float]` — Lista de fracciones másicas de cada componente en el orden en que fueron especificados.

| Componentes | Retorno típico |
|-------------|----------------|
| 2 componentes | `[0.5, 0.5]` |
| 3 componentes | `[0.4, 0.4, 0.2]` |

## Uso básico

```python
import CoolProp.CoolProp as CP

# Crear y configurar mezcla
state = CP.AbstractState('HEOS', 'R32&R134a')
state.set_mass_fractions([0.6, 0.4])

# Obtener fracciones
fractions = state.get_mass_fractions()
print(f"Fracción R32: {fractions[0]}")    # 0.6
print(f"Fracción R134a: {fractions[1]}")  # 0.4
```

## Verificar composición actual

```python
# Útil para depuración
fractions = state.get_mass_fractions()

for i, frac in enumerate(fractions):
    print(f"Componente {i}: {frac:.3f}")

print(f"Suma: {sum(fractions)}")  # Debe ser 1.0
```

## Fluido puro vs mezcla

```python
# Fluido puro (sin set_mass_fractions)
state_pure = CP.AbstractState('HEOS', 'Water')
# get_mass_fractions() puede fallar o retornar lista vacía

# Mezcla
state_mix = CP.AbstractState('HEOS', 'R32&R134a')
state_mix.set_mass_fractions([0.5, 0.5])
fractions = state_mix.get_mass_fractions()  # [0.5, 0.5]
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.set_mass_fractions]]
- [[AbstractState.set_mole_fractions]]
- [[AbstractState.get_mole_fractions]]
