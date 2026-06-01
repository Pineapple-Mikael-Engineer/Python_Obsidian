---
title: np.roots — Raíces de un polinomio
aliases:
  - roots
  - np.roots
  - raices
tags:
  - numpy
  - api/funcion
  - polinomios

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.roots — Raíces de un polinomio

## Firma de la función

```python
np.roots(p) -> ndarray
```

## Valor de retorno

Devuelve las **raíces** (valores donde el polinomio vale 0) de `p`. Para un polinomio de grado `n` devuelve `n` raíces, que pueden ser **complejas**.

```python
import numpy as np
# x² - 5x + 6 = (x-2)(x-3)
np.roots([1, -5, 6])      # array([3., 2.])

# x² + 1 → raíces complejas
np.roots([1, 0, 1])       # array([0.+1.j, 0.-1.j])
```

## Parámetros en detalle

### `p` — coeficientes

Array (mayor a menor grado) o [[np.poly1d]].

## Casos de uso

### Resolver una ecuación polinómica

```python
# 2x³ - 3x² - 11x + 6 = 0
np.roots([2, -3, -11, 6])
```

### Encontrar puntos críticos

```python
criticos = np.roots(np.polyder(p))   # donde la derivada es 0
```

## Buenas prácticas

1. El resultado puede ser **complejo**: revisa `np.isreal` si solo te interesan reales.
2. Equivale al atributo `p.r` de [[np.poly1d]].
3. Para raíces de una función no polinómica, usa `scipy.optimize`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Raíces complejas inesperadas | el polinomio no tiene reales | filtrar con `np.isreal` |
| Pequeña parte imaginaria residual | error numérico | tomar `.real` si es despreciable |

## Limitaciones

- Solo polinomios; sensible numéricamente con grados altos o raíces múltiples.

## Notas relacionadas

- [[concepto_dtype]]
- [[np.poly1d]]
- [[np.polyfit]]
- [[np.polyder]]
