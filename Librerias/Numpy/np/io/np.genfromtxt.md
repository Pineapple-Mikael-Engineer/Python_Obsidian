---
title: np.genfromtxt — Cargar texto con valores faltantes
aliases:
  - genfromtxt
  - np.genfromtxt
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.genfromtxt — Cargar texto con valores faltantes

## Firma de la función

```python
np.genfromtxt(
    fname,
    dtype=float,
    delimiter=None,
    skip_header=0,
    missing_values=None,
    filling_values=None,
    names=None,
    usecols=None
) -> ndarray
```

## Valor de retorno

Versión más **robusta** de [[np.loadtxt]]: tolera **valores faltantes**, tipos mixtos y cabeceras con nombres. Más lenta, pero maneja datos "sucios".

```python
import numpy as np
# CSV con un hueco
datos = np.genfromtxt('sucio.csv', delimiter=',', filling_values=0)
```

## genfromtxt vs loadtxt

| | [[np.loadtxt]] | `np.genfromtxt` |
|--|---------------|-----------------|
| Valores faltantes | ❌ falla | ✅ los rellena |
| Velocidad | rápida | más lenta |
| Tipos mixtos / nombres | limitado | sí (`names=True`) |

## Parámetros en detalle

### `missing_values` / `filling_values`

Qué se considera faltante y con qué rellenarlo (por defecto `nan`).

### `names` — nombres de columna

`names=True` lee la cabecera y crea un **array estructurado** accesible por nombre:

```python
d = np.genfromtxt('t.csv', delimiter=',', names=True)
d['temperatura']
```

### `skip_header` — saltar líneas

Equivalente a `skiprows` de loadtxt.

## Casos de uso

### Leer un CSV con huecos

```python
np.genfromtxt('datos.csv', delimiter=',', filling_values=np.nan)
```

## Buenas prácticas

1. Úsala cuando [[np.loadtxt]] falle por huecos o formato irregular.
2. `names=True` da acceso por nombre de columna (array estructurado).
3. Para análisis de datos serio, considera pandas `read_csv`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Columnas con `nan` inesperados | huecos rellenados por defecto | ajustar `filling_values` |
| Rendimiento lento | archivo enorme | usar pandas o [[np.load]] binario |

## Limitaciones

- Más lenta que loadtxt; el manejo de tipos mixtos puede ser delicado.

## Notas relacionadas

- [[concepto_dtype]]
- [[np.loadtxt]]
- [[np.savetxt]]
