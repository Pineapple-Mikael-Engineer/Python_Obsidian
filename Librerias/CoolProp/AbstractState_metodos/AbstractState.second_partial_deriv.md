---
title: AbstractState.second_partial_deriv — Derivada parcial de segundo orden
aliases:
  - second_partial_deriv
  - derivada_segundo_orden
  - derivada_segunda

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

# AbstractState.second_partial_deriv — Derivada parcial de segundo orden

## Firma de la función

```python
AbstractState.second_partial_deriv(
    output: int,
    input1: int,
    input2: int,
    input3: int
) -> float
```

## Valor de retorno

`float` — Valor de la derivada parcial de segundo orden en unidades combinadas.

## Parámetros en detalle

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `output` | `int` | Variable que se deriva | `CP.iD` (densidad) |
| `input1` | `int` | Primera variable respecto a la cual se deriva | `CP.iT` |
| `input2` | `int` | Segunda variable respecto a la cual se deriva | `CP.iT` |
| `input3` | `int` | Variable que se mantiene constante | `CP.iP` |

**Interpretación:** `(∂²output / ∂input1 ∂input2) a input3 constante`

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.iT, 298.15, CP.iP, 101325)

# (∂²ρ/∂T²) a P constante
deriv2 = state.second_partial_deriv(CP.iD, CP.iT, CP.iT, CP.iP)
print(f"∂²ρ/∂T² = {deriv2:.6f} kg/(m³·K²)")
```

## Derivadas mixtas

```python
# Derivada mixta (∂²ρ/∂T∂P)
# Primero respecto a T, luego respecto a P
deriv_mix = state.second_partial_deriv(CP.iD, CP.iT, CP.iP, CP.iConst)
```

## Derivadas comunes

```python
# (∂²h/∂T²) a P constante (relacionado con Cp)
d2h_dT2 = state.second_partial_deriv(CP.iH, CP.iT, CP.iT, CP.iP)

# (∂²s/∂T²) a P constante
d2s_dT2 = state.second_partial_deriv(CP.iSmass, CP.iT, CP.iT, CP.iP)

# (∂²ρ/∂P²) a T constante
d2rho_dP2 = state.second_partial_deriv(CP.iD, CP.iP, CP.iP, CP.iT)
```

## Orden de parámetros

El orden es **siempre** `(output, input1, input2, input3)`:

```python
# ∂²ρ/∂T² manteniendo P constante
state.second_partial_deriv(CP.iD, CP.iT, CP.iT, CP.iP)

# ∂²h/∂T∂P (mixta)
state.second_partial_deriv(CP.iH, CP.iT, CP.iP, CP.iConst)
```

## Notas sobre input3

La tercera variable (`input3`) puede ser:

| Constante | Significado |
|-----------|-------------|
| `CP.iT` | Temperatura constante |
| `CP.iP` | Presión constante |
| `CP.iD` | Densidad constante |
| `CP.iH` | Entalpía constante |
| `CP.iSmass` | Entropía constante |
| `CP.iConst` | Constante especificada (para derivadas mixtas) |

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `The state is not valid` | No se llamó a `update` | Ejecutar `state.update(...)` primero |
| Valores extremos | Cerca de punto crítico | Alejar T, P del punto crítico |
| `input3` inválido | Constante no soportada | Usar `CP.iConst` para mixtas |

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.first_partial_deriv]]
- [[Constants]]
