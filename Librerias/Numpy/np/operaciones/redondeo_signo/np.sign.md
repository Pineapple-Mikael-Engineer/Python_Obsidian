---
title: np.sign — Signo de cada elemento (ufunc)
aliases:
  - sign
  - np.sign
  - signo
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

# np.sign — Signo de cada elemento (ufunc)

## Firma de la función

```python
np.sign(x, /, out=None, *, where=True, dtype=None) -> ndarray
```

## Valor de retorno

Devuelve el **signo** elemento a elemento: `-1`, `0` o `+1`.

| `x` | Resultado |
|-----|-----------|
| `> 0` | `1` |
| `== 0` | `0` |
| `< 0` | `-1` |

```python
import numpy as np
np.sign([-5, 0, 3, -0.2])   # array([-1.,  0.,  1., -1.])
```

## Parámetros en detalle

`x` cualquiera; `out`, `where`, `dtype` como toda ufunc (ver [[np.add]]). Para `nan`, devuelve `nan`.

## Casos de uso

### Dirección de un cambio

```python
direccion = np.sign(np.diff(serie))   # +1 sube, -1 baja, 0 igual
```

### Reconstruir valor desde magnitud y signo

```python
resultado = np.sign(x) * np.abs(x)
```

## Buenas prácticas

1. Combínala con [[np.abs]] para separar magnitud y signo.
2. El `0` produce signo `0` (no `+1`).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar ±1 y obtener 0 | el valor era exactamente 0 | tratar el 0 aparte si molesta |
| `nan` en el resultado | había NaN | filtrar antes |

## Limitaciones

- Tres valores posibles; no indica magnitud.

## Notas relacionadas

- [[concepto_ufuncs]]
- [[np.abs]]
- [[np.ceil]]
