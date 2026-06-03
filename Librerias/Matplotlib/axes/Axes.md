---
title: Axes — La región de ploteo de Matplotlib
aliases:
  - Axes
  - ax
  - ejes
  - region de ploteo

tags:
  - matplotlib
  - api/clase
  - estructura

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: clase

# --- Comportamiento ---
retorna: Axes
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_figure_axes

draft: false
---

# Axes — La región de ploteo de Matplotlib

## Qué es

Un `Axes` es **la región de ploteo individual**: el sistema de coordenadas rectangular donde realmente se dibujan los datos. Es el objeto **central** de Matplotlib, donde ocurre el 95% del trabajo: trazar curvas (`ax.plot`), pintar imágenes (`ax.imshow`), poner títulos y formatear ejes (`ax.set_*`).

No debe confundirse con un `Axis` (singular): un `Axes` **contiene** dos (o tres) objetos `Axis` —el eje X y el eje Y—, pero el `Axes` es la región completa. La jerarquía contenedora completa (Figure → Axes → Axis) se explica en [[concepto_figure_axes]].

**Regla mental:** un `Figure` es el lienzo y contiene N `Axes`; cada `Axes` es un subgrafo con sus propios datos, límites, ticks y leyenda.

## Cómo se obtiene

La vía idiomática es [[plt.subplots]], que crea el `Figure` y sus `Axes` de una sola llamada:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()          # 1 Figure + 1 Axes suelto
fig, axs = plt.subplots(2, 3)     # axs: array (2,3) de Axes
```

| Forma | Resultado | Acceso |
|-------|-----------|--------|
| `plt.subplots()` | un `Axes` suelto | `ax.plot(...)` |
| `plt.subplots(2, 2)` | array `(2,2)` de `Axes` | `axs[0, 1].plot(...)` |
| `plt.subplots(1, 3)` | array `(3,)` de `Axes` | `for ax in axs: ...` |
| `fig.add_subplot(111)` | un `Axes` añadido al `Figure` | `ax.plot(...)` |
| `fig.add_axes([l,b,w,h])` | `Axes` en posición manual (0-1) | `ax.plot(...)` |

Casi nunca se instancia `Axes(...)` directamente: siempre se obtiene desde un `Figure`.

## Métodos clave

### Métodos gráficos (crean Artists)

| Método | Dibuja | Retorna |
|--------|--------|---------|
| [[ax.plot]] | líneas / curvas | lista de `Line2D` |
| `ax.scatter` | nube de puntos | `PathCollection` |
| `ax.bar` / `ax.barh` | barras | `BarContainer` |
| [[ax.boxplot]] | caja y bigotes (distribución) | dict de Artists |
| `ax.hist` | histograma | `(n, bins, patches)` |
| [[ax.contourf]] | contornos rellenos | `QuadContourSet` |
| `ax.contour` | contornos de línea | `QuadContourSet` |
| [[ax.imshow]] | matriz/imagen como píxeles | `AxesImage` |
| [[ax.pie]] | sectores circulares | `(wedges, texts[, autotexts])` |

### Métodos de formato (configuran el Axes)

| Método | Controla | Ejemplo |
|--------|----------|---------|
| `ax.set_title` | título del subgrafo | `ax.set_title("Señal")` |
| `ax.set_xlabel` / `ax.set_ylabel` | etiquetas de ejes | `ax.set_xlabel("t [s]")` |
| `ax.set_xlim` / `ax.set_ylim` | límites de los ejes | `ax.set_xlim(0, 10)` |
| `ax.set_xticks` / `ax.set_yticks` | posiciones de marcas | `ax.set_xticks([0,5,10])` |
| `ax.set_xscale` / `ax.set_yscale` | escala (lin/log) | `ax.set_yscale("log")` |
| `ax.legend` | leyenda (usa `label`) | `ax.legend()` |
| `ax.grid` | rejilla | `ax.grid(True)` |
| `ax.set` | varios a la vez | `ax.set(title="t", xlim=(0,1))` |

Como muestra la tabla de reparto de responsabilidades en [[concepto_figure_axes]], lo que afecta a un subgrafo vive en el `Axes`; lo que afecta a todo el lienzo (guardar, título global) vive en el `Figure`.

## Atributos

Cada `Axes` mantiene listas de los Artists que contiene. Son útiles para inspeccionar o modificar el contenido después de dibujarlo.

| Atributo | Contiene | Tipo |
|----------|----------|------|
| `ax.lines` | las líneas dibujadas con `plot` | lista de `Line2D` |
| `ax.patches` | parches (barras, cuñas de pie, polígonos) | lista de `Patch` |
| `ax.images` | imágenes de `imshow` | lista de `AxesImage` |
| `ax.collections` | colecciones (`scatter`, contornos) | lista de `Collection` |
| `ax.texts` | textos sueltos añadidos | lista de `Text` |
| `ax.xaxis` / `ax.yaxis` | los ejes individuales | `Axis` |
| `ax.figure` | el `Figure` contenedor | `Figure` |
| `ax.title` | el Artist del título | `Text` |

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3])
len(ax.lines)            # 1
ax.lines[0].set_color("red")   # modificar la línea ya dibujada
```

Todos estos objetos son [[concepto_artist]]: la clase base de todo lo dibujable en Matplotlib.

## Ejemplo de ciclo de vida

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)

fig, ax = plt.subplots(figsize=(6, 4))   # crear Figure + Axes
ax.plot(x, np.sin(x), label="sin")       # dibujar (muta el Axes)
ax.plot(x, np.cos(x), label="cos")
ax.set_title("Funciones trigonométricas")  # formatear
ax.set_xlabel("x [rad]")
ax.set_ylabel("y")
ax.legend()                              # leyenda con los labels
ax.grid(True)

fig.savefig("trig.png")                  # guardar (responsabilidad del Figure)
```

## Buenas prácticas

1. Usa siempre la interfaz orientada a objetos (`ax.metodo(...)`) en lugar de `plt.metodo(...)`; es explícita y escala a múltiples subgrafos.
2. Crea `Figure` y `Axes` juntos con `plt.subplots(...)` y nombra `ax` (o `axs`) de forma clara.
3. Pasa `figsize` al crear el `Axes` para fijar proporciones desde el principio.
4. Agrupa primero los métodos gráficos y después los de formato (`set_*`, `legend`, `grid`).
5. Guarda la referencia del Artist retornado si vas a modificarlo después.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'numpy.ndarray' object has no attribute 'plot'` | indexar mal un array de Axes | usar `axs[i, j].plot(...)` |
| Confundir `Axes` con `Axis` | son objetos distintos | `Axes` = región; `Axis` = eje X o Y |
| `ax.title("t")` falla | `title` es atributo, no método | usar `ax.set_title("t")` |
| Leyenda vacía | no se pasó `label` al graficar | pasar `label=...` y luego `ax.legend()` |
| Mezclar `plt.*` con `ax.*` y perder el subgrafo activo | `plt` apunta al "Axes actual" | usar siempre el `ax` explícito |

## Notas relacionadas

- [[concepto_figure_axes]]
- [[concepto_artist]]
- [[plt.subplots]]
- [[ax.plot]]
- [[ax.boxplot]]
- [[ax.contourf]]
- [[ax.imshow]]
- [[ax.pie]]
