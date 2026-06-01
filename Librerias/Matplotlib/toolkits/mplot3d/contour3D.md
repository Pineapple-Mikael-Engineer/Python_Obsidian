---
title: Axes3D.contour3D — Curvas de nivel flotando en 3D
aliases:
  - contour3D
  - contour 3d
  - curvas de nivel 3d
  - contornos 3d

tags:
  - matplotlib
  - api/metodo
  - plot/3d

# --- Clasificación ---
lib: matplotlib
obj: Axes3D
tipo: metodo

# --- Comportamiento ---
retorna: QuadContourSet
muta_estado: true

# --- Dependencias ---
requiere:
  - axes3d
  - numpy.meshgrid

draft: false
---

# Axes3D.contour3D — Curvas de nivel flotando en 3D

## Firma de la función

```python
Axes3D.contour3D(
    X, Y, Z,
    *,
    levels=None,
    zdir='z', offset=None,
    cmap=None, colors=None,
    **kwargs
)  # -> QuadContourSet

# equivalente moderno (mismo efecto sobre un Axes3D):
Axes3D.contour(X, Y, Z, levels=..., **kwargs)
```

Dibuja **líneas de contorno (curvas de nivel) en el espacio 3D**: para cada nivel de `Z` traza la curva donde la superficie alcanza ese valor, situada a la altura correspondiente. El resultado son curvas que "flotan" apiladas, como las capas de un mapa topográfico levantadas en altura. A diferencia de [[plot_surface]] (que rellena la superficie) o de `contourf3D` (contornos rellenos), aquí solo hay líneas. Requiere un `Axes3D` (ver [[axes3d]]), que se crea con `ax = fig.add_subplot(projection='3d')`; muta ese Axes añadiendo el conjunto de contornos.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| mallas X, Y, Z 2D coherentes | `QuadContourSet` | `cs = ax.contour3D(X, Y, Z)` |
| con `levels=20` | `QuadContourSet` con ~20 niveles | `ax.contour3D(X, Y, Z, levels=20)` |
| con `offset=z0` | `QuadContourSet` proyectado a un plano | `ax.contour(X, Y, Z, offset=-1)` |

```python
cs = ax.contour3D(X, Y, Z, levels=15, cmap='viridis')
type(cs)         # → <class 'matplotlib.contour.QuadContourSet'>
ax.clabel(cs)    # el retorno permite etiquetar los niveles
```

## Formas básicas de llamada

| Llamada | Efecto |
|---------|--------|
| `ax.contour3D(X, Y, Z)` | curvas de nivel automáticas en el espacio |
| `ax.contour3D(X, Y, Z, levels=30)` | ~30 niveles equiespaciados |
| `ax.contour3D(X, Y, Z, levels=[0, 1, 2])` | solo esos niveles concretos |
| `ax.contour(X, Y, Z, cmap='plasma')` | API moderna, color por nivel |
| `ax.contour(X, Y, Z, zdir='z', offset=-2)` | proyección de las curvas a un plano base |

## Parámetros en detalle

### `X`, `Y`, `Z`

Las tres mallas 2D. `X` e `Y` suelen venir de `np.meshgrid` y `Z` es el campo escalar cuyos niveles se contornean. Las tres deben tener la **misma forma 2D**.

```python
import numpy as np
x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))
ax.contour3D(X, Y, Z, levels=25)
```

### `levels`

Define los niveles a contornear. Un entero pide ~N niveles automáticos; una secuencia fija exactamente esos valores de `Z`.

```python
ax.contour3D(X, Y, Z, levels=40)            # muchos niveles, aspecto denso
ax.contour3D(X, Y, Z, levels=[0.2, 0.5, 0.8])  # solo tres curvas
```

### `zdir`, `offset` (proyección)

`zdir` indica la dirección de proyección (`'z'`, `'x'`, `'y'`) y `offset` aplana los contornos sobre un plano a esa coordenada, en lugar de dejarlos a su altura real. Útil para "sombras" de contorno bajo o detrás de una superficie.

```python
ax.contour(X, Y, Z, zdir='z', offset=Z.min() - 0.5)  # proyectados al suelo
```

### `cmap`, `colors`

`cmap` colorea los niveles según su valor (mapa continuo); `colors` fija colores explícitos por nivel. Son alternativos.

```python
ax.contour3D(X, Y, Z, cmap='coolwarm')           # color por nivel
ax.contour3D(X, Y, Z, colors='k', linewidths=0.5)  # todas negras
```

## Casos de uso

```python
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra la proyección '3d'

x = np.linspace(-6, 6, 100)
y = np.linspace(-6, 6, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection='3d')      # imprescindible: Axes3D
cs = ax.contour3D(X, Y, Z, levels=30, cmap='viridis')
ax.set_zlabel("z")
ax.view_init(elev=35, azim=-50)
# → anillos concéntricos del "sombrero mexicano" apilados en altura
```

```python
# Superficie + sus contornos proyectados al plano base (efecto mapa)
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
ax.contour(X, Y, Z, zdir='z', offset=Z.min() - 0.5, cmap='viridis')
# → la superficie con su "topografía" dibujada debajo
```

## Buenas prácticas

1. Crea el `Axes3D` con `ax = fig.add_subplot(projection='3d')` antes de contornear.
2. Genera `X`, `Y` con `np.meshgrid` y calcula `Z` vectorizado.
3. Empieza con `levels` entero para explorar y luego fija una lista para resaltar niveles concretos.
4. Combina con `plot_surface` + `offset` para proyectar los contornos como "sombra" topográfica.
5. Guarda el retorno (`cs = ...`) si vas a etiquetar niveles con `ax.clabel(cs)`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'Axes' object has no attribute 'contour3D'` | el Axes no es 3D | crear con `projection='3d'` |
| `Input z must be 2D` | `Z` es 1D | construir `Z` sobre mallas de `np.meshgrid` |
| Formas incompatibles X/Y/Z | no comparten la misma forma 2D | verificar `X.shape == Y.shape == Z.shape` |
| Contornos vacíos | los `levels` quedan fuera del rango de `Z` | usar niveles dentro de `[Z.min(), Z.max()]` |
| `cmap` y `colors` juntos sin efecto | son excluyentes | usar solo uno de los dos |

## Notas relacionadas

- [[axes3d]]
- [[plot_surface]]
