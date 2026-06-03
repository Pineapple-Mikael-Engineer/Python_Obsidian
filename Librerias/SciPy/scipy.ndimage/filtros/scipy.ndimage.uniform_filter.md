---
title: scipy.ndimage.uniform_filter — filtro de media / caja N-D (lineal, rapido)
aliases:
  - uniform_filter
  - scipy.ndimage.uniform_filter
  - filtro de media
tags:
  - scipy
  - api/funcion
  - procesamiento-imagen
lib: scipy
tipo: funcion
mod: scipy.ndimage
retorna: ndarray
requiere:
  - numpy
draft: false
---

# scipy.ndimage.uniform_filter — filtro de media / caja N-D (lineal, rapido)

Reemplaza cada pixel por la **media aritmetica** de su vecindario de tamaño `size`: un filtro de **caja** (box filter) que pondera **por igual** a todos los vecinos. Es **lineal** y **separable**, por lo que es de los suavizados mas **rapidos** disponibles; equivale a una **media movil** extendida a N dimensiones. Suaviza el ruido, pero al promediar sin ponderar por distancia **difumina los bordes** y es **menos selectivo** que el gaussiano: introduce mas artefactos de "caja" en la respuesta en frecuencia. Opera sobre el `ndarray` de NumPy y devuelve un array del **mismo shape**.

> Posicion entre los tres filtros. `uniform` (media plana, lineal, rapido, difumina) es el mas simple; `gaussian` (media ponderada, lineal, mas selectivo) suaviza mejor a igual desenfoque; `median` (no lineal) preserva bordes y elimina outliers. Para promediado rapido sin exigencias de calidad, `uniform` es la opcion economica.

## Firma

```python
scipy.ndimage.uniform_filter(
    input,             # ndarray: imagen / volumen / campo de entrada
    size=3,            # int | secuencia: lado de la ventana (por eje si secuencia)
    output=None,       # ndarray | dtype: array o tipo de salida
    mode='reflect',    # str: tratamiento del borde
    cval=0.0,          # float: valor de relleno si mode='constant'
    origin=0           # int | secuencia: desplaza el centro de la ventana
) -> ndarray
```

## Valor de retorno

| Devuelve | Shape | Significado |
|----------|-------|-------------|
| `ndarray` | igual al de `input` | Array filtrado; cada pixel es la media de su vecindario de lado `size` |

```python
import numpy as np
from scipy.ndimage import uniform_filter

img = np.random.rand(64, 64)
prom = uniform_filter(img, size=3)
prom.shape   # → (64, 64)   mismo shape que la entrada
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Media en ventana 3x3 (2-D) | `uniform_filter(img, size=3)` |
| Media movil rectangular por eje | `uniform_filter(img, size=(1, 5))` |
| Promediado de un volumen 3-D | `uniform_filter(vol, size=3)` |
| Suavizado mas fuerte | `uniform_filter(img, size=7)` |
| Borde por relleno con cero | `uniform_filter(img, size=3, mode='constant', cval=0.0)` |

## Parametros en detalle

### `input` (obligatorio)

Array N-dimensional a promediar (imagen, volumen o campo escalar). Es el `ndarray` que SciPy recorre aplicando la media local; la relacion dato/algoritmo entre NumPy y SciPy se trata en [[concepto_relacion_numpy]].

### `size`

Lado de la **ventana** de promediado, centrada en cada pixel. Como escalar (defecto `3`) aplica el mismo lado en todos los ejes; como secuencia define un lado por eje, lo que permite una **media movil 1-D dentro de un array 2-D** (por ejemplo `size=(1, 5)` promedia solo a lo largo de las columnas). A mayor `size`, mas suavizado y mas perdida de detalle.

```python
uniform_filter(img, size=3)        # suavizado leve
uniform_filter(img, size=9)        # promedio amplio, muy borroso
uniform_filter(img, size=(1, 5))   # media movil horizontal de longitud 5
```

### `mode`

Tratamiento del **borde** donde la ventana sobresale del array: `'reflect'` (defecto), `'nearest'`, `'mirror'`, `'wrap'` y `'constant'` (rellena con `cval`). Determina que vecinos virtuales entran en la media en la orilla.

### `cval`

Valor del exterior virtual cuando `mode='constant'`. Si difiere mucho del contenido del borde, arrastra la media de los pixeles limitrofes hacia ese valor y oscurece o aclara la orilla.

### `origin`

Desplaza el **centro** de la ventana respecto al pixel procesado. `0` (defecto) la mantiene centrada; un valor distinto la corre, util para una media movil **causal** (que solo mira "hacia atras"). Acepta un desplazamiento por eje.

## Casos de uso

### Media movil 2-D / promediado rapido

```python
import numpy as np
from scipy.ndimage import uniform_filter

# Suavizar rapidamente un mapa o imagen cuando la calidad no es critica
prom = uniform_filter(img, size=5)
# cada pixel es el promedio de su entorno 5x5; muy rapido por ser separable
```

Cuando solo se busca **aplanar** ruido o estimar una tendencia local de forma barata, el filtro de caja es la opcion mas eficiente; el coste apenas crece con el tamaño de la ventana gracias a la separabilidad.

### Media movil dirigida en un campo 2-D

```python
# Promediar solo a lo largo del eje horizontal (medias por fila)
suave = uniform_filter(campo, size=(1, 7))
# equivale a una media movil 1-D aplicada fila a fila
```

### Estimacion rapida de un fondo local

```python
# Aproximar el fondo de una imagen con una media de ventana grande
fondo = uniform_filter(img, size=31)
# luego: detalle = img - fondo   (realce por substraccion de fondo)
```

## Buenas practicas

1. Usa `uniform_filter` cuando prime la **velocidad** sobre la calidad del suavizado; para suavizar bien a igual desenfoque, prefiere el gaussiano.
2. Aprovecha `size` como **secuencia** para medias moviles dirigidas (un solo eje) dentro de un array N-D.
3. Si necesitas **preservar bordes**, no uses este filtro: difumina; recurre a la mediana.
4. Ajusta `mode` al borde (`'nearest'`/`'reflect'`) para evitar el sesgo de orilla que provoca `'constant'`.
5. Trabaja en `float`; promediar enteros puede truncar y perder precision.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Bordes muy difuminados | El filtro de caja no preserva discontinuidades | Usar `median_filter` si hay que conservar bordes |
| Artefactos / "ringing" en frecuencia | La caja tiene mala respuesta espectral | Usar `gaussian_filter` para suavizado mas limpio |
| Orilla oscurecida o aclarada | `mode='constant'` con `cval` ajeno al borde | Usar `mode='nearest'` o `'reflect'` |
| Suavizado en eje no deseado | `size` escalar cuando se queria 1-D | Pasar `size` como secuencia, p.ej. `(1, k)` |
| Salida truncada | `input` entero, la media se redondea | Convertir a `float` antes de filtrar |

## Limitaciones

- Es **lineal**: difumina bordes junto al ruido, sin adaptarse al contenido.
- **Menos selectivo** que el gaussiano: la respuesta en frecuencia de la caja produce artefactos (lobulos laterales).
- Inutil contra ruido **impulsivo**: promedia los outliers en lugar de descartarlos.
- Pondera todos los vecinos por igual; no hay control fino de la forma del suavizado mas alla del tamaño.

## Notas relacionadas

- [[scipy.ndimage.gaussian_filter]]
- [[scipy.ndimage.median_filter]]
- [[concepto_relacion_numpy]]
