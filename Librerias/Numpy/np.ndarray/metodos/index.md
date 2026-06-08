---
title: np.ndarray — metodos
tags:
  - numpy
  - indice
draft: false
---

# np.ndarray — metodos

Los 34 metodos del ndarray son operaciones que el array realiza sobre si mismo: `arr.metodo()`. La mayoria tiene una funcion equivalente en el namespace `np` (`arr.sum()` equivale a `np.sum(arr)`), pero los metodos son mas concisos para uso interactivo y permiten encadenamiento fluido: `arr.reshape(-1).cumsum()`.

```python
# Funcion
np.sum(arr, axis=0)

# Metodo equivalente — mismo resultado, mas conciso
arr.sum(axis=0)
```

La diferencia funcional es que los metodos a veces tienen comportamientos por defecto distintos a sus contrapartes funcionales, pero en la gran mayoria de casos el resultado es identico.

## Subcarpetas

### [[Librerias/Numpy/np.ndarray/metodos/forma/index|forma/]]

6 metodos para cambiar la estructura dimensional del array sin tocar los datos. `reshape` asigna una nueva forma compatible y devuelve vista si el array es contiguo; `ravel` y `flatten` aplanan a 1D con la diferencia clave de que `ravel` devuelve vista cuando es posible y `flatten` siempre devuelve copia; `transpose` y `swapaxes` reordenan los ejes (siempre vista); `squeeze` elimina las dimensiones de tamaño 1 que dejan residuos de forma como `(1, n, 1)`.

### [[Librerias/Numpy/np.ndarray/metodos/seleccion/index|seleccion/]]

4 metodos para extraer o modificar elementos por indices o condiciones booleanas. `take` extrae elementos por indices con soporte explicito de `axis` (equivalente mas legible al fancy indexing); `put` escribe in-place usando indices planos; `compress` filtra filas o columnas donde una mascara booleana es `True`; `nonzero` devuelve las posiciones de todos los elementos distintos de cero, uno por dimension, listas para usar directamente como indices.

### [[Librerias/Numpy/np.ndarray/metodos/reducciones/index|reducciones/]]

14 metodos que colapsan el array (o uno de sus ejes) a un resultado de menor dimension. Incluyen suma y producto con sus versiones acumuladas (`sum`, `cumsum`, `prod`, `cumprod`); estadistica descriptiva (`mean`, `var`, `std` con soporte de `ddof=`); localizacion de extremos (`min`, `max`, `argmin`, `argmax`); y utilidades de preprocesado (`clip` para recortar valores a un rango, `round` para redondear decimales).

### [[Librerias/Numpy/np.ndarray/metodos/transformacion/index|transformacion/]]

5 metodos que cambian el tipo de dato, la interpretacion de los bytes o el contenido del array. La distincion vista/copia/in-place es critica: `astype` siempre copia y convierte valores; `view` reinterpreta los mismos bytes sin copiar; `copy` garantiza una copia profunda independiente; `fill` rellena todos los elementos in-place sin devolver nada; `byteswap` invierte el orden de bytes para compatibilidad de endianness entre arquitecturas.

### [[Librerias/Numpy/np.ndarray/metodos/serializacion/index|serializacion/]]

5 metodos para exportar el array fuera del ecosistema NumPy. `tofile` escribe los bytes crudos a disco sin metadatos (maximo rendimiento, minima portabilidad); `dump` serializa con pickle preservando dtype y shape; `tolist` convierte a lista Python anidada de escalares nativos (util para JSON); `tobytes` devuelve el buffer crudo como objeto `bytes` en memoria; `dumps` hace lo mismo que `dump` pero devuelve `bytes` en vez de escribir a archivo.
