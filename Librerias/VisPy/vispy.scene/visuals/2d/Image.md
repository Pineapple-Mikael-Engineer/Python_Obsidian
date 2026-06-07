---
title: Image — textura 2D desde array numpy
aliases: [Image, vispy image, imagen vispy]
tags: [vispy, api/clase, scene/visuals]
lib: vispy
mod: vispy.scene.visuals
tipo: clase
requiere: [SceneCanvas, ViewBox]
draft: false
---

# Image — textura 2D desde array numpy

Visual que sube un array NumPy 2D o RGB/RGBA a la GPU como textura y lo renderiza en el
[[ViewBox]]. Mucho mas rapido que `imshow` de Matplotlib para imagenes grandes o streams de
video: la transferencia y el renderizado ocurren completamente en GPU.

## Importacion

```python
import vispy; vispy.use('pyqt5')
from vispy import scene, app
import numpy as np
```

## Constructor / Firma

```python
scene.visuals.Image(
    data=None,       # array numpy — ver formas aceptadas
    cmap='grays',    # string de colormap (solo para datos escalares)
    clim='auto',     # (vmin, vmax) o 'auto'
    method='auto',   # 'auto' | 'impostor' | 'subdivide'
    grid=(1, 1),     # subdivision de la textura (raramente necesario)
    parent=None,     # nodo padre
)
```

## Parametros clave

### `data` — formas aceptadas

| Shape | dtype | Interpretacion |
|-------|-------|---------------|
| `(H, W)` | float32 | escalar — se colorea con `cmap` + `clim` |
| `(H, W, 3)` | uint8 o float32 | RGB — `cmap`/`clim` se ignoran |
| `(H, W, 4)` | uint8 o float32 | RGBA — soporte de transparencia |

Para float: rango esperado `[0, 1]` (o definido por `clim`).
Para uint8: rango `[0, 255]`.

```python
# Escalar — se colorea con cmap
data_escalar = np.random.rand(256, 256).astype('float32')

# RGB desde uint8
data_rgb = np.random.randint(0, 255, (256, 256, 3), dtype='uint8')
```

### `cmap`

Solo tiene efecto cuando `data` es escalar `(H, W)`.

| String | Descripcion |
|--------|-------------|
| `'grays'` | escala de grises (defecto para imagenes) |
| `'viridis'` | perceptualmente uniforme, accesible |
| `'fire'` | negro → rojo → amarillo → blanco |
| `'hot'` | similar a fire, mas clasico |
| `'coolwarm'` | divergente — util para campos con signo |

### `clim`

```python
# Mapeo fijo
img = scene.visuals.Image(data, cmap='fire', clim=(0.2, 0.8), parent=view.scene)

# Auto — usa min/max del array
img = scene.visuals.Image(data, clim='auto', parent=view.scene)
```

## Casos de uso

### Mapa de calor

```python
canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'

H, W = 200, 300
data = np.random.rand(H, W).astype('float32')
img = scene.visuals.Image(data, cmap='fire', clim=(0, 1), parent=view.scene)

view.camera.set_range()
app.run()
```

### Stream de video / animacion

```python
from vispy.visuals.transforms import STTransform

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(640, 480))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'

H, W = 480, 640
frame = np.zeros((H, W, 3), dtype='uint8')
img = scene.visuals.Image(frame, parent=view.scene)
view.camera.set_range()

def on_timer(event):
    # Simula nuevo frame — en produccion vendria de una camara
    frame[:] = np.random.randint(0, 255, (H, W, 3), dtype='uint8')
    img.set_data(frame)
    canvas.update()

timer = app.Timer(interval=1/30, connect=on_timer, start=True)
app.run()
```

### Posicionar la imagen con STTransform

Por defecto la imagen se ubica en el origen `(0, 0)` con escala de 1 pixel = 1 unidad.
Para moverla o escalarla, aplicar una transformacion:

```python
from vispy.visuals.transforms import STTransform

img.transform = STTransform(translate=(10, 5), scale=(0.1, 0.1))
```

## Metodos y atributos

| Miembro | Descripcion |
|---------|-------------|
| `.set_data(data)` | sube nuevo array a la textura GPU (sin recrear el visual) |
| `.cmap` | propiedad asignable — cambia colormap en caliente |
| `.clim` | propiedad asignable — `(vmin, vmax)` o `'auto'` |
| `.transform` | transformacion espacial (`STTransform`, `MatrixTransform`…) |
| `.visible` | bool |
| `.parent` | nodo padre en el scene graph |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|---------|
| Imagen en negro | `clim` no cubre el rango del array | ajustar `clim` o usar `'auto'` |
| `cmap` sin efecto | datos RGB/RGBA en lugar de escalar | solo funciona con shape `(H, W)` |
| Imagen muy pequena | escala pixel/unidad | usar `STTransform(scale=...)` |
| Imagen volteada | origen en esquina inferior | aplicar `scale=(1, -1)` o ajustar camara |
| ValueError dtype | uint16 u otros tipos | convertir a float32 o uint8 |

## Notas relacionadas

- [[Text]]
- [[ViewBox]]
- [[SceneCanvas]]
- [[vispy.scene/visuals/2d/index\|Visuals 2D]]
