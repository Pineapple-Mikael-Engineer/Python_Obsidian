---
title: NumPy — motor de arrays N-dimensionales
tags:
  - numpy
  - indice
draft: false
---

# NumPy — motor de arrays N-dimensionales

NumPy no es simplemente "la libreria de arrays". Es el sistema que define como Python representa y transforma datos numericos en memoria. Bajo el capot corre codigo C compilado que llama directamente a BLAS y LAPACK — las mismas rutinas que usan Matlab y Fortran cientifico. El resultado es que una operacion sobre un array de un millon de elementos ocurre en microsegundos, no en los cientos de milisegundos que tardaria un bucle Python equivalente.

Su influencia va mas alla de su propio API. Pandas representa sus columnas como arrays NumPy. SciPy construye sus algoritmos numericos sobre ellos. scikit-learn recibe y devuelve ndarrays en cada `fit` y `predict`. Matplotlib traza ndarrays directamente. Sin NumPy, ninguna de estas librerias existiria en su forma actual — el ndarray es el tipo de datos compartido de todo el ecosistema cientifico de Python.

## Las dos capas de NumPy

NumPy tiene una arquitectura de dos capas que conviene mantener separadas mentalmente:

**El ndarray** — el objeto. Un buffer de bytes contiguo en memoria C, mas tres metadatos: `shape` (cuantos elementos en cada dimension), `dtype` (como interpretar cada grupo de bytes) y `strides` (cuantos bytes avanzar en memoria para pasar al siguiente elemento de cada dimension). Todo el poder de NumPy descansa en esta representacion compacta.

**Las funciones** — las transformaciones. El namespace `np.*` expone cientos de funciones que toman ndarrays, los transforman, y devuelven ndarrays nuevos (o modifican los existentes en el lugar). Estan implementadas en C y operan sobre el buffer directamente, sin que el interprete Python intervenga elemento por elemento.

## El sabor de NumPy en diez lineas

```python
import numpy as np

# Crear una matriz 4x3 con datos reales
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              [10, 11, 12]], dtype=np.float64)

fila_media = A.mean(axis=1)          # reduccion por filas → (4,)
A_centrada = A - fila_media[:, None] # broadcasting: (4,3) - (4,1) → (4,3)
normas     = np.linalg.norm(A_centrada, axis=1)  # norma de cada fila
mascara    = normas > normas.mean()  # indexado booleano
print(A[mascara])                    # filas con norma superior a la media
```

Este fragmento ilustra los cinco mecanismos centrales de NumPy actuando juntos: creacion, reduccion con `axis`, broadcasting, algebra lineal e indexado booleano — sin un solo bucle Python.

## Como navegar el vault

El vault esta organizado en cinco bloques. El orden de lectura recomendado es de arriba a abajo: los conceptos transversales antes que las funciones, y el namespace raiz antes que los submodulos.

### `conceptos_transversales/` — el modelo mental

[[Librerias/Numpy/conceptos_transversales/index|conceptos_transversales]] contiene los diez conceptos sin los cuales ninguna funcion del API tiene sentido completo. No es documentacion de funciones: es la teoria que explica por que NumPy se comporta como se comporta. Leer aqui primero evita horas de depuracion de bugs sutiles — modificaciones inesperadas del original por compartir memoria, errores de shape en broadcasting, resultados incorrectos despues de transponer. Si solo se va a leer una seccion antes de usar NumPy, es esta.

### `np/` — el namespace raiz

[[Librerias/Numpy/np/index|np]] cubre todas las funciones que se invocan como `np.algo(...)`: creacion de arrays (`zeros`, `ones`, `arange`, `linspace`), manipulacion de forma (`reshape`, `concatenate`, `stack`, `split`), seleccion y ordenamiento, operaciones matematicas element-wise, reducciones (`sum`, `max`, `mean`), estadisticas, algebra basica, manejo de conjuntos e I/O. Es el catalogo operacional de NumPy — la referencia a consultar cuando se sabe que se quiere hacer pero no se recuerda el nombre exacto de la funcion.

### `np.ndarray/` — el objeto base

[[Librerias/Numpy/np.ndarray/index|np.ndarray]] documenta el objeto que devuelven casi todas las funciones de NumPy. Esta dividido en dos grupos: **atributos** (propiedades que describen al array — `shape`, `dtype`, `ndim`, `strides`, `flags`, `nbytes`) y **metodos** (acciones que el propio array puede ejecutar sobre si mismo — `reshape`, `copy`, `flatten`, `astype`, `view`, `transpose`). La distincion importa: los atributos son lectura, los metodos son transformacion.

### `np.linalg/` — algebra lineal

[[Librerias/Numpy/np.linalg/index|np.linalg]] es el submodulo para problemas del algebra lineal numerica: resolver sistemas de ecuaciones (`solve`), calcular inversas y determinantes, factorizar matrices (LU, QR, SVD, Cholesky), obtener autovalores y autovectores, y calcular normas matriciales y vectoriales. Esta capa llama directamente a LAPACK, la misma biblioteca que usa software de calculo numerico profesional.

### `np.random/` — numeros aleatorios

[[Librerias/Numpy/np.random/index|np.random]] cubre la generacion de numeros aleatorios de calidad cientifica. El modelo moderno usa un `Generator` explicit con semilla reproducible (`np.random.default_rng(seed)`), separando el estado del generador de las funciones de muestreo. Incluye distribuciones continuas (uniforme, normal, exponencial, beta), discretas (binomial, Poisson), muestreo sin reemplazo y permutaciones.
