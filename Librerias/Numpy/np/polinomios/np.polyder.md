---
title: np.polyder — Derivada de un polinomio
aliases:
  - polyder
  - np.polyder
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

# np.polyder — Derivada de un polinomio

## Firma de la función

```python
np.polyder(p, m=1) -> ndarray | poly1d
```

## Valor de retorno

Devuelve los coeficientes de la **derivada** del polinomio `p`. Si `p` es un [[np.poly1d]], devuelve otro `poly1d`.

```python
import numpy as np
# x³ + 2x² + 3x + 4  →  3x² + 4x + 3
np.polyder([1, 2, 3, 4])     # array([3, 4, 3])
```

## Parámetros en detalle

### `p` — polinomio

Coeficientes (mayor a menor) o un objeto [[np.poly1d]].

### `m` — orden de derivación

Número de veces a derivar (`m=2` → segunda derivada).

```python
np.polyder([1, 0, 0, 0], 2)   # 6x  (2ª derivada de x³)
```

## Casos de uso

### Velocidad/aceleración desde posición polinómica

```python
pos = np.poly1d(np.polyfit(t, x, 3))
vel = np.polyder(pos)        # poly1d derivado
acc = np.polyder(pos, 2)
```

### Encontrar extremos (derivada = 0)

```python
criticos = np.roots(np.polyder(p))
```

## Buenas prácticas

1. Equivale al método `p.deriv()` de [[np.poly1d]].
2. Combínalo con [[np.roots]] para hallar máximos/mínimos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Orden de coeficientes invertido | mayor→menor grado | respetar la convención |

## Limitaciones

- API antigua (ver `np.polynomial.Polynomial.deriv`).

## Notas relacionadas

- [[concepto_shape]]
- [[np.polyint]]
- [[np.poly1d]]
- [[np.roots]]
