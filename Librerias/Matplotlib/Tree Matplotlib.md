---
title: Tree Matplotlib
draft: true
---

# 🌳 Tree Matplotlib

> Estructura **jerárquica** por **objetos/módulos** de la API (`pyplot`, `figure`, `axes`,
> `ticker`, `patches`…) cruzados con **temáticas** (`graficos/`, `formato/`, `anotaciones/`).
> `✅` = nota creada · sin marca = esqueleto pendiente (roadmap).

---

## 📁 Tipos de notas

| Tipo | Ubicación | Ejemplo |
|------|-----------|---------|
| **Método de Axes** | `axes/metodos/<tematica>/` | `axes/metodos/graficos/ax.plot.md` |
| **Función de pyplot** | `pyplot/funciones/` | `pyplot/funciones/plt.subplots.md` |
| **Clase / objeto** | `<modulo>/` | `lines/Line2D.md`, `figure/Figure.md` |
| **Config** | `config/` | `config/rcParams.md` |
| **Concepto transversal** | `conceptos_transversales/` | `concepto_figure_axes.md` |

---

## 📂 Estructura completa

```tree
Matplotlib/
│
├── ✅ introduccion.md
│
├── 📁 conceptos_transversales/        (8/8 ✅ completo · modelo mental)
│   ├── ✅ concepto_figure_axes.md
│   ├── ✅ concepto_artist.md
│   ├── ✅ concepto_pyplot_vs_oo.md
│   ├── ✅ concepto_anatomia_figura.md
│   ├── ✅ concepto_backend.md
│   ├── ✅ concepto_color_mapping.md
│   ├── ✅ concepto_property_cycle.md
│   └── ✅ concepto_transforms.md
│
├── 📁 pyplot/                         (8/8 ✅ completo)
│   └── 📁 funciones/
│       ├── ✅ plt.subplots.md
│       ├── ✅ plt.figure.md
│       ├── ✅ plt.savefig.md
│       ├── ✅ plt.show.md
│       ├── ✅ plt.close.md
│       ├── ✅ plt.clf.md
│       ├── ✅ plt.colorbar.md
│       └── ✅ plt.subplot_mosaic.md
│
├── 📁 figure/                         (6/6 ✅ completo)
│   ├── ✅ Figure.md
│   └── 📁 metodos/
│       ├── ✅ fig.suptitle.md
│       ├── ✅ fig.tight_layout.md
│       ├── ✅ fig.add_subplot.md
│       ├── ✅ fig.add_axes.md
│       └── ✅ constrained_layout.md
│
├── 📁 axes/                           (33/33 ✅ completo)
│   ├── ✅ arrays.md
│   ├── ✅ Axes.md
│   └── 📁 metodos/
│       │
│       ├── 📁 graficos/
│       │   ├── ✅ ax.plot.md
│       │   ├── ✅ ax.scatter.md
│       │   ├── ✅ ax.bar.md
│       │   ├── ✅ ax.barh.md
│       │   ├── ✅ ax.hist.md
│       │   ├── ✅ ax.contour.md
│       │   ├── ✅ ax.fill_between.md
│       │   ├── ✅ ax.fill_betweenx.md
│       │   ├── ✅ ax.boxplot.md
│       │   ├── ✅ ax.contourf.md
│       │   ├── ✅ ax.imshow.md
│       │   ├── ✅ ax.pie.md
│       │   └── ✅ ax.add_patch.md
│       │
│       ├── 📁 formato/
│       │   ├── ✅ ax.grid.md
│       │   ├── ✅ ax.legend.md
│       │   ├── ✅ ax.set_title.md
│       │   ├── ✅ ax.set_xlabel.md
│       │   ├── ✅ ax.set_ylabel.md
│       │   ├── ✅ ax.set_xticks.md
│       │   ├── ✅ ax.set_yticks.md
│       │   ├── ✅ ax.tick_params.md
│       │   ├── ✅ ax.set_xlim.md
│       │   ├── ✅ ax.set_ylim.md
│       │   ├── ✅ ax.set_xscale.md
│       │   ├── ✅ ax.set_yscale.md
│       │   ├── ✅ ax.set_facecolor.md
│       │   └── ✅ ax.set_aspect.md
│       │
│       ├── 📁 anotaciones/
│       │   ├── ✅ ax.text.md
│       │   └── ✅ ax.annotate.md
│       │
│       ├── 📁 spines/
│       │   └── ✅ ax.spines.md
│       │
│       └── 📁 composicion/
│           └── ✅ ax.inset_axes.md
│
├── 📁 config/                         (3/3 ✅ completo)
│   ├── ✅ rcParams.md
│   ├── ✅ plt.style.use.md
│   └── ✅ estilos.md
│
├── 📁 gridspec/                       (2/2 ✅ completo)
│   ├── ✅ GridSpec.md
│   └── ✅ GridSpecFromSubplotSpec.md
│
├── 📁 ticker/                         (4/4 ✅ completo)
│   ├── ✅ Locators.md
│   ├── ✅ Formatters.md
│   ├── ✅ DateFormatter.md
│   └── ✅ FuncFormatter.md
│
├── 📁 cm/                             (2/2 ✅ completo)
│   ├── ✅ Colormaps.md
│   └── ✅ ListedColormap.md
│
├── 📁 colors/                         (5/5 ✅ completo · normalización y mapeo de color)
│   ├── ✅ Colorbar.md
│   ├── ✅ Normalize.md
│   ├── ✅ LogNorm.md
│   ├── ✅ BoundaryNorm.md
│   └── ✅ LinearSegmentedColormap.md
│
├── 📁 legend/                         (4/4 ✅ completo · leyendas)
│   ├── ✅ Legend.md
│   ├── ✅ Personalizacion_Leyendas.md
│   ├── ✅ Multiples_Leyendas.md
│   └── ✅ handles_labels.md
│
├── 📁 patches/                        (5/5 ✅ completo)
│   ├── ✅ Patch.md
│   ├── ✅ Rectangle.md
│   ├── ✅ Polygon.md
│   ├── ✅ Circle.md
│   └── ✅ Ellipse.md
│
├── 📁 collections/                    (4/4 ✅ completo)
│   ├── ✅ PathCollection.md
│   ├── ✅ QuadContourSet.md
│   ├── ✅ PatchCollection.md
│   └── ✅ LineCollection.md
│
├── 📁 image/                          (2/2 ✅ completo)
│   ├── ✅ imread.md
│   └── ✅ imsave.md
│
├── 📁 text/                           (4/4 ✅ completo)
│   ├── ✅ Text.md
│   ├── ✅ Annotation.md
│   ├── ✅ LaTeX_mathtext.md
│   └── ✅ fontdict.md
│
├── 📁 lines/                          (4/4 ✅ completo · incl. referencias de estilo)
│   ├── ✅ Line2D.md
│   ├── ✅ marker.md
│   ├── ✅ Colores_Nombres.md
│   └── ✅ Estilos_Linea.md
│
├── 📁 animation/                      (1/1 ✅ completo)
│   └── ✅ FuncAnimation.md
│
├── 📁 backend/                        (2/2 ✅ completo)
│   ├── ✅ backends.md
│   └── ✅ cambiar_backend.md
│
└── 📁 toolkits/
    └── 📁 mplot3d/                    (7/7 ✅ completo)
        ├── ✅ plot_surface.md
        ├── ✅ axes3d.md
        ├── ✅ plot_wireframe.md
        ├── ✅ scatter3D.md
        ├── ✅ contour3D.md
        ├── ✅ bar3d.md
        └── ✅ view_init.md
```

---

## 📊 Estado actual de implementación

> Sincronizado con el disco. `✅` = nota creada · sin marca = pendiente (roadmap).

> **Base v1 (80) + expansión 🅱️🅲️🅳️ (25) completas.** Roadmap del Tree al 100%.

| Carpeta | Existentes | Plan | Estado |
|---------|-----------|------|--------|
| `conceptos_transversales/` | 8 | 8 | ✅ completo (modelo mental, +color_mapping/property_cycle/transforms) |
| `pyplot/` | 8 | 8 | ✅ completo |
| `figure/` | 6 | 6 | ✅ completo |
| `axes/` (métodos + arrays) | 33 | 33 | ✅ completo |
| `colors/` 🆕 | 5 | 5 | ✅ completo (Colorbar, Normalize, LogNorm, BoundaryNorm, LinearSegmentedColormap) |
| `legend/` 🆕 | 4 | 4 | ✅ completo (Legend, personalización, múltiples, handles) |
| `collections/` | 4 | 4 | ✅ completo |
| `text/` | 4 | 4 | ✅ completo (+LaTeX_mathtext, fontdict) |
| `toolkits/mplot3d/` | 7 | 7 | ✅ completo (+wireframe, scatter3D, contour3D, bar3d, view_init) |
| `config/`·`gridspec/`·`ticker/`·`lines/`·`patches/`·`cm/`·`image/`·`animation/`·`backend/` | 25 | 25 | ✅ completo |
| raíz (`introduccion.md`) | 1 | — | ✅ |
| **Total** | **105** | **105** | 🎉 roadmap completo |

### Cambios de sincronización aplicados

- Conteo corregido: 23 → **58** notas reales tras los lotes de conceptos + relleno.
- Eliminada `REPORTE_REFACTORIZACION.md` del árbol y de notas relacionadas (no existe en disco).
- `plt.style.use.md` reubicada en el árbol a `config/` (donde está en disco), no en `pyplot/config/`.
- Integrado el antiguo esqueleto pendiente (`<details>`) dentro del árbol, en sus carpetas.
- Añadidas marcas `✅` a las 58 notas existentes y sección "Estado actual".
- ✅ Completados los módulos de Artists primitivos (`patches/`, `cm/`, `collections/`, `image/`, `text/`, `animation/`, `backend/`, `toolkits/mplot3d/`) — **roadmap del Tree al 100% (76 notas)**.

### Expansión del roadmap (bloques aprobados 🅱️🅲️🅳️)

- 🅱️ **Leyendas y color** — módulos nuevos `legend/` (4) y `colors/` (5) + `collections/` (+2). Resuelve links rotos: `Colorbar`, `Normalize`, `LogNorm`, `PatchCollection`, `Personalizacion_Leyendas`, `Multiples_Leyendas`.
- 🅲️ **Conceptos + layout** — 3 conceptos (`color_mapping`, `property_cycle`, `transforms`) + layout avanzado (`subplot_mosaic`, `constrained_layout`, `fig.add_axes`, `ax.inset_axes`).
- 🅳️ **Texto/LaTeX + 3D** — `text/` (+2: `LaTeX_mathtext`, `fontdict`) + `mplot3d` (+5). Resuelve `LaTeX`.
- ⏭️ Bloque 🅰️ (más gráficos + ejes) NO incluido; queda como posible ampliación futura.
- Siguiente acción: **rellenar** estas 25 hojas con subagentes + revisión (cuando se indique).

---

## Notas relacionadas

- [[introduccion]]
- [[Estandarizan Directorio Librerias]]
