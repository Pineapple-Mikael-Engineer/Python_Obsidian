---
title: np.random — generacion de numeros aleatorios (API legacy)
tags:
  - numpy
  - indice
draft: false
---

# np.random — generacion de numeros aleatorios (API legacy)

`numpy.random` es el submodulo de generacion de numeros pseudoaleatorios de NumPy. "Pseudoaleatorio" significa que los numeros son deterministas pero tienen las propiedades estadisticas de numeros aleatorios reales: fijando la semilla (`np.random.seed(n)`) se obtiene exactamente la misma secuencia en cualquier maquina y en cualquier momento — esencial para reproducibilidad en ciencia e investigacion.

Este directorio documenta la **API legacy**: la interfaz funcional directa donde se llama `np.random.normal(...)` sin instanciar ningun objeto. Desde NumPy 1.17 existe la API moderna basada en `Generator`: `rng = np.random.default_rng(seed); rng.normal(...)`. La API moderna permite multiples generadores independientes, no comparte estado global y es mas rapida. Para codigo nuevo, preferir `default_rng`. La API legacy sigue siendo ampliamente usada y es la que aparece en la mayoria de tutoriales y libros.

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
rng = np.random.default_rng(seed=42)   # Generator independiente, sin estado global
rng.normal(0, 1, size=(3, 3))
```

Ventaja clave sobre la API legacy: cada `rng` encapsula su propio estado — multiples generadores pueden coexistir sin interferirse, y ninguna libreria externa puede perturbar la secuencia.
