---
title: Constants — Identificadores para variables termodinámicas
aliases:
  - constantes CoolProp
  - CP.iT
  - CP.iP
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

El módulo `Constants` de CoolProp proporciona **enteros predefinidos** que actúan como identificadores para las variables termodinámicas. Se utilizan exclusivamente en la API de bajo nivel ([[AbstractState]]) para especificar qué variables se están proporcionando o consultando.

**No son strings.** No se usan con [[CoolProp.PropsSI]].

## Importación

```python
import CoolProp.CoolProp as CP

# Las constantes están disponibles directamente en CP
print(CP.iT)   # 0
print(CP.iP)   # 1
```

## Tabla de constantes

| Constante | Valor | Variable | Unidad | Uso típico |
|-----------|-------|----------|--------|------------|
| `CP.iT` | 0 | Temperatura | K | `update`, derivadas |
| `CP.iP` | 1 | Presión | Pa | `update`, derivadas |
| `CP.iD` | 2 | Densidad | kg/m³ | `update`, derivadas |
| `CP.iH` | 4 | Entalpía específica | J/kg | `update`, derivadas |
| `CP.iSmass` | 5 | Entropía específica | J/(kg·K) | `update`, derivadas |
| `CP.iU` | 6 | Energía interna específica | J/kg | `update`, derivadas |
| `CP.iQ` | 8 | Calidad (0=líquido, 1=vapor) | - | `update` |
| `CP.iCpmass` | 9 | Cp (calor específico a P cte) | J/(kg·K) | derivadas |
| `CP.iCvmass` | 10 | Cv (calor específico a V cte) | J/(kg·K) | derivadas |

## Constantes de fase (specify_phase)

Usadas con [[AbstractState.specify_phase]] para forzar una fase específica:

| Constante | Valor | Fase |
|-----------|-------|------|
| `CP.iphase_liquid` | 0 | Líquido |
| `CP.iphase_gas` | 1 | Gas/vapor |
| `CP.iphase_supercritical` | 2 | Supercrítico |
| `CP.iphase_supercritical_gas` | 3 | Gas supercrítico |
| `CP.iphase_supercritical_liquid` | 4 | Líquido supercrítico |
| `CP.iphase_critical_point` | 5 | Punto crítico |
| `CP.iphase_twophase` | 6 | Mezcla saturada (líquido+vapor) |

## Uso en AbstractState.update

```python
import CoolProp.CoolProp as CP

state = CP.AbstractState('HEOS', 'Water')

# Usando constantes como identificadores
state.update(CP.iT, 300, CP.iP, 101325)  # T y P
state.update(CP.iP, 1e5, CP.iQ, 1.0)     # P y calidad (vapor saturado)
state.update(CP.iT, 373.15, CP.iQ, 0.0)  # T y calidad (líquido saturado)
state.update(CP.iP, 5e5, CP.iH, 450000)  # P y entalpía
```

## Uso en derivadas parciales

```python
# (∂ρ/∂T) a P constante
deriv = state.first_partial_deriv(CP.iD, CP.iT, CP.iP)

# (∂h/∂P) a T constante
deriv = state.first_partial_deriv(CP.iH, CP.iP, CP.iT)
```

Los parámetros siguen el orden: `(output, input1, input2)`.

## Uso en consultas de propiedades

Las constantes **no** se usan para consultar propiedades. Para eso existen métodos específicos:

```python
# Correcto
T = state.T()
rho = state.rho()

# Incorrecto (no funciona)
T = state.update(CP.iT)  # No tiene sentido
```

## Relación con PropsSI

| Aspecto | [[CoolProp.PropsSI]] | `Constants` + [[AbstractState]] |
|---------|---------------------|--------------------------------|
| Identificadores | Strings (`'T'`, `'P'`) | Enteros (`CP.iT`, `CP.iP`) |
| Facilidad | Alta (legible) | Media (requiere conocer códigos) |
| Flexibilidad | Baja | Alta (derivadas, control de fase) |

## Buenas prácticas

1. **Siempre importar `CoolProp.CoolProp as CP`** para tener acceso a las constantes
2. **Usar los nombres simbólicos** (`CP.iT`), no los valores numéricos (`0`)
3. **Para derivadas**, recordar el orden: `first_partial_deriv(output, input1, input2)`
4. **Para `specify_phase`**, usar las constantes `CP.iphase_*`

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `NameError: name 'iT' is not defined` | No se importó CP correctamente | `import CoolProp.CoolProp as CP` |
| `Expected int, got str` | Se usó string en lugar de constante | Usar `CP.iT` no `'T'` |
| `Invalid input pair` | Combinación de constantes no válida | Verificar tabla de combinaciones en [[AbstractState.update]] |

## Notas relacionadas

- [[AbstractState.update]]
- [[AbstractState.first_partial_deriv]]
- [[AbstractState.specify_phase]]
- [[CoolProp.PropsSI]]
