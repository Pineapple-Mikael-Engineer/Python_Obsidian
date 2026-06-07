---
title: ColorArray — coleccion de N colores en VisPy
aliases:
  - ColorArray
  - vispy colorarray
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

# ColorArray — coleccion de N colores en VisPy

`ColorArray` agrupa **N colores en un unico objeto** y expone el resultado como un array RGBA de forma `(N, 4)`. Es el tipo correcto cuando cada punto de un [[Markers]] o cada vertice de un [[Mesh]] necesita un color propio. Acepta formatos mezclados (strings, hex, tuplas) en la misma lista.

## Importacion

```python
from vispy.color import ColorArray
```

## Constructor / Firma

```python
ColorArray(colors, alpha=None, color_space='rgb')
```

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `colors` | `list \| np.ndarray` | Lista de colores en cualquier formato soportado por `Color`; o array NumPy `(N, 3/4)` float32 |
| `alpha` | `float \| None` | Sobreescribe el canal alfa de todos los colores |
| `color_space` | `str` | `'rgb'` (default) o `'hsv'` si el input ya esta en HSV |

## Propiedades clave

| Propiedad | Tipo | Descripcion |
|-----------|------|-------------|
| `.rgba` | `np.ndarray` shape `(N, 4)` float32 | Todos los colores en RGBA |
| `.rgb` | `np.ndarray` shape `(N, 3)` float32 | Solo canales RGB |
| `.hex` | `list[str]` | Lista de strings hex para cada color |
| `.colors[i]` | `Color` | Color individual en el indice `i` |

## Casos de uso

### Construccion desde lista mixta

```python
import vispy
vispy.use('pyqt5')

from vispy.color import ColorArray

ca = ColorArray(['red', 'green', 'blue'])
print(ca.rgba)
# array([[1.   , 0.   , 0.   , 1.   ],
#        [0.   , 0.502, 0.   , 1.   ],   # verde CSS ≈ (0, 128/255, 0)
#        [0.   , 0.   , 1.   , 1.   ]], dtype=float32)

# Formato mixto: nombre + hex + tupla
ca2 = ColorArray(['tomato', '#1f77b4', (0.2, 0.9, 0.4)])
ca2.rgba.shape   # (3, 4)

# Acceder a un color individual
ca2.colors[0]    # Color('tomato')
```

### Uso con Markers (un color por punto)

Caso mas comun: asignar un color distinto a cada uno de los N puntos de un scatter.

```python
import vispy
vispy.use('pyqt5')

import numpy as np
from vispy import scene
from vispy.color import ColorArray

n = 200
pos = np.random.rand(n, 2).astype('float32') * 10

# Paleta ciclica de 3 colores para n puntos
base_colors = ['#e41a1c', '#377eb8', '#4daf4a']
colors = ColorArray([base_colors[i % 3] for i in range(n)])

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'panzoom'
view.camera.set_range(x=(0, 10), y=(0, 10))

markers = scene.visuals.Markers(
    pos=pos,
    face_color=colors.rgba,   # (N, 4) — un RGBA por punto
    size=8,
    parent=view.scene
)

from vispy import app
app.run()
```

### Uso con Mesh (colores por vertice)

```python
import vispy
vispy.use('pyqt5')

import numpy as np
from vispy import scene
from vispy.color import ColorArray

# Vertices de un triangulo
vertices = np.array([[0, 0, 0],
                     [1, 0, 0],
                     [0.5, 1, 0]], dtype='float32')
faces = np.array([[0, 1, 2]])

# Un color por vertice
vc = ColorArray(['red', 'green', 'blue'])

canvas = scene.SceneCanvas(keys='interactive', show=True)
view = canvas.central_widget.add_view()
view.camera = 'turntable'

mesh = scene.visuals.Mesh(
    vertices=vertices,
    faces=faces,
    vertex_colors=vc.rgba,   # (3, 4)
    parent=view.scene
)

from vispy import app
app.run()
```

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Shape `(N, 4)` no coincide con N puntos | Se paso menos colores que puntos | Asegurarse de que `len(colors_list) == n_puntos` |
| `ValueError` en color mixto | Un elemento de la lista no es color valido | Verificar cada entrada con `Color(elem)` de forma aislada |
| Broadcasting no esperado | Se paso un array `(1, 4)` en vez de `(N, 4)` | VisPy puede broadccastear; si no, replicar con `np.tile` |

## Notas relacionadas

- [[Color]] — color individual; `ColorArray.colors[i]` devuelve un `Color`
- [[vispy.get_colormap]] — alternativa cuando los colores se derivan de datos escalares
- [[Markers]] — visual que acepta `face_color` como array `(N, 4)`
- [[Mesh]] — visual que acepta `vertex_colors` como array `(N, 4)`
