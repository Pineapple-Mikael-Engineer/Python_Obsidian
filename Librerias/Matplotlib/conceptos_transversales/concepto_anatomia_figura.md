---
title: Anatomia de una figura — El vocabulario visual
aliases:
  - anatomia de una figura
  - partes de un grafico
  - axis vs axes
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

# Anatomia de una figura — El vocabulario visual

## Definicion fundamental

Cada parte visible de un grafico tiene un **nombre tecnico** preciso. Conocerlo es lo que permite buscar el metodo correcto: si sabes que esa raya de fondo es un *gridline* y ese borde es un *spine*, encuentras `ax.grid` y `ax.spines` sin adivinar.

## El mapa de partes

```
Figure (lienzo completo)
└── Axes (region de ploteo)
    ├── Axis X  ──┐
    ├── Axis Y  ──┤ cada Axis tiene:
    │             ├── ticks (marcas: major y minor)
    │             ├── tick labels (numeros)
    │             └── axis label (titulo del eje)
    ├── spines (los 4 bordes: top, bottom, left, right)
    ├── title (titulo del Axes)
    ├── legend (leyenda)
    ├── gridlines (rejilla de fondo)
    └── los datos dibujados (Line2D, Patch, ...)
```

## La distincion critica: Axes vs Axis

| Termino | Que es | Cuantos por subgrafo |
|---------|--------|----------------------|
| **Axes** | la region de ploteo completa | 1 (el subgrafo entero) |
| **Axis** | un eje de coordenadas (X o Y) | 2 (`ax.xaxis`, `ax.yaxis`) |

> "Axes" suena a plural pero es **singular** (la region). "Axis" es cada eje. Es la confusion terminologica nº1 de Matplotlib.

## Vocabulario y su metodo asociado

| Parte visible | Nombre | Cómo se toca |
|---------------|--------|--------------|
| Titulo del subgrafo | title | [[ax.set_title]] |
| Etiqueta del eje X/Y | axis label | [[ax.set_xlabel]] / [[ax.set_ylabel]] |
| Numeros de los ejes | tick labels | [[ax.set_xticks]] / [[ax.tick_params]] |
| Marcas de los ejes | ticks (major/minor) | [[Locators]], [[ax.tick_params]] |
| Bordes del recuadro | spines | `ax.spines['top'].set_visible(False)` |
| Rejilla de fondo | gridlines | [[ax.grid]] |
| Caja de series | legend | [[ax.legend]] |
| Limites visibles | limits | `ax.set_xlim`, `ax.set_ylim` |

## Por que este vocabulario ahorra tiempo

Sin el vocabulario, "quitar la linea de arriba del recuadro" es un misterio. Con el: es el **spine** `top` → `ax.spines['top'].set_visible(False)`. El nombre es el atajo al metodo.

## Ticks: major vs minor

Cada Axis tiene dos niveles de marcas:
- **major ticks**: las principales (con numero).
- **minor ticks**: subdivisiones (normalmente sin etiqueta).

Su posicion la deciden los **Locators** y su formato los **Formatters** (ver [[Locators]]).

## Relacion con otros conceptos

- [[concepto_figure_axes]]
- [[concepto_artist]]
- [[ax.grid]]
- [[ax.tick_params]]
- [[Locators]]
