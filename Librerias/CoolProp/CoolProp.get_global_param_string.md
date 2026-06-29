---
title: CoolProp.get_global_param_string — metadata global de CoolProp
aliases:
  - get_global_param_string
  - lista de fluidos
  - versión de CoolProp
tags: [coolprop, api/funcion, metadata]
lib: coolprop
mod: CoolProp
tipo: funcion
retorna: str
muta_estado: false
draft: false
---

# CoolProp.get_global_param_string — metadata global de CoolProp

Devuelve, como string, información **global de la biblioteca** (no de un fluido concreto): versión, revisión de git, la **lista de fluidos disponibles**, las mezclas predefinidas, la lista de parámetros, etc. Su uso más valioso en la práctica es **comprobar si un fluido existe**, porque CoolProp no tiene una función `has_fluid`.

## Firma de la función

```python
get_global_param_string(param: str) -> str
```

## Valor de retorno

Un `str`. Cuando la información es una colección (fluidos, mezclas...), viene como **una sola cadena separada por comas** que tú divides con `.split(',')`.

| `param` | Qué devuelve | Ejemplo de retorno |
|---------|--------------|--------------------|
| `'version'` | versión de CoolProp | `'8.0.0'` |
| `'gitrevision'` | hash del commit | `'ae81610e7d23...'` |
| `'fluids_list'` | fluidos puros y pseudopuros (CSV) | `'R1234ze(E),CarbonDioxide,...'` (136 fluidos) |
| `'incompressible_list_pure'` | fluidos incompresibles puros (CSV) | `'TY24,AS55,NBS,...'` |
| `'predefined_mixtures'` | mezclas `.MIX` predefinidas (CSV) | `'AIR.MIX,AMARILLO.MIX,...'` |
| `'parameter_list'` | claves de propiedad reconocidas (CSV) | `'A,ACENTRIC,ALPHA0,...'` |
| `'REFPROP_version'` | versión de REFPROP, o `'n/a'` si no está | `'n/a'` |

## Parámetros en detalle

### `param` — qué metadato global pedir

String con la clave del metadato (ver tabla anterior). Es **sensible a mayúsculas**; un valor no reconocido lanza error (ver más abajo).

## Casos de uso

### Versión y revisión de la biblioteca

```python
import CoolProp.CoolProp as CP

CP.get_global_param_string('version')      # -> '8.0.0'
CP.get_global_param_string('gitrevision')  # -> 'ae81610e7d23efc57f9d051c8e70a4d66e87537f'
```

### Verificar si un fluido existe

CoolProp **no tiene `has_fluid`**. El idioma canónico es buscar el nombre en la lista de fluidos partida por comas:

```python
import CoolProp.CoolProp as CP

fluidos = CP.get_global_param_string('fluids_list').split(',')

'Water' in fluidos   # -> True
'Agua' in fluidos    # -> False  (CoolProp usa nombres en inglés)
len(fluidos)         # -> 136
```

> [!tip] Útil antes de un bucle
> Validar el nombre del fluido con este idioma evita el error `... is not a fluid` a mitad de un cálculo largo. Recuerda que los nombres son en inglés y sensibles a mayúsculas (`'Water'`, no `'water'` ni `'Agua'`); para conocer los alias aceptados de un fluido usa [[CoolProp.get_fluid_param_string|get_fluid_param_string]] con `'aliases'`.

### Inventario de mezclas e incompresibles

```python
import CoolProp.CoolProp as CP

CP.get_global_param_string('predefined_mixtures').split(',')[:3]
# -> ['AIR.MIX', 'AMARILLO.MIX', 'Air.mix']

CP.get_global_param_string('REFPROP_version')
# -> 'n/a'   (REFPROP no instalado en este sistema)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: Input parameter [nope] is invalid` | clave de metadato no reconocida | usar una de las claves válidas de la tabla |
| el `in` siempre da `False` | se olvidó el `.split(',')` y se busca dentro de una sola cadena gigante | dividir primero: `.split(',')` |
| `'water' not in fluids` | nombre en minúscula o en español | los nombres son en inglés y sensibles a mayúsculas (`'Water'`) |

## Limitaciones

- Devuelve **metadata de la biblioteca**, no propiedades de fluidos: para eso usa [[CoolProp.PropsSI|PropsSI]] (numéricas) o [[CoolProp.get_fluid_param_string|get_fluid_param_string]] (textuales).
- Para datos de un parámetro por su índice entero, usa [[CoolProp.get_parameter_information|get_parameter_information]].

## Notas relacionadas

- [[CoolProp.get_fluid_param_string]] — metadata textual de UN fluido
- [[CoolProp.get_parameter_information]] — info de un parámetro por su índice
- [[CoolProp.PropsSI]]
- [[Constants]]
