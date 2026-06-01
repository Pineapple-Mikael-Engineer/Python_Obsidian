---
title: Axes3D.bar3d — Barras volumétricas en 3D
aliases:
  - bar3d
  - barras 3d
  - histograma 3d

tags:
  - matplotlib
  - api/metodo
  - plot/3d

# --- Clasificación ---
lib: matplotlib
obj: Axes3D
tipo: metodo

# --- Comportamiento ---
retorna: Poly3DCollection
muta_estado: true

# --- Dependencias ---
requiere:
  - axes3d

draft: false
---

# Axes3D.bar3d — Barras volumétricas en 3D

## Firma de la función

```python
Axes3D.bar3d(
    x, y, z,
    dx, dy, dz,
    *,
    color=None, shade=True,
    **kwargs
)  # -> Poly3DCollection
```

Dibuja **barras tridimensionales (prismas)**: cada barra arranca en la esquina base `(x, y, z)` y se extiende con tamaños `(dx, dy, dz)` en cada dirección. Es la herramienta para histogramas 3D y para representar matrices/tablas como columnas de altura variable sobre un plano X-Y. A diferencia de [[plot_surface]], que interpola una superficie continua, `bar3d` muestra valores discretos como bloques. Requiere un `Axes3D` (ver [[axes3d]]), que se obtiene con `ax = fig.add_subplot(projection='3d')`; muta ese Axes añadiendo la colección de polígonos.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| posiciones y tamaños 1D de igual longitud | `Poly3DCollection` | `bars = ax.bar3d(x, y, z, dx, dy, dz)` |
| con `color=array` | `Poly3DCollection` coloreada por barra | `ax.bar3d(x, y, z, dx, dy, dz, color=cols)` |
| con `shade=False` | `Poly3DCollection` sin sombreado | `ax.bar3d(x, y, z, dx, dy, dz, shade=False)` |

```python
bars = ax.bar3d(x, y, z, dx, dy, dz, color='steelblue')
type(bars)        # → <class 'mpl_toolkits.mplot3d.art3d.Poly3DCollection'>
```

## Formas básicas de llamada

| Llamada | Efecto |
|---------|--------|
| `ax.bar3d(x, y, z, dx, dy, dz)` | barras desde la base con tamaños dados |
| `ax.bar3d(x, y, 0, dx, dy, alturas)` | barras desde z=0 con altura = dato |
| `ax.bar3d(x, y, z, 1, 1, dz)` | barras de base unitaria (matriz) |
| `ax.bar3d(x, y, z, dx, dy, dz, color=cols)` | un color por barra |
| `ax.bar3d(x, y, z, dx, dy, dz, shade=False)` | sin sombreado de caras |

## Parámetros en detalle

### `x`, `y`, `z` (esquina base)

Coordenadas de la **esquina inferior** de cada barra, como secuencias 1D de igual longitud. Normalmente `z=0` para que las barras nazcan del suelo. Suelen aplanarse desde una rejilla con `.ravel()`.

```python
import numpy as np
_x = np.arange(4)
_y = np.arange(3)
X, Y = np.meshgrid(_x, _y)
x = X.ravel()                  # esquinas base aplanadas
y = Y.ravel()
z = np.zeros_like(x)           # arrancan en z=0
```

### `dx`, `dy`, `dz` (tamaños)

Anchos de la barra en cada eje: `dx`, `dy` definen la **base rectangular** y `dz` la **altura** (el dato). Pueden ser escalares (mismo tamaño para todas) o arrays por barra. La altura `dz` es la variable que normalmente porta la información.

```python
alturas = np.random.randint(1, 10, size=x.size)
ax.bar3d(x, y, z, dx=0.8, dy=0.8, dz=alturas)   # base 0.8x0.8, altura = dato
```

### `color`, `shade`

`color` admite un color único o un array (un color por barra, p. ej. mapeando la altura con un `cmap` calculado a mano). `shade=True` sombrea las caras para dar volumen; `shade=False` las deja planas.

```python
import matplotlib.cm as cm
cols = cm.viridis(alturas / alturas.max())      # color por altura
ax.bar3d(x, y, z, 0.8, 0.8, alturas, color=cols, shade=True)
```

## Casos de uso

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra la proyección '3d'

_x = np.arange(5)
_y = np.arange(5)
X, Y = np.meshgrid(_x, _y)
x, y = X.ravel(), Y.ravel()
z = np.zeros_like(x)
alturas = (x + y).astype(float)            # dato a representar

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection='3d')      # imprescindible: Axes3D
ax.bar3d(x, y, z, dx=0.7, dy=0.7, dz=alturas, shade=True)
ax.set_zlabel("valor")
ax.view_init(elev=30, azim=-60)
# → matriz 5x5 representada como columnas de altura creciente
```

```python
# Histograma 2D mostrado como barras 3D
hist, xedges, yedges = np.histogram2d(datos_x, datos_y, bins=8)
xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1])
xpos, ypos = xpos.ravel(), ypos.ravel()
ax.bar3d(xpos, ypos, 0, 1, 1, hist.ravel())
# → histograma bivariado en columnas
```

## Buenas prácticas

1. Crea el `Axes3D` con `ax = fig.add_subplot(projection='3d')` antes de dibujar las barras.
2. Aplana las rejillas con `.ravel()` para alinear `x, y, z` y los tamaños.
3. Usa `z=0` salvo que quieras barras flotantes o apiladas a una base distinta.
4. Deja un hueco (`dx, dy < 1`) entre barras para que se distingan visualmente.
5. Mapea la altura a `color` con un `cmap` para reforzar la lectura del valor.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'Axes' object has no attribute 'bar3d'` | el Axes no es 3D | crear con `projection='3d'` |
| Barras solapadas | `dx`/`dy` ≥ separación entre bases | usar `dx, dy < 1` (p. ej. 0.7) |
| Longitudes incompatibles | `x, y, z, dz` no coinciden en tamaño | aplanar todo con `.ravel()` e igualar formas |
| Barras invisibles | `dz` (altura) es 0 o negativa | pasar alturas positivas como `dz` |
| Color único cuando se quería por barra | `color` recibió un escalar | pasar un array de colores del mismo largo |

## Notas relacionadas

- [[axes3d]]
- [[plot_surface]]
