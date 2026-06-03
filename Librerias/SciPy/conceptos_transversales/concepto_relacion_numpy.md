---
title: relacion NumPy-SciPy — SciPy es la capa de algoritmos sobre el ndarray
aliases:
  - relacion numpy scipy
  - scipy vs numpy
  - numpy base de scipy
tags:
  - scipy
  - concepto
  - fundamentos
lib: scipy
tipo: concepto
requiere:
  - concepto_ndarray
draft: false
---

# relacion NumPy-SciPy — SciPy es la capa de algoritmos sobre el ndarray

## Definicion fundamental

SciPy **no reemplaza a NumPy: lo extiende**. NumPy aporta la estructura de datos —el `ndarray`— y las operaciones vectorizadas elementales; SciPy aporta los **algoritmos cientificos** (optimizacion, integracion, interpolacion, estadistica, procesamiento de señales) que operan sobre ese mismo `ndarray`.

La regla mental: todo lo que **entra y sale** de una rutina de SciPy es, casi siempre, un [[concepto_ndarray|array de NumPy]]. SciPy es comportamiento; NumPy es el dato.

## Por que existe la division

NumPy busca ser ligero y universal: tipos, forma, broadcasting, ufuncs. Meter en el mismo paquete los solucionadores de EDO, los algoritmos de minimizacion o las 100+ distribuciones estadisticas lo volveria pesado y lento de importar. SciPy es ese segundo piso: depende de NumPy, nunca al reves.

```python
import numpy as np
from scipy import integrate

x = np.linspace(0, np.pi, 100)   # ndarray de NumPy
y = np.sin(x)                    # ufunc de NumPy
area = integrate.simpson(y, x=x) # algoritmo de SciPy sobre el ndarray
# → ~2.0
```

## La regla central: quien hace que

| Necesidad | Vive en | Ejemplo |
|-----------|---------|---------|
| Crear / dar forma / indexar datos | **NumPy** | `np.array`, `reshape`, slicing |
| Operacion elemento a elemento | **NumPy** (ufunc) | `np.sin`, `np.exp`, `+`, `*` |
| Reduccion simple | **NumPy** | `np.sum`, `np.mean`, `np.max` |
| Algoritmo numerico no trivial | **SciPy** | `minimize`, `solve_ivp`, `curve_fit` |
| Modelo estadistico / distribucion | **SciPy** | `stats.norm`, `ttest_ind` |
| Transformada / filtro / señal | **SciPy** | `fft`, `butter`, `find_peaks` |

## El caso `linalg`: el solapamiento mas importante

NumPy y SciPy **ambos** tienen `linalg`, y aqui no son intercambiables:

| | `numpy.linalg` | `scipy.linalg` |
|--|----------------|----------------|
| Backend | BLAS/LAPACK (si esta disponible) | **siempre** BLAS/LAPACK |
| Cobertura | basica (`inv`, `solve`, `eig`, `svd`) | **superset** mas completo |
| Descomposiciones extra | — | `lu`, `schur`, `qz`, `expm`, `cholesky` ampliado |
| Recomendacion | uso casual | **codigo numerico serio** |

Por eso `scipy.linalg.lu` **existe** y `numpy.linalg.lu` no. Para trabajo de ingenieria, prefiere `scipy.linalg`.

```python
import numpy as np
from scipy import linalg

A = np.array([[4.0, 3.0], [6.0, 3.0]])
P, L, U = linalg.lu(A)   # solo en SciPy: factorizacion LU con pivoteo
```

## Casos que confunden

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `scipy.sin` no existe (deprecado/eliminado) | Los alias de NumPy en SciPy se retiraron | Usa `np.sin`, no `scipy.sin` |
| Resultado distinto entre `np.linalg` y `scipy.linalg` | Distinta ruta LAPACK / orden de operaciones | Esperable a nivel de epsilon; fija uno para reproducir |
| `import scipy` y luego `scipy.optimize` falla | Submodulos no se autoimportan | Ver [[concepto_import_submodulos|import de submodulos]] |

## Notas relacionadas

- [[concepto_ndarray]]
- [[concepto_import_submodulos]]
- [[concepto_objetos_resultado]]
