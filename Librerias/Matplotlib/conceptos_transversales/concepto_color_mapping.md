---
title: Color mapping — De un valor de datos a un color
aliases:
  - color mapping
  - mapeo de color
  - norm cmap colorbar
  - scalarmappable
tags:
  - matplotlib
  - concepto
  - render
lib: matplotlib
tipo: concepto
requiere:
  - concepto_artist
draft: false
---

# Color mapping — De un valor de datos a un color

## Definicion fundamental

Cuando un grafico colorea **segun el valor de los datos** (un mapa de calor, un scatter coloreado por una tercera variable, un contour relleno), Matplotlib ejecuta un **pipeline** fijo que convierte cada numero en un color RGBA. El objeto que tiene datos y sabe colorearlos se llama **ScalarMappable** (lo son `imshow`, `pcolormesh`, `scatter` con `c=`, `contourf`).

**Regla mental:** los datos NO se guardan como colores. Se guardan como numeros y el color se calcula al dibujar, en tres piezas independientes: **norm** (escala el numero) → **cmap** (lo convierte en color) → **colorbar** (lo explica al lector).

## Por que existe este pipeline

Separar el dato del color permite **cambiar la escala o la paleta sin tocar los datos**, y garantizar que la leyenda (la colorbar) siempre refleje el mapeo real. Si el color se fijara a mano, cualquier reescalado romperia la correspondencia.

```python
import matplotlib.pyplot as plt
import numpy as np

datos = np.random.rand(10, 10)
fig, ax = plt.subplots()
im = ax.imshow(datos, cmap="viridis")   # im es un ScalarMappable
fig.colorbar(im, ax=ax)                  # la leyenda del mapeo
```

## Las tres piezas (mas el contenedor)

| Pieza | Objeto | Que hace | Dominio → rango |
|-------|--------|----------|-----------------|
| Contenedor | ScalarMappable | guarda los datos numericos | — |
| **norm** | [[Normalize]] | escala los valores al intervalo unitario | datos → [0, 1] |
| **cmap** | [[Colormaps]] | tabla de busqueda que asigna color | [0, 1] → RGBA |
| **colorbar** | [[Colorbar]] | dibuja la leyenda visual del mapeo | — |

> Las dos primeras hacen el trabajo (norm + cmap); la colorbar solo lo **comunica**. Si cambias norm o cmap, la colorbar se actualiza para seguir siendo veraz.

## El pipeline paso a paso

| Etapa | Entrada | Operacion | Salida |
|-------|---------|-----------|--------|
| 1 | valor de dato (p.ej. `73.0`) | el ScalarMappable lo tiene en su array | `73.0` |
| 2 | `73.0`, con `vmin=0, vmax=100` | `norm` lo lleva a [0, 1] | `0.73` |
| 3 | `0.73` | `cmap(0.73)` busca en la paleta | `(0.12, 0.56, 0.55, 1.0)` RGBA |
| 4 | todo el rango | `colorbar` dibuja la barra-leyenda | barra graduada |

```python
from matplotlib.colors import Normalize
import matplotlib.cm as cm

norm = Normalize(vmin=0, vmax=100)
cmap = plt.get_cmap("viridis")
norm(73.0)        # → 0.73   (escala)
cmap(0.73)        # → (0.127, 0.566, 0.550, 1.0)  RGBA  (color)
```

## Control de la escala con norm

El `norm` decide **como se reparte el color** sobre el rango de datos. Cambiarlo no cambia los datos, cambia el contraste.

| norm | Para que | Efecto |
|------|----------|--------|
| `Normalize(vmin, vmax)` | lineal, por defecto | reparto uniforme |
| `LogNorm()` | datos con varios ordenes de magnitud | comprime los grandes |
| `BoundaryNorm(limites, N)` | bandas discretas | colores por tramos |
| `TwoSlopeNorm(vcenter=0)` | divergente alrededor de un centro | resalta el signo |

```python
from matplotlib.colors import LogNorm
ax.imshow(datos, norm=LogNorm(), cmap="magma")   # escala logaritmica
```

## Casos que confunden o que fallan

### Mapear DATOS a color vs fijar UN color

Este pipeline es para **colorear por valor**. Si solo quieres que una linea sea roja, eso NO usa norm/cmap: es un color fijo (ver [[Colores_Nombres]]).

```python
ax.plot(x, y, color="red")          # color FIJO, sin pipeline
ax.scatter(x, y, c=z, cmap="plasma")  # color MAPEADO desde z, con pipeline
```

La pista: si pasas `color=` es fijo; si pasas `c=` con datos y `cmap=`, es mapeo.

### scatter: `c=` (mapeo) vs `color=` (fijo)

```python
ax.scatter(x, y, c=valores, cmap="viridis")  # cada punto segun su valor
ax.scatter(x, y, color="blue")               # todos azules
```

Mezclar ambos o pasar una lista de colores a `c=` produce resultados sorprendentes.

### La colorbar necesita el ScalarMappable, no el Axes

```python
im = ax.imshow(datos)
fig.colorbar(im, ax=ax)   # se pasa `im` (el mappable), no `ax`
```

Sin un ScalarMappable de referencia, la colorbar no sabe que mapeo dibujar.

### vmin/vmax recortan, no reescalan suavemente

Valores fuera de `[vmin, vmax]` se saturan al color extremo (no desaparecen). Util para fijar una escala comun entre subgrafos, pero esconde outliers.

## Relacion con otros conceptos

- [[concepto_artist]]
- [[Normalize]]
- [[Colormaps]]
- [[Colorbar]]
- [[Colores_Nombres]]
