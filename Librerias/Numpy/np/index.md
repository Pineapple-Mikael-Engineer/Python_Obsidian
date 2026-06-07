---
title: np — modulo principal de NumPy
tags:
  - numpy
  - indice
draft: false
---

# np — modulo principal de NumPy

El modulo `np` es el espacio de nombres raiz de NumPy: todo lo que se importa con `import numpy as np` queda accesible como `np.funcion()`. Agrupa ufuncs, constructores de arrays, operaciones de algebra lineal, herramientas de I/O y mas.

Las notas de esta vault estan organizadas en subcarpetas por tematica para facilitar la busqueda por contexto de uso.

## Subcarpetas

| Carpeta | Descripcion | Funciones |
|---------|-------------|-----------|
| [[Numpy/np/creacion/index\|creacion]] | Construir arrays desde cero o desde datos existentes | 11 |
| [[Numpy/np/manipulacion_forma/index\|manipulacion_forma]] | Cambiar forma, reordenar ejes, combinar y dividir arrays | 19 |
| [[Numpy/np/seleccion/index\|seleccion]] | Extraer, filtrar o modificar elementos segun condiciones o indices | 7 |
| [[Numpy/np/operaciones/index\|operaciones]] | Ufuncs aritmeticas, trigonometricas, exponenciales y de redondeo | 26 |
| [[Numpy/np/reducciones/index\|reducciones]] | Agregacion, promedios, extremos, diferencial y variantes nan-safe | 29 |
| [[Numpy/np/estadisticas/index\|estadisticas]] | Correlacion, covarianza, histogramas, percentiles y discretizacion | 8 |
| [[Numpy/np/conjuntos/index\|conjuntos]] | Operaciones de teoria de conjuntos sobre arrays 1D | 5 |
| [[Numpy/np/io/index\|io]] | Lectura y escritura de arrays en disco (texto y binario) | 8 |
| [[Numpy/np/polinomios/index\|polinomios]] | API legacy de polinomios: ajuste, evaluacion, derivacion e integracion | 6 |

## Guia de orientacion rapida

Si sabes lo que quieres hacer pero no la funcion exacta, usa esta tabla:

| Necesito… | Ir a |
|-----------|------|
| Crear un array | [[Numpy/np/creacion/index\|creacion]] |
| Cambiar el shape o combinar arrays | [[Numpy/np/manipulacion_forma/index\|manipulacion_forma]] |
| Filtrar o extraer elementos | [[Numpy/np/seleccion/index\|seleccion]] |
| Operaciones elemento a elemento | [[Numpy/np/operaciones/index\|operaciones]] |
| Suma, media, maximo por eje | [[Numpy/np/reducciones/index\|reducciones]] |
| Estadisticas avanzadas o histogramas | [[Numpy/np/estadisticas/index\|estadisticas]] |
| Union, interseccion, unicidad | [[Numpy/np/conjuntos/index\|conjuntos]] |
| Leer o guardar archivos | [[Numpy/np/io/index\|io]] |
| Trabajar con polinomios | [[Numpy/np/polinomios/index\|polinomios]] |
