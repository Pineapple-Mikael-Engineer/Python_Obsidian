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
├── 📁 conceptos_transversales/        (5/5 ✅ · modelo mental)
│   ├── ✅ concepto_figure_axes.md
│   ├── ✅ concepto_artist.md
│   ├── ✅ concepto_pyplot_vs_oo.md
│   ├── ✅ concepto_anatomia_figura.md
│   └── ✅ concepto_backend.md
│
├── 📁 pyplot/                         (7/7 ✅ completo)
│   └── 📁 funciones/
│       ├── ✅ plt.subplots.md
│       ├── ✅ plt.figure.md
│       ├── ✅ plt.savefig.md
│       ├── ✅ plt.show.md
│       ├── ✅ plt.close.md
│       ├── ✅ plt.clf.md
│       └── ✅ plt.colorbar.md
│
├── 📁 figure/                         (4/4 ✅ completo)
│   ├── ✅ Figure.md
│   └── 📁 metodos/
│       ├── ✅ fig.suptitle.md
│       ├── ✅ fig.tight_layout.md
│       └── ✅ fig.add_subplot.md
│
├── 📁 axes/                           (30/35)
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
│       │   └── ✅ ax.pie.md
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
│       │   └── ✅ ax.set_facecolor.md
│       │
│       ├── 📁 anotaciones/
│       │   ├── ✅ ax.text.md
│       │   └── ✅ ax.annotate.md
│       │
│       └── 📁 spines/
│           └── ✅ ax.spines.md
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
├── 📁 lines/                          (2/2 ✅ completo)
│   ├── ✅ Line2D.md
│   └── ✅ marker.md
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
| `conceptos_transversales/` | 5 | 5 | ✅ completo (modelo mental) |
| `pyplot/` | 7 | 7 | ✅ completo |
| `figure/` | 4 | 4 | ✅ completo |
| `config/` | 3 | 3 | ✅ completo |
| `gridspec/` | 2 | 2 | ✅ completo |
| `ticker/` | 4 | 4 | ✅ completo |
| `lines/` | 2 | 2 | ✅ completo |
| `axes/` (métodos + arrays) | 30 | 35 | en progreso (faltan algunos gráficos/anotaciones) |
| `cm/` · `patches/` · `collections/` · `image/` · `text/` · `animation/` · `backend/` · `toolkits/` | 0 | ~18 | pendiente (primitivos/Artists) |
| raíz (`introduccion.md`) | 1 | — | ✅ |
| **Total** | **58** | ~75 | — |

### Cambios de sincronización aplicados

- Conteo corregido: 23 → **58** notas reales tras los lotes de conceptos + relleno.
- Eliminada `REPORTE_REFACTORIZACION.md` del árbol y de notas relacionadas (no existe en disco).
- `plt.style.use.md` reubicada en el árbol a `config/` (donde está en disco), no en `pyplot/config/`.
- Integrado el antiguo esqueleto pendiente (`<details>`) dentro del árbol, en sus carpetas.
- Añadidas marcas `✅` a las 58 notas existentes y sección "Estado actual".
- Pendiente: módulos de Artists primitivos (`patches/`, `cm/`, `collections/`, `image/`, `text/`, `animation/`, `backend/`, `toolkits/mplot3d/`).

### Próximos pasos sugeridos

- ✅ `conceptos_transversales/` creada (figure_axes, artist, pyplot_vs_oo, anatomia_figura, backend).
- Crear las clases base que vertebran el modelo de objetos: `figure/Figure.md`, `axes/Axes.md`, `lines/Line2D.md`.
- Rellenar las hojas pendientes (pyplot, figure/metodos, axes/metodos restantes, ticker, patches…).

---

## Notas relacionadas

- [[introduccion]]
- [[Estandarizan Directorio Librerias]]
