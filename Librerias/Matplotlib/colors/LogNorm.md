---
title: LogNorm — Normalización logarítmica para datos de varios órdenes de magnitud
aliases:
  - LogNorm
  - norma logarítmica
  - escala log de color
tags:
  - matplotlib
  - api/clase
  - styling
lib: matplotlib
obj: LogNorm
tipo: clase
retorna: LogNorm
muta_estado: false
draft: false
---

# LogNorm — Normalización logarítmica para datos de varios órdenes de magnitud

## Idea clave

`LogNorm` mapea los datos a `[0, 1]` siguiendo una escala **logarítmica** en lugar de lineal. Es una subclase de [[Normalize]] pensada para datos que abarcan varios órdenes de magnitud: mapas de calor con picos agudos, conteos, intensidades, donde una norma lineal aplastaría todo el detalle en el extremo bajo. Al usar logaritmo, los valores pequeños recuperan contraste visible. Se pasa con `norm=` igual que cualquier norma del [[concepto_color_mapping]].

## Firma del constructor

```python
matplotlib.colors.LogNorm(
    vmin=None,   # valor mínimo (debe ser > 0)
    vmax=None,   # valor máximo
    clip=False,  # recorta fuera de rango si True
)
```

## Qué hace / Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Tipo de mapeo | **logarítmico** (`log10` del valor → posición en `[0, 1]`) |
| Requisito | todos los datos deben ser **estrictamente positivos** (`> 0`) |
| Hereda de | `Normalize` (mismo interfaz `norm=`, mismos métodos) |
| `muta_estado` | `false` — describe la transformación, no altera datos |

```python
from matplotlib.colors import LogNorm

norm = LogNorm(vmin=1, vmax=1000)
norm(1)      # → 0.0
norm(10)     # → 0.333...   (un orden de magnitud)
norm(100)    # → 0.666...
norm(1000)   # → 1.0
```

## Parámetros en detalle

### `vmin` / `vmax` — extremos positivos

```python
# vmin DEBE ser > 0: el log de 0 o negativos no existe
norm = LogNorm(vmin=1e-3, vmax=1e3)        # cubre 6 órdenes de magnitud
ax.imshow(intensidad, cmap='inferno', norm=norm)
```

### Uso con un mapa de calor de picos

```python
im = ax.pcolormesh(X, Y, densidad, cmap='viridis', norm=LogNorm())
fig.colorbar(im, ax=ax)   # la barra muestra una escala logarítmica
```

## Casos de uso

### Histograma 2D con conteos muy desiguales

```python
h = ax.hist2d(x, y, bins=50, norm=LogNorm())   # celdas raras siguen visibles
fig.colorbar(h[3], ax=ax)
```

### Espectro o intensidad con pico dominante

```python
norm = LogNorm(vmin=1, vmax=intensidad.max())
ax.imshow(intensidad, cmap='magma', norm=norm)   # detalle también en el fondo bajo
```

## Buenas prácticas

1. Úsala cuando el rango de datos cubra **2 o más órdenes de magnitud**; si no, la lineal basta.
2. Asegura datos positivos: filtra o desplaza los ceros/negativos antes de aplicarla.
3. Fija `vmin` a un suelo razonable (no al mínimo absoluto) para no dar peso a ruido cercano a cero.
4. Combina con una colorbar: la barra rotula automáticamente las décadas logarítmicas.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: minvalue must be positive` | hay ceros o negativos en los datos | filtrar/recortar a valores `> 0` |
| Imagen casi toda de un color | datos en realidad casi lineales | volver a `Normalize` lineal |
| `vmin <= 0` | se pasó un mínimo no positivo | fijar `vmin` a un valor positivo pequeño |
| Ticks de la barra ilegibles | escala con muchas décadas | ajustar `vmin`/`vmax` al rango útil |

## Notas relacionadas

- [[Normalize]]
- [[BoundaryNorm]]
- [[concepto_color_mapping]]
- [[plt.colorbar]]
