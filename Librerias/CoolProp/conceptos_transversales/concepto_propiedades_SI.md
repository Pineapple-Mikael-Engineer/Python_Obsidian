---
title: Propiedades y unidades SI — claves de entrada y salida
aliases:
  - propiedades SI
  - claves de propiedad
  - unidades CoolProp
tags:
  - coolprop
  - concepto
  - propiedades
lib: coolprop
tipo: concepto
draft: false
---

# Propiedades y unidades SI — claves de entrada y salida

## Definicion

En CoolProp cada propiedad termodinámica o de transporte se identifica con una **clave string** (`'T'`, `'P'`, `'D'`, `'H'`...) y CoolProp trabaja **siempre en SI estricto**: presión en pascales, temperatura en kelvin, energías en joule por kilogramo. La misma clave sirve para pedir una propiedad de salida y para nombrar una propiedad de entrada del estado.

## Por que existe

El sufijo `SI` de [[CoolProp.PropsSI]] no es decorativo: garantiza que **todo** entra y sale en el Sistema Internacional, sin factores de conversión ocultos ni ambigüedad de unidades. Un único sistema coherente elimina la fuente de error más típica en termodinámica computacional (mezclar bar con Pa, °C con K, kJ con J). El precio es que **tú** debes convertir tus datos a SI antes de pasarlos.

## La regla central

> [!regla] Todo en SI, siempre
> Pa (no bar), K (no °C), J/kg (no kJ/kg). Conversiones obligatorias: `T_K = T_C + 273.15` y `P_Pa = bar * 1e5`. Si tus datos vienen en °C o bar, conviértelos **antes** de llamar a CoolProp.

Claves de propiedad para [[CoolProp.PropsSI]] y [[AbstractState]]:

| Clave | Propiedad | Unidad SI |
|-------|-----------|-----------|
| `'T'` | Temperatura | K |
| `'P'` | Presión | Pa |
| `'D'` | Densidad | kg/m³ |
| `'H'` | Entalpía específica (= `Hmass`) | J/kg |
| `'S'` | Entropía específica (= `Smass`) | J/(kg·K) |
| `'U'` | Energía interna específica | J/kg |
| `'Q'` | Calidad de vapor (0 = líquido sat., 1 = vapor sat.) | adimensional |
| `'C'` | Cp, calor específico a presión constante (= `Cpmass`) | J/(kg·K) |
| `'O'` | Cv, calor específico a volumen constante (= `Cvmass`) | J/(kg·K) |
| `'V'` | Viscosidad dinámica | Pa·s |
| `'L'` | Conductividad térmica | W/(m·K) |
| `'A'` | Velocidad del sonido | m/s |
| `'Z'` | Factor de compresibilidad | adimensional |
| `'Prandtl'` | Número de Prandtl | adimensional |

### Másico vs molar

Casi todas las claves de energía y capacidad tienen variante **másica** (por kg) y **molar** (por mol). `'H'` es atajo de `'Hmass'`; existe también `'Hmolar'` (J/mol). Análogamente `Smass`/`Smolar`, `Cpmass`/`Cpmolar`, `Dmass`/`Dmolar`. **No las confundas**: difieren en el factor de la masa molar `M`.

### Propiedades "triviales"

Las constantes del fluido (no dependen del estado) se llaman **triviales** y se piden con una forma corta de dos argumentos `PropsSI('<clave>', '<fluido>')`:

| Clave | Significado | Unidad |
|-------|-------------|--------|
| `'Tcrit'` | Temperatura crítica | K |
| `'pcrit'` | Presión crítica | Pa |
| `'Tmin'` | Temperatura mínima válida | K |
| `'M'` (= `molar_mass`) | Masa molar | kg/mol |

## Nivel 1 — pedir varias propiedades de un mismo estado

```python
from CoolProp.CoolProp import PropsSI

# Agua liquida a 25 C (298.15 K) y 1 atm (101325 Pa)
Cp = PropsSI('C', 'T', 298.15, 'P', 101325, 'Water')        # -> 4181.31 J/(kg K)
mu = PropsSI('V', 'T', 298.15, 'P', 101325, 'Water')        # viscosidad -> 8.900e-4 Pa s
k  = PropsSI('L', 'T', 298.15, 'P', 101325, 'Water')        # conductividad -> 0.6065 W/(m K)
a  = PropsSI('A', 'T', 298.15, 'P', 101325, 'Water')        # vel. del sonido -> 1496.7 m/s
Pr = PropsSI('Prandtl', 'T', 298.15, 'P', 101325, 'Water')  # -> 6.136 (adimensional)
```

## Nivel 2 — convertir desde °C y bar antes de llamar

```python
from CoolProp.CoolProp import PropsSI

# Datos en unidades de ingenieria: 25 C y 1 bar
T_C, P_bar = 25.0, 1.0

T = T_C + 273.15   # -> 298.15 K
P = P_bar * 1e5    # -> 100000 Pa

D = PropsSI('D', 'T', T, 'P', P, 'Water')  # -> 997.05 kg/m3
```

## Nivel 3 — másico vs molar y propiedades triviales

```python
from CoolProp.CoolProp import PropsSI

# Misma entalpia, dos bases distintas
h_mass  = PropsSI('Hmass',  'T', 298.15, 'P', 101325, 'Water')  # -> 104920.1 J/kg
h_molar = PropsSI('Hmolar', 'T', 298.15, 'P', 101325, 'Water')  # -> 1890.16 J/mol

# Propiedades triviales: forma corta de 2 argumentos
Tcrit = PropsSI('Tcrit', 'Water')   # -> 647.096 K
pcrit = PropsSI('pcrit', 'Water')   # -> 22.064e6 Pa
M     = PropsSI('M', 'Water')       # masa molar -> 0.018015 kg/mol

# Las dos bases se relacionan por la masa molar:  h_molar ~= h_mass * M
print(h_mass * M)                   # -> 1890.16 J/mol  (coincide con h_molar)
```

## Casos que fallan

| Intento | Qué ocurre |
|---------|-----------|
| Pasar `25` por temperatura (creyendo °C) | CoolProp lo interpreta como **25 K** (cerca del cero absoluto): estado inválido o disparate físico |
| Pasar `1` por presión (creyendo bar) | Lo interpreta como **1 Pa** (vacío casi total), no como 1 bar |
| Mezclar `'H'` (J/kg) con un valor en kJ/kg | Error de tres órdenes de magnitud silencioso; el resultado no avisa |
| Confundir `'Hmass'` con `'Hmolar'` | Difieren en el factor `M`; un balance de energía sale mal por completo |

```python
from CoolProp.CoolProp import PropsSI

# MAL: 25 se interpreta como 25 K, no como 25 C
# PropsSI('D', 'T', 25, 'P', 101325, 'Water')   # estado invalido o sin sentido

# BIEN: convertir a kelvin primero
D = PropsSI('D', 'T', 25 + 273.15, 'P', 101325, 'Water')  # -> 997.05 kg/m3
```

## Relacion con otros conceptos

- [[concepto_estado_termodinamico]] — estas claves son las que forman el par que define el estado
- [[concepto_backend]] — el backend produce estos valores; la convención SI no cambia con él
- [[Constants]] — los pares de entrada (`PT_INPUTS`, `PQ_INPUTS`...) y los índices de propiedad para [[AbstractState]]
- [[CoolProp.PropsSI]] — usa estas claves como `output`, `input1` e `input2`
