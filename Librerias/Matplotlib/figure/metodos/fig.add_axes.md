---
title: fig.add_axes — Axes en posición arbitraria de la figura
aliases:
  - add_axes
  - axes en posición libre
  - fig.add_axes
tags:
  - matplotlib
  - api/metodo
  - layout

# --- Clasificación ---
lib: matplotlib
obj: Figure
tipo: metodo

# --- Comportamiento ---
retorna: Axes
muta_estado: true

draft: false
---

# fig.add_axes — Axes en posición arbitraria de la figura

## Firma de la función

```python
Figure.add_axes(
    rect,             # [left, bottom, width, height] en coords de figura (0-1)
    *,
    projection=None,  # 'polar', '3d', ... proyección del Axes
    sharex=None,      # comparte eje X con otro Axes
    sharey=None,      # comparte eje Y con otro Axes
    label='',         # etiqueta interna del Axes
    **kwargs          # más propiedades del Axes (facecolor, frame_on, ...)
)
```

`add_axes` coloca un `Axes` en una **posición arbitraria** dentro de la figura, especificada en coordenadas de figura normalizadas (0-1). A diferencia de [[plt.subplots]] o [[GridSpec]], no hay rejilla: tú das el rectángulo exacto. Es la herramienta para insets manuales, paneles superpuestos y layouts a medida.

El rectángulo se interpreta mediante el sistema de [[concepto_transforms]] de la figura (`fig.transFigure`): `(0,0)` es la esquina inferior izquierda y `(1,1)` la superior derecha.

## Valor de retorno

```python
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
```

| Retorno | Tipo | Descripción |
|---------|------|-------------|
| `ax` | `matplotlib.axes.Axes` | El Axes recién creado y ya añadido a la figura |

El método **muta** la figura: el nuevo `Axes` queda registrado en `fig.axes`.

## Parámetros en detalle

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `rect` | `[float, float, float, float]` | — | `[left, bottom, width, height]`, todos en 0-1 |
| `projection` | `str` | `None` | `'polar'`, `'3d'`, etc. |
| `sharex`, `sharey` | `Axes` | `None` | Comparte límites/ticks con otro Axes |
| `label` | `str` | `''` | Identificador interno (útil si hay Axes superpuestos) |
| `facecolor` | color | — | Color de fondo del Axes |
| `frame_on` | `bool` | `True` | Dibuja o no el marco del Axes |

### Interpretación de `rect`

| Valor de `rect` | Resultado |
|-----------------|-----------|
| `[0, 0, 1, 1]` | Axes que ocupa toda la figura |
| `[0.1, 0.1, 0.8, 0.8]` | Axes centrado con márgenes del 10% |
| `[0.65, 0.65, 0.2, 0.2]` | Panel pequeño en la esquina superior derecha |

## Casos de uso

### Inset manual superpuesto

```python
fig = plt.figure(figsize=(6, 6))
ax_main = fig.add_axes([0.1, 0.1, 0.8, 0.8])   # gráfico principal
ax_main.plot(x, y)

ax_inset = fig.add_axes([0.6, 0.6, 0.25, 0.25])# panel superpuesto
ax_inset.plot(x, y)
ax_inset.set_xlim(0, 1)   # zoom a una región
```

### Dos paneles a medida

```python
fig = plt.figure(figsize=(8, 4))
izq = fig.add_axes([0.05, 0.1, 0.4, 0.8])
der = fig.add_axes([0.55, 0.1, 0.4, 0.8])
```

### Eje extra para una barra de color manual

```python
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.7, 0.8])
cax = fig.add_axes([0.85, 0.1, 0.04, 0.8])   # franja estrecha para colorbar
im = ax.imshow(datos)
fig.colorbar(im, cax=cax)
```

## Buenas prácticas

1. Reserva `add_axes` para posiciones **realmente arbitrarias**: para rejillas regulares usa [[plt.subplots]] y para spans usa [[GridSpec]].
2. Recuerda que `rect` está en coordenadas de figura, no de datos: piénsalo en términos del sistema de [[concepto_transforms]].
3. Para insets *dentro* de un Axes concreto (no de la figura), prefiere [[ax.inset_axes]]: se reposiciona con el Axes padre.
4. Los Axes de posición fija **no** los gestiona el motor [[constrained_layout]]: contrólalos tú.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Axes invisible o fuera de marco | valores de `rect` fuera de 0-1 | mantén `left+width` y `bottom+height` ≤ 1 |
| Inset que no sigue al Axes padre | usar `add_axes` (coords de figura) | usa `ax.inset_axes` para anclar al padre |
| Solapamiento inesperado | dos rectángulos que se pisan | ajusta `left`/`bottom` o usa `zorder` |
| constrained no lo ajusta | Axes de posición fija | gestiona los márgenes manualmente |

## Notas relacionadas

- [[plt.subplots]]
- [[GridSpec]]
- [[ax.inset_axes]]
- [[concepto_transforms]]
