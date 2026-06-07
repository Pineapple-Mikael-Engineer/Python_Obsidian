---
title: np.random — generacion de numeros aleatorios (API legacy)
tags:
  - numpy
  - indice
draft: false
---

# np.random — generacion de numeros aleatorios (API legacy)

`np.random` es la API legacy de NumPy para generacion de numeros aleatorios; se llama directamente como `np.random.funcion()`. Desde NumPy 1.17 existe la API moderna `numpy.random.Generator` (via `np.random.default_rng()`), que es preferible para codigo nuevo porque permite varios generadores independientes. Esta carpeta documenta la API legacy, que sigue siendo muy usada.

Agrupa **28 funciones** en 6 subcarpetas.

## Subcarpetas

| Subcarpeta | Funciones | Descripcion |
|------------|-----------|-------------|
| [[Librerias/Numpy/np.random/semilla_estado/index\|semilla_estado/]] | 3 | Control de semilla y estado del generador global |
| [[Librerias/Numpy/np.random/uniformes/index\|uniformes/]] | 6 | Distribucion uniforme y sus alias |
| [[Librerias/Numpy/np.random/normales/index\|normales/]] | 3 | Distribuciones normales / gaussianas |
| [[Librerias/Numpy/np.random/discretas/index\|discretas/]] | 5 | Distribuciones de valores enteros o categorias |
| [[Librerias/Numpy/np.random/continuas_especiales/index\|continuas_especiales/]] | 9 | Distribuciones continuas mas alla de uniforme y normal |
| [[Librerias/Numpy/np.random/permutaciones/index\|permutaciones/]] | 2 | Mezcla y permutacion de arrays |

## API moderna (recomendada para codigo nuevo)

```python
rng = np.random.default_rng(seed=42)   # Generator independiente
rng.normal(0, 1, size=(3, 3))
```

Ventaja sobre la API legacy: multiples generadores independientes, sin estado global compartido.
