---
title: GridSpec — Rejilla flexible de subplots
aliases:
  - GridSpec
  - rejilla de subplots
tags:
  - matplotlib
  - api/clase
  - layout

# --- Clasificación ---
lib: matplotlib
obj: GridSpec
tipo: clase

# --- Comportamiento ---
muta_estado: false

draft: false
---

# GridSpec — Rejilla flexible de subplots

## Firma del constructor

```python
GridSpec(
    nrows,
    ncols,
    figure=None,
    left=None, right=None, bottom=None, top=None,
    wspace=None, hspace=None,
    width_ratios=None,
    height_ratios=None
)
```

## Qué es

`GridSpec` define una **rejilla de celdas** sobre la que se colocan los Axes, con control fino del tamaño relativo y el espaciado. Es el motor de layout que usa [[plt.subplots]] por debajo, pero expuesto para construir disposiciones **no uniformes** (celdas que abarcan varias filas/columnas, anchos desiguales).

| Vía de uso | Cuándo |
|-----------|--------|
| `plt.subplots(2, 2)` | rejilla regular simple |
| `gridspec_kw=...` en `plt.subplots` | rejilla regular con ratios |
| `fig.add_gridspec(...)` + slicing | layouts complejos (spans) |
| `plt.subplot_mosaic(...)` | layouts con nombres (alto nivel) |

## Parámetros clave

### `width_ratios`, `height_ratios`

Listas con el tamaño **relativo** de columnas/filas (no absoluto):

```python
import matplotlib.pyplot as plt
fig = plt.figure()
gs = fig.add_gridspec(2, 2, width_ratios=[2, 1], height_ratios=[1, 3])
```

### `wspace`, `hspace`

Espaciado horizontal/vertical entre celdas (fracción del tamaño medio).

## Celdas que abarcan varias filas/columnas (slicing)

La gran ventaja de `GridSpec`: indexar como un array para que un Axes ocupe varias celdas.

```python
fig = plt.figure(figsize=(8, 6))
gs = fig.add_gridspec(3, 3)

ax_grande = fig.add_subplot(gs[0:2, 0:2])   # abarca 2x2
ax_der    = fig.add_subplot(gs[0:2, 2])     # columna derecha
ax_abajo  = fig.add_subplot(gs[2, :])       # fila inferior completa
```

## Casos de uso

### Dashboard con un panel principal y paneles laterales

```python
gs = fig.add_gridspec(2, 3, width_ratios=[3, 1, 1])
principal = fig.add_subplot(gs[:, 0])
fig.add_subplot(gs[0, 1])
fig.add_subplot(gs[1, 2])
```

### Pasar ratios directamente a subplots

```python
fig, axs = plt.subplots(1, 2, gridspec_kw={"width_ratios": [3, 1]})
```

## Buenas prácticas

1. Para rejillas regulares basta [[plt.subplots]]; usa `GridSpec` cuando necesites **spans** o ratios desiguales.
2. `fig.add_gridspec(...)` es la forma moderna recomendada (frente a instanciar `GridSpec` directo).
3. Para anidar una sub-rejilla dentro de una celda, usa [[GridSpecFromSubplotSpec]].
4. Si solo quieres nombrar regiones, `plt.subplot_mosaic` es más legible.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Solapamiento de subplots | spans que se pisan al indexar | revisar los rangos `gs[i:j, k:l]` |
| Ratios ignorados | se pasaron a `subplots` sin `gridspec_kw` | usar `gridspec_kw={"width_ratios": ...}` |
| Espaciado feo | `wspace`/`hspace` por defecto | ajustarlos o usar `fig.tight_layout` |

## Limitaciones

- Define la rejilla, no crea los Axes por sí sola: hay que `add_subplot(gs[...])`.

## Notas relacionadas

- [[plt.subplots]]
- [[GridSpecFromSubplotSpec]]
- [[Figure]]
- [[concepto_figure_axes]]
