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
    input1: int,
    value1: float,
    input2: int,
    value2: float
) -> None
```

## Valor de retorno

`None` — el método modifica el estado interno del objeto [[AbstractState]] pero no retorna ningún valor.

## Parámetros en detalle

### `input1`, `input2` — identificadores de variables

Enteros (`int`) definidos en el módulo [[Constants]]. Indican qué variable termodinámica se está especificando.

| Constante | Variable | Unidad |
|-----------|----------|--------|
| [[Constants.iT]] | Temperatura | K |
| [[Constants.iP]] | Presión | Pa |
| [[Constants.iH]] | Entalpía | J/kg |
| [[Constants.iSmass]] | Entropía | J/(kg·K) |
| [[Constants.iD]] | Densidad | kg/m³ |
| [[Constants.iQ]] | Calidad (0-1) | - |
| [[Constants.iU]] | Energía interna | J/kg |

**Importante:** No usar strings como `'T'` o `'P'`. `update` solo acepta las constantes enteras.

### `value1`, `value2` — valores numéricos

`float` con el valor de la variable especificada, en unidades SI.

## Combinaciones válidas de entrada

| input1 + input2 | Uso típico | Ejemplo |
|-----------------|------------|---------|
| `iT` + `iP` | Estado general | `state.update(CP.iT, 300, CP.iP, 1e5)` |
| `iT` + `iQ` | Saturación por temperatura | `state.update(CP.iT, 373.15, CP.iQ, 0)` |
| `iP` + `iQ` | Saturación por presión | `state.update(CP.iP, 1e5, CP.iQ, 1)` |
| `iP` + `iH` | Procesos reales (compresores) | `state.update(CP.iP, 5e5, CP.iH, 450000)` |
| `iP` + `iSmass` | Procesos isentrópicos | `state.update(CP.iP, 5e5, CP.iSmass, 1.7e3)` |
| `iT` + `iD` | Líquido comprimido | `state.update(CP.iT, 300, CP.iD, 997)` |
| `iH` + `iP` | Estado por entalpía-presión | `state.update(CP.iH, 3e6, CP.iP, 1e5)` |
| `iSmass` + `iP` | Estado por entropía-presión | `state.update(CP.iSmass, 6e3, CP.iP, 1e5)` |
| `iD` + `iP` | Estado por densidad-presión | `state.update(CP.iD, 1.2, CP.iP, 1e5)` |

## No todas las combinaciones son válidas

Algunas combinaciones pueden fallar porque no definen un estado único o porque el estado no existe físicamente:

| Combinación problemática | Razón |
|-------------------------|-------|
| `iT` + `iH` | No es monotónica en toda la región |
| `iT` + `iS` | Puede tener múltiples soluciones |
| `iH` + `iS` | Frecuentemente falla |

**Recomendación:** Usar `iT` + `iP` para estados generales, e `iP` + `iQ` o `iT` + `iQ` para saturación.

## Uso básico

### Importar constantes

```python
import CoolProp.CoolProp as CP

# Constantes disponibles directamente en CP
print(CP.iT)   # 0
print(CP.iP)   # 1
print(CP.iQ)   # 8
```

### Estado general (T, P)

```python
state = CP.AbstractState('HEOS', 'Water')

# Agua a 25°C y 1 atm
state.update(CP.iT, 298.15, CP.iP, 101325)

# Consultar propiedades después del update
rho = state.rho()  # ~997 kg/m³
```

### Saturación con calidad

```python
# Vapor saturado de R134a a 0°C
state = CP.AbstractState('HEOS', 'R134a')
state.update(CP.iT, 273.15, CP.iQ, 1.0)

# Líquido saturado a misma temperatura
state.update(CP.iT, 273.15, CP.iQ, 0.0)

# Mezcla con calidad 0.5 (50% vapor)
state.update(CP.iT, 273.15, CP.iQ, 0.5)
```

### Proceso isentrópico (compresor)

```python
# Estado 1: entrada al compresor (vapor saturado)
state = CP.AbstractState('HEOS', 'R134a')
state.update(CP.iT, 263.15, CP.iQ, 1.0)  # -10°C, vapor saturado

# Guardar entropía
s1 = state.smass()  # ~1.73 kJ/(kg·K)

# Estado 2: compresión isentrópica hasta 10 bar
state.update(CP.iP, 1e6, CP.iSmass, s1)  # P=10 bar, misma entropía

h2 = state.hmass()  # entalpía después de compresión
```

### Proceso con cambio de fase

```python
state = CP.AbstractState('HEOS', 'Water')

# Agua líquida a 20°C, 1 bar
state.update(CP.iT, 293.15, CP.iP, 1e5)
h_liq = state.hmass()

# Mismo fluido como vapor a 150°C, 1 bar
state.update(CP.iT, 423.15, CP.iP, 1e5)
h_vap = state.hmass()

print(f"Calor de vaporización: {h_vap - h_liq:.0f} J/kg")
```

## Especificar fase para evitar ambigüedades

En regiones donde existen múltiples fases (ej: cerca del punto crítico), usar [[AbstractState.specify_phase]] antes de `update`:

```python
state.specify_phase(CP.iphase_gas)  # forzar fase gas
state.update(CP.iT, 374.15, CP.iP, 2.2e7)
```

Ver [[Constants.phase_flags]] para valores disponibles.

## Verificar si el update fue exitoso

Después de `update`, se puede consultar la fase actual:

```python
state.update(CP.iT, 373.15, CP.iP, 101325)
phase = state.phase()  # 0=líquido, 1=vapor, 6=mezcla

if phase == 6:
    print("Mezcla saturada")
    Q = state.Q()  # calidad
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `The given state is not valid` | Par de variables fuera de rango físico | Verificar T, P dentro de región válida |
| `Inputs are not consistent` | Combinación de inputs no válida | Usar `iT+iP` o `iP+iQ` |
| `did not evaluate to a finite value` | Estado cerca del punto crítico o inválido | Alejar T o P del punto crítico |
| `no common root` | La solución no existe | Probar otra combinación de inputs |

## Buenas prácticas

1. **Siempre verificar que `update` no lanza excepción** antes de consultar propiedades
2. **Usar `try-except`** para manejar estados inválidos:

```python
try:
    state.update(CP.iT, 300, CP.iP, 1e8)  # presión muy alta
    rho = state.rho()
except:
    print("Estado no válido")
```

3. **Para saturación, preferir `iP+iQ` sobre `iT+iQ`** (más estable numéricamente)
4. **Reutilizar el mismo estado** para múltiples puntos:

```python
# Correcto: reutilizar
state = CP.AbstractState('HEOS', 'Water')
for T in temperatures:
    state.update(CP.iT, T, CP.iP, 1e5)
    rho = state.rho()

# Incorrecto: crear nuevo estado en cada iteración
for T in temperatures:
    state = CP.AbstractState('HEOS', 'Water')  # lento
    state.update(CP.iT, T, CP.iP, 1e5)
```

## Diferencia con PropsSI

| Aspecto | [[CoolProp.PropsSI]] | `AbstractState.update` |
|---------|---------------------|------------------------|
| Inputs | Strings (`'T'`, `'P'`) | Constantes (`CP.iT`, `CP.iP`) |
| Estado | Se crea y destruye internamente | Persiste en el objeto |
| Velocidad (bucle) | Lenta | Rápida |
| Control de fase | No | Sí (con `specify_phase`) |

## Notas relacionadas

- [[AbstractState]]
- [[Constants.iT]]
- [[Constants.iP]]
- [[Constants.iQ]]
- [[AbstractState.specify_phase]]
- [[AbstractState.phase]]
- [[CoolProp.PropsSI]]
