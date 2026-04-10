---
title: AbstractState.update — Actualizar estado termodinámico
aliases:
  - update
  - actualizar estado
  - cambiar estado

tags:
  - coolprop
  - api/metodo
  - abstractstate

# --- Clasificación ---
lib: coolprop
obj: AbstractState
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: true

draft: false
---

# AbstractState.update — Actualizar estado termodinámico

## Firma de la función

```python
AbstractState.update(
    input_pair: int,
    value1: float,
    value2: float
) -> None
```

## Valor de retorno

`None` — el método modifica el estado interno del objeto [[AbstractState]] pero no retorna ningún valor.

## Parámetros en detalle

### `input_pair` — combinación predefinida

Entero (`int`) que define qué par de variables se está especificando. Las combinaciones están definidas en el módulo [[Constants]].

| Constante | Variables | Orden | Unidades |
|-----------|-----------|-------|----------|
| `CP.PT_INPUTS` | Presión, Temperatura | `(P, T)` | Pa, K |
| `CP.PQ_INPUTS` | Presión, Calidad | `(P, Q)` | Pa, - |
| `CP.TQ_INPUTS` | Temperatura, Calidad | `(T, Q)` | K, - |
| `CP.PH_INPUTS` | Presión, Entalpía | `(P, H)` | Pa, J/kg |
| `CP.PSmass_INPUTS` | Presión, Entropía | `(P, S)` | Pa, J/(kg·K) |
| `CP.HmassP_INPUTS` | Entalpía, Presión | `(H, P)` | J/kg, Pa |
| `CP.SmassP_INPUTS` | Entropía, Presión | `(S, P)` | J/(kg·K), Pa |
| `CP.DP_INPUTS` | Densidad, Presión | `(D, P)` | kg/m³, Pa |
| `CP.HmassQ_INPUTS` | Entalpía, Calidad | `(H, Q)` | J/kg, - |
| `CP.SmassQ_INPUTS` | Entropía, Calidad | `(S, Q)` | J/(kg·K), - |

### `value1`, `value2` — valores numéricos

`float` con el valor de las variables en el orden especificado por `input_pair`, en unidades SI.

## Uso básico

### Importar constantes

```python
import CoolProp.CoolProp as CP

# Combinaciones disponibles
print(CP.PT_INPUTS)      # 0
print(CP.PQ_INPUTS)      # 1
print(CP.TQ_INPUTS)      # 2
```

### Estado general (P, T)

```python
state = CP.AbstractState('HEOS', 'Water')

# Agua a 25°C y 1 atm
state.update(CP.PT_INPUTS, 101325, 298.15)

# Consultar propiedades después del update
rho = state.rho()  # ~997 kg/m³
```

### Saturación por presión

```python
# Vapor saturado de R134a a 5 bar
state = CP.AbstractState('HEOS', 'R134a')
state.update(CP.PQ_INPUTS, 5e5, 1.0)

# Líquido saturado a 5 bar
state.update(CP.PQ_INPUTS, 5e5, 0.0)

# Mezcla con calidad 0.5
state.update(CP.PQ_INPUTS, 5e5, 0.5)
```

### Saturación por temperatura

```python
# Vapor saturado a 100°C
state = CP.AbstractState('HEOS', 'Water')
state.update(CP.TQ_INPUTS, 373.15, 1.0)

# Líquido saturado a 100°C
state.update(CP.TQ_INPUTS, 373.15, 0.0)
```

### Proceso isentrópico (compresor)

```python
# Estado 1: entrada al compresor (vapor saturado a -10°C)
state = CP.AbstractState('HEOS', 'R134a')
state.update(CP.TQ_INPUTS, 263.15, 1.0)

# Guardar entropía
s1 = state.smass()

# Estado 2: compresión isentrópica hasta 10 bar
state.update(CP.PSmass_INPUTS, 1e6, s1)

h2 = state.hmass()  # entalpía después de compresión
```

### Proceso con cambio de fase

```python
state = CP.AbstractState('HEOS', 'Water')

# Agua líquida a 20°C, 1 bar
state.update(CP.PT_INPUTS, 1e5, 293.15)
h_liq = state.hmass()

# Mismo fluido como vapor a 150°C, 1 bar
state.update(CP.PT_INPUTS, 1e5, 423.15)
h_vap = state.hmass()

print(f"Calor de vaporización: {h_vap - h_liq:.0f} J/kg")
```

### Estado por entalpía y presión

```python
# Estado definido por entalpía y presión
state.update(CP.PH_INPUTS, 5e5, 450000)
T = state.T()
```

## Especificar fase para evitar ambigüedades

En regiones donde existen múltiples fases (ej: cerca del punto crítico), usar [[AbstractState.specify_phase]] antes de `update`:

```python
state.specify_phase(CP.iphase_gas)  # forzar fase gas
state.update(CP.PT_INPUTS, 2.2e7, 374.15)
```

Ver [[Constants.phase_flags]] para valores disponibles.

## Verificar si el update fue exitoso

Después de `update`, se puede consultar la fase actual:

```python
state.update(CP.PT_INPUTS, 1e5, 373.15)
phase = state.phase()  # 6 (mezcla saturada en este caso)

if phase == 6:
    Q = state.Q()  # calidad
    print(f"Calidad: {Q}")
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `The given state is not valid` | Par de variables fuera de rango físico | Verificar P, T dentro de región válida |
| `Inputs are not consistent` | Combinación no válida | Usar `PT_INPUTS` o `PQ_INPUTS` |
| `did not evaluate to a finite value` | Estado cerca del punto crítico | Alejar T o P del punto crítico |
| `no common root` | La solución no existe | Probar otra combinación de inputs |

## Buenas prácticas

1. **Usar `try-except`** para manejar estados inválidos:

```python
try:
    state.update(CP.PT_INPUTS, 1e8, 300)  # presión muy alta
    rho = state.rho()
except:
    print("Estado no válido")
```

2. **Reutilizar el mismo estado** para múltiples puntos:

```python
# Correcto: reutilizar
state = CP.AbstractState('HEOS', 'Water')
for T in temperatures:
    state.update(CP.PT_INPUTS, 1e5, T)
    rho = state.rho()

# Incorrecto: crear nuevo estado en cada iteración
for T in temperatures:
    state = CP.AbstractState('HEOS', 'Water')  # lento
    state.update(CP.PT_INPUTS, 1e5, T)
```

## Diferencia con PropsSI

| Aspecto | [[CoolProp.PropsSI]] | `AbstractState.update` |
|---------|---------------------|------------------------|
| Inputs | Strings (`'T'`, `'P'`) | Combinaciones (`CP.PT_INPUTS`) |
| Estado | Se crea y destruye internamente | Persiste en el objeto |
| Velocidad (bucle) | Lenta | Rápida |
| Control de fase | No | Sí (con `specify_phase`) |

## Notas relacionadas

- [[AbstractState]]
- [[Constants]]
- [[AbstractState.specify_phase]]
- [[AbstractState.phase]]
- [[CoolProp.PropsSI]]
