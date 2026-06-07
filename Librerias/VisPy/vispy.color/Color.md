---
title: Color — color individual en VisPy
aliases:
  - Color
  - vispy color
tags:
  - vispy
  - api/clase
  - color
lib: vispy
mod: vispy.color
tipo: clase
requiere: []
draft: false
---

# Color — color individual en VisPy

`Color` representa un **unico color RGBA** en VisPy. Acepta cualquier forma de especificacion de color (nombre CSS, hex, tupla RGB/RGBA) y expone propiedades para leer el valor en distintos formatos. Es el tipo basico que VisPy espera cuando un argumento `color` acepta un string.

## Importacion

```python
from vispy.color import Color
```

## Constructor / Firma

```python
Color(color='black', alpha=None)
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `color` | `str \| tuple` | Nombre CSS (`'red'`), hex (`'#ff0000'`), tupla RGB `(r, g, b)` o RGBA `(r, g, b, a)` |
| `alpha` | `float \| None` | Sobreescribe el canal alfa; rango 0.0–1.0 |

## Propiedades clave

| Propiedad | Tipo | Descripcion |
|-----------|------|-------------|
| `.rgba` | `np.ndarray` shape `(4,)` float32 | Canal RGBA completo |
| `.rgb` | `np.ndarray` shape `(3,)` float32 | Solo canales RGB |
| `.hex` | `str` | Color en formato hexadecimal (`'#rrggbb'`) |
| `.alpha` | `float` | Canal alfa (0.0 = transparente, 1.0 = opaco) |

## Metodos

| Metodo | Descripcion |
|--------|-------------|
| `.lighter(dv=0.1)` | Devuelve un `Color` mas claro en `dv` unidades |
| `.darker(dv=0.1)` | Devuelve un `Color` mas oscuro en `dv` unidades |

## Casos de uso

```python
import vispy
vispy.use('pyqt5')

from vispy.color import Color

# Desde nombre CSS
c = Color('red')
print(c.rgba)   # array([1., 0., 0., 1.], dtype=float32)
print(c.hex)    # '#ff0000'

# Desde hex
Color('#00ff00').rgb    # array([0., 1., 0.], dtype=float32)

# Desde tupla RGBA
Color((0.2, 0.4, 0.8, 0.9)).alpha   # 0.9

# Sobreescribir alfa en la construccion
c_semi = Color('blue', alpha=0.5)
c_semi.rgba   # array([0., 0., 1., 0.5], dtype=float32)

# Variantes de luminosidad
c_light = Color('steelblue').lighter(0.2)
c_dark  = Color('steelblue').darker(0.15)
```

### Pasar `Color` a un visual

`Color` se puede pasar directamente a cualquier argumento `color` de VisPy que acepte string. Tambien se puede usar `.rgba` para pasarlo como array NumPy.

```python
import vispy
vispy.use('pyqt5')

import numpy as np
from vispy import scene
from vispy.color import Color

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'panzoom'

pos = np.random.rand(50, 2).astype('float32') * 10

markers = scene.visuals.Markers(
    pos=pos,
    face_color=Color('tomato').rgba,   # array (4,) como color uniforme
    parent=view.scene
)

from vispy import app
app.run()
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `ValueError: unknown color` | Nombre CSS no reconocido | Usar hex o tupla; verificar nombre en `vispy.color.get_color_names()` |
| Shape error al pasar a visual | Se paso un `Color` objeto en vez de array | Usar `.rgba` o `.rgb` para obtener el array NumPy |
| Alpha ignorado | Se paso `alpha` pero el color ya tenia RGBA completo | `alpha` sobreescribe; revisar que el orden sea `(r, g, b, a)` |

## Notas relacionadas

- [[ColorArray]] — para asignar un color distinto a cada elemento
- [[vispy.get_colormap]] — para mapear datos escalares a colores
- [[Markers]] — visual donde `face_color` acepta `Color`, array o `ColorArray`
