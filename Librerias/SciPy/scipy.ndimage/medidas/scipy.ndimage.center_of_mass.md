---
title: scipy.ndimage.center_of_mass — centroide ponderado por intensidad
aliases:
  - center_of_mass
  - scipy.ndimage.center_of_mass
  - centro de masa
tags:
  - scipy
  - api/funcion
  - procesamiento-imagen
lib: scipy
tipo: funcion
mod: scipy.ndimage
retorna: tuple | list[tuple]
requiere:
  - numpy
draft: false
---

# scipy.ndimage.center_of_mass — centroide ponderado por intensidad

Calcula el **centro de masa** (centroide) de un array, **ponderado por la intensidad** de cada pixel: las zonas con valores mayores pesan mas en la posicion del centroide. Sin etiquetas devuelve un unico centro para toda la imagen; con `labels` e `index` devuelve el centroide de **cada region etiquetada**. El retorno es una **tupla de coordenadas** (una por dimension), o una **lista de tuplas** si `index` es una secuencia.

> Las coordenadas salen en **orden de ejes del array**, es decir `(fila, columna)` = `(y, x)` en 2D, no `(x, y)`. Confundir el orden es el error mas habitual al pintar los centroides sobre la imagen.

## Firma

```python
scipy.ndimage.center_of_mass(
    input,           # array_like: imagen; los valores actuan como "masa" (peso)
    labels=None,     # ndarray int: array de etiquetas (tipicamente salida de label)
    index=None,      # int | secuencia: etiqueta(s) cuyo centroide se calcula
) -> tuple | list
```

## Valor de retorno

| Caso | Tipo | Significado |
|------|------|-------------|
| `index` ausente o escalar | `tuple` de floats | Coordenadas `(fila, col, ...)` de un unico centroide |
| `index` es una secuencia | `list` de `tuple` | Un centroide por cada etiqueta pedida, en el mismo orden |

```python
center_of_mass(img)                       # → (y, x) de la imagen entera
center_of_mass(img, labels, index=[1,2])  # → [(y1,x1), (y2,x2)]
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Centroide de toda la imagen | `center_of_mass(img)` |
| Centroide de una region | `center_of_mass(img, labels, index=1)` |
| Centroide de varias regiones | `center_of_mass(img, labels, index=range(1, n+1))` |
| Centroide de una mascara binaria | `center_of_mass(mask)` (cada pixel pesa igual) |

## Parametros en detalle

### `input` (obligatorio)

Array cuyos **valores se usan como peso** (masa). Sobre una imagen en escala de grises, los pixeles brillantes desplazan el centroide hacia ellos. Sobre una **mascara binaria** (todos los pixeles del objeto valen 1) el resultado es el **centroide geometrico** de la region.

```python
import numpy as np
from scipy.ndimage import center_of_mass

img = np.array([[0, 0, 0],
                [0, 9, 0],
                [0, 0, 0]])
center_of_mass(img)
# → (1.0, 1.0)   (fila 1, columna 1: el unico pixel con masa)
```

### `labels`

Array de **etiquetas** que separa la imagen en regiones, normalmente la salida de `label`. Cada etiqueta delimita un objeto cuyo centroide se calcula por separado. Sin `labels`, toda la imagen se trata como una sola masa.

### `index`

Que etiqueta(s) medir. Un **escalar** devuelve una tupla; una **secuencia** (lista o `range`) devuelve una lista de tuplas, una por etiqueta y **en el mismo orden** que `index`. Para todas las regiones de un `label` con `n` objetos, lo idiomatico es `index=range(1, n + 1)`.

```python
from scipy.ndimage import label
labeled, n = label(img > 0)
center_of_mass(img, labeled, index=range(1, n + 1))
# → [(1.0, 1.0)]   lista con un centroide por region
```

## Casos de uso

### Centro de cada objeto tras etiquetar

El uso canonico encadena `label` y `center_of_mass`: se etiquetan las regiones y luego se obtiene el centroide de cada una pasando `labels` e `index`. El etiquetado proviene de la funcion de componentes conexas.

```python
import numpy as np
from scipy.ndimage import label, center_of_mass

m = np.zeros((5,5))
m[0:2,0:2] = 1     # objeto A
m[3:5,3:5] = 1     # objeto B
labeled, n = label(m)
centros = center_of_mass(m, labeled, index=range(1, n + 1))
centros            # → [(0.5, 0.5), (3.5, 3.5)]   (y, x) de cada objeto
```

### Localizar el punto mas brillante (ponderado)

Sobre una imagen de intensidades, el centroide indica donde se concentra la "masa" luminosa.

```python
y, x = center_of_mass(intensidades)   # ojo: (fila, columna)
```

## Buenas practicas

1. Recuerda que las coordenadas son `(fila, columna)` = `(y, x)`; **invierte el orden** al pasarlas a funciones de dibujo que esperan `(x, y)`.
2. Para el centroide **geometrico** de una forma, usa una mascara binaria; para el centroide **ponderado** por brillo, pasa la imagen de intensidades.
3. Combina con el etiquetado de componentes conexas y `index=range(1, n+1)` para procesar todos los objetos de una sola llamada.
4. El orden de la lista de salida coincide con el de `index`: aprovechalo para alinear centroides con otras medidas (areas, sumas).

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Centroide en posicion espejada al pintarlo | El retorno es `(y, x)`, no `(x, y)` | Invertir: pasar `(x, y)` a la funcion de dibujo |
| Un solo centroide en vez de uno por objeto | Falta `labels`/`index` | Pasar `labels` y `index=range(1, n+1)` |
| `index=0` da el centroide del fondo | La etiqueta 0 es el fondo | Empezar el rango en 1 |
| Centroide desviado hacia zonas brillantes | El input pondera por intensidad | Usar mascara binaria si se quiere el centro geometrico |
| Desajuste entre centroides y regiones | Orden de `index` distinto al esperado | La salida sigue el orden de `index`; mantenerlo consistente |

## Limitaciones

- Pondera **siempre por el valor** del array: sobre intensidades no da el centro geometrico salvo que se binarice la entrada.
- Asume valores **no negativos**; intensidades negativas distorsionan el calculo de masa.
- Devuelve coordenadas en **orden de ejes** del array `(fila, col, ...)`, que no coincide con la convencion `(x, y)` de muchas APIs graficas.
- No detecta ni etiqueta regiones por si misma: necesita un array de etiquetas previo para medir objetos individuales.

## Notas relacionadas

- [[scipy.ndimage.label]]
- [[scipy.ndimage.binary_dilation]]
