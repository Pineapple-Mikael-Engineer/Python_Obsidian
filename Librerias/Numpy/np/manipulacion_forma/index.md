---
title: np/manipulacion_forma — reorganizar arrays
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma — reorganizar arrays

`manipulacion_forma/` agrupa las 19 funciones de NumPy que modifican la estructura de un array sin alterar sus datos. La idea clave: cambiar como se ven los elementos (forma, ejes, disposicion) sin moverlos en memoria salvo cuando es estrictamente necesario.

Las operaciones cubiertas son cuatro tipos: cambiar la forma del array, permutar sus ejes, combinar varios arrays en uno y partir un array en trozos. La subcarpeta `repetir_desplazar/` cubre ademas duplicar y rotar elementos.

## Subcarpetas

| Carpeta | Descripcion | Funciones |
|---------|-------------|-----------|
| [[Numpy/np/manipulacion_forma/cambio_forma/index\|cambio_forma]] | Reagrupar elementos en una nueva forma sin copiar datos | 4 |
| [[Numpy/np/manipulacion_forma/reordenar_ejes/index\|reordenar_ejes]] | Cambiar el orden de los ejes sin mover datos | 3 |
| [[Numpy/np/manipulacion_forma/combinar/index\|combinar]] | Unir varios arrays en uno a lo largo de un eje | 6 |
| [[Numpy/np/manipulacion_forma/dividir/index\|dividir]] | Partir un array en subarrays a lo largo de un eje | 3 |
| [[Numpy/np/manipulacion_forma/repetir_desplazar/index\|repetir_desplazar]] | Duplicar o mover elementos dentro del array | 3 |

## Tabla de decision rapida

Si sabes lo que quieres hacer pero no la funcion exacta:

| Necesito… | Ir a |
|-----------|------|
| Cambiar el shape del array | [[Numpy/np/manipulacion_forma/cambio_forma/index\|cambio_forma]] |
| Permutar o mover dimensiones | [[Numpy/np/manipulacion_forma/reordenar_ejes/index\|reordenar_ejes]] |
| Unir arrays en uno | [[Numpy/np/manipulacion_forma/combinar/index\|combinar]] |
| Partir un array en trozos | [[Numpy/np/manipulacion_forma/dividir/index\|dividir]] |
| Repetir o rotar elementos | [[Numpy/np/manipulacion_forma/repetir_desplazar/index\|repetir_desplazar]] |
