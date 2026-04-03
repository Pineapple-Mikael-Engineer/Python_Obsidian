---
title: Tree Matplotlib
draft: true
---
# Tree

```tree
Matplotlib/
├── pyplot/
│   ├── funciones/
│   │   ├── plt.subplots.md
│   │   ├── plt.figure.md
│   │   ├── plt.savefig.md
│   │   ├── plt.show.md
│   │   ├── plt.close.md
│   │   ├── plt.clf.md
│   │   └── plt.colorbar.md
│   └── config/
│       └── plt.style.use.md
├── figure/
│   ├── Figure.md
│   └── metodos/
│       ├── fig.suptitle.md
│       ├── fig.tight_layout.md
│       └── fig.add_subplot.md
├── axes/
│   ├── Axes.md
│   └── metodos/
│       ├── graficos/
│       │   ├── ax.plot.md
│       │   ├── ax.scatter.md
│       │   ├── ax.bar.md
│       │   ├── ax.barh.md
│       │   ├── ax.hist.md
│       │   ├── ax.boxplot.md
│       │   ├── ax.contour.md
│       │   ├── ax.contourf.md
│       │   ├── ax.imshow.md
│       │   ├── ax.fill_between.md
│       │   └── ax.pie.md
│       ├── formato/
│       │   ├── ax.set_title.md
│       │   ├── ax.set_xlabel.md
│       │   ├── ax.set_ylabel.md
│       │   ├── ax.legend.md
│       │   ├── ax.grid.md
│       │   ├── ax.set_xlim.md
│       │   ├── ax.set_ylim.md
│       │   ├── ax.set_xscale.md
│       │   ├── ax.set_yscale.md
│       │   ├── ax.set_xticks.md
│       │   ├── ax.set_yticks.md
│       │   ├── ax.tick_params.md
│       │   └── ax.set_facecolor.md
│       ├── anotaciones/
│       │   ├── ax.text.md
│       │   └── ax.annotate.md
│       └── spines/
│           └── ax.spines.md
├── gridspec/
│   ├── GridSpec.md
│   └── GridSpecFromSubplotSpec.md
├── ticker/
│   ├── Locators.md
│   ├── Formatters.md
│   ├── DateFormatter.md
│   └── FuncFormatter.md
├── cm/
│   ├── Colormaps.md
│   └── ListedColormap.md
├── patches/
│   ├── Patch.md
│   ├── Rectangle.md
│   ├── Polygon.md
│   ├── Circle.md
│   └── Ellipse.md
├── collections/
│   ├── PathCollection.md
│   └── QuadContourSet.md
├── image/
│   ├── imread.md
│   └── imsave.md
├── text/
│   ├── Text.md
│   └── Annotation.md
├── lines/
│   ├── Line2D.md
│   └── marker.md
├── animation/
│   └── FuncAnimation.md
├── backend/
│   ├── backends.md
│   └── cambiar_backend.md
├── toolkits/
│   └── mplot3d/
│       ├── plot_surface.md
│       └── axes3d.md
└── config/
    ├── rcParams.md
    └── estilos.md
```

**chat** : [Chat](https://chat.deepseek.com/a/chat/s/e0e24ee8-216a-4703-b37b-4777590b5644)

# Futuro



## 1. La API Orientada a Objetos (El "verdadero" poder)

Mientras que `pyplot` gestiona cosas automáticamente, la API orientada a objetos te da el control total. Se basa en dos componentes principales:

- **Figure:** El lienzo completo o ventana donde se dibuja.
    
- **Axes:** El área específica donde se grafican los datos (un "gráfico" individual con sus ejes $x$ e $y$).
    

---

## 2. Matplotlib Patches y Shapes

No todo son líneas y puntos. El módulo `matplotlib.patches` permite dibujar formas geométricas complejas manualmente:

- **Círculos, Elipses y Rectángulos.**
    
- **Polígonos** con cualquier número de lados.
    
- **Flechas y cuñas** (útiles para diagramas de flujo o anotaciones personalizadas).
    

---

## 3. Manejo de Imágenes (`matplotlib.image`)

Matplotlib no solo genera gráficos, también es un procesador de imágenes básico. Con el módulo `image` puedes:

- Leer archivos (PNG, JPG).
    
- Visualizar matrices de datos como imágenes (mapas de calor o _heatmaps_).
    
- Aplicar filtros de interpolación y ajustar escalas de colores (_colormaps_).
    

---

## 4. Toolkits Especializados

Matplotlib incluye extensiones para nichos específicos que mucha gente olvida:

- **mplot3d:** Para visualizaciones en 3D (superficies, nubes de puntos tridimensionales).
    
- **AxesGrid:** Para crear rejillas de gráficos muy precisas y alineadas, común en publicaciones científicas.
    
- **Cartopy / Basemap:** (Aunque a veces requieren instalación extra) se integran con Matplotlib para crear mapas geográficos y proyecciones de la Tierra.
    

---

## 5. El Backend (La capa invisible)

Esta es la parte técnica que hace que Matplotlib funcione en cualquier lugar. Se divide en dos:

1. **Backends de Usuario (Interactivos):** Permiten que el gráfico aparezca en una ventana (usando librerías como Qt, Tkinter o GTK) y que puedas hacer zoom o moverte por el gráfico.
    
2. **Backends de Renderizado (Hardcopy):** Se encargan de convertir tus comandos en archivos reales como **PDF, SVG, EPS** (vectores) o **PNG, JPG** (píxeles).
    

---

## 6. Animaciones y Eventos

- **`matplotlib.animation`:** Permite crear GIFs o videos (MP4) actualizando los datos de un gráfico en tiempo real.
    
- **Manejo de Eventos:** Puedes programar Matplotlib para que responda a clics del ratón o pulsaciones de teclas. Por ejemplo, que al hacer clic en un punto del gráfico, se muestre más información sobre ese dato.
    

---

## 7. Estilos y Tipografías (`rcParams`)

Matplotlib tiene un motor de configuración global llamado `rcParams`. Con esto puedes:

- Configurar el uso de **LaTeX** para fórmulas matemáticas complejas: $E = mc^2$.
    
- Cambiar estilos visuales completos (como `ggplot`, `seaborn` o el modo oscuro) con una sola línea de código.
    

