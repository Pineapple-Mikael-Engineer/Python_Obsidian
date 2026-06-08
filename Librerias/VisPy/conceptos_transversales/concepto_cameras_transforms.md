---
title: concepto_cameras_transforms — Camaras y transformaciones en vispy.scene
aliases: [camaras vispy, PanZoomCamera, TurntableCamera, STTransform vispy]
tags: [vispy, api/concepto, fundamentos]
lib: vispy
mod: vispy.scene
tipo: concepto
draft: false
---

# Camaras y transformaciones en vispy.scene

Una camara en VisPy define como se proyecta la escena 3D sobre el canvas 2D: determina el
punto de vista, el zoom, el tipo de proyeccion (ortografica o perspectiva) y que eventos
de mouse/teclado controlan la navegacion. Las transformaciones (`STTransform`,
`MatrixTransform`) posicionan visuals en el espacio del scene graph. Elegir la camara
correcta es la decision mas rapida para que una visualizacion sea util.

## La idea central

Cada `ViewBox` tiene exactamente una camara. Se asigna con `view.camera = 'nombre'` (string
de atajo) o con una instancia explicitica. Las camaras responden automaticamente a eventos
de mouse y teclado sin codigo adicional. Para ajustar el zoom inicial se usa
`view.camera.set_range()`.

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'               # orbitar en 3D con el mouse

pts = np.random.randn(300, 3).astype('float32')
scene.visuals.Markers(parent=view.scene).set_data(pts, face_color='cyan', size=5)

view.camera.set_range()                 # ajustar zoom para ver todos los puntos
app.run()
```

## Como funciona

### Las tres camaras principales

| Camara | Atajo string | Proyeccion | Interaccion |
|--------|-------------|------------|-------------|
| `PanZoomCamera` | `'panzoom'` | Ortografica 2D | Drag = pan \| Rueda = zoom |
| `TurntableCamera` | `'turntable'` | Perspectiva 3D | Drag = orbitar \| Rueda = zoom |
| `FlyCamera` | `'fly'` | Perspectiva 3D | WASD = mover \| Mouse = apuntar |

### PanZoomCamera — datos 2D

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'                 # camara 2D

x = np.linspace(0, 4 * np.pi, 500).astype('float32')
y = np.sin(x).astype('float32')
pos = np.column_stack([x, y])
scene.visuals.Line(pos=pos, color='lime', parent=view.scene)

# set_range define el rango visible inicial (coordenadas del scene)
view.camera.set_range(x=(0, 4 * np.pi), y=(-1.2, 1.2))
app.run()
```

### TurntableCamera — datos 3D con orbita

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()

# Instancia explicita para configurar parametros
cam = scene.cameras.TurntableCamera(elevation=30, azimuth=45, fov=60)
view.camera = cam

# Helicoide 3D
t = np.linspace(0, 4 * np.pi, 500).astype('float32')
pos = np.column_stack([np.cos(t), np.sin(t), t / (4 * np.pi)])
scene.visuals.Line(pos=pos, color='orange', parent=view.scene)

view.camera.set_range()
app.run()
```

### FlyCamera — navegacion libre tipo FPS

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'fly'                     # WASD para moverse, mouse para apuntar

pts = np.random.randn(1000, 3).astype('float32') * 5
scene.visuals.Markers(parent=view.scene).set_data(pts, face_color='white', size=3)
app.run()
```

### Transformaciones: posicionar visuals en el espacio

Las transformaciones se asignan al atributo `transform` de cualquier nodo. Se propagan
en cascada: la transformacion de un nodo padre se compone con la de sus hijos.

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
from vispy.visuals.transforms import STTransform, MatrixTransform
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'

pos = np.array([[0, 0], [1, 0], [0.5, 1], [0, 0]], dtype='float32')

# Visual 1: sin transformacion — triangulo en el origen
line1 = scene.visuals.Line(pos=pos, color='cyan', parent=view.scene)

# Visual 2: trasladado (3, 0) y escalado x2 en Y
line2 = scene.visuals.Line(pos=pos, color='magenta', parent=view.scene)
line2.transform = STTransform(scale=(1, 2), translate=(3, 0))

view.camera.set_range(x=(-0.5, 5.5), y=(-0.5, 2.5))
app.run()
```

`MatrixTransform` permite rotaciones y transformaciones arbitrarias con una matriz 4x4:

```python
from vispy.visuals.transforms import MatrixTransform
import numpy as np

mt = MatrixTransform()
mt.rotate(45, (0, 0, 1))   # rotar 45 grados alrededor del eje Z
mt.translate((2, 0, 0))    # luego trasladar
# visual.transform = mt
```

## Casos de uso

### Caso 1: fijar el aspecto de la camara 2D

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()

# aspect=1 mantiene la relacion de aspecto: un circulo se ve circular
cam = scene.cameras.PanZoomCamera(aspect=1)
view.camera = cam

theta = np.linspace(0, 2 * np.pi, 200).astype('float32')
pos = np.column_stack([np.cos(theta), np.sin(theta)])
scene.visuals.Line(pos=pos, color='yellow', parent=view.scene)

view.camera.set_range(x=(-1.5, 1.5), y=(-1.5, 1.5))
app.run()
```

### Caso 2: camara programatica (sin interaccion de usuario)

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
cam = scene.cameras.TurntableCamera(elevation=45, azimuth=30, distance=5)
view.camera = cam

# Rotar la camara en cada frame
t = [0.0]

def update(event):
    t[0] += 0.5
    cam.azimuth = t[0] % 360
    canvas.update()

timer = app.Timer(interval=1/30, connect=update, start=True)

pts = np.random.randn(500, 3).astype('float32')
scene.visuals.Markers(parent=view.scene).set_data(pts, face_color='lime', size=4)
app.run()
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El scene se ve vacio al arrancar | `set_range()` no se llamo y la camara apunta al origen con zoom por defecto | Llamar `view.camera.set_range()` despues de agregar visuals |
| La escena 3D se ve plana | Se uso `'panzoom'` para datos 3D | Cambiar a `'turntable'` o `'fly'` |
| El circulo se ve como elipse | `PanZoomCamera` sin `aspect=1` | Crear `PanZoomCamera(aspect=1)` |
| La camara no responde al mouse | El canvas no tiene `keys='interactive'` | Pasar `keys='interactive'` al crear el `SceneCanvas` |
| `set_range()` no tiene efecto | Se llamo antes de agregar los visuals | Llamar `set_range()` despues de agregar todos los visuals |

## Notas relacionadas

- [[concepto_scene_graph]] — el ViewBox que contiene la camara
- [[concepto_canvas_app]] — el event loop que procesa los eventos de mouse/teclado
- [[concepto_gloo_pipeline]] — nivel inferior donde no hay camaras automaticas
- [[Tree VisPy]]
