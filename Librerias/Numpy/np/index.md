---
title: np — fachada principal de NumPy
tags:
  - numpy
  - indice
draft: false
---

# np — fachada principal de NumPy

`np` no es un submodulo: es la fachada completa de NumPy. Todo lo que se importa con `import numpy as np` queda accesible directamente como `np.funcion()`, sin importar en que parte del codigo fuente de NumPy vive internamente. La fachada expone constructores de arrays, ufuncs, reducciones, herramientas de IO y mucho mas — siempre operando sobre `ndarray` como tipo central.

La organizacion de este vault divide ese espacio de nombres plano en subcarpetas tematicas. Cada subcarpeta responde a una pregunta de uso: ¿quiero construir un array? ¿reorganizarlo? ¿filtrar elementos? ¿calcular algo sobre el?

## Subcarpetas

| Carpeta | Lo que agrupa |
|---------|---------------|
| [[Numpy/np/creacion/index\|creacion]] | Como construir un ndarray desde cero o desde datos existentes — la eleccion correcta de funcion evita copias implicitas y errores de dtype |
| [[Numpy/np/manipulacion_forma/index\|manipulacion_forma]] | Como reorganizar la estructura de un array (shape, ejes, combinaciones, divisiones) sin alterar sus datos |
| [[Numpy/np/seleccion/index\|seleccion]] | Como extraer, filtrar o modificar elementos segun condiciones logicas o listas de indices — alternativa funcional al indexado directo |
| [[Numpy/np/operaciones/index\|operaciones]] | Ufuncs element-wise: aritmetica, trigonometria, exponenciales y logaritmos, redondeo y signo — operan en paralelo sobre todos los elementos del array |
| [[Numpy/np/reducciones/index\|reducciones]] | Funciones que colapsan un eje: suma, media, extremos, diferencias acumuladas — cada una acepta el parametro `axis=` para reducir en la dimension deseada |
| [[Numpy/np/estadisticas/index\|estadisticas]] | Analisis mas alla del resumen simple: correlacion, covarianza, distribucion de frecuencias (histogramas) y cuantiles |
| [[Numpy/np/conjuntos/index\|conjuntos]] | Operaciones de teoria de conjuntos sobre arrays 1D: unicidad, union, interseccion, diferencia — mas rapidas que `set` de Python para datos numericos grandes |
| [[Numpy/np/io/index\|io]] | Lectura y escritura de arrays en disco — texto (CSV) o binario NumPy (`.npy`/`.npz`), con preservacion exacta de dtype y shape en el formato binario |
| [[Numpy/np/polinomios/index\|polinomios]] | API legacy de polinomios como arrays de coeficientes: ajuste, evaluacion, derivacion, integracion y calculo de raices |

## Orientacion rapida

| Quiero… | Ir a |
|---------|------|
| Crear un array | [[Numpy/np/creacion/index\|creacion]] |
| Cambiar el shape o combinar arrays | [[Numpy/np/manipulacion_forma/index\|manipulacion_forma]] |
| Filtrar o extraer elementos | [[Numpy/np/seleccion/index\|seleccion]] |
| Operaciones elemento a elemento | [[Numpy/np/operaciones/index\|operaciones]] |
| Suma, media, maximo por eje | [[Numpy/np/reducciones/index\|reducciones]] |
| Correlacion, histogramas, percentiles | [[Numpy/np/estadisticas/index\|estadisticas]] |
| Union, interseccion, unicidad | [[Numpy/np/conjuntos/index\|conjuntos]] |
| Leer o guardar archivos | [[Numpy/np/io/index\|io]] |
| Trabajar con polinomios | [[Numpy/np/polinomios/index\|polinomios]] |
