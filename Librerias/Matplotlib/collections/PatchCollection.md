---
title: PatchCollection — Muchos parches gestionados como un solo Artist
aliases:
  - PatchCollection
  - colección de parches
tags:
  - matplotlib
  - api/clase
  - plot/formas

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.collections
tipo: clase
obj: PatchCollection

# --- Comportamiento ---
retorna: PatchCollection
muta_estado: false

draft: false
---

# PatchCollection — Muchos parches gestionados como un solo Artist

## Definición

`PatchCollection` agrupa **muchos [[Patch]]** (Rectangles, Circles, Polygons...) en un **único Artist**, en lugar de añadir cada forma por separado. Dibujar miles de parches sueltos es lento; una colección los renderiza de golpe y permite recolorearlos o ajustarlos con una sola llamada. Se inserta en el Axes con `ax.add_collection`.

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection

circles = [Circle((x[i], y[i]), r[i]) for i in range(N)]
pc = PatchCollection(circles)
ax.add_collection(pc)        # un solo Artist para N círculos
ax.autoscale()               # los Collection no autoescalan solos
```

## Parámetros del constructor

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `patches` | lista de `Patch` | — | las formas a agrupar |
| `match_original` | `bool` | `False` | conservar el color/estilo de cada parche original |
| `cmap` | `Colormap`/`str` | `None` | colormap para colorear por valor (con `set_array`) |
| `norm` | `Normalize` | `None` | mapeo valor→[0,1] de la escala de color |
| `alpha` | `float` | `None` | transparencia global |
| `edgecolor` / `facecolor` | color | `None` | colores comunes a toda la colección |

## Métodos principales

| Método | Qué hace | Ejemplo |
|--------|----------|---------|
| `set_array(valores)` | array escalar que el colormap traduce a color | `pc.set_array(z)` |
| `set_cmap(name)` | cambia el colormap | `pc.set_cmap('plasma')` |
| `set_clim(lo, hi)` | fija los límites de la escala de color | `pc.set_clim(0, 100)` |
| `set_facecolors(c)` | color de relleno común | `pc.set_facecolors('skyblue')` |
| `set_edgecolors(c)` | color de borde | `pc.set_edgecolors('black')` |
| `set_alpha(a)` | transparencia global | `pc.set_alpha(0.6)` |
| `remove()` | elimina la colección del Axes | `pc.remove()` |

## Colorear por valor

Para teñir cada parche según un dato numérico, la colección guarda un **array escalar** y un colormap lo traduce a color, normalizado por [[Normalize]]. `set_array` actualiza ese array tras la creación.

```python
pc = PatchCollection(rectangles, cmap='viridis')
pc.set_array(valores)          # un valor por parche
pc.set_clim(valores.min(), valores.max())
ax.add_collection(pc)
plt.colorbar(pc, ax=ax)        # leyenda de la escala
```

## Casos de uso

### Mapa de muchos rectángulos coloreados

```python
from matplotlib.patches import Rectangle

rects = [Rectangle((i, 0), 1, h[i]) for i in range(len(h))]
pc = PatchCollection(rects, cmap='magma')
pc.set_array(h)
ax.add_collection(pc)
ax.autoscale()
```

### Conservar el color individual de cada parche

```python
shapes = [Circle((x[i], y[i]), 0.1, color=col[i]) for i in range(N)]
pc = PatchCollection(shapes, match_original=True)   # respeta cada color
ax.add_collection(pc)
```

## Buenas prácticas

1. Tras `add_collection` llama `ax.autoscale()` o fija límites: las colecciones no ajustan los ejes automáticamente.
2. Usa `match_original=True` solo si ya diste color a cada parche; si vas a colorear por valor, omítelo y usa `set_array`.
3. Una colección es un `Artist`; aprovecha el protocolo `get_*`/`set_*` de [[concepto_artist]] para inspeccionarla y modificarla en bloque.
4. Para nubes de **marcadores** (puntos de scatter) usa la colección específica que devuelve [[ax.scatter]], no `PatchCollection`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Nada se ve tras crear la colección | no se añadió al Axes | `ax.add_collection(pc)` |
| Los ejes no encuadran las formas | colecciones no autoescalan | `ax.autoscale()` o fijar `set_xlim`/`set_ylim` |
| `set_array` no colorea | falta colormap | crear con `cmap=` o `set_cmap` |
| Colores individuales ignorados | sin `match_original` | `PatchCollection(..., match_original=True)` |
| Colorbar vacía | no se pasó la colección | `plt.colorbar(pc)` |

## Notas relacionadas

- [[Patch]]
- [[Normalize]]
- [[concepto_artist]]
- [[LineCollection]]
- [[ax.scatter]]
