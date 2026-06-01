---
title: Annotation — Texto con flecha que devuelve ax.annotate
aliases:
  - Annotation
  - anotación
  - text.Annotation

tags:
  - matplotlib
  - api/clase
  - styling

# --- Clasificación ---
lib: matplotlib
obj: Annotation
mod: matplotlib.text
tipo: clase

# --- Comportamiento ---
retorna: Annotation
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_artist

draft: false
---

# Annotation — Texto con flecha que devuelve ax.annotate

## Definición

`Annotation` es una **subclase de** [[Text]] que añade un **punto señalado** y una **flecha opcional** que conecta el texto con ese punto. Hereda todas las propiedades de texto (`text`, `color`, `fontsize`, `ha`, `va`, ...) y suma `xy` (el punto al que apunta), `xytext` (dónde se coloca la cadena) y `arrowprops` (estilo de la flecha). Es un [[concepto_artist|Artist]] y es el tipo de objeto que devuelve [[ax.annotate]].

## Constructor

Raramente se construye a mano (lo crea `ax.annotate`), pero su firma define lo que añade sobre `Text`:

```python
from matplotlib.text import Annotation

a = Annotation(
    text,                 # cadena a mostrar
    xy,                   # (x, y) del punto señalado
    *,
    xytext=None,          # (x, y) donde se ubica el texto (por defecto = xy)
    xycoords='data',      # sistema de coordenadas de xy
    textcoords=None,      # sistema de coordenadas de xytext
    arrowprops=None,      # dict que define y activa la flecha
    **kwargs              # heredados de Text: color, fontsize, ha, va, ...
)
ax.add_artist(a)
```

En la práctica:

```python
a = ax.annotate('pico', xy=(2, 5), xytext=(3, 7),
                arrowprops=dict(arrowstyle='->'))
a.set_color('crimson')   # muta el objeto ya dibujado
```

## Propiedades clave (set_ / get_)

Hereda las de `Text` y añade las específicas de anotación. Mutan el estado del objeto.

| Propiedad | Setter | Getter | Origen | Tipo / valores |
|-----------|--------|--------|--------|----------------|
| text | `set_text(s)` | `get_text()` | Text | str |
| xy (punto señalado) | `set_position(xy)` vía atributo `xy` | atributo `.xy` | Annotation | tupla `(x, y)` |
| xytext (posición del texto) | `set_position((x, y))` | `get_position()` | Text | tupla `(x, y)` |
| arrowprops | atributo `.arrowprops` | atributo `.arrowprops` | Annotation | dict o `None` |
| color | `set_color(c)` | `get_color()` | Text | nombre, hex, RGB(A) |
| fontsize | `set_fontsize(s)` | `get_fontsize()` | Text | float |
| ha | `set_horizontalalignment(a)` | `get_horizontalalignment()` | Text | `'left'`, `'center'`, `'right'` |
| va | `set_verticalalignment(a)` | `get_verticalalignment()` | Text | `'top'`, `'center'`, `'bottom'`, `'baseline'` |
| rotation | `set_rotation(r)` | `get_rotation()` | Text | grados |

Claves frecuentes dentro de `arrowprops`:

| Clave | Qué controla | Valores típicos |
|-------|--------------|-----------------|
| arrowstyle | forma de la flecha | `'->'`, `'-|>'`, `'fancy'`, `'wedge'` |
| color | color de la flecha | nombre, hex, RGB(A) |
| lw | grosor de la línea | float |
| connectionstyle | curvatura del conector | `'arc3,rad=0.2'`, `'angle3'` |
| shrink | margen entre flecha y extremos | float 0..1 |

## Casos de uso

### Anotar un punto con flecha

```python
fig, ax = plt.subplots()
ax.plot(x, y)
a = ax.annotate('máximo', xy=(2, 5), xytext=(3, 7),
                arrowprops=dict(arrowstyle='->', color='black'))
```

### Anotación sin flecha (solo texto reubicado)

```python
a = ax.annotate('nota', xy=(1, 1), xytext=(2, 2))
# sin arrowprops no se dibuja flecha: equivale a un Text desplazado
```

### Flecha curvada y caja de fondo

```python
a = ax.annotate('detalle', xy=(4, 2), xytext=(6, 4),
                arrowprops=dict(arrowstyle='-|>',
                                connectionstyle='arc3,rad=0.3'),
                bbox=dict(boxstyle='round', facecolor='wheat'))
```

### Coordenadas relativas al eje

```python
a = ax.annotate('esquina', xy=(0.5, 0.5), xycoords='data',
                xytext=(0.9, 0.9), textcoords='axes fraction')
```

## Buenas prácticas

1. Define `arrowprops` solo cuando quieras flecha; sin él, `annotate` se comporta como texto desplazado.
2. Distingue `xy` (lo señalado) de `xytext` (dónde va la cadena): confundirlos invierte la flecha.
3. Usa `xycoords` / `textcoords` para mezclar coordenadas de datos y de eje según convenga.
4. Reutiliza el objeto devuelto y muta con `set_*` en lugar de recrear la anotación.
5. Para texto sin punto señalado ni flecha, prefiere [[ax.text]] por simplicidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| No aparece flecha | falta `arrowprops` | pasa `arrowprops=dict(arrowstyle='->')` |
| Flecha apunta al lugar equivocado | `xy` y `xytext` intercambiados | `xy` = punto señalado, `xytext` = texto |
| `xytext` ignorado | se omitió y toma el valor de `xy` | indica `xytext` explícito para separar el texto |
| Flecha recta cuando se quería curva | falta `connectionstyle` | añade `connectionstyle='arc3,rad=0.2'` |
| Coordenadas no coinciden | `xycoords`/`textcoords` mal elegidos | usa `'data'` o `'axes fraction'` de forma consistente |

## Limitaciones

`Annotation` está pensada para señalar un punto concreto; para texto suelto sin ancla la sobrecarga de `xy`/`arrowprops` es innecesaria. Las flechas complejas se controlan por completo desde el dict `arrowprops`, no con métodos `set_*` dedicados.

## Notas relacionadas

- [[Text]]
- [[ax.annotate]]
- [[concepto_artist]]
- [[ax.text]]
