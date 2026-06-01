---
title: BoundaryNorm — Normalización discreta por bins de color
aliases:
  - BoundaryNorm
  - norma discreta
  - normalización por niveles
tags:
  - matplotlib
  - api/clase
  - styling
lib: matplotlib
obj: BoundaryNorm
tipo: clase
retorna: BoundaryNorm
muta_estado: false
draft: false
---

# BoundaryNorm — Normalización discreta por bins de color

## Idea clave

`BoundaryNorm` reparte los datos en **bins discretos** según una lista de fronteras (`boundaries`) y asigna a cada bin un color del colormap. A diferencia de la norma lineal continua de [[Normalize]], aquí el color **salta** por niveles en vez de variar suavemente. Es ideal para mapas por categorías, escalas escalonadas o cuando quieres que cada banda de valores tenga un color sólido y distinguible. Forma parte del [[concepto_color_mapping]] y se combina muy bien con un colormap discreto.

## Firma del constructor

```python
matplotlib.colors.BoundaryNorm(
    boundaries,    # lista creciente de fronteras de los bins, p.ej. [0, 10, 20, 30]
    ncolors,       # nº de colores disponibles en el colormap
    clip=False,    # recorta fuera de rango si True
    extend='neither',  # 'min' | 'max' | 'both' para colores de desborde
)
```

> Con `N` fronteras se forman `N-1` bins; conviene que `ncolors >= N-1`.

## Qué hace / Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Tipo de mapeo | **discreto**: cada valor cae en un bin y toma su color |
| Define | `len(boundaries) - 1` bandas de color |
| `muta_estado` | `false` — describe el reparto en bins, no altera datos |
| Combina con | colormaps discretos (`plt.get_cmap('viridis', 4)`) |

```python
from matplotlib.colors import BoundaryNorm

bounds = [0, 10, 20, 30]              # 3 bins: [0,10), [10,20), [20,30)
norm = BoundaryNorm(bounds, ncolors=3)
norm(5)      # → 0   (primer bin)
norm(15)     # → 1   (segundo bin)
norm(25)     # → 2   (tercer bin)
```

## Parámetros en detalle

### `boundaries` — fronteras de los bins

```python
# Niveles de precipitación en mm: cada banda un color sólido
bounds = [0, 1, 5, 20, 50, 100]
norm = BoundaryNorm(bounds, ncolors=256)
```

### `ncolors` — paleta disponible

```python
cmap = plt.get_cmap('viridis', 5)            # 5 colores discretos
norm = BoundaryNorm([0, 2, 4, 6, 8, 10], ncolors=5)
ax.pcolormesh(X, Y, Z, cmap=cmap, norm=norm)
```

### `extend` — colores de desborde

```python
norm = BoundaryNorm(bounds, ncolors=256, extend='both')  # color extra <min y >max
```

## Casos de uso

### Mapa por niveles (escala escalonada)

```python
bounds = [0, 25, 50, 75, 100]
cmap = plt.get_cmap('plasma', 4)
im = ax.imshow(M, cmap=cmap, norm=BoundaryNorm(bounds, 4))
fig.colorbar(im, ax=ax)   # la barra muestra los cortes discretos
```

### Categorías codificadas como enteros

```python
bounds = [-0.5, 0.5, 1.5, 2.5]               # clases 0, 1, 2
norm = BoundaryNorm(bounds, ncolors=3)
ax.scatter(x, y, c=clase, cmap='tab10', norm=norm)
```

## Buenas prácticas

1. Empareja `ncolors` con un colormap discreto del mismo número de niveles para colores nítidos.
2. Centra las fronteras entre enteros (`-0.5, 0.5, ...`) cuando codifiques categorías.
3. Usa `extend` si esperas valores fuera del rango cubierto por las fronteras.
4. Pasa las mismas `boundaries` a la colorbar para que las marcas caigan en los cortes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Colores no coinciden con los bins | `ncolors` ≠ niveles del cmap | igualar `ncolors` y la versión discreta del colormap |
| Fronteras no monótonas | `boundaries` no es creciente | ordenar la lista de forma estrictamente creciente |
| Valores fuera de rango sin color | falta `extend` | usar `extend='min'`, `'max'` o `'both'` |
| Transición suave inesperada | se usó norma lineal | usar `BoundaryNorm`, no `Normalize` |

## Notas relacionadas

- [[Normalize]]
- [[ListedColormap]]
- [[concepto_color_mapping]]
- [[plt.colorbar]]
