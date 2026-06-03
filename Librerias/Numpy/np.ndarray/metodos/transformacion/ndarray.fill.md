---
title: ndarray.fill — Rellenar todo el array con un escalar (in-place)
aliases:
  - fill
  - ndarray.fill
tags:
  - numpy
  - api/metodo
  - transformaciones
lib: numpy
obj: ndarray
tipo: metodo
retorna: None
inplace: true
draft: false
---

# ndarray.fill — Rellenar todo el array con un escalar (in-place)

## Firma del método

```python
ndarray.fill(value) -> None
```

## Valor de retorno

Retorna `None`. **Modifica `self` in-place**: escribe el escalar `value` en **todos** los elementos, conservando shape y dtype. El valor se castea al dtype del array.

| Entrada (`self`) | Llamada | Efecto |
|------------------|---------|--------|
| `[0, 0, 0]` | `arr.fill(7)` | `self` → `[7, 7, 7]` |
| shape `(2, 2)` | `arr.fill(1)` | `self` → `[[1,1],[1,1]]` |
| float64 | `arr.fill(2.9)` int array | castea al dtype: `[2, 2, ...]` |

```python
import numpy as np
a = np.empty(4)
a.fill(3.5)
a            # array([3.5, 3.5, 3.5, 3.5])
a.fill(7)
a            # array([7., 7., 7., 7.])  → 7 se castea a float64
```

## Equivalencia

No existe `np.fill`: vive solo como **método**. La alternativa idiomática con asignación por slice es `arr[:] = value`, y para crear ya relleno está `np.full`.

```python
arr.fill(9)        # in-place, solo método
arr[:] = 9         # equivalente con slice (también in-place)
np.full(arr.shape, 9)   # crea un array nuevo lleno de 9
```

| Forma | Crea array nuevo | In-place |
|-------|------------------|----------|
| `arr.fill(v)` | no | sí |
| `arr[:] = v` | no | sí |
| `np.full(shape, v)` | sí | no |

## Parámetros en detalle

### `value` — escalar a propagar

Debe ser un **escalar** (no un array). Se castea al dtype de `self`; si no encaja, puede truncar o fallar.

```python
a = np.zeros(3, dtype=np.int32)
a.fill(2.9)   # array([2, 2, 2])  → trunca al castear a int
```

## Casos de uso

### Reinicializar un buffer reutilizado

```python
buf = np.empty(1000)
for _ in range(3):
    buf.fill(0.0)    # limpia sin reasignar la variable
    # ... usar buf
```

### Inicializar un array recién creado con empty

```python
mask = np.empty((4, 4), dtype=bool)
mask.fill(True)      # más explícito que crear y reasignar
```

## Buenas prácticas

1. Usa `fill` para **reutilizar** un buffer existente sin asignar memoria nueva (a diferencia de `np.full`).
2. Recuerda que el valor se **castea** al dtype del array: un float en un array int trunca.
3. `value` debe ser escalar; para patrones por posición usa asignación con slice o [[ndarray.put]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Pasar un array como `value` | `fill` solo acepta escalar | usar `arr[:] = otro_array` |
| Esperar un retorno | `fill` devuelve `None` | leer `self` tras la llamada |
| Pérdida de decimales | castea float→dtype int | usar dtype float o `np.round` |

## Notas relacionadas

- [[ndarray.put]]
- [[concepto_dtype]]
- [[np.full]]
