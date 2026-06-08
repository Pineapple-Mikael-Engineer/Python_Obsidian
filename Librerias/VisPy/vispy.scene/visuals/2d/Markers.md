---
title: Markers — scatter plot de puntos y simbolos
aliases: [Markers, vispy markers, scatter vispy]
tags: [vispy, api/clase, scene/visuals]
lib: vispy
mod: vispy.scene.visuals
tipo: clase
requiere: [SceneCanvas, ViewBox]
draft: false
---

# Markers — scatter plot de puntos y simbolos

Visual de alto nivel para dibujar colecciones de puntos o simbolos sobre un [[ViewBox]].
Indispensable para scatter plots con grandes volumenes de datos (>100 k puntos) donde
Matplotlib se vuelve inviable: Markers delega todo el renderizado a la GPU.

## Importacion

```python
import vispy; vispy.use('pyqt5')
from vispy import scene, app
import numpy as np
```

## Constructor / Firma

```python
markers = scene.visuals.Markers(parent=view.scene)
```

El constructor acepta pocos parametros directamente; los datos se asignan con `.set_data()`.

```python
markers.set_data(
    pos,                    # array (N, 2) o (N, 3) float32 — obligatorio
    face_color='white',     # string CSS, RGBA, o array (N, 4)
    edge_color='black',     # color del borde; None desactiva borde
    size=10.0,              # float o array (N,) en pixeles
    edge_width=1.0,         # grosor del borde en pixeles
    symbol='o',             # string — ver tabla de simbolos
)
```

## Parametros clave

### `pos`

| Forma | Shape | Uso |
|-------|-------|-----|
| 2D | `(N, 2)` float32 | scatter en plano |
| 3D | `(N, 3)` float32 | scatter en espacio 3D |

```python
N = 10_000
pos = np.random.randn(N, 2).astype('float32')
```

### `face_color` / `edge_color`

| Tipo de valor | Ejemplo | Resultado |
|---------------|---------|-----------|
| String CSS | `'yellow'` | color uniforme |
| Tuple RGBA | `(0, 1, 0.5, 0.8)` | color uniforme con alfa |
| Array `(N, 4)` | `colores` | color individual por punto |
| `None` | — | desactiva esa capa (util para `edge_color`) |

### `symbol`

| Codigo | Forma |
|--------|-------|
| `'o'` | circulo (defecto) |
| `'s'` | cuadrado |
| `'+'` | cruz |
| `'^'` | triangulo arriba |
| `'v'` | triangulo abajo |
| `'*'` | estrella |
| `'d'` | diamante |

### `size`

Puede ser un escalar (todos igual) o un array `(N,)` para tamanos individuales:

```python
sizes = np.abs(np.random.randn(N)).astype('float32') * 10 + 5
markers.set_data(pos=pos, size=sizes, face_color='cyan')
```

## Casos de uso

### Scatter plot basico

```python
canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'panzoom'

N = 5000
pos = np.random.randn(N, 2).astype('float32')
markers = scene.visuals.Markers(parent=view.scene)
markers.set_data(pos=pos, face_color='yellow', size=6, symbol='o')

view.camera.set_range()
app.run()
```

### Color por magnitud

```python
magnitud = np.linalg.norm(pos, axis=1)            # (N,)
t = (magnitud - magnitud.min()) / magnitud.ptp()  # normalizar a [0, 1]

from vispy.color import get_colormap
cmap = get_colormap('fire')
colores = cmap[t].rgba.astype('float32')           # (N, 4)

markers.set_data(pos=pos, face_color=colores, size=8, edge_color=None)
```

### Actualizar en animacion (sin recrear)

```python
def on_timer(event):
    pos[:, 0] += 0.01                             # mover puntos
    markers.set_data(pos=pos, face_color='cyan')
    canvas.update()

timer = app.Timer(interval=1/60, connect=on_timer, start=True)
app.run()
```

Nunca recrear `scene.visuals.Markers(...)` dentro del callback — es muy costoso.

## Metodos y atributos

| Miembro | Descripcion |
|---------|-------------|
| `.set_data(pos, face_color, edge_color, size, symbol)` | actualiza todos los datos de golpe |
| `.pos` | array de posiciones actual |
| `.symbol` | simbolo actual |
| `.size` | tamano actual |
| `.visible` | bool — ocultar/mostrar |
| `.parent` | nodo padre en el scene graph |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|---------|
| Sin render visible | `parent` incorrecto | usar `parent=view.scene` |
| Lentitud inesperada | recrear `Markers` cada frame | usar `.set_data()` en su lugar |
| ValueError en pos | dtype float64 | `pos.astype('float32')` |
| Simbolos invisibles | `size` demasiado pequeno | probar con `size=10` como base |

## Notas relacionadas

- [[Line]]
- [[ViewBox]]
- [[SceneCanvas]]
- [[vispy.scene/visuals/2d/index\|Visuals 2D]]
