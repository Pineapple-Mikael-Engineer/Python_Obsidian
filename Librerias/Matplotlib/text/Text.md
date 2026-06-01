---
title: Text — Objeto de texto que devuelve ax.text
aliases:
  - Text
  - objeto texto
  - text.Text

tags:
  - matplotlib
  - api/clase
  - styling

# --- Clasificación ---
lib: matplotlib
obj: Text
mod: matplotlib.text
tipo: clase

# --- Comportamiento ---
retorna: Text
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_artist

draft: false
---

# Text — Objeto de texto que devuelve ax.text

## Definición

`Text` es el objeto que representa **una cadena de texto dibujada** sobre los ejes o la figura. Es un [[concepto_artist|Artist]] primitivo: vive en el árbol de la figura, se redibuja en cada render y se manipula con sus métodos `set_*` / `get_*`. Es el tipo de objeto que devuelve [[ax.text]]; guardar esa referencia permite mover, recolorear o reformatear el texto sin volver a crearlo.

## Constructor

Raramente se construye a mano (lo crea `ax.text`), pero su firma define las propiedades disponibles:

```python
from matplotlib.text import Text

t = Text(
    x=0, y=0,             # posición en coordenadas de datos
    text='',              # cadena a mostrar
    *,
    color=None,           # color del texto
    fontsize=None,        # tamaño en puntos (alias size)
    fontweight=None,      # 'normal', 'bold', ...
    horizontalalignment='left',   # alias ha: 'left' | 'center' | 'right'
    verticalalignment='baseline', # alias va: 'top' | 'center' | 'bottom' | 'baseline'
    rotation=None,        # grados o 'horizontal' | 'vertical'
    bbox=None,            # dict de caja de fondo
    **kwargs
)
ax.add_artist(t)          # hay que añadirlo manualmente
```

En la práctica:

```python
t = ax.text(0.5, 0.5, 'hola')   # devuelve el Text ya añadido
t.set_color('crimson')          # muta el objeto ya dibujado
```

## Propiedades clave (set_ / get_)

Cada propiedad se lee con `get_<prop>()` y se escribe con `set_<prop>(valor)`. Mutan el estado del objeto.

| Propiedad | Setter | Getter | Alias kwarg | Tipo / valores |
|-----------|--------|--------|-------------|----------------|
| text | `set_text(s)` | `get_text()` | — | str (acepta `$...$` LaTeX) |
| position | `set_position((x, y))` | `get_position()` | — | tupla `(x, y)` |
| color | `set_color(c)` | `get_color()` | `c` | nombre, hex, RGB(A) |
| fontsize | `set_fontsize(s)` | `get_fontsize()` | `size` | float o `'small'`, `'large'`, ... |
| fontweight | `set_fontweight(w)` | `get_fontweight()` | `weight` | `'normal'`, `'bold'`, número 0..1000 |
| ha | `set_horizontalalignment(a)` | `get_horizontalalignment()` | `ha` | `'left'`, `'center'`, `'right'` |
| va | `set_verticalalignment(a)` | `get_verticalalignment()` | `va` | `'top'`, `'center'`, `'bottom'`, `'baseline'` |
| rotation | `set_rotation(r)` | `get_rotation()` | — | grados, `'horizontal'`, `'vertical'` |
| bbox | `set_bbox(d)` | — | — | dict (`facecolor`, `edgecolor`, `boxstyle`, ...) |
| visible | `set_visible(b)` | `get_visible()` | — | `True` / `False` |

Atajo `set()` para varias a la vez:

```python
t.set(color='navy', fontsize=14, fontweight='bold', rotation=30)
```

## Casos de uso

### Modificar un texto después de crearlo

```python
fig, ax = plt.subplots()
t = ax.text(0.5, 0.5, 'borrador')
t.set_text('versión final')
t.set_color('darkgreen')
t.get_text()          # → 'versión final'
```

### Reposicionar y alinear

```python
t = ax.text(1, 1, 'etiqueta')
t.set_position((2, 3))
t.set_horizontalalignment('center')
t.set_verticalalignment('bottom')
```

### Texto con caja de fondo

```python
t = ax.text(0.5, 0.5, 'destacado')
t.set_bbox(dict(facecolor='yellow', edgecolor='black', boxstyle='round'))
```

## Buenas prácticas

1. Guarda la referencia que devuelve `ax.text` solo si vas a modificar el texto después.
2. Usa `set()` para agrupar varios cambios de estilo y mejorar la legibilidad.
3. Prefiere mutar con `set_text` / `set_position` antes que borrar y recrear el Artist.
4. Usa `ha`/`va` para controlar exactamente el anclaje respecto a la coordenada dada.
5. Para texto con flecha apuntando a un punto, usa [[Annotation]] en lugar de un `Text` simple.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Texto aparece desalineado | `ha`/`va` por defecto distintos de lo esperado | fija `set_horizontalalignment` / `set_verticalalignment` |
| `$...$` no se renderiza como matemática | falta el modo math correcto | encierra la expresión en `$...$` y escapa con raw string |
| Texto fuera de los ejes | coordenadas en datos fuera de los límites | usa `transform=ax.transAxes` para coords relativas 0..1 |
| Cambios no se ven | falta refrescar el canvas interactivo | `fig.canvas.draw_idle()` |
| Confundir `set_text` con `set_label` | `label` es para leyenda, no el contenido | usa `set_text` para el contenido visible |

## Notas relacionadas

- [[concepto_artist]]
- [[ax.text]]
- [[Annotation]]
- [[ax.annotate]]
