---
title: np/manipulacion_forma/combinar — unir arrays en uno
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/combinar — unir arrays en uno

`combinar/` agrupa las funciones que unen varios arrays en un unico array. La diferencia clave entre ellas esta en si la union ocurre a lo largo de un eje existente o si se crea un nuevo eje en el proceso.

Todas las funciones de esta carpeta devuelven una **copia**: no existe vista al combinar multiples arrays independientes.

## Funciones

| Funcion | Que hace | Crea eje nuevo |
|---------|----------|----------------|
| [[np.concatenate]] | Une a lo largo de un eje existente | No |
| [[np.stack]] | Apila arrays a lo largo de un nuevo eje | Si |
| [[np.vstack]] | Concatena verticalmente (eje 0); equivalente 2D de `row_stack` | No |
| [[np.hstack]] | Concatena horizontalmente (eje 1 para 2D, eje 0 para 1D) | No |
| [[np.dstack]] | Concatena en profundidad (eje 2); util para arrays 3D | No |
| [[np.column_stack]] | Convierte vectores 1D en columnas de una matriz 2D | No |

## Guia de eleccion

| Situacion | Funcion recomendada |
|-----------|---------------------|
| Arrays de cualquier dimension, eje libre | [[np.concatenate]] |
| Crear una nueva dimension de apilamiento | [[np.stack]] |
| Apilar filas (matrices o vectores fila) | [[np.vstack]] |
| Apilar columnas (matrices o vectores columna) | [[np.hstack]] o [[np.column_stack]] |
| Combinar en la tercera dimension | [[np.dstack]] |

## Notas relacionadas

- [[np.concatenate]]
- [[np.stack]]
- [[np.vstack]]
- [[np.hstack]]
- [[np.dstack]]
- [[np.column_stack]]
