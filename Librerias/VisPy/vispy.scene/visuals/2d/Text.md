---
title: Text — etiquetas y anotaciones de texto
aliases: [Text, vispy text, etiqueta vispy]
tags: [vispy, api/clase, scene/visuals]
lib: vispy
mod: vispy.scene.visuals
tipo: clase
requiere: [SceneCanvas, ViewBox]
draft: false
---

# Text — etiquetas y anotaciones de texto

Visual para renderizar texto en coordenadas de escena o de pantalla sobre un [[ViewBox]].
Soporta una cadena unica o un array de strings con posiciones correspondientes, lo que lo
hace util para ejes personalizados, etiquetas de puntos y anotaciones dinamicas.

## Importacion

```python
import vispy; vispy.use('pyqt5')
from vispy import scene, app
import numpy as np
```

## Constructor / Firma

```python
scene.visuals.Text(
    text=None,          # str o lista de str
    color='white',      # string CSS o tuple RGBA
    bold=False,
    italic=False,
    face='OpenSans',    # fuente (OpenSans disponible sin instalacion extra)
    font_size=12.0,     # tamano en puntos
    pos=(0, 0, 0),      # (x, y) o (x, y, z), o array (N, 2/3) para N etiquetas
    rotation=0.0,       # angulo en grados (antihorario)
    anchor_x='center',  # 'left' | 'center' | 'right'
    anchor_y='center',  # 'top' | 'center' | 'bottom' | 'baseline'
    parent=None,
)
```

## Parametros clave

### `text` y `pos` — uso individual vs multiple

| Caso | `text` | `pos` | Notas |
|------|--------|-------|-------|
| Etiqueta unica | `'Hola'` | `(5, 2)` | la mas comun |
| N etiquetas | `['A', 'B', 'C']` | array `(3, 2)` | una posicion por string |

```python
# N etiquetas con N posiciones
labels = ['P1', 'P2', 'P3']
posiciones = np.array([[1, 0], [3, 1], [5, -1]], dtype='float32')
texto = scene.visuals.Text(text=labels, pos=posiciones, color='white',
                           font_size=10, anchor_x='center', parent=view.scene)
```

### `anchor_x` / `anchor_y`

Controlan el punto de anclaje del texto respecto a `pos`:

| `anchor_x` | Significado |
|------------|-------------|
| `'left'` | `pos` = borde izquierdo del texto |
| `'center'` | `pos` = centro horizontal |
| `'right'` | `pos` = borde derecho |

| `anchor_y` | Significado |
|------------|-------------|
| `'top'` | `pos` = borde superior |
| `'center'` | `pos` = centro vertical |
| `'baseline'` | `pos` = linea base tipografica |
| `'bottom'` | `pos` = borde inferior |

### `font_size`

En puntos tipograficos. El tamano final en pantalla depende del DPI y de la camara.
Para texto de UI (tamano fijo en pantalla) usar el sistema de coordenadas de canvas, no
de escena.

## Casos de uso

### Etiqueta estatica

```python
canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
view.camera.set_range(x=(0, 10), y=(-2, 2))

label = scene.visuals.Text(
    'Maximo', pos=(5, 1), color='yellow',
    font_size=14, anchor_x='center', anchor_y='bottom',
    parent=view.scene
)
app.run()
```

### Etiquetas para scatter plot

```python
N = 5
pos_pts = np.random.rand(N, 2).astype('float32') * 10
nombres = [f'P{i}' for i in range(N)]

markers = scene.visuals.Markers(parent=view.scene)
markers.set_data(pos=pos_pts, face_color='cyan', size=8)

etiquetas = scene.visuals.Text(
    text=nombres, pos=pos_pts, color='white',
    font_size=10, anchor_x='left', anchor_y='bottom',
    parent=view.scene
)
```

### Actualizar texto en animacion

Las propiedades `.text` y `.pos` son asignables directamente:

```python
def on_timer(event):
    valor = np.sin(event.elapsed)
    label.text = f'y = {valor:.3f}'   # actualizar cadena
    label.pos = (event.elapsed % 10, valor)  # mover posicion
    canvas.update()

timer = app.Timer(interval=1/30, connect=on_timer, start=True)
```

## Metodos y atributos

| Miembro | Descripcion |
|---------|-------------|
| `.text` | propiedad asignable — string o lista de strings |
| `.pos` | propiedad asignable — posicion o array de posiciones |
| `.color` | propiedad asignable |
| `.font_size` | propiedad asignable |
| `.rotation` | angulo de rotacion en grados |
| `.visible` | bool |
| `.parent` | nodo padre en el scene graph |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|---------|
| Texto no visible | color igual al fondo | usar `color='white'` o contrastar |
| Texto muy pequeno al hacer zoom | font_size en coordenadas de escena | ajustar font_size o usar `pos` en coords de canvas |
| N strings != N posiciones | longitudes distintas | verificar `len(text) == len(pos)` |
| Texto fuera de viewport | anchor mal configurado | probar `anchor_x='center', anchor_y='center'` |

## Notas relacionadas

- [[Line]]
- [[Markers]]
- [[ViewBox]]
- [[vispy.scene/visuals/2d/index\|Visuals 2D]]
