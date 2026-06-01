---
title: Artist — Todo lo dibujable es un objeto
aliases:
  - Artist
  - artist
  - artists
  - modelo de objetos
tags:
  - matplotlib
  - concepto
  - modelo_objetos
lib: matplotlib
tipo: concepto
requiere:
  - concepto_figure_axes
draft: false
---

# Artist — Todo lo dibujable es un objeto

## Definicion fundamental

En Matplotlib **todo lo que se puede dibujar es un Artist**: el [[concepto_figure_axes|Figure y los Axes]], pero tambien cada linea, punto, texto, barra, leyenda, tick y rectangulo. `Artist` es la clase base de la que todos heredan.

**Consecuencia clave:** cada elemento del grafico es un **objeto con propiedades** que puedes guardar en una variable y modificar despues con `set_*` / consultar con `get_*`.

## Por que importa

Entender que todo es un Artist convierte un grafico en algo **manipulable y programable**, no una imagen estatica:

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

linea, = ax.plot([1, 2, 3])     # ax.plot devuelve una lista de Artists (Line2D)
linea.set_color("red")          # modifico el Artist despues de crearlo
linea.set_linewidth(3)
linea.get_color()               # 'red'
```

Casi todas las funciones de dibujo **devuelven el/los Artist** que crean, para que los guardes y ajustes.

## Dos familias de Artists

| Familia | Que son | Ejemplos |
|---------|---------|----------|
| **Contenedores** | agrupan otros Artists | `Figure`, `Axes`, `Axis` |
| **Primitivos** | lo que realmente se pinta | `Line2D`, `Text`, `Patch` (Rectangle, Circle), `Collection`, `Image` |

Un Axes (contenedor) guarda listas de los primitivos que contiene: `ax.lines`, `ax.patches`, `ax.texts`, `ax.collections`.

## El patron universal get/set

Todo Artist expone el mismo protocolo:

```python
artist.set_<propiedad>(valor)   # cambiar
artist.get_<propiedad>()        # consultar
artist.set(color="blue", alpha=0.5)   # varias a la vez
plt.setp(artist)                # listar propiedades disponibles
```

| Que devuelve cada funcion | Artist retornado |
|---------------------------|------------------|
| `ax.plot()` | lista de [[Line2D]] |
| `ax.scatter()` | [[PathCollection]] |
| `ax.bar()` | contenedor de [[Rectangle]] (Patch) |
| `ax.text()` / `ax.annotate()` | [[Text]] / [[Annotation]] |
| `ax.legend()` | objeto Legend |

## Casos que confunden

### plot devuelve una LISTA

```python
linea, = ax.plot(x, y)   # la coma desempaqueta la lista de 1 elemento
# sin la coma, `linea` seria la lista, no el Line2D
```

### El orden de dibujo: zorder

Los Artists se pintan en capas segun su `zorder` (mayor = mas arriba). Util cuando se solapan.

## Relacion con otros conceptos

- [[concepto_figure_axes]]
- [[concepto_anatomia_figura]]
- [[Line2D]]
- [[Text]]
- [[Patch]]
