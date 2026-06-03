---
title: ndarray.nonzero — Índices de los elementos distintos de cero
aliases:
  - nonzero
  - ndarray.nonzero
tags:
  - numpy
  - api/metodo
  - indexado
lib: numpy
obj: ndarray
tipo: metodo
retorna: tuple
inplace: false
draft: false
---

# ndarray.nonzero — Índices de los elementos distintos de cero

## Firma del método

```python
ndarray.nonzero() -> tuple[ndarray, ...]
```

## Valor de retorno

| Entrada (`self`) | Retorno |
|------------------|---------|
| `[0, 5, 0, 8]` | `(array([1, 3]),)` |
| `[[0,1],[2,0]]` | `(array([0, 1]), array([0, 1]))` |
| `[False,True,True]` | `(array([1, 2]),)` |

Devuelve una **tupla con un array de índices por cada dimensión** de `self`. Para un array N-D, la tupla tiene N arrays; agrupados por posición, dan las coordenadas de cada elemento no nulo (en orden C). `self[self.nonzero()]` recupera siempre esos valores no nulos.

```python
import numpy as np
a = np.array([0, 5, 0, 8])
a.nonzero()        # (array([1, 3]),)
a[a.nonzero()]     # array([5, 8])
```

## Equivalencia con np.nonzero

`a.nonzero()` es la forma "bound" de [[np.nonzero]]: `np.nonzero(a)`. Resultado idéntico. Es la base de la indexación booleana del [[concepto_indexing|fancy indexing]]: aplicar una máscara `m` equivale a indexar con `m.nonzero()`. Para condiciones, lo habitual es `(arr > 0).nonzero()`.

## Parámetros en detalle

No recibe parámetros. El criterio de "no nulo" abarca:

| Tipo | Se considera nulo |
|------|-------------------|
| numérico | `0`, `0.0` |
| booleano | `False` |
| complejo | `0+0j` |

`NaN` y `inf` **no** son nulos: aparecen en el resultado.

## Casos de uso

### Localizar elementos que cumplen una condición

```python
arr = np.array([3, -1, 0, 7, -2])
(arr > 0).nonzero()   # (array([0, 3]),)  → posiciones de positivos
```

### Coordenadas (fila, columna) en 2D

```python
M = np.array([[0, 2],
              [0, 0],
              [4, 0]])
filas, cols = M.nonzero()
list(zip(filas, cols))   # [(0, 1), (2, 0)]
```

### Reconstruir los valores no nulos

```python
M[M.nonzero()]   # array([2, 4])
```

## Buenas prácticas

1. Para obtener **valores** que cumplen, indexa con la máscara (`arr[arr > 0]`); usa `nonzero` cuando necesites las **posiciones**.
2. Desempaqueta la tupla por eje: `filas, cols = M.nonzero()`.
3. Para condiciones con elección de valores (if/else vectorizado) usa `np.where`; `nonzero` solo da posiciones.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Tratar el retorno como un array plano | `nonzero` devuelve una **tupla** de arrays | desempaquetar por eje |
| Sorpresa con `NaN`/`inf` presentes | no son cero, sí cuentan | filtrar con `np.isnan`/`np.isfinite` antes |
| Esperar valores en vez de índices | devuelve posiciones | indexar `self[self.nonzero()]` |

## Notas relacionadas

- [[np.nonzero]]
- [[concepto_indexing]]
- [[ndarray.take]]
- [[np.where]]
