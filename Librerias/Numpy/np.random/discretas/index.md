---
title: discretas — distribuciones de valores enteros o categorias
tags:
  - numpy
  - indice
draft: false
---

# discretas — distribuciones de valores enteros o categorias

Distribuciones para variables aleatorias que toman valores enteros o de un conjunto finito. Fundamentales para simulacion de procesos de conteo, muestreo aleatorio y modelos estadisticos discretos. `randint` y `choice` son las de uso mas frecuente; `binomial` y `poisson` aparecen en modelado estadistico.

## Funciones

| Funcion | Descripcion |
|---------|-------------|
| [[np.random.randint]] | Enteros uniformes en `[low, high)`; la mas usada para indices y splits |
| [[np.random.random_integers]] | DEPRECADA — usar `randint` |
| [[np.random.binomial]] | Numero de exitos en `n` ensayos Bernoulli con probabilidad `p` |
| [[np.random.poisson]] | Numero de eventos en un intervalo con tasa media `lam` |
| [[np.random.choice]] | Muestreo aleatorio de un array o rango, con o sin reposicion |

`binomial` modela: cuantas caras en n lanzamientos de moneda, cuantos clientes que compran en n visitas. `poisson` modela: llamadas por hora, fotones detectados, fallos por dia — para `lam` grande, la Poisson se aproxima a la normal. `choice` es la mas versatil: acepta arrays de cualquier tipo, soporta probabilidades no uniformes y muestreo sin reposicion, lo que la hace la herramienta principal para bootstrapping.

## Ejemplos rapidos

```python
import numpy as np
np.random.seed(0)

# Enteros uniformes en [0, 10)
np.random.randint(0, 10, size=5)           # array([5, 0, 3, 3, 7])

# Binomial: caras en 10 lanzamientos (p=0.5)
np.random.binomial(n=10, p=0.5, size=5)   # array([4, 6, 5, 3, 5])

# Poisson: llamadas por minuto (tasa=3)
np.random.poisson(lam=3, size=5)           # array([3, 0, 3, 4, 2])

# Choice sin reposicion
np.random.choice(['a', 'b', 'c'], size=2, replace=False)

# Choice con probabilidades no uniformes
np.random.choice([1, 2, 3], size=4, p=[0.1, 0.6, 0.3])
```

## Nota sobre random_integers

`np.random.random_integers` esta deprecada desde NumPy 1.11. Su rango era cerrado `[low, high]`; el equivalente moderno es `randint(low, high+1)` (rango semiabierto `[low, high)`).
