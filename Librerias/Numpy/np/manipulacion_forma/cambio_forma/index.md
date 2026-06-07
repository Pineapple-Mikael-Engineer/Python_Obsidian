---
title: np/manipulacion_forma/cambio_forma — nueva forma sin copiar datos
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/cambio_forma — nueva forma sin copiar datos

`cambio_forma/` reagrupa los elementos de un array en una nueva forma sin copiar datos en la mayoria de los casos. El resultado es una [[concepto_views_vs_copias|vista]] que comparte memoria con el original; solo se genera copia cuando el array no es contiguo y el nuevo layout lo exige.

Regla central: el numero total de elementos debe mantenerse igual entre la forma original y la nueva. Cualquier funcion de esta carpeta lanzara un error si esa condicion no se cumple.

## Funciones

| Funcion | Que hace | Vista si es posible |
|---------|----------|---------------------|
| [[np.reshape]] | Nueva forma arbitraria con el mismo numero de elementos | Si |
| [[np.ravel]] | Aplana el array a 1D | Si |
| [[np.squeeze]] | Elimina todas las dimensiones de tamano 1 | Si |
| [[np.expand_dims]] | Inserta una dimension de tamano 1 en la posicion indicada | Si |

## Notas relacionadas

- [[np.reshape]]
- [[np.ravel]]
- [[np.squeeze]]
- [[np.expand_dims]]
