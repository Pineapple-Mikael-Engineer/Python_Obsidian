---
title: vispy.scene/visuals — visuals de alto nivel
tags:
  - vispy
  - indice
draft: false
---

# vispy.scene/visuals — visuals de alto nivel

Los **visuals** son los objetos de dibujo de `vispy.scene`: se crean con Python,
se asignan a un `ViewBox` mediante `parent=view.scene`, y VisPy los renderiza
en GPU automaticamente. No hay que escribir ningun shader.

Hay dos familias segun la dimension de los datos:

- **2D** (`vispy.scene/visuals/2d/`): datos planos — lineas, puntos, imagenes, texto.
  Usar con `PanZoomCamera`.
- **3D** (`vispy.scene/visuals/3d/`): geometria volumetrica — mallas, volumenes, superficies.
  Usar con `TurntableCamera` o `FlyCamera`.

## Patron universal de uso

```python
import vispy; vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'panzoom'   # o 'turntable' para 3D

# Crear visual y asignarlo al scene
line = scene.visuals.Line(pos=..., color='cyan', parent=view.scene)
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos=..., face_color='yellow', size=6)

app.run()
```

> [!warning] Siempre `parent=view.scene`
> Los visuals DEBEN tener `parent=view.scene` para aparecer en el viewport correcto.
> Usar `.add()` directamente en el ViewBox no funciona para visuals.

## Como se relacionan

| Tipo de dato | Visual recomendado | Camara |
|--------------|-------------------|--------|
| Curva o trayectoria | [[Line]] | PanZoomCamera |
| Nube de puntos 2D/3D | [[Markers]] | PanZoom / Turntable |
| Array 2D o imagen | [[Image]] | PanZoomCamera |
| Etiquetas de texto | [[Text]] | cualquiera |
| Malla triangular 3D | [[Mesh]] | TurntableCamera |
| Datos volumetricos (CT, MRI) | [[Volume]] | TurntableCamera |
| Superficie z=f(x,y) | [[Surface]] | TurntableCamera |

## Actualizacion en animacion

Para todos los visuals, el patron de animacion es identico:

```python
timer = app.Timer('auto', start=True)

@timer.connect
def on_timer(event):
    new_pos = ...                       # calcular nuevos datos
    visual.set_data(new_pos, ...)       # actualizar sin recrear
    canvas.update()                     # forzar redibujado
```

Nunca recrear el visual dentro del callback; solo llamar `.set_data()`.

## Notas

### Visuals 2D

- [[vispy.scene/visuals/2d/index|2D]] — hub de la subcarpeta
  - [[Line]] — lineas y curvas; `pos`, `color`, `width`, `connect`
  - [[Markers]] — scatter de puntos/simbolos; `symbol`, `size`, `face_color`
  - [[Image]] — textura 2D desde array numpy; `cmap`, `clim`
  - [[Text]] — etiquetas; `font_size`, `anchor_x`, `anchor_y`

### Visuals 3D

- [[vispy.scene/visuals/3d/index|3D]] — hub de la subcarpeta
  - [[Mesh]] — malla triangular; `vertices`, `faces`, `vertex_colors`, `shading`
  - [[Volume]] — render volumetrico; `method`, `cmap`, `clim`
  - [[Surface]] — superficie z=f(x,y) en grid regular; `shading`

## Notas relacionadas

- [[ViewBox]]
- [[SceneCanvas]]
- [[vispy.color/index|vispy.color]] — colormaps y ColorArray para colorear visuals
- [[concepto_scene_graph]]
