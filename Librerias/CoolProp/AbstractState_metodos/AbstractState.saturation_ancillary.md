---
title: AbstractState.saturation_ancillary — Propiedades de saturación por ecuaciones auxiliares
aliases:
  - saturation_ancillary
  - sat_ancillary
  - ecuaciones_auxiliares_saturacion

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

# AbstractState.saturation_ancillary — Propiedades de saturación por ecuaciones auxiliares

## Firma de la función

```python
AbstractState.saturation_ancillary(
    input: int,
    value: float,
    output: int
) -> float
```

## Valor de retorno

`float` — Propiedad de saturación calculada mediante ecuaciones auxiliares (correlaciones rápidas).

## Parámetros en detalle

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `input` | `int` | Variable de entrada | `CP.iT` o `CP.iP` |
| `value` | `float` | Valor de la variable de entrada | `373.15` (T en K) |
| `output` | `int` | Propiedad de salida | `CP.iP`, `CP.iD`, `CP.iH` |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')

# Presión de saturación a T=373.15 K
Psat = state.saturation_ancillary(CP.iT, 373.15, CP.iP)
print(f"Psat: {Psat/1000:.2f} kPa")  # ~101.33 kPa

# Densidad del líquido saturado a T=373.15 K
rho_f = state.saturation_ancillary(CP.iT, 373.15, CP.iD)
```

## Diferencia con update + Q

| Método | Velocidad | Precisión | Uso típico |
|--------|-----------|-----------|------------|
| `saturation_ancillary` | Muy rápida | Alta (correlaciones) | Cálculos repetitivos |
| `update` + `Q=0/1` | Más lenta | Máxima | Cálculos precisos |

## Ejemplo: curva de presión de vapor

```python
import numpy as np
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
temperatures = np.linspace(273.15, 373.15, 50)

presiones = []
for T in temperatures:
    Psat = state.saturation_ancillary(CP.iT, T, CP.iP)
    presiones.append(Psat)
```

## Propiedades disponibles

| Output | Descripción |
|--------|-------------|
| `CP.iP` | Presión de saturación |
| `CP.iD` | Densidad del líquido o vapor |
| `CP.iH` | Entalpía del líquido o vapor |
| `CP.iSmass` | Entropía del líquido o vapor |

**Nota:** Para densidad, entalpía o entropía, se necesita especificar también la fase mediante `specify_phase` o usar `update` tradicional.

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.saturation_pressure]]
- [[Constants]]
