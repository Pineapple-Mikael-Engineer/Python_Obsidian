---
title: AbstractState.saturation_pressure — Presión de saturación
aliases:
  - saturation_pressure
  - presion_saturacion
  - Psat

tags:
  - coolprop
  - api/metodo
  - abstractstate
  - saturacion

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: metodo

# --- Comportamiento ---
retorna: float
muta_estado: false

draft: false
---

# AbstractState.saturation_pressure — Presión de saturación

## Firma de la función

```python
AbstractState.saturation_pressure(
    T: float
) -> float
```

## Valor de retorno

`float` — Presión de saturación en **Pa** a la temperatura especificada.

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `T` | `float` | Temperatura en Kelvin (K) |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')

# Presión de saturación a 100°C
Psat = state.saturation_pressure(373.15)
print(f"Psat: {Psat/1000:.2f} kPa")  # ~101.33 kPa
```

## Comparación con saturation_ancillary

| Método | Entrada | Salida | Velocidad |
|--------|---------|--------|-----------|
| `saturation_pressure` | Solo T | Solo P | Rápida |
| `saturation_ancillary` | Variable + valor | Variable variable | Rápida |

```python
# Estas dos son equivalentes para presión de saturación
Psat1 = state.saturation_pressure(373.15)
Psat2 = state.saturation_ancillary(CP.iT, 373.15, CP.iP)
# Psat1 == Psat2
```

## Uso en cálculos de saturación

```python
# Obtener Psat, luego actualizar estado
Psat = state.saturation_pressure(373.15)
state.update(CP.iP, Psat, CP.iQ, 0)  # Líquido saturado
h_f = state.hmass()

state.update(CP.iP, Psat, CP.iQ, 1)  # Vapor saturado
h_g = state.hmass()
```

## Temperatura de saturación (inversa)

CoolProp no tiene `saturation_temperature` directo. Para obtener Tsat dada una presión:

```python
# Método indirecto
def get_Tsat(P):
    # Usar búsqueda binaria o saturation_ancillary
    # Alternativa: usar PropsSI
    from CoolProp.CoolProp import PropsSI
    return PropsSI('T', 'P', P, 'Q', 0, 'Water')

Tsat = get_Tsat(101325)  # ~373.15 K
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.saturation_ancillary]]
- [[AbstractState.update]]
- [[CoolProp.PropsSI]]
