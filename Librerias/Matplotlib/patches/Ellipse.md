---
title: Ellipse — Elipse de centro, anchos de ejes y rotación
aliases:
  - Ellipse
  - patches.Ellipse
  - elipse

tags:
  - matplotlib
  - api/clase
  - plot/formas

# --- Clasificación ---
lib: matplotlib
obj: Ellipse
mod: matplotlib.patches
tipo: clase

# --- Comportamiento ---
retorna: Ellipse
muta_estado: false

# --- Dependencias ---
requiere:
  - Patch

draft: false
---

# Ellipse — Elipse de centro, anchos de ejes y rotación

## Definición

`Ellipse` es la forma elíptica de Matplotlib: se define por su **centro** `xy`, el `width` (diámetro total del eje horizontal) y el `height` (diámetro total del eje vertical), con un `angle` opcional de rotación. Es un [[concepto_artist|Artist]] que **no se dibuja solo**: se añade con `ax.add_patch(elip)`. Hereda de la clase base [[Patch]] todas las propiedades de estilo. Un `Circle` es el caso particular con `width == height`; la elipse es la forma general para representar dispersiones, errores o regiones de confianza.

## Firma del constructor

```python
from matplotlib.patches import Ellipse

Ellipse(
    xy,                # (x, y) del CENTRO
    width,             # DIÁMETRO total del eje horizontal (no el semieje)
    height,            # DIÁMETRO total del eje vertical
    *,
    angle=0.0,         # rotación en grados (antihoraria) sobre el centro
    **kwargs           # facecolor, edgecolor, lw, alpha, fill, hatch, zorder (de Patch)
)
```

## Parámetros / propiedades

| Propiedad | Setter | Tipo / valores | Descripción |
|-----------|--------|----------------|-------------|
| center | `set_center((x, y))` | tupla | centro de la elipse |
| width | `set_width(w)` | float | diámetro del eje horizontal |
| height | `set_height(h)` | float | diámetro del eje vertical |
| angle | `set_angle(a)` | float (grados) | rotación antihoraria |
| facecolor | `set_facecolor(c)` | color / `'none'` | relleno (heredado de Patch) |
| edgecolor | `set_edgecolor(c)` | color / `'none'` | borde (heredado) |
| linewidth | `set_linewidth(w)` | float | grosor del borde (`lw`) |
| alpha | `set_alpha(a)` | float 0..1 | transparencia |
| fill | `set_fill(b)` | `True`/`False` | si `False`, solo contorno |
| hatch | `set_hatch(s)` | `'/'`, `'x'`, ... | patrón de tramado |
| zorder | `set_zorder(z)` | float | orden de dibujo |

```python
elip.get_center()    # → (0.5, 0.5)
elip.set_angle(45)   # gira la elipse 45°
```

## Cómo añadirlo al Axes

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

fig, ax = plt.subplots()
elip = Ellipse((0.5, 0.5), width=0.6, height=0.3, angle=30,
               facecolor='plum', edgecolor='purple', lw=2)
ax.add_patch(elip)        # ← imprescindible
plt.show()
```

## Casos de uso

### Marcar una región/cluster de puntos

```python
ax.scatter(xs, ys, s=10)
region = Ellipse((xs.mean(), ys.mean()), width=4, height=2, angle=20,
                 facecolor='none', edgecolor='red', lw=2)
ax.add_patch(region)       # contorno que envuelve el cluster
```

### Elipse de confianza (covarianza)

```python
import numpy as np
vals, vecs = np.linalg.eigh(cov)            # autovalores/autovectores
ang = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
w, h = 2 * np.sqrt(vals)                     # ejes ∝ desviación
elip = Ellipse(media, width=w, height=h, angle=ang, alpha=0.3)
ax.add_patch(elip)         # región de dispersión sobre los datos
```

### Óvalo decorativo rotado

```python
o = Ellipse((0.5, 0.5), 0.8, 0.4, angle=45, facecolor='gold', alpha=0.5)
ax.add_patch(o)
ax.set_aspect('equal')     # respeta la proporción de los ejes
```

## Buenas prácticas

1. Recuerda que `width`/`height` son **diámetros completos**, no semiejes: para semieje `a` pasa `width=2*a`.
2. `xy` es el **centro** de la elipse, igual que en `Circle`.
3. Para que la rotación y la proporción se vean fieles, usa `ax.set_aspect('equal')`.
4. En elipses de confianza, escala los ejes con la desviación (p. ej. `2*sqrt(autovalor)` para ~1σ).
5. Usa `facecolor='none'` cuando solo quieras delimitar una región sin tapar los puntos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| La elipse sale el doble de grande | se pasó el semieje como `width` | `width`/`height` son **diámetros** |
| No aparece | falta `ax.add_patch(elip)` | añadirla al Axes |
| Proporción/ángulo distorsionados | escalas de ejes desiguales | `ax.set_aspect('equal')` |
| Posición desplazada | se usó `xy` como esquina | `xy` es el **centro** |
| Ángulo «al revés» | `angle` es antihorario en grados | ajustar el signo del ángulo |

## Notas relacionadas

- [[Patch]]
- [[concepto_artist]]
- [[ax.add_patch]]
- [[Circle]]
- [[ax.set_aspect]]
