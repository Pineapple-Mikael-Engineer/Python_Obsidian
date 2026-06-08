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

## La clase base: Visual + Node

Cada `scene.visuals.X` es un **VisualNode**: una combinacion de DOS bases que se fusionan
en una sola clase mediante `create_visual_node`. Por eso un `scene.visuals.Line` tiene a la
vez `.parent`/`.transform` (de Node) Y `.set_data()` (de Visual).

- Lado **Node** → el visual vive en el scene graph: `.parent`, `.children`, `.transform`,
  `.transforms`, `.visible`.
- Lado **Visual** → el visual sabe dibujarse en GPU: `.set_data(...)`, `.attach()`,
  `.draw()`, `.update()`, los shaders internos.

La jerarquia del lado dibujo (los `Visual` base) es:

```
BaseVisual
└── Visual
     ├── LineVisual        → scene.visuals.Line
     ├── MarkersVisual     → scene.visuals.Markers
     ├── ImageVisual       → scene.visuals.Image
     ├── TextVisual        → scene.visuals.Text
     ├── MeshVisual        → scene.visuals.Mesh
     ├── VolumeVisual      → scene.visuals.Volume
     └── CompoundVisual    → (varios visuals combinados; ej. SurfacePlot, Axis)
```

En `scene.visuals`, cada uno de esos `Visual` base se envuelve junto con `Node` para
producir el `VisualNode` que realmente se usa. Asi un mismo objeto se posiciona en el
arbol (Node) y se renderiza en GPU (Visual) sin escribir shaders.

## Metodos que comparten todos los visuals

Como todo `scene.visuals.X` hereda de Node + Visual, comparten esta interfaz comun
(cada visual ademas anade sus propios args en `.set_data`):

| Metodo/atributo | Viene de | Que hace |
|-----------------|----------|----------|
| `.set_data(...)` | Visual | Actualizar los datos SIN recrear el objeto; cada visual acepta args distintos |
| `.transform` | Visual | Posicionar, escalar o rotar el visual en el espacio |
| `.update()` | Visual | Marcar el visual como sucio para forzar redibujado |
| `.attach(filter)` | Visual | Adjuntar un filtro/efecto al pipeline GPU del visual |
| `.parent` | Node | Donde vive en el arbol; siempre `parent=view.scene` |
| `.children` | Node | Visuals hijos colgados de este nodo |
| `.transforms` | Node | Cadena de transforms acumulada por el scene graph |
| `.visible` | Node | Mostrar u ocultar el visual sin destruirlo |
| `.order` | Node | Orden de dibujado relativo entre hermanos |

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
