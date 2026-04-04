---
title: AbstractState.p — Presión
aliases:
  - p
  - presion
  - pressure

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

# AbstractState.p — Presión

## Firma de la función

```python
AbstractState.p() -> float
```

## Valor de retorno

`float` — Presión en **Pascal (Pa)**.

| Condición | Valor típico |
|-----------|--------------|
| Presión atmosférica estándar | 101,325 Pa |
| 1 bar | 100,000 Pa |
| 10 bar | 1,000,000 Pa |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.iT, 373.15, CP.iQ, 0)  # Líquido saturado a 100°C

P = state.p()
print(f"Presión de saturación: {P / 1000:.2f} kPa")  # ~101.33 kPa
```

## Conversión a otras unidades

```python
P_Pa = state.p()
P_kPa = P_Pa / 1000           # kilopascal
P_bar = P_Pa / 100000         # bar
P_psi = P_Pa * 0.000145038    # libras por pulgada cuadrada
P_atm = P_Pa / 101325         # atmósferas
```

## Presión de saturación a partir de temperatura

```python
# Dada una temperatura, obtener Psat
state.update(CP.iT, 373.15, CP.iQ, 0)  # Líquido saturado a 100°C
Psat = state.p()
print(f"Psat a 100°C: {Psat / 1000:.2f} kPa")
```

## Presión a partir de entalpía y temperatura

```python
# Conocer P dado un estado (T, H)
state.update(CP.iT, 400, CP.iH, 2.8e6)
P = state.p()
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.T]]
- [[AbstractState.Q]]
- [[CoolProp.PropsSI]]
