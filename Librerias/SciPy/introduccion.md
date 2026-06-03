---
title: introduccion — que es SciPy y como navegar este modulo
aliases:
  - introduccion scipy
  - scipy overview
  - mapa de scipy
tags:
  - scipy
  - concepto
  - indice
lib: scipy
tipo: concepto
requiere:
  - concepto_relacion_numpy
draft: false
---

# introduccion — que es SciPy y como navegar este modulo

**SciPy** es la biblioteca de **algoritmos cientificos** de Python construida sobre NumPy. Donde NumPy aporta el `ndarray` y las operaciones vectorizadas elementales, SciPy aporta las rutinas de alto nivel —optimizacion, integracion, algebra lineal, estadistica, procesamiento de señales e imagen, transformadas— que operan sobre ese mismo array. La relacion completa se detalla en [[concepto_relacion_numpy|SciPy extiende NumPy]].

```python
import numpy as np
from scipy import optimize, integrate, stats   # submodulos: import explicito
```

## Antes de tocar cualquier submodulo: 4 ideas que gobiernan todo

Estos conceptos transversales se aplican en casi todas las rutinas; conviene leerlos primero.

| Concepto | Idea clave |
|----------|-----------|
| [[concepto_relacion_numpy \| Relacion NumPy-SciPy]] | el `ndarray` entra y sale de casi todo; `scipy.linalg` es superset de `numpy.linalg` |
| [[concepto_import_submodulos \| Import de submodulos]] | `import scipy` no basta: hay que importar `scipy.optimize`, etc. |
| [[concepto_objetos_resultado \| Objetos resultado]] | muchas rutinas devuelven un Bunch (`OptimizeResult`…); revisa `.success` antes de `.x` |
| [[concepto_callbacks_vectorizados \| Callbacks y vectorizacion]] | pasas una funcion que SciPy llama N veces: vectorizala; cuidado con la firma `f(t,y)` vs `f(y,t)` |

## Mapa de submodulos

| Submodulo | Para que | Entradas tipicas |
|-----------|----------|------------------|
| `scipy.optimize` | minimizar, ajustar curvas, hallar raices | `minimize`, `curve_fit`, `root`, `brentq` |
| `scipy.integrate` | integrales definidas y EDOs | `quad`, `simpson`, `solve_ivp`, `odeint` |
| `scipy.interpolate` | interpolar datos | `CubicSpline`, `griddata`, `RegularGridInterpolator` |
| `scipy.linalg` | algebra lineal (LAPACK) | `solve`, `lu`, `svd`, `eig`, `expm` |
| `scipy.stats` | distribuciones, tests, descriptiva | `norm`, `ttest_ind`, `linregress`, `gaussian_kde` |
| `scipy.signal` | filtrado, convolucion, espectro | `butter`, `filtfilt`, `find_peaks`, `welch` |
| `scipy.ndimage` | imagenes / arrays N-D | `gaussian_filter`, `label`, `binary_erosion` |
| `scipy.special` | funciones especiales | `gamma`, `erf`, `comb`, `jv` |
| `scipy.fft` | transformada de Fourier | `fft`, `rfft`, `fftfreq` |
| `scipy.spatial` | geometria computacional | `KDTree`, `ConvexHull`, `Delaunay` |
| `scipy.sparse` | matrices dispersas | `csr_matrix`, `coo_matrix` |
| `scipy.constants` | constantes fisicas (CODATA) | `c`, `G`, `physical_constants` |

> Cada submodulo tiene su propia carpeta con notas API-style (`scipy.<sub>.<funcion>.md`) y clases con su nombre real (`KDTree.md`).

## Como usar este arbol

1. **Empieza por los conceptos transversales** si vienes de cero: dan el modelo mental.
2. **Busca por nombre de API**: los archivos imitan la documentacion oficial (`scipy.optimize.minimize.md`).
3. **Sigue los wikilinks** al final de cada nota (`## Notas relacionadas`) para saltar a la rutina vecina.
4. **Distingue legacy de moderno**: notas como `fsolve`, `interp1d` u `odeint` llevan un aviso y apuntan a su reemplazo recomendado.

## Notas relacionadas

- [[concepto_relacion_numpy]]
- [[concepto_import_submodulos]]
- [[concepto_objetos_resultado]]
- [[concepto_callbacks_vectorizados]]
