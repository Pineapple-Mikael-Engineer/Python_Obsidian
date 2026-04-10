---
title: AbstractState.set_mass_fractions — Establecer fracciones másicas
aliases:
  - set_mass_fractions
  - fracciones_masicas
  - mass_fractions

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

# AbstractState.set_mass_fractions — Establecer fracciones másicas

## Firma de la función

```python
AbstractState.set_mass_fractions(
    fractions: List[float]
) -> None
```

## Valor de retorno

`None` — Modifica el estado interno del objeto.

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `fractions` | `List[float]` | Lista de fracciones másicas. Deben sumar 1.0 |

## Uso básico

```python
import CoolProp.CoolProp as CP

# Crear estado para mezcla binaria
state = CP.AbstractState('HEOS', 'R32&R134a')

# Establecer fracciones másicas (50% R32, 50% R134a)
state.set_mass_fractions([0.5, 0.5])

# Ahora se puede actualizar el estado de la mezcla
state.update(CP.iT, 300, CP.iP, 1e5)
h = state.hmass()
```

## Mezcla con más de 2 componentes

```python
# Mezcla ternaria: R32 (40%), R125 (40%), R134a (20%)
state = CP.AbstractState('HEOS', 'R32&R125&R134a')
state.set_mass_fractions([0.4, 0.4, 0.2])
```

## Verificar suma de fracciones

```python
fractions = [0.6, 0.4]
total = sum(fractions)

if abs(total - 1.0) < 1e-6:
    state.set_mass_fractions(fractions)
else:
    print(f"Error: las fracciones suman {total}, debe ser 1.0")
```

## Fracciones molares vs másicas

```python
# Másicas (recomendado para ingeniería)
state.set_mass_fractions([0.5, 0.5])

# Molares (requiere conocer pesos moleculares)
state.set_mole_fractions([0.5, 0.5])
```

Ver [[AbstractState.set_mole_fractions]]

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.set_mole_fractions]]
- [[AbstractState.get_mass_fractions]]
- [[AbstractState.get_mole_fractions]]
