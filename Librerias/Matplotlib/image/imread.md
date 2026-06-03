---
title: plt.imread — Leer un archivo de imagen a un array NumPy
aliases:
  - imread
  - plt.imread
  - image.imread

tags:
  - matplotlib
  - api/funcion
  - datos

# --- Clasificación ---
lib: matplotlib
mod: matplotlib.image
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
muta_estado: false

# --- Dependencias ---
requiere:
  - numpy

draft: false
---

# plt.imread — Leer un archivo de imagen a un array NumPy

## Definición

`imread` lee un archivo de imagen (PNG, JPG, etc.) desde disco y lo devuelve como un array NumPy con forma `(alto, ancho, canales)`. No dibuja nada: solo carga los píxeles en memoria. Para ver el array resultante se usa [[ax.imshow]], que lo pinta como una imagen sobre los ejes. Está disponible como `matplotlib.pyplot.imread` y en el módulo `matplotlib.image`.

## Firma de la función

```python
import matplotlib.pyplot as plt

arr = plt.imread(
    fname,            # ruta del archivo o file-like object
    format=None,      # extensión forzada si no se infiere de fname
)
```

## Valor de retorno

| Entrada | Retorno | Forma del array |
|---------|---------|-----------------|
| PNG en escala de grises | `ndarray` | `(alto, ancho)` |
| PNG RGB | `ndarray` | `(alto, ancho, 3)` |
| PNG RGBA (con alfa) | `ndarray` | `(alto, ancho, 4)` |
| JPG / otros (vía Pillow) | `ndarray` | `(alto, ancho, 3)` |

```python
arr = plt.imread('foto.png')
arr.shape          # → (480, 640, 4)
arr.dtype          # → float32  (PNG: valores 0..1)
arr.dtype          # → uint8    (JPG vía Pillow: valores 0..255)
```

## Parámetros en detalle

### `fname`

Ruta a un archivo o un objeto file-like ya abierto en binario.

```python
arr = plt.imread('ruta/imagen.png')
with open('imagen.png', 'rb') as f:
    arr = plt.imread(f)
```

### `format`

Fuerza el formato cuando `fname` no tiene extensión reconocible.

```python
arr = plt.imread(buffer, format='png')
```

## Casos de uso

### Cargar y mostrar una imagen

```python
fig, ax = plt.subplots()
arr = plt.imread('foto.png')
ax.imshow(arr)          # delega el render del array a imshow
ax.axis('off')
```

### Inspeccionar un canal concreto

```python
arr = plt.imread('foto.png')   # (alto, ancho, 4)
rojo = arr[:, :, 0]            # solo el canal R
ax.imshow(rojo, cmap='Reds')
```

### Recortar antes de mostrar

```python
arr = plt.imread('foto.png')
recorte = arr[50:200, 100:300]
ax.imshow(recorte)
```

## Buenas prácticas

1. Recuerda que PNG devuelve `float32` en `0..1` y otros formatos `uint8` en `0..255`: normaliza si mezclas fuentes.
2. Para JPG y formatos distintos de PNG necesitas Pillow instalado.
3. `imread` no muta nada ni dibuja; separa la carga (`imread`) del render con [[ax.imshow]].
4. Usa indexación NumPy sobre el array para recortar o seleccionar canales antes de mostrar.
5. Verifica `arr.shape` para saber si hay canal alfa antes de operar sobre los canales.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `FileNotFoundError` | ruta incorrecta | usa ruta absoluta o verifica `os.path.exists` |
| Colores raros en imshow | valores `uint8` tratados como `0..1` | normaliza dividiendo por 255 o deja que imshow infiera dtype |
| `ValueError: Only know how to handle PNG` sin Pillow | falta Pillow para JPG | `pip install pillow` |
| `IndexError` al acceder a canal alfa | imagen sin canal 4 | comprueba `arr.shape[-1]` antes de indexar |
| Imagen aparece invertida verticalmente | confundir orden de filas con coordenadas | el origen por defecto de imshow es la esquina superior |

## Limitaciones

`imread` carga el array completo en memoria; para imágenes enormes considera Pillow con carga perezosa o procesamiento por bloques. No conserva metadatos EXIF: solo devuelve píxeles.

## Notas relacionadas

- [[ax.imshow]]
- [[imsave]]
- [[concepto_artist]]
