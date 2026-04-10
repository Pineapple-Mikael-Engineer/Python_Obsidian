---
title: AbstractState.phase — Identificador de fase
aliases:
  - phase
  - fase
  - identificar_fase

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
retorna: int
muta_estado: false

draft: false
---

# AbstractState.phase — Identificador de fase

## Firma de la función

```python
AbstractState.phase() -> int
```

## Valor de retorno

`int` — Identificador numérico de la fase actual.

| Valor | Fase | Constante equivalente |
|-------|------|----------------------|
| `0` | Líquido | `CP.iphase_liquid` |
| `1` | Gas / Vapor | `CP.iphase_gas` |
| `2` | Supercrítico | `CP.iphase_supercritical` |
| `3` | Gas supercrítico | `CP.iphase_supercritical_gas` |
| `4` | Líquido supercrítico | `CP.iphase_supercritical_liquid` |
| `5` | Punto crítico | `CP.iphase_critical_point` |
| `6` | Mezcla saturada (líquido+vapor) | `CP.iphase_twophase` |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')
state.update(CP.PT_INPUTS, 101325, 298.15)

phase = state.phase()
print(f"Fase: {phase}")  # 0 (líquido)
```

## Verificar fase específica

```python
phase = state.phase()

if phase == 0:
    print("Líquido subenfriado")
elif phase == 1:
    print("Vapor sobrecalentado")
elif phase == 6:
    print("Mezcla saturada - Q disponible")
    Q = state.Q()
else:
    print(f"Otra fase: {phase}")
```

## Prevenir errores antes de consultar calidad

```python
# Q() falla fuera de saturación, phase() no
state.update(CP.PT_INPUTS, 1e7, 300)  # Líquido comprimido

if state.phase() == 6:
    Q = state.Q()  # Solo seguro en saturación
else:
    print("No en saturación, Q no aplica")
```

## Usar constantes para legibilidad

```python
import CoolProp.CoolProp as CP

phase = state.phase()

if phase == CP.iphase_twophase:
    print("Mezcla saturada")
elif phase == CP.iphase_gas:
    print("Vapor")
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.Q]]
- [[Constants]]
- [[AbstractState.specify_phase]]
