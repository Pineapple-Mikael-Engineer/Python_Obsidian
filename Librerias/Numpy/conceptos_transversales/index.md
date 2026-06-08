---
title: conceptos_transversales — el modelo mental de NumPy
tags:
  - numpy
  - indice
draft: false
---

# conceptos_transversales — el modelo mental de NumPy

Esta carpeta es la mas importante del vault NumPy. Antes de saber que funciones existen hay que entender como piensa NumPy — porque en este ecosistema los conceptos no son "contexto opcional": son los prerrequisitos que determinan si el resultado de una funcion tiene sentido o no.

Una llamada como `np.sum(a, axis=1)` parece trivial hasta que se necesita saber: que forma tiene el resultado, por que el resultado tiene una dimension menos, que pasa si `a` es una vista de otro array, que diferencia hay con `a.sum(axis=1)`. Ninguna de esas preguntas se puede responder sin entender [[concepto_ndarray]], [[concepto_shape]] y [[concepto_axis_parametro]] primero. El API de NumPy es una superficie pequena; el modelo mental que lo gobierna es lo que hay que dominar.

## Por que los conceptos gobiernan

NumPy expone mas de 600 funciones en su namespace publico. Memorizarlas no es la estrategia correcta. La estrategia correcta es entender las diez ideas de esta carpeta, porque con ellas se puede:

- **Predecir** el shape del resultado de cualquier operacion sin ejecutarla
- **Razonar** sobre si una asignacion modifica el array original o uno nuevo
- **Diagnosticar** por que dos arrays con shapes "compatibles" producen un error de broadcasting
- **Optimizar** codigo identificando donde hay copias innecesarias o iteracion en Python

Los diez conceptos no son independientes — forman un grafo de dependencias. Aprenderlos en el orden correcto evita la confusion de estudiar broadcasting antes de entender shape, o vistas antes de entender el ndarray.

## El grafo de dependencias

```
concepto_ndarray
    ├── concepto_shape
    │       ├── concepto_axis_parametro
    │       └── concepto_broadcasting
    ├── concepto_dtype
    └── concepto_views_vs_copias
            ├── concepto_contiguidad_memoria
            └── concepto_indexing

concepto_broadcasting ──► concepto_vectorizacion ──► concepto_ufuncs
```

El [[concepto_ndarray]] es la raiz: define que es un array. De el dependen [[concepto_shape]] (como esta organizado el espacio logico), [[concepto_dtype]] (como se interpretan los bytes) y [[concepto_views_vs_copias]] (si las operaciones comparten o duplican memoria). El [[concepto_broadcasting]] y el [[concepto_axis_parametro]] requieren [[concepto_shape]]. La [[concepto_vectorizacion]] es la consecuencia practica del broadcasting, y las [[concepto_ufuncs]] son su implementacion concreta.

## Los diez conceptos

### [[concepto_ndarray]] — la estructura base

El ndarray es un buffer de bytes contiguo en memoria C mas tres metadatos: `shape`, `dtype` y `strides`. Los strides son la clave oculta: dicen cuantos bytes hay que avanzar en el buffer para pasar al siguiente elemento de cada dimension. Entender esto explica por que `a.T` no copia datos (solo invierte los strides), por que las operaciones son rapidas (el buffer ya esta en cache de CPU) y por que mezclar tipos de datos inesperadamente puede duplicar el uso de memoria.

### [[concepto_shape]] — el espacio logico del array

La shape es una tupla de enteros, uno por dimension, que indica cuantos elementos hay en esa dimension. Un array `(3, 4)` tiene 3 filas y 4 columnas; un array `(3,)` es un vector de 3 elementos; un array `(3, 1)` es una columna de 3 elementos — diferente de `(3,)` a efectos de broadcasting. La shape gobierna que operaciones son validas, que significa el parametro `axis` y como se alinean los arrays en broadcasting.

### [[concepto_dtype]] — el tipo de dato homogeneo

Cada array NumPy tiene un unico dtype: todos sus elementos ocupan el mismo numero de bytes y se interpretan de la misma manera. El dtype determina la precision de los calculos, el uso de memoria y las conversiones implicitas. NumPy infiere el dtype al crear arrays y puede sorprender: mezclar una lista de enteros con un float produce `float64`; operar un `int32` con un `float32` produce `float64`. Saber esto previene acumulaciones de error numerico y usos innecesarios de memoria.

### [[concepto_views_vs_copias]] — compartir o duplicar memoria

La mayoria de las operaciones de slicing y reshape devuelven una **vista**: un nuevo objeto ndarray que apunta al mismo buffer de bytes que el original. Modificar la vista modifica el original. Este es el error mas frecuente en codigo NumPy intermedio — y tambien es una feature de rendimiento cuando se usa deliberadamente. Una copia explicita requiere `.copy()`. La forma de verificar si dos arrays comparten memoria es `np.shares_memory(a, b)`.

### [[concepto_contiguidad_memoria]] — el layout fisico del buffer

Un array es **C-contiguo** (row-major) si sus filas estan almacenadas de forma consecutiva en memoria; es **F-contiguo** (column-major) si son las columnas. La mayoria de arrays NumPy son C-contiguos. Transponer con `.T` invierte los strides pero no mueve datos, por lo que el resultado es F-contiguo. Esto importa al pasar arrays a codigo C/Fortran externo, al hacer reshape despues de transponer (que fuerza una copia), y al iterar sobre dimensiones en bucles de bajo nivel.

### [[concepto_indexing]] — tres tipos de acceso

NumPy tiene tres mecanismos de indexado con comportamientos distintos. El **indexado basico** (enteros y slices, `a[1:3, :]`) siempre devuelve una vista. El **indexado avanzado** (fancy indexing con arrays de enteros, `a[[0, 2], :]`) siempre devuelve una copia. El **indexado booleano** (mascara, `a[a > 0]`) siempre devuelve una copia. Confundir basico con avanzado es la segunda fuente mas comun de bugs de modificacion inesperada despues de las vistas.

### [[concepto_axis_parametro]] — el parametro mas confundido

El parametro `axis` en funciones como `sum`, `mean`, `max`, `concatenate` especifica la dimension sobre la que opera la funcion — no la dimension que queda en el resultado, sino la que **desaparece**. `axis=0` opera "hacia abajo" (colapsa las filas); `axis=1` opera "hacia los lados" (colapsa las columnas). Para un array `(m, n)`, `a.sum(axis=0)` devuelve `(n,)` y `a.sum(axis=1)` devuelve `(m,)`. La regla es: el axis indicado es el que se consume.

### [[concepto_broadcasting]] — alineacion automatica de shapes

Cuando dos arrays tienen shapes incompatibles, NumPy intenta alinearlos siguiendo dos reglas: primero rellena con 1s por la izquierda hasta igualar el numero de dimensiones, luego estira las dimensiones de tamaño 1 para igualar las de tamaño mayor. Este "estiramiento" es virtual — no se copia memoria. Broadcasting elimina la necesidad de loops explicitos para operar un vector sobre cada fila de una matriz, o una constante sobre todo un array. Entender cuando dos shapes son compatibles requiere dominar la shape primero.

### [[concepto_vectorizacion]] — operaciones sin bucles Python

Vectorizar significa escribir operaciones sobre arrays enteros en lugar de iterar elemento por elemento con un bucle Python. El codigo resultante es 10 a 100 veces mas rapido porque el bucle ocurre en C, donde no hay overhead de interpretacion, boxing de tipos ni llamadas a funciones dinamicas. La habilidad de vectorizar — transformar un bucle en una expresion de arrays — es la competencia central de NumPy. Requiere pensar en formas y en como las operaciones se propagan sobre dimensiones, no en indices individuales.

### [[concepto_ufuncs]] — las funciones universales

Las ufuncs (universal functions) son el mecanismo de implementacion de la vectorizacion: funciones compiladas en C que operan element-wise sobre arrays, soportan broadcasting automatico y tienen parametros avanzados como `out=` (escribir el resultado en un array preasignado para evitar una allocation) y `where=` (aplicar la operacion solo donde una condicion booleana es verdadera). Ejemplos: `np.add`, `np.multiply`, `np.sin`, `np.exp`. Las operaciones `+`, `-`, `*` entre arrays son syntax sugar sobre las ufuncs correspondientes.

## Orden de lectura sugerido

| # | Concepto | Por que en este orden |
|---|---|---|
| 1 | [[concepto_ndarray]] | Es la base de todo; define que es un array y como esta representado en memoria |
| 2 | [[concepto_shape]] | El primer metadato que se usa en cualquier operacion; necesario para los siguientes ocho |
| 3 | [[concepto_dtype]] | Complementa la shape; juntos describen completamente el contenido del array |
| 4 | [[concepto_views_vs_copias]] | Antes de hacer cualquier slicing o reshape; evita el bug mas frecuente de NumPy |
| 5 | [[concepto_contiguidad_memoria]] | Explica por que algunos reshape producen copias y otros no; dependiente de vistas |
| 6 | [[concepto_indexing]] | Extiende las vistas al acceso por indices arbitrarios; requiere entender cuando hay copia |
| 7 | [[concepto_axis_parametro]] | Necesario antes de usar cualquier funcion de reduccion (`sum`, `mean`, `max`…) |
| 8 | [[concepto_broadcasting]] | Requiere dominar shape y axis; explica como se combinan arrays de shapes distintas |
| 9 | [[concepto_vectorizacion]] | La consecuencia practica del broadcasting; como pensar en arrays en lugar de bucles |
| 10 | [[concepto_ufuncs]] | El mecanismo concreto que implementa la vectorizacion; profundiza en el motor interno |

---

- [[Librerias/Numpy/index|NumPy — indice raiz]]
- [[Librerias/Numpy/np/index|np — namespace raiz]]
- [[Librerias/Numpy/np.ndarray/index|np.ndarray — el objeto]]
