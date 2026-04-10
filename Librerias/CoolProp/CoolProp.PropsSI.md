---
title: CoolProp.PropsSI — Propiedades termodinámicas de fluidos
aliases:
  - PropsSI
  - PropsSI función
  - propiedades termodinámicas

tags:
  - coolprop
  - api/funcion
  - propiedades

# --- Clasificación ---
lib: coolprop
mod: CoolProp
tipo: funcion

# --- Comportamiento ---
retorna: float o ndarray
muta_estado: false

draft: false
---

# CoolProp.PropsSI — Propiedades termodinámicas

## Firma de la función

```python
PropsSI(
    output: str,
    input1: str,
    value1: float,
    input2: str,
    value2: float,
    fluid: str,
    *,
    fractions: Optional[List[float]] = None
) -> Union[float, np.ndarray]
```

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| Punto único (float) | `float` | `PropsSI('D','T',300,'P',1e5,'Water')` → `996.56` |
| Array de valores | `np.ndarray` | `PropsSI('D','T',[300,310,320],'P',1e5,'Water')` → array de densidades |

**Con arrays:** cualquier parámetro `value1` o `value2` puede ser un array. El retorno tiene la misma forma que el array de entrada.

```python
import numpy as np
from CoolProp.CoolProp import PropsSI

temperaturas = np.linspace(300, 350, 50)
densidades = PropsSI('D', 'T', temperaturas, 'P', 101325, 'Water')
# densidades.shape == temperaturas.shape
```

## Parámetros en detalle

### `output` — propiedad de salida

String que indica qué propiedad calcular. Ver [[Propiedades_SI]] para lista completa.

| Símbolo | Descripción | Unidad |
|---------|-------------|--------|
| `'T'` | Temperatura | K |
| `'P'` | Presión | Pa |
| `'D'` | Densidad | kg/m³ |
| `'H'` | Entalpía específica | J/kg |
| `'S'` | Entropía específica | J/(kg·K) |
| `'U'` | Energía interna específica | J/kg |
| `'Q'` | Calidad (0=líquido, 1=vapor) | - |
| `'C'` | Cp (calor específico a P cte) | J/(kg·K) |
| `'O'` | Cv (calor específico a V cte) | J/(kg·K) |
| `'V'` | Volumen específico | m³/kg |

### `input1`, `input2` — variables de entrada

Pares de variables independientes que definen el estado termodinámico. Ver [[Concepto_estado_termodinamico]].

| Input | Descripción | Unidad |
|-------|-------------|--------|
| `'T'` | Temperatura | K |
| `'P'` | Presión | Pa |
| `'H'` | Entalpía | J/kg |
| `'S'` | Entropía | J/(kg·K) |
| `'D'` | Densidad | kg/m³ |
| `'Q'` | Calidad | - |

### `value1`, `value2` — valores numéricos

`float` o `np.ndarray`. Deben ser consistentes con las unidades SI.

### `fluid` — nombre del fluido

String con el fluido. Opcionalmente con prefijo de [[Concepto_backend|backend]]:

```python
# Backend por defecto (HEOS)
PropsSI('D', 'T', 300, 'P', 1e5, 'Water')

# IF97 para agua (recomendado para agua)
PropsSI('D', 'T', 300, 'P', 1e5, 'IF97::Water')

# REFPROP (si instalado)
PropsSI('D', 'T', 300, 'P', 1e5, 'REFPROP::Water')
```

**Fluidos comunes:**

| Fluido | Nombre en CoolProp |
|--------|-------------------|
| Agua | `'Water'` |
| R134a | `'R134a'` |
| R410A | `'R410A'` |
| R290 (propano) | `'R290'` |
| Nitrógeno | `'Nitrogen'` |
| Oxígeno | `'Oxygen'` |
| CO₂ | `'CarbonDioxide'` |
| Aire | `'Air'` |

Ver [[CoolProp.has_fluid]] para verificar disponibilidad.

### `fractions` — fracciones para mezclas (opcional)

`List[float]` de fracciones másicas o molares. Requiere que `fluid` especifique los componentes con `&`.

```python
# Mezcla 50/50 en masa de R32 y R134a
PropsSI('D', 'T', 300, 'P', 1e5, 'R32&R134a', fractions=[0.5, 0.5])
```

Ver [[AbstractState.set_mass_fractions]] para más detalles sobre mezclas.

## Combinaciones válidas de entrada

| input1 + input2 | Uso típico |
|-----------------|------------|
| `'T'` + `'P'` | Estado general (líquido, vapor, gas) |
| `'P'` + `'Q'` | Saturación con calidad conocida |
| `'T'` + `'Q'` | Saturación con calidad conocida |
| `'P'` + `'H'` | Procesos reales (compresores, turbinas) |
| `'P'` + `'S'` | Procesos isentrópicos |
| `'T'` + `'D'` | Estado denso (líquido comprimido) |
| `'H'` + `'P'` | Estado por entalpía y presión |

**No todas las combinaciones son válidas para todas las regiones.** Algunas pueden fallar si el estado no existe físicamente.

## Identificar la fase

Usar `'Phase'` como `output`:

```python
phase = PropsSI('Phase', 'T', 373.15, 'P', 101325, 'Water')
```

| Valor | Significado |
|-------|-------------|
| `0` | Líquido |
| `1` | Vapor |
| `2` | Supercrítico |
| `3` | Gas (no condensable) |
| `6` | Mezcla saturada (líquido+vapor) |

Ver [[CoolProp.PhaseSI]] para más detalles.

## Casos de uso

### Propiedades de saturación

```python
# Temperatura de saturación a 1 bar (agua)
Tsat = PropsSI('T', 'P', 1e5, 'Q', 0, 'Water')

# Entalpía de vaporización a 1 bar
h_vap = PropsSI('H', 'P', 1e5, 'Q', 1, 'Water')
h_liq = PropsSI('H', 'P', 1e5, 'Q', 0, 'Water')
h_fg = h_vap - h_liq
```

### Proceso isentrópico (compresor ideal)

```python
# Estado entrada: R134a a -10°C, vapor saturado
h1 = PropsSI('H', 'T', 263.15, 'Q', 1, 'R134a')
s1 = PropsSI('S', 'T', 263.15, 'Q', 1, 'R134a')

# Estado salida: isentrópico hasta 10 bar
h2 = PropsSI('H', 'P', 1e6, 'S', s1, 'R134a')
```

### Trabajo con arrays (curvas)

```python
import numpy as np
from CoolProp.CoolProp import PropsSI

temperaturas = np.linspace(280, 400, 100)
presiones = 1e5 * np.ones_like(temperaturas)

entalpias = PropsSI('H', 'T', temperaturas, 'P', presiones, 'Water')
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `CoolProp does not have fluid '...'` | Fluido mal escrito | Verificar con [[CoolProp.has_fluid]] |
| `The given state is not valid` | Combinación de propiedades fuera de rango físico | Usar [[CoolProp.PhaseSI]] para depurar |
| `No backend could be obtained` | Backend no disponible para ese fluido | Usar `'HEOS::'` o verificar backends con [[CoolProp.get_parameter_information]] |
| `Inputs are not consistent` | Par de variables incompatible | Cambiar combinación (ej: `T+P` en lugar de `T+H` en ciertas regiones) |

## Limitaciones

- No todos los fluidos tienen todos los [[Concepto_backend|backends]]
- Estados cerca del punto crítico pueden tener baja precisión
- Algunas combinaciones (`'H'` + `'S'`) pueden fallar por no ser monotónicas
- Para cálculos repetitivos en bucles, usar [[AbstractState.__init__|AbstractState]] es más eficiente

## Alternativa: AbstractState

Para múltiples consultas al mismo fluido, [[AbstractState.__init__]] es más rápido:

```python
import CoolProp.CoolProp as CP
state = CP.AbstractState('HEOS', 'Water')
state.update(CP.iT, 300, CP.iP, 1e5)
rho = state.rho()  # en lugar de PropsSI repetidamente
```

Ver [[AbstractState.update]] y [[AbstractState.rho]] para más detalles.

## Notas relacionadas

- [[Propiedades_SI]]
- [[Concepto_estado_termodinamico]]
- [[Concepto_backend]]
- [[CoolProp.PhaseSI]]
- [[CoolProp.has_fluid]]
- [[AbstractState.__init__]]
- [[AbstractState.update]]
- [[AbstractState.rho]]
