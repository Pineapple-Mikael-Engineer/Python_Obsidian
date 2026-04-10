---
title: AbstractState.set_mole_fractions — Establecer fracciones molares
aliases:
  - set_mole_fractions
  - fracciones_molares
  - mole_fractions

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
retorna: None
muta_estado: true

draft: false
---

# AbstractState.set_mole_fractions — Establecer fracciones molares

## Firma de la función

```python
AbstractState.set_mole_fractions(
    fractions: List[float]
) -> None
```

## Valor de retorno

`None` — Modifica el estado interno del objeto.

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `fractions` | `List[float]` | Lista de fracciones molares. Deben sumar 1.0 |

## Uso básico

```python
import CoolProp.CoolProp as CP

# Crear estado para mezcla binaria
state = CP.AbstractState('HEOS', 'R32&R134a')

# Establecer fracciones molares (50% R32, 50% R134a)
state.set_mole_fractions([0.5, 0.5])

# Actualizar y consultar propiedades
state.update(CP.iT, 300, CP.iP, 1e5)
h = state.hmass()
```

## Fracciones másicas vs molares

```python
# Diferencia clave:
# - Másicas: basadas en masa
# - Molares: basadas en número de moles

# Para mezcla 50/50 en masa
state.set_mass_fractions([0.5, 0.5])

# Para mezcla 50/50 en moles
state.set_mole_fractions([0.5, 0.5])
```

## Verificar suma de fracciones

```python
fractions = [0.7, 0.3]
total = sum(fractions)

if abs(total - 1.0) < 1e-6:
    state.set_mole_fractions(fractions)
else:
    print(f"Error: las fracciones suman {total}, debe ser 1.0")
```

## Conversión entre fracciones

CoolProp no proporciona conversión automática. Para convertir:

```python
# Obtener pesos moleculares (requiere consulta externa)
# mass_frac = (mole_frac * MW_i) / sum(mole_frac * MW_j)
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.set_mass_fractions]]
- [[AbstractState.get_mass_fractions]]
- [[AbstractState.get_mole_fractions]]
