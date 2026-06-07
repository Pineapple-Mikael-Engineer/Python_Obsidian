---
title: conceptos_transversales — modelo mental de NumPy
tags:
  - numpy
  - indice
draft: false
---

# conceptos_transversales — modelo mental de NumPy

Antes de usar cualquier funcion de NumPy, estos diez conceptos gobiernan el comportamiento. No son detalles de la API: son las reglas con las que el motor interno decide como almacenar los datos, como alinear dimensiones, si copiar o compartir memoria y con que eficiencia se ejecuta cada operacion. Entenderlos elimina la mayoria de bugs sutiles (modificaciones inesperadas del original, errores de shape, resultados incorrectos despues de una transposicion) y permite razonar sobre rendimiento sin necesidad de perfilar.

## Orden sugerido de lectura

| # | Concepto | Cuando leerlo |
|---|---|---|
| 1 | [[concepto_ndarray]] | Primer contacto con NumPy; antes que cualquier otra nota |
| 2 | [[concepto_shape]] | Inmediatamente despues de ndarray; necesario para todo lo demas |
| 3 | [[concepto_dtype]] | Al crear arrays o al mezclar tipos de datos |
| 4 | [[concepto_views_vs_copias]] | Antes de hacer slicing, reshape o transpose |
| 5 | [[concepto_contiguidad_memoria]] | Al depurar reshape inesperado o al optimizar rendimiento |
| 6 | [[concepto_indexing]] | Al necesitar seleccionar subconjuntos no triviales |
| 7 | [[concepto_axis_parametro]] | Antes de usar cualquier funcion con parametro `axis` |
| 8 | [[concepto_broadcasting]] | Al combinar arrays de diferentes shapes en una operacion |
| 9 | [[concepto_vectorizacion]] | Al eliminar bucles Python o al medir rendimiento |
| 10 | [[concepto_ufuncs]] | Al profundizar en como NumPy implementa operaciones element-wise |

## Como se relacionan

El [[concepto_ndarray]] es el punto de partida: todo array tiene un [[concepto_shape]] (tupla de dimensiones) y un [[concepto_dtype]] (tipo de dato uniforme). Esos dos metadatos determinan cuanta memoria ocupa el array y como se interpreta cada byte en el buffer.

Una vez que el array existe, cualquier operacion de seleccion o transformacion enfrenta la pregunta de [[concepto_views_vs_copias]]: si la operacion puede reutilizar el buffer original (vista) o necesita uno nuevo (copia). Esa decision depende de la [[concepto_contiguidad_memoria]], que describe si los elementos estan dispuestos de forma consecutiva en RAM (C-order o F-order). El [[concepto_indexing]] extiende la seleccion a patrones complejos (fancy indexing, booleano), que por definicion siempre producen copias.

Con shapes y contiguidad claros, entran los mecanismos de computo. El [[concepto_axis_parametro]] permite dirigir reducciones y transformaciones a lo largo de dimensiones especificas. El [[concepto_broadcasting]] resuelve la compatibilidad cuando dos arrays tienen shapes diferentes, estirando virtualmente las dimensiones de tamaño 1 sin copiar datos. Sobre ese sustrato, la [[concepto_vectorizacion]] explica por que las operaciones element-wise de NumPy son rapidas (evitan el overhead del interprete Python) y las [[concepto_ufuncs]] son la implementacion concreta de esa idea: funciones compiladas en C que operan sobre el array entero de forma eficiente y que tambien aplican broadcasting.

## Notas

- [[concepto_ndarray]] — estructura base: buffer de datos + shape + dtype + strides
- [[concepto_shape]] — tupla de dimensiones; define el espacio logico del array
- [[concepto_dtype]] — tipo de dato homogeneo; controla conversion y memoria por elemento
- [[concepto_views_vs_copias]] — cuando una operacion comparte memoria o crea un buffer nuevo
- [[concepto_contiguidad_memoria]] — layout C vs F; afecta reshape, transpose y rendimiento de iteracion
- [[concepto_indexing]] — acceso avanzado: fancy indexing, indexado booleano, ix_
- [[concepto_axis_parametro]] — el parametro `axis` en reducciones y transformaciones
- [[concepto_broadcasting]] — alineacion automatica de shapes para operar arrays distintos
- [[concepto_vectorizacion]] — operaciones element-wise sin bucles Python explicitos
- [[concepto_ufuncs]] — funciones universales compiladas que implementan la vectorizacion

## Notas relacionadas

- [[Librerias/Numpy/index|NumPy — indice raiz]]
- [[Librerias/Numpy/np/index|np]]
- [[Librerias/Numpy/np.ndarray/index|np.ndarray]]
