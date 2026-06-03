---
title: scipy.ndimage.binary_erosion — erosion morfologica binaria
aliases:
  - binary_erosion
  - scipy.ndimage.binary_erosion
  - erosion binaria
tags:
  - scipy
  - api/funcion
  - procesamiento-imagen
lib: scipy
tipo: funcion
mod: scipy.ndimage
retorna: ndarray (bool)
requiere:
  - numpy
draft: false
---

# scipy.ndimage.binary_erosion — erosion morfologica binaria

**Erosiona** (encoge) el **primer plano** de una mascara binaria. Un pixel sobrevive como verdadero **solo si TODO el elemento estructurante cabe dentro del objeto** al centrarse sobre el; basta que un vecino quede en el fondo para apagarlo. El efecto neto es **adelgazar los bordes**, **eliminar motas pequeñas** (regiones mas chicas que el elemento estructurante desaparecen) y **desconectar puentes finos** entre regiones. Devuelve un `ndarray` **booleano** del mismo tamaño que la entrada.

> La erosion es la operacion **dual** de la dilatacion: erosionar el primer plano equivale a dilatar el fondo. Por eso una erosion seguida de una dilatacion (apertura) limpia ruido sin encoger globalmente los objetos grandes.

## Firma

```python
scipy.ndimage.binary_erosion(
    input,               # array_like: mascara binaria (se interpreta por verdad/falsedad)
    structure=None,      # ndarray bool: elemento estructurante (def: conectividad-1, cruz)
    iterations=1,        # int: numero de erosiones sucesivas
    mask=None,           # array_like: pixeles que pueden cambiar (los demas se congelan)
    output=None,         # ndarray: array destino opcional
    border_value=0,      # 0|1: valor asumido fuera del borde de la imagen
    origin=0,            # int|tuple: desplazamiento del elemento estructurante
    brute_force=False,   # bool: estrategia de iteracion
) -> ndarray
```

## Valor de retorno

| Tipo | Significado |
|------|-------------|
| `ndarray` (dtype `bool`) | Mascara erosionada: `True` donde el elemento estructurante cabe entero dentro del primer plano original |

```python
out = binary_erosion(mask)
out.dtype    # → dtype('bool')
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Erosion por defecto (cruz 3x3) | `binary_erosion(mask)` |
| Erosion mas agresiva (cuadrado 3x3) | `binary_erosion(mask, structure=np.ones((3,3)))` |
| Encoger varios pasos | `binary_erosion(mask, iterations=3)` |
| Limitar a una region | `binary_erosion(mask, mask=region)` |
| Quitar motas (apertura) | `binary_dilation(binary_erosion(mask))` |

## Parametros en detalle

### `input` (obligatorio)

Mascara a erosionar. Se interpreta por **verdad/falsedad**: cualquier valor no nulo es primer plano. Lo habitual es pasar un array `bool`; un array de enteros tambien sirve pero el resultado siempre sale booleano.

```python
import numpy as np
from scipy.ndimage import binary_erosion

mask = np.array([[0,0,0,0,0],
                 [0,1,1,1,0],
                 [0,1,1,1,0],
                 [0,1,1,1,0],
                 [0,0,0,0,0]], dtype=bool)
binary_erosion(mask).astype(int)
# → solo sobrevive el pixel central (los bordes se erosionan)
# [[0 0 0 0 0]
#  [0 0 0 0 0]
#  [0 0 1 0 0]
#  [0 0 0 0 0]
#  [0 0 0 0 0]]
```

### `structure`

**Elemento estructurante**: la vecindad que debe caber dentro del objeto. Por defecto es la **conectividad-1** (cruz: el pixel y sus 4 vecinos ortogonales en 2D). Un elemento mas grande (p. ej. `np.ones((3,3))`, los 8 vecinos) erosiona **mas** en una sola pasada. Se genera comodamente con `generate_binary_structure` o `iterate_structure`.

```python
from scipy.ndimage import generate_binary_structure
cruz = generate_binary_structure(2, 1)   # cruz (def)
cuad = generate_binary_structure(2, 2)   # cuadrado 3x3 (8-vecinos)
```

### `iterations`

Repite la erosion `n` veces; equivale a erosionar con un elemento estructurante dilatado `n` veces, pero suele ser mas claro. A mas iteraciones, mas se encoge el objeto (puede desaparecer del todo).

### `mask`

Solo los pixeles donde `mask` es verdadero pueden cambiar de valor; el resto se **congela** en su estado de entrada. Util para erosionar localmente sin tocar el resto de la escena.

### `border_value`

Valor que se asume **fuera** de los limites de la imagen. Con el valor por defecto `0` (fondo), los objetos que tocan el borde se **erosionan tambien por ahi**. Poner `border_value=1` evita ese recorte en los bordes de la imagen.

## Casos de uso

### Eliminar ruido tipo "sal" (motas)

Una erosion borra los puntos aislados mas pequeños que el elemento estructurante.

```python
import numpy as np
from scipy.ndimage import binary_erosion

m = np.zeros((6,6), dtype=bool)
m[1:5,1:5] = True     # bloque grande
m[0,0] = True         # mota aislada
binary_erosion(m).astype(int)
# la mota (0,0) desaparece; el bloque solo se adelgaza un pixel
```

### Apertura: limpiar sin encoger (erosion + dilatacion)

El patron mas comun es **erosionar y luego dilatar** (apertura morfologica): la erosion mata el ruido y la dilatacion devuelve a los objetos grandes su tamaño aproximado. Esto es exactamente lo que hace `binary_opening`.

```python
from scipy.ndimage import binary_dilation
limpio = binary_dilation(binary_erosion(m))   # equivalente a binary_opening(m)
```

## Buenas practicas

1. Trabaja siempre sobre arrays `bool`; convierte con `mask = imagen > umbral` antes de erosionar.
2. Para **limpiar ruido sin encoger** objetos grandes, usa la apertura (erosion + dilatacion) en vez de una erosion sola.
3. Controla la intensidad con `iterations` o cambiando `structure`, no encadenando llamadas a mano.
4. Si los objetos tocan el borde y no quieres recortarlos ahi, pon `border_value=1`.
5. Genera elementos estructurantes con `generate_binary_structure` para no equivocarte de conectividad.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| El objeto desaparece por completo | Demasiadas `iterations` o elemento mas grande que el objeto | Reducir iteraciones o usar elemento mas pequeño |
| Resultado entero en vez de booleano esperado | La salida siempre es `bool` | Convertir con `.astype(int)` si se necesita 0/1 |
| Se erosiona de mas en los bordes | `border_value=0` trata el exterior como fondo | Usar `border_value=1` |
| No limpia el ruido como se esperaba | Una erosion sola tambien encoge lo bueno | Aplicar apertura (erosion + dilatacion) |
| Conectividad inesperada | Elemento por defecto es la cruz (4-vecinos) | Pasar `structure=np.ones((3,3))` para 8-vecinos |

## Limitaciones

- Opera sobre **mascaras binarias**; para imagenes en escala de grises se usan las variantes de morfologia gris (`grey_erosion`).
- Una erosion aislada **siempre encoge** tambien los objetos validos: para preservar tamaño hay que componerla con una dilatacion (apertura).
- El resultado depende fuertemente del **elemento estructurante**; elegir mal la conectividad cambia que se conserva y que se rompe.
- No etiqueta ni mide regiones; solo transforma la mascara.

## Notas relacionadas

- [[scipy.ndimage.binary_dilation]]
- [[scipy.ndimage.label]]
