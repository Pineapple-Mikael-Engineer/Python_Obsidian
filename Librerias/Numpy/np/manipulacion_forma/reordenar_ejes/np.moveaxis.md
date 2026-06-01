---
title: np.moveaxis — Reubicar ejes conservando el orden del resto
aliases:
  - moveaxis
  - np.moveaxis
tags:
  - numpy
  - api/funcion
  - shape

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_views_vs_copias

draft: false
---

# np.moveaxis — Reubicar ejes conservando el orden del resto

## Firma de la función

```python
np.moveaxis(
    a,
    source,
    destination
) -> ndarray
```

## Valor de retorno

Devuelve una [[concepto_views_vs_copias|vista]] de `a` donde los ejes en `source` se trasladan a las posiciones `destination`, **manteniendo el orden relativo** de los demás ejes. No copia datos.

| Shape entrada | `source → destination` | Shape salida |
|---------------|------------------------|--------------|
| `(2, 3, 4)` | `0 → 2` | `(3, 4, 2)` |
| `(2, 3, 4)` | `2 → 0` | `(4, 2, 3)` |
| `(2, 3, 4)` | `[0, 1] → [1, 2]` | `(4, 2, 3)` |

```python
import numpy as np
T = np.ones((2, 3, 4))
np.moveaxis(T, 0, -1).shape   # (3, 4, 2)  → lleva el eje 0 al final
```

## La diferencia con swapaxes y transpose

| Función | Qué hace |
|---------|----------|
| [[np.swapaxes]] | intercambia **dos** ejes (el resto puede desordenarse) |
| `np.moveaxis` | mueve eje(s) a una posición, **conservando el orden** de los demás |
| [[np.transpose]] | permutación arbitraria y completa de ejes |

```python
T = np.ones((2, 3, 4, 5))
np.moveaxis(T, 1, 3).shape   # (2, 4, 5, 3)  → 0,2,3 quedan en su orden
```

## Parámetros en detalle

### `a` — array de entrada

Array de cualquier dimensión.

### `source` — posición(es) original(es)

Entero o secuencia de enteros (admite negativos).

### `destination` — posición(es) destino

Entero o secuencia de la misma longitud que `source`.

## Casos de uso

### Convertir formato de imagen CHW ↔ HWC

```python
chw = np.random.rand(3, 224, 224)        # canal, alto, ancho
hwc = np.moveaxis(chw, 0, -1)            # (224, 224, 3)  alto, ancho, canal
```

### Llevar el eje temporal al frente

```python
datos = np.random.rand(32, 100, 10)      # (batch, tiempo, feat)
por_tiempo = np.moveaxis(datos, 1, 0)    # (100, 32, 10)
```

## Buenas prácticas

1. Prefiérelo sobre `transpose` cuando solo quieras **reubicar** uno o pocos ejes sin tocar el orden del resto: es más legible y menos propenso a errores.
2. Es ideal para conversiones de convención de ejes (canales, batch, tiempo).
3. Devuelve vista; usa `.copy()` o `np.ascontiguousarray` si necesitas contigüidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `source and destination must have the same number of elements` | longitudes distintas | igualar el número de ejes movidos |
| `AxisError` | eje fuera de rango | usar ejes válidos |
| Resultado inesperado vs `transpose` | confundir "mover" con "permutar" | recordar que conserva el orden del resto |

## Limitaciones

- No copia datos; reordena strides (puede dejar el array no contiguo).

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_views_vs_copias]]
- [[np.swapaxes]]
- [[np.transpose]]
