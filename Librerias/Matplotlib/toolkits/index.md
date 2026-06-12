---
title: toolkits — Extensiones de Matplotlib (mpl_toolkits)
tags: [matplotlib, indice]
draft: false
---

# toolkits — Extensiones de Matplotlib (mpl_toolkits)

`mpl_toolkits` es el espacio de nombres donde viven las **extensiones** de Matplotlib: módulos que añaden capacidades que no forman parte del núcleo y que **no se cargan por defecto**. Se distribuyen junto a Matplotlib pero se importan aparte (`from mpl_toolkits.mplot3d import Axes3D`, `from mpl_toolkits.axes_grid1 import ...`). La pieza más usada —y la única que cubrimos aquí— es **`mplot3d`**, que registra la proyección `'3d'` y aporta el `Axes3D` para graficar superficies, mallas, nubes de puntos y barras en el espacio. Mentalmente: el núcleo de Matplotlib dibuja en 2D; los toolkits son enchufes opcionales que amplían ese núcleo, y `mplot3d` es el que le da la tercera dimensión.

## En acción

Activar un toolkit es importarlo: el import de `mplot3d` **registra** la proyección `'3d'`, que a partir de ahí está disponible al crear un subgrafo.

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # registra la proyección '3d'

fig = plt.figure(figsize=(6, 5))
ax = fig.add_subplot(projection="3d")     # ax es un Axes3D, no un Axes 2D
type(ax)        # → <class 'mpl_toolkits.mplot3d.axes3d.Axes3D'>
ax.set_zlabel("z")                         # método propio del 3D
```

En versiones modernas `projection='3d'` funciona sin el import explícito, pero conviene escribirlo por compatibilidad y para dejar claro de qué toolkit procede la capacidad.

## Qué hay en esta carpeta

| Subcarpeta | Para qué |
|------------|----------|
| [[Matplotlib/toolkits/mplot3d/index\|mplot3d]] | Gráficos **3D**: el `Axes3D` y sus métodos (`plot_surface`, `plot_wireframe`, `scatter`, `bar3d`, `contour3D`, `view_init`). |

> [!note] Un enchufe, no el núcleo
> Lo que hay bajo `toolkits` no está cargado de serie: se importa por separado. Si ves `Unknown projection '3d'`, falta importar `mpl_toolkits.mplot3d`.

## Notas relacionadas

- [[Axes3D]] — la región de ploteo 3D que aporta `mplot3d`
- [[concepto_figure_axes]] — el modelo Figure / Axes que el 3D extiende
- [[Matplotlib/index\|Matplotlib]] — el índice raíz
