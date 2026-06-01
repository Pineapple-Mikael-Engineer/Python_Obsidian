---
title: LineCollection — Muchos segmentos de línea como un solo Artist
aliases:
  - LineCollection
  - colección de líneas
tags:
  - matplotlib
  - api/clase
  - plot/lineas

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.collections
tipo: clase
obj: LineCollection

# --- Comportamiento ---
retorna: LineCollection
muta_estado: false

draft: false
---

# LineCollection — Muchos segmentos de línea como un solo Artist

## Definición

`LineCollection` agrupa **muchos segmentos de línea** en un **único Artist**. Es la herramienta idónea para trayectorias coloreadas por valor: cada segmento puede llevar un color distinto según un array (velocidad a lo largo de un recorrido, tiempo, temperatura...). Mucho más eficiente que graficar miles de líneas sueltas. Se añade al Axes con `ax.add_collection`.

```python
import numpy as np
from matplotlib.collections import LineCollection

# segmentos: array (N, 2, 2) → N segmentos, cada uno [[x0,y0],[x1,y1]]
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

lc = LineCollection(segments, cmap='viridis')
lc.set_array(z)              # un valor por segmento → color
ax.add_collection(lc)
ax.autoscale()
```

## Parámetros del constructor

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `segments` | array `(N, 2, 2)` o lista | — | cada segmento es un par de puntos `[[x0,y0],[x1,y1]]` |
| `cmap` | `Colormap`/`str` | `None` | colormap para colorear por valor |
| `norm` | `Normalize` | `None` | mapeo valor→[0,1] de la escala |
| `linewidths` | `float`/lista | `None` | grosor común o por segmento |
| `colors` | color/lista | `None` | colores fijos (alternativa a `set_array`) |
| `linestyle` | `str` | `'solid'` | estilo de trazo |

## Métodos principales

| Método | Qué hace | Ejemplo |
|--------|----------|---------|
| `set_array(valores)` | array escalar → color por segmento | `lc.set_array(z)` |
| `set_cmap(name)` | cambia el colormap | `lc.set_cmap('plasma')` |
| `set_clim(lo, hi)` | límites de la escala de color | `lc.set_clim(0, 1)` |
| `set_segments(segs)` | reemplaza los segmentos | `lc.set_segments(nuevos)` |
| `set_linewidth(w)` | grosor común | `lc.set_linewidth(2)` |
| `set_alpha(a)` | transparencia global | `lc.set_alpha(0.7)` |
| `remove()` | elimina la colección | `lc.remove()` |

## Colorear una trayectoria por valor

La colección guarda un **array escalar** (uno por segmento) que un colormap traduce a color, normalizado mediante [[Normalize]]. Así una sola línea cambia de color a lo largo de su recorrido.

```python
lc = LineCollection(segments, cmap='viridis')
lc.set_array(velocidad)        # color = velocidad en cada tramo
lc.set_clim(velocidad.min(), velocidad.max())
ax.add_collection(lc)
plt.colorbar(lc, ax=ax, label='velocidad')
```

## Casos de uso

### Trayectoria coloreada por tiempo

```python
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)
lc = LineCollection(segments, cmap='plasma')
lc.set_array(np.arange(len(x)))   # progresión temporal
ax.add_collection(lc)
ax.autoscale()
```

### Muchas líneas de color fijo (sin colormap)

```python
lc = LineCollection(segments, colors='gray', linewidths=0.5, alpha=0.4)
ax.add_collection(lc)
ax.autoscale()
```

## Buenas prácticas

1. Construye los segmentos con el patrón `reshape(-1,1,2)` + `concatenate`: produce el array `(N,2,2)` que espera la clase.
2. Tras `add_collection` llama `ax.autoscale()`; las colecciones no ajustan los ejes solas.
3. Para color fijo usa `colors=`; para color por valor usa `cmap=` + `set_array` (no mezcles ambos). El mapeo se apoya en [[concepto_color_mapping]].
4. Es un `Artist` estándar; expone el protocolo `get_*`/`set_*` de [[concepto_artist]] para ajustes en bloque.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Nada aparece | falta `ax.add_collection` | añadir la colección al Axes |
| Ejes vacíos / mal encuadrados | no autoescala | `ax.autoscale()` |
| `set_array` no colorea | sin colormap o long. ≠ nº segmentos | usar `cmap=` y array de longitud N−1 |
| Forma de segmentos inválida | array no es `(N,2,2)` | reconstruir con reshape+concatenate |
| Colorbar vacía | no se pasó la colección | `plt.colorbar(lc)` |

## Notas relacionadas

- [[concepto_color_mapping]]
- [[Normalize]]
- [[concepto_artist]]
- [[PatchCollection]]
- [[Line2D]]
