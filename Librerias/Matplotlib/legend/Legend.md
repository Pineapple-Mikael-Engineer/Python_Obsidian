---
title: Legend — El objeto leyenda que vive en el Axes
aliases:
  - Legend
  - objeto leyenda
tags:
  - matplotlib
  - api/clase
  - styling

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.legend
tipo: clase
obj: Legend

# --- Comportamiento ---
retorna: Legend
muta_estado: false

draft: false
---

# Legend — El objeto leyenda que vive en el Axes

## Definición

`Legend` es el `Artist` que **devuelve** [[ax.legend]]: representa el recuadro con los handles (marcadores/líneas de muestra) y sus etiquetas. Aunque normalmente se crea de forma implícita al llamar `ax.legend()`, guardar el retorno permite reposicionarlo, restilizarlo o reusarlo (por ejemplo para apilar varias leyendas en un mismo Axes).

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x, y, label='Datos')
leg = ax.legend()
type(leg)   # → <class 'matplotlib.legend.Legend'>
```

## Parámetros del constructor (kwargs de ax.legend)

Estos kwargs se pasan a través de `ax.legend(**kwargs)` y configuran el objeto resultante.

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `loc` | `str` o `int` | `'best'` | Posición dentro del Axes (`'upper right'`, `'best'`...) |
| `bbox_to_anchor` | tupla `(x, y[, w, h])` | `None` | Rectángulo de anclaje en coords del Axes; saca la leyenda fuera |
| `ncol` / `ncols` | `int` | `1` | Número de columnas (`ncols` es el alias moderno, ≥3.6) |
| `frameon` | `bool` | `True` | Dibuja o no el recuadro de fondo |
| `framealpha` | `float` | `0.8` | Opacidad del fondo (0=transparente, 1=opaco) |
| `fontsize` | `int` o `str` | `None` | Tamaño de las etiquetas (`'small'`, `12`...) |
| `title` | `str` | `None` | Título del recuadro de leyenda |
| `shadow` | `bool` | `False` | Sombra bajo el recuadro |

## Métodos y propiedades clave

| Miembro | Qué hace | Ejemplo |
|---------|----------|---------|
| `set_title(t)` | cambia el título tras crear | `leg.set_title('Curvas')` |
| `get_texts()` | lista de los `Text` de las etiquetas | `for t in leg.get_texts(): t.set_color('gray')` |
| `get_lines()` | handles de tipo línea | `leg.get_lines()` |
| `set_visible(b)` | muestra u oculta la leyenda | `leg.set_visible(False)` |
| `get_frame()` | el `Patch` del recuadro | `leg.get_frame().set_facecolor('0.9')` |
| `set_draggable(b)` | hace la leyenda arrastrable con el ratón | `leg.set_draggable(True)` |
| `remove()` | elimina la leyenda del Axes | `leg.remove()` |

## Casos de uso

### Guardar y reestilizar

```python
leg = ax.legend(title='Series', framealpha=0.5)
leg.get_frame().set_edgecolor('black')   # borde del recuadro
for txt in leg.get_texts():
    txt.set_fontstyle('italic')
```

### Recuperar la leyenda ya dibujada

```python
ax.plot(x, y, label='A')
ax.legend()
leg = ax.get_legend()    # → el mismo objeto Legend, sin recrearlo
leg.set_visible(False)   # ocultar sin borrar
```

### Leyenda arrastrable (interactivo)

```python
leg = ax.legend()
leg.set_draggable(True)  # el usuario la reposiciona con el ratón
```

## Buenas prácticas

1. Guarda el retorno (`leg = ax.legend(...)`) cuando vayas a modificarlo después: es la misma instancia que crea internamente el Axes.
2. Recuerda que `Legend` es un `Artist` más; expone el protocolo `get_*`/`set_*` descrito en [[concepto_artist]] para inspección y ajuste fino.
3. Usa `framealpha < 1` cuando la leyenda solape datos, para no taparlos por completo.
4. Para combinar varias leyendas en un mismo Axes, consulta la guía dedicada en vez de sobrescribir la existente.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ax.legend()` borra la leyenda anterior | cada llamada reemplaza la previa | Guardar la 1ª y reañadirla con `ax.add_artist` |
| `get_legend()` devuelve `None` | aún no se llamó a `legend()` | Crear primero con `ax.legend()` |
| El recuadro no cambia de color | se editó el `Legend`, no su frame | Usar `leg.get_frame().set_*` |
| `ncol` ignorado en versiones nuevas | API renombró a `ncols` | Usar `ncols` en Matplotlib ≥3.6 |

## Notas relacionadas

- [[ax.legend]]
- [[concepto_artist]]
- [[Personalizacion_Leyendas]]
- [[Multiples_Leyendas]]
- [[handles_labels]]
