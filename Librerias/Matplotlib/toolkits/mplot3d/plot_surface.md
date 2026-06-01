---
title: Axes3D.plot_surface — Dibujar una superficie 3D
aliases:
  - plot_surface
  - superficie 3d
  - surface

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
  - numpy.meshgrid

draft: false
---

# Axes3D.plot_surface — Dibujar una superficie 3D

## Firma de la función

```python
Axes3D.plot_surface(
    X, Y, Z,
    *,
    rcount=50, ccount=50,
    rstride=None, cstride=None,
    cmap=None, color=None,
    norm=None, vmin=None, vmax=None,
    shade=True, lightsource=None,
    **kwargs
)  # -> Poly3DCollection
```

Dibuja una **superficie continua** a partir de dos mallas de coordenadas `X`, `Y` (típicamente de `np.meshgrid`) y una malla de alturas `Z`. Cada celda de la malla se convierte en un parche poligonal coloreado, normalmente según su altura. Requiere un `Axes3D` (ver [[axes3d]]); muta ese Axes añadiendo la superficie a su lista de colecciones.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| mallas X, Y, Z 2D coherentes | `Poly3DCollection` | `surf = ax.plot_surface(X, Y, Z)` |
| con `cmap='viridis'` | `Poly3DCollection` coloreado por altura | `ax.plot_surface(X, Y, Z, cmap='viridis')` |
| con `color='gray'` | `Poly3DCollection` de color uniforme | `ax.plot_surface(X, Y, Z, color='gray')` |

```python
surf = ax.plot_surface(X, Y, Z, cmap='viridis')
type(surf)        # → <class 'mpl_toolkits.mplot3d.art3d.Poly3DCollection'>
fig.colorbar(surf)   # usar el retorno para añadir barra de color
```

## Formas básicas de llamada

| Llamada | Efecto |
|---------|--------|
| `ax.plot_surface(X, Y, Z)` | superficie con color por defecto |
| `ax.plot_surface(X, Y, Z, cmap='plasma')` | coloreada por altura (mapa de color) |
| `ax.plot_surface(X, Y, Z, color='steelblue')` | color uniforme, sin mapa |
| `ax.plot_surface(X, Y, Z, rstride=2, cstride=2)` | submuestreo de la malla (más rápido) |
| `ax.plot_surface(X, Y, Z, edgecolor='k', linewidth=0.2)` | superficie con aristas visibles |

## Parámetros en detalle

### `X`, `Y`, `Z`

Las tres mallas que definen la superficie. `X` e `Y` suelen venir de `np.meshgrid`; `Z` es la altura en cada punto de la malla. Las tres deben ser **arrays 2D de la misma forma**.

```python
import numpy as np
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)        # X, Y: (50, 50)
Z = np.exp(-(X**2 + Y**2))      # Z:    (50, 50)
ax.plot_surface(X, Y, Z)
```

### `cmap`

Mapa de color aplicado según la altura `Z`. Es lo que da el efecto de "mapa de calor" tridimensional. Mutuamente excluyente con `color`.

```python
ax.plot_surface(X, Y, Z, cmap='viridis')   # color por altura
ax.plot_surface(X, Y, Z, cmap='coolwarm')  # divergente
```

### `rstride`, `cstride` (o `rcount`, `ccount`)

Controlan el **submuestreo** de la malla: cada cuántas filas/columnas se toma un parche. Valores altos dibujan menos polígonos (más rápido, menos detalle). En versiones modernas se prefiere `rcount`/`ccount` (número objetivo de muestras).

| Parámetro | Significado | Efecto |
|-----------|-------------|--------|
| `rstride=1, cstride=1` | usar todas las filas/columnas | máximo detalle, más lento |
| `rstride=5, cstride=5` | una de cada 5 | superficie más tosca, rápida |
| `rcount=30, ccount=30` | ~30 muestras por eje | control por conteo objetivo |

### `color`, `edgecolor`, `linewidth`, `alpha`

Estilo visual cuando no se usa `cmap`: `color` da relleno uniforme, `edgecolor`+`linewidth` dibujan las aristas de la malla y `alpha` la transparencia.

```python
ax.plot_surface(X, Y, Z, color='gray', edgecolor='k',
                linewidth=0.3, alpha=0.8)
```

## Casos de uso

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Superficie básica con mapa de color por altura
x = np.linspace(-5, 5, 80)
y = np.linspace(-5, 5, 80)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap='viridis')
fig.colorbar(surf, shrink=0.6)        # barra de color desde el retorno
ax.set_zlabel("z")
ax.view_init(elev=40, azim=-60)
```

```python
# Paraboloide con malla visible y submuestreo
Z = X**2 + Y**2
ax.plot_surface(X, Y, Z, rstride=4, cstride=4,
                edgecolor='k', linewidth=0.2, alpha=0.7)
# → superficie tipo cuenco con rejilla negra
```

## Buenas prácticas

1. Genera `X`, `Y` con `np.meshgrid` y calcula `Z` con operaciones vectorizadas sobre esas mallas.
2. Guarda el retorno (`surf = ax.plot_surface(...)`) si vas a añadir `fig.colorbar(surf)`.
3. Usa `cmap` para datos donde la altura es la variable de interés; reserva `color` para formas geométricas.
4. Ajusta `rcount`/`ccount` (o `rstride`/`cstride`) para equilibrar detalle y rendimiento en mallas grandes.
5. Combina con `view_init` para presentar la superficie desde el ángulo más legible.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'Axes' object has no attribute 'plot_surface'` | el Axes no es 3D | crear con `projection='3d'` |
| `Argument Z must be 2-dimensional` | `Z` es 1D | construir `Z` sobre mallas de `np.meshgrid` |
| Formas incompatibles X/Y/Z | las tres no tienen la misma forma 2D | verificar `X.shape == Y.shape == Z.shape` |
| `cmap` y `color` juntos sin efecto | son excluyentes | usar solo uno de los dos |
| Render lentísimo | malla demasiado densa | subir `rstride`/`cstride` o bajar `rcount`/`ccount` |

## Limitaciones

`plot_surface` asume una **malla regular** (grilla estructurada X/Y). Para datos dispersos o triangulaciones irregulares usa `plot_trisurf`. Para ver solo la estructura sin relleno, `plot_wireframe` es más ligero. Mallas muy densas penalizan el rendimiento del renderizado vectorial.

## Notas relacionadas

- [[axes3d]]
- [[Axes]]
