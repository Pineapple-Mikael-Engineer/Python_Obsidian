---
title: LinearSegmentedColormap — Colormap continuo por segmentos de anclaje
aliases:
  - LinearSegmentedColormap
  - colormap continuo
  - cmap por segmentos
tags:
  - matplotlib
  - api/clase
  - styling
lib: matplotlib
obj: LinearSegmentedColormap
tipo: clase
retorna: LinearSegmentedColormap
muta_estado: false
draft: false
---

# LinearSegmentedColormap — Colormap continuo por segmentos de anclaje

## Idea clave

`LinearSegmentedColormap` es un colormap **continuo** definido por puntos de anclaje entre los que el color se interpola suavemente. Es la maquinaria detrás de la mayoría de los [[Colormaps]] de Matplotlib (`viridis`, `coolwarm`...). Para crear uno propio rara vez se usa el constructor crudo: el atajo es `from_list`, que recibe una lista de colores y construye el gradiente. Contrasta con [[ListedColormap]], que produce una lista **discreta** de colores sin interpolar. Es la fuente de color del [[concepto_color_mapping]].

## Firma del constructor

```python
# Constructor de clase (atajo recomendado):
matplotlib.colors.LinearSegmentedColormap.from_list(
    name,         # nombre del colormap, p.ej. 'azul_blanco_rojo'
    colors,       # lista de colores de anclaje: ['blue', 'white', 'red']
    N=256,        # nº de niveles de resolución del gradiente
)

# Constructor crudo (avanzado, con segmentos por canal):
matplotlib.colors.LinearSegmentedColormap(name, segmentdata, N=256)
```

## Qué hace / Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Tipo | colormap **continuo** (interpola entre anclas) |
| Retorna | un objeto `Colormap` llamable: `cmap(0.0..1.0)` → RGBA |
| Vía recomendada | `LinearSegmentedColormap.from_list(...)` |
| `muta_estado` | `false` — produce un objeto nuevo, no altera nada global |
| Contraste | continuo, frente al discreto de `ListedColormap` |

```python
from matplotlib.colors import LinearSegmentedColormap

cmap = LinearSegmentedColormap.from_list('bwr2', ['blue', 'white', 'red'])
cmap(0.0)    # → (0.0, 0.0, 1.0, 1.0)   azul
cmap(0.5)    # → (1.0, 1.0, 1.0, 1.0)   blanco (interpolado)
cmap(1.0)    # → (1.0, 0.0, 0.0, 1.0)   rojo
```

## Parámetros en detalle

### `colors` — anclas del gradiente

```python
# El color se interpola linealmente entre cada par de anclas consecutivas
cmap = LinearSegmentedColormap.from_list('fuego', ['black', 'red', 'yellow'])
```

### `N` — resolución del gradiente

```python
cmap = LinearSegmentedColormap.from_list('grad', ['#003f5c', '#ffa600'], N=512)
# más N → transición más fina (más niveles intermedios)
```

### Anclas con posición explícita

```python
# Cada ancla como (posición_0a1, color): controla DÓNDE cae cada color
cmap = LinearSegmentedColormap.from_list(
    'sesgado', [(0.0, 'blue'), (0.2, 'white'), (1.0, 'red')]
)
```

## Casos de uso

### Colormap divergente a medida

```python
cmap = LinearSegmentedColormap.from_list('anom', ['navy', 'white', 'darkred'])
ax.imshow(anomalias, cmap=cmap, vmin=-5, vmax=5)
```

### Gradiente de marca corporativa

```python
cmap = LinearSegmentedColormap.from_list('marca', ['#1b2a49', '#00a8cc'])
sc = ax.scatter(x, y, c=z, cmap=cmap)
fig.colorbar(sc, ax=ax)
```

## Buenas prácticas

1. Usa `from_list` para casos normales; reserva el constructor crudo con `segmentdata` para control por canal RGB.
2. Para divergentes, pon el color neutro (blanco/gris) exactamente en el centro de la lista.
3. Sube `N` solo si ves bandas visibles en el gradiente; 256 suele bastar.
4. Si quieres colores planos sin transición, usa `ListedColormap` en su lugar.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Bandas visibles en el gradiente | `N` demasiado bajo | aumentar `N` (p.ej. 256 → 512) |
| Color central descentrado | anclas mal posicionadas | dar posiciones explícitas `(pos, color)` |
| `ValueError: Invalid RGBA argument` | nombre de color inválido | usar nombres válidos o hex `'#rrggbb'` |
| Transición suave no deseada | se quería discreto | usar `ListedColormap` en vez de este |

## Notas relacionadas

- [[ListedColormap]]
- [[Colormaps]]
- [[concepto_color_mapping]]
- [[Normalize]]
