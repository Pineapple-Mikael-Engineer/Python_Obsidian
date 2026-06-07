---
title: np/seleccion — extraccion y filtrado condicional
tags:
  - numpy
  - indice
draft: false
---

# np/seleccion — extraccion y filtrado condicional

Este grupo cubre las funciones para extraer, filtrar o modificar elementos de un array segun condiciones logicas o listas de indices. Son la alternativa funcional al indexado directo de NumPy cuando se necesita broadcasting, escritura in-place controlada, o patrones de seleccion mas expresivos que una simple mascara booleana.

La distincion clave con el indexado: estas funciones son llamadas explicitas con nombre, lo que hace la intencion mas legible y en algunos casos habilita parametros extra (`axis=`, vectorizacion completa).

## Notas de la carpeta

- [[np.where]] — seleccion ternaria element-wise: devuelve `x` donde la condicion es True, `y` donde es False. Sin argumentos `x`/`y`, devuelve una tupla de arrays con los indices donde la condicion es True — equivale a `np.nonzero`.
- [[np.select]] — version multi-condicion de `where`: recibe una lista de condiciones y una lista de opciones, evalua en orden y aplica el primer valor que coincide. Equivalente vectorizado de un bloque `if/elif/else` encadenado.
- [[np.take]] — extrae elementos por lista de indices a lo largo de un eje. Equivale a fancy indexing pero es mas explicito y acepta el parametro `axis=` directamente sin necesidad de slicing adicional.
- [[np.put]] — modifica el array in-place en las posiciones dadas (indices planos, no por eje). El array original cambia; no devuelve nada util.
- [[np.clip]] — recorta los valores del array al rango `[a_min, a_max]`. Util para normalizar señales, evitar valores fuera de rango fisico, o preparar datos antes de una operacion que requiere acotacion.
- [[np.choose]] — selecciona entre varias arrays usando un array de indices enteros como selector element-wise. Menos comun en la practica; `np.select` suele ser mas legible para la misma tarea.
- [[np.nonzero]] — devuelve una tupla de arrays con los indices de los elementos distintos de cero (o donde una condicion booleana es True). El resultado se puede usar directamente para indexar el array original.
