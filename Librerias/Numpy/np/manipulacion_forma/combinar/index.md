---
title: np/manipulacion_forma/combinar — unir arrays en uno
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/combinar — unir arrays en uno

Las seis funciones de esta carpeta toman varios arrays separados y los fusionan en uno solo. Todas devuelven una **copia** — no existe vista al combinar buffers de memoria independientes.

La distincion conceptual mas importante: algunas funciones unen a lo largo de un **eje existente** (los arrays deben tener el mismo numero de dimensiones y shapes compatibles) y `np.stack` crea un **eje nuevo** (todos los arrays deben tener exactamente la misma shape). Confundir estas dos categorias es la fuente mas comun de errores de shape en NumPy.

## El eje existente vs. el eje nuevo

Dos vectores `(5,)` unidos con `np.concatenate` dan `(10,)` — mismo numero de dimensiones, mas elementos en el eje 0. Los mismos vectores unidos con `np.stack(axis=0)` dan `(2, 5)` — una nueva dimension aparece. Elegir entre ellos depende de si el resultado debe tener el mismo numero de ejes que los inputs o uno mas.

## Funciones

### [[np.concatenate]] — union generica por eje existente

La funcion base de todo el grupo. Acepta una secuencia de arrays y un eje a lo largo del cual unirlos. Todos los arrays deben tener el mismo `ndim` y la misma shape en todos los ejes excepto en `axis`. No crea nuevas dimensiones. Es la mas flexible y la mas explicita: si sabes que eje quieres usar y tus arrays ya tienen la dimension correcta, esta es la eleccion.

### [[np.stack]] — apilar creando un eje nuevo

A diferencia de todas las demas funciones de este grupo, `stack` exige que todos los arrays tengan exactamente la misma shape e inserta un nuevo eje en la posicion `axis`. El resultado tiene `ndim + 1` dimensiones. Util para construir un tensor de lotes desde muestras individuales: N arrays de shape `(H, W)` apilados con `axis=0` dan `(N, H, W)`.

### [[np.vstack]] — apilar verticalmente (eje 0)

Une arrays a lo largo del eje 0. Para arrays 2D es identico a `concatenate(..., axis=0)`. El caso especial util: para arrays 1D, `vstack` los convierte a filas antes de apilar — un vector `(5,)` se trata como `(1, 5)`. Conveniente cuando se tienen vectores que se quieren apilar como filas de una matriz.

### [[np.hstack]] — apilar horizontalmente (eje 1)

Une arrays a lo largo del eje 1 para arrays de 2D o mas. Para arrays 1D es simplemente una concatenacion en el eje 0 (porque un vector no tiene eje 1). Util para anadir columnas a una matriz existente.

### [[np.dstack]] — apilar en profundidad (eje 2)

Une arrays a lo largo del tercer eje. Antes de apilar, convierte arrays 1D a shape `(1, n, 1)` y arrays 2D a `(m, n, 1)`. Especializado para construir arrays 3D (imagenes RGB, volumenes) desde capas 2D o vectores de profundidad.

### [[np.column_stack]] — vectores 1D como columnas

Convierte vectores 1D en columnas `(n, 1)` y luego los concatena horizontalmente. Para arrays 2D se comporta como `hstack`. Muy util en el patron clasico de construir una matriz de datos desde vectores de caracteristicas: `np.column_stack([x, y, z])` donde `x`, `y`, `z` son vectores.

## Tabla de funciones

| Funcion | Une por | Crea eje nuevo | Caso especial 1D |
|---------|---------|----------------|-----------------|
| [[np.concatenate]] | Eje libre | No | Concatena en eje 0 |
| [[np.stack]] | Eje nuevo | Si | Trata cada vector como elemento |
| [[np.vstack]] | Eje 0 | No | Convierte a fila `(1, n)` |
| [[np.hstack]] | Eje 1 | No | Concatena en eje 0 |
| [[np.dstack]] | Eje 2 | No | Convierte a `(1, n, 1)` |
| [[np.column_stack]] | Eje 1 | No | Convierte a columna `(n, 1)` |

## Guia de eleccion

| Situacion | Funcion recomendada |
|-----------|---------------------|
| Arrays con el mismo ndim, eje libre | [[np.concatenate]] |
| Construir lote desde muestras de igual shape | [[np.stack]] |
| Anadir filas a una matriz | [[np.vstack]] |
| Anadir columnas a una matriz (desde arrays 2D) | [[np.hstack]] |
| Construir matriz desde vectores de datos | [[np.column_stack]] |
| Apilar imagenes o capas en la dimension de profundidad | [[np.dstack]] |

## Ejemplo: construir matriz de datos

```python
import numpy as np

tiempo = np.linspace(0, 1, 100)    # shape (100,)
senal = np.sin(2 * np.pi * tiempo) # shape (100,)
ruido = np.random.randn(100)       # shape (100,)

# column_stack: cada vector se convierte en columna
datos = np.column_stack([tiempo, senal, ruido])  # shape (100, 3)

# Equivalente explicito con concatenate:
datos2 = np.concatenate([
    tiempo.reshape(-1, 1),
    senal.reshape(-1, 1),
    ruido.reshape(-1, 1)
], axis=1)
```
