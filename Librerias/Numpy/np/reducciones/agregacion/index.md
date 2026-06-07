---
title: np/reducciones/agregacion — suma y producto
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/agregacion — suma y producto

Las 4 funciones de agregacion realizan sumas y productos sobre arrays. Se dividen en dos grupos segun si reducen la dimension o no:

- `sum` / `prod` — **reducen**: colapsan el eje indicado y devuelven un array de menor rango (o un escalar si `axis=None`).
- `cumsum` / `cumprod` — **acumulan**: recorren el array y van guardando el resultado parcial; la salida tiene **la misma forma** que la entrada.

```python
import numpy as np
a = np.array([1, 2, 3, 4])

np.sum(a)      # 10          — escalar
np.cumsum(a)   # [1, 3, 6, 10] — mismo shape

np.prod(a)     # 24
np.cumprod(a)  # [1, 2, 6, 24]
```

Con `axis=` en arrays 2-D:

```python
M = np.array([[1, 2],
              [3, 4]])

np.sum(M, axis=0)     # [4, 6]    — suma por columna
np.cumsum(M, axis=1)  # [[1,3],[3,7]] — acumulado por fila
```

## Notas de esta subcarpeta

| Funcion | Que hace |
|---|---|
| [[np.sum]] | Suma de elementos a lo largo de un eje |
| [[np.prod]] | Producto de elementos a lo largo de un eje |
| [[np.cumsum]] | Suma acumulativa (sin reducir dimension) |
| [[np.cumprod]] | Producto acumulativo (sin reducir dimension) |
