---
title: np/manipulacion_forma/repetir_desplazar — duplicar y rotar elementos
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/repetir_desplazar — duplicar y rotar elementos

Las tres funciones de esta carpeta trabajan sobre un solo array y modifican como se distribuyen sus elementos: dos de ellas aumentan el tamano duplicando datos (`tile`, `repeat`) y una mantiene el tamano y rota los elementos circularmente (`roll`). Todas devuelven una **copia**.

El grupo existe porque estos patrones aparecen con frecuencia en simulacion, procesado de senales y preparacion de datos: construir un kernel repetido, expandir una secuencia corta, implementar convolucion circular o preparar arrays para broadcasting sin copiar manualmente.

## La distincion clave: tile vs. repeat

Ambas duplican datos, pero en unidades diferentes:

- `np.tile(a, 2)` repite el **array completo** como un mosaico: `[1,2,3]` → `[1,2,3,1,2,3]`
- `np.repeat(a, 2)` repite cada **elemento** individualmente: `[1,2,3]` → `[1,1,2,2,3,3]`

Confundirlas produce resultados correctos en apariencia pero erroneos en significado.

## Funciones

### [[np.tile]] — repetir el array como mosaico

Construye un array nuevo repitiendo el array de entrada segun el parametro `reps`. Si `reps` es un entero, repite en el eje final. Si es una tupla `(2, 3)`, repite 2 veces en el eje 0 y 3 veces en el eje 1. Si `reps` tiene mas dimensiones que el array, el array se expande primero con dimensiones de tamano 1 al frente.

Util para crear fondos periodicos, kernels de convolucion, o cualquier patron que se repite espacialmente.

### [[np.repeat]] — repetir cada elemento N veces

Repite cada elemento del array un numero dado de veces. Con `repeats` como entero todos los elementos se repiten el mismo numero de veces; con `repeats` como array se puede especificar cuantas veces se repite cada elemento individualmente. El parametro `axis` controla si la repeticion es elemento a elemento a lo largo de ese eje o sobre el array aplanado.

Util para expandir etiquetas, duplicar muestras en un dataset desbalanceado, o construir senales con duraciones variables por segmento.

### [[np.roll]] — desplazamiento circular

Desplaza los elementos del array `shift` posiciones a lo largo del eje `axis`. Los elementos que "caen" por un extremo reaparecen por el otro — desplazamiento circular, no perdida de datos. `shift` positivo mueve hacia la derecha (o hacia abajo si `axis=0`); negativo, hacia la izquierda. Sin `axis`, el array se aplana antes de desplazar y luego se restaura la forma original.

Util para correlacion circular, alineamiento de series temporales, implementacion de buffers circulares, o calcular diferencias con retardo: `a - np.roll(a, 1)` da la diferencia entre cada elemento y el anterior.

## Tabla de funciones

| Funcion | Unidad que se repite | Tamano resultado | Siempre copia |
|---------|---------------------|-----------------|---------------|
| [[np.tile]] | El array completo | Mayor | Si |
| [[np.repeat]] | Cada elemento individualmente | Mayor | Si |
| [[np.roll]] | N/A (rota, no duplica) | Igual | Si |

## Ejemplo comparativo: tile vs. repeat

```python
import numpy as np

a = np.array([1, 2, 3])

np.tile(a, 3)      # [1, 2, 3, 1, 2, 3, 1, 2, 3]
np.repeat(a, 3)    # [1, 1, 1, 2, 2, 2, 3, 3, 3]

# tile en 2D: reps como tupla
b = np.array([[1, 2], [3, 4]])
np.tile(b, (2, 3))
# [[1, 2, 1, 2, 1, 2],
#  [3, 4, 3, 4, 3, 4],
#  [1, 2, 1, 2, 1, 2],
#  [3, 4, 3, 4, 3, 4]]
```

## Ejemplo: roll para diferencias con retardo

```python
import numpy as np

senal = np.array([10, 13, 12, 15, 14, 16])
retardo = np.roll(senal, 1)   # [16, 10, 13, 12, 15, 14]
diferencia = senal - retardo   # diferencia entre cada muestra y la anterior
# [−6, 3, −1, 3, −1, 2]
# Nota: el primer elemento (-6) es el wrap-around circular, no una diferencia real
```
