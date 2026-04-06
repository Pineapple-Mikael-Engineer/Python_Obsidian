---
title: Constants — Identificadores para variables termodinámicas
aliases:
  - constantes CoolProp
  - CP.iT
  - CP.PT_INPUTS
  - identificadores

tags:
  - coolprop
  - api/config
  - constants

# --- Clasificación ---
lib: coolprop
mod: Constants
tipo: constantes

draft: false
---

# Constants — Identificadores para variables termodinámicas

## Descripción

El módulo `Constants` de CoolProp proporciona **enteros predefinidos** que actúan como identificadores. Se dividen en tres categorías:

1. **Combinaciones de entrada** → para `AbstractState.update`
2. **Variables individuales** → para derivadas parciales
3. **Identificadores de fase** → para `specify_phase`

## Importación

```python
import CoolProp.CoolProp as CP

# Todas las constantes están disponibles directamente en CP
```

## 1. Combinaciones de entrada (para update)

Estas son las **más importantes** para `AbstractState.update`. Definen qué par de variables se está especificando y en qué orden.

| Constante | Variables | Orden | Uso típico |
|-----------|-----------|-------|------------|
| `CP.PT_INPUTS` | Presión, Temperatura | `(P, T)` | Estado general |
| `CP.PQ_INPUTS` | Presión, Calidad | `(P, Q)` | Saturación por presión |
| `CP.TQ_INPUTS` | Temperatura, Calidad | `(T, Q)` | Saturación por temperatura |
| `CP.PH_INPUTS` | Presión, Entalpía | `(P, H)` | Procesos reales |
| `CP.PSmass_INPUTS` | Presión, Entropía | `(P, S)` | Procesos isentrópicos |
| `CP.HmassP_INPUTS` | Entalpía, Presión | `(H, P)` | Estado por entalpía |
| `CP.SmassP_INPUTS` | Entropía, Presión | `(S, P)` | Estado por entropía |
| `CP.DP_INPUTS` | Densidad, Presión | `(D, P)` | Líquido comprimido |
| `CP.DT_INPUTS` | Densidad, Temperatura | `(D, T)` | Estado por densidad |
| `CP.HmassQ_INPUTS` | Entalpía, Calidad | `(H, Q)` | Saturación por entalpía |
| `CP.SmassQ_INPUTS` | Entropía, Calidad | `(S, Q)` | Saturación por entropía |

### Ejemplo

```python
state.update(CP.PT_INPUTS, 101325, 298.15)  # P y T
state.update(CP.PQ_INPUTS, 101325, 1.0)     # P y Q (vapor saturado)
state.update(CP.PSmass_INPUTS, 1e6, s1)     # P y S (isentrópico)
```

## 2. Variables individuales (para derivadas)

Usadas en `first_partial_deriv` y `second_partial_deriv`.

| Constante | Variable | Unidad |
|-----------|----------|--------|
| `CP.iT` | Temperatura | K |
| `CP.iP` | Presión | Pa |
| `CP.iD` | Densidad | kg/m³ |
| `CP.iH` | Entalpía específica | J/kg |
| `CP.iSmass` | Entropía específica | J/(kg·K) |
| `CP.iU` | Energía interna específica | J/kg |
| `CP.iQ` | Calidad | - |
| `CP.iCpmass` | Cp | J/(kg·K) |
| `CP.iCvmass` | Cv | J/(kg·K) |

### Ejemplo

```python
# (∂ρ/∂T) a P constante
deriv = state.first_partial_deriv(CP.iD, CP.iT, CP.iP)
```

## 3. Identificadores de fase (para specify_phase)

Usados con `AbstractState.specify_phase` para forzar una fase específica.

| Constante | Valor | Fase |
|-----------|-------|------|
| `CP.iphase_liquid` | 0 | Líquido |
| `CP.iphase_gas` | 1 | Gas / Vapor |
| `CP.iphase_supercritical` | 2 | Supercrítico |
| `CP.iphase_supercritical_gas` | 3 | Gas supercrítico |
| `CP.iphase_supercritical_liquid` | 4 | Líquido supercrítico |
| `CP.iphase_critical_point` | 5 | Punto crítico |
| `CP.iphase_twophase` | 6 | Mezcla saturada |

### Ejemplo

```python
state.specify_phase(CP.iphase_gas)  # Forzar fase gas
state.update(CP.PT_INPUTS, 2.2e7, 374.15)
```

## Resumen de uso

| Método | Qué constantes usa |
|--------|-------------------|
| `AbstractState.update` | `CP.PT_INPUTS`, `CP.PQ_INPUTS`, etc. |
| `AbstractState.first_partial_deriv` | `CP.iT`, `CP.iP`, `CP.iD`, etc. |
| `AbstractState.specify_phase` | `CP.iphase_liquid`, `CP.iphase_gas`, etc. |

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `NameError: name 'PT_INPUTS' is not defined` | Importación incorrecta | `import CoolProp.CoolProp as CP` |
| `Expected int, got str` | Se usó string en lugar de constante | Usar `CP.PT_INPUTS` no `'PT_INPUTS'` |
| `Invalid input pair` | Combinación no válida para el fluido | Usar `PT_INPUTS` o `PQ_INPUTS` |

## Notas relacionadas

- [[AbstractState.update]]
- [[AbstractState.first_partial_deriv]]
- [[AbstractState.specify_phase]]
- [[CoolProp.PropsSI]]
