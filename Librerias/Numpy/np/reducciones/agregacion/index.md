---
title: np/reducciones/agregacion — suma y producto
tags:
  - numpy
  - indice
draft: false
---

# np/reducciones/agregacion — suma y producto

Las 4 funciones de agregacion realizan sumas y productos sobre arrays. La distincion central es si **reducen** la dimension o la **conservan**:

- `sum` / `prod` reducen: colapsan el eje indicado y devuelven un array de menor rango (o un escalar si `axis=None`).
- `cumsum` / `cumprod` acumulan: recorren el array posicion a posicion guardando el resultado parcial; la salida tiene la **misma forma** que la entrada.

```python
import numpy as np
a = np.array([1, 2, 3, 4])

np.sum(a)      # 10             — escalar
np.cumsum(a)   # [1, 3, 6, 10] — mismo shape, suma de prefijos

np.prod(a)     # 24
np.cumprod(a)  # [1, 2, 6, 24]
```

Con arrays 2-D el parametro `axis` determina la orientacion del colapso o la acumulacion:

```python
M = np.array([[1, 2],
              [3, 4]])

np.sum(M, axis=0)     # [4, 6]      — suma por columna (colapsa filas)
np.cumsum(M, axis=1)  # [[1,3],[3,7]] — acumulado a lo largo de cada fila
```

## Notas de esta subcarpeta

| Funcion | Que hace |
|---|---|
| [[np.sum]] | Suma de elementos a lo largo de un eje. El workhorse de las reducciones: soporta `dtype=`, `keepdims=`, `initial=`. Controlar el `dtype` de acumulacion evita overflow silencioso en sumas de enteros pequeños. |
| [[np.prod]] | Producto de elementos a lo largo de un eje. El producto de muchos valores mayores que 1 crece exponencialmente; para productos de probabilidades usar `np.sum(np.log(p))` en su lugar. |
| [[np.cumsum]] | Suma acumulativa: el elemento i del resultado es la suma de los elementos 0 a i del input. Util para sumas de prefijos y distribuciones de probabilidad acumuladas. |
| [[np.cumprod]] | Producto acumulativo: el elemento i es el producto de los elementos 0 a i. Misma advertencia que `prod` respecto al overflow rapido. |
