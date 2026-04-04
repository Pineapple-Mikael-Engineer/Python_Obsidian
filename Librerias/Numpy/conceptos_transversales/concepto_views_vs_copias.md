---
title: Views vs Copias — Cuando se comparte memoria
aliases:
  - view
  - copy
  - vista
  - copia
  - memoria compartida
tags:
  - numpy
  - concepto
  - memoria
  - rendimiento
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_contiguidad_memoria
draft: false
---

# Views vs Copias — Cuando se comparte memoria

## Definicion fundamental

En NumPy, una **vista (view)** es un nuevo array que comparte el buffer de memoria con el array original. Una **copia (copy)** es un nuevo array con su propio buffer de memoria independiente.

La distincion es critica porque:
- Las vistas son instantaneas y usan poca memoria
- Las copias consumen tiempo y memoria adicional
- Modificar una vista modifica el original
- Modificar una copia no afecta al original

## Comparacion fundamental

| Caracteristica | Vista | Copia |
|----------------|-------|-------|
| Memoria adicional | Casi nula (solo metadatos) | Completa (todos los datos) |
| Tiempo de creacion | Muy rapido (microsegundos) | Lento (proporcional al tamaño) |
| Comparte datos con original | SI | NO |
| Modificar afecta al original | SI | NO |
| `flags.owndata` | `False` | `True` |
| `base` atributo | Apunta al original | `None` |

## Cuando se crea una vista

### Operaciones que tipicamente crean vistas

| Operacion | Ejemplo | ¿Vista? |
|-----------|---------|---------|
| Slicing | `arr[1:5, 2:6]` | SI (siempre) |
| reshape (si es posible) | `arr.reshape(4, 3)` | SI (si contiguo) |
| transpose | `arr.T` | SI |
| ravel (a veces) | `arr.ravel()` | SI (si contiguo) |
| squeeze | `arr.squeeze()` | SI |
| expand_dims | `np.expand_dims(arr, 0)` | SI |
| swapaxes | `arr.swapaxes(0, 1)` | SI |

### Verificacion practica

```python
import numpy as np

arr = np.arange(12).reshape(3, 4)

vista = arr[0:2, 1:3]
print(vista.base is arr)  # True

vista_reshape = arr.reshape(4, 3)
print(vista_reshape.base is arr)  # True

vista_t = arr.T
print(vista_t.base is arr)  # True

vista[0, 0] = 999
print(arr[0, 1])  # 999
```

## Cuando se crea una copia

### Operaciones que tipicamente crean copias

| Operacion | Ejemplo | ¿Copia? |
|-----------|---------|---------|
| copy() | `arr.copy()` | SI (siempre) |
| reshape (si no es contiguo) | `arr.T.reshape(12)` | SI |
| ravel (si no es contiguo) | `arr.T.ravel()` | SI |
| flatten | `arr.flatten()` | SI (siempre) |
| astype | `arr.astype(np.float64)` | SI |
| Indexado avanzado | `arr[[0, 1, 2]]` | SI |
| Indexado booleano | `arr[arr > 5]` | SI |

### Verificacion practica

```python
arr = np.arange(12).reshape(3, 4)

copia = arr.copy()
print(copia.base is arr)  # False
print(copia.flags.owndata)  # True

copia_idx = arr[[0, 1, 2], [0, 1, 2]]
print(copia_idx.base is arr)  # False

copia_flat = arr.flatten()
print(copia_flat.base is arr)  # False

copia[0, 0] = 999
print(arr[0, 0])  # 0
```

## El caso especial: reshape

reshape es la operacion mas confusa respecto a vistas vs copias. Para entender completamente este caso, es necesario comprender como NumPy organiza los datos en memoria (ver [[concepto_contiguidad_memoria]]).

### Regla: reshape crea vista SI es posible

| Condicion | Resultado | Ejemplo |
|-----------|-----------|---------|
| Array contiguo (C-order) | Vista | `arr.reshape(12)` |
| Array contiguo (F-order) | Vista | `arr.reshape(12)` |
| Array no contiguo | Copia | `arr.T.reshape(12)` |

### Ejemplo del caso problematico

```python
arr = np.arange(12).reshape(3, 4)

vista = arr.reshape(12)
print(vista.base is arr)  # True

arr_transpuesta = arr.T
copia = arr_transpuesta.reshape(12)
print(copia.base is arr_transpuesta)  # False
print(copia.flags.owndata)  # True
```

## El caso especial: ravel vs flatten

| Funcion | Comportamiento | Recomendacion |
|---------|---------------|---------------|
| ravel | Vista si es posible, copia si no | Preferida (mas eficiente) |
| flatten | Siempre copia | Usar solo si se necesita copia garantizada |

```python
arr = np.arange(12).reshape(3, 4)

vista = arr.ravel()
print(vista.base is arr)  # True

copia = arr.flatten()
print(copia.base is arr)  # False

arr_t = arr.T
vista_o_copia = arr_t.ravel()
print(vista_o_copia.base is arr_t)  # False
```

## Como verificar si es vista o copia

### Metodo 1: Atributo base

El atributo [[ndarray.base]] permite saber si un array comparte memoria con otro.

```python
arr = np.arange(10)

vista = arr[0:5]
print(vista.base is arr)  # True → es vista

copia = arr.copy()
print(copia.base is arr)  # False → es copia
```

### Metodo 2: Flag owndata

```python
arr = np.arange(10)
print(arr.flags.owndata)  # True

vista = arr[0:5]
print(vista.flags.owndata)  # False

copia = arr.copy()
print(copia.flags.owndata)  # True
```

### Metodo 3: Modificar y observar

```python
arr = np.arange(5)
vista = arr[0:3]
copia = arr[0:3].copy()

vista[0] = 999
copia[0] = 888

print(arr)  # [999, 1, 2, 3, 4]
```

## Implicancias de memoria y rendimiento

### Tiempo de creacion

```python
import time

arr = np.random.rand(10000000)

inicio = time.time()
vista = arr[0:5000000]
print(f"Vista: {time.time() - inicio:.6f} seg")

inicio = time.time()
copia = arr[0:5000000].copy()
print(f"Copia: {time.time() - inicio:.6f} seg")
```

### Memoria utilizada

```python
arr = np.random.rand(10000000)

vista = arr[0:5000000]
copia = arr[0:5000000].copy()

print(f"Original: {arr.nbytes / 1024 / 1024:.1f} MB")
print(f"Vista: {vista.nbytes / 1024 / 1024:.1f} MB")
print(f"Copia: {copia.nbytes / 1024 / 1024:.1f} MB")
```

## Problemas comunes por no entender views

### Problema 1: Modificar sin querer el original

```python
arr = np.array([1, 2, 3, 4, 5])
vista = arr[1:4]
vista[:] = 0
print(arr)  # [1, 0, 0, 0, 5]
```

**Solucion:** Usar `.copy()` si se necesita independencia.

### Problema 2: Asumir que reshape siempre es gratis

```python
arr = np.random.rand(1000, 1000)
arr_t = arr.T

copia = arr_t.reshape(1000000)  # Lento (copia)
vista = arr.reshape(1000000)    # Rapido (vista)
```

### Problema 3: Cadenas de operaciones que fuerzan copias

```python
arr = np.random.rand(100, 100)
resultado = arr[::2, ::2].T.reshape(50, 25)
print(resultado.flags.owndata)  # Puede ser True
```

## Reglas practicas

| Situacion | Recomendacion |
|-----------|---------------|
| Solo lectura de datos | Usar vista (mas eficiente) |
| Modificar sin afectar original | Usar `.copy()` explicitamente |
| No saber si se necesita independencia | Usar `.copy()` para estar seguro |
| Operar con arrays no contiguos | Esperar posibles copias en reshape |
| Indexado avanzado o booleano | Asumir que crea copia |
| Necesitar garantia de vista | Usar slicing simple |

## Relacion con otros conceptos

- [[concepto_ndarray]]
- [[concepto_contiguidad_memoria]]
- [[np.reshape]]
- [[np.ravel]]
- [[ndarray.flatten]]
- [[ndarray.copy]]
- [[ndarray.base]]
- [[ndarray.flags]]
