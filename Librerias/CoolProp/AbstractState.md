---
title: AbstractState — Estado termodinámico de bajo nivel
aliases:
  - AbstractState clase
  - estado AbstractState
  - API bajo nivel

tags:
  - coolprop
  - api/clase
  - abstractstate

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: clase

# --- Comportamiento ---
muta_estado: true

draft: false
---

# AbstractState — Estado termodinámico de bajo nivel

## Descripción

`AbstractState` es la **clase fundamental de la API de bajo nivel** de CoolProp. Representa un estado termodinámico de un fluido o mezcla, permitiendo:

- Actualizar el estado con diferentes pares de variables independientes
- Consultar múltiples propiedades sin recalcular el estado completo
- Calcular derivadas parciales
- Trabajar con mezclas y sus fracciones

**Ventaja sobre [[CoolProp.PropsSI]]:** Es significativamente más rápida cuando se realizan múltiples consultas al mismo fluido o en bucles.

## Firma del constructor

```python
class AbstractState(
    backend: str,
    fluid: str
)
```

## Parámetros del constructor

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `backend` | `str` | Motor de cálculo. Ver [[Concepto_backend]] |
| `fluid` | `str` | Nombre del fluido o mezcla (`'Water'`, `'R134a'`, `'R32&R134a'`) |

## Instanciación

```python
import CoolProp.CoolProp as CP

# Fluido puro
state = CP.AbstractState('HEOS', 'Water')

# Fluido con backend específico
state = CP.AbstractState('IF97', 'Water')

# Mezcla (fracciones se establecen después)
state = CP.AbstractState('HEOS', 'R32&R134a')
state.set_mass_fractions([0.5, 0.5])
```

## Flujo de trabajo típico

```python
# 1. Instanciar
state = CP.AbstractState('HEOS', 'Water')

# 2. Actualizar estado (definir P y T)
state.update(CP.PT_INPUTS, 101325, 298.15)

# 3. Consultar propiedades
rho = state.rho()      # densidad [kg/m³]
h = state.hmass()      # entalpía [J/kg]
s = state.smass()      # entropía [J/(kg·K)]

# 4. Cambiar estado sin recrear el objeto
state.update(CP.PT_INPUTS, 200000, 350)
rho2 = state.rho()     # nueva densidad
```

## Estados de entrada (update)

El método [[AbstractState.update]] define el estado termodinámico usando combinaciones predefinidas:

| Input Constante | Orden de valores | Uso típico |
|----------------|------------------|------------|
| `CP.PT_INPUTS` | `(P, T)` | Estado general |
| `CP.PQ_INPUTS` | `(P, Q)` | Saturación por presión |
| `CP.TQ_INPUTS` | `(T, Q)` | Saturación por temperatura |
| `CP.PH_INPUTS` | `(P, H)` | Procesos reales (compresores) |
| `CP.PSmass_INPUTS` | `(P, S)` | Procesos isentrópicos |
| `CP.HmassP_INPUTS` | `(H, P)` | Entalpía y presión |
| `CP.SmassP_INPUTS` | `(S, P)` | Entropía y presión |

```python
# Ejemplo: vapor saturado a 1 bar
state.update(CP.PQ_INPUTS, 1e5, 1.0)

# Ejemplo: líquido subenfriado a 25°C
state.update(CP.PT_INPUTS, 1e5, 298.15)
```

## Propiedades consultables

| Método | Propiedad | Unidad |
|--------|-----------|--------|
| [[AbstractState.T]] | Temperatura | K |
| [[AbstractState.p]] | Presión | Pa |
| [[AbstractState.rho]] | Densidad | kg/m³ |
| [[AbstractState.hmass]] | Entalpía específica | J/kg |
| [[AbstractState.smass]] | Entropía específica | J/(kg·K) |
| [[AbstractState.umass]] | Energía interna específica | J/kg |
| [[AbstractState.cpmass]] | Cp (calor específico a P cte) | J/(kg·K) |
| [[AbstractState.cvmass]] | Cv (calor específico a V cte) | J/(kg·K) |
| [[AbstractState.Q]] | Calidad (0=líquido, 1=vapor) | - |
| [[AbstractState.phase]] | Fase actual | - |

## Mezclas

Para mezclas, establecer fracciones después de instanciar:

```python
# Crear estado para mezcla binaria
state = CP.AbstractState('HEOS', 'R32&R134a')

# Fracciones másicas (50% cada uno)
state.set_mass_fractions([0.5, 0.5])

# Actualizar estado de la mezcla
state.update(CP.PT_INPUTS, 1e5, 300)
h_mix = state.hmass()
```

Ver [[AbstractState.set_mass_fractions]] y [[AbstractState.set_mole_fractions]].

## Derivadas parciales

```python
# (∂ρ/∂T) a P constante
deriv = state.first_partial_deriv(CP.iD, CP.iT, CP.iP)

# (∂h/∂P) a T constante
deriv = state.first_partial_deriv(CP.iH, CP.iP, CP.iT)
```

Ver [[AbstractState.first_partial_deriv]] y [[AbstractState.second_partial_deriv]].

## Rendimiento

`AbstractState` es mucho más rápida que [[CoolProp.PropsSI]] para múltiples consultas:

```python
# Lento: PropsSI en bucle
for T in temperaturas:
    h = PropsSI('H', 'T', T, 'P', 1e5, 'Water')

# Rápido: AbstractState
state = CP.AbstractState('HEOS', 'Water')
for T in temperaturas:
    state.update(CP.PT_INPUTS, 1e5, T)
    h = state.hmass()
```

## Diferencias con PropsSI

| Aspecto | [[CoolProp.PropsSI]] | `AbstractState` |
|---------|---------------------|-----------------|
| Facilidad | Alta (una línea) | Media (requiere instanciación) |
| Velocidad (1 consulta) | Buena | Similar |
| Velocidad (N consultas) | Lenta | Rápida |
| Derivadas parciales | No | Sí |
| Control de fase | Limitado | `specify_phase` disponible |
| Mezclas | Limitado | Completo |

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AbstractState.__init__() missing 1 required positional argument: 'fluid'` | Faltó el fluido | `CP.AbstractState('HEOS', 'Water')` |
| `The given state is not valid` | Estado fuera de rango | Verificar P, T dentro de región válida |

## Notas relacionadas

- [[CoolProp.PropsSI]]
- [[Concepto_backend]]
- [[AbstractState.update]]
- [[AbstractState.rho]]
- [[AbstractState.hmass]]
- [[Constants]]
- [[AbstractState.set_mass_fractions]]