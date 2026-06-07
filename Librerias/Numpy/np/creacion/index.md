---
title: np/creacion — funciones de creacion de arrays
tags:
  - numpy
  - indice
draft: false
---

# np/creacion — funciones de creacion de arrays

`creacion/` agrupa las 11 funciones de NumPy para construir arrays desde cero o desde datos existentes. La clave es elegir la funcion correcta segun el origen y la naturaleza de los datos: hacerlo bien evita copias innecesarias y mejora la legibilidad.

## Tabla de decision

| Situacion | Funcion recomendada |
|-----------|---------------------|
| Tengo datos en una lista/tupla | [[np.array]] |
| Quiero un rango de enteros o flotantes uniforme | [[np.arange]] |
| Quiero N puntos equiespaciados entre dos extremos | [[np.linspace]] |
| Quiero N puntos en escala logaritmica | [[np.logspace]] |
| Relleno con ceros | [[np.zeros]] |
| Relleno con unos | [[np.ones]] |
| Relleno con un valor arbitrario | [[np.full]] |
| Memoria sin inicializar (maximo rendimiento) | [[np.empty]] |
| Matriz identidad cuadrada | [[np.eye]] o [[np.identity]] |
| Valores calculados por una funcion de indices | [[np.fromfunction]] |

## Ejemplo: cuatro formas de crear arrays

```python
import numpy as np

# Desde datos existentes
a = np.array([1, 2, 3, 4, 5])

# Rango uniforme (enteros)
b = np.arange(0, 10, 2)        # [0, 2, 4, 6, 8]

# N puntos equiespaciados
c = np.linspace(0, 1, 5)       # [0., .25, .5, .75, 1.]

# Relleno constante
d = np.full((3, 3), 7.0)       # matriz 3x3 de sietes
```

## Notas de la carpeta

- [[np.array]] — desde listas, tuplas o arrays existentes
- [[np.zeros]] — relleno de ceros
- [[np.ones]] — relleno de unos
- [[np.empty]] — memoria no inicializada
- [[np.full]] — relleno con valor arbitrario
- [[np.arange]] — rango con paso fijo
- [[np.linspace]] — N puntos equiespaciados en escala lineal
- [[np.logspace]] — N puntos equiespaciados en escala logaritmica
- [[np.eye]] — matriz identidad (permite offset de la diagonal)
- [[np.identity]] — matriz identidad cuadrada estricta
- [[np.fromfunction]] — valores generados por una funcion de indices
