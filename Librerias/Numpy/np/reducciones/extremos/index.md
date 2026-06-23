---
title: np/reducciones/extremos — mínimo, máximo, su posición y el rango
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/extremos — mínimo, máximo, su posición y el rango

Las 5 funciones de esta subcarpeta localizan los **valores extremos** de un array a lo largo de un
[[concepto_axis_parametro|eje]]. Lo que las separa no es *qué* extremo buscan, sino *qué devuelven*
sobre ese extremo. Hay tres respuestas distintas a la misma pregunta:

- **El VALOR** del extremo — `np.max` / `np.min`: "¿*cuánto* vale el mayor/menor?".
- **La POSICIÓN** del extremo — `np.argmax` / `np.argmin`: "¿*dónde* está el mayor/menor?" (un
  índice entero, no el valor).
- **El RANGO** entre extremos — `np.ptp` (peak-to-peak): `max - min`, la amplitud completa.

```python
import numpy as np
a = np.array([3, 1, 4, 1, 5, 9, 2, 6])

np.min(a)     # 1  — VALOR mínimo
np.argmin(a)  # 1  — POSICIÓN del mínimo (primera ocurrencia)

np.max(a)     # 9  — VALOR máximo
np.argmax(a)  # 5  — POSICIÓN del máximo

np.ptp(a)     # 8  — RANGO: 9 - 1
```

## Tabla de decisión

| Quiero… | Función | Devuelve | Ejemplo de uso |
|---|---|---|---|
| el valor más grande | `np.max` | el valor | el pico de una señal |
| el valor más pequeño | `np.min` | el valor | el suelo de una serie |
| la posición del mayor | `np.argmax` | un índice entero | la clase predicha de unos logits |
| la posición del menor | `np.argmin` | un índice entero | el vecino más cercano |
| la amplitud (máx − mín) | `np.ptp` | el valor | normalizar a `[0,1]` |

Todas comparten el comportamiento de `axis`: con un array 2-D, `axis=0` busca el extremo **entre
filas** (resultado por columna) y `axis=1` lo busca **entre columnas** (resultado por fila). El eje
indicado es el que se colapsa.

```python
M = np.array([[3, 1],
              [4, 2]])

np.argmin(M, axis=0)  # [0, 0] — fila donde está el mínimo de cada columna
np.argmin(M, axis=1)  # [1, 1] — columna donde está el mínimo de cada fila
```

## Dos trampas que hay que recordar

> [!warning] La trampa del `NaN`
> Con datos que pueden contener `NaN`, estas cinco funciones fallan: `max`/`min` **propagan** el
> `NaN` (devuelven `NaN`) y `argmax`/`argmin` apuntan a una posición poco fiable. Usa las variantes
> que lo ignoran — [[np.nanmin]], [[np.nanmax]], [[np.nanargmin]] y [[np.nanargmax]] — de
> [[Librerias/Numpy/np/reducciones/nan_safe/index|nan_safe/]].

> [!warning] La trampa del array aplanado en `argmax`/`argmin`
> Sin `axis`, `argmax`/`argmin` devuelven el índice sobre el array **aplanado** a 1D, no una posición
> N-D. En 2D+ ese número no es una fila ni una columna. Para recuperar la posición real, tradúcelo
> con `np.unravel_index(idx, a.shape)` (o, para el valor directo, `a.flat[np.argmin(a)]`).

## Notas de esta subcarpeta

| Función | Qué devuelve |
|---|---|
| [[np.min]] | El **valor** del elemento mínimo. Equivalente a `a.min()`. |
| [[np.max]] | El **valor** del elemento máximo. Equivalente a `a.max()`. |
| [[np.argmin]] | El **índice** del mínimo. Sin `axis`, el índice aplanado; con `axis`, el índice a lo largo del eje. |
| [[np.argmax]] | El **índice** del máximo. Mismo comportamiento que `argmin`. |
| [[np.ptp]] | El **rango** peak-to-peak: `max - min`. Útil para normalizar con `(a - a.min()) / a.ptp()`. Deprecada como método en versiones recientes de NumPy (usar `np.ptp(a)`). |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se colapsa al buscar el extremo
- [[concepto_indexing]] — `np.unravel_index` para el índice aplanado de `argmax`/`argmin`
- [[Librerias/Numpy/np/reducciones/nan_safe/index|nan_safe/]] — las variantes que ignoran `NaN`
- [[np.sum]] — la reducción de referencia (mismo mapa de shapes)
