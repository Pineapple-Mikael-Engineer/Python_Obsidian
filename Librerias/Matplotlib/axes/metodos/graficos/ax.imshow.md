---
title: ax.imshow — Mostrar una matriz/imagen como píxeles
aliases:
  - imshow
  - ax.imshow
  - mostrar imagen
  - mostrar matriz

tags:
  - matplotlib
  - api/metodo
  - plot/imagenes

# --- Clasificación ---
lib: matplotlib
obj: Axes
tipo: metodo

# --- Comportamiento ---
retorna: AxesImage
muta_estado: true

# --- Dependencias ---
requiere:
  - concepto_figure_axes

draft: false
---

# ax.imshow — Mostrar una matriz/imagen como píxeles

## Firma de la función

```python
Axes.imshow(
    X,
    cmap=None,
    norm=None,
    aspect=None,
    interpolation=None,
    alpha=None,
    vmin=None,
    vmax=None,
    origin=None,
    extent=None,
    **kwargs
)
```

## Valor de retorno

Retorna un único objeto `AxesImage` (un [[concepto_artist]] de tipo imagen). Ese objeto es el que se pasa a [[plt.colorbar]] cuando `X` representa valores escalares.

| Entrada `X` | Interpretación | Retorno |
|-------------|----------------|---------|
| array 2D `(M, N)` | mapa escalar → coloreado vía `cmap` | `AxesImage` |
| array 3D `(M, N, 3)` | imagen RGB (0–1 float o 0–255 uint8) | `AxesImage` |
| array 3D `(M, N, 4)` | imagen RGBA (con canal alfa) | `AxesImage` |

```python
im = ax.imshow(Z, cmap='viridis')
fig.colorbar(im, ax=ax)     # escala de color para datos escalares
im.set_clim(0, 1)           # ajustar el rango de color después
```

## Parámetros en detalle

### `X` — la matriz o imagen

El dato posicional. Si es 2D se colorea con un `cmap`; si es 3D se interpreta como imagen de color y `cmap` se ignora.

### `origin` — dónde va la fila 0

**El parámetro que más confunde.** Controla si la fila 0 de la matriz se dibuja arriba o abajo.

| Valor | Fila 0 | Uso típico |
|-------|--------|-----------|
| `'upper'` (por defecto) | **arriba** | imágenes, matrices (convención fila-columna) |
| `'lower'` | abajo | datos científicos con eje Y creciente hacia arriba |

```python
ax.imshow(Z)                  # origin='upper': fila 0 arriba (def)
ax.imshow(Z, origin='lower')  # fila 0 abajo, como un plano cartesiano
```

Por defecto `origin='upper'`, así que el eje Y "crece hacia abajo": es lo natural para una imagen, pero sorprende al graficar campos físicos.

### `extent` — coordenadas de los bordes

Reasigna los píxeles a un sistema de coordenadas real `(izq, der, abajo, arriba)`.

```python
ax.imshow(Z, extent=[0, 10, 0, 5])   # mapea los píxeles a x∈[0,10], y∈[0,5]
```

### `aspect` — relación de aspecto

```python
ax.imshow(Z, aspect='equal')   # píxeles cuadrados (por defecto en imshow)
ax.imshow(Z, aspect='auto')    # estira para llenar el Axes
ax.imshow(Z, aspect=2)         # razón y/x fijada manualmente
```

### `cmap`, `vmin`, `vmax` — coloreado escalar

```python
ax.imshow(Z, cmap='gray')             # escala de grises
ax.imshow(Z, cmap='viridis', vmin=0, vmax=1)  # fijar el rango de color
```

`vmin`/`vmax` recortan el rango; útil para comparar varias imágenes con la misma escala.

### `interpolation` — suavizado entre píxeles

```python
ax.imshow(Z, interpolation='nearest')   # píxeles nítidos (sin suavizar)
ax.imshow(Z, interpolation='bilinear')  # suavizado
```

Usa `'nearest'` para inspeccionar valores reales de la matriz sin interpolación engañosa.

## Casos de uso

### Visualizar una matriz escalar con barra de color

```python
import numpy as np
import matplotlib.pyplot as plt

Z = np.random.rand(20, 30)

fig, ax = plt.subplots()
im = ax.imshow(Z, cmap='viridis', origin='lower')
fig.colorbar(im, ax=ax, label="valor")
ax.set_title("Matriz 20×30")
```

### Mostrar una imagen RGB

```python
img = plt.imread("foto.png")   # array (alto, ancho, 3 o 4)
ax.imshow(img)                 # cmap se ignora para RGB(A)
ax.axis("off")                 # ocultar ejes
```

### Mapear a coordenadas reales

```python
ax.imshow(Z, extent=[-2, 2, -1, 1], origin='lower', aspect='auto')
# los píxeles ahora viven en x∈[-2,2], y∈[-1,1]
```

## Buenas prácticas

1. Recuerda `origin='upper'` por defecto: usa `origin='lower'` para datos físicos.
2. Acompaña los mapas escalares con una barra de color para dar escala.
3. Fija `vmin`/`vmax` iguales al comparar varias imágenes.
4. Usa `interpolation='nearest'` cuando importe ver el valor exacto de cada celda.
5. Para imágenes RGB no pases `cmap`: se ignora y puede confundir.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Imagen "al revés" | `origin='upper'` por defecto | pasar `origin='lower'` |
| RGB se ve raro | valores fuera de `[0,1]` siendo float | normalizar o usar `uint8` 0–255 |
| Píxeles deformados | `aspect='equal'` con datos no cuadrados | usar `aspect='auto'` |
| Sin escala de color | falta `colorbar` en datos escalares | añadir `fig.colorbar(im)` |
| `cmap` no tiene efecto | `X` es 3D (RGB) | `cmap` solo aplica a matrices 2D |

## Notas relacionadas

- [[plt.colorbar]]
- [[concepto_artist]]
- [[Axes]]
- [[ax.contourf]]
- [[plt.subplots]]
