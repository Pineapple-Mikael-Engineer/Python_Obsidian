---
title: Transforms — Los sistemas de coordenadas de Matplotlib
aliases:
  - transforms
  - sistemas de coordenadas
  - transData transAxes transFigure
  - coordenadas display
tags:
  - matplotlib
  - concepto
  - estructura
lib: matplotlib
tipo: concepto
requiere:
  - concepto_figure_axes
draft: false
---

# Transforms — Los sistemas de coordenadas de Matplotlib

## Definicion fundamental

Un mismo punto `(x, y)` puede situarse en **espacios de coordenadas distintos**: ¿`(0.5, 0.5)` es el centro de los datos, el centro del subgrafo o el centro del lienzo? Matplotlib resuelve esa ambiguedad con los **transforms**: objetos que traducen coordenadas de un espacio al de pantalla (pixeles). El parametro `transform=` de los metodos de dibujo elige en que espacio interpretas tus numeros.

**Regla mental:** la cifra que pasas no significa nada por si sola; el `transform` decide **respecto a que** se mide. `(0.5, 0.5)` en `transAxes` es el centro del Axes pase lo que pase con los datos.

## Por que existe

Permite **anclar elementos a lo que importa**: una etiqueta en la esquina superior del subgrafo (coords del Axes) no debe moverse aunque cambies los limites de los datos. Sin transforms, tendrias que recalcular posiciones cada vez que el rango de datos cambia.

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([0, 100], [0, 1])
# Etiqueta SIEMPRE arriba-izquierda del Axes, dependa lo que dependa de los datos
ax.text(0.02, 0.95, "A", transform=ax.transAxes)
```

## Los cuatro sistemas

| Sistema | Transform | Rango / unidad | Uso tipico |
|---------|-----------|----------------|------------|
| **data** | `ax.transData` | unidades de tus datos | poner algo junto a un punto concreto (por defecto) |
| **axes** | `ax.transAxes` | `(0,0)` esquina inf-izq → `(1,1)` sup-der del Axes | etiquetas en esquinas, lineas de referencia |
| **figure** | `fig.transFigure` | `(0,0)` → `(1,1)` del lienzo completo | texto/lineas que cruzan varios subgrafos |
| **display** | `None` / identidad | pixeles de pantalla | rara vez directo; es el destino comun |

> Todos los transforms terminan convirtiendo a **display** (pixeles): es el espacio final donde se pinta. Los demas son atajos comodos hacia el.

## Eleccion segun lo que quieras anclar

| Quiero que el elemento... | Sistema | Transform |
|---------------------------|---------|-----------|
| este junto a un dato `(x, y)` | data | `ax.transData` (defecto) |
| este en una esquina del subgrafo | axes | `ax.transAxes` |
| cruce o etiquete toda la figura | figure | `fig.transFigure` |
| este en un pixel exacto | display | identidad |

```python
# data: en el valor x=42 de los datos
ax.axvline(42)                                  # usa transData implicito

# axes: linea horizontal a media altura del subgrafo
ax.axhline(0.5, transform=ax.transAxes)         # mitad del Axes, no de los datos

# figure: texto centrado en TODO el lienzo
fig.text(0.5, 0.98, "Titulo global", transform=fig.transFigure, ha="center")
```

## Mezclar espacios: blended transform

A veces quieres **X en datos pero Y en fraccion del Axes** (p.ej. una banda vertical en x=10 que ocupe toda la altura visible sin saber sus limites).

```python
import matplotlib.transforms as mtransforms
trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
ax.add_patch(plt.Rectangle((10, 0), 5, 1, transform=trans, alpha=0.2))
# x=10..15 en datos · y=0..1 en fraccion del Axes (toda la altura)
```

## Casos que confunden o que fallan

### Por defecto es transData

Si no pasas `transform=`, tus numeros son **coordenadas de datos**. `ax.text(2, 3, "hola")` pone el texto en el punto de datos `(2, 3)`, no en una fraccion del Axes.

### transAxes ignora los limites de datos

`(0.5, 0.5)` en `transAxes` es el centro del subgrafo **aunque** `set_xlim` cambie. Ese es justo su valor: posicionar sin depender de los datos. Confundirlo con data coords coloca las cosas donde no esperas.

### Las anotaciones pueden mezclar dos espacios

`ax.annotate` admite `xycoords` (donde apunta) y `textcoords` (donde va el texto) distintos: la flecha en un dato (`data`) y la caja en una esquina (`axes fraction`). Util para insets y llamadas.

```python
ax.annotate("pico", xy=(42, 99), xycoords="data",
            xytext=(0.8, 0.9), textcoords="axes fraction",
            arrowprops=dict(arrowstyle="->"))
```

### figure vs axes en multiples subgrafos

Para algo que debe cruzar varios subgrafos usa `fig.transFigure`; `transAxes` queda confinado a un unico [[concepto_figure_axes|Axes]].

## Relacion con otros conceptos

- [[concepto_figure_axes]]
- [[concepto_anatomia_figura]]
- [[ax.annotate]]
- [[ax.text]]
- [[concepto_artist]]
