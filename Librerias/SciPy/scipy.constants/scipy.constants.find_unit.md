---
title: scipy.constants.find — descubrir claves CODATA y leer valor, unidad e incertidumbre
aliases:
  - scipy.constants.find
  - find constants
  - value unit precision
  - buscar constante CODATA
tags:
  - scipy
  - api/funcion
  - constantes
lib: scipy
tipo: funcion
mod: scipy.constants
retorna: list[str]
requiere:
  - scipy.constants
draft: false
---

# scipy.constants.find — descubrir claves CODATA y leer valor, unidad e incertidumbre

`find(sub=None, disp=False)` **busca claves** en el diccionario `physical_constants` cuyo nombre **contenga el substring** `sub` (insensible a mayusculas). Sirve para **descubrir el nombre exacto** de una constante antes de consultarla, ya que las claves CODATA son largas y especificas (`'electron mass'`, `'Bohr radius'`, ...). Por defecto **devuelve una lista** ordenada de claves coincidentes; con `disp=True` las **imprime** y devuelve `None`. Una vez hallada la clave, se lee con `value(key)`, `unit(key)` y `precision(key)`. Este archivo documenta `find` mas ese flujo de consulta.

> Nota de nombre: la funcion se llama `scipy.constants.find` (no `find_unit`). Este nodo agrupa `find` con los extractores `value` / `unit` / `precision` como un unico **flujo de consulta**: buscar la clave, luego leer sus campos. El panorama del submodulo esta en [[scipy.constants.constantes_fisicas]].

## Firma

```python
scipy.constants.find(
    sub=None,     # str | None: substring a buscar en las claves (None -> todas)
    disp=False,   # bool: True imprime y devuelve None; False devuelve la lista
) -> list[str] | None
```

## Valor de retorno

| `disp` | Devuelve | Efecto |
|--------|----------|--------|
| `False` (defecto) | `list[str]` de claves coincidentes | Ninguno; usable en codigo |
| `True` | `None` | Imprime las claves por pantalla |

```python
from scipy.constants import find
find('electron')          # → ['Bohr electron magn. ...', 'classical electron radius', 'electron mass', ...]
find('electron', disp=True)   # imprime la lista, devuelve None
```

## Flujo de consulta: buscar y leer

```python
import scipy.constants as const

# 1) Descubrir el nombre exacto de la clave
const.find('electron mass')
# → ['electron mass', 'electron mass energy equivalent', 'electron mass in u', ...]

# 2) Leer sus campos con la clave exacta
const.value('electron mass')       # → 9.1093837015e-31
const.unit('electron mass')        # → 'kg'
const.precision('electron mass')   # → 3.1e-10   (incertidumbre relativa)
```

## Extractores asociados

Tras encontrar la clave con `find`, estos tres extraen cada campo de la tupla `(valor, unidad, incertidumbre)` que guarda `physical_constants`.

| Funcion | Devuelve | Significado |
|---------|----------|-------------|
| `value(key)` | `float` | Valor numerico de la constante |
| `unit(key)` | `str` | Unidad SI como texto |
| `precision(key)` | `float` | Incertidumbre **relativa** (inc. absoluta / valor) |

```python
# Equivalencia con el diccionario crudo
const.value('proton mass') == const.physical_constants['proton mass'][0]   # → True
const.unit('proton mass')  == const.physical_constants['proton mass'][1]   # → True
```

## Casos de uso

### Descubrir una constante de la que no recuerdas la clave

```python
import scipy.constants as const

const.find('Avogadro')      # → ['Avogadro constant']
const.value('Avogadro constant')   # → 6.02214076e+23
```

### Explorar una familia de constantes

```python
# Todas las claves relativas al proton
const.find('proton')
# → ['proton charge to mass quotient', 'proton mass', 'proton mass energy equivalent', ...]
```

### Inventario completo

```python
todas = const.find()        # sin sub: lista TODAS las claves CODATA
len(todas)                  # → varios cientos (depende de la version)
```

## Buenas practicas

1. Usa `find('substring')` (sin `disp`) cuando trabajes en codigo: obtienes una **lista** filtrable; reserva `disp=True` para exploracion interactiva.
2. Pasa el substring mas distintivo posible para acotar la lista (`'electron mass'` mejor que `'mass'`).
3. Confirma la clave exacta antes de usar `value` / `unit` / `precision`: un nombre aproximado da `KeyError`.
4. Recuerda que `precision` es **relativa**; para la incertidumbre absoluta lee `physical_constants[key][2]`.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `KeyError` en `value(key)` | Clave aproximada, no la exacta de `find` | Copiar literal una entrada devuelta por `find` |
| `find` devuelve `[]` | Substring no aparece en ninguna clave | Probar termino mas corto o ingles (claves en ingles) |
| Esperar tupla de `find` | `find` devuelve **lista de claves**, no valores | Leer cada clave con `value` / `unit` / `precision` |
| `None` inesperado | Se llamo con `disp=True` | Quitar `disp` para obtener la lista |

## Limitaciones

- Las claves estan en **ingles** y siguen la nomenclatura CODATA; la busqueda es por substring literal, sin sinonimos ni fuzzy matching.
- `find` solo cubre `physical_constants`; los **atributos directos** (`c`, `pi`, `kilo`) y los factores de conversion no aparecen en sus resultados.

## Notas relacionadas

- [[scipy.constants.constantes_fisicas]]
