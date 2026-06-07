---
title: np/manipulacion_forma/dividir — partir arrays en subarrays
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/dividir — partir arrays en subarrays

`dividir/` es el inverso de `combinar/`: parte un array en una lista de subarrays a lo largo de un eje. Los subarrays resultantes son vistas del array original, no copias.

Las tres funciones son variantes de la misma operacion con distintas restricciones de eje: `np.split` es la mas general, mientras que `np.vsplit` y `np.hsplit` son atajos para los ejes 0 y 1 respectivamente.

## Funciones

| Funcion | Divide a lo largo de | Restriccion |
|---------|----------------------|-------------|
| [[np.split]] | Cualquier eje (por defecto eje 0) | Division debe ser exacta o dar indices explicitos |
| [[np.vsplit]] | Eje 0 (filas) | Solo arrays de 2D o mas |
| [[np.hsplit]] | Eje 1 (columnas) | Solo arrays de 2D o mas; en 1D divide el propio eje 0 |

## Notas relacionadas

- [[np.split]]
- [[np.vsplit]]
- [[np.hsplit]]
