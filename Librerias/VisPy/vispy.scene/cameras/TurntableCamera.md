---
title: TurntableCamera — camara 3D de orbita
aliases: [TurntableCamera]
tags: [vispy, api/clase, scene]
lib: vispy
mod: vispy.scene.cameras
tipo: clase
retorna: TurntableCamera
requiere: [ViewBox]
draft: false
---

# TurntableCamera — camara 3D de orbita

`TurntableCamera` es la camara **3D de orbita** de VisPy: el usuario gira alrededor de un punto central fijo usando el raton, como si la escena estuviera sobre una plataforma giratoria. Es la camara 3D por defecto y la mas adecuada para nubes de puntos, mallas, volumenes y cualquier objeto que se quiera inspeccionar desde todos los angulos.

## Importacion

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
from vispy.scene.cameras import TurntableCamera

# Opcion A — string shortcut
view.camera = 'turntable'

# Opcion B — instancia con parametros
view.camera = TurntableCamera(fov=45, distance=5, elevation=30, azimuth=45)
```

## Constructor / Firma

```python
TurntableCamera(
    fov=45.0,          # campo de vision en grados; 0 = proyeccion ortografica
    elevation=30.0,    # angulo vertical inicial (grados desde el plano xy)
    azimuth=135.0,     # angulo horizontal inicial (grados)
    roll=0.0,          # rotacion de la camara alrededor de su propio eje
    distance=None,     # distancia al centro; None = auto desde set_range
    center=(0,0,0),    # punto alrededor del cual orbita la camara
    **kwargs,
)
```

## Parametros clave

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| `fov` | `float` | `45.0` | Campo de vision (degrees); `0` = proyeccion ortografica |
| `elevation` | `float` | `30.0` | Angulo vertical respecto al plano horizontal |
| `azimuth` | `float` | `135.0` | Angulo horizontal; 0 = eje +x |
| `distance` | `float \| None` | `None` | Distancia al punto central |
| `center` | `tuple` | `(0,0,0)` | Punto de orbita; cambiarlo desplaza el foco |

## Interaccion con el raton

| Accion | Efecto |
|--------|--------|
| Drag boton izquierdo | Orbitar — cambia `elevation` y `azimuth` |
| Rueda de scroll | Zoom — acercar/alejar |
| Drag boton derecho | Pan — desplaza el punto central |
| Doble click izquierdo | Reset a la vista inicial |

## Casos de uso

### Nube de puntos 3D — patron basico

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'

pos = np.random.randn(1000, 3).astype('float32')
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos, face_color='white', size=4)

view.camera.set_range(x=(-3, 3), y=(-3, 3), z=(-3, 3))

app.run()
```

### Camara con parametros explicitos

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
from vispy.scene.cameras import TurntableCamera
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()

cam = TurntableCamera(
    fov=60,
    elevation=20,
    azimuth=45,
    distance=10,
    center=(0, 0, 0),
)
view.camera = cam

# Malla simple
verts = np.array([
    [-1, -1, 0], [1, -1, 0], [0, 1, 0], [0, 0, 1]
], dtype='float32')
faces = np.array([[0, 1, 2], [0, 1, 3], [1, 2, 3], [0, 2, 3]], dtype='uint32')
colors = np.array([
    [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 0, 1]
], dtype='float32')
scene.visuals.Mesh(vertices=verts, faces=faces, vertex_colors=colors, parent=view.scene)

app.run()
```

### Proyeccion ortografica (fov=0)

```python
cam = TurntableCamera(fov=0, distance=8)   # fov=0 => ortografica
view.camera = cam
```

La proyeccion ortografica es util para comparar tamanios relativos sin distorsion de perspectiva (diagramas tecnicos, datos de ingenieria).

### Cambiar punto de orbita en tiempo de ejecucion

```python
view.camera.center = (2.0, 1.0, 0.5)   # desplazar el foco a otro punto
view.camera.reset()
```

## Metodos utiles

| Metodo / Atributo | Descripcion |
|-------------------|-------------|
| `set_range(x=..., y=..., z=...)` | Ajusta el rango visible y calcula `distance` automaticamente |
| `reset()` | Vuelve a `elevation`, `azimuth` y `distance` iniciales |
| `.elevation` | Angulo vertical actual; asignable directamente |
| `.azimuth` | Angulo horizontal actual; asignable directamente |
| `.fov` | Campo de vision; asignable (0 = ortografica) |

## Diferencia con FlyCamera

| Aspecto | `TurntableCamera` | `FlyCamera` |
|---------|-------------------|-------------|
| Punto de referencia | Orbita alrededor de `center` fijo | Se mueve libremente en el espacio |
| Control | Raton + rueda | WASD + raton |
| Caso tipico | Inspeccionar un objeto desde fuera | Explorar escenas extensas desde dentro |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Escena demasiado pequena | `distance` auto muy grande | Llamar `set_range` con el rango de los datos |
| Orbita salta al mover | `center` no coincide con los datos | Ajustar `center` al centroide de los datos |
| Sin perspectiva | `fov=0` activado | Usar `fov=45` (o cualquier valor > 0) |

## Notas relacionadas

- [[ViewBox]] — contenedor donde se asigna la camara
- [[PanZoomCamera]] — alternativa 2D
- [[FlyCamera]] — alternativa 3D de movimiento libre
- [[vispy.scene/cameras/index\|cameras]] — tabla de decision entre camaras
- [[Tree VisPy]]
