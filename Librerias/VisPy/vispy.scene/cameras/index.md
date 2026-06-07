---
title: vispy.scene/cameras — camaras de navegacion
tags:
  - vispy
  - indice
draft: false
---

# vispy.scene/cameras — camaras de navegacion

Las camaras de VisPy determinan **dos cosas a la vez**: como el usuario **interactua** con la escena (que hace el raton y el teclado) y como la escena se **proyecta en pantalla** (perspectiva, ortografica, 2D plana). Cada [[ViewBox]] tiene exactamente una camara activa; cambiarla en tiempo de ejecucion es inmediato.

La camara no es solo una configuracion de proyeccion: define el modelo de interaccion completo. Elegir la camara correcta desde el inicio evita tener que reescribir la logica de navegacion.

## Asignar una camara a un ViewBox

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()

# --- Elegir UNA de las siguientes lineas ---
view.camera = 'panzoom'      # 2D: pan con drag izquierdo, zoom con rueda
view.camera = 'turntable'    # 3D: orbita alrededor de un punto fijo
view.camera = 'fly'          # 3D: movimiento libre tipo FPS

# Ajustar el rango visible inicial (aplica a cualquier camara)
view.camera.set_range(x=(-5, 5), y=(-5, 5), z=(-5, 5))

# Volver a la vista inicial en cualquier momento
view.camera.reset()

app.run()
```

## Como se relacionan — tabla de decision

| Camara | Dimension | Patron de interaccion | Cuando usarla |
|--------|-----------|----------------------|---------------|
| [[PanZoomCamera]] | 2D | Drag = pan \| Rueda = zoom | Imagenes, graficas de senales, datos en coordenadas de pantalla, scatter 2D |
| [[TurntableCamera]] | 3D | Drag izq = orbitar \| Rueda = zoom \| Drag der = pan | Nubes de puntos, mallas, volumenes — inspeccionar un objeto desde fuera |
| [[FlyCamera]] | 3D | WASD = moverse \| Mouse = orientar | Escenas 3D grandes — explorar desde adentro, terrenos, volumenes extensos |

### Reglas de decision rapida

- Tus datos son 2D (senales, imagenes, scatter xy) → **PanZoomCamera**
- Tus datos son 3D y quieres ver el objeto completo desde fuera → **TurntableCamera**
- Tu escena es tan grande que necesitas "entrar" en ella → **FlyCamera**
- Quieres proporciones iguales en x e y (pixeles cuadrados) → **PanZoomCamera** con `aspect=1`
- Quieres proyeccion ortografica 3D (sin perspectiva) → **TurntableCamera** con `fov=0`

## Cambiar la camara en tiempo de ejecucion

```python
# Cambio instantaneo — el ViewBox adopta la nueva camara y sus controles
view.camera = 'turntable'
view.camera.set_range(x=(-5, 5), y=(-5, 5), z=(-5, 5))
```

No es necesario recrear los visuals al cambiar la camara; el scene graph se mantiene intacto.

## Notas

- [[PanZoomCamera]] — camara 2D con pan y zoom
- [[TurntableCamera]] — camara 3D de orbita
- [[FlyCamera]] — camara 3D de movimiento libre tipo FPS

## Notas relacionadas

- [[ViewBox]] — contenedor que aloja la camara
- [[SceneCanvas]] — el canvas padre del ViewBox
- [[Tree VisPy]]
