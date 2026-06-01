---
title: Line2D — Objeto línea que devuelve ax.plot
aliases:
  - Line2D
  - objeto línea
  - lines.Line2D

tags:
  - matplotlib
  - api/clase
  - plot/lineas

# --- Clasificación ---
lib: matplotlib
obj: Line2D
mod: matplotlib.lines
tipo: clase

# --- Comportamiento ---
retorna: Line2D
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_artist

draft: false
---

# Line2D — Objeto línea que devuelve ax.plot

## Definición

`Line2D` es el objeto que representa **una línea** (con sus marcadores) en unos ejes. Es el tipo de objeto que devuelve [[ax.plot]] dentro de la lista de retorno, y es un [[concepto_artist|Artist]]: vive en el árbol de la figura y se redibuja en cada render. Una vez creado, se manipula con sus métodos `set_*` / `get_*` en lugar de volver a llamar a `plot`.

## Constructor

Raramente se construye a mano (lo crea `ax.plot`), pero su firma define las propiedades disponibles:

```python
from matplotlib.lines import Line2D

linea = Line2D(
    xdata,                # secuencia de coordenadas x
    ydata,                # secuencia de coordenadas y
    *,
    color=None,           # color de la línea
    linewidth=None,       # grosor en puntos (alias lw)
    linestyle=None,       # estilo de trazo (alias ls)
    marker=None,          # estilo de marcador
    markersize=None,      # tamaño del marcador (alias ms)
    alpha=None,           # transparencia 0..1
    label=None,           # etiqueta para la leyenda
    zorder=2,             # orden de dibujo
    **kwargs
)
ax.add_line(linea)        # hay que añadirla al Axes manualmente
```

En la práctica:

```python
linea, = ax.plot(x, y)    # la coma desempaqueta la lista de 1 Line2D
linea.set_color('red')    # muta el objeto ya dibujado
```

## Propiedades clave (set_ / get_)

Cada propiedad se lee con `get_<prop>()` y se escribe con `set_<prop>(valor)`. Mutan el estado del objeto.

| Propiedad | Setter | Getter | Alias kwarg | Tipo / valores |
|-----------|--------|--------|-------------|----------------|
| color | `set_color(c)` | `get_color()` | `c` | nombre, hex, RGB(A), gris `'0.5'` |
| linewidth | `set_linewidth(w)` | `get_linewidth()` | `lw` | float (puntos) |
| linestyle | `set_linestyle(s)` | `get_linestyle()` | `ls` | `'-'`, `'--'`, `':'`, `'-.'`, `'none'` |
| marker | `set_marker(m)` | `get_marker()` | — | código de marcador (`'o'`, `'s'`, ...) |
| markersize | `set_markersize(s)` | `get_markersize()` | `ms` | float (puntos) |
| markerfacecolor | `set_markerfacecolor(c)` | `get_markerfacecolor()` | `mfc` | color de relleno |
| markeredgecolor | `set_markeredgecolor(c)` | `get_markeredgecolor()` | `mec` | color de borde |
| alpha | `set_alpha(a)` | `get_alpha()` | — | float 0..1 o `None` |
| label | `set_label(s)` | `get_label()` | — | str (leyenda) |
| zorder | `set_zorder(z)` | `get_zorder()` | — | float (mayor = encima) |
| xdata / ydata | `set_xdata(x)` / `set_ydata(y)` | `get_xdata()` / `get_ydata()` | — | secuencia / array |
| visible | `set_visible(b)` | `get_visible()` | — | `True` / `False` |

Atajo `set()` para varias a la vez:

```python
linea.set(color='navy', lw=2, ls='--', marker='o')
```

## Casos de uso

### Modificar una línea después de crearla

```python
fig, ax = plt.subplots()
linea, = ax.plot(x, y)
linea.set_color('crimson')
linea.set_linewidth(3)
linea.set_linestyle('--')
linea.get_color()          # → 'crimson'
```

### Animar / actualizar datos sin recrear la línea

```python
linea, = ax.plot(x, y)
linea.set_ydata(y_nuevo)   # solo cambia Y, reutiliza el mismo Artist
fig.canvas.draw_idle()
```

### Iterar sobre varias líneas devueltas por plot

```python
lineas = ax.plot(x, y_matrix)   # lista de N Line2D
for ln in lineas:
    ln.set_alpha(0.6)
    ln.set_linewidth(1)
```

### Crear una entrada de leyenda "proxy"

```python
from matplotlib.lines import Line2D
proxy = Line2D([], [], color='gray', ls='--', label='referencia')
ax.legend(handles=[proxy])
```

## Buenas prácticas

1. Guarda la referencia (`linea, = ax.plot(...)`) solo si vas a modificarla después.
2. Prefiere mutar con `set_*` antes que borrar y volver a graficar: es más rápido y conserva `zorder`.
3. Usa `set()` para agrupar cambios y mejorar legibilidad.
4. Reutiliza la misma `Line2D` con `set_ydata` en animaciones; recrear líneas degrada el rendimiento.
5. Asigna `label` en la creación si usarás [[ax.plot]] junto a una leyenda.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `'list' object has no attribute 'set_color'` | `ax.plot` devuelve **lista**, no la línea | desempaqueta: `linea, = ax.plot(...)` |
| Cambios no se ven | falta refrescar el canvas en modo interactivo | `fig.canvas.draw_idle()` |
| `set_data` con longitudes distintas de x e y | `xdata` e `ydata` deben coincidir | igualar longitudes antes de `set_data` |
| Color ignorado tras `style.use` | la hoja de estilo fija colores por ciclo | aplica `set_color` después o usa `color=` explícito |
| Confundir `markersize` con `linewidth` | propiedades distintas | `ms` afecta marcador, `lw` afecta trazo |

## Notas relacionadas

- [[concepto_artist]]
- [[ax.plot]]
- [[marker]]
- [[Estilos_Linea]]
- [[Colores_Nombres]]
- [[ax.legend]]
