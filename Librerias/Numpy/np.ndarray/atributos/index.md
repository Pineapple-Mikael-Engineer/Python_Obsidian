---
title: np.ndarray — atributos
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — atributos

Los atributos de un ndarray describen su estructura sin modificarlo. Son propiedades de solo lectura (la mayoria) que permiten inspeccionar el array sin hacer ninguna operacion. Conocerlos es fundamental para depurar shapes inesperadas y para escribir funciones que acepten arrays de cualquier dimension.

## Esenciales

Los cuatro atributos que se consultan con mas frecuencia y definen la "identidad" del array:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.shape]] | `tuple[int]` | Tupla con el tamaño de cada dimension. `(3, 4)` significa 3 filas y 4 columnas. Asignarlo directamente hace reshape in-place si la shape es compatible. |
| [[ndarray.dtype]] | `dtype` | Tipo de dato de los elementos (float64, int32, bool, etc.). Determina cuantos bytes ocupa cada elemento y que operaciones son validas. |
| [[ndarray.ndim]] | `int` | Numero de dimensiones (longitud de `shape`). Un vector tiene ndim=1, una matriz ndim=2. |
| [[ndarray.size]] | `int` | Numero total de elementos: el producto de todos los valores de `shape`. |

## Memoria

Atributos que exponen la disposicion fisica del array en memoria. Fundamentales para entender views, contiguidad y compatibilidad con C/Fortran:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.itemsize]] | `int` | Bytes que ocupa un solo elemento. `float64.itemsize == 8`, `int32.itemsize == 4`. |
| [[ndarray.nbytes]] | `int` | Bytes totales del buffer de datos: `size * itemsize`. |
| [[ndarray.strides]] | `tuple[int]` | Tupla con cuantos bytes hay que avanzar en memoria para pasar al siguiente elemento en cada dimension. La clave para entender views y contiguidad: un stride negativo indica que el array esta invertido en esa dimension. |
| [[ndarray.data]] | `memoryview` | Buffer de memoria Python que contiene los datos reales. Raramente se accede directamente; se usa a traves de los metodos de serializacion o la interfaz ctypes. |
| [[ndarray.flags]] | `flagsobj` | Informacion sobre el layout de memoria: si el array es C-contiguo (fila a fila), F-contiguo (columna a columna), de solo lectura, propietario de su memoria, etc. |

## Transformacion

Atributos que devuelven una vista transformada del mismo buffer de datos sin copiar:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.T]] | `ndarray` | Array transpuesto (vista). Para 2D intercambia filas y columnas. Para 1D no hace nada (los vectores no tienen "dimension columna"). |
| [[ndarray.flat]] | `flatiter` | Iterador que recorre todos los elementos en orden C (fila a fila). Permite acceso 1D a arrays N-dimensionales y escritura por indice plano. |

## Estado

Atributos que describen el historial del array y su relacion con otros arrays en memoria:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.base]] | `ndarray` o `None` | El array original del que este es una vista, o `None` si el array es propietario de sus datos. Clave para detectar si modificar el array afectara a otro. |

## Numeros complejos

Atributos solo relevantes cuando `dtype` es complejo; para arrays reales tambien funcionan pero `imag` devuelve ceros:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.real]] | `ndarray` | Parte real del array. Si `dtype` es complejo, es una vista del mismo buffer; si es real, es el array mismo. |
| [[ndarray.imag]] | `ndarray` | Parte imaginaria. Para arrays reales devuelve un array de ceros con el mismo shape; para complejos es una vista del buffer. |

## Interfaz de bajo nivel

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.ctypes]] | objeto ctypes | Interfaz para pasar el array a funciones C via ctypes. Expone el puntero al buffer y el shape como tipos compatibles con C. |
