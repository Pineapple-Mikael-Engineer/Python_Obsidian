---
title: np.moveaxis — mueve ejes a una nueva posición conservando el resto
aliases:
  - moveaxis
  - np.moveaxis
tags:
  - numpy
  - api/funcion
  - shape

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape
  - concepto_views_vs_copias

draft: false
---

# np.moveaxis — mueve ejes a una nueva posición conservando el resto

`np.moveaxis` **traslada uno o varios ejes** de su posición actual (`source`) a una nueva
(`destination`), **manteniendo el orden relativo** de todos los demás. Es la forma más legible de
reordenar *un solo eje* sin tener que enumerar la permutación completa que exigiría [[np.transpose]].
Como todas las funciones de este grupo, no copia: reordena los `strides` y devuelve una
[[concepto_views_vs_copias|vista]].

## La idea en una fórmula

Mover el eje de la posición $s$ a la posición $d$ extrae ese tamaño de la tupla y lo reinserta en su
nuevo sitio; los demás se desplazan para cerrar el hueco, **sin cambiar su orden entre sí**:

$$
(n_0, \dots, n_s, \dots, n_{k-1}) \;\xrightarrow{\ \text{moveaxis}(s \to d)\ }\; (\dots, \underbrace{n_s}_{\text{posición } d}, \dots)
$$

Esa es la diferencia clave con `swapaxes`: aquí **nada más se desordena**. Por ejemplo, mover el eje
0 al final de un `(2, 3, 4)`:

$$
(n_0, n_1, n_2) \;\xrightarrow{\ 0 \to -1\ }\; (n_1, n_2, n_0) \qquad (2,3,4) \to (3,4,2)
$$

los ejes 1 y 2 quedan en su orden original, solo que adelantados una posición.

## Firma

```python
np.moveaxis(
    a,             # array_like: el tensor de entrada
    source,        # int | secuencia[int]: posición(es) original(es)
    destination,   # int | secuencia[int]: posición(es) destino (misma longitud)
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` de cualquier dimensión. Se convierte a `ndarray` si no lo es.

### `source` — posición(es) de origen
Entero o secuencia de enteros (admite **negativos**). Son los ejes que se van a mover, identificados
por su posición **actual**.

### `destination` — posición(es) de destino
Entero o secuencia con la **misma longitud** que `source` (negativos válidos). Son las posiciones a
las que llegan esos ejes en la salida. Si `source` y `destination` tienen longitudes distintas, lanza
`ValueError`.

```python
T = np.ones((2, 3, 4))
np.moveaxis(T, 0, -1).shape       # (3, 4, 2)  → eje 0 al final
np.moveaxis(T, [0, 1], [1, 0]).shape   # (3, 2, 4)  → intercambia 0 y 1
```

## El caso N-D

La clave es que solo los ejes de `source` se reubican; el resto **conserva su orden relativo** y se
desplaza para rellenar. Esto hace a `moveaxis` la herramienta natural para conversiones de convención
de ejes (canal, lote, tiempo).

| `a.shape` | `source → destination` | salida | lectura |
|-----------|------------------------|--------|---------|
| `(2, 3, 4)` | `0 → 2` | `(3, 4, 2)` | primer eje al final |
| `(2, 3, 4)` | `2 → 0` | `(4, 2, 3)` | último eje al frente |
| `(2, 3, 4, 5)` | `1 → 3` | `(2, 4, 5, 3)` | ejes 0,2,3 quedan en su orden |
| `(2, 3, 4)` | `[0, 1] → [1, 2]` | `(4, 2, 3)` | mueve dos ejes a la vez |

```python
# Imagen CHW → HWC (lleva el canal del frente al final)
chw = np.arange(3*2*2).reshape(3, 2, 2)   # canal, alto, ancho
hwc = np.moveaxis(chw, 0, -1)             # (2, 2, 3)  alto, ancho, canal
chw[0, 1, 1] == hwc[1, 1, 0]              # True  → mismo dato, eje reubicado
```

> [!note] Por qué es más legible que `transpose` para un solo eje
> Para llevar el canal de `(H, W, C)` a `(C, H, W)`, con `transpose` hay que escribir la
> permutación completa `(2, 0, 1)`; con `moveaxis` basta `np.moveaxis(img, -1, 0)`: dices *qué eje
> mueves y a dónde*, no reordenas todo el resto a mano.

## Vista vs copia

`np.moveaxis` **siempre devuelve una vista**: reubicar ejes es reordenar la tupla de `strides`, sin
mover el buffer (ver [[concepto_ndarray|strides]]). El resultado comparte memoria con `a`; escribir
en él muta el original.

```python
chw = np.arange(12).reshape(3, 2, 2)
hwc = np.moveaxis(chw, 0, -1)
hwc.base is chw      # True
hwc[0, 0, 0] = 99
chw[0, 0, 0]         # 99  → mismo buffer
```

Tras mover ejes el array deja de ser C-contiguo; usa `.copy()` o `np.ascontiguousarray` si necesitas
contigüidad (ver [[concepto_contiguidad_memoria]]).

## Valor de retorno

| Entrada | `source → destination` | salida (shape) | tipo |
|---------|------------------------|----------------|------|
| `(2, 3, 4)` | `0 → -1` | `(3, 4, 2)` | `ndarray` (vista) |
| `(n_0,\dots,n_{k-1})` | un eje a otra posición | el eje reubicado, resto en orden | `ndarray` (vista) |
| cualquiera | `s → s` | igual a la entrada | `ndarray` (vista) |

El `dtype` se conserva. Nunca devuelve escalar.

## Casos de uso

### Convertir formato de imagen CHW → HWC
```python
chw = np.random.rand(3, 224, 224)     # canal, alto, ancho
hwc = np.moveaxis(chw, 0, -1)         # (224, 224, 3)  alto, ancho, canal
```

### 4D: lote de imágenes NCHW → NHWC (la forma idiomática)
Este es **el** uso canónico de `moveaxis`: para convertir un lote de PyTorch (`NCHW`) al formato
`NHWC` basta con mover el canal (eje 1) al final; lote, alto y ancho se desplazan solos en orden:

```python
x = np.random.rand(8, 3, 32, 32)     # (N, C, H, W)  lote de 8 imágenes RGB 32x32
nhwc = np.moveaxis(x, 1, -1)         # lleva C al final; N, H, W quedan en orden
nhwc.shape                            # (8, 32, 32, 3)  → NHWC
```

> [!note] Más legible que `transpose` para mover un eje
> Lo mismo con [[np.transpose]] obliga a enumerar la permutación completa
> `np.transpose(x, (0, 2, 3, 1))`. Con `moveaxis` dices solo *qué eje mueves y a dónde*
> (`1 → -1`); el resto se reordena solo, sin riesgo de equivocarte al escribir la tupla.

### 5D: lote de vídeos NTCHW → NTHWC
En `(N, T, C, H, W)` se mueve el canal (eje 2) al final; lote y tiempo permanecen al frente y alto/
ancho se adelantan una posición conservando su orden:

```python
vid = np.random.rand(4, 10, 3, 32, 32)   # (N, T, C, H, W)
nthwc = np.moveaxis(vid, 2, -1)          # canal (2) al final
nthwc.shape                               # (4, 10, 32, 32, 3)  → NTHWC
# equivalente, menos legible: np.transpose(vid, (0, 1, 3, 4, 2))
```

### Llevar el eje de lote al frente
```python
datos = np.random.rand(32, 100, 10)   # (batch, tiempo, feat)
por_tiempo = np.moveaxis(datos, 1, 0) # (100, 32, 10)  el tiempo al frente
```

### Mover dos ejes a la vez
```python
T = np.ones((2, 3, 4, 5))
np.moveaxis(T, [0, 1], [-1, -2]).shape   # (4, 5, 3, 2)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: source and destination ... same number of elements` | longitudes distintas | igualar el número de ejes movidos |
| `AxisError` | eje fuera de rango | usar ejes válidos (o negativos) |
| Resultado inesperado vs `transpose` | confundir "mover" con "permutar" | `moveaxis` conserva el orden del resto |
| Se modificó el original | el retorno es una vista | `.copy()` si necesitas independencia |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes del traslado
- [[concepto_views_vs_copias]] — por qué es una vista
- [[concepto_contiguidad_memoria]] — el resultado deja de ser contiguo
- [[np.swapaxes]] — intercambiar exactamente dos ejes
- [[np.transpose]] — permutación general de todos los ejes
