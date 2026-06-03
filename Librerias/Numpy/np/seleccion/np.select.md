---
title: np.select — Selección por múltiples condiciones
aliases:
  - select
  - np.select
tags:
  - numpy
  - api/funcion
  - indexado

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
  - concepto_broadcasting

draft: false
---

# np.select — Selección por múltiples condiciones

## Firma de la función

```python
np.select(
    condlist,
    choicelist,
    default=0
) -> ndarray
```

## Valor de retorno

Construye un array eligiendo, para cada posición, el valor de la **primera condición que se cumple**. Generaliza [[np.where]] (que solo maneja 2 ramas) a N ramas.

| `condlist` | `choicelist` | Resultado |
|------------|--------------|-----------|
| `[a<0, a<10]` | `['neg', 'bajo']` | primera condición True gana |

```python
import numpy as np
a = np.array([-5, 3, 50, 200])

condiciones = [a < 0, a < 100, a >= 100]
opciones    = ['negativo', 'normal', 'alto']
np.select(condiciones, opciones, default='?')
# array(['negativo', 'normal', 'normal', 'alto'])
```

## Parámetros en detalle

### `condlist` — lista de condiciones

Lista de arrays booleanos del mismo shape. Se evalúan **en orden**: gana la primera True.

### `choicelist` — lista de valores

Misma longitud que `condlist`. El valor (escalar o array) que se toma cuando su condición correspondiente es la primera en cumplirse.

### `default` — valor por defecto

Se usa donde **ninguna** condición se cumple (por defecto `0`).

## select vs where vs choose

| Función | Selección por |
|---------|---------------|
| [[np.where]] | 1 condición (2 ramas) |
| `np.select` | N condiciones (orden de prioridad) |
| [[np.choose]] | un array de índices enteros |

## Casos de uso

### Categorizar en rangos (binning)

```python
notas = np.array([45, 70, 85, 95])
cond = [notas < 60, notas < 80, notas < 90, notas >= 90]
cat  = ['F', 'C', 'B', 'A']
np.select(cond, cat)   # ['F', 'C', 'B', 'A']
```

### Función definida a trozos

```python
y = np.select([x < 0, x < 1], [0, x], default=1)   # rampa
```

## Buenas prácticas

1. Sustituye `where` anidados por `select`: mucho más legible con ≥3 ramas.
2. Ordena las condiciones por **prioridad**: la primera True gana.
3. Define `default` explícito para cubrir el caso "ninguna condición".

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `list of cases must be same length as list of conditions` | `condlist` y `choicelist` distintos | igualar longitudes |
| Solapamientos inesperados | varias condiciones True | recordar que gana la **primera** |
| `default=0` no encaja con dtype texto | tipo incompatible | pasar `default` del tipo correcto |

## Limitaciones

- Todas las condiciones se evalúan (sin cortocircuito).
- `condlist` y `choicelist` deben tener la misma longitud.

## Notas relacionadas

- [[concepto_indexing]]
- [[np.where]]
- [[np.choose]]
- [[np.clip]]
