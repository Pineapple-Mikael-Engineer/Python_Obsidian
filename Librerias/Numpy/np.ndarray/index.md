---
title: np.ndarray — objeto array N-dimensional
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — objeto array N-dimensional

`np.ndarray` es el objeto central de NumPy: cada vez que se llama a una funcion de NumPy, el resultado es un ndarray. Entenderlo como objeto — no solo como "array" — es importante porque tiene **atributos** que lo describen (que tipo de datos tiene, que forma, cuanto ocupa en memoria) y **metodos** que le piden que se transforme a si mismo. La distincion no es solo sintactica: los atributos son propiedades del estado del objeto; los metodos son operaciones que pueden modificarlo o crear uno nuevo.

## Anatomia del objeto

Un ndarray tiene dos partes distinguibles:

- **Metadatos** — describen el array sin tocar los datos: forma, tipo, strides, flags. Viven en los **atributos**.
- **Operaciones** — le piden al array que se transforme a si mismo. Son los **metodos**: `arr.reshape(...)`, `arr.mean()`, etc.

Esta separacion es deliberada: los atributos son de solo lectura (o casi) y los metodos producen resultados nuevos o modifican in-place con semantica explicitamente documentada.

## Diferencia con las funciones `np.X`

| Estilo | Ejemplo | Cuando usarlo |
|--------|---------|---------------|
| Metodo del objeto | `arr.reshape(3, 4)` | Encadenamiento fluido, lectura natural |
| Funcion NumPy | `np.reshape(arr, (3, 4))` | Cuando el array llega como argumento, APIs funcionales |

Ambos estilos producen el mismo resultado; la eleccion es de legibilidad.

## Subcarpetas

### [[Librerias/Numpy/np.ndarray/atributos/index|atributos/]]

15 atributos que describen el array sin modificarlo: su forma, tipo de dato, disposicion en memoria y estado interno. Se dividen en cuatro grupos segun lo que describen — los esenciales (`shape`, `dtype`, `size`, `ndim`) son los que se consultan el 90% del tiempo; los de memoria (`strides`, `itemsize`, `nbytes`) son clave para entender views y contiguidad; los de transformacion (`T`, `flat`) dan vistas alternativas del mismo buffer; y los de estado (`base`, `flags`, `real`, `imag`) exponen la relacion del array con su memoria y con otros arrays.

### [[Librerias/Numpy/np.ndarray/metodos/index|metodos/]]

34 metodos agrupados en 5 subcarpetas segun el proposito de la operacion. Los metodos de **forma** reorganizan la estructura dimensional sin tocar los datos; los de **seleccion** extraen o modifican elementos por indices o condicion; los de **reducciones** colapsan valores a lo largo de ejes (sumas, medias, extremos); los de **transformacion** cambian el tipo de dato o crean copias o vistas con interpretacion diferente; y los de **serializacion** exportan el array fuera de NumPy a disco, listas Python o bytes.
