---
title: np.isin — máscara booleana de pertenencia, conserva la shape
aliases:
  - isin
  - np.isin
  - pertenencia
tags:
  - numpy
  - api/funcion
  - conjuntos

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.isin — máscara booleana de pertenencia, conserva la shape

`np.isin` responde, **elemento a elemento**, a la pregunta "¿este valor está en el conjunto de
prueba?". Devuelve un array **booleano con exactamente el mismo shape que `element`**, donde cada
posición es `True` si su valor aparece en `test_elements`. Es la única operación de conjunto de
NumPy que **conserva la forma** de su entrada (las demás aplanan y devuelven 1D), lo que la hace
ideal para filtrar y enmascarar matrices y tensores. Es el **reemplazo moderno** de la antigua
`np.in1d` (que siempre devolvía 1D).

## La idea

La operación es la **pertenencia** $\in$ evaluada en cada celda. A diferencia de las demás funciones
de este grupo, no produce un conjunto: produce una **máscara** del mismo tamaño que la entrada.

$$ \text{isin}(E, T)_{\,i} \;=\; \big( E_i \in T \big) \;\in\; \{\text{True}, \text{False}\} $$

El **mapa de shapes** es la clave y lo que la distingue del resto del grupo: la salida copia el shape
de `element`, no se aplana.

$$ E\ \text{de shape}\ (n_0,\dots,n_k)\ \xrightarrow{\ \text{isin}\ }\ \text{máscara bool de shape}\ (n_0,\dots,n_k) $$

`test_elements` sí se trata como un conjunto plano (su shape no importa, solo sus valores).

```python
import numpy as np
np.isin([1, 2, 3, 4], [2, 4])   # array([False,  True, False,  True])
```

## Firma

```python
np.isin(
    element,                 # array_like: valores a comprobar (la salida hereda SU shape)
    test_elements,           # array_like: conjunto contra el que se comprueba (se aplana)
    assume_unique=False,     # bool: True salta la deduplicación interna (más rápido)
    invert=False,            # bool: True devuelve "NO está en" (niega la máscara)
    *,
    kind=None,               # None | 'sort' | 'table': estrategia interna de búsqueda
) -> ndarray  # bool, shape de element
```

## Los parámetros en detalle

### `element` — los valores a comprobar
`array_like` de **cualquier shape**. La máscara de salida tiene exactamente este shape. Es lo que
diferencia a `isin` del resto del grupo: aquí la forma de la entrada **sí importa y se conserva**.

### `test_elements` — el conjunto de prueba
`array_like`. Se trata como un **conjunto plano**: solo cuentan sus valores, no su shape. Cada
elemento de `element` se busca dentro de este conjunto.

### `assume_unique` — saltarse la deduplicación
`bool`. Si garantizas que las entradas no tienen duplicados, `True` acelera. Con duplicados
presentes y `True`, el resultado puede ser incorrecto.

### `invert` — negar la máscara
`bool`. Si `True`, devuelve `True` donde el elemento **NO** está en `test_elements`. Equivale a
`~np.isin(...)` pero en una sola pasada.

```python
np.isin([1, 2, 3, 4], [2, 4], invert=True)   # [ True, False,  True, False]
```

### `kind` — estrategia de búsqueda
`None | 'sort' | 'table'`. Pista de rendimiento. `'sort'` usa búsqueda por ordenación (general);
`'table'` usa una tabla de presencia (muy rápida con enteros de rango acotado, pero usa memoria
proporcional al rango). `None` (defecto) deja que NumPy elija. Rara vez hace falta tocarlo.

## El caso N-D

Aquí **sí** hay caso N-D, y es la razón de ser de `isin`: la máscara replica el shape de `element`,
por grande que sea. Cada celda se evalúa de forma independiente contra el conjunto `test_elements`.

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])              # shape (2, 3)
permitidos = [2, 4, 6]

mascara = np.isin(M, permitidos)
# [[False,  True, False],
#  [ True, False,  True]]              → shape (2, 3), igual que M

M[mascara]          # [2, 4, 6]        → seleccionar (esto sí aplana, es indexing booleano)
M[~mascara] = 0     # poner a 0 lo no permitido, in-place
```

Con un tensor 3D la máscara sigue copiando el shape:

```python
T = np.arange(24).reshape(2, 3, 4)
np.isin(T, [0, 5, 23]).shape   # (2, 3, 4)  → la máscara conserva las tres dimensiones
```

## Casos de uso

### Filtrar las filas/celdas de una matriz por un conjunto permitido
```python
datos = np.array([[10, 99, 30], [99, 50, 99]])
codigos_validos = [10, 30, 50]
limpio = np.where(np.isin(datos, codigos_validos), datos, -1)
# [[ 10,  -1,  30],
#  [ -1,  50,  -1]]   → reemplaza lo no válido por -1, conservando el shape
```

### Excluir valores prohibidos conservando la forma (con `invert`)
```python
imagen = np.array([[0, 5, 7], [7, 2, 0]])
fondo = [0, 7]
es_objeto = np.isin(imagen, fondo, invert=True)   # True donde NO es fondo
```

### Máscara de pertenencia a un vocabulario
```python
tokens = np.array(['hola', 'xyz', 'mundo', 'foo'])
vocab  = np.array(['hola', 'mundo', 'adios'])
np.isin(tokens, vocab)   # [ True, False,  True, False]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar 1D y recibir la shape de `element` | `isin` **conserva la forma** del primer argumento | es lo correcto; usa [[np.intersect1d]] si quieres el conjunto plano |
| Usar la vieja `np.in1d` | obsoleta (siempre 1D) | migrar a `np.isin`, que conserva el shape |
| Confundir el orden de los argumentos | `isin(element, test)`: el primero es lo que se comprueba | recordar "¿está `element` en `test`?" |
| `assume_unique=True` con duplicados | resultado incorrecto | dejar `assume_unique=False` |

## Notas relacionadas

- [[concepto_indexing]] — la máscara booleana se usa para seleccionar/asignar con shape
- [[np.where]] — elegir entre dos valores según la máscara de `isin`
- [[Librerias/Numpy/np/conjuntos/index|operaciones de conjunto]] — la nota madre
- [[np.intersect1d]] · [[np.setdiff1d]] · [[np.unique]]
