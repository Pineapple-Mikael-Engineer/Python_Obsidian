---
title: np.setdiff1d — diferencia, en el primero pero no en el segundo
aliases:
  - setdiff1d
  - np.setdiff1d
  - diferencia
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

# np.setdiff1d — diferencia, en el primero pero no en el segundo

`np.setdiff1d` devuelve los valores de `ar1` que **no** están en `ar2`: la diferencia de conjuntos
$A \setminus B$. Como el resto de operaciones binarias, **aplana** ambas entradas a 1D y devuelve el
resultado **único y ordenado**. Es la versión vectorizada de `set(a) - set(b)`. **No es simétrica**:
el orden de los argumentos importa.

## La idea

La operación es la **diferencia**: un valor sobrevive si está en `ar1` y **no** en `ar2`.

$$ A \setminus B \;=\; \{\, x : x \in A \ \wedge\ x \notin B \,\} $$

La salida es **siempre 1D**, ordenada y sin repetidos. No hay caso N-D (ambas entradas se aplanan).
A diferencia de la unión o la intersección, **no es simétrica**: $A \setminus B \neq B \setminus A$.

```python
import numpy as np
np.setdiff1d([1, 2, 3, 4], [3, 4, 5])   # array([1, 2])  → A − B
np.setdiff1d([3, 4, 5], [1, 2, 3, 4])   # array([5])     → B − A, distinto
```

## Firma

```python
np.setdiff1d(
    ar1,                    # array_like: conjunto base (de aquí salen los valores)
    ar2,                    # array_like: valores a excluir
    assume_unique=False,    # bool: True salta la deduplicación interna (más rápido)
) -> ndarray
```

## Los parámetros en detalle

### `ar1` — el conjunto base
`array_like`. Se **aplana a 1D**. La salida es un subconjunto de sus valores únicos: los que
sobreviven al filtrado.

### `ar2` — los valores a excluir
`array_like`. Se aplana. Cualquier valor de `ar1` que aparezca aquí se elimina del resultado. Los
valores de `ar2` que **no** estén en `ar1` se ignoran (no aportan nada).

### `assume_unique` — saltarse la deduplicación
`bool`. Si garantizas que ninguna entrada tiene duplicados, `True` evita el `unique` interno y
acelera. Con duplicados presentes y `True`, el resultado puede ser incorrecto.

## El caso N-D

No aplica: `setdiff1d` **aplana** ambas entradas y devuelve siempre un vector 1D ordenado. Si lo que
quieres es una **máscara** que diga, manteniendo el shape, qué elementos de `ar1` no están en `ar2`,
usa `~np.isin(ar1, ar2)` ([[np.isin]] conserva la forma del primer argumento).

## Casos de uso

### Elementos exclusivos del primer conjunto
```python
ids_train = np.array([1, 2, 3, 4])
ids_test  = np.array([3, 4])
solo_en_train = np.setdiff1d(ids_train, ids_test)   # [1, 2]
```

### Filtrar valores prohibidos (lista negra)
```python
candidatos  = np.array([10, 20, 30, 40])
lista_negra = np.array([20, 40])
validos = np.setdiff1d(candidatos, lista_negra)   # [10, 30]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado vacío inesperado | argumentos invertidos (`A` y `B` al revés) | revisar cuál es el conjunto base |
| Esperar simetría | `setdiff1d` es **direccional** | para ambos sentidos a la vez usar [[np.setxor1d]] |
| Resultados raros con `assume_unique=True` | había duplicados | dejar `assume_unique=False` |

## Notas relacionadas

- [[concepto_indexing]] — `~np.isin(...)` da la máscara equivalente con shape
- [[np.setxor1d]] — la versión **simétrica** (diferencia en ambos sentidos)
- [[Librerias/Numpy/np/conjuntos/index|operaciones de conjunto]] — la nota madre
- [[np.intersect1d]] · [[np.union1d]] · [[np.isin]]
