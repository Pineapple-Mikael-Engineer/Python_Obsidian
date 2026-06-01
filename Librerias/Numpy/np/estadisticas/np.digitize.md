---
title: np.digitize — Asignar valores a intervalos (bins)
aliases:
  - digitize
  - np.digitize
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.digitize — Asignar valores a intervalos (bins)

## Firma de la función

```python
np.digitize(
    x,
    bins,
    right=False
) -> ndarray
```

## Valor de retorno

Devuelve, para cada valor de `x`, el **índice del bin** al que pertenece según los bordes `bins`. Útil para discretizar/categorizar datos continuos.

| `x` | `bins` | Resultado |
|-----|--------|-----------|
| `[0.2, 1.5, 2.7]` | `[0, 1, 2, 3]` | `[1, 2, 3]` |

```python
import numpy as np
x = np.array([0.2, 1.5, 2.7, 5.0])
bins = np.array([0, 1, 2, 3])
np.digitize(x, bins)   # array([1, 2, 3, 4])
```

## Convención de índices

- `0` → menor que `bins[0]`
- `i` → en `[bins[i-1], bins[i])`
- `len(bins)` → mayor o igual que el último borde

## Parámetros en detalle

### `x` — valores a clasificar

Array de entrada.

### `bins` — bordes (monótonos)

Deben estar **ordenados** (ascendente o descendente).

### `right` — lado cerrado del intervalo

`False` (por defecto): intervalos `[izq, der)`. `True`: `(izq, der]`.

## Casos de uso

### Convertir notas en categorías

```python
notas = np.array([55, 72, 88, 95])
cortes = np.array([60, 70, 80, 90])
np.digitize(notas, cortes)   # [0, 2, 3, 4] → F, C, B, A
```

### Mapear valores a sus bins de histograma

```python
hist, edges = np.histogram(datos, bins=10)
bin_idx = np.digitize(datos, edges)
```

## Buenas prácticas

1. `bins` debe estar **ordenado**; si no, los resultados no tienen sentido.
2. Combínalo con [[np.histogram]] para saber a qué bin fue cada dato.
3. Para categorías por condiciones (no rangos), usa [[np.select]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índices sin sentido | `bins` no ordenado | ordenar los bordes |
| Off-by-one en los extremos | semántica `[izq, der)` | revisar `right` |

## Limitaciones

- Requiere `bins` monótono; índices 0 y `len(bins)` son los desbordes.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.histogram]]
- [[np.bincount]]
- [[np.select]]
