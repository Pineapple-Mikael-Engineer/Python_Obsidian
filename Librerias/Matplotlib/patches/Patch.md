---
title: Patch — Clase base de todas las formas rellenas
aliases:
  - Patch
  - patches.Patch
  - parche

tags:
  - matplotlib
  - api/clase
  - plot/formas

# --- Clasificación ---
lib: matplotlib
obj: Patch
mod: matplotlib.patches
tipo: clase

# --- Comportamiento ---
retorna: Patch
muta_estado: false

# --- Dependencias ---
requiere:
  - concepto_artist

draft: false
---

# Patch — Clase base de todas las formas rellenas

## Definición

`Patch` es la **clase base abstracta** de la que heredan todas las formas geométricas rellenas de Matplotlib: `Rectangle`, `Circle`, `Polygon`, `Ellipse`, `Wedge`, `Arrow`, etc. Es un [[concepto_artist|Artist]] primitivo, así que **no se dibuja solo**: hay que añadirlo al Axes con `ax.add_patch(patch)`. No se instancia directamente (es abstracta); cada subclase define su geometría pero **hereda de aquí todas las propiedades de estilo** (relleno, borde, transparencia, tramado).

## Firma del constructor

No se construye a mano; sirve de referencia de los kwargs que aceptan **todas** las subclases:

```python
from matplotlib.patches import Patch

Patch(
    *,
    edgecolor=None,    # color del borde (alias ec)
    facecolor=None,    # color de relleno (alias fc)
    color=None,        # fija edgecolor Y facecolor a la vez
    linewidth=None,    # grosor del borde en puntos (alias lw)
    linestyle=None,    # estilo del borde (alias ls): '-', '--', ':', '-.'
    antialiased=None,  # suavizado de bordes
    hatch=None,        # patrón de tramado: '/', '\\', '|', '-', '+', 'x', 'o', '.', '*'
    fill=True,         # si False, solo dibuja el borde (sin relleno)
    alpha=None,        # transparencia 0..1
    zorder=1,          # orden de dibujo (mayor = encima)
    **kwargs
)
```

## Parámetros / propiedades

Heredadas por todas las subclases. Cada una se lee con `get_<prop>()` y se escribe con `set_<prop>(valor)`.

| Propiedad | Alias kwarg | Setter | Tipo / valores | Por defecto |
|-----------|-------------|--------|----------------|-------------|
| facecolor | `fc` | `set_facecolor(c)` | nombre, hex, RGB(A), `'none'` | según rcParams |
| edgecolor | `ec` | `set_edgecolor(c)` | nombre, hex, RGB(A), `'none'` | según rcParams |
| color | — | `set_color(c)` | fija facecolor y edgecolor juntos | — |
| linewidth | `lw` | `set_linewidth(w)` | float (puntos) | rcParams |
| linestyle | `ls` | `set_linestyle(s)` | `'-'`, `'--'`, `':'`, `'-.'` | `'-'` |
| alpha | — | `set_alpha(a)` | float 0..1 o `None` | `None` |
| fill | — | `set_fill(b)` | `True` / `False` | `True` |
| hatch | — | `set_hatch(s)` | `'/'`, `'\\'`, `'x'`, `'o'`, `'.'`, ... | `None` |
| zorder | — | `set_zorder(z)` | float (mayor = encima) | `1` |

```python
p.set(facecolor='skyblue', edgecolor='navy', lw=2, alpha=0.5)   # set() agrupa cambios
```

## Cómo añadirlo al Axes

Un `Patch` es un Artist que **no se dibuja solo**; debe registrarse en el Axes:

```python
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

fig, ax = plt.subplots()
p = Rectangle((0.2, 0.2), 0.5, 0.3, facecolor='salmon')
ax.add_patch(p)            # ← imprescindible: lo añade a ax.patches
plt.show()
```

`ax.add_patch(p)` devuelve el mismo patch y lo guarda en la lista `ax.patches`.

## Casos de uso

### Estilizar de forma uniforme con la API común

```python
p.set_facecolor('gold')       # cambia relleno
p.set_edgecolor('black')      # cambia borde
p.set_hatch('//')             # añade tramado diagonal
p.get_facecolor()             # → (1.0, 0.843, 0.0, 1.0)  RGBA
```

### Solo contorno, sin relleno

```python
p.set_fill(False)             # equivale a facecolor='none'
# útil para resaltar regiones sin tapar lo que hay debajo
```

### Proxy para leyenda

```python
from matplotlib.patches import Patch
proxy = Patch(facecolor='steelblue', edgecolor='k', label='región A')
ax.legend(handles=[proxy])    # Patch sirve de "handle" de leyenda
```

## Buenas prácticas

1. Recuerda siempre `ax.add_patch(p)`: sin esa llamada la forma existe pero no aparece.
2. Usa `facecolor='none'` o `set_fill(False)` para resaltar regiones sin ocultar los datos.
3. Agrupa estilos con `p.set(...)` en lugar de varios `set_*` encadenados.
4. Sube el `zorder` si la forma debe quedar por encima de las líneas de datos.
5. Para muchas formas iguales, considera una `PatchCollection`: es más eficiente que añadir cientos de patches sueltos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El patch no aparece | falta `ax.add_patch(p)` | añadirlo explícitamente al Axes |
| El relleno tapa los datos | `facecolor` opaco con `zorder` alto | usar `alpha` o `facecolor='none'` |
| `Patch()` no dibuja nada útil | es clase **abstracta**, sin geometría | instanciar una subclase (`Rectangle`, `Circle`, ...) |
| `color=` ignora `facecolor=` | `color` fija ambos a la vez | usar `facecolor`/`edgecolor` por separado |
| Tramado invisible | `hatch` requiere `edgecolor` definido | fijar `edgecolor` distinto de `'none'` |

## Notas relacionadas

- [[concepto_artist]]
- [[Rectangle]]
- [[Circle]]
- [[Polygon]]
- [[Ellipse]]
- [[ax.add_patch]]
- [[PatchCollection]]
