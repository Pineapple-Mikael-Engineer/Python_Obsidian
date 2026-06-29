---
title: CoolProp.PhaseSI — la fase como texto legible
aliases:
  - PhaseSI
  - fase de un fluido
tags: [coolprop, api/funcion, fase]
lib: coolprop
mod: CoolProp
tipo: funcion
retorna: str
muta_estado: false
draft: false
---

# CoolProp.PhaseSI — la fase como texto legible

Devuelve, como **string legible**, en qué fase (líquido, gas, supercrítico, bifásico...) se encuentra un fluido en un estado dado. Es el complemento "humano" de pedir `'Phase'` a [[CoolProp.PropsSI|PropsSI]], que devuelve un **entero** poco intuitivo. Igual que `PropsSI`, fija el estado con **dos** propiedades independientes.

## Firma de la función

```python
PhaseSI(
    In1Name: str, In1Val: float,
    In2Name: str, In2Val: float,
    Fluid: str,
) -> str
```

## Valor de retorno

Un `str` con el nombre de la fase. Valores posibles (verificados en 8.0.0):

| String devuelto | Significado |
|-----------------|-------------|
| `'liquid'` | líquido subenfriado / comprimido |
| `'gas'` | gas / vapor por debajo del punto crítico |
| `'twophase'` | mezcla líquido + vapor (campana de saturación) |
| `'supercritical'` | T y P por encima de las críticas |
| `'supercritical_gas'` | P < pcrit pero T > Tcrit |
| `'supercritical_liquid'` | T < Tcrit pero P > pcrit |
| `'critical_point'` | justo en el punto crítico |

### Contraste con `PropsSI('Phase', ...)`

`PhaseSI` y `PropsSI('Phase',...)` responden lo mismo, pero en distinto tipo: uno texto, otro un código entero (`0.0` para líquido). Para lógica de programa el entero es cómodo; para leer e imprimir, el string de `PhaseSI` es claro.

```python
import CoolProp.CoolProp as CP

CP.PhaseSI('T', 300, 'P', 101325, 'Water')           # -> 'liquid'
CP.PropsSI('Phase', 'T', 300, 'P', 101325, 'Water')  # -> 0.0   (mismo estado, código int)
```

Ver el mapeo completo de códigos enteros en [[CoolProp.PropsSI]] y [[Constants]].

## Parámetros en detalle

### `In1Name`, `In2Name` — el par de variables de estado

Dos claves de propiedad independientes (`'T'`, `'P'`, `'D'`, `'Q'`, `'H'`, `'S'`...), igual que en [[CoolProp.PropsSI|PropsSI]]. El par fija el [[concepto_estado_termodinamico|estado]].

### `In1Val`, `In2Val` — los valores en SI

`float` en unidades SI: temperatura en K, presión en Pa, densidad en kg/m³, etc.

### `Fluid` — el fluido

String con el fluido, opcionalmente con prefijo de [[concepto_backend|backend]] (`'HEOS::Water'`, `'IF97::Water'`).

## Casos de uso

### Las fases del agua a 1 atm

```python
import CoolProp.CoolProp as CP

CP.PhaseSI('T', 300, 'P', 101325, 'Water')  # -> 'liquid'  (27 °C, líquida)
CP.PhaseSI('T', 500, 'P', 101325, 'Water')  # -> 'gas'     (227 °C, vapor)
```

### Estado supercrítico y bifásico

```python
import CoolProp.CoolProp as CP

CP.PhaseSI('T', 700, 'P', 3e7, 'Water')      # -> 'supercritical'      (T>Tcrit y P>pcrit)
CP.PhaseSI('T', 800, 'P', 1e7, 'Water')      # -> 'supercritical_gas'  (T>Tcrit, P<pcrit)
CP.PhaseSI('P', 101325, 'Q', 0.5, 'Water')   # -> 'twophase'           (saturación, calidad 0.5)
```

### Depurar un "estado no válido"

Si una llamada a [[CoolProp.PropsSI|PropsSI]] falla con un par de entradas, `PhaseSI` ayuda a entender en qué región cae el punto:

```python
import CoolProp.CoolProp as CP

fase = CP.PhaseSI('T', 373.15, 'P', 101325, 'Water')
print(fase)  # -> 'twophase'  (justo en la línea de saturación a 1 atm)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `... is not a fluid` / nombre inválido | fluido mal escrito | verificar con `'Water' in CP.get_global_param_string('fluids_list').split(',')` (ver [[CoolProp.get_global_param_string]]) |
| esperar un número y recibir texto | confundir con `PropsSI('Phase',...)` | `PhaseSI` devuelve **string**; el entero lo da `PropsSI` |
| confundir `'gas'` y `'supercritical_gas'` | no distinguir si T supera la crítica | `'gas'` es subcrítico; `'supercritical_gas'` es T>Tcrit con P<pcrit |

## Limitaciones

- Solo informa de la fase; no devuelve propiedades numéricas (usa [[CoolProp.PropsSI|PropsSI]] para eso).
- Cerca de la línea de saturación o del punto crítico, pequeñas variaciones del estado cambian la fase devuelta.
- Para mezclas el concepto de "fase" es más delicado que en fluidos puros.

## Notas relacionadas

- [[CoolProp.PropsSI]] — devuelve la fase como entero con `output='Phase'`
- [[concepto_estado_termodinamico]]
- [[Constants]]
