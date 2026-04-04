```markdown
---
title: AbstractState.Q — Calidad (título de vapor)
aliases:
  - Q
  - calidad
  - titulo_vapor
  - vapor_quality

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

# AbstractState.Q — Calidad (título de vapor)

## Firma de la función

```python
AbstractState.Q() -> float
```

## Valor de retorno

`float` — Calidad (título de vapor) en el rango **0 a 1**.

| Valor | Significado |
|-------|-------------|
| `0.0` | Líquido saturado |
| `>0.0 y <1.0` | Mezcla saturada (líquido + vapor) |
| `1.0` | Vapor saturado |
| Fuera de saturación | Lanza excepción o retorna valor fuera de rango |

## Uso básico

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')

# Mezcla con calidad 0.5 (50% vapor, 50% líquido)
state.update(CP.iP, 101325, CP.iQ, 0.5)
Q = state.Q()
print(f"Calidad: {Q}")  # 0.5
```

## Verificar si está en saturación

```python
# Si el estado no está en saturación, Q() puede fallar
# Es mejor verificar la fase primero
phase = state.phase()  # 6 = mezcla saturada

if phase == 6:
    Q = state.Q()
    print(f"Calidad: {Q:.3f}")
else:
    print("No está en saturación")
```

## Propiedades en saturación usando calidad

```python
# Para una mezcla, cualquier propiedad es el promedio ponderado
state.update(CP.iP, 101325, CP.iQ, 0.3)  # 30% vapor

h_mix = state.hmass()  # h_f + Q * h_fg
# Equivalente a:
# h_mix = (1-Q)*h_f + Q*h_g
```

## Líquido y vapor saturados

```python
# Líquido saturado (Q=0)
state.update(CP.iP, 101325, CP.iQ, 0)
h_f = state.hmass()
rho_f = state.rho()

# Vapor saturado (Q=1)
state.update(CP.iP, 101325, CP.iQ, 1)
h_g = state.hmass()
rho_g = state.rho()

# Calor latente
h_fg = h_g - h_f
```

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.phase]]
- [[AbstractState.hmass]]
- [[CoolProp.PropsSI]]
