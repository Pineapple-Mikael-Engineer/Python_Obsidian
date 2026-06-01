---
title: Polygon — Polígono de vértices arbitrarios
aliases:
  - Polygon
  - patches.Polygon
  - polígono

tags:
  - matplotlib
  - api/clase
  - plot/formas

# --- Clasificación ---
lib: matplotlib
obj: Polygon
mod: matplotlib.patches
tipo: clase

# --- Comportamiento ---
retorna: Polygon
muta_estado: false

# --- Dependencias ---
requiere:
  - Patch

draft: false
---

# Polygon — Polígono de vértices arbitrarios

## Definición

`Polygon` es la forma de **vértices arbitrarios** de Matplotlib: se construye a partir de un array `Nx2` de puntos `(x, y)` y conecta esos vértices en orden. Es un [[concepto_artist|Artist]] que **no se dibuja solo**: se añade con `ax.add_patch(poly)`. Hereda de la clase base [[Patch]] todas las propiedades de estilo. Sirve para triángulos, flechas, polígonos irregulares o regiones definidas por una lista de puntos.

## Firma del constructor

```python
from matplotlib.patches import Polygon

Polygon(
    xy,                # array Nx2 de vértices [[x0, y0], [x1, y1], ...]
    *,
    closed=True,       # True conecta el último vértice con el primero
    **kwargs           # facecolor, edgecolor, lw, alpha, fill, hatch, zorder (de Patch)
)
```

## Parámetros / propiedades

| Propiedad | Setter | Tipo / valores | Descripción |
|-----------|--------|----------------|-------------|
| xy | `set_xy(arr)` | array `Nx2` | vértices del polígono |
| closed | `set_closed(b)` | `True`/`False` | cierra la figura uniendo extremos |
| facecolor | `set_facecolor(c)` | color / `'none'` | relleno (heredado de Patch) |
| edgecolor | `set_edgecolor(c)` | color / `'none'` | borde (heredado) |
| linewidth | `set_linewidth(w)` | float | grosor del borde (`lw`) |
| alpha | `set_alpha(a)` | float 0..1 | transparencia |
| fill | `set_fill(b)` | `True`/`False` | si `False`, solo contorno |
| hatch | `set_hatch(s)` | `'/'`, `'x'`, ... | patrón de tramado |
| zorder | `set_zorder(z)` | float | orden de dibujo |

```python
poly.get_xy()        # → array de vértices (puede incluir el de cierre)
```

## Cómo añadirlo al Axes

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

fig, ax = plt.subplots()
verts = [[0.2, 0.2], [0.8, 0.3], [0.5, 0.9]]   # triángulo
tri = Polygon(verts, facecolor='lightgreen', edgecolor='darkgreen', lw=2)
ax.add_patch(tri)         # ← imprescindible
plt.show()
```

## Casos de uso

### Triángulo o forma irregular

```python
verts = [[0, 0], [4, 0], [4, 3], [1, 5]]      # cuadrilátero irregular
p = Polygon(verts, facecolor='tan', alpha=0.6)
ax.add_patch(p)
```

### Línea quebrada abierta (sin cerrar)

```python
camino = Polygon([[0, 0], [1, 2], [2, 1], [3, 3]],
                 closed=False, fill=False, edgecolor='black')
ax.add_patch(camino)       # trazo abierto, no se une el último con el primero
```

### Rellenar el área bajo una curva manualmente

```python
import numpy as np
x = np.linspace(0, 5, 50)
y = np.sin(x) + 1
verts = np.column_stack([np.r_[x, x[::-1]],
                         np.r_[y, np.zeros_like(y)]])   # contorno cerrado
area = Polygon(verts, facecolor='skyblue', alpha=0.4)
ax.add_patch(area)         # similar a ax.fill_between, pero como Patch
```

## Buenas prácticas

1. Pasa los vértices en orden coherente (horario o antihorario); el orden define la silueta.
2. Usa `closed=False` con `fill=False` para trazar polilíneas abiertas.
3. Para rellenar áreas bajo curvas de datos, `ax.fill` / `ax.fill_between` suele ser más directo que construir el `Polygon` a mano.
4. No repitas el primer vértice al final: con `closed=True` el cierre es automático.
5. Para muchos polígonos, agrúpalos en una `PatchCollection` por rendimiento.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Forma cruzada/«mariposa» | vértices en orden incorrecto | reordenar los puntos por el contorno |
| El polígono no aparece | falta `ax.add_patch(poly)` | añadirlo al Axes |
| `ValueError` de shape | `xy` no es `Nx2` | pasar lista de pares `(x, y)` |
| El relleno desaparece con `closed=False` | una figura abierta no encierra área | usar `closed=True` para rellenar |
| Contorno doble en el cierre | se repitió el primer vértice al final | quitarlo y dejar que `closed` cierre |

## Notas relacionadas

- [[Patch]]
- [[concepto_artist]]
- [[ax.add_patch]]
- [[ax.fill]]
- [[Rectangle]]
