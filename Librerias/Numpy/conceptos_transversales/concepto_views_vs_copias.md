---
title: Views vs Copias — Cuándo se comparte memoria
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

# Views vs Copias — Cuándo se comparte memoria

## Definición fundamental

Una **vista (view)** es un ndarray nuevo que apunta al **mismo buffer de memoria** que el original, solo que con otros `shape`, `strides` y `offset`. Una **copia (copy)** es un ndarray nuevo con su **propio buffer** independiente.

La consecuencia práctica que gobierna todo: **modificar una vista modifica el original**; modificar una copia no.

## Por qué importa la distinción

```python
import numpy as np
arr = np.array([1, 2, 3, 4, 5])

vista = arr[1:4]      # comparte buffer con arr
vista[:] = 0
arr                   # [1, 0, 0, 0, 5]  ← el original cambió

copia = arr[1:4].copy()
copia[:] = 99
arr                   # [1, 0, 0, 0, 5]  ← intacto
```

La vista es instantánea y no consume memoria de datos (solo metadatos: `shape`, `strides`, un puntero). La copia cuesta tiempo y memoria proporcionales al tamaño. El bug clásico es modificar una vista creyéndola independiente y corromper el original sin darse cuenta.

## El modelo: mismo buffer, distintos strides

Un ndarray son **datos** (el buffer plano) más **metadatos** que describen cómo recorrerlo. Una vista reutiliza el buffer y solo cambia los metadatos (ver [[concepto_ndarray|ndarray]] y sus `strides`). Por eso un slice, una transpuesta o un reshape contiguo no copian nada: solo reinterpretan el mismo bloque de bytes.

| Característica | Vista | Copia |
|---------------|-------|-------|
| Buffer de datos | Compartido con el original | Propio e independiente |
| Memoria adicional | Casi nula (solo metadatos) | Completa (todos los datos) |
| Tiempo de creación | Muy rápido (microsegundos) | Proporcional al tamaño |
| Modificar afecta al original | SÍ | NO |
| `.base` | Apunta al original (o a su ancestro) | `None` |
| `.flags.owndata` | `False` | `True` |

## La regla central: qué devuelve cada operación

| Operación | Ejemplo | Devuelve |
|-----------|---------|----------|
| Slicing básico | `arr[1:5, 2:6]` | **vista** (siempre) |
| `reshape` (si se puede) | `arr.reshape(4, 3)` | **vista** si es contiguo, copia si no |
| Transpuesta | `arr.T`, `arr.swapaxes(0, 1)` | **vista** |
| `ravel` | `arr.ravel()` | **vista** si es contiguo, copia si no |
| `squeeze` / `expand_dims` | `arr.squeeze()` | **vista** |
| Fancy indexing | `arr[[0, 2]]` | **copia** |
| Indexado booleano | `arr[arr > 0]` | **copia** |
| `flatten` | `arr.flatten()` | **copia** (siempre) |
| `copy` | `arr.copy()` | **copia** (siempre) |
| `astype` | `arr.astype(np.float64)` | **copia** |

> [!regla] La frontera vista/copia coincide con la frontera básico/avanzado
> El [[concepto_indexing|indexing]] **básico** (slices) da vistas; el **avanzado** (fancy y booleano) da copias. Y entre las funciones de forma, las que solo reordenan ejes o reinterpretan un buffer contiguo (`reshape`, `.T`, `ravel`) dan vistas; las que garantizan independencia (`flatten`, `copy`, `astype`) dan copias.

## Cómo verificar si es vista o copia

```python
arr = np.arange(12).reshape(3, 4)

vista = arr[0:2, 1:3]
np.shares_memory(arr, vista)   # True
vista.base is arr              # True

copia = arr[[0, 1]]
np.shares_memory(arr, copia)   # False
copia.base                     # None
copia.flags.owndata            # True
```

- `np.shares_memory(a, b)` es la prueba definitiva: responde si dos arrays comparten algún byte de buffer.
- `.base` apunta al array dueño del buffer (o `None` si el array es dueño).
- `.flags.owndata` es `True` cuando el array posee su propio buffer.

## El caso especial: `reshape` depende de la contigüidad

`reshape` da vista **si los datos pueden reinterpretarse sin moverlos**, lo que exige que el array sea contiguo en memoria (ver [[concepto_contiguidad_memoria|contigüidad]]). Si no lo es, NumPy se ve forzado a copiar:

```python
arr = np.arange(12).reshape(3, 4)

vista = arr.reshape(12)
np.shares_memory(arr, vista)        # True  → contiguo, vista

copia = arr.T.reshape(12)           # arr.T no es contiguo
np.shares_memory(arr, copia)        # False → tuvo que copiar
```

Lo mismo para `ravel` (vista si puede) frente a `flatten` (copia siempre).

## Ejemplos progresivos N-D

### Vista de un tensor `(b, n, m)`

```python
a = np.arange(24).reshape(2, 3, 4)

plano = a[0]                  # primer lote, shape (3, 4) → VISTA
plano[0, 0] = 999
a[0, 0, 0]                    # 999  ← cambió el original

sub = a[:, 1:, ::2]           # slicing básico en 3 ejes → VISTA
np.shares_memory(a, sub)      # True
```

### Fancy/booleano en N-D siempre copia

```python
a = np.arange(24).reshape(2, 3, 4)

lotes = a[[1, 0]]             # fancy sobre el eje 0 → COPIA, shape (2,3,4)
np.shares_memory(a, lotes)    # False

positivos = a[a > 10]         # booleano → COPIA 1D
np.shares_memory(a, positivos)# False
```

## Casos que fallan (errores típicos)

### Error 1: modificar un slice creyéndolo independiente

```python
arr = np.array([1, 2, 3, 4, 5])
vista = arr[1:4]
vista[:] = 0
arr                  # [1, 0, 0, 0, 5]  ← se modificó sin querer
# Solución: arr[1:4].copy() si se necesita independencia
```

### Error 2: `b = a` vs `b = a[:]` vs `b = a.copy()`

Tres formas que parecen iguales y no lo son:

```python
a = np.arange(5)

b = a            # MISMO objeto: b is a → True; no es ni vista ni copia
c = a[:]         # VISTA: objeto distinto, mismo buffer
d = a.copy()     # COPIA: buffer propio

b is a                       # True
np.shares_memory(a, c)       # True   (vista)
np.shares_memory(a, d)       # False  (copia)

c[0] = 99
a[0]             # 99  ← la vista propagó el cambio
```

### Error 3: asumir que `reshape` siempre es gratis

```python
arr = np.random.rand(1000, 1000)
vista = arr.reshape(1000000)        # rápido: vista (contiguo)
copia = arr.T.reshape(1000000)      # lento: copia (no contiguo)
```

## Reglas prácticas

| Situación | Recomendación |
|-----------|---------------|
| Solo lectura de datos | Usar vista (más eficiente) |
| Modificar sin afectar al original | Usar `.copy()` explícitamente |
| No saber si se necesita independencia | Usar `.copy()` para estar seguro |
| Operar con arrays no contiguos | Esperar copias en `reshape`/`ravel` |
| Indexado avanzado o booleano | Asumir que crea copia |
| Necesitar garantía de vista | Usar slicing básico |

## Relación con otros conceptos

- [[concepto_ndarray]]
- [[concepto_contiguidad_memoria]]
- [[concepto_indexing]]
- [[np.reshape]]
- [[np.ravel]]
- [[ndarray.flatten]]
- [[ndarray.copy]]
- [[ndarray.base]]
- [[ndarray.flags]]
