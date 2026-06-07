---
title: discretas — distribuciones de valores enteros o categorias
tags:
  - numpy
  - indice
draft: false
---

# discretas — distribuciones de valores enteros o categorias

Funciones para generar muestras discretas: enteros uniformes, conteos de exitos/eventos o muestreo de categorias.

## Funciones

| Funcion | Descripcion |
|---------|-------------|
| [[np.random.randint]] | Enteros uniformes en `[low, high)` |
| [[np.random.random_integers]] | DEPRECADA — usar `randint` |
| [[np.random.binomial]] | Numero de exitos en `n` ensayos con probabilidad `p` |
| [[np.random.poisson]] | Eventos en un intervalo con tasa `lam` |
| [[np.random.choice]] | Muestreo con o sin reposicion de un array o rango |

## Ejemplos rapidos

```python
import numpy as np
np.random.seed(0)

# Enteros uniformes en [0, 10)
np.random.randint(0, 10, size=5)          # array([5, 0, 3, 3, 7])

# Binomial: numero de caras en 10 lanzamientos (p=0.5)
np.random.binomial(n=10, p=0.5, size=5)  # array([4, 6, 5, 3, 5])

# Poisson: llamadas por minuto (tasa=3)
np.random.poisson(lam=3, size=5)          # array([3, 0, 3, 4, 2])

# Choice: muestreo sin reposicion
np.random.choice(['a', 'b', 'c'], size=2, replace=False)

# Choice con probabilidades no uniformes
np.random.choice([1, 2, 3], size=4, p=[0.1, 0.6, 0.3])
```

## Nota sobre random_integers

`np.random.random_integers` esta deprecada desde NumPy 1.11. Su equivalente es `randint(low, high+1)` (el rango de `random_integers` era cerrado `[low, high]`, el de `randint` es semiabierto `[low, high)`).
