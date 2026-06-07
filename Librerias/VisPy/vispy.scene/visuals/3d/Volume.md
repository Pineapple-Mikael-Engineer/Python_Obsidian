---
title: Volume — renderizado volumetrico 3D
aliases:
  - Volume
  - vispy volume
tags:
  - vispy
  - api/clase
  - scene/visuals
lib: vispy
mod: vispy.scene.visuals
tipo: clase
retorna: Volume
requiere:
  - SceneCanvas
  - ViewBox
  - TurntableCamera
draft: false
---

# Volume — renderizado volumetrico 3D

`scene.visuals.Volume` renderiza un array 3D `(D, H, W)` directamente en la GPU usando
ray-casting volumetrico. Es el visual adecuado para datos que tienen densidad en el espacio:
escaneres CT/MRI, simulaciones CFD, datos de sismologia o atmosfera. El metodo de renderizado
(`method`) controla como los rayos acumulan o seleccionan la intensidad a lo largo del volumen.

## Importacion

```python
from vispy import scene, app
import vispy
vispy.use('pyqt5')

vol = scene.visuals.Volume(...)
```

## Constructor / Firma

```python
scene.visuals.Volume(
    vol,                  # array (D, H, W) float32 — datos volumetricos
    clim=None,            # (vmin, vmax) — rango de mapeado de color
    cmap='grays',         # colormap string ('grays', 'fire', 'viridis', …)
    method='mip',         # metodo de renderizado (ver abajo)
    threshold=None,       # umbral para method='iso'
    relative_step_size=0.8,  # tamano de paso del ray-caster (calidad vs velocidad)
    parent=None,
)
```

## Parametros clave

| Parametro | Tipo | Descripcion |
|-----------|------|-------------|
| `vol` | `(D, H, W) float32` | Volumen 3D; eje 0 = profundidad, eje 1 = altura, eje 2 = ancho |
| `clim` | `(float, float)` | Valores minimo y maximo para el mapeado de color; `None` = auto |
| `cmap` | str | Colormap: `'grays'`, `'fire'`, `'viridis'`, `'hot'`, `'RdBu'`… |
| `method` | str | Algoritmo de ray-casting (ver tabla de metodos) |
| `threshold` | float | Solo para `method='iso'`; nivel de isosuperficie |
| `relative_step_size` | float | `< 1` = mas calidad, mas lento; `> 1` = mas rapido, menos detalle |

### Metodos de renderizado

| `method` | Nombre completo | Descripcion |
|----------|-----------------|-------------|
| `'mip'` | Maximum Intensity Projection | Cada pixel = valor maximo a lo largo del rayo. Ideal para estructuras brillantes (vasos, huesos) |
| `'translucent'` | Compositing translucido | Acumula color+opacidad a lo largo del rayo. Muestra interiores |
| `'iso'` | Isosuperficie | Renderiza la primera superficie en `threshold`. Efecto solido |
| `'additive'` | Suma aditiva | Suma todas las intensidades; util para nubes de puntos difusas |

## Casos de uso

### Volumen aleatorio con MIP

```python
import vispy
vispy.use('pyqt5')
from vispy import scene, app
import numpy as np

canvas = scene.SceneCanvas(keys='interactive', show=True, size=(800, 600))
view = canvas.central_widget.add_view()
view.camera = 'turntable'

vol_data = np.random.rand(64, 64, 64).astype('float32')
vol = scene.visuals.Volume(
    vol_data,
    clim=(0.0, 1.0),
    cmap='fire',
    method='mip',
    parent=view.scene,
)
app.run()
```

### Datos medicos (CT/MRI con SimpleITK)

```python
import SimpleITK as sitk
import numpy as np

img = sitk.ReadImage('scan.nii.gz')
arr = sitk.GetArrayFromImage(img).astype('float32')  # shape: (D, H, W)

# Normalizar al rango [0, 1]
arr = (arr - arr.min()) / (arr.max() - arr.min())

vol = scene.visuals.Volume(
    arr,
    clim=(0, 1),
    cmap='grays',
    method='mip',
    parent=view.scene,
)
```

### Isosuperficie

```python
# Esfera implicita en un volumen
D, H, W = 64, 64, 64
x = np.linspace(-1, 1, W)
y = np.linspace(-1, 1, H)
z = np.linspace(-1, 1, D)
Z, Y, X = np.meshgrid(z, y, x, indexing='ij')
esfera = (X**2 + Y**2 + Z**2).astype('float32')

vol = scene.visuals.Volume(
    esfera,
    clim=(0, 3),
    cmap='grays',
    method='iso',
    threshold=0.5,   # isosuperficie a r=0.707
    parent=view.scene,
)
```

### Actualizar datos en animacion

```python
# Usar .set_data() en el callback del Timer, nunca reasignar
def on_timer(event):
    nuevo_vol = generar_frame().astype('float32')
    vol.set_data(nuevo_vol)
    canvas.update()

timer = app.Timer(interval=0.05, connect=on_timer, start=True)
```

## Metodos y atributos

| Nombre | Descripcion |
|--------|-------------|
| `.set_data(vol)` | Actualiza el array volumetrico en la GPU |
| `.clim` | Propiedad lectura/escritura para el rango de color |
| `.cmap` | Propiedad lectura/escritura para el colormap |
| `.method` | Propiedad lectura/escritura para el metodo de renderizado |
| `.threshold` | Umbral de isosuperficie (solo `method='iso'`) |

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Volumen negro / invisible | `clim` fuera del rango real de datos | Usar `clim=(arr.min(), arr.max())` |
| Bajo rendimiento | `relative_step_size` muy pequeno o volumen muy grande | Aumentar step_size o reducir resolucion del array |
| `TypeError: vol must be float32` | Array en `float64` o `int` | `vol.astype('float32')` |
| Imagen girada incorrectamente | Eje de profundidad incorrecto | Verificar el orden de ejes: `np.transpose(arr, ...)` |

## Notas relacionadas

- [[vispy.scene/visuals/3d/index|visuals 3D]] — contexto del submodulo
- [[TurntableCamera]] — camara orbital indispensable para inspeccionar volumenes
- [[Mesh]] — alternativa cuando el dato ya es una malla superficial (STL, OBJ)
- [[Surface]] — para funciones z=f(x,y) en grid regular, mas liviano que Volume
