---
title: Colorbar — La barra de color como leyenda de un mapeo valor → color
aliases:
  - Colorbar
  - barra de color
  - colorbar object
tags:
  - matplotlib
  - api/clase
  - styling
lib: matplotlib
obj: Colorbar
tipo: clase
retorna: Colorbar
muta_estado: false
draft: false
---

# Colorbar — La barra de color como leyenda de un mapeo valor → color

## Idea clave

`Colorbar` es el **objeto barra de color**: la "leyenda" que traduce los colores de un gráfico a sus valores numéricos. No se construye a mano normalmente, sino que lo **devuelve** la función [[plt.colorbar]] al asociarse a un *mappable* (una imagen de `imshow`, un `scatter`, un `contourf` o un `pcolormesh`). Una vez obtenido, se configura con sus métodos: etiqueta, posiciones de ticks y textos. Es la pieza que cierra el ciclo del [[concepto_color_mapping]]: dato → norma → color → leyenda.

## Firma del constructor

```python
matplotlib.colorbar.Colorbar(
    ax,              # el Axes donde se dibuja la barra
    mappable=None,   # ScalarMappable de origen (imshow, scatter, contourf...)
    *,
    orientation='vertical',
    ticks=None,      # posiciones de las marcas
    format=None,     # formato de los números
    label='',        # texto descriptivo de la barra
)
```

> En la práctica casi nunca se instancia directamente: se obtiene con `cb = fig.colorbar(mappable, ax=ax)`.

## Qué hace / Valor de retorno

| Aspecto | Detalle |
|---------|---------|
| Qué representa | la correspondencia color ↔ valor de un mappable |
| Cómo se obtiene | retorno de `plt.colorbar()` / `fig.colorbar()` |
| `muta_estado` | `false` — el objeto en sí no muta la figura; sus métodos sí ajustan la barra |
| Atributo clave | `.ax` → el `Axes` propio de la barra (para control fino) |

```python
im = ax.imshow(matriz, cmap='viridis')
cb = fig.colorbar(im, ax=ax)
type(cb)          # → <class 'matplotlib.colorbar.Colorbar'>
cb.ax             # → el Axes que contiene la barra
```

## Parámetros en detalle

### `set_label` — texto descriptivo

```python
cb.set_label("Temperatura (°C)")        # rotula la barra con unidades
cb.set_label("densidad", rotation=270, labelpad=15)
```

### `set_ticks` — posiciones de las marcas

```python
cb.set_ticks([0, 25, 50, 75, 100])       # marcas en valores concretos del dato
```

### `set_ticklabels` — textos de las marcas

```python
cb.set_ticks([0, 1, 2])
cb.set_ticklabels(["bajo", "medio", "alto"])   # etiquetas legibles por nivel
```

### `.ax` — el Axes de la barra

```python
cb.ax.tick_params(labelsize=8)           # control directo sobre los ticks
cb.ax.set_title("escala", fontsize=9)
```

## Casos de uso

### Mapa de calor con leyenda rotulada

```python
fig, ax = plt.subplots()
im = ax.imshow(matriz, cmap='plasma')
cb = fig.colorbar(im, ax=ax)
cb.set_label("intensidad")
```

### Escala categórica con etiquetas de texto

```python
cb = fig.colorbar(im, ax=ax)
cb.set_ticks([0, 1, 2, 3])
cb.set_ticklabels(["agua", "bosque", "urbano", "roca"])
```

### Ajuste fino vía el Axes propio

```python
cb = fig.colorbar(sc, ax=ax)
cb.ax.tick_params(labelsize=7, length=2)   # tipografía pequeña en la barra
```

## Buenas prácticas

1. Guarda siempre el retorno (`cb = fig.colorbar(...)`) para poder etiquetar y ajustar después.
2. Etiqueta con `set_label` incluyendo unidades: una barra sin unidades no informa.
3. Usa `set_ticks` para anclar las marcas a valores significativos del dominio del dato.
4. Para retoques visuales (tamaño de fuente, longitud de ticks) opera sobre `cb.ax`, no sobre el Axes del gráfico.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `set_ticklabels` desalineadas | nº de labels ≠ nº de ticks | fijar primero `set_ticks` con la misma longitud |
| La etiqueta no aparece | se llamó `set_label('')` o se sobrescribió | pasar texto no vacío y tras crear la barra |
| Cambios de estilo sin efecto | se operó sobre el Axes del plot, no sobre `cb.ax` | usar el atributo `.ax` de la colorbar |
| Colores no coinciden con el dato | mappable equivocado al crearla | pasar el mappable concreto a `colorbar` |

## Notas relacionadas

- [[plt.colorbar]]
- [[Normalize]]
- [[Colormaps]]
- [[concepto_color_mapping]]
