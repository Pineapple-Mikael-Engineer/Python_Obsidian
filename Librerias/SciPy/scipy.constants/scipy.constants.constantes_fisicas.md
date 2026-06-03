---
title: scipy.constants — constantes fisicas y matematicas listas para usar
aliases:
  - scipy.constants
  - constantes fisicas
  - physical_constants
  - CODATA scipy
tags:
  - scipy
  - api/submodulo
  - constantes
lib: scipy
tipo: submodulo
mod: scipy.constants
requiere:
  - numpy
draft: false
---

# scipy.constants — constantes fisicas y matematicas listas para usar

Submodulo que expone **constantes fisicas, matematicas y factores de conversion** ya tabulados, para no teclearlos a mano ni arrastrar errores de transcripcion. Tres niveles de acceso: (1) **atributos directos** del modulo (`scipy.constants.c`, `G`, `h`, ...) que devuelven un `float` listo para operar; (2) el **diccionario** `physical_constants[clave]` que devuelve la **tupla** `(valor, unidad, incertidumbre)` segun **CODATA**; (3) **prefijos SI** y **factores de conversion** (`kilo`, `atm`, `g`, `hour`, ...) como floats. Los valores fisicos siguen el ajuste CODATA empotrado en la version de SciPy instalada.

> Distincion clave: el **atributo** (`constants.c`) da solo el numero; la **clave de diccionario** (`physical_constants['speed of light in vacuum']`) da `(valor, unidad, incertidumbre)`. Usa atributos para calcular, el diccionario cuando necesitas tambien la unidad o el error. Para descubrir el nombre exacto de una clave se usa [[scipy.constants.find_unit]].

## Acceso: tres vias

| Via | Forma | Devuelve |
|-----|-------|----------|
| Atributo directo | `scipy.constants.c` | `float` |
| Diccionario CODATA | `scipy.constants.physical_constants['elementary charge']` | `tuple (valor, unidad, incertidumbre)` |
| Extractores por campo | `value(key)`, `unit(key)`, `precision(key)` | `float`, `str`, `float` |

```python
import scipy.constants as const

const.c                              # → 299792458.0   (m/s, atributo float)
const.physical_constants['speed of light in vacuum']
# → (299792458.0, 'm s^-1', 0.0)    (valor, unidad, incertidumbre)
```

## Constantes como atributos directos

Constantes fisicas y matematicas accesibles como `scipy.constants.<nombre>` (un `float` cada una).

| Atributo | Constante | Valor aprox. | Unidad |
|----------|-----------|--------------|--------|
| `c`, `speed_of_light` | Velocidad de la luz | `2.998e8` | m/s |
| `G`, `gravitational_constant` | Gravitacion universal | `6.674e-11` | m^3 kg^-1 s^-2 |
| `g` | Aceleracion gravedad estandar | `9.80665` | m/s^2 |
| `h`, `Planck` | Constante de Planck | `6.626e-34` | J s |
| `hbar` | Planck reducida (h/2pi) | `1.055e-34` | J s |
| `k`, `Boltzmann` | Constante de Boltzmann | `1.381e-23` | J/K |
| `N_A`, `Avogadro` | Numero de Avogadro | `6.022e23` | 1/mol |
| `R`, `gas_constant` | Constante de los gases | `8.3145` | J mol^-1 K^-1 |
| `e`, `elementary_charge` | Carga elemental | `1.602e-19` | C |
| `epsilon_0` | Permitividad del vacio | `8.854e-12` | F/m |
| `mu_0` | Permeabilidad del vacio | `1.257e-6` | N/A^2 |
| `m_e`, `electron_mass` | Masa del electron | `9.109e-31` | kg |
| `m_p`, `proton_mass` | Masa del proton | `1.673e-27` | kg |
| `m_n`, `neutron_mass` | Masa del neutron | `1.675e-27` | kg |
| `sigma`, `Stefan_Boltzmann` | Stefan-Boltzmann | `5.670e-8` | W m^-2 K^-4 |
| `pi` | Numero pi | `3.14159` | adim. |
| `golden`, `golden_ratio` | Razon aurea | `1.61803` | adim. |

```python
# Energia de un foton de 500 nm: E = h c / lambda
E = const.h * const.c / 500e-9
E    # → 3.97e-19 J
```

## Diccionario physical_constants

`physical_constants` mapea **clave (str)** a la tupla `(valor, unidad, incertidumbre_absoluta)`. Es la fuente CODATA cruda; los atributos directos son atajos sobre ella.

```python
const.physical_constants['electron mass']
# → (9.1093837015e-31, 'kg', 2.8e-40)
val, uni, inc = const.physical_constants['electron mass']
val    # → 9.109e-31
uni    # → 'kg'
inc    # → 2.8e-40   (incertidumbre absoluta)
```

## Extractores por campo

En vez de desempaquetar la tupla a mano, tres funciones devuelven un campo concreto de una clave. La `precision(key)` devuelve la **incertidumbre relativa** (incertidumbre / valor), no la absoluta.

| Funcion | Devuelve | Equivale a |
|---------|----------|------------|
| `value(key)` | `float` valor | `physical_constants[key][0]` |
| `unit(key)` | `str` unidad | `physical_constants[key][1]` |
| `precision(key)` | `float` incertidumbre relativa | `inc / valor` |

```python
const.value('proton mass')       # → 1.67262192369e-27
const.unit('proton mass')        # → 'kg'
const.precision('proton mass')   # → 3.1e-10   (relativa, adimensional)
```

## Prefijos SI

Factores multiplicativos como floats. Multiplican una magnitud base por la potencia de 10 correspondiente.

| Atributo | Factor | Atributo | Factor |
|----------|--------|----------|--------|
| `yotta` | `1e24` | `centi` | `1e-2` |
| `peta` | `1e15` | `milli` | `1e-3` |
| `tera` | `1e12` | `micro` | `1e-6` |
| `giga` | `1e9` | `nano` | `1e-9` |
| `mega` | `1e6` | `pico` | `1e-12` |
| `kilo` | `1e3` | `femto` | `1e-15` |

```python
5 * const.mega        # → 5000000.0   (5 MHz en Hz)
200 * const.nano      # → 2e-07       (200 nm en m)
```

## Factores de conversion

Atributos `float` que convierten unidades no-SI a SI (multiplicando) o dan valores de referencia.

| Atributo | Significado | Valor |
|----------|-------------|-------|
| `g` | Gravedad estandar | `9.80665` m/s^2 |
| `atm`, `atmosphere` | Atmosfera estandar | `101325.0` Pa |
| `bar` | bar | `1e5` Pa |
| `mmHg`, `torr` | Milimetro de mercurio | `133.322` Pa |
| `inch` | Pulgada | `0.0254` m |
| `foot` | Pie | `0.3048` m |
| `mile` | Milla | `1609.344` m |
| `lb`, `pound` | Libra masa | `0.4536` kg |
| `hour` | Hora | `3600.0` s |
| `day` | Dia | `86400.0` s |
| `eV`, `electron_volt` | Electronvoltio | `1.602e-19` J |
| `calorie` | Caloria | `4.184` J |

```python
# Presion de 2.5 atm en pascales
p = 2.5 * const.atm
p    # → 253312.5 Pa

# 6 pulgadas en metros
6 * const.inch    # → 0.1524
```

## Caso de uso: ingenieria sin teclear valores

```python
import numpy as np
import scipy.constants as const

# Velocidad eficaz (rms) de moleculas de N2 a 300 K
# v_rms = sqrt(3 k T / m),  m = 28 u
m = 28 * const.value('atomic mass constant')   # masa de N2 en kg
T = 300                                         # K
v_rms = np.sqrt(3 * const.k * T / m)
v_rms    # → ~516 m/s
```

```python
# Ley de gases ideales: presion de 2 mol a 350 K en 0.05 m^3
n, T, V = 2.0, 350.0, 0.05
P = n * const.R * T / V
P    # → ~116403 Pa  (~1.15 atm)
P / const.atm    # → ~1.149
```

## Buenas practicas

1. Importa como `import scipy.constants as const` y usa atributos para calcular: el codigo queda autodocumentado y exacto a CODATA.
2. Usa `physical_constants[key]` o `unit(key)` cuando necesites **verificar la unidad**; evita asumir el SI de memoria.
3. `precision(key)` da incertidumbre **relativa**; para la **absoluta** lee el tercer elemento de la tupla.
4. No mezcles `np.pi` y `const.pi`: son el mismo valor, pero manten una sola fuente por claridad.
5. Para limites de unidades no estandar (atm, eV, inch) multiplica por el factor del modulo en lugar de codificar el numero.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `KeyError` en `physical_constants` | Clave inexacta o mal escrita | Buscar la clave con `find('...')` antes |
| Confundir `g` gravedad con `const.e` | Nombres cortos colisionan con variables locales | Acceder via el namespace: `const.g`, `const.e` |
| Tomar `precision` como incertidumbre absoluta | `precision(key)` es relativa | Usar `physical_constants[key][2]` para la absoluta |
| Atributo inexistente | No toda constante tiene atajo directo | Usar la clave de diccionario o `value(key)` |

## Notas relacionadas

- [[scipy.constants.find_unit]]
- [[scipy.integrate.quad]]
