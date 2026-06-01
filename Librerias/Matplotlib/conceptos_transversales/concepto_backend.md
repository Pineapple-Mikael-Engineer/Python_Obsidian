---
title: Backend y render — Dónde y cómo se dibuja
aliases:
  - backend
  - backends
  - render
  - show vs savefig
tags:
  - matplotlib
  - concepto
  - render
lib: matplotlib
tipo: concepto
requiere:
  - concepto_figure_axes
draft: false
---

# Backend y render — Dónde y cómo se dibuja

## Definicion fundamental

Cuando creas un grafico, Matplotlib **no lo pinta de inmediato**: construye una estructura de [[concepto_artist|Artists]] en memoria. El **backend** es el motor que finalmente convierte esa estructura en pixeles (una ventana, un PNG, un SVG, una celda de notebook).

**Idea clave:** el mismo codigo de ploteo produce salidas distintas segun el backend activo, sin cambiar una linea del grafico.

## Dos tipos de backend

| Tipo | Para que | Ejemplos |
|------|----------|----------|
| **Interactivos** | abrir ventanas, hacer zoom | `TkAgg`, `QtAgg`, `MacOSX`, `nbAgg`/`inline` (notebook) |
| **No interactivos** (de archivo) | generar imagenes sin pantalla | `Agg` (PNG), `PDF`, `SVG`, `PS` |

`Agg` (Anti-Grain Geometry) es el rasterizador por defecto para archivos PNG.

## Show vs savefig: el momento del render

| Accion | Que hace | Cuando |
|--------|----------|--------|
| `plt.show()` | renderiza en una **ventana** interactiva (bloquea el script) | backend interactivo |
| `fig.savefig("x.png")` | renderiza a **archivo** | cualquier backend |

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3])

fig.savefig("grafico.png")   # escribe el archivo (no necesita pantalla)
plt.show()                   # abre la ventana (si hay backend interactivo)
```

> En un script sin entorno grafico (servidor, CI), usa el backend `Agg` y `savefig`; `plt.show()` no tendria donde dibujar.

## Elegir el backend

```python
import matplotlib
matplotlib.use("Agg")        # ANTES de importar pyplot; fuerza salida a archivo
import matplotlib.pyplot as plt
```

En Jupyter, `%matplotlib inline` (estatico) o `%matplotlib widget` (interactivo) seleccionan el backend de la celda.

## Por que importa

| Sintoma | Causa probable | Solucion |
|---------|----------------|----------|
| `plt.show()` no abre nada | backend no interactivo (`Agg`) | usar `savefig`, o un backend interactivo |
| El grafico no aparece en el notebook | falta `%matplotlib inline` | añadir el magic |
| Error "no display" en servidor | backend interactivo sin pantalla | `matplotlib.use("Agg")` |

## El ciclo de dibujo (resumen)

1. Creas Figure/Axes y añades [[concepto_artist|Artists]] → solo memoria.
2. `draw()` (lo dispara `show`/`savefig`) recorre los Artists y pide al backend que los rasterice/vectorice.
3. El backend produce la salida (ventana, PNG, SVG…).

## Relacion con otros conceptos

- [[concepto_figure_axes]]
- [[concepto_artist]]
- [[concepto_pyplot_vs_oo]]
- [[plt.savefig]]
- [[plt.show]]
