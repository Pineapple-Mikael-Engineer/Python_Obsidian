---
title: scipy.ndimage.gaussian_filter — suavizado gaussiano N-D (filtro lineal separable)
aliases:
  - gaussian_filter
  - scipy.ndimage.gaussian_filter
  - filtro gaussiano
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

# scipy.ndimage.gaussian_filter — suavizado gaussiano N-D (filtro lineal separable)

Convoluciona un array N-dimensional con un nucleo **gaussiano**, produciendo un suavizado **lineal** y **separable**: cada pixel se reemplaza por una media ponderada de su vecindario, donde el peso decae con la distancia segun una campana de Gauss. Es el suavizado por defecto para **reducir ruido** antes de detectar bordes o picos, porque atenua las altas frecuencias de forma isotropa y controlada. Al ser separable, internamente aplica un filtro 1-D por cada eje, lo que lo hace eficiente incluso en volumenes 3-D. Opera sobre el mismo `ndarray` de NumPy y devuelve un array del **mismo shape** y dtype compatible.

> Lineal vs no lineal: `gaussian_filter` es **lineal** (promedia con pesos) y por tanto **difumina los bordes** junto con el ruido. Si necesitas eliminar ruido impulsivo conservando bordes, usa un filtro no lineal como la mediana.

## Firma

```python
scipy.ndimage.gaussian_filter(
    input,             # ndarray: imagen / volumen / campo de entrada
    sigma,             # float | secuencia: desviacion del nucleo (por eje si secuencia)
    order=0,           # int | secuencia: 0 suaviza; >0 -> derivada gaussiana
    output=None,       # ndarray | dtype: array o tipo de salida
    mode='reflect',    # str: tratamiento del borde
    cval=0.0,          # float: valor de relleno si mode='constant'
    truncate=4.0       # float: trunca el nucleo a truncate*sigma desviaciones
) -> ndarray
```

## Valor de retorno

| Devuelve | Shape | Significado |
|----------|-------|-------------|
| `ndarray` | igual al de `input` | Array filtrado; cada voxel es la media gaussiana ponderada de su vecindario |

```python
import numpy as np
from scipy.ndimage import gaussian_filter

img = np.random.rand(64, 64)
suave = gaussian_filter(img, sigma=2)
suave.shape   # → (64, 64)   mismo shape que la entrada
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Suavizado isotropo de una imagen 2-D | `gaussian_filter(img, sigma=2)` |
| Sigma distinto por eje (anisotropo) | `gaussian_filter(img, sigma=[1, 3])` |
| Suavizado de un volumen 3-D | `gaussian_filter(vol, sigma=1.5)` |
| Derivada gaussiana en el eje 0 (bordes) | `gaussian_filter(img, sigma=2, order=[1, 0])` |
| Borde por relleno con cero | `gaussian_filter(img, sigma=2, mode='constant', cval=0.0)` |
| Nucleo mas compacto (mas rapido) | `gaussian_filter(img, sigma=2, truncate=2.0)` |

## Parametros en detalle

### `input` (obligatorio)

Array N-dimensional sobre el que actuar: una imagen 2-D, un volumen 3-D o cualquier campo escalar. Es el `ndarray` de NumPy que SciPy procesa; la relacion entre el dato (NumPy) y el algoritmo (SciPy) se describe en [[concepto_relacion_numpy]].

### `sigma` (obligatorio)

Desviacion estandar del nucleo gaussiano, en pixeles. Controla **cuanto** se suaviza: a mayor `sigma`, mas ancho el nucleo y **mas borroso** el resultado. Puede ser un **escalar** (mismo suavizado en todos los ejes) o una **secuencia** con un valor por eje, util cuando la resolucion difiere entre dimensiones (por ejemplo, un volumen con voxeles anisotropos).

```python
# Mas sigma -> mas desenfoque
poco  = gaussian_filter(img, sigma=1)   # detalle casi intacto
mucho = gaussian_filter(img, sigma=5)   # muy difuminado
```

### `order`

Orden de la derivada gaussiana por eje. Con `order=0` (defecto) solo **suaviza**. Con `order>0` calcula la **derivada gaussiana** de ese orden: el filtro deriva y suaviza a la vez, lo que da una estimacion robusta del gradiente y es la base de muchos **detectores de bordes**. Acepta un valor por eje como secuencia.

```python
# Derivada primera en el eje vertical: resalta bordes horizontales
gx = gaussian_filter(img, sigma=2, order=[1, 0])
```

### `mode`

Define como se tratan los **bordes** al no haber vecinos fuera del array. Opciones: `'reflect'` (defecto, espeja sin repetir el borde), `'nearest'` (extiende el valor del borde), `'mirror'` (espeja repitiendo el borde), `'wrap'` (periodico) y `'constant'` (rellena con `cval`). La eleccion afecta a los pixeles cercanos al limite, donde puede aparecer un halo o atenuacion artificial.

### `cval`

Valor de relleno usado **solo** cuando `mode='constant'`. Define el "exterior" virtual del array; un `cval` muy distinto del contenido del borde introduce un escalon que se traduce en artefactos.

### `truncate`

Limita el tamaño del nucleo a `truncate * sigma` desviaciones a cada lado (radio efectivo). Reducirlo acelera el calculo a costa de precision; el valor por defecto `4.0` captura practicamente toda la energia de la gaussiana.

```python
# Radio del nucleo ~ truncate*sigma; aqui ~8 px a cada lado
gaussian_filter(img, sigma=2, truncate=4.0)
```

## Casos de uso

### Reducir ruido antes de detectar bordes o picos

```python
import numpy as np
from scipy.ndimage import gaussian_filter

img = imagen_con_ruido                        # ndarray 2-D ruidoso
suave = gaussian_filter(img, sigma=1.5)       # pre-suavizado
# sobre 'suave' se aplica luego un detector de bordes o de maximos:
# el gaussiano evita que el ruido genere bordes/picos espurios
```

El pre-suavizado gaussiano es el paso clasico previo a operadores derivativos (Sobel, Laplaciano) y a la busqueda de maximos locales: estabiliza el gradiente y reduce falsos positivos.

### Suavizar un campo 2-D (no solo imagenes)

```python
# Campo escalar (p.ej. temperatura o elevacion) sobre una malla 2-D
campo_suave = gaussian_filter(campo, sigma=3, mode='nearest')
# atenua fluctuaciones de pequeña escala conservando la tendencia
```

### Suavizado anisotropo de un volumen 3-D

```python
# Voxeles mas espaciados en z: menos suavizado en ese eje
vol_suave = gaussian_filter(vol3d, sigma=[2, 2, 0.8])
```

## Buenas practicas

1. Elige `sigma` segun la **escala del ruido**, no de la imagen: suaviza lo justo para perder ruido sin borrar la estructura util.
2. Usa una **secuencia** de `sigma` cuando los ejes tengan resolucion distinta (volumenes anisotropos); evita sobre-suavizar el eje fino.
3. Para detectar bordes, prefiere `order>0` (derivada gaussiana) frente a derivar a mano una imagen ruidosa.
4. Ajusta `mode` al contenido del borde: `'nearest'` o `'reflect'` evitan el halo que produce `'constant'` con un `cval` arbitrario.
5. Trabaja en `float`; filtrar enteros puede truncar y degradar el resultado.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Imagen demasiado borrosa | `sigma` excesivo para la escala util | Reducir `sigma`; suavizar solo a la escala del ruido |
| Bordes oscuros / halo en el limite | `mode='constant'` con `cval` lejos del borde | Usar `mode='nearest'` o `'reflect'` |
| Salida con escalones / saturada | `input` entero, se trunca al filtrar | Convertir a `float` antes de filtrar |
| Suavizado desigual entre ejes | `sigma` escalar con voxeles anisotropos | Pasar `sigma` como secuencia por eje |
| Derivada inesperada en vez de suavizado | `order` mayor que 0 sin querer | Fijar `order=0` para solo suavizar |

## Limitaciones

- Es **lineal**: difumina bordes y detalles finos junto con el ruido; no preserva discontinuidades.
- Poco eficaz contra **ruido impulsivo** (sal y pimienta): promedia los pixeles atipicos en lugar de descartarlos.
- El coste crece con `sigma` (nucleo mas ancho); `truncate` lo acota a cambio de algo de precision.
- Asume vecindarios regulares; no se adapta al contenido local de la imagen.

## Notas relacionadas

- [[scipy.ndimage.median_filter]]
- [[scipy.ndimage.uniform_filter]]
- [[concepto_relacion_numpy]]
