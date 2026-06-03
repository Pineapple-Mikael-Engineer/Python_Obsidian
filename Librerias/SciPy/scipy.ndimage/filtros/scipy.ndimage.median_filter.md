---
title: scipy.ndimage.median_filter — filtro de mediana N-D (no lineal, preserva bordes)
aliases:
  - median_filter
  - scipy.ndimage.median_filter
  - filtro de mediana
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

# scipy.ndimage.median_filter — filtro de mediana N-D (no lineal, preserva bordes)

Reemplaza cada pixel por la **mediana** de los valores de su vecindario. Es un filtro **NO lineal**: no promedia, ordena y toma el valor central, por lo que un valor atipico aislado (un pixel disparado a blanco o negro) **se descarta** en lugar de contaminar a sus vecinos. Por eso es la herramienta de referencia contra el **ruido impulsivo** (sal y pimienta) y, a diferencia del suavizado gaussiano, **preserva los bordes**: la mediana no mezcla los dos lados de una discontinuidad, los mantiene nitidos. Opera sobre el `ndarray` N-dimensional de NumPy y devuelve un array del **mismo shape**.

> Contraste clave. `gaussian_filter` (lineal) promedia con pesos y **difumina los bordes**; `median_filter` (no lineal) ordena y elige la mediana, **conservando los bordes** y eliminando outliers. Gaussiano para ruido suave de banda ancha; mediana para picos impulsivos. La distincion lineal vs no lineal se desarrolla en [[concepto_relacion_numpy]].

## Firma

```python
scipy.ndimage.median_filter(
    input,             # ndarray: imagen / volumen de entrada
    size=None,         # int | tupla: tamaño de la ventana (por eje si tupla)
    footprint=None,    # ndarray bool: mascara de vecindario (alternativa a size)
    output=None,       # ndarray | dtype: array o tipo de salida
    mode='reflect',    # str: tratamiento del borde
    cval=0.0,          # float: valor de relleno si mode='constant'
    origin=0           # int | secuencia: desplaza el centro de la ventana
) -> ndarray
```

## Valor de retorno

| Devuelve | Shape | Significado |
|----------|-------|-------------|
| `ndarray` | igual al de `input` | Array filtrado; cada pixel es la mediana de su vecindario |

```python
import numpy as np
from scipy.ndimage import median_filter

img = np.random.rand(64, 64)
limpio = median_filter(img, size=3)
limpio.shape   # → (64, 64)   mismo shape que la entrada
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Mediana en ventana 3x3 (2-D) | `median_filter(img, size=3)` |
| Ventana rectangular por eje | `median_filter(img, size=(3, 5))` |
| Vecindario en cruz (no cuadrado) | `median_filter(img, footprint=cruz)` |
| Volumen 3-D, ventana 3x3x3 | `median_filter(vol, size=3)` |
| Borde por relleno con cero | `median_filter(img, size=3, mode='constant', cval=0.0)` |

## Parametros en detalle

### `input` (obligatorio)

Array N-dimensional a filtrar (imagen, volumen o campo). Tipico para imagenes contaminadas con pixeles "muertos" o destellos puntuales.

### `size`

Tamaño de la **ventana** (vecindario cuadrado/hipercubico) centrada en cada pixel. Como escalar aplica el mismo lado en todos los ejes (`size=3` → ventana `3x3` en 2-D); como tupla define un lado por eje. Ventanas mayores eliminan ruido mas agresivo pero empiezan a borrar detalle fino. Debe darse `size` **o** `footprint`, no ambos.

```python
median_filter(img, size=3)        # ventana 3x3, suave
median_filter(img, size=5)        # ventana 5x5, mas agresiva
```

### `footprint`

Mascara **booleana** que define la **forma** exacta del vecindario, alternativa a `size`. Solo los pixeles marcados `True` entran en la mediana, lo que permite vecindarios no cuadrados (cruz, disco) para preservar mejor ciertas estructuras. Su shape fija las dimensiones; el numero de `True` determina cuantos valores se ordenan.

```python
import numpy as np
cruz = np.array([[0, 1, 0],
                 [1, 1, 1],
                 [0, 1, 0]], dtype=bool)
median_filter(img, footprint=cruz)   # mediana sobre 5 vecinos en cruz
```

### `mode`

Tratamiento del **borde**: `'reflect'` (defecto), `'nearest'`, `'mirror'`, `'wrap'` y `'constant'` (rellena con `cval`). Igual que en el resto de filtros de `ndimage`, decide que vecinos virtuales se usan donde la ventana se sale del array.

### `cval`

Valor de relleno del exterior cuando `mode='constant'`. Un `cval` muy distinto del borde puede inyectarse en la mediana de los pixeles limitrofes y sesgar el resultado en la orilla.

### `origin`

Desplaza el **centro** de la ventana respecto al pixel procesado. Con `0` (defecto) la ventana esta centrada; valores distintos la corren, util para filtros causales o asimetricos. Acepta un desplazamiento por eje.

## Casos de uso

### Eliminar ruido sal y pimienta conservando bordes

```python
import numpy as np
from scipy.ndimage import median_filter

# Imagen con pixeles disparados a 0 (pimienta) y 1 (sal)
limpia = median_filter(img_ruidosa, size=3)
# los pixeles atipicos quedan fuera de la mediana y desaparecen;
# los bordes reales se mantienen nitidos (no se difuminan)
```

Donde un gaussiano dejaria un borron gris alrededor de cada pixel disparado, la mediana lo **elimina por completo** sin tocar la estructura, porque un outlier nunca es el valor central de su vecindario.

### Limpiar un volumen 3-D preservando interfaces

```python
# Quitar voxeles atipicos de un volumen sin suavizar las superficies
vol_limpio = median_filter(vol3d, size=3)
```

### Preservar lineas finas con footprint en cruz

```python
import numpy as np
cruz = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=bool)
res = median_filter(img, footprint=cruz)
# la cruz respeta mejor estructuras horizontales/verticales que un 3x3 pleno
```

## Buenas practicas

1. Usa la mediana, no el gaussiano, cuando el ruido sea **impulsivo** (pixeles atipicos aislados): conserva bordes y borra outliers.
2. Empieza con `size=3` y sube solo si queda ruido; ventanas grandes erosionan detalles y redondean esquinas.
3. Prefiere `footprint` (cruz, disco) cuando quieras preservar estructuras direccionales o evitar el redondeo de un vecindario cuadrado.
4. Para ruido gaussiano de banda ancha, combina o sustituye por un suavizado lineal; la mediana no es optima ahi.
5. Recuerda que es **mas lento** que un filtro lineal separable: ordenar cuesta mas que promediar.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `TypeError` / conflicto de vecindario | Pasar `size` y `footprint` a la vez | Usar solo uno de los dos |
| Detalles finos se pierden / esquinas redondeadas | `size` demasiado grande | Reducir la ventana o usar `footprint` en cruz |
| Sigue habiendo ruido de banda ancha | Mediana aplicada a ruido gaussiano | Usar suavizado lineal (gaussiano) en su lugar |
| Sesgo en los bordes de la imagen | `mode='constant'` con `cval` ajeno al borde | Usar `mode='nearest'` o `'reflect'` |
| Resultado desplazado | `origin` distinto de 0 sin querer | Dejar `origin=0` para ventana centrada |

## Limitaciones

- Mas **costoso** que los filtros lineales separables: requiere ordenar el vecindario en cada pixel.
- Ventanas grandes eliminan detalle fino y **redondean** esquinas y lineas delgadas.
- No es ideal contra ruido **gaussiano** de banda ancha; brilla con outliers impulsivos.
- No es separable: el coste crece rapido con el tamaño del vecindario en alta dimension.

## Notas relacionadas

- [[scipy.ndimage.gaussian_filter]]
- [[scipy.ndimage.uniform_filter]]
- [[concepto_relacion_numpy]]
