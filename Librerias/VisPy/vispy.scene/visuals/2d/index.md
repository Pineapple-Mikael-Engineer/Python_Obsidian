---
title: vispy.scene/visuals/2d — visuals 2D de alto nivel
tags:
  - vispy
  - indice
draft: false
---

# vispy.scene/visuals/2d — visuals 2D de alto nivel

Los visuals 2D son los objetos de dibujo de alto nivel de [[SceneCanvas]] para datos planos:
lineas, puntos dispersos, imagenes y anotaciones de texto. Cada uno encapsula un pipeline
GPU especializado y se integra al scene graph de VisPy mediante `parent=view.scene`.

El patron de uso es uniforme: crear el visual con `parent=view.scene` (o actualizar sus datos
con `.set_data(...)`) y llamar `canvas.update()` cuando el canvas no redibuja automaticamente.
Nunca recrear el visual dentro de un callback de animacion — solo actualizar sus datos.

## Ejemplo unificador — Line + Markers + Text sobre un ViewBox

```python
import vispy; vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
view.camera.set_range(x=(0, 10), y=(-2, 2))

# --- Line: curva continua ---
t = np.linspace(0, 10, 1000)
y = np.sin(t)
pos = np.column_stack([t, y]).astype('float32')
line = scene.visuals.Line(pos=pos, color='cyan', width=2, parent=view.scene)

# --- Markers: resaltar puntos de interes ---
idx = np.arange(0, len(t), 50)
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(
    pos=pos[idx],
    face_color='yellow',
    size=10,
    symbol='o'
)

# --- Text: anotar el maximo ---
i_max = np.argmax(y)
label = scene.visuals.Text(
    'max', pos=(t[i_max], y[i_max]),
    color='white', font_size=12,
    anchor_x='center', anchor_y='bottom',
    parent=view.scene
)

app.run()
```

Todos los visuals comparten el mismo [[ViewBox]]: sus coordenadas viven en el mismo espacio
de datos y responden juntos al pan/zoom de la camara `panzoom`.

## Clases que aporta

Cada clase es un **VisualNode** (Node + Visual): hereda lo del scene graph (`.parent`,
`.transform`, `.visible`) y lo del dibujo en GPU (`.set_data`, `.update`). La columna
`set_data recibe` resume los args clave de cada una.

| Clase | Hereda de | set_data recibe |
|-------|-----------|-----------------|
| [[Line]] | Node + Visual (VisualNode) | `pos`, `color`, `width`, `connect` |
| [[Markers]] | Node + Visual (VisualNode) | `pos`, `face_color`, `edge_color`, `size`, `symbol` |
| [[Image]] | Node + Visual (VisualNode) | `data` (array `(H,W)` o `(H,W,3/4)`), `cmap`, `clim` |
| [[Text]] | Node + Visual (VisualNode) | `text`, `pos`, `color`, `font_size`, `anchor_x`, `anchor_y` |

Todas comparten `.set_data()`, `.transform` y se montan con `parent=view.scene`.

## Como se relacionan

Tabla de decision: que visual usar segun el tipo de dato.

| Dato a visualizar | Visual recomendado | Alternativa |
|-------------------|--------------------|-------------|
| Funcion o trayectoria continua | [[Line]] | — |
| Serie de puntos / scatter | [[Markers]] | [[Line]] con `connect='segments'` |
| Array 2D (mapa de calor, imagen) | [[Image]] | — |
| Etiqueta o anotacion de texto | [[Text]] | — |
| Grafica completa con ejes | [[Line]] + [[Text]] manual | `scene.visuals.Axis` (pendiente) |
| >100 k puntos | [[Markers]] (GPU) | evitar Matplotlib |

### Patron de animacion (todos los visuals)

```python
def on_timer(event):
    # Actualizar solo datos — NO recrear el visual
    line.set_data(pos=nuevo_pos)
    scatter.set_data(pos=nuevos_puntos, face_color='yellow', size=10)
    label.text = f't = {event.elapsed:.2f}'
    canvas.update()   # forzar redibujo

timer = app.Timer(interval=1/60, connect=on_timer, start=True)
```

## Notas

- [[Line]] — lineas continuas o segmentos; `connect='strip'` / `'segments'`; `method='gl'` o `'agg'`
- [[Markers]] — scatter de puntos y simbolos; `.set_data()` es la interfaz principal
- [[Image]] — textura 2D en GPU desde array `(H, W)` escalar o `(H, W, 3/4)` RGB/RGBA
- [[Text]] — etiquetas con posicion en coordenadas de escena; soporta N strings con N posiciones

## Notas relacionadas

- [[ViewBox]]
- [[SceneCanvas]]
- [[Tree VisPy]]
