---
title: FlyCamera — camara 3D de movimiento libre tipo FPS
aliases: [FlyCamera]
tags: [vispy, api/clase, scene]
lib: vispy
mod: vispy.scene.cameras
tipo: clase
retorna: FlyCamera
requiere: [ViewBox]
draft: false
---

# FlyCamera — camara 3D de movimiento libre tipo FPS

`FlyCamera` es la camara de **movimiento libre** de VisPy: funciona como un juego en primera persona (FPS), permitiendo desplazarse libremente dentro del espacio 3D con el teclado y orientar la camara con el raton. A diferencia de [[TurntableCamera]], no gira alrededor de un punto fijo: la camara se mueve en el espacio y la escena queda detras.

Es la camara adecuada para **explorar escenas extensas desde adentro**: volumenes grandes, terrenos, conjuntos de datos donde el observador debe moverse entre los objetos.

## Importacion

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
from vispy.scene.cameras import FlyCamera

# Opcion A — string shortcut
view.camera = 'fly'

# Opcion B — instancia
view.camera = FlyCamera(fov=60)
```

## Constructor / Firma

```python
FlyCamera(
    fov=60.0,           # campo de vision en grados
    rotation_speed=1.0, # sensibilidad del raton
    speed=1.0,          # velocidad de movimiento con teclado
    **kwargs,
)
```

## Parametros clave

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| `fov` | `float` | `60.0` | Campo de vision; valores tipicos 45–90 |
| `rotation_speed` | `float` | `1.0` | Sensibilidad de rotacion con el raton |
| `speed` | `float` | `1.0` | Velocidad de desplazamiento con WASD |

## Controles de teclado y raton

| Entrada | Efecto |
|---------|--------|
| `W` | Avanzar en la direccion de la camara |
| `S` | Retroceder |
| `A` | Moverse a la izquierda (strafe) |
| `D` | Moverse a la derecha (strafe) |
| `R` | Subir (ascender en Y) |
| `F` | Bajar (descender en Y) |
| Mover raton | Orientar la camara (yaw y pitch) |
| Rueda de scroll | Cambiar velocidad de movimiento |

> [!info] Activar controles de teclado
> El canvas debe crearse con `keys='interactive'` para que los eventos de teclado
> lleguen a la camara: `scene.SceneCanvas(keys='interactive', ...)`.

## Casos de uso

### Exploracion de volumen 3D extenso

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(900, 600))
view = canvas.central_widget.add_view()
view.camera = 'fly'

# Posicion inicial de la camara antes de entrar al volumen
view.camera.set_range(x=(-10, 10), y=(-10, 10), z=(-10, 10))

# Nube densa de puntos simulando un volumen
pos = (np.random.rand(5000, 3).astype('float32') - 0.5) * 20
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos, face_color='lightblue', size=3)

app.run()
```

### Parametros personalizados para escenas grandes

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
from vispy.scene.cameras import FlyCamera
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(1024, 768))
view = canvas.central_widget.add_view()

cam = FlyCamera(fov=75, speed=2.0)   # mas campo de vision y movimiento mas rapido
view.camera = cam

# Escena grande: malla tipo terreno
n = 50
x = np.linspace(-10, 10, n).astype('float32')
y = np.linspace(-10, 10, n).astype('float32')
xx, yy = np.meshgrid(x, y)
zz = np.sin(xx) * np.cos(yy)

# Puntos del terreno
pos = np.column_stack([xx.ravel(), yy.ravel(), zz.ravel()]).astype('float32')
m = scene.visuals.Markers(parent=view.scene)
m.set_data(pos, face_color='green', size=2)

app.run()
```

## Diferencia con TurntableCamera

| Aspecto | `FlyCamera` | `TurntableCamera` |
|---------|-------------|-------------------|
| Tipo de movimiento | Libre en el espacio (FPS) | Orbita alrededor de un punto fijo |
| Control principal | Teclado WASD + raton | Drag de raton |
| Punto de referencia | No existe: la camara se mueve | `center` fijo |
| Ideal para | Explorar desde adentro, escenas grandes | Inspeccionar un objeto desde fuera |
| Desorientacion | Mayor en escenas pequenas | Menor; siempre visible el objeto central |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| WASD no responde | `keys='interactive'` ausente | Crear canvas con `keys='interactive'` |
| Movimiento demasiado lento | Escena muy grande vs `speed=1.0` | Aumentar `speed` en el constructor |
| Camara empieza dentro de un objeto | Posicion inicial mal configurada | Usar `set_range` con los limites de la escena |
| Orientacion confusa | `fov` muy alto | Reducir `fov` a 45–60 grados |

## Metodos utiles

| Metodo / Atributo | Descripcion |
|-------------------|-------------|
| `set_range(x=..., y=..., z=...)` | Posiciona la camara para ver el rango dado |
| `reset()` | Vuelve a la posicion y orientacion iniciales |
| `.fov` | Campo de vision; asignable en tiempo de ejecucion |

## Notas relacionadas

- [[ViewBox]] — contenedor donde se asigna la camara
- [[TurntableCamera]] — alternativa 3D de orbita (mas comun para objetos puntuales)
- [[PanZoomCamera]] — alternativa 2D
- [[vispy.scene/cameras/index\|cameras]] — tabla de decision entre camaras
