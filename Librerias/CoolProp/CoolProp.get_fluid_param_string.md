---
title: CoolProp.get_fluid_param_string — metadata textual de un fluido
aliases:
  - get_fluid_param_string
  - CAS de un fluido
  - alias de un fluido
tags: [coolprop, api/funcion, metadata]
lib: coolprop
mod: CoolProp
tipo: funcion
retorna: str
muta_estado: false
draft: false
---

# CoolProp.get_fluid_param_string — metadata textual de un fluido

Devuelve metadata **textual** de un fluido concreto: su número CAS, sus alias, la fórmula química, la clasificación de seguridad ASHRAE o las referencias bibliográficas. Es para datos de **catálogo** (cadenas de texto), no para propiedades numéricas: esas se piden a [[CoolProp.PropsSI|PropsSI]].

## Firma de la función

```python
get_fluid_param_string(Fluid: str, Param: str) -> str
```

## Valor de retorno

Un `str` con el dato pedido del fluido.

| `Param` | Qué devuelve | Ejemplo (`'Water'`) |
|---------|--------------|---------------------|
| `'CAS'` | número de registro CAS | `'7732-18-5'` |
| `'aliases'` | otros nombres aceptados (CSV) | `'water,WATER,H2O,h2o,R718'` |
| `'formula'` | fórmula química | `'H_{2}O_{1}'` |
| `'ASHRAE34'` | clasificación de seguridad ASHRAE 34 | (R134a → `'A1'`) |
| `'BibTeX-EOS'` | clave BibTeX de la ecuación de estado | (cadena de referencia) |
| `'BibTeX-CP0'` | clave BibTeX del calor específico ideal | (cadena de referencia) |

## Parámetros en detalle

### `Fluid` — el fluido

String con el nombre del fluido (en inglés, sensible a mayúsculas). Para validar que existe, ver [[CoolProp.get_global_param_string|get_global_param_string]] con `'fluids_list'`.

### `Param` — qué metadato textual pedir

String con la clave del metadato (ver tabla). Debe ser una propiedad **textual**; pasar aquí una propiedad numérica lanza error (ver más abajo).

## Casos de uso

### Identificar un fluido (CAS, fórmula, alias)

```python
import CoolProp.CoolProp as CP

CP.get_fluid_param_string('Water', 'CAS')      # -> '7732-18-5'
CP.get_fluid_param_string('Water', 'formula')  # -> 'H_{2}O_{1}'
CP.get_fluid_param_string('Water', 'aliases')  # -> 'water,WATER,H2O,h2o,R718'
```

### Clasificación de seguridad de un refrigerante

```python
import CoolProp.CoolProp as CP

CP.get_fluid_param_string('R134a', 'ASHRAE34')  # -> 'A1'  (baja toxicidad, no inflamable)
CP.get_fluid_param_string('R134a', 'CAS')       # -> '811-97-2'
```

### Para propiedades NUMÉRICAS, NO uses esta función

Temperatura/presión críticas, masa molar, punto triple... **no** son metadata textual: se piden a [[CoolProp.PropsSI|PropsSI]] como salidas "triviales" (las que no necesitan fijar dos variables de estado):

```python
import CoolProp.CoolProp as CP

CP.PropsSI('Tcrit', 'Water')    # -> 647.096 K
CP.PropsSI('pcrit', 'Water')    # -> 22063999.99... Pa  (~22.06 MPa)
CP.PropsSI('M', 'Water')        # -> 0.018015268 kg/mol  (masa molar)
CP.PropsSI('Ttriple', 'Water')  # -> 273.16 K
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: fluid parameter [Tcrit] is invalid` | se pidió una propiedad numérica (Tcrit, M, pcrit...) aquí | pedirla a [[CoolProp.PropsSI|PropsSI]] (`PropsSI('Tcrit','Water')`) |
| fluido no encontrado | nombre mal escrito o en español | validar con `'fluids_list'` de [[CoolProp.get_global_param_string|get_global_param_string]] |
| clave de metadato desconocida | `Param` no es una de las textuales | usar `'CAS'`, `'aliases'`, `'formula'`, `'ASHRAE34'`, `'BibTeX-*'` |

## Limitaciones

- Solo devuelve **texto**; toda propiedad numérica del fluido va por [[CoolProp.PropsSI|PropsSI]].
- Las referencias `BibTeX-*` son claves/cadenas bibliográficas, no DOIs ni texto formateado.

## Notas relacionadas

- [[CoolProp.get_global_param_string]] — metadata global (lista de fluidos, versión)
- [[CoolProp.PropsSI]] — propiedades numéricas, incluidas las "triviales" (Tcrit, M...)
- [[CoolProp.get_parameter_information]]
- [[Constants]]
