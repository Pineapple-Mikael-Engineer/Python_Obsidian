---
title: np.ndarray — metodos
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos

Los 34 metodos del ndarray se llaman directamente sobre el objeto: `arr.metodo()`. A diferencia de las funciones `np.X`, que reciben el array como primer argumento, los metodos son "bound": el array es `self`.

```python
# Funcion
np.sum(arr, axis=0)

# Metodo equivalente
arr.sum(axis=0)
```

Ambas formas producen el mismo resultado. Los metodos permiten encadenamiento fluido: `arr.reshape(-1).cumsum()`.

## Subcarpetas

| Subcarpeta | Metodos | Que hacen |
|------------|---------|-----------|
| [[Librerias/Numpy/np.ndarray/metodos/forma/index\|forma/]] | 6 | Modificar la forma del array: reshape, aplanar, transponer, eliminar ejes unitarios |
| [[Librerias/Numpy/np.ndarray/metodos/seleccion/index\|seleccion/]] | 4 | Extraer o modificar elementos por indices o condicion booleana |
| [[Librerias/Numpy/np.ndarray/metodos/reducciones/index\|reducciones/]] | 14 | Reducir el array a un escalar o un array de menor dimension: sumas, medias, extremos |
| [[Librerias/Numpy/np.ndarray/metodos/transformacion/index\|transformacion/]] | 5 | Cambiar el tipo, la vista o el contenido del array |
| [[Librerias/Numpy/np.ndarray/metodos/serializacion/index\|serializacion/]] | 5 | Exportar el array fuera de NumPy: disco, lista Python, bytes |
