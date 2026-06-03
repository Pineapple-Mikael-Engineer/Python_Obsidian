---
title: np.mod — Resto de la división (módulo, ufunc)
aliases:
  - mod
  - np.mod
  - remainder
  - modulo
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs

draft: false
---

# np.mod — Resto de la división (módulo, ufunc)

## Firma de la función

```python
np.mod(x1, x2, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve el **resto** de `x1 / x2` elemento a elemento. Es la [[concepto_ufuncs|ufunc]] del operador `%`. El signo del resultado sigue al del **divisor** (`x2`).

| `x1` | `x2` | Resultado |
|------|------|-----------|
| `[5, 6, 7]` | `3` | `[2, 0, 1]` |
| `-7` | `3` | `2` (signo del divisor) |
| `7` | `-3` | `-2` |

```python
import numpy as np
np.mod([5, 6, 7, 8], 3)   # array([2, 0, 1, 2])
```

## mod vs fmod (signo)

| Función | Signo del resultado |
|---------|---------------------|
| `np.mod` (`%`) | sigue al **divisor** |
| `np.fmod` | sigue al **dividendo** (estilo C) |

```python
np.mod(-7, 3)    #  2
np.fmod(-7, 3)   # -1
```

## Parámetros en detalle

Idénticos a [[np.add]]: `out`, `where`, `dtype`.

## Casos de uso

### Detectar pares / múltiplos

```python
pares = np.mod(arr, 2) == 0
```

### Envolver índices en un rango (wrap-around)

```python
np.mod(indices, n)   # mantiene en [0, n)
```

### Convertir a coordenadas cíclicas

```python
horas = np.mod(minutos // 60, 24)
```

## Buenas prácticas

1. Recuerda que el signo sigue al **divisor** (usa `np.fmod` para estilo C).
2. Útil para periodicidad, paridad y wrap-around de índices.
3. División por 0 da `nan`/`0` con warning; enmascara con `where`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Signo inesperado con negativos | sigue al divisor | usar `np.fmod` si quieres signo del dividendo |
| `RuntimeWarning` | divisor 0 | `where=x2 != 0` |

## Limitaciones

- Comportamiento del signo distinto a C (usar `fmod` si importa).

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.divide]]
- [[np.add]]
