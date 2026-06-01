---
title: np.where — Selección condicional elemento a elemento
aliases:
  - where
  - np.where
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing
  - concepto_broadcasting

draft: false
---

# np.where — Selección condicional elemento a elemento

## Firma de la función

```python
np.where(condition, [x, y, ]/) -> ndarray | tuple[ndarray, ...]
```

Tiene **dos modos** según el número de argumentos.

## Valor de retorno

| Modo | Llamada | Retorno |
|------|---------|---------|
| Selección | `np.where(cond, x, y)` | array: `x` donde `cond` es True, `y` donde es False |
| Índices | `np.where(cond)` | tupla de arrays con las **posiciones** donde `cond` es True |

```python
import numpy as np
arr = np.array([1, -2, 3, -4])

# Modo selección: reemplazo condicional
np.where(arr > 0, arr, 0)     # [1, 0, 3, 0]

# Modo índices: dónde se cumple
np.where(arr > 0)             # (array([0, 2]),)
```

## Modo 1: selección `where(cond, x, y)`

Construye un array tomando de `x` o de `y` según la condición, elemento a elemento. `x`, `y` y `cond` se alinean por [[concepto_broadcasting|broadcasting]].

```python
a = np.array([10, 20, 30, 40])
np.where(a > 25, a, -1)       # [-1, -1, 30, 40]
np.where(a > 25, a * 2, 0)    # [0, 0, 60, 80]

# x e y pueden ser escalares o arrays
np.where(a > 25, 'alto', 'bajo')   # ['bajo','bajo','alto','alto']
```

### Anidado (varias condiciones)

```python
np.where(a < 15, 'A',
  np.where(a < 35, 'B', 'C'))   # para >2 ramas, ver np.select
```

## Modo 2: índices `where(cond)`

Equivale a [[np.nonzero]] aplicado a la máscara booleana. Devuelve una **tupla** (un array de índices por dimensión).

```python
M = np.array([[0, 5], [3, 0]])
filas, cols = np.where(M > 0)
# filas = [0, 1], cols = [1, 0]  → posiciones (0,1) y (1,0)
M[filas, cols]                 # [5, 3]
```

## Parámetros en detalle

### `condition` — array booleano

Máscara (o expresión que la produzca). Define qué posiciones toman `x` y cuáles `y`.

### `x`, `y` — valores alternativos

Solo en modo selección. Deben ser broadcastables con `condition`. Ambos o ninguno.

## Casos de uso

### Reemplazar negativos por cero (ReLU)

```python
np.where(x < 0, 0, x)
```

### Evitar división por cero

```python
np.where(b != 0, a / b, 0)   # ⚠️ ojo: a/b se evalúa completo (ver limitaciones)
```

### Localizar elementos que cumplen una condición

```python
indices = np.where(temperaturas > 100)[0]
```

## Buenas prácticas

1. Para **más de dos ramas**, usa [[np.select]] (más legible que `where` anidado).
2. En modo índices, `np.where(cond)` ≡ `np.nonzero(cond)`; usa el que comunique mejor la intención.
3. Si solo necesitas filtrar valores (no posiciones), la máscara booleana directa `arr[arr > 0]` es más simple (ver [[concepto_indexing]]).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: either both or neither of x and y` | se pasó solo `x` | pasar `x` e `y`, o ninguno |
| Warning de división por cero | `a/b` se evalúa **entero** antes de seleccionar | usar máscara o `np.divide(..., where=)` |
| Esperar array y recibir tupla | modo índices devuelve tupla | indexar `[0]` para 1D |

## Limitaciones

- En `where(cond, f(a), g(a))`, **ambas** ramas se evalúan por completo antes de seleccionar: no hay cortocircuito (cuidado con operaciones inválidas o costosas).
- Para muchas condiciones, [[np.select]] escala mejor.

## Notas relacionadas

- [[concepto_indexing]]
- [[concepto_broadcasting]]
- [[np.nonzero]]
- [[np.select]]
- [[np.clip]]
- [[np.take]]
