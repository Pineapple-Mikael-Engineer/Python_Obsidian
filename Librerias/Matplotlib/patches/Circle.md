---
title: Circle — Círculo de centro y radio
aliases:
  - Circle
  - patches.Circle
  - círculo

tags:
  - matplotlib
  - api/clase
  - plot/formas

# --- Clasificación ---
lib: matplotlib
obj: Circle
mod: matplotlib.patches
tipo: clase

# --- Comportamiento ---
retorna: Circle
muta_estado: false

# --- Dependencias ---
requiere:
  - Patch

draft: false
---

# Circle — Círculo de centro y radio

## Definición

`Circle` es la forma circular de Matplotlib: se define por su **centro** `xy` y un `radius`. Es un [[concepto_artist|Artist]] que **no se dibuja solo**: se añade con `ax.add_patch(circ)`. Hereda de la clase base [[Patch]] todas las propiedades de estilo. Detalle clave: el radio está en coordenadas de datos, así que **se ve elíptico si los ejes no tienen la misma escala**; usa `ax.set_aspect('equal')` para que salga realmente redondo.

## Firma del constructor

```python
from matplotlib.patches import Circle

Circle(
    xy,                # (x, y) del CENTRO del círculo
    radius=5,          # radio en coordenadas de datos
    **kwargs           # facecolor, edgecolor, lw, alpha, fill, hatch, zorder (de Patch)
)
```

## Parámetros / propiedades

| Propiedad | Setter | Tipo / valores | Descripción |
|-----------|--------|----------------|-------------|
| center | `set_center((x, y))` | tupla | centro del círculo |
| radius | `set_radius(r)` | float | radio en unidades de datos |
| facecolor | `set_facecolor(c)` | color / `'none'` | relleno (heredado de Patch) |
| edgecolor | `set_edgecolor(c)` | color / `'none'` | borde (heredado) |
| linewidth | `set_linewidth(w)` | float | grosor del borde (`lw`) |
| alpha | `set_alpha(a)` | float 0..1 | transparencia |
| fill | `set_fill(b)` | `True`/`False` | si `False`, solo contorno |
| hatch | `set_hatch(s)` | `'/'`, `'x'`, ... | patrón de tramado |
| zorder | `set_zorder(z)` | float | orden de dibujo |

```python
circ.get_center()    # → (0.5, 0.5)
circ.get_radius()    # → 0.2
```

## Cómo añadirlo al Axes

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

fig, ax = plt.subplots()
ax.set_aspect('equal')        # ← para que se vea redondo, no ovalado
circ = Circle((0.5, 0.5), 0.2, facecolor='lightcoral', edgecolor='darkred')
ax.add_patch(circ)            # ← imprescindible
plt.show()
```

## Casos de uso

### Marcar un punto con un disco

```python
ax.scatter(px, py)
foco = Circle((px, py), 0.5, facecolor='none', edgecolor='red', lw=2)
ax.add_patch(foco)            # halo alrededor de un punto de interés
```

### Varios círculos en un bucle

```python
for (cx, cy), r in zip(centros, radios):
    ax.add_patch(Circle((cx, cy), r, alpha=0.4))   # se añaden uno a uno
ax.set_aspect('equal')
```

### Círculo de referencia sin relleno

```python
ref = Circle((0, 0), 1.0, fill=False, ls='--', edgecolor='gray')
ax.add_patch(ref)             # círculo unitario punteado
```

## Buenas prácticas

1. Llama a `ax.set_aspect('equal')` siempre que quieras un círculo geométricamente correcto.
2. `xy` es el **centro** (no la esquina, como en `Rectangle`): tenlo presente al posicionar.
3. Recuerda añadirlo con `ax.add_patch`; los límites no se autoajustan al patch, ajusta `xlim`/`ylim` si hace falta.
4. Para resaltar puntos sin tapar, usa `facecolor='none'` y un `edgecolor` visible.
5. Si necesitas un círculo de tamaño fijo en píxeles (independiente del zoom), valora `ax.scatter` con un marcador `'o'` en lugar de `Circle`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El círculo se ve ovalado | escalas de ejes distintas | `ax.set_aspect('equal')` |
| No aparece | falta `ax.add_patch(circ)` | añadirlo al Axes |
| Posición inesperada | se trató `xy` como esquina | `xy` es el **centro** |
| Círculo fuera de vista | límites no abarcan la forma | ajustar `xlim`/`ylim` |
| Tamaño cambia al hacer zoom | el radio está en datos, no en píxeles | usar `scatter` si quieres tamaño en puntos |

## Notas relacionadas

- [[Patch]]
- [[concepto_artist]]
- [[ax.add_patch]]
- [[Ellipse]]
- [[ax.set_aspect]]
