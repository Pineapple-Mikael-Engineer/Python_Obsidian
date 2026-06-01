---
title: ax.inset_axes — Axes incrustado dentro de otro Axes
aliases:
  - inset_axes
  - inset
  - zoom incrustado
tags:
  - matplotlib
  - api/metodo
  - layout

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: Axes
muta_estado: true

draft: false
---

# ax.inset_axes — Axes incrustado dentro de otro Axes

## Firma de la función

```python
Axes.inset_axes(
    bounds,            # [x, y, width, height] en coords del Axes padre (0-1)
    *,
    transform=None,    # sistema de coordenadas de bounds (default: ax.transAxes)
    zorder=5,          # orden de dibujo sobre el Axes padre
    **kwargs           # más propiedades del Axes hijo (projection, ...)
)
```

`inset_axes` crea un `Axes` **pequeño dentro de otro Axes** (un *inset*): típicamente un zoom de una región, un mini-mapa o un panel de detalle. Por defecto, `bounds` se interpreta en coordenadas del Axes padre (0-1), por lo que el inset se reposiciona automáticamente si el padre cambia de tamaño.

La diferencia clave con [[fig.add_axes]]: aquí el rectángulo es relativo al **Axes padre**, no a la figura, gracias al `transform=ax.transAxes` por defecto del sistema de [[concepto_transforms]].

## Valor de retorno

```python
axins = ax.inset_axes([0.6, 0.6, 0.35, 0.35])
```

| Retorno | Tipo | Descripción |
|---------|------|-------------|
| `axins` | `matplotlib.axes.Axes` | El Axes inset, hijo y dibujado sobre el padre |

El método **muta** el Axes padre: registra el inset como hijo.

## Parámetros en detalle

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `bounds` | `[float, float, float, float]` | — | `[x, y, width, height]` en coords del padre (0-1) |
| `transform` | `Transform` | `ax.transAxes` | Sistema de coords de `bounds`; usa `ax.transData` para datos |
| `zorder` | `float` | `5` | Profundidad de dibujo; mayor = encima |
| `projection` | `str` | `None` | `'polar'`, `'3d'`, etc. para el inset |

### Interpretación de `bounds`

| Valor de `bounds` | Resultado |
|-------------------|-----------|
| `[0.6, 0.6, 0.35, 0.35]` | inset en la esquina superior derecha del padre |
| `[0.05, 0.05, 0.3, 0.3]` | inset en la esquina inferior izquierda |
| `[0.1, 0.1, 0.8, 0.4]` | franja ancha en la mitad inferior |

## Casos de uso

### Zoom de una región con líneas indicadoras

```python
fig, ax = plt.subplots()
ax.plot(x, y)

axins = ax.inset_axes([0.55, 0.55, 0.4, 0.4])
axins.plot(x, y)
axins.set_xlim(2, 3)    # región ampliada
axins.set_ylim(0, 0.5)
ax.indicate_inset_zoom(axins)   # dibuja el recuadro y las líneas guía
```

### Mini-panel de contexto

```python
fig, ax = plt.subplots()
ax.imshow(mapa_grande)
mini = ax.inset_axes([0.02, 0.7, 0.25, 0.25])
mini.imshow(mapa_global)
mini.set_xticks([]); mini.set_yticks([])
```

### Inset anclado a coordenadas de datos

```python
axins = ax.inset_axes(
    [5, 10, 3, 4],            # ahora en unidades de datos
    transform=ax.transData
)
```

## Buenas prácticas

1. Úsalo (en vez de [[fig.add_axes]]) cuando el panel debe pertenecer a un Axes concreto y seguirlo si se mueve o redimensiona.
2. Para insets de zoom, combínalo con `ax.indicate_inset_zoom(axins)`: dibuja el recuadro origen y las líneas conectoras.
3. Limpia ticks del inset (`set_xticks([])`) cuando solo sirve de referencia visual.
4. Cambia `transform=ax.transData` solo si quieres anclar el inset a una posición de datos en vez de relativa.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Inset en sitio inesperado | se asumió coords de datos con el default | recuerda que el default es `ax.transAxes` (0-1) |
| El zoom no muestra recuadro guía | falta llamar al indicador | usa `ax.indicate_inset_zoom(axins)` |
| Inset tapado por el contenido | `zorder` bajo | sube `zorder` del inset |
| Inset no escala con el padre | se usó `fig.add_axes` por error | usa `ax.inset_axes` para anclar al padre |

## Notas relacionadas

- [[fig.add_axes]]
- [[concepto_transforms]]
- [[plt.subplots]]
- [[concepto_figure_axes]]
