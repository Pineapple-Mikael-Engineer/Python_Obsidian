---
title: np.ndarray — objeto array N-dimensional
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — objeto array N-dimensional

`np.ndarray` es el objeto central de NumPy. Toda funcion de NumPy devuelve o trabaja con un ndarray; las funciones son, en esencia, envolturas que operan sobre este unico tipo de objeto.

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

### `atributos/`

15 atributos que describen el array: su forma, tipo de dato, disposicion en memoria y estado de los flags. Ver [[Librerias/Numpy/np.ndarray/atributos/index|atributos/index]].

### `metodos/`

34 metodos agrupados en 5 categorias segun lo que hacen con el array. Ver [[Librerias/Numpy/np.ndarray/metodos/index|metodos/index]].
