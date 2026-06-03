---
title: ListedColormap — Colormap discreto a partir de una lista de colores
aliases:
  - ListedColormap
  - colormap discreto
  - colormap personalizado
tags:
  - matplotlib
  - api/clase
  - styling

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.colors
tipo: clase
obj: ListedColormap

# --- Comportamiento ---
retorna: ListedColormap
muta_estado: false

draft: false
---

# ListedColormap — Colormap discreto a partir de una lista de colores

## Firma del constructor

```python
matplotlib.colors.ListedColormap(
    colors,        # lista de colores (nombres, hex o tuplas RGBA)
    name='from_list',
    N=None         # nº de entradas; por defecto len(colors)
)
```

Crea un colormap **discreto** a partir de una lista **explícita** de colores. Cada color ocupa una banda fija: ideal para clasificaciones, máscaras o paletas de marca donde quieres control total y bordes nítidos entre niveles. Es una de las dos formas de construir un colormap propio dentro del universo de [[Colormaps]].

```python
from matplotlib.colors import ListedColormap

cmap = ListedColormap(['red', 'green', 'blue'])
cmap.N        # → 3   número de colores
cmap(0)       # → (1.0, 0.0, 0.0, 1.0)  primer color (rojo)
cmap(2)       # → (0.0, 0.0, 1.0, 1.0)  tercer color (azul)
```

## Discreto vs continuo

| Clase | Construcción | Resultado | Uso típico |
|-------|--------------|-----------|------------|
| `ListedColormap` | lista explícita de colores | bandas discretas, bordes nítidos | clases, máscaras, paletas fijas |
| `LinearSegmentedColormap` | puntos de anclaje interpolados | gradiente continuo | magnitudes, datos continuos |

`ListedColormap` **no interpola**: con 3 colores tendrás exactamente 3 bandas. `LinearSegmentedColormap` rellena el espacio entre anclas con un degradado suave.

## Casos de uso

### Paleta de clasificación discreta

```python
from matplotlib.colors import ListedColormap

cmap = ListedColormap(['#1b9e77', '#d95f02', '#7570b3'])
ax.scatter(x, y, c=etiquetas, cmap=cmap)   # 3 grupos, 3 colores fijos
```

### Máscara binaria (dos colores)

```python
cmap = ListedColormap(['white', 'black'])
ax.imshow(mascara, cmap=cmap)   # 0 → blanco, 1 → negro
```

### Recortar un colormap existente a N niveles

```python
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

base = plt.get_cmap('viridis')
cmap = ListedColormap(base(np.linspace(0, 1, 5)))   # 5 bandas de viridis
```

## Buenas prácticas

1. Usa `ListedColormap` cuando el dato es **categórico** o quieres bandas visibles; reserva el gradiente continuo para magnitudes.
2. Combínalo con `BoundaryNorm` para mapear rangos numéricos concretos a cada banda de color.
3. Mantén un nº de colores razonable (<= ~12): demasiadas categorías se vuelven indistinguibles.
4. Acepta cualquier formato de color de Matplotlib (nombre, hex, RGBA), así que puedes reutilizar paletas corporativas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Colores fuera de rango se ven recortados | índice mayor que `N-1` | Ajustar `N` o normalizar el dato |
| Transición suave inesperada | se esperaba discreto pero se usó interpolación | Confirmar que es `ListedColormap`, no `LinearSegmentedColormap` |
| `ValueError: Invalid RGBA argument` | string de color no válido | Usar nombre/hex válido de Matplotlib |
| Bandas mal alineadas con los datos | norm por defecto | Acompañar con `BoundaryNorm` y límites explícitos |

## Notas relacionadas

- [[Colormaps]]
- [[plt.colorbar]]
- [[concepto_artist]]
