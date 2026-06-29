---
title: CoolProp.get_parameter_information — describir un parámetro por su índice
aliases:
  - get_parameter_information
  - unidades de un parámetro
tags: [coolprop, api/funcion, metadata]
lib: coolprop
mod: CoolProp
tipo: funcion
retorna: str
muta_estado: false
draft: false
---

# CoolProp.get_parameter_information — describir un parámetro por su índice

Devuelve información descriptiva de un parámetro (nombre corto, nombre largo, **unidades** SI, tipo de entrada/salida), identificándolo por su **índice entero**, no por su clave string. Se usa junto a `get_parameter_index(key)`, que traduce la clave (`'T'`, `'P'`, `'H'`...) a ese índice.

## Firma de la función

```python
get_parameter_information(index: int, info: str) -> str

# función compañera para obtener el índice desde la clave:
get_parameter_index(key: str) -> int
```

## Valor de retorno

Un `str` con el campo pedido del parámetro.

| `info` | Qué devuelve | Ejemplo (`'T'`) |
|--------|--------------|-----------------|
| `'short'` | nombre/símbolo corto | `'T'` |
| `'long'` | nombre descriptivo | `'Temperature'` |
| `'units'` | unidades SI | `'K'` |
| `'IO'` | si sirve de entrada/salida | `'IO'` |

## Parámetros en detalle

### `index` — el índice ENTERO del parámetro

`int`. **No es la clave string**: hay que obtenerlo antes con `get_parameter_index('T')`. Por ejemplo `'T'` → `19`, `'P'` → `20`, `'H'` → `41` en CoolProp 8.0.0 (los números pueden variar entre versiones; por eso conviene calcularlos, no escribirlos a mano).

### `info` — qué campo del parámetro

String, uno de `'short'`, `'long'`, `'units'`, `'IO'`.

## Casos de uso

### Unidades SI de una clave de propiedad

```python
import CoolProp.CoolProp as CP

idx = CP.get_parameter_index('T')            # -> 19  (índice entero de la temperatura)
CP.get_parameter_information(idx, 'units')   # -> 'K'
CP.get_parameter_information(idx, 'long')    # -> 'Temperature'
```

### Documentar varias propiedades de golpe

```python
import CoolProp.CoolProp as CP

for clave in ['T', 'P', 'H', 'D']:
    idx = CP.get_parameter_index(clave)
    largo = CP.get_parameter_information(idx, 'long')
    unidad = CP.get_parameter_information(idx, 'units')
    print(f"{clave}: {largo} [{unidad}]")

# T: Temperature [K]
# P: Pressure [Pa]
# H: Mass specific enthalpy [J/kg]
# D: Mass density [kg/m^3]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: Unable to match the key [99999] ...` | índice entero fuera de rango | obtener el índice con `get_parameter_index`, no inventarlo |
| pasar `'T'` directamente como primer argumento | se confundió clave string con índice entero | traducir primero: `idx = get_parameter_index('T')` |
| `ValueError: Your input name [NOPE] is not valid ... (names are case sensitive)` | clave inexistente o mal capitalizada en `get_parameter_index` | usar una clave válida (ver [[Constants]]); respeta mayúsculas |

## Limitaciones

- Devuelve **descripciones**, no valores: para el valor numérico de una propiedad usa [[CoolProp.PropsSI|PropsSI]].
- Los índices enteros son detalle interno y pueden cambiar entre versiones; trátalos como opacos (obtenidos vía `get_parameter_index`).

## Notas relacionadas

- [[Constants]] — claves de propiedad y pares de entrada
- [[concepto_propiedades_SI]] — las unidades SI de cada propiedad
- [[CoolProp.PropsSI]]
- [[CoolProp.get_global_param_string]] — `'parameter_list'` con todas las claves
