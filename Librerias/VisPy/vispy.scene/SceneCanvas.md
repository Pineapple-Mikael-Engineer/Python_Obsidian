---
title: SceneCanvas — canvas con scene graph integrado
aliases: [SceneCanvas]
tags: [vispy, api/clase, scene]
lib: vispy
mod: vispy.scene
tipo: clase
retorna: SceneCanvas
requiere: [vispy.use]
draft: false
---

# SceneCanvas — canvas con scene graph integrado

`SceneCanvas` es el canvas de alto nivel de VisPy: gestiona automaticamente un **scene graph** completo, el ciclo de redibujado y la interaccion del usuario. Es el punto de entrada para el 95 % de los casos de uso con la API `scene`. A diferencia de [[Canvas]] (bajo nivel, `vispy.app`), no necesitas implementar `on_draw` manualmente: el scene graph se renderiza automaticamente cuando cambias cualquier visual.

## Importacion

```python
import vispy
vispy.use('pyqt5')           # seleccionar backend antes de crear la ventana
from vispy import scene, app

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
```

## Constructor / Firma

```python
scene.SceneCanvas(
    title='VisPy canvas',
    size=(800, 600),
    keys=None,           # 'interactive' habilita esc=cerrar, +/-=zoom, etc.
    show=False,          # mostrar la ventana al crear
    bgcolor='black',     # color de fondo; nombre CSS, hex o tuple RGBA
)
```

## Parametros clave

| Parametro | Tipo | Default | Descripcion |
|-----------|------|---------|-------------|
| `title` | `str` | `'VisPy canvas'` | Titulo de la ventana |
| `size` | `tuple[int,int]` | `(800, 600)` | Ancho x alto en pixels |
| `keys` | `str \| None` | `None` | `'interactive'` activa shortcuts de teclado |
| `show` | `bool` | `False` | Llamar `.show()` automaticamente al construir |
| `bgcolor` | `str \| tuple` | `'black'` | Color de fondo de la ventana |

### `keys='interactive'` — shortcuts activos

| Tecla | Accion |
|-------|--------|
| `Esc` | Cerrar ventana |
| `+` / `-` | Zoom in/out |
| `0` | Reset camara |
| `s` | Captura de pantalla |

## Atributos principales

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| `.scene` | `Node` | Nodo raiz del scene graph; padre de todos los visuals globales |
| `.central_widget` | `Widget` | Widget que llena todo el canvas; punto de partida para layouts |
| `.size` | `tuple` | Tamano actual `(width, height)` en pixels |
| `.bgcolor` | `Color` | Color de fondo; asignable: `canvas.bgcolor = 'white'` |

## Casos de uso

### Patron minimo — un solo viewport

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()   # devuelve un ViewBox
view.camera = 'turntable'

pos = np.random.randn(500, 3).astype('float32')
scatter = scene.visuals.Markers(parent=view.scene)
scatter.set_data(pos, face_color='white', size=4)

app.run()
```

`canvas.central_widget.add_view()` crea un [[ViewBox]] que ocupa todo el canvas y lo devuelve listo para recibir una camara y visuals.

### Multiples ViewBox con grid (subplots)

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(1000, 500))
grid = canvas.central_widget.add_grid()   # layout de cuadricula

v1 = grid.add_view(row=0, col=0)   # columna izquierda
v2 = grid.add_view(row=0, col=1)   # columna derecha

v1.camera = 'panzoom'
v2.camera = 'turntable'

# visual en v1 (2D)
t = np.linspace(0, 2 * np.pi, 200).astype('float32')
pos2d = np.column_stack([t, np.sin(t)]).astype('float32')
scene.visuals.Line(pos2d, color='cyan', parent=v1.scene)

# visual en v2 (3D)
pos3d = np.random.randn(300, 3).astype('float32')
m = scene.visuals.Markers(parent=v2.scene)
m.set_data(pos3d, face_color='orange', size=5)

app.run()
```

### Forzar redibujado en animacion

```python
# dentro de un callback de Timer:
def on_timer(event):
    scatter.set_data(new_pos, face_color='white', size=4)
    canvas.update()   # fuerza el repaint del frame actual
```

`.update()` es necesario cuando los datos cambian fuera del loop de eventos (por ejemplo, en un Timer). En condiciones normales el scene graph se redibuja solo.

## Diferencia con `Canvas` (vispy.app)

| Aspecto | `Canvas` | `SceneCanvas` |
|---------|----------|---------------|
| API | Bajo nivel (`vispy.app`) | Alto nivel (`vispy.scene`) |
| Redibujado | Manual — implementas `on_draw` | Automatico — el scene graph se renderiza solo |
| Visuals | No soportados directamente | `scene.visuals.*` con `parent=view.scene` |
| Camara/interaccion | A mano | Integrada en `ViewBox` |
| Caso de uso tipico | Shaders `gloo` personalizados | Graficas cientificas, scatter, mallas, volumenes |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Ventana negra / nada | `show=False` y no se llamo `.show()` | Usar `show=True` o llamar `canvas.show()` |
| `RuntimeError: no backend` | Backend no instalado o no llamado `vispy.use()` | Instalar `pyqt5`/`pyglet` y llamar `vispy.use(...)` antes |
| Visual no aparece | `parent` incorrecto | Usar `parent=view.scene`, no `parent=canvas.scene` |
| `app.run()` no bloquea | Falta la llamada | Siempre terminar con `app.run()` |

## Metodos y atributos

| Metodo / Atributo | Descripcion |
|-------------------|-------------|
| `.central_widget.add_view()` | Crea y devuelve un [[ViewBox]] que llena el widget |
| `.central_widget.add_grid()` | Devuelve un grid para multiples viewboxes |
| `.update()` | Fuerza un redibujado del canvas |
| `.show()` | Muestra la ventana (si `show=False` en constructor) |
| `.close()` | Cierra y destruye la ventana |
| `.screenshot()` | Captura el frame actual como array NumPy RGBA |

## Notas relacionadas

- [[ViewBox]] — viewport que vive dentro del `central_widget`
- [[vispy.scene/cameras/index\|cameras]] — camaras que se asignan al ViewBox
- [[Canvas]] — alternativa de bajo nivel para uso con `gloo`
- [[Tree VisPy]]
