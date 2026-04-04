---
title: AbstractState.first_partial_deriv — Derivada parcial de primer orden
aliases:
  - first_partial_deriv
  - derivada_parcial
  - derivada

tags:
  - coolprop
  - api/metodo
  - abstractstate
  - derivadas

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: metodo

# --- Comportamiento ---
retorna: float
muta_estado: false

draft: false
---

# AbstractState.first_partial_deriv — Derivada parcial de primer orden

## Firma de la función

```python
AbstractState.first_partial_deriv(
    output: int,
    input1: int,
    input2: int
) -> float
```

## Valor de retorno

`float` — Valor de la derivada parcial en unidades combinadas.

## Parámetros en detalle

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `output` | `int` | Variable que se deriva | `CP.iD` (densidad) |
| `input1` | `int` | Variable respecto a la cual se deriva | `CP.iT` (temperatura) |
| `input2` | `int` | Variable que se mantiene constante | `CP.iP` (presión) |

**Interpretación:** `(∂output / ∂input1) a input2 constante`

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.iT, 298.15, CP.iP, 101325)

# (∂ρ/∂T) a P constante
deriv = state.first_partial_deriv(CP.iD, CP.iT, CP.iP)
print(f"∂ρ/∂T = {deriv:.6f} kg/(m³·K)")
```

## Derivadas comunes en termodinámica

```python
# Coeficiente de expansión térmica β = -(1/ρ)(∂ρ/∂T)_P
rho = state.rho()
beta = - (1/rho) * state.first_partial_deriv(CP.iD, CP.iT, CP.iP)

# Compresibilidad isotérmica κ_T = -(1/ρ)(∂ρ/∂P)_T
kappa = - (1/rho) * state.first_partial_deriv(CP.iD, CP.iP, CP.iT)

# Cp = (∂h/∂T)_P
cp = state.first_partial_deriv(CP.iH, CP.iT, CP.iP)  # equivalente a state.cpmass()

# Cv = (∂u/∂T)_P (no es exacto, mejor usar state.cvmass())
```

## Derivadas con diferentes variables

```python
# (∂h/∂P) a T constante
dh_dP = state.first_partial_deriv(CP.iH, CP.iP, CP.iT)

# (∂s/∂T) a P constante
ds_dT = state.first_partial_deriv(CP.iSmass, CP.iT, CP.iP)

# (∂T/∂P) a s constante (coeficiente Joule-Thomson)
dT_dP = state.first_partial_deriv(CP.iT, CP.iP, CP.iSmass)
```

## Orden de parámetros

El orden es **siempre** `(output, input1, input2)`:

```python
# ∂ρ/∂T manteniendo P constante
state.first_partial_deriv(CP.iD, CP.iT, CP.iP)

# ∂T/∂P manteniendo s constante
state.first_partial_deriv(CP.iT, CP.iP, CP.iSmass)

# ∂h/∂P manteniendo T constante
state.first_partial_deriv(CP.iH, CP.iP, CP.iT)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores extremadamente grandes | Cerca de punto crítico | Alejar T, P del punto crítico |
| `The state is not valid` | No se llamó a `update` | Ejecutar `state.update(...)` primero |

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.second_partial_deriv]]
- [[Constants]]
