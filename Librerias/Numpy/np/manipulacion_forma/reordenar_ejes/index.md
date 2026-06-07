---
title: np/manipulacion_forma/reordenar_ejes — permutar dimensiones
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/reordenar_ejes — permutar dimensiones

Cambiar el orden de los ejes de un array sin mover sus datos. Cuando NumPy permuta ejes, no reorganiza los bytes en memoria: solo ajusta los *strides* — los saltos que usa para avanzar de un elemento al siguiente en cada dimension. El resultado siempre es una **vista**.

Este grupo existe porque en matematicas y en datos la orientacion importa. Una matriz de coeficientes, un tensor de imagenes `(batch, H, W, C)`, una serie temporal `(tiempo, canales)` — todos pueden necesitar ser transpuestos o reorientados antes de pasarlos a una funcion que espera un eje especifico. Las tres funciones difieren en cuanto control ofrecen: desde la transposicion global hasta el intercambio de exactamente dos ejes.

## Por que siempre es una vista

Permutar ejes es equivalente a reescribir el vector de strides. Si un array 2D tiene strides `(32, 8)` (avanza 32 bytes por fila, 8 por columna), su transpuesta tiene strides `(8, 32)` — el mismo buffer, leido en orden diferente. No hay copia, sin importar el tamano del array.

## Funciones

### [[np.transpose]] — permutacion completa de todos los ejes

La operacion de transposicion generica. Sin argumento `axes`, invierte el orden de todos los ejes: `(a, b, c)` se convierte en `(c, b, a)`. Para una matriz 2D esto intercambia filas y columnas, el uso mas comun. Con `axes=(2, 0, 1)` reordena segun el patron indicado. El atributo `.T` es un alias para el caso sin argumentos.

Caso tipico: adaptar un tensor de imagenes de `(H, W, C)` (formato matplotlib) a `(C, H, W)` (formato PyTorch) con `np.transpose(img, (2, 0, 1))`.

### [[np.moveaxis]] — mover ejes seleccionados

Mueve uno o varios ejes de sus posiciones actuales a nuevas posiciones sin alterar el resto. `np.moveaxis(a, source=0, destination=-1)` toma el primer eje y lo pone al final. Acepta listas: `np.moveaxis(a, [0, 1], [-1, -2])`. Es mas legible que `transpose` cuando se quiere mover ejes especificos sin enumerar todos los demas.

Diferencia con `transpose`: `moveaxis` permite especificar solo los ejes que cambian; el resto se ajusta automaticamente. Con `transpose` hay que indicar la permutacion completa.

### [[np.swapaxes]] — intercambiar exactamente dos ejes

Intercambia dos ejes entre si. `np.swapaxes(a, 1, 2)` en un array `(batch, H, W)` produce `(batch, W, H)`. Es el caso especial de `transpose` donde se intercambian solo dos posiciones. Mas explicito que `transpose` cuando la intencion es precisamente "intercambiar estos dos ejes y dejar el resto igual".

## Tabla de funciones

| Funcion | Descripcion | Cuantos ejes mueve | Vista |
|---------|-------------|-------------------|-------|
| [[np.transpose]] | Permutacion completa o inversion de todos los ejes | Todos | Siempre |
| [[np.moveaxis]] | Mueve ejes elegidos a posiciones arbitrarias | Uno o varios | Siempre |
| [[np.swapaxes]] | Intercambia exactamente dos ejes | Dos | Siempre |

## Guia de eleccion

| Situacion | Funcion |
|-----------|---------|
| Transponer matriz 2D | `a.T` o `np.transpose(a)` |
| Reordenar tensor con patron conocido, todos los ejes | `np.transpose(a, axes)` |
| Mover un eje al principio o al final | `np.moveaxis(a, source, destination)` |
| Intercambiar dos dimensiones concretas | `np.swapaxes(a, ax1, ax2)` |

## Ejemplo: formato de imagen

```python
import numpy as np

# Imagen en formato HWC (matplotlib): shape (480, 640, 3)
img = np.zeros((480, 640, 3))

# Convertir a CHW (PyTorch): shape (3, 480, 640)
img_torch = np.transpose(img, (2, 0, 1))

# Equivalente con moveaxis: mas legible si solo se mueve el eje de canales
img_torch2 = np.moveaxis(img, -1, 0)
