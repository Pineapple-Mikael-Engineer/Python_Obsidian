---
title: Personalizacion_Leyendas — Catálogo de opciones de estilo y posición
aliases:
  - Personalizacion_Leyendas
  - personalizar leyenda
  - opciones de legend
tags:
  - matplotlib
  - api/objeto
  - styling

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.legend
tipo: objeto
obj: Legend

# --- Comportamiento ---
retorna: Legend
muta_estado: false

draft: false
---

# Personalizacion_Leyendas — Catálogo de opciones de estilo y posición

## Definición

Referencia transversal de los kwargs que acepta [[ax.legend]] para ajustar **posición, layout y estilo** del recuadro. Todos se pasan en la misma llamada y configuran el objeto resultante (ver [[Legend]]).

## Posición — códigos de loc

| String | Código | Posición |
|--------|--------|----------|
| `'best'` | 0 | Automática (minimiza solapamiento) |
| `'upper right'` | 1 | Superior derecha |
| `'upper left'` | 2 | Superior izquierda |
| `'lower left'` | 3 | Inferior izquierda |
| `'lower right'` | 4 | Inferior derecha |
| `'right'` | 5 | Derecha |
| `'center left'` | 6 | Centro izquierda |
| `'center right'` | 7 | Centro derecha |
| `'lower center'` | 8 | Centro inferior |
| `'upper center'` | 9 | Centro superior |
| `'center'` | 10 | Centro |

```python
ax.legend(loc='upper left')   # posición fija dentro del Axes
```

## Sacar la leyenda fuera del Axes (bbox_to_anchor)

`bbox_to_anchor` define un punto/rectángulo de anclaje en coordenadas normalizadas (0–1) del Axes; `loc` indica qué esquina de la leyenda se ancla ahí. Valores `>1` o `<0` la sitúan fuera.

```python
# Fuera, a la derecha, alineada arriba
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Debajo del Axes, centrada
ax.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=3)
```

## Layout interno

| Parámetro | Tipo | Default | Efecto |
|-----------|------|---------|--------|
| `ncol` / `ncols` | `int` | `1` | Reparte las entradas en N columnas |
| `columnspacing` | `float` | `2.0` | Separación horizontal entre columnas |
| `labelspacing` | `float` | `0.5` | Separación vertical entre entradas |
| `handlelength` | `float` | `2.0` | Longitud del muestrario (la línea/marcador) |
| `handletextpad` | `float` | `0.8` | Espacio entre handle y texto |
| `borderpad` | `float` | `0.4` | Margen interior del recuadro |
| `markerscale` | `float` | `1.0` | Escala de los marcadores en la leyenda |

```python
ax.legend(ncol=2, columnspacing=1.0, handlelength=1.5)
```

## Estilo del recuadro y texto

| Parámetro | Tipo | Default | Efecto |
|-----------|------|---------|--------|
| `frameon` | `bool` | `True` | Mostrar el recuadro de fondo |
| `framealpha` | `float` | `0.8` | Opacidad del fondo |
| `facecolor` | color | `'inherit'` | Color de fondo del recuadro |
| `edgecolor` | color | `'inherit'` | Color del borde |
| `shadow` | `bool` | `False` | Sombra bajo el recuadro |
| `fontsize` | `int`/`str` | `None` | Tamaño de las etiquetas |
| `title` | `str` | `None` | Título del recuadro |
| `title_fontsize` | `int`/`str` | `None` | Tamaño del título |

```python
ax.legend(
    title='Series', title_fontsize=12,
    frameon=True, framealpha=0.4, facecolor='white', edgecolor='gray',
)
```

## Casos de uso

### Leyenda compacta multicolumna

```python
ax.legend(ncol=3, fontsize='small', columnspacing=0.8, handlelength=1.2)
```

### Leyenda fuera + ajuste de márgenes

```python
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
fig.tight_layout()             # evita que la leyenda quede recortada
```

## Buenas prácticas

1. Para mover la leyenda fuera del Axes apóyate en `bbox_to_anchor` y luego usa `fig.tight_layout()`; el patrón completo está descrito en [[ax.legend]].
2. Mantén `ncol` bajo (2–3) y aumenta `columnspacing`/`handlelength` solo si las entradas se ven apretadas.
3. Baja `framealpha` cuando la leyenda solape la curva, en vez de ocultarla.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Leyenda recortada al sacarla fuera | el layout no reserva espacio | `fig.tight_layout()` o `fig.subplots_adjust()` |
| `loc` parece invertido con `bbox_to_anchor` | `loc` ancla la leyenda, no el punto | Pensar qué esquina de la leyenda toca el ancla |
| `framealpha` sin efecto | `frameon=False` | Mantener `frameon=True` |
| `ncols` da error | versión <3.6 | Usar `ncol` en versiones antiguas |

## Notas relacionadas

- [[ax.legend]]
- [[Legend]]
- [[Multiples_Leyendas]]
- [[handles_labels]]
