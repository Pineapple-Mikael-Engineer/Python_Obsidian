---
title: np/manipulacion_forma/reordenar_ejes — reordenar ejes y voltear contenido
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/reordenar_ejes — reordenar ejes y voltear contenido

Reorientar un array **sin tocar sus datos en memoria**. Hay dos operaciones distintas en este grupo:
**reordenar ejes** (cambiar qué dimensión va en qué posición: [[np.transpose]], [[np.swapaxes]],
[[np.moveaxis]]) e **invertir el contenido** a lo largo de un eje conservando la forma
([[np.flip]]). En todos los casos NumPy no reorganiza los bytes: solo reescribe los `strides` —los
saltos con que avanza de un elemento al siguiente en cada eje—. Por eso **todas devuelven una vista**
de coste $O(1)$, sin importar el tamaño del array.

Este grupo existe porque en matemáticas y en datos la orientación importa: una matriz de
coeficientes, un tensor de imágenes `(batch, H, W, C)`, una serie temporal `(tiempo, canales)`...
todos pueden necesitar transponerse, reorientarse o reflejarse antes de pasarlos a una función que
espera un eje en una posición concreta.

## Por qué siempre es una vista

Permutar o invertir ejes equivale a reescribir el vector de `strides` (ver
[[concepto_views_vs_copias]]). Si una matriz 2D tiene strides `(32, 8)`, su transpuesta tiene
`(8, 32)` —el mismo buffer leído en otro orden— y su `flip` por columnas tiene un stride **negativo**
con el puntero al final. Nunca hay copia; el resultado simplemente deja de ser C-contiguo.

## Reordenar ejes vs voltear contenido

La distinción es la clave del grupo: **transpose / swapaxes / moveaxis cambian el shape** (reordenan
las dimensiones), mientras que **flip conserva el shape** y solo invierte el orden de los elementos.

| Operación | Qué cambia | Mapa de shapes |
|-----------|------------|----------------|
| reordenar ejes | la posición de las dimensiones | $(n_0,\dots,n_{k-1}) \to (n_{\sigma(0)},\dots,n_{\sigma(k-1)})$ |
| voltear contenido | el orden de los elementos (no el shape) | $(n_0,\dots,n_{k-1}) \to (n_0,\dots,n_{k-1})$ invertido |

## Tabla de funciones

| Función | Descripción | Ejes / efecto | Vista |
|---------|-------------|---------------|-------|
| [[np.transpose]] | Permuta (o invierte) todos los ejes; `.T` es la inversión total | Todos | Siempre |
| [[np.moveaxis]] | Mueve ejes elegidos a otra posición, conservando el orden del resto | Uno o varios | Siempre |
| [[np.swapaxes]] | Intercambia exactamente dos ejes | Dos | Siempre |
| [[np.flip]] | Invierte el orden de los elementos (shape intacto); atajos `fliplr`/`flipud` | Contenido | Siempre |

## Guía de elección

| Situación | Función |
|-----------|---------|
| Transponer una matriz 2D | `a.T` o `np.transpose(a)` |
| Reordenar un tensor con permutación conocida de todos los ejes | `np.transpose(a, axes)` |
| Mover un eje al principio o al final (canal, lote, tiempo) | `np.moveaxis(a, source, destination)` |
| Intercambiar dos dimensiones concretas | `np.swapaxes(a, ax1, ax2)` |
| Reflejar/invertir el contenido a lo largo de un eje | `np.flip(a, axis)` (`fliplr`/`flipud` en 2D) |

## Ejemplo: formato de imagen y reflejo

```python
import numpy as np

# Imagen en formato HWC (matplotlib): shape (480, 640, 3)
img = np.zeros((480, 640, 3))

# Reordenar ejes a CHW (PyTorch): shape (3, 480, 640)
img_torch = np.transpose(img, (2, 0, 1))
img_torch2 = np.moveaxis(img, -1, 0)   # equivalente, más legible

# Voltear el contenido: reflejo horizontal (shape intacto, (480, 640, 3))
img_espejo = np.flip(img, axis=1)
```
