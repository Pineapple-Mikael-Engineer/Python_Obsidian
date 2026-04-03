---
title: Tree_Matplotlib — Tree Matplotlib
aliases:
  - Tree Matplotlib
  - Tree_Matplotlib
tags:
  - matplotlib
  - api/clase
  - api/clase
lib: matplotlib
tipo: clase
muta_estado: false
requiere: []
draft: true
---





# Tree

```tree
Matplotlib/
├── Configuracion.md
├── Figura_Ejes/
│   ├── plt.subplots.md
│   ├── plt.figure.md
│   ├── figsize_dpi.md
│   └── add_subplot.md
│   └── Manejo_Arrays_Axes.md
├── Tipos_Plot/
│   ├── Lineas/
│   │   ├── ax.plot.md
│   │   └── Estilos_Linea/
│   │       ├── marker.md
│   │       └── linestyle.md
│   ├── Dispersión/
│   │   ├── ax.scatter.md
│   │   └── colormap_en_scatter.md
│   ├── Barras/
│   │   ├── ax.bar.md
│   │   ├── ax.barh.md
│   │   └── Barras_Apiladas.md
│   ├── Distribuciones/
│   │   ├── ax.hist.md
│   │   └── ax.boxplot.md
│   ├── Contornos_Imagenes/
│   │   ├── ax.contour.md
│   │   ├── ax.contourf.md
│   │   └── ax.imshow.md
│   └── Otros/
│       ├── ax.fill_between.md
│       └── ax.pie.md
├── Ejes_Formato/
│   ├── Limites_Escalas.md
│   ├── Ticks/
│   │   ├── ax.set_xticks_yticks.md
│   │   ├── ax.tick_params.md
│   │   └── Formato_Ticks/
│   │       ├── Locators.md
│   │       ├── Formatters.md
│   │       ├── DateFormatter.md
│   │       └── FuncFormatter.md
│   └── ax.grid.md
├── Labels_Leyendas/
│   ├── ax.set_title.md
│   ├── ax.set_xlabel_ylabel.md
│   └── ax.legend.md
├── Anotaciones/
│   ├── ax.text.md
│   └── ax.annotate.md
├── Color_Estilo/
│   ├── Colores_Nombres.md
│   ├── Colormaps/
│   │   ├── reversed.md
│   │   └── ListedColormap.md
│   └── plt.colorbar.md
├── Multiples_Graficos/
│   ├── subplots_adjust_tight.md
│   ├── GridSpec.md
│   └── Ejes_Compartidos.md
├── Guardar_Exportar/
│   ├── plt.savefig.md
│   └── Formatos/
│       ├── pdf_svg.md
│       └── transparent.md
└── Control/
    ├── plt.show.md
    └── plt.close_clf.md
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

## Notas relacionadas

- [[Tree_Matplotlib]]
