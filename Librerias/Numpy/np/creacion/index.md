---
title: np/creacion — construccion de arrays
tags:
  - numpy
  - indice
draft: false
---

# np/creacion — construccion de arrays

Este grupo cubre todas las rutas para construir un ndarray. La eleccion correcta depende del origen de los datos y la forma que se necesita: definir bien el dtype y el shape desde el principio evita conversiones implicitas costosas y sorpresas numericas mas adelante.

El eje de decision es: ¿tienes datos ya existentes, o necesitas generar valores con una regla?

## Notas de la carpeta

- [[np.array]] — el constructor universal: convierte cualquier secuencia Python (lista, tupla, array existente) en ndarray. Infiere el dtype automaticamente — puede sorprender con listas mixtas; usar `dtype=` para forzar. Siempre copia el dato original.
- [[np.zeros]] — array prerelleno con 0.0. Por defecto float64; especificar `dtype=int` si se necesitan enteros. Util para inicializar acumuladores o matrices de resultado antes de un loop.
- [[np.ones]] — idem pero con 1.0. Mismo comportamiento de dtype que `zeros`. Punto de partida para arrays de escala o mascaras binarias.
- [[np.empty]] — reserva memoria sin inicializarla; los valores son el estado anterior de esa region de memoria (basura). Mas rapido que `zeros`/`ones` para arrays que se van a rellenar completamente justo despues.
- [[np.full]] — rellena con un escalar arbitrario. Alternativa mas legible a `np.zeros(...) + valor` cuando el valor inicial importa pero no es 0 ni 1.
- [[np.arange]] — rango con paso fijo, analogo a `range()` pero devuelve ndarray. Con floats puede acumular errores de punto flotante en el ultimo elemento; preferir `linspace` para rangos flotantes donde importa el extremo final.
- [[np.linspace]] — N puntos exactamente equiespaciados entre dos extremos, ambos incluidos por defecto. No acumula errores de punto flotante. La opcion natural para ejes de graficas o vectores de evaluacion.
- [[np.logspace]] — N puntos equiespaciados en escala logaritmica. Los argumentos `start` y `stop` son los exponentes de la base (10 por defecto), no los valores finales. Util para barridos de frecuencia o parametros que varian en ordenes de magnitud.
- [[np.eye]] — matriz cuadrada o rectangular con 1s en la diagonal, desplazable con `k=`. Para la identidad cuadrada pura, `np.identity` es mas explicito.
- [[np.identity]] — matriz identidad cuadrada estricta sin parametros extra. Alias semantico de `np.eye(n)` cuando no se necesita desplazamiento ni forma rectangular.
- [[np.fromfunction]] — construye un array donde cada elemento es el resultado de llamar a una funcion con sus indices como argumentos. Util para grids matematicos o kernels sin loops explicitos.
