---
title: Tree Matplotlib
draft: true
---

# Tree Matplotlib (Estructura actual)

```tree
Matplotlib/
├── pyplot/
│   ├── funciones/
│   │   └── plt.subplots.md
│   └── config/
│       └── plt.style.use.md
├── figure/
│   └── metodos/
├── axes/
│   ├── arrays.md
│   └── metodos/
│       ├── graficos/
│       │   ├── ax.bar.md
│       │   ├── ax.barh.md
│       │   ├── ax.contour.md
│       │   ├── ax.fill_between.md
│       │   ├── ax.fill_betweenx.md
│       │   ├── ax.hist.md
│       │   ├── ax.plot.md
│       │   └── ax.scatter.md
│       ├── formato/
│       │   ├── ax.grid.md
│       │   ├── ax.legend.md
│       │   ├── ax.set_title.md
│       │   ├── ax.set_xlabel.md
│       │   ├── ax.set_xticks.md
│       │   ├── ax.set_ylabel.md
│       │   ├── ax.set_yticks.md
│       │   └── ax.tick_params.md
│       ├── anotaciones/
│       └── spines/
├── backend/
├── cm/
├── collections/
├── config/
│   ├── plt.style.use.md
│   └── rcParams.md
├── gridspec/
│   └── GridSpec.md
├── image/
├── lines/
├── patches/
├── text/
├── ticker/
│   └── Locators.md
├── toolkits/
│   └── mplot3d/
├── introduccion.md
└── REPORTE_REFACTORIZACION.md
```

## Notas existentes: 26 archivos

| Módulo | Archivos existentes |
|--------|---------------------|
| pyplot/funciones/ | plt.subplots.md |
| pyplot/config/ | plt.style.use.md |
| axes/metodos/graficos/ | ax.bar.md, ax.barh.md, ax.contour.md, ax.fill_between.md, ax.fill_betweenx.md, ax.hist.md, ax.plot.md, ax.scatter.md |
| axes/metodos/formato/ | ax.grid.md, ax.legend.md, ax.set_title.md, ax.set_xlabel.md, ax.set_xticks.md, ax.set_ylabel.md, ax.set_yticks.md, ax.tick_params.md |
| axes/ | arrays.md |
| config/ | rcParams.md |
| gridspec/ | GridSpec.md |
| ticker/ | Locators.md |
| raíz | introduccion.md, REPORTE_REFACTORIZACION.md |

## Notas pendientes por crear (esqueleto)

<details>
<summary>Hacer clic para ver lista completa</summary>

```bash
# pyplot/funciones/
plt.figure.md
plt.savefig.md
plt.show.md
plt.close.md
plt.clf.md
plt.colorbar.md

# figure/
Figure.md
figure/metodos/fig.suptitle.md
figure/metodos/fig.tight_layout.md
figure/metodos/fig.add_subplot.md

# axes/
Axes.md
axes/metodos/anotaciones/ax.text.md
axes/metodos/anotaciones/ax.annotate.md
axes/metodos/spines/ax.spines.md
axes/metodos/formato/ax.set_xlim.md
axes/metodos/formato/ax.set_ylim.md
axes/metodos/formato/ax.set_xscale.md
axes/metodos/formato/ax.set_yscale.md
axes/metodos/formato/ax.set_facecolor.md
axes/metodos/graficos/ax.boxplot.md
axes/metodos/graficos/ax.contourf.md
axes/metodos/graficos/ax.imshow.md
axes/metodos/graficos/ax.pie.md

# gridspec/
GridSpecFromSubplotSpec.md

# ticker/
Formatters.md
DateFormatter.md
FuncFormatter.md

# cm/
Colormaps.md
ListedColormap.md

# patches/
Patch.md
Rectangle.md
Polygon.md
Circle.md
Ellipse.md

# collections/
PathCollection.md
QuadContourSet.md

# image/
imread.md
imsave.md

# text/
Text.md
Annotation.md

# lines/
Line2D.md
marker.md

# animation/
FuncAnimation.md

# backend/
backends.md
cambiar_backend.md

# toolkits/mplot3d/
plot_surface.md
axes3d.md

# config/
estilos.md
```
</details>

## Notas relacionadas

- [[REPORTE_REFACTORIZACION]]
- [[introduccion]]
