---
title: AbstractState.T — Temperatura
aliases:
  - T
  - temperatura
  - temperature

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

# AbstractState.T — Temperatura

## Firma de la función

```python
AbstractState.T() -> float
```

## Valor de retorno

`float` — Temperatura en **Kelvin (K)**.

| Condición | Valor típico |
|-----------|--------------|
| Punto de congelación del agua | 273.15 K |
| Temperatura ambiente | ~298.15 K |
| Punto de ebullición del agua (1 atm) | 373.15 K |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.PQ_INPUTS, 101325, 1)  # Vapor saturado a 1 atm

T = state.T()
print(f"Temperatura de saturación: {T - 273.15:.2f} °C")  # 100.00 °C
```

## Conversión a otras unidades

```python
T_K = state.T()
T_C = T_K - 273.15  # Celsius
T_F = T_K * 9/5 - 459.67  # Fahrenheit
```

## Temperatura de saturación a partir de presión

```python
# Dada una presión, obtener Tsat
state.update(CP.PQ_INPUTS, 5e5, 0)  # Líquido saturado a 5 bar
Tsat = state.T()
print(f"Tsat a 5 bar: {Tsat - 273.15:.2f} °C")
```

## Temperatura a partir de entalpía y presión

```python
# Conocer T dado un estado (P, H)
state.update(CP.PH_INPUTS, 1e6, 3e6)
T = state.T()
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.p]]
- [[AbstractState.Q]]
- [[CoolProp.PropsSI]]
