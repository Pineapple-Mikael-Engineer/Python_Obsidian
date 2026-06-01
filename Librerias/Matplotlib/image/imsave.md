---
title: plt.imsave — Guardar un array como archivo de imagen
aliases:
  - imsave
  - plt.imsave
  - image.imsave

tags:
  - matplotlib
  - api/funcion
  - datos

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.image
tipo: funcion

# --- Comportamiento ---
retorna: None
muta_estado: false

# --- Dependencias ---
requiere:
  - numpy

draft: false
---

# plt.imsave — Guardar un array como archivo de imagen

## Definición

`imsave` toma un array NumPy de píxeles y lo escribe directamente a disco como archivo de imagen (PNG, JPG, etc.). Es la operación inversa de [[imread]]. A diferencia de `fig.savefig` —que renderiza la **figura completa** con ejes, títulos y márgenes— `imsave` guarda **solo el array de datos** como imagen, sin decoración alguna. Está disponible como `matplotlib.pyplot.imsave` y en el módulo `matplotlib.image`.

## Firma de la función

```python
import matplotlib.pyplot as plt

plt.imsave(
    fname,            # ruta de salida (la extensión define el formato)
    arr,              # array (alto, ancho) | (alto, ancho, 3) | (alto, ancho, 4)
    *,
    cmap=None,        # colormap aplicado si arr es 2D escalar
    vmin=None,        # límite inferior de normalización (con cmap)
    vmax=None,        # límite superior de normalización (con cmap)
    origin=None,      # 'upper' (defecto) | 'lower'
    dpi=100,          # puntos por pulgada en metadatos del archivo
    format=None,      # formato forzado si no se infiere de fname
)
```

## Valor de retorno

| Entrada | Retorno | Efecto |
|---------|---------|--------|
| array 2D + `cmap` | `None` | escribe imagen coloreada con el colormap |
| array RGB / RGBA | `None` | escribe los píxeles tal cual |
| cualquier llamada válida | `None` | el resultado es el archivo en disco, no un valor |

```python
plt.imsave('salida.png', arr)   # → None  (efecto: archivo 'salida.png')
```

## Parámetros en detalle

### `fname` y `format`

La extensión de `fname` determina el formato; `format` lo fuerza si no hay extensión clara.

```python
plt.imsave('mapa.png', arr)
plt.imsave(buffer, arr, format='png')
```

### `cmap`, `vmin`, `vmax`

Solo aplican cuando `arr` es 2D (escalar): mapean valores a colores.

```python
plt.imsave('calor.png', matriz2d, cmap='viridis', vmin=0, vmax=1)
```

### `origin`

Define qué fila va arriba. `'upper'` (defecto) coloca la fila 0 arriba.

```python
plt.imsave('flip.png', arr, origin='lower')
```

## Casos de uso

### Guardar un array procesado

```python
arr = plt.imread('foto.png')
recorte = arr[50:200, 100:300]
plt.imsave('recorte.png', recorte)   # solo los píxeles, sin ejes
```

### Exportar una matriz numérica como mapa de calor

```python
import numpy as np
m = np.random.rand(100, 100)
plt.imsave('heatmap.png', m, cmap='inferno')
```

### Contraste con guardar la figura completa

```python
fig, ax = plt.subplots()
ax.imshow(arr)
fig.savefig('figura.png')   # incluye ejes, márgenes y fondo de la figura
plt.imsave('solo_datos.png', arr)   # solo el array, pixel a pixel
```

## Buenas prácticas

1. Usa `imsave` cuando quieras la imagen "cruda"; usa `fig.savefig` cuando quieras la figura con ejes y anotaciones.
2. Especifica `cmap` solo con arrays 2D; con RGB/RGBA se ignora.
3. Fija `vmin`/`vmax` para comparar varios mapas de calor con la misma escala de color.
4. Asegúrate de que el dtype y rango del array sean válidos (`float` en `0..1` o `uint8` en `0..255`).
5. La extensión del nombre decide el formato: usa `.png` para preservar canal alfa.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Imagen totalmente negra o blanca | rango fuera de `0..1` sin normalizar | pasa `vmin`/`vmax` o normaliza el array |
| `cmap` ignorado | el array es RGB/RGBA, no 2D | aplica `cmap` solo a arrays 2D escalares |
| Esperar la figura con ejes | `imsave` guarda solo el array | usa `fig.savefig` para la figura completa |
| `ValueError` por shape inesperada | array no es 2D ni `(h, w, 3|4)` | reorganiza el array a una forma de imagen válida |
| JPG falla | falta Pillow | `pip install pillow` o guarda en PNG |

## Limitaciones

`imsave` no añade ejes, títulos ni leyendas: para eso está `fig.savefig`. Tampoco controla resolución de píxeles de salida más allá del tamaño del array (el `dpi` solo afecta metadatos, no remuestrea).

## Notas relacionadas

- [[imread]]
- [[ax.imshow]]
- [[concepto_artist]]
