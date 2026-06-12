---
title: scipy.constants — constantes fisicas y matematicas
tags: [scipy, indice]
draft: false
---

# scipy.constants — constantes fisicas y matematicas

`scipy.constants` es el submodulo de **constantes fisicas, matematicas y factores de conversion** ya tabulados, para no teclearlos a mano ni arrastrar errores de transcripcion. Reune la velocidad de la luz `c`, la constante de gravitacion `G`, la de Planck `h`, la de Boltzmann `k`, `pi`, el numero de Avogadro, los prefijos SI (`kilo`, `mega`, `nano`...) y decenas de conversiones de unidades (`atm`, `hour`, `g`, `mile`...). Los valores fisicos siguen el ajuste **CODATA** empotrado en la version de SciPy instalada, asi que son los oficiales y reproducibles.

## En accion

```python
import numpy as np
import scipy.constants as const

# 1. Constantes como atributos directos (un float listo para operar)
const.c        # → 299792458.0      velocidad de la luz (m/s)
const.G        # → 6.674e-11        gravitacion universal (m^3 kg^-1 s^-2)
const.g        # → 9.80665          gravedad estandar (m/s^2)
const.h        # → 6.626e-34        constante de Planck (J s)
const.k        # → 1.381e-23        constante de Boltzmann (J/K)
const.pi       # → 3.141592653589793

# 2. Calcular con ellas: energia de un foton de 500 nm  (E = h c / lambda)
E = const.h * const.c / 500e-9            # → 3.97e-19 J

# 3. Convertir unidades multiplicando por el factor a SI
p = 2.5 * const.atm                       # 2.5 atm → 253312.5 Pa
d = 6 * const.inch                        # 6 pulgadas → 0.1524 m
t = 3 * const.hour                        # 3 horas → 10800.0 s

# 4. Diccionario CODATA: tambien la unidad y la incertidumbre
const.physical_constants['electron mass']
# → (9.1093837015e-31, 'kg', 2.8e-40)    (valor, unidad, incertidumbre)
```

## Tres vias de acceso

La distincion clave es **cuanto** necesitas de cada constante. El **atributo** da solo el numero (ideal para calcular); la **clave de diccionario** da ademas la unidad y la incertidumbre (util para documentar o propagar el error). Las claves CODATA son largas y especificas (`'electron mass'`, `'Bohr radius'`), por lo que existe una funcion de busqueda para descubrirlas.

| Via | Forma | Devuelve |
|-----|-------|----------|
| Atributo directo | `const.c`, `const.G`, `const.h`, `const.k`, `const.pi` | un `float` listo para operar |
| Diccionario CODATA | `const.physical_constants['speed of light in vacuum']` | la tupla `(valor, unidad, incertidumbre)` |
| Extractores por campo | `value(key)`, `unit(key)`, `precision(key)` | `float`, `str`, `float` (incertidumbre relativa) |
| Prefijos SI | `const.kilo`, `const.mega`, `const.nano` | factor `float` (potencia de 10) |
| Factores de conversion | `const.atm`, `const.hour`, `const.inch`, `const.eV` | factor `float` a unidades SI |

## Notas del submodulo

### [[scipy.constants.constantes_fisicas|constantes_fisicas]]
Panorama del submodulo: las **tres vias de acceso** (atributo, diccionario `physical_constants`, prefijos y conversiones) con sus ejemplos. Explica cuando usar el atributo (solo el numero, para calcular) frente a la clave de diccionario (valor, unidad e incertidumbre CODATA), y tabula las constantes, prefijos y factores de conversion mas habituales.

### [[scipy.constants.find_unit|find_unit]]
Flujo de **consulta del catalogo CODATA**: `find(sub)` busca claves cuyo nombre contenga un substring (las claves son largas y especificas, hay que descubrirlas), y los extractores `value(key)`, `unit(key)` y `precision(key)` leen cada campo de la constante una vez hallada su clave exacta.

## Notas relacionadas

- [[SciPy/index\|SciPy]]
- [[SciPy/scipy.special/index\|scipy.special]]
