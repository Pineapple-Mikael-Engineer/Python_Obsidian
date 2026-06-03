---
title: GridSpecFromSubplotSpec — Sub-rejilla anidada en una celda
aliases:
  - GridSpecFromSubplotSpec
  - subgrid
  - rejilla anidada

tags:
  - matplotlib
  - api/clase
  - layout

# --- Clasificación ---
lib: matplotlib
obj: GridSpecFromSubplotSpec
mod: matplotlib.gridspec
tipo: clase

# --- Comportamiento ---
retorna: GridSpecFromSubplotSpec
muta_estado: false

# --- Dependencias ---
requiere:
  - GridSpec

draft: false
---

# GridSpecFromSubplotSpec — Sub-rejilla anidada en una celda

## Definición

`GridSpecFromSubplotSpec` crea una **rejilla dentro de una celda** de un [[GridSpec]] ya existente. Se usa para layouts complejos donde una región del lienzo necesita su propia subdivisión (rejilla dentro de rejilla) sin afectar al resto. No dibuja nada por sí misma: define el reparto del espacio del que luego se piden ejes con `add_subplot`.

## Constructor

```python
from matplotlib.gridspec import GridSpecFromSubplotSpec

sub_gs = GridSpecFromSubplotSpec(
    nrows,                # filas de la sub-rejilla
    ncols,                # columnas de la sub-rejilla
    subplot_spec,         # celda del GridSpec padre a subdividir
    wspace=None,          # separación horizontal entre celdas hijas
    hspace=None,          # separación vertical entre celdas hijas
    height_ratios=None,   # proporciones de alto por fila
    width_ratios=None     # proporciones de ancho por columna
)
```

El argumento clave es `subplot_spec`: una celda (un `SubplotSpec`) que se obtiene indexando un `GridSpec` padre, p. ej. `gs_padre[0, 1]`.

## Propiedades / parámetros clave

| Parámetro | Tipo | Función |
|-----------|------|---------|
| `nrows`, `ncols` | int | dimensiones de la sub-rejilla |
| `subplot_spec` | `SubplotSpec` | celda del padre a subdividir (obligatorio) |
| `wspace` | float | espacio horizontal entre celdas hijas |
| `hspace` | float | espacio vertical entre celdas hijas |
| `width_ratios` | secuencia | anchos relativos de columnas |
| `height_ratios` | secuencia | altos relativos de filas |

Métodos útiles heredados de la base de gridspec:

| Método | Devuelve |
|--------|----------|
| `sub_gs[i, j]` | un `SubplotSpec` hijo (para `fig.add_subplot`) |
| `subgridspec(...)` | atajo equivalente desde un `SubplotSpec` |

## Casos de uso

### Subdividir una celda de un GridSpec padre

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec

fig = plt.figure(figsize=(8, 6))
gs = GridSpec(1, 2, figure=fig)        # rejilla padre: 1 fila, 2 columnas

ax_izq = fig.add_subplot(gs[0, 0])     # mitad izquierda: un solo eje

# mitad derecha subdividida en 2x2
sub = GridSpecFromSubplotSpec(2, 2, subplot_spec=gs[0, 1], hspace=0.3, wspace=0.3)
for i in range(2):
    for j in range(2):
        fig.add_subplot(sub[i, j])
```

### Atajo equivalente con subgridspec

```python
gs = fig.add_gridspec(2, 1)
# subdividir la celda superior en 1x3 sin instanciar la clase directamente
sub = gs[0, 0].subgridspec(1, 3)
for k in range(3):
    fig.add_subplot(sub[0, k])
```

### Proporciones desiguales dentro de la sub-rejilla

```python
sub = GridSpecFromSubplotSpec(
    2, 1, subplot_spec=gs[0, 1],
    height_ratios=[3, 1]               # panel grande arriba, tira pequeña abajo
)
ax_main = fig.add_subplot(sub[0, 0])
ax_resid = fig.add_subplot(sub[1, 0])  # típico: gráfico + residuales
```

## Buenas prácticas

1. Reserva los anidamientos para layouts que un [[GridSpec]] plano no puede expresar; no anides por defecto.
2. Ajusta `wspace`/`hspace` en la sub-rejilla, ya que no hereda los del padre.
3. Usa `height_ratios`/`width_ratios` para paneles tipo "principal + residual".
4. Prefiere `gs[i, j].subgridspec(...)` por brevedad cuando no necesites guardar la clase aparte.
5. Para casos simples evalúa `subplot_mosaic`, más legible que anidar a mano.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `subplot_spec` inválido | pasar el `GridSpec` entero, no una celda | indexa: `subplot_spec=gs[0, 1]` |
| Ejes vacíos / no aparecen | olvidar `fig.add_subplot(sub[i, j])` | crea explícitamente cada eje hijo |
| Separaciones ignoradas | `wspace`/`hspace` puestos en el padre | defínelos en la sub-rejilla |
| Solapamiento de paneles | `tight_layout` no resuelve anidados bien | usa `constrained_layout=True` en la figura |
| `IndexError` al indexar `sub` | índice fuera de `nrows`/`ncols` | respeta las dimensiones declaradas |

## Notas relacionadas

- [[GridSpec]]
- [[plt.subplots]]
- [[figure.add_subplot]]
