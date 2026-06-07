---
title: get_colormap — obtener un colormap por nombre en VisPy
aliases:
  - get_colormap
  - vispy colormap
tags:
  - vispy
  - api/funcion
  - color
lib: vispy
mod: vispy.color
tipo: funcion
retorna: Colormap
requiere: []
draft: false
---

# get_colormap — obtener un colormap por nombre en VisPy

`get_colormap(name)` devuelve un objeto `Colormap` que transforma valores escalares en el rango 0–1 a colores RGBA. Es el puente entre **datos numericos** y **colores visuales**: tomar un array de floats y obtener un array `(N, 4)` para pasarlo directamente a [[Markers]], [[Image]] u otros visuals.

## Importacion

```python
from vispy.color import get_colormap, get_colormaps
```

## Firma

```python
get_colormap(name)          # -> Colormap
get_colormaps()             # -> dict con todos los colormaps disponibles
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `name` | `str` | Nombre del colormap (ver tabla de disponibles) |

El objeto `Colormap` resultante se llama con `.map(values)`:

```python
cmap = get_colormap('viridis')
rgba = cmap.map(values)   # values: array float32, rango [0, 1] → (N, 4) float32
```

## Colormaps disponibles

| Nombre | Descripcion |
|--------|-------------|
| `'fire'` | Negro → rojo → amarillo → blanco (intensidad) |
| `'grays'` | Negro → blanco (escala de grises) |
| `'hot'` | Negro → rojo → naranja → amarillo (termico) |
| `'cool'` | Cian → magenta |
| `'viridis'` | Azul → verde → amarillo (perceptualmente uniforme) |
| `'inferno'` | Negro → violeta → naranja → blanco |
| `'plasma'` | Azul → magenta → amarillo |
| `'rainbow'` | Espectro completo (no perceptualmente uniforme) |
| `'bipolar'` | Azul → blanco → rojo (para datos con cero central) |

Para listar todos los disponibles en la instalacion actual:

```python
from vispy.color import get_colormaps
print(list(get_colormaps().keys()))
```

## Casos de uso

### Mapeo basico de datos escalares

```python
import numpy as np
from vispy.color import get_colormap

cmap = get_colormap('fire')
vals = np.linspace(0, 1, 5).astype('float32')
rgba = cmap.map(vals)
print(rgba)
# array de shape (5, 4), dtype float32
# cada fila es [R, G, B, A] para el valor correspondiente
```

### Normalizar datos fuera del rango [0, 1]

Los valores deben estar en `[0, 1]` antes de llamar a `.map()`. Normalizar con `np.interp` o manualmente:

```python
import numpy as np
from vispy.color import get_colormap

data = np.array([2.5, 7.1, 3.8, 9.0, 1.2], dtype='float32')

# Normalizar al rango [0, 1]
vmin, vmax = data.min(), data.max()
vals_norm = ((data - vmin) / (vmax - vmin)).astype('float32')

cmap = get_colormap('viridis')
colors = cmap.map(vals_norm)   # (5, 4)
```

### Uso tipico: datos → colores → Markers

Patron mas comun: mapear 1000 mediciones a colores para un scatter plot.

```python
import vispy
vispy.use('pyqt5')

import numpy as np
from vispy import scene
from vispy.color import get_colormap

n = 1000
pos = np.random.rand(n, 2).astype('float32') * 10
data_values = np.random.rand(n).astype('float32')   # ya en [0, 1]

cmap = get_colormap('plasma')
colors = cmap.map(data_values)   # (1000, 4) float32

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
view.camera.set_range(x=(0, 10), y=(0, 10))

markers = scene.visuals.Markers(
    pos=pos,
    face_color=colors,   # (N, 4)
    size=6,
    parent=view.scene
)

from vispy import app
app.run()
```

### Uso con Image (mapa de calor)

```python
import vispy
vispy.use('pyqt5')

import numpy as np
from vispy import scene

# Image acepta el nombre del colormap directamente como string
data = np.random.rand(64, 64).astype('float32')

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'panzoom'

image = scene.visuals.Image(
    data,
    cmap='fire',        # nombre de colormap como string
    clim=(0.0, 1.0),
    parent=view.scene
)

from vispy import app
app.run()
```

> [!info] `cmap` como string vs objeto
> Muchos visuals de VisPy (`Image`, `Volume`) aceptan el nombre del colormap directamente como string en el parametro `cmap`. `get_colormap` es util cuando se necesita el objeto para llamar a `.map()` explicitamente, por ejemplo al construir un `ColorArray` o al generar colores fuera de un visual.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `KeyError: 'nombre'` | Nombre de colormap incorrecto | Verificar con `list(get_colormaps().keys())` |
| Output `NaN` o colores negros | Valores fuera del rango `[0, 1]` | Normalizar antes de llamar a `.map()` |
| dtype error en `.map()` | Array no es `float32` | Convertir con `.astype('float32')` |

## Notas relacionadas

- [[Color]] — cuando se necesita un unico color (no un mapeo)
- [[ColorArray]] — para construir un array de colores desde una lista explicita
- [[Markers]] — visual que acepta `face_color` como array `(N, 4)` producido por `.map()`
- [[Image]] — acepta `cmap` como string; usa colormap internamente
