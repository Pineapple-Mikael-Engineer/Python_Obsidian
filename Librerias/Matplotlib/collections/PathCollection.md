---
title: PathCollection — La colección de puntos que devuelve scatter
aliases:
  - PathCollection
  - colección de puntos
tags:
  - matplotlib
  - api/clase
  - plot/dispersion

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.collections
tipo: clase
obj: PathCollection

# --- Comportamiento ---
retorna: PathCollection
muta_estado: false

draft: false
---

# PathCollection — La colección de puntos que devuelve scatter

## Definición

`PathCollection` es el objeto que **devuelve** [[ax.scatter]]: en lugar de crear un `Artist` por cada punto, gestiona **todos los marcadores como un único Artist** mediante una sola `Path` repetida con distintos offsets. Esto lo hace mucho más eficiente que dibujar miles de líneas individuales, y permite cambiar color, tamaño o posición de toda la nube con una sola llamada.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
scat = ax.scatter(x, y, c=z, cmap='viridis')
type(scat)   # → <class 'matplotlib.collections.PathCollection'>
```

## Métodos principales

| Método | Qué hace | Ejemplo |
|--------|----------|---------|
| `set_array(valores)` | asigna los valores escalares que se mapean a color vía colormap | `scat.set_array(z)` |
| `set_sizes(s)` | cambia el tamaño de cada punto (points^2) | `scat.set_sizes([20, 50, 80])` |
| `set_offsets(coords)` | reposiciona los puntos (array (N,2)) | `scat.set_offsets(np.c_[x2, y2])` |
| `set_cmap(name)` | cambia el colormap aplicado | `scat.set_cmap('plasma')` |
| `set_facecolors(c)` | color de relleno | `scat.set_facecolors('red')` |
| `set_edgecolors(c)` | color del borde | `scat.set_edgecolors('black')` |
| `set_alpha(a)` | transparencia global | `scat.set_alpha(0.5)` |
| `get_offsets()` | devuelve las posiciones actuales | `pos = scat.get_offsets()` |
| `remove()` | elimina la colección del axes | `scat.remove()` |

## Colorear por valor

Para que los puntos se coloreen por un valor numérico, la colección guarda un **array escalar** que un colormap traduce a color. `set_array` actualiza ese array tras la creación, base de muchas animaciones de [[Colormaps]].

```python
scat = ax.scatter(x, y, c=z, cmap='viridis')
scat.set_array(z_nuevo)        # recolorea sin redibujar todo
scat.set_clim(0, 1)            # fija límites de la escala de color
plt.colorbar(scat)             # leyenda de la escala
```

## Casos de uso

### Tamaño y color variables (burbujas)

```python
scat = ax.scatter(x, y, c=valores, s=areas, cmap='plasma', alpha=0.6)
plt.colorbar(scat, label='valor')
```

### Animar una nube de puntos

```python
def update(frame):
    scat.set_offsets(posiciones[frame])   # mover todos los puntos
    scat.set_array(colores[frame])         # recolorear
    return scat,
```

### Modificar tras crear

```python
scat = ax.scatter(x, y)
scat.set_sizes(pesos * 100)    # tamaño proporcional a un peso
scat.set_edgecolors('black')
```

## Buenas prácticas

1. Guarda el retorno de `scatter` (`scat = ax.scatter(...)`) para poder pasarlo a [[plt.colorbar]] y modificarlo después.
2. Para actualizaciones (animaciones, sliders) usa `set_offsets`/`set_array` en vez de volver a llamar a `scatter`: reutiliza el mismo Artist y es mucho más rápido.
3. Como todo Artist, expone el protocolo `get_*`/`set_*` descrito en [[concepto_artist]]; aprovéchalo para inspeccionar y ajustar la colección.
4. `set_sizes` espera **points^2**; recuerda elevar al cuadrado si piensas en diámetros.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `set_array` no cambia color | no hay colormap asociado | Crear con `cmap=` o llamar `set_cmap` |
| Colorbar vacía o errónea | no se pasó la colección a `colorbar` | `plt.colorbar(scat)` con el retorno guardado |
| `set_offsets` falla | forma incorrecta del array | Pasar array `(N, 2)`, p. ej. `np.c_[x, y]` |
| Tamaños inesperadamente grandes | `s` interpretado como points^2 | Ajustar la escala al cuadrado |

## Notas relacionadas

- [[ax.scatter]]
- [[Colormaps]]
- [[plt.colorbar]]
- [[concepto_artist]]
- [[QuadContourSet]]
