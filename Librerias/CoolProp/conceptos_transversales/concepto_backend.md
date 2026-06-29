---
title: Backend — el motor de cálculo intercambiable
aliases:
  - backend
  - motor de calculo
  - BACKEND::Fluido
tags:
  - coolprop
  - concepto
  - backend
lib: coolprop
tipo: concepto
draft: false
---

# Backend — el motor de cálculo intercambiable

## Definicion

El **backend** es el modelo matemático con el que CoolProp calcula las propiedades de un fluido. CoolProp separa dos cosas que es fácil confundir: *qué propiedad quieres* (densidad, entalpía...) y *con qué modelo se calcula* (ecuación de Helmholtz, formulación industrial del agua, ecuación cúbica...). El backend es esa segunda parte, y es **intercambiable** sin tocar el resto del código.

## Por que existe

No hay un único modelo «mejor» para todos los casos: el más preciso (Helmholtz multiparamétrico) es también más lento, y para agua/vapor la industria usa una formulación propia (IF97) que es estándar en calderas y turbinas. Separar el motor del cálculo permite **elegir el compromiso precisión/velocidad/cobertura** que necesitas escribiendo solo un prefijo, sin reescribir nada. Si CoolProp obligara a un único modelo, o sería lento para todos o impreciso para muchos.

## La regla central

> [!regla] La sintaxis es BACKEND::Fluido
> El backend se antepone al nombre del fluido con `::`. `'HEOS::Water'`, `'IF97::Water'`, `'REFPROP::R134a'`. Si **omites** el prefijo, CoolProp usa **`HEOS`** por defecto: `'Water'` equivale a `'HEOS::Water'`.

| Backend | Modelo | Cuándo usarlo |
|---------|--------|---------------|
| `HEOS` | Helmholtz multiparamétrico | **Por defecto.** El más general y preciso; cubre casi todos los fluidos y mezclas |
| `IF97` | Formulación industrial IAPWS-IF97 (agua/vapor) | Agua y vapor: rápido y es el **estándar industrial** de calderas y turbinas |
| `REFPROP` | Modelos NIST REFPROP | Máxima precisión de referencia; **requiere licencia** e instalación aparte |
| `SRK` / `PR` | Ecuaciones cúbicas (Soave-Redlich-Kwong / Peng-Robinson) | Rápidas y ligeras; menos precisas, útiles para gases e hidrocarburos |
| `INCOMP` | Fluidos incompresibles | Líquidos y soluciones tratados como incompresibles (aceites térmicos, salmueras) |
| `BICUBIC&HEOS` | Interpolación bicúbica sobre tablas HEOS | Misma física que HEOS pero **mucho más rápido** vía tablas precalculadas |

## Nivel 1 — el prefijo en PropsSI

```python
from CoolProp.CoolProp import PropsSI

# Sin prefijo: backend por defecto HEOS
D_def = PropsSI('D', 'T', 373.15, 'P', 101325, 'Water')        # -> 0.597612 kg/m3

# Explicito: identico a lo anterior
D_heos = PropsSI('D', 'T', 373.15, 'P', 101325, 'HEOS::Water')  # -> 0.597612 kg/m3

# IF97: formulacion industrial del agua (valor casi igual, calculo mas rapido)
D_if97 = PropsSI('D', 'T', 373.15, 'P', 101325, 'IF97::Water')  # -> 0.597579 kg/m3
```

`HEOS` e `IF97` coinciden hasta la cuarta cifra: misma física, distinto compromiso de velocidad.

## Nivel 2 — el mismo cálculo con una ecuación cúbica

```python
from CoolProp.CoolProp import PropsSI

# HEOS (referencia) frente a cubicas, mismo estado de agua liquida a 1 atm, 25 C
D_heos = PropsSI('D', 'T', 373.15, 'P', 101325, 'Water')      # -> 0.597612 kg/m3
D_srk  = PropsSI('D', 'T', 373.15, 'P', 101325, 'SRK::Water')  # -> 710.31 kg/m3 (impreciso aqui)
D_pr   = PropsSI('D', 'T', 373.15, 'P', 101325, 'PR::Water')   # -> 800.61 kg/m3 (impreciso aqui)
```

Las cúbicas son rápidas y baratas pero pierden precisión cerca de líquido y saturación: aquí dan densidades muy distintas a la referencia. Para agua, usa `HEOS` o `IF97`.

## Nivel 3 — el backend como primer argumento de AbstractState

```python
import CoolProp.CoolProp as CP

# En la API de bajo nivel el backend es el 1er argumento del constructor
state = CP.AbstractState('IF97', 'Water')      # backend IF97 explicito
state.update(CP.PT_INPUTS, 101325, 373.15)
D = state.rhomass()                            # -> 0.597579 kg/m3
```

En [[AbstractState]] el backend no va pegado al fluido sino como argumento propio: `AbstractState(backend, fluido)`.

## Casos que fallan

| Intento | Qué ocurre |
|---------|-----------|
| `'REFPROP::Water'` sin REFPROP instalado | Error de carga de librería: REFPROP es comercial y se instala aparte de CoolProp |
| Backend que no soporta el fluido | `No backend could be obtained` o resultados sin sentido (p. ej. `IF97` solo entiende agua) |
| Usar cúbicas (`SRK`/`PR`) cerca de líquido/saturación esperando precisión | Convergen pero con error grande; son para gases e hidrocarburos, no para agua densa |

```python
import CoolProp.CoolProp as CP

# Comprobar si REFPROP esta disponible ANTES de pedirlo
ver = CP.get_global_param_string('REFPROP_version')
print(ver)   # -> 'n/a' si REFPROP no esta instalado; una version (p.ej. '10.0') si si
```

> [!tip] Verifica REFPROP antes de usarlo
> `get_global_param_string('REFPROP_version')` devuelve `'n/a'` cuando REFPROP no está instalado. Compruébalo antes de pasar el prefijo `'REFPROP::'` para evitar un error de carga en tiempo de ejecución.

## Relacion con otros conceptos

- [[concepto_estado_termodinamico]] — el backend resuelve la ecuación de estado a partir del par de propiedades
- [[concepto_propiedades_SI]] — sea cual sea el backend, la entrada y la salida van en SI
- [[CoolProp.PropsSI]] — recibe el backend como prefijo del fluido (`'IF97::Water'`)
- [[AbstractState]] — recibe el backend como primer argumento del constructor
- [[CoolProp/backends/index|backends]] — fichas detalladas de cada motor
