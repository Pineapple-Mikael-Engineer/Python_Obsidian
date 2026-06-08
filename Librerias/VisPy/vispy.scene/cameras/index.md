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

## Clases que aporta

Todas las camaras son nodos del scene graph: heredan (directa o indirectamente) de
`Node`, asi que viven dentro del `ViewBox` como cualquier otro nodo.

| Clase | Hereda de | Rol |
|-------|-----------|-----|
| `BaseCamera` | `Node` | Base de TODAS las camaras; define `.set_range()`, `.reset()`, `.link()`, `.interactive`, `.center` |
| [[PanZoomCamera]] | `BaseCamera` | Camara 2D: pan + zoom en el plano |
| `PerspectiveCamera` | `BaseCamera` | Base de las camaras 3D; aporta `.fov` (campo de vision) |
| [[TurntableCamera]] | `PerspectiveCamera` | 3D de orbita; `.elevation`, `.azimuth`, `.distance` |
| [[FlyCamera]] | `PerspectiveCamera` | 3D de movimiento libre tipo FPS (WASD) |
| [[ArcballCamera]] | `PerspectiveCamera` | 3D arcball; rotacion tipo bola virtual |

`BaseCamera` y `PerspectiveCamera` no tienen nota propia: son clases base que no se
instancian directamente, pero entender de ellas explica que metodos comparten las demas.

## Herencia y metodos compartidos

```
Node
└── BaseCamera ──► .set_range()  .reset()  .link()  .interactive  .center
    ├── PanZoomCamera                  (2D: pan + zoom)
    └── PerspectiveCamera ──► .fov
         ├── TurntableCamera ──► .elevation .azimuth .distance   (3D orbita)
         ├── FlyCamera                                           (3D libre, WASD)
         └── ArcballCamera                                       (3D arcball)
```

Por que importa:

- Como TODAS heredan de `BaseCamera`, `view.camera.set_range(...)`, `.reset()` y
  `.link(otra_camara)` funcionan igual sin importar cual camara este activa. Por eso
  esos metodos aparecen en los ejemplos de abajo independientes del tipo.
- Las 3D (`Turntable`, `Fly`, `Arcball`) heredan de `PerspectiveCamera`, asi que todas
  comparten `.fov`; ponerlo en `0` da proyeccion ortografica.
- Como cada camara es un `Node`, tiene `.parent` y `.transform` como cualquier visual;
  esa es la base de `.link()` para sincronizar dos vistas.

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

- [[PanZoomCamera]] — camara 2D con pan y zoom; hereda de `BaseCamera`
- [[TurntableCamera]] — camara 3D de orbita; hereda de `PerspectiveCamera`
- [[FlyCamera]] — camara 3D de movimiento libre tipo FPS; hereda de `PerspectiveCamera`
- [[ArcballCamera]] — camara 3D arcball; hereda de `PerspectiveCamera`

## Notas relacionadas

- [[ViewBox]] — contenedor que aloja la camara
- [[SceneCanvas]] — el canvas padre del ViewBox
- [[Tree VisPy]]
