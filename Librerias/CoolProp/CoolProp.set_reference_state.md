---
title: CoolProp.set_reference_state — fijar el cero de entalpía y entropía
aliases:
  - set_reference_state
  - estado de referencia
  - IIR ASHRAE NBP
tags: [coolprop, api/funcion, referencia]
lib: coolprop
mod: CoolProp
tipo: funcion
retorna: None
muta_estado: true
draft: false
---

# CoolProp.set_reference_state — fijar el cero de entalpía y entropía

Fija **dónde valen cero la entalpía y la entropía** de un fluido. La entalpía y la entropía absolutas no tienen un cero físico universal: cada convención (IIR, ASHRAE, NBP...) lo pone en un punto distinto. Esta función elige esa convención. Afecta a los **valores absolutos** de `H` y `S`, no a sus **diferencias** (un salto de entalpía en un ciclo es el mismo en cualquier referencia).

> [!warning] Efecto global y con estado: muta_estado
> Es un **ajuste global** con efecto colateral: cambia los resultados de `H` y `S` de [[CoolProp.PropsSI|PropsSI]] y [[AbstractState]] para ese fluido **en todo el programa**, desde la llamada en adelante. Por eso lleva `muta_estado: true`. Vuelve a `'DEF'` cuando termines para no contaminar otros cálculos.

## Firma de la función

```python
set_reference_state(Fluid: str, ReferenceState: str) -> None
```

## Valor de retorno

`None`. No devuelve nada: su efecto es el cambio de estado global de la referencia del fluido.

## Parámetros en detalle

### `Fluid` — el fluido afectado

String con el nombre del fluido. La referencia se cambia **solo para ese fluido**.

### `ReferenceState` — la convención de cero

String con una de las referencias estándar:

| Valor | Convención | Dónde pone los ceros |
|-------|-----------|----------------------|
| `'IIR'` | International Institute of Refrigeration | `h = 200 kJ/kg`, `s = 1 kJ/(kg·K)` en líquido saturado a 0 °C |
| `'ASHRAE'` | ASHRAE | `h = 0`, `s = 0` en líquido saturado a −40 °C |
| `'NBP'` | Normal Boiling Point | `h = 0`, `s = 0` en el punto de ebullición normal (a 1 atm) |
| `'DEF'` | por defecto del backend | la que trae el backend para ese fluido |

## Casos de uso

### Comparar la entalpía absoluta con distintas referencias

```python
import CoolProp.CoolProp as CP

# Por defecto del backend (DEF)
h_def = CP.PropsSI('H', 'T', 273.15, 'Q', 0, 'Ammonia')
# -> 345674.94 J/kg  (líquido saturado a 0 °C)

# Convención IIR: h = 200 kJ/kg en ese mismo punto
CP.set_reference_state('Ammonia', 'IIR')
h_iir = CP.PropsSI('H', 'T', 273.15, 'Q', 0, 'Ammonia')
s_iir = CP.PropsSI('S', 'T', 273.15, 'Q', 0, 'Ammonia')
# h_iir -> 200000.0 J/kg ; s_iir -> 1000.0 J/(kg·K)

# IMPORTANTE: volver a la referencia por defecto
CP.set_reference_state('Ammonia', 'DEF')
```

### Las referencias ASHRAE y NBP

```python
import CoolProp.CoolProp as CP

CP.set_reference_state('Ammonia', 'ASHRAE')
h_ash = CP.PropsSI('H', 'T', 233.15, 'Q', 0, 'Ammonia')  # -> ~0 J/kg  (líq. sat. a -40 °C)

CP.set_reference_state('Ammonia', 'NBP')
Tnbp = CP.PropsSI('T', 'P', 101325, 'Q', 0, 'Ammonia')   # -> 239.83 K  (ebullición a 1 atm)
h_nbp = CP.PropsSI('H', 'P', 101325, 'Q', 0, 'Ammonia')  # -> ~0 J/kg  (cero en ese punto)

CP.set_reference_state('Ammonia', 'DEF')  # restaurar siempre
```

> [!tip] Las DIFERENCIAS no cambian
> Aunque `h` absoluta cambie con la referencia, un salto `h2 - h1` dentro de un mismo fluido es **idéntico** en cualquier convención. La referencia solo importa al comparar valores absolutos o tablas de distintas fuentes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: Reference state string is invalid: [XXX]` | referencia no reconocida | usar `'IIR'`, `'ASHRAE'`, `'NBP'` o `'DEF'` |
| `Cannot use IIR reference state; Ttriple [...] is greater than 273.15 K` | la referencia (p. ej. IIR a 0 °C) cae fuera del rango del fluido (el agua tiene punto triple a 273.16 K) | usar una referencia válida para ese fluido (`'NBP'`, `'DEF'`) |
| resultados de H/S "cambiados" en otra parte del programa | la referencia quedó alterada globalmente | restaurar con `set_reference_state(fluido, 'DEF')` |
| comparar tablas de distintas fuentes y no cuadran | cada fuente usa otra referencia | fijar la misma referencia (`'IIR'`/`'ASHRAE'`) en ambos lados |

## Limitaciones

- Afecta al **estado global** del programa para ese fluido; no es un cálculo local. Convive mal con código concurrente o con librerías de terceros que asuman la referencia por defecto.
- No todos los fluidos admiten todas las referencias (p. ej. el agua no admite `'IIR'` por su punto triple).
- No cambia propiedades que no dependen del cero de H/S (densidad, presión, etc.).

## Notas relacionadas

- [[CoolProp.PropsSI]] — los valores de H y S que esta función desplaza
- [[AbstractState]] — también afectado por la referencia global
- [[concepto_propiedades_SI]]
- [[concepto_estado_termodinamico]]
