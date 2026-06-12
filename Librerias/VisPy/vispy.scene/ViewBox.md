---
title: ViewBox — viewport con camara y visuals
aliases: [ViewBox]
tags: [vispy, api/clase, scene]
lib: vispy
mod: vispy.scene.widgets
tipo: clase
retorna: ViewBox
requiere: [SceneCanvas]
draft: false
---

# ViewBox — viewport con camara y visuals

`ViewBox` es el **contenedor principal de la API scene**: agrupa una camara, un area de recorte (clipping) y todos los visuals que se renderizan dentro de ese viewport. Casi toda la logica de una app VisPy vive en el ViewBox: se le asigna una camara, se le agregan visuals como hijos de `.scene`, y el redibujado es automatico.

No se instancia directamente; se obtiene via [[SceneCanvas]]:

```python
view = canvas.central_widget.add_view()   # devuelve un ViewBox
```

## Importacion

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
```

## Atributos principales

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| `.camera` | `BaseCamera` | Camara activa; asignable con string o instancia |
| `.scene` | `Node` | Nodo padre de todos los visuals del viewport |
| `.bgcolor` | `Color \| None` | Color de fondo del viewport (independiente del canvas) |
| `.border_color` | `Color \| None` | Color del borde del viewport |

## Asignar camara

Puedes usar un **string shortcut** o una **instancia** con parametros:

```python
# Shortcut — camara con configuracion por defecto
view.camera = 'turntable'   # 3D: orbitar
view.camera = 'panzoom'     # 2D: pan y zoom
view.camera = 'fly'         # 3D: movimiento libre FPS

# Instancia — control total de parametros
from vispy.scene.cameras import TurntableCamera
view.camera = TurntableCamera(fov=45, distance=5, elevation=30, azimuth=45)
```

Despues de asignar la camara, ajusta el rango visible:

```python
view.camera.set_range(x=(-5, 5), y=(-5, 5))          # 2D
view.camera.set_range(x=(-5, 5), y=(-5, 5), z=(-5, 5))  # 3D
```

## Agregar visuals

Todos los visuals deben declarar `parent=view.scene`:

```python
import numpy as np

pos = np.random.randn(500, 3).astype('float32')

scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos, face_color='cyan', size=5)

line_pos = np.column_stack([np.linspace(-3, 3, 100),
                            np.sin(np.linspace(-3, 3, 100)),
                            np.zeros(100)]).astype('float32')
scene.visuals.Line(line_pos, color='yellow', parent=view.scene)
```

> [!warning] `parent` obligatorio
> Nunca uses `.add()` para agregar visuals a un ViewBox. El patron correcto es
> `parent=view.scene` en el constructor del visual o despues con `visual.parent = view.scene`.

## Casos de uso

### Patron completo — 3D

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'
view.camera.set_range(x=(-5, 5), y=(-5, 5), z=(-5, 5))

pos = np.random.randn(1000, 3).astype('float32')
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos, face_color='white', size=3)

app.run()
```

### Patron completo — 2D con rango fijo

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 400))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
view.camera.set_range(x=(0, 10), y=(-1.5, 1.5))

t = np.linspace(0, 10, 500).astype('float32')
pos = np.column_stack([t, np.sin(2 * np.pi * t)]).astype('float32')
scene.visuals.Line(pos, color='lime', parent=view.scene)

app.run()
```

### Multiples ViewBox como subplots

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(1000, 500))
grid = canvas.central_widget.add_grid()

v1 = grid.add_view(row=0, col=0)
v2 = grid.add_view(row=0, col=1)

v1.camera = 'panzoom'
v1.camera.set_range(x=(0, 6), y=(-1.5, 1.5))

v2.camera = 'turntable'

t = np.linspace(0, 6, 300).astype('float32')
scene.visuals.Line(
    np.column_stack([t, np.cos(t)]).astype('float32'),
    color='cyan', parent=v1.scene
)

pos3 = np.random.randn(200, 3).astype('float32')
m = scene.visuals.Markers(parent=v2.scene)
m.set_data(pos3, face_color='orange', size=5)

app.run()
```

## Metodos de camara

| Metodo | Descripcion |
|--------|-------------|
| `view.camera.set_range(x=..., y=..., z=...)` | Ajusta el rango visible inicial |
| `view.camera.reset()` | Vuelve a la vista inicial guardada |
| `view.camera.zoom(factor)` | Aplica un zoom programatico |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Visual fuera del viewport | `parent=canvas.scene` en lugar de `view.scene` | Usar siempre `parent=view.scene` |
| Camara no responde a mouse | `keys='interactive'` no activado en canvas | `scene.SceneCanvas(keys='interactive', ...)` |
| `set_range` sin efecto | Llamado antes de asignar la camara | Asignar camara primero, luego `set_range` |
| Subplots solapados | Grid no configurado | Usar `add_grid()` y `add_view(row=r, col=c)` |

## Notas relacionadas

- [[SceneCanvas]] — el canvas que contiene al ViewBox
- [[PanZoomCamera]] — camara 2D
- [[TurntableCamera]] — camara 3D de orbita
- [[FlyCamera]] — camara 3D de movimiento libre
- [[vispy.scene/cameras/index\|cameras]] — tabla de decision de camaras
