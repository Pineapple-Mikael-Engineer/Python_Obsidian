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

# 2. Actualizar estado (definir T y P)
state.update(CP.iT, 300, CP.iP, 101325)

# 3. Consultar propiedades
rho = state.rho()      # densidad [kg/m³]
h = state.hmass()      # entalpía [J/kg]
s = state.smass()      # entropía [J/(kg·K)]

# 4. Cambiar estado sin recrear el objeto
state.update(CP.iT, 350, CP.iP, 200000)
rho2 = state.rho()     # nueva densidad
```

## Estados de entrada (update)

El método [[AbstractState.update]] define el estado termodinámico usando pares de variables independientes:

| Par de entrada | Constantes | Uso típico |
|----------------|------------|------------|
| `iT` + `iP` | [[Constants.iT]], [[Constants.iP]] | Estado general |
| `iP` + `iQ` | [[Constants.iP]], [[Constants.iQ]] | Saturación con calidad |
| `iT` + `iQ` | [[Constants.iT]], [[Constants.iQ]] | Saturación con calidad |
| `iP` + `iH` | [[Constants.iP]], [[Constants.iH]] | Procesos reales (compresores) |
| `iP` + `iSmass` | [[Constants.iP]], [[Constants.iSmass]] | Procesos isentrópicos |

```python
# Ejemplo: vapor saturado a 1 bar
state.update(CP.iP, 1e5, CP.iQ, 1.0)

# Ejemplo: líquido subenfriado a 25°C
state.update(CP.iT, 298.15, CP.iQ, 0.0)
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
| [[AbstractState.phase]] | Fase actual (0,1,6,etc.) | - |

## Mezclas

Para mezclas, establecer fracciones después de instanciar:

```python
# Crear estado para mezcla binaria
state = CP.AbstractState('HEOS', 'R32&R134a')

# Fracciones másicas (50% cada uno)
state.set_mass_fractions([0.5, 0.5])

# Verificar fracciones actuales
mass_fracs = state.get_mass_fractions()  # [0.5, 0.5]

# Actualizar estado de la mezcla
state.update(CP.iT, 300, CP.iP, 1e5)
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
    state.update(CP.iT, T, CP.iP, 1e5)
    h = state.hmass()
```

## Diferencias con PropsSI

| Aspecto | [[CoolProp.PropsSI]] | `AbstractState` |
|---------|---------------------|-----------------|
| Facilidad | Alta (una línea) | Media (requiere instanciación) |
| Velocidad (1 consulta) | Buena | Similar |
| Velocidad (N consultas) | Lenta (recalcula backend) | Rápida (reutiliza estado) |
| Derivadas parciales | No | Sí |
| Control de fase | Limitado | `specify_phase` disponible |
| Mezclas | Limitado | Completo |

## Buenas prácticas

1. **Reutilizar el mismo objeto** para múltiples actualizaciones en lugar de crear uno nuevo
2. **Usar `'HEOS'` como backend** a menos que tengas razón específica para otro
3. **Para agua en aplicaciones industriales**, considerar `'IF97'`
4. **Verificar fase** con [[AbstractState.phase]] cuando los resultados sean inesperados
5. **En bucles largos**, instanciar fuera del bucle y solo llamar a `update` dentro

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AbstractState.__init__() missing 1 required positional argument: 'fluid'` | Faltó el fluido | `CP.AbstractState('HEOS', 'Water')` |
| `The given state is not valid` | Estado fuera de rango físico | Verificar T, P dentro de región válida |
| `Index out of bounds` | Fracciones mal especificadas | Asegurar que sum(fraciones) = 1.0 |

## Notas relacionadas

- [[CoolProp.PropsSI]]
- [[Concepto_backend]]
- [[AbstractState.update]]
- [[AbstractState.rho]]
- [[AbstractState.hmass]]
- [[Constants.iT]]
- [[Constants.iP]]
- [[AbstractState.set_mass_fractions]]
