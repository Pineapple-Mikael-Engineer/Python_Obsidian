---
title: plt.subplot_mosaic — Layout de Axes con nombres
aliases:
  - subplot_mosaic
  - mosaico de ejes
  - layout con nombres
tags:
  - matplotlib
  - api/funcion
  - layout

# --- Clasificación ---
lib: matplotlib
obj: pyplot
tipo: funcion

# --- Comportamiento ---
retorna: (Figure, dict {nombre: Axes})
muta_estado: false

draft: false
---

# plt.subplot_mosaic — Layout de Axes con nombres

## Firma de la función

```python
matplotlib.pyplot.subplot_mosaic(
    mosaic,             # str ASCII o lista anidada que describe el layout
    *,
    sharex=False,       # comparte eje X entre todos los Axes
    sharey=False,       # comparte eje Y entre todos los Axes
    width_ratios=None,  # tamaño relativo de columnas
    height_ratios=None, # tamaño relativo de filas
    empty_sentinel='.', # carácter que marca una celda vacía
    subplot_kw=None,    # kwargs por Axes (p.ej. projection)
    gridspec_kw=None,   # kwargs reenviados al GridSpec interno
    per_subplot_kw=None,# kwargs por nombre concreto de Axes
    layout='constrained',  # motor de layout aplicado a la Figure
    **fig_kw            # kwargs de Figure (figsize, dpi, ...)
)
```

Es la API de **alto nivel** para construir disposiciones de Axes: describes el dibujo del layout con arte ASCII y matplotlib crea cada `Axes` y lo asocia a un nombre. Por debajo usa un `GridSpec`, pero te ahorra el slicing manual de [[GridSpec]].

## Valor de retorno

```python
fig, axd = plt.subplot_mosaic("AB;CC")
```

| Retorno | Tipo | Descripción |
|---------|------|-------------|
| `fig` | `matplotlib.figure.Figure` | Figura contenedora; control global de título, tamaño y guardado |
| `axd` | `dict` `{str: Axes}` | Diccionario que mapea cada nombre del mosaico a su `Axes` |

`subplot_mosaic` no muta un objeto existente: **construye** Figure + Axes nuevos y los devuelve.

## Parámetros en detalle

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `mosaic` | `str` / `list` | — | Arte ASCII (`"AB;CC"`) o listas anidadas (`[['A','B'],['C','C']]`) |
| `sharex`, `sharey` | `bool` | `False` | Comparten límites y ticks entre todos los Axes |
| `width_ratios` | `list` | `None` | Tamaño relativo de columnas (longitud = nº columnas) |
| `height_ratios` | `list` | `None` | Tamaño relativo de filas (longitud = nº filas) |
| `empty_sentinel` | `str` | `'.'` | Carácter que deja una celda sin Axes (hueco) |
| `per_subplot_kw` | `dict` | `None` | Config por nombre: `{'A': {'projection': '3d'}}` |
| `layout` | `str` | `'constrained'` | Motor de layout aplicado a la figura |
| `**fig_kw` | — | — | `figsize`, `dpi`, etc., reenviados a `Figure` |

### Sintaxis del mosaico ASCII

| Sintaxis | Significado |
|----------|-------------|
| `"AB"` | dos Axes lado a lado: `A`, `B` |
| `"AB;CC"` | `;` separa filas; `C` repetido abarca toda la fila inferior |
| `"A."` | el `.` deja una celda vacía (sin Axes) |
| `[['izq','der'], ['abajo','abajo']]` | equivalente con listas; nombres multicarácter |

## Casos de uso

### Layout asimétrico clásico

```python
fig, axd = plt.subplot_mosaic("AB;CC")
# axd → {'A': Axes, 'B': Axes, 'C': Axes}
axd['A'].plot([0, 1], [0, 1])   # arriba-izquierda
axd['B'].scatter([1, 2], [3, 4])# arriba-derecha
axd['C'].bar(['x', 'y'], [5, 3])# fila inferior completa
```

### Nombres descriptivos con listas anidadas

```python
fig, axd = plt.subplot_mosaic(
    [['serie', 'serie'],
     ['hist',  'caja']]
)
axd['serie'].plot(t, y)   # fila superior completa
axd['hist'].hist(y)       # abajo-izquierda
```

### Hueco con celda vacía y ratios

```python
fig, axd = plt.subplot_mosaic(
    "A.;CC",
    width_ratios=[3, 1],
    empty_sentinel='.'
)
# 'A' arriba-izquierda, hueco arriba-derecha, 'C' abarca abajo
```

### Config por subplot concreto

```python
fig, axd = plt.subplot_mosaic(
    "AB",
    per_subplot_kw={'B': {'projection': 'polar'}}
)
```

## Buenas prácticas

1. Úsalo cuando el layout sea **irregular pero estable**: gana enormemente en legibilidad frente al slicing de [[GridSpec]].
2. Da nombres **semánticos** (`'mapa'`, `'leyenda'`) en lugar de letras cuando uses listas anidadas: el código se autodocumenta.
3. Combínalo con el motor [[constrained_layout]] (es el `layout` por defecto aquí) para que nada se solape.
4. Itera con `for nombre, ax in axd.items(): ...` para aplicar estilos comunes.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `KeyError` al indexar `axd` | el nombre no coincide con el mosaico | revisa mayúsculas/espacios del arte ASCII |
| Axes solapados o spans raros | el mismo carácter aparece en celdas no contiguas | un nombre debe formar un rectángulo conexo |
| Filas de distinta longitud | strings de filas con distinto nº de caracteres | iguala la longitud de cada bloque entre `;` |
| Celda vacía sin querer | usaste `.` sin querer un hueco | cambia `empty_sentinel` o usa otra letra |

## Notas relacionadas

- [[plt.subplots]]
- [[GridSpec]]
- [[constrained_layout]]
- [[concepto_figure_axes]]
