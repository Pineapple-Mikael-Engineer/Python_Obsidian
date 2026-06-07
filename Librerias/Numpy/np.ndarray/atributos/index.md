---
title: np.ndarray — atributos
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — atributos

Los 15 atributos del ndarray describen el array sin modificarlo. Son metadatos: forma, tipo, disposicion en memoria y estado interno.

## Grupos

### Esenciales

Los cuatro atributos que se consultan con mas frecuencia y definen la "identidad" del array:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.shape]] | `tuple[int]` | Tamaño de cada dimension |
| [[ndarray.dtype]] | `dtype` | Tipo de dato de cada elemento |
| [[ndarray.size]] | `int` | Numero total de elementos |
| [[ndarray.ndim]] | `int` | Numero de dimensiones (rango) |

### Memoria

Atributos que exponen la disposicion fisica del array en memoria:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.itemsize]] | `int` | Bytes que ocupa un solo elemento |
| [[ndarray.nbytes]] | `int` | Bytes totales del buffer de datos |
| [[ndarray.strides]] | `tuple[int]` | Bytes a avanzar por eje para llegar al siguiente elemento |
| [[ndarray.data]] | `memoryview` | Buffer de bytes crudo (raramente usado directamente) |
| [[ndarray.ctypes]] | objeto ctypes | Interfaz con la libreria ctypes de C |

### Transformacion

Atributos que devuelven una vista transformada del array:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.T]] | `ndarray` | Vista transpuesta (ejes invertidos) |
| [[ndarray.flat]] | `flatiter` | Iterador plano sobre todos los elementos |

### Estado

Atributos que describen el historial o las propiedades de escritura del array:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.base]] | `ndarray` o `None` | Array del que este es vista; `None` si posee sus datos |
| [[ndarray.flags]] | `flagsobj` | Informacion sobre contiguidad, escritura, orden C/F |

### Numeros complejos

Atributos solo relevantes cuando `dtype` es complejo:

| Atributo | Tipo | Descripcion |
|----------|------|-------------|
| [[ndarray.real]] | `ndarray` | Parte real (vista si complejo, el array mismo si real) |
| [[ndarray.imag]] | `ndarray` | Parte imaginaria (vista de ceros si dtype es real) |
