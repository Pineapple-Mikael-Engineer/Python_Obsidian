---
title: np/manipulacion_forma — reorganizar arrays
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma — reorganizar arrays

La **forma** (`shape`) de un array es el esquema que determina como se interpretan sus bytes: cuantas filas, columnas, capas, etc. Lo que hace `manipulacion_forma/` es cambiar ese esquema — y en la mayoria de casos sin mover un solo byte en memoria. Un array de 12 elementos puede aparecer como `(12,)`, `(3,4)`, `(2,6)`, `(2,3,2)` o `(1,12)` usando el mismo buffer; solo cambian los *strides* que NumPy usa para avanzar entre dimensiones.

Este grupo de 19 funciones existe porque el shape no es un detalle estetico: define que operaciones son validas, como se aplica el broadcasting, y como interactua el array con algebra lineal, redes neuronales o senales. Dominar estas funciones es la diferencia entre escribir bucles manuales y aprovechar NumPy al maximo.

## Por que existe este grupo

En NumPy los datos viven en un buffer plano (un bloque contiguo de bytes). La *shape* y los *strides* son metadatos que le dicen al interprete: "para avanzar una posicion en el eje 0, salta N bytes; en el eje 1, salta M bytes". Cambiar esos metadatos es gratis en tiempo y memoria. Solo se genera una copia cuando el array no es contiguo y el nuevo layout lo exige — y saber cuando ocurre eso es una de las lecciones clave de `cambio_forma/`.

## Subcarpetas

### [[Numpy/np/manipulacion_forma/cambio_forma/index|cambio_forma]] — nueva shape, mismos datos

Reinterpreta los elementos en una forma diferente. `np.reshape` es la navaja suiza; `np.ravel` aplana a 1D; `np.squeeze` y `np.expand_dims` insertan o eliminan dimensiones de tamano 1. Casi siempre devuelven vistas.

### [[Numpy/np/manipulacion_forma/reordenar_ejes/index|reordenar_ejes]] — permutar dimensiones

Cambia el orden de los ejes sin mover datos. `np.transpose` lo hace sobre todos los ejes a la vez (es la `T` de matrices); `np.moveaxis` mueve ejes elegidos a posiciones arbitrarias; `np.swapaxes` intercambia exactamente dos. Siempre devuelven vistas.

### [[Numpy/np/manipulacion_forma/combinar/index|combinar]] — unir varios arrays en uno

Une arrays a lo largo de un eje existente (`np.concatenate`, `np.vstack`, `np.hstack`, `np.dstack`, `np.column_stack`) o crea un eje nuevo en el proceso (`np.stack`). La confusion mas comun: `stack` aumenta el numero de dimensiones; `concatenate` no. Siempre copias.

### [[Numpy/np/manipulacion_forma/dividir/index|dividir]] — partir en subarrays

El inverso de combinar. `np.split` es la funcion generica; `np.vsplit` y `np.hsplit` son atajos por eje. Los subarrays devueltos son vistas del original. La restriccion principal: si se pide division en partes iguales, el eje debe ser divisible exactamente.

### [[Numpy/np/manipulacion_forma/repetir_desplazar/index|repetir_desplazar]] — duplicar o rotar elementos

`np.tile` repite el array completo como un mosaico; `np.repeat` repite cada elemento individualmente — la diferencia es sutil pero importante. `np.roll` desplaza los elementos de forma circular sin cambiar el tamano: lo que cae por un extremo reaparece por el otro.

## Tabla de decision rapida

| Quiero… | Ir a |
|---------|------|
| Cambiar la shape total del array | [[Numpy/np/manipulacion_forma/cambio_forma/index\|cambio_forma]] |
| Aplanar a 1D | [[np.ravel]] |
| Eliminar dimensiones de tamano 1 | [[np.squeeze]] |
| Anadir una dimension de tamano 1 | [[np.expand_dims]] |
| Transponer o permutar ejes | [[Numpy/np/manipulacion_forma/reordenar_ejes/index\|reordenar_ejes]] |
| Unir arrays sin crear nueva dimension | [[np.concatenate]] |
| Apilar arrays creando nueva dimension | [[np.stack]] |
| Partir un array en trozos | [[Numpy/np/manipulacion_forma/dividir/index\|dividir]] |
| Repetir el array completo N veces | [[np.tile]] |
| Repetir cada elemento N veces | [[np.repeat]] |
| Rotar elementos circularmente | [[np.roll]] |

## Vista vs. copia — regla practica

La mayoria de funciones de `cambio_forma/` y `reordenar_ejes/` devuelven vistas cuando el array de entrada es C-contiguo (layout por filas, el mas comun). Todas las funciones de `combinar/` devuelven copias. Las de `dividir/` devuelven vistas. Las de `repetir_desplazar/` devuelven copias (`tile`, `repeat`) o vistas (`roll` devuelve copia en la implementacion actual). Para verificar: `np.shares_memory(a, resultado)`.
