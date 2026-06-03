---
title: Axes3D.view_init — Fijar el ángulo de cámara 3D
aliases:
  - view_init
  - angulo de camara
  - elevacion azimut
  - orientar vista 3d

tags:
  - matplotlib
  - api/metodo
  - plot/3d

# --- Clasificación ---
lib: matplotlib
obj: Axes3D
tipo: metodo

# --- Comportamiento ---
retorna: None
muta_estado: true

# --- Dependencias ---
requiere:
  - axes3d

draft: false
---

# Axes3D.view_init — Fijar el ángulo de cámara 3D

## Firma de la función

```python
Axes3D.view_init(
    elev=None,
    azim=None,
    roll=0,
    vertical_axis='z',
    *,
    share=False
)  # -> None
```

Orienta la **cámara virtual** desde la que se observa la escena 3D, sin tocar los datos dibujados. `elev` es la **elevación** (ángulo vertical sobre el plano X-Y) y `azim` el **azimut** (rotación horizontal alrededor del eje vertical); `roll` inclina la cámara sobre su propio eje. Es la forma de elegir desde qué punto se mira una superficie de [[plot_surface]] o una nube de puntos para que sea legible. Requiere un `Axes3D` (ver [[axes3d]]), que se crea con `ax = fig.add_subplot(projection='3d')`. Muta el estado del Axes (cambia sus atributos `ax.elev`, `ax.azim`) y **no retorna nada** (`None`).

## Valor de retorno

| Llamada | Retorno | Efecto |
|---------|---------|--------|
| `ax.view_init(30, 45)` | `None` | reorienta la cámara, no devuelve valor |
| `ax.view_init(elev=90)` | `None` | vista cenital (desde arriba) |
| `ax.view_init(azim=0, roll=15)` | `None` | rotación + inclinación de cámara |

```python
ret = ax.view_init(elev=30, azim=45)
ret               # → None  (muta el Axes, no devuelve)
ax.elev, ax.azim  # → (30, 45)  el estado quedó actualizado
```

## Formas básicas de llamada

| Llamada | Vista resultante |
|---------|------------------|
| `ax.view_init(elev=30, azim=-60)` | vista 3D estándar de Matplotlib |
| `ax.view_init(elev=90, azim=-90)` | cenital: como un mapa 2D desde arriba |
| `ax.view_init(elev=0, azim=0)` | lateral: se ve el "perfil" de la superficie |
| `ax.view_init(elev=20, azim=120)` | gira la escena para ver otra cara |
| `ax.view_init(elev=30, azim=45, roll=10)` | añade inclinación de cámara |

## Parámetros en detalle

### `elev` (elevación)

Ángulo en grados **por encima del plano X-Y**. Valores altos miran la escena desde arriba; `0` la mira de canto y `90` es cenital (planta). Por defecto vale 30.

```python
ax.view_init(elev=0)    # mirada horizontal, perfil de la superficie
ax.view_init(elev=90)   # mirada vertical, vista de planta (tipo mapa)
```

### `azim` (azimut)

Ángulo en grados de **rotación horizontal** alrededor del eje vertical. Gira la escena lateralmente para enfrentar distintas caras. Por defecto vale -60.

```python
ax.view_init(azim=0)     # cara frontal
ax.view_init(azim=90)    # un cuarto de vuelta lateral
```

### `roll`

Inclinación de la cámara sobre su propia línea de visión (gira la "horizontal" de la imagen). Útil para encuadres especiales; por defecto 0.

```python
ax.view_init(elev=30, azim=45, roll=20)   # imagen inclinada 20°
```

### `vertical_axis`

Qué eje actúa como vertical de la cámara (`'z'` por defecto). Cambiarlo a `'x'` o `'y'` reinterpreta elevación y azimut respecto a otro eje, útil cuando la variable de interés no es Z.

## Casos de uso

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra la proyección '3d'

x = np.linspace(-5, 5, 80)
y = np.linspace(-5, 5, 80)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection='3d')      # imprescindible: Axes3D
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=45, azim=-50)            # encuadre legible de la cresta
```

```python
# Una rejilla de vistas del mismo objeto desde ángulos distintos
fig = plt.figure(figsize=(9, 3))
for i, azim in enumerate([-60, 0, 60]):
    ax = fig.add_subplot(1, 3, i + 1, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='plasma')
    ax.view_init(elev=30, azim=azim)       # mismo objeto, tres azimuts
```

```python
# Animación: girar la cámara variando azim cuadro a cuadro
for ang in range(0, 360, 5):
    ax.view_init(elev=30, azim=ang)        # muta la vista
    fig.canvas.draw_idle()
```

## Buenas prácticas

1. Crea el `Axes3D` con `ax = fig.add_subplot(projection='3d')` antes de orientar la cámara.
2. Llama a `view_init` **después** de dibujar; es solo cámara y no depende del orden de trazado.
3. No asignes su retorno: devuelve `None` y actúa por efecto secundario sobre el Axes.
4. Usa `elev=90` para una lectura tipo mapa 2D y `elev=0` para inspeccionar el perfil.
5. Para animaciones, recorre `azim` en un bucle y redibuja en cada paso.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'Axes' object has no attribute 'view_init'` | el Axes no es 3D | crear con `projection='3d'` |
| `view_init` "no devuelve la vista" | retorna `None`, muta el Axes | leer `ax.elev` / `ax.azim`, no el retorno |
| La cámara no cambia | se llamó antes de `plt.show` pero se sobrescribió luego | fijar `view_init` como último ajuste de cámara |
| Vista cenital inesperada | `elev=90` aplana la percepción de Z | bajar `elev` para recuperar el volumen |
| `roll` no reconocido | versión antigua de Matplotlib | actualizar o usar solo `elev`/`azim` |

## Notas relacionadas

- [[axes3d]]
- [[plot_surface]]
