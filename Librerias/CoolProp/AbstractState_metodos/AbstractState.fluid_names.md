---
title: AbstractState.fluid_names — Nombres de fluidos en una mezcla
aliases:
  - fluid_names
  - nombres_fluidos
  - componentes_mezcla

tags:
  - coolprop
  - api/metodo
  - abstractstate
  - mezclas
  - utilidades

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: metodo

# --- Comportamiento ---
retorna: List[str]
muta_estado: false

draft: false
---

# AbstractState.fluid_names — Nombres de fluidos en una mezcla

## Firma de la función

```python
AbstractState.fluid_names() -> List[str]
```

## Valor de retorno

`List[str]` — Lista de nombres de los componentes de la mezcla en el orden en que fueron especificados.

| Tipo de fluido | Retorno |
|----------------|---------|
| Fluido puro | `['Water']` |
| Mezcla binaria | `['R32', 'R134a']` |
| Mezcla ternaria | `['R32', 'R125', 'R134a']` |

## Uso básico

```python
import CoolProp.CoolProp as CP

# Fluido puro
state = CP.AbstractState('HEOS', 'Water')
names = state.fluid_names()
print(names)  # ['Water']

# Mezcla
state = CP.AbstractState('HEOS', 'R32&R134a')
names = state.fluid_names()
print(names)  # ['R32', 'R134a']
```

## Verificar componentes de una mezcla

```python
state = CP.AbstractState('HEOS', 'R32&R125&R134a')
state.set_mass_fractions([0.4, 0.4, 0.2])

componentes = state.fluid_names()
fracciones = state.get_mass_fractions()

for name, frac in zip(componentes, fracciones):
    print(f"{name}: {frac * 100:.1f}%")
# Salida:
# R32: 40.0%
# R125: 40.0%
# R134a: 20.0%
```

## Útil para depuración

```python
# Verificar que la mezcla se creó correctamente
state = CP.AbstractState('HEOS', 'R410A')  # R410A es 50/50 R32/R125
names = state.fluid_names()
print(f"Componentes de R410A: {names}")  # ['R32', 'R125']
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.fluid_parameter]]
- [[AbstractState.get_mass_fractions]]
- [[CoolProp.has_fluid]]
