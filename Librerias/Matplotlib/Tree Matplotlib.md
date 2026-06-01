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
| **Concepto transversal** | `conceptos_transversales/` (pendiente) | `concepto_figure_axes.md` |

---

## 📂 Estructura completa

```tree
Matplotlib/
│
├── ✅ introduccion.md
│
├── 📁 pyplot/                         (1/7)
│   └── 📁 funciones/
│       ├── ✅ plt.subplots.md
│       ├── plt.figure.md
│       ├── plt.savefig.md
│       ├── plt.show.md
│       ├── plt.close.md
│       ├── plt.clf.md
│       └── plt.colorbar.md
│
├── 📁 figure/                         (0/4)
│   ├── Figure.md
│   └── 📁 metodos/
│       ├── fig.suptitle.md
│       ├── fig.tight_layout.md
│       └── fig.add_subplot.md
│
├── 📁 axes/                           (17/35)
│   ├── ✅ arrays.md
│   ├── Axes.md
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
│       │   ├── ax.boxplot.md
│       │   ├── ax.contourf.md
│       │   ├── ax.imshow.md
│       │   └── ax.pie.md
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
│       │   ├── ax.set_xlim.md
│       │   ├── ax.set_ylim.md
│       │   ├── ax.set_xscale.md
│       │   ├── ax.set_yscale.md
│       │   └── ax.set_facecolor.md
│       │
│       ├── 📁 anotaciones/
│       │   ├── ax.text.md
│       │   └── ax.annotate.md
│       │
│       └── 📁 spines/
│           └── ax.spines.md
│
├── 📁 config/                         (2/3)
│   ├── ✅ rcParams.md
│   ├── ✅ plt.style.use.md
│   └── estilos.md
│
├── 📁 gridspec/                       (1/2)
│   ├── ✅ GridSpec.md
│   └── GridSpecFromSubplotSpec.md
│
├── 📁 ticker/                         (1/4)
│   ├── ✅ Locators.md
│   ├── Formatters.md
│   ├── DateFormatter.md
│   └── FuncFormatter.md
│
├── 📁 cm/                             (0/2)
│   ├── Colormaps.md
│   └── ListedColormap.md
│
├── 📁 patches/                        (0/5)
│   ├── Patch.md
│   ├── Rectangle.md
│   ├── Polygon.md
│   ├── Circle.md
│   └── Ellipse.md
│
├── 📁 collections/                    (0/2)
│   ├── PathCollection.md
│   └── QuadContourSet.md
│
├── 📁 image/                          (0/2)
│   ├── imread.md
│   └── imsave.md
│
├── 📁 text/                           (0/2)
│   ├── Text.md
│   └── Annotation.md
│
├── 📁 lines/                          (0/2)
│   ├── Line2D.md
│   └── marker.md
│
├── 📁 animation/                      (0/1)
│   └── FuncAnimation.md
│
├── 📁 backend/                        (0/2)
│   ├── backends.md
│   └── cambiar_backend.md
│
└── 📁 toolkits/
    └── 📁 mplot3d/                    (0/2)
        ├── plot_surface.md
        └── axes3d.md
```

---

## 📊 Estado actual de implementación

> Sincronizado con el disco. `✅` = nota creada · sin marca = pendiente (roadmap).

| Carpeta | Existentes | Plan | Estado |
|---------|-----------|------|--------|
| `axes/` (métodos + arrays) | 17 | 35 | en progreso |
| `config/` | 2 | 3 | en progreso |
| `pyplot/` | 1 | 7 | en progreso |
| `gridspec/` | 1 | 2 | en progreso |
| `ticker/` | 1 | 4 | en progreso |
| `figure/` · `cm/` · `patches/` · `collections/` · `image/` · `text/` · `lines/` · `animation/` · `backend/` · `toolkits/` | 0 | — | pendiente |
| raíz (`introduccion.md`) | 1 | — | ✅ |
| **Total** | **23** | ~70 | — |

### Notas existentes (23)

```text
introduccion.md
pyplot/funciones/    → plt.subplots
config/              → rcParams, plt.style.use
axes/                → arrays
axes/metodos/graficos/ → ax.plot, ax.scatter, ax.bar, ax.barh, ax.hist, ax.contour,
                         ax.fill_between, ax.fill_betweenx
axes/metodos/formato/  → ax.grid, ax.legend, ax.set_title, ax.set_xlabel, ax.set_ylabel,
                         ax.set_xticks, ax.set_yticks, ax.tick_params
gridspec/            → GridSpec
ticker/              → Locators
```

### Cambios de sincronización aplicados

- Conteo corregido: **23** notas reales (antes decía "26").
- Eliminada `REPORTE_REFACTORIZACION.md` del árbol y de notas relacionadas (no existe en disco).
- `plt.style.use.md` reubicada en el árbol a `config/` (donde está en disco), no en `pyplot/config/`.
- Integrado el antiguo esqueleto pendiente (`<details>`) dentro del árbol, en sus carpetas, como hojas sin `✅`.
- Añadidas marcas `✅` a las 23 notas existentes y sección "Estado actual".

### Próximos pasos sugeridos

- Crear las clases base que vertebran el modelo de objetos: `figure/Figure.md`, `axes/Axes.md`, `lines/Line2D.md`.
- Considerar una carpeta `conceptos_transversales/` (modelo `Figure → Axes → Artist`, backends, el bucle de render) al estilo del vault NumPy.

---

## Notas relacionadas

- [[introduccion]]
- [[Estandarizan Directorio Librerias]]
