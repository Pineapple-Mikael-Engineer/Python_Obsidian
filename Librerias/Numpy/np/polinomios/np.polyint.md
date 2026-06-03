---
title: np.polyint — Integral de un polinomio
aliases:
  - polyint
  - np.polyint
tags:
  - numpy
  - api/funcion
  - polinomios

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o poly1d
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.polyint — Integral de un polinomio

## Firma de la función

```python
np.polyint(p, m=1, k=None) -> ndarray | poly1d
```

## Valor de retorno

Devuelve los coeficientes de la **integral** (antiderivada) del polinomio `p`. Operación inversa de [[np.polyder]]. Si `p` es un [[np.poly1d]], devuelve otro `poly1d`.

```python
import numpy as np
# 3x² + 2x  →  x³ + x² + C
np.polyint([3, 2, 0])     # array([1., 1., 0., 0.])
```

## Parámetros en detalle

### `p` — polinomio

Coeficientes (mayor a menor) o [[np.poly1d]].

### `m` — orden de integración

Número de veces a integrar.

### `k` — constantes de integración

Lista de constantes (una por integración). Por defecto `0`.

```python
np.polyint([2, 0], k=5)    # x² + 5  (constante explícita)
```

## Casos de uso

### Recuperar posición desde velocidad

```python
v = np.poly1d([2, 1])      # velocidad
x = np.polyint(v, k=[x0])  # posición con condición inicial
```

## Buenas prácticas

1. Equivale al método `p.integ()` de [[np.poly1d]].
2. Usa `k` para fijar la constante de integración (condición inicial).

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Constante perdida | no se pasó `k` | indicar `k` para la condición inicial |

## Limitaciones

- API antigua (ver `np.polynomial.Polynomial.integ`).

## Notas relacionadas

- [[concepto_shape]]
- [[np.polyder]]
- [[np.poly1d]]
