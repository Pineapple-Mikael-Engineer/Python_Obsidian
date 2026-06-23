---
title: np.setxor1d — diferencia simétrica, en uno u otro pero no en ambos
aliases:
  - setxor1d
  - np.setxor1d
  - diferencia simétrica
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

# np.setxor1d — diferencia simétrica, en uno u otro pero no en ambos

`np.setxor1d` devuelve los valores que están en `ar1` **o** en `ar2`, pero **no en ambos**: la
diferencia simétrica de conjuntos $A \triangle B$. Como el resto de operaciones binarias, **aplana**
las dos entradas a 1D y devuelve el resultado **único y ordenado**. Es la versión vectorizada de
`set(a) ^ set(b)`. A diferencia de [[np.setdiff1d]], **sí es simétrica**.

## La idea

La operación es la **diferencia simétrica**: un valor sobrevive si está en exactamente **uno** de
los dos arrays. Equivale a la unión menos la intersección.

$$ A \triangle B \;=\; (A \cup B) \setminus (A \cap B) \;=\; \{\, x : x \in A \oplus x \in B \,\} $$

La salida es **siempre 1D**, ordenada y sin repetidos. No hay caso N-D (ambas entradas se aplanan).
Es **simétrica**: el orden de los argumentos no cambia el resultado.

```python
import numpy as np
np.setxor1d([1, 2, 3, 4], [3, 4, 5, 6])   # array([1, 2, 5, 6])
# están en uno solo: 1,2 (solo en A) y 5,6 (solo en B); 3,4 caen porque están en ambos
```

## Firma

```python
np.setxor1d(
    ar1,                    # array_like: primer array (se aplana)
    ar2,                    # array_like: segundo array (se aplana)
    assume_unique=False,    # bool: True salta la deduplicación interna (más rápido)
) -> ndarray
```

## Los parámetros en detalle

### `ar1`, `ar2` — los dos arrays
`array_like`. Se **aplanan a 1D** y se deduplican. El rol de ambos es intercambiable: la operación
es simétrica.

### `assume_unique` — saltarse la deduplicación
`bool`. Si garantizas que ninguna entrada tiene duplicados, `True` evita el `unique` interno y
acelera. Con duplicados presentes y `True`, el resultado puede ser incorrecto.

## El caso N-D

No aplica: `setxor1d` **aplana** ambas entradas y devuelve siempre un vector 1D ordenado. La forma
original de las entradas se pierde. Se puede expresar a mano combinando las otras operaciones:

```python
A, B = np.array([1, 2, 3, 4]), np.array([3, 4, 5, 6])
np.setdiff1d(np.union1d(A, B), np.intersect1d(A, B))   # = np.setxor1d(A, B)
```

## Casos de uso

### Detectar elementos que cambiaron entre dos estados
```python
antes   = np.array([1, 2, 3])
despues = np.array([2, 3, 4])
cambios = np.setxor1d(antes, despues)   # [1, 4]  → el 1 se fue, el 4 llegó
```

### Comparar dos conjuntos en ambos sentidos a la vez
```python
diferencias = np.setxor1d(config_a, config_b)   # todo lo que no coincide
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar solo lo nuevo | incluye lo que **se fue** y lo que **llegó** | usar [[np.setdiff1d]] para un solo sentido |
| Esperar conservar el shape | `setxor1d` aplana siempre | la salida es 1D por diseño |
| Resultados raros con `assume_unique=True` | había duplicados | dejar `assume_unique=False` |

## Notas relacionadas

- [[concepto_indexing]] — la salida es un índice ordenado de valores
- [[np.setdiff1d]] — la versión **direccional** (un solo sentido)
- [[Librerias/Numpy/np/conjuntos/index|operaciones de conjunto]] — la nota madre
- [[np.intersect1d]] · [[np.union1d]] · [[np.isin]]
