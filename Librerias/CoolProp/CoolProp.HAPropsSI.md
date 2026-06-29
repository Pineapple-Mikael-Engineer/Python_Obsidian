---
title: CoolProp.HAPropsSI — propiedades del aire húmedo
aliases:
  - HAPropsSI
  - aire húmedo
  - psicrometría
tags: [coolprop, api/funcion, aire_humedo]
lib: coolprop
mod: CoolProp
tipo: funcion
retorna: float
muta_estado: false
draft: false
---

# CoolProp.HAPropsSI — propiedades del aire húmedo

Calcula propiedades del **aire húmedo** (mezcla de aire seco + vapor de agua): entalpía, punto de rocío, temperatura de bulbo húmedo, relación de humedad, etc. Es la herramienta de **psicrometría** de CoolProp y la prima de [[CoolProp.PropsSI|PropsSI]], pero con una diferencia esencial: el aire húmedo es una mezcla cuyo estado **requiere TRES propiedades independientes** (no dos), porque hay que fijar también cuánta agua contiene la mezcla.

## Firma de la función

```python
HAPropsSI(
    Output: str,
    In1Name: str, In1Val: float,
    In2Name: str, In2Val: float,
    In3Name: str, In3Val: float,
) -> float
```

Tres pares `Nombre, Valor`: típicamente uno fija la temperatura, otro la presión y el tercero el contenido de agua (`'R'`, `'W'`, `'Tdp'`...).

## Valor de retorno

Devuelve un `float` con la propiedad pedida, **en unidades SI** y referida a **un kilogramo de aire SECO** en las propiedades extensivas (entalpía, volumen, entropía).

| Output | Propiedad | Unidad |
|--------|-----------|--------|
| `'H'` o `'Hda'` | entalpía por kg de aire seco | J/kg |
| `'S'` o `'Sda'` | entropía por kg de aire seco | J/(kg·K) |
| `'V'` o `'Vda'` | volumen por kg de aire seco | m³/kg |
| `'W'` | relación de humedad (kg agua / kg aire seco) | - |
| `'R'` | humedad relativa | fracción 0–1 |
| `'Tdp'` | temperatura de punto de rocío | K |
| `'Twb'` | temperatura de bulbo húmedo | K |
| `'cp'` | calor específico de la mezcla | J/(kg·K) |

> [!warning] La entalpía es por kg de aire SECO, no por kg de mezcla
> Como la cantidad de vapor varía, todas las propiedades extensivas (`H`, `S`, `V`) se refieren a la masa de aire seco, que sí se conserva en un proceso psicrométrico. Por eso `'V'` (alias `'Vda'`) suele ser > 0.8 m³/kg.

## Parámetros en detalle

### `Output` — propiedad a calcular

String con la clave de la propiedad de salida (ver tabla anterior). A diferencia de [[CoolProp.PropsSI|PropsSI]], las claves de aire húmedo son **propias de HAPropsSI** y en buena parte van en minúscula o con sufijo `da` ("dry air").

### `In1Name`...`In3Name` — las TRES variables de entrada

El aire húmedo necesita tres entradas independientes. Las combinaciones habituales:

| Trío de entrada | Uso típico |
|-----------------|------------|
| `'T'`, `'P'`, `'R'` | dato de termómetro + barómetro + higrómetro (lo más común) |
| `'T'`, `'P'`, `'W'` | se conoce la relación de humedad (kg agua/kg aire seco) |
| `'T'`, `'P'`, `'Tdp'` | se mide el punto de rocío |
| `'T'`, `'P'`, `'Twb'` | se mide con psicrómetro (bulbo húmedo) |

Claves de entrada/salida: `'T'` (temperatura, K), `'P'` (presión, Pa), `'R'` (humedad relativa, **fracción 0–1**), `'W'` (relación de humedad, kg/kg), `'Tdp'` (rocío, K), `'Twb'` (bulbo húmedo, K).

### `In1Val`...`In3Val` — los valores en SI

`float`, en unidades SI estrictas: temperaturas en **K** (convierte desde °C con `T = 25 + 273.15`), presión en **Pa** (1 atm = 101325 Pa) y la humedad relativa como **fracción** (50 % → `0.5`).

## Casos de uso

### Entalpía de aire a 25 °C, 1 atm y 50 % HR

```python
import CoolProp.CoolProp as CP

T = 25 + 273.15          # 298.15 K
h = CP.HAPropsSI('H', 'T', T, 'P', 101325, 'R', 0.5)
# -> 50423.45 J/kg de aire seco
```

### Punto de rocío y bulbo húmedo (psicrometría básica)

```python
import CoolProp.CoolProp as CP

T, P, RH = 298.15, 101325, 0.5
Tdp = CP.HAPropsSI('Tdp', 'T', T, 'P', P, 'R', RH)  # -> 287.02 K  (13.87 °C)
Twb = CP.HAPropsSI('Twb', 'T', T, 'P', P, 'R', RH)  # -> 291.03 K  (17.88 °C)
W   = CP.HAPropsSI('W',   'T', T, 'P', P, 'R', RH)  # -> 0.009926 kg agua/kg aire seco
V   = CP.HAPropsSI('V',   'T', T, 'P', P, 'R', RH)  # -> 0.85779 m^3/kg aire seco
```

### De la relación de humedad a la humedad relativa

```python
import CoolProp.CoolProp as CP

# Si conozco W (kg agua/kg aire seco) en vez de la HR
RH = CP.HAPropsSI('R', 'T', 298.15, 'P', 101325, 'W', 0.01)
# -> 0.50368  (50.4 %)
```

### Calor sensible para calentar aire (a W constante)

```python
import CoolProp.CoolProp as CP

P = 101325
W = 0.008  # kg agua/kg aire seco fijo (calentamiento sensible)
h1 = CP.HAPropsSI('H', 'T', 20 + 273.15, 'P', P, 'W', W)
h2 = CP.HAPropsSI('H', 'T', 40 + 273.15, 'P', P, 'W', W)
q = h2 - h1   # J por kg de aire seco
# -> ~20431 J/kg de aire seco
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError: HAPropsSI(): incompatible function arguments` | se pasaron solo DOS entradas (como en PropsSI) | el aire húmedo necesita **tres** pares `Nombre,Valor` |
| Humedad absurda / fuera de rango | se pasó la HR como porcentaje (`50`) en vez de fracción (`0.5`) | `'R'` va de 0 a 1 |
| Resultados raros en entalpía | se interpretó `H` como "por kg de mezcla" | `H`, `S`, `V` son **por kg de aire seco** |
| Valor incoherente con °C | se pasó la temperatura en °C | convertir a K (`T + 273.15`) |

## Limitaciones

- Solo modela **aire húmedo**; para cualquier otro fluido puro o mezcla usa [[CoolProp.PropsSI|PropsSI]] o [[AbstractState]].
- Válida en un rango acotado de temperatura, presión y humedad (en torno a condiciones atmosféricas y de climatización); fuera de él puede no converger.
- Es independiente del backend `BACKEND::Fluido` de los fluidos puros: el modelo de aire húmedo es interno.

## Notas relacionadas

- [[CoolProp.PropsSI]] — propiedades de fluidos puros (dos entradas)
- [[concepto_propiedades_SI]]
- [[concepto_estado_termodinamico]]
- [[Constants]]
