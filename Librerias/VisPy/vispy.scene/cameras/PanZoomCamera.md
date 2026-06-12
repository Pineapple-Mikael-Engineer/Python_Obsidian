---
title: PanZoomCamera — camara 2D con pan y zoom
aliases: [PanZoomCamera]
tags: [vispy, api/clase, scene]
lib: vispy
mod: vispy.scene.cameras
tipo: clase
retorna: PanZoomCamera
requiere: [ViewBox]
draft: false
---

# PanZoomCamera — camara 2D con pan y zoom

`PanZoomCamera` es la camara de navegacion **2D** de VisPy: permite desplazar la vista (pan) arrastrando con el boton izquierdo del raton y hacer zoom con la rueda. Es la camara adecuada para imagenes, graficas de senales, datos en coordenadas de pantalla y cualquier visualizacion plana donde los ejes deben mantener unidades fisicas reales.

## Importacion

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
from vispy.scene.cameras import PanZoomCamera

# Opcion A — string shortcut (configuracion por defecto)
view.camera = 'panzoom'

# Opcion B — instancia con parametros
view.camera = PanZoomCamera(aspect=1)
```

## Constructor / Firma

```python
PanZoomCamera(
    aspect=None,          # None = ejes independientes; 1 = misma escala x/y
    flip=(False, False),  # invertir eje x y/o y
    zoom_factor=1.1,      # factor de zoom por paso de rueda
    **kwargs,             # argumentos de BaseCamera: rect, name...
)
```

## Parametros clave

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| `aspect` | `float \| None` | `None` | `1` = proporciones iguales en x e y (util para imagenes) |
| `flip` | `tuple[bool,bool]` | `(False,False)` | Invertir eje x y/o y; p.ej. `(False,True)` para imagen con origen arriba |
| `zoom_factor` | `float` | `1.1` | Multiplicador de zoom por paso de rueda |

## Interaccion con el raton

| Accion | Efecto |
|--------|--------|
| Drag boton izquierdo | Pan — desplaza la vista |
| Rueda de scroll | Zoom centrado en el cursor |
| Doble click izquierdo | Reset a la vista inicial |

## Casos de uso

### Grafica 2D basica

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
scene.visuals.Line(pos, color='cyan', parent=view.scene)

app.run()
```

### Imagen con proporciones correctas

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(600, 600))
view = canvas.central_widget.add_view()

# aspect=1 para que pixels sean cuadrados; flip y para origen arriba-izquierda
view.camera = 'panzoom'
view.camera.aspect = 1
view.camera.flip = (False, True)

img_data = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)
image = scene.visuals.Image(img_data, parent=view.scene)
view.camera.set_range(x=(0, 256), y=(0, 256))

app.run()
```

### Instancia con parametros personalizados

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
from vispy.scene.cameras import PanZoomCamera
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 400))
view = canvas.central_widget.add_view()

cam = PanZoomCamera(aspect=1, flip=(False, True))
view.camera = cam
view.camera.set_range(x=(0, 100), y=(0, 100))

app.run()
```

## Metodos utiles

| Metodo | Descripcion |
|--------|-------------|
| `set_range(x=(a,b), y=(c,d))` | Define el rango visible inicial |
| `reset()` | Vuelve al rango inicial configurado |
| `zoom(factor, center=None)` | Zoom programatico |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Ejes deformados en imagen | `aspect=None` | Usar `aspect=1` |
| Imagen invertida verticalmente | Coordenadas y de OpenGL | `flip=(False, True)` |
| `set_range` no tiene efecto | Llamado antes de asignar la camara | Asignar camara primero |
| Pan muy rapido/lento | `zoom_factor` muy alto/bajo | Ajustar `zoom_factor` en el constructor |

## Notas relacionadas

- [[ViewBox]] — contenedor donde se asigna la camara
- [[TurntableCamera]] — alternativa 3D para orbitar
- [[FlyCamera]] — alternativa 3D de movimiento libre
- [[vispy.scene/cameras/index\|cameras]] — tabla de decision entre camaras
