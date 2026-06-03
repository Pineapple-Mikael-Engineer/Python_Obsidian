---
title: Rectangle — Rectángulo desde la esquina inferior izquierda
aliases:
  - Rectangle
  - patches.Rectangle
  - rectángulo

tags:
  - matplotlib
  - api/clase
  - plot/formas

# --- Clasificación ---
lib: matplotlib
obj: Rectangle
mod: matplotlib.patches
tipo: clase

# --- Comportamiento ---
retorna: Rectangle
muta_estado: false

# --- Dependencias ---
requiere:
  - Patch

draft: false
---

# Rectangle — Rectángulo desde la esquina inferior izquierda

## Definición

`Rectangle` es la forma rectangular de Matplotlib. Se define por su **esquina inferior izquierda** `xy`, más el `width` y el `height` (puede rotarse con `angle`). Es un [[concepto_artist|Artist]] que **no se dibuja solo**: se añade con `ax.add_patch(rect)`. Hereda de la clase base [[Patch]] todas las propiedades de estilo (relleno, borde, alpha, tramado). Se usa típicamente para **resaltar regiones** rectangulares de un gráfico; internamente es la pieza con la que se construyen las barras de `ax.bar`.

## Firma del constructor

```python
from matplotlib.patches import Rectangle

Rectangle(
    xy,                # (x, y) de la ESQUINA INFERIOR IZQUIERDA
    width,             # ancho (puede ser negativo: crece hacia la izquierda)
    height,            # alto (puede ser negativo: crece hacia abajo)
    *,
    angle=0.0,         # rotación en grados, pivota sobre xy
    rotation_point='xy',
    **kwargs           # facecolor, edgecolor, lw, alpha, fill, hatch, zorder (de Patch)
)
```

## Parámetros / propiedades

Propias del rectángulo (las de estilo se heredan de la clase base):

| Propiedad | Setter | Tipo / valores | Descripción |
|-----------|--------|----------------|-------------|
| xy | `set_xy((x, y))` | tupla | esquina inferior izquierda |
| width | `set_width(w)` | float | ancho (negativo = hacia la izquierda) |
| height | `set_height(h)` | float | alto (negativo = hacia abajo) |
| angle | `set_angle(a)` | float (grados) | rotación sobre `rotation_point` |
| facecolor | `set_facecolor(c)` | color / `'none'` | relleno (heredado de Patch) |
| edgecolor | `set_edgecolor(c)` | color / `'none'` | borde (heredado) |
| linewidth | `set_linewidth(w)` | float | grosor del borde (`lw`) |
| alpha | `set_alpha(a)` | float 0..1 | transparencia |
| fill | `set_fill(b)` | `True`/`False` | si `False`, solo contorno |
| hatch | `set_hatch(s)` | `'/'`, `'x'`, ... | patrón de tramado |
| zorder | `set_zorder(z)` | float | orden de dibujo |

```python
rect.get_xy()        # → (0.2, 0.2)
rect.get_width()     # → 0.5
```

## Cómo añadirlo al Axes

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots()
rect = Rectangle((0.2, 0.2), 0.5, 0.3,
                 facecolor='lightblue', edgecolor='navy', lw=2)
ax.add_patch(rect)        # ← sin esto el rectángulo no aparece
plt.show()
```

## Casos de uso

### Resaltar una región de interés

```python
ax.plot(x, y)
banda = Rectangle((2, 0), 3, 10,          # de x=2 a x=5, de y=0 a y=10
                  facecolor='yellow', alpha=0.3)
ax.add_patch(banda)        # zona destacada translúcida bajo la curva
```

### Marco sin relleno (solo borde)

```python
marco = Rectangle((0.1, 0.1), 0.8, 0.8,
                  fill=False, edgecolor='red', lw=2, ls='--')
ax.add_patch(marco)        # recuadro vacío, no tapa el contenido
```

### Rectángulo rotado

```python
r = Rectangle((0.5, 0.5), 0.4, 0.2, angle=30, facecolor='salmon')
ax.add_patch(r)            # girado 30° sobre su esquina (0.5, 0.5)
```

## Buenas prácticas

1. Recuerda que `xy` es la **esquina inferior izquierda**, no el centro (a diferencia de `Circle` o `Ellipse`).
2. Para resaltar bandas verticales/horizontales que abarcan todo el eje, valora `ax.axvspan` / `ax.axhspan` antes que `Rectangle`.
3. Usa `alpha` bajo en regiones de resalte para no ocultar los datos.
4. Reutiliza el patch con `set_width`/`set_height` en animaciones en lugar de recrearlo.
5. Combina `fill=False` con un `edgecolor` visible para marcos limpios.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El rectángulo aparece descentrado | `xy` es la esquina, no el centro | restar `width/2`, `height/2` al centro deseado |
| No se ve nada | falta `ax.add_patch(rect)` | añadirlo al Axes |
| Rectángulo fuera de vista | límites de ejes no abarcan la forma | `ax.set_xlim` / `ax.set_ylim` o `ax.autoscale()` |
| Borde invisible | `linewidth=0` o `edgecolor='none'` | fijar `lw>0` y un `edgecolor` |
| Rota sobre el punto equivocado | `rotation_point` por defecto es `'xy'` | pasar `rotation_point='center'` |

## Notas relacionadas

- [[Patch]]
- [[concepto_artist]]
- [[ax.add_patch]]
- [[ax.bar]]
- [[Polygon]]
