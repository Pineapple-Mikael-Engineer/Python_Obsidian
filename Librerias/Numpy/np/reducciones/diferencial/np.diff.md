---
title: np.diff — Diferencias discretas entre elementos
aliases:
  - diff
  - np.diff
  - diferencias
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.diff — Diferencias discretas entre elementos

## Firma de la función

```python
np.diff(
    a,
    n=1,
    axis=-1,
    prepend=<sin valor>,
    append=<sin valor>
) -> ndarray
```

## Valor de retorno

Calcula la diferencia entre elementos consecutivos: `out[i] = a[i+1] - a[i]`. El resultado tiene **un elemento menos** por cada orden de diferencia. Es la operación inversa aproximada de [[np.cumsum]].

| Entrada | `n` | Salida |
|---------|-----|--------|
| `[1, 2, 4, 7]` | `1` | `[1, 2, 3]` |
| `[1, 2, 4, 7]` | `2` | `[1, 1]` (diferencia de la diferencia) |

```python
import numpy as np
np.diff([1, 2, 4, 7, 0])   # array([ 1,  2,  3, -7])
```

## Parámetros en detalle

### `n` — orden de la diferencia

Aplica `diff` recursivamente `n` veces. `n=2` da la segunda diferencia (análoga a la segunda derivada discreta).

### `axis` — eje

Por defecto `-1` (último eje). Ver [[concepto_axis_parametro]].

```python
M = np.array([[1, 3, 6],
              [2, 5, 9]])
np.diff(M, axis=1)   # [[2, 3], [3, 4]]
```

### `prepend` / `append` — conservar longitud

Insertan valores antes/después para que el resultado mantenga el tamaño original.

```python
x = np.array([1, 2, 4, 7])
np.diff(x, prepend=x[0])   # [0, 1, 2, 3]  → misma longitud
```

## Casos de uso

### Velocidad a partir de posiciones

```python
posicion = np.array([0, 5, 12, 20])
velocidad = np.diff(posicion)   # [5, 7, 8]
```

### Detectar cambios / saltos en una serie

```python
cambios = np.where(np.diff(serie) != 0)[0]
```

## Buenas prácticas

1. Recuerda que **acorta** el array; usa `prepend`/`append` si necesitas conservar la longitud.
2. Para una derivada numérica con espaciado real, usa [[np.gradient]] (mantiene la longitud y usa diferencias centradas).
3. `n>1` para diferencias de orden superior.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Desalineación de longitudes | `diff` quita un elemento | usar `prepend`/`append` |
| Eje equivocado | por defecto `axis=-1` | pasar `axis` explícito |
| Se esperaba derivada con escala | `diff` ignora el espaciado | usar [[np.gradient]] |

## Limitaciones

- No considera el espaciado entre puntos (asume paso 1).
- Reduce la longitud en `n`.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[np.gradient]]
- [[np.cumsum]]
- [[np.trapz]]
