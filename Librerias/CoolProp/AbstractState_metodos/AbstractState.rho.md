---
title: AbstractState.rho — Densidad
aliases:
  - rho
  - densidad
  - density

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

# AbstractState.rho — Densidad

## Firma de la función

```python
AbstractState.rho() -> float
```

## Valor de retorno

`float` — Densidad en **kg/m³**.

| Fluido | Condiciones | Valor típico |
|--------|-------------|--------------|
| Agua | 25°C, 1 atm | ~997 kg/m³ |
| Agua | 100°C, 1 atm (vapor) | ~0.59 kg/m³ |
| R134a | 20°C, vapor saturado | ~34 kg/m³ |
| Aire | 25°C, 1 atm | ~1.18 kg/m³ |

## Uso básico

```python
import CoolProp.CoolProp as CP

# Crear estado
state = CP.AbstractState('HEOS', 'Water')

# Definir estado (T=25°C, P=1 atm)
state.update(CP.iT, 298.15, CP.iP, 101325)

# Obtener densidad
rho = state.rho()
print(f"Densidad: {rho:.2f} kg/m³")  # Densidad: 997.05 kg/m³
```

## Relación con volumen específico

La densidad es el inverso del volumen específico:

```python
v = 1.0 / state.rho()  # volumen específico en m³/kg
```

## Comportamiento en diferentes regiones

### Líquido (densidad alta)

```python
state.update(CP.iT, 293.15, CP.iP, 101325)  # Agua líquida
rho = state.rho()  # ~998 kg/m³
```

### Vapor (densidad baja)

```python
state.update(CP.iT, 373.15, CP.iP, 101325)  # Vapor a 100°C
rho = state.rho()  # ~0.59 kg/m³
```

### Mezcla saturada (líquido+vapor)

```python
state.update(CP.iP, 101325, CP.iQ, 0.5)  # Calidad 0.5
rho_liq = state.rho()  # Densidad de la mezcla (promedio)
# Nota: rho() en mezcla saturada retorna la densidad promedio
```

Para obtener densidades de líquido y vapor saturados por separado:

```python
# Líquido saturado
state.update(CP.iP, 101325, CP.iQ, 0)
rho_f = state.rho()

# Vapor saturado
state.update(CP.iP, 101325, CP.iQ, 1)
rho_g = state.rho()
```

### Supercrítico

```python
state.update(CP.iT, 400, CP.iP, 2.5e7)  # Agua supercrítica
rho = state.rho()  # Valor intermedio entre líquido y vapor
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `The given state is not valid` | No se llamó a `update` antes | Ejecutar `state.update(...)` primero |
| Valores extremos (ej: 1e-6) | Estado cerca del punto crítico | Verificar T, P dentro de rango válido |

## Rendimiento

`AbstractState.rho()` es **extremadamente rápida** después de `update`. La operación costosa es `update`, no la consulta de propiedades.

```python
# Lento (update por cada consulta)
for T in temperaturas:
    state.update(CP.iT, T, CP.iP, 1e5)
    rho = state.rho()  # rho es rápida

# Rápido (un solo update, múltiples consultas)
state.update(CP.iT, 298.15, CP.iP, 1e5)
rho1 = state.rho()
h1 = state.hmass()
s1 = state.smass()
# Todas las consultas son inmediatas
```

## Comparación con PropsSI

| Aspecto | `PropsSI('D', ...)` | `AbstractState.rho()` |
|---------|---------------------|----------------------|
| Sintaxis | `PropsSI('D', 'T', 300, 'P', 1e5, 'Water')` | `state.rho()` |
| Velocidad (1 consulta) | Similar | Similar |
| Velocidad (N consultas) | Lenta (recalcula backend) | Rápida (reutiliza estado) |
| Requiere `update` | No | Sí |

## Notas relacionadas

- [[AbstractState]]
- [[AbstractState.update]]
- [[AbstractState.hmass]]
- [[AbstractState.smass]]
- [[CoolProp.PropsSI]]
