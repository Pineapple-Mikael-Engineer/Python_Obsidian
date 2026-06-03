---
title: import de submodulos — por que `import scipy` no basta
aliases:
  - import scipy
  - submodulos scipy
  - scipy no autoimporta
tags:
  - scipy
  - concepto
  - fundamentos
lib: scipy
tipo: concepto
requiere:
  - concepto_relacion_numpy
draft: false
---

# import de submodulos — por que `import scipy` no basta

## Definicion fundamental

SciPy esta organizado en **submodulos independientes** (`scipy.optimize`, `scipy.integrate`, `scipy.stats`…) que **no se cargan automaticamente** al hacer `import scipy`. Cada submodulo debe importarse de forma **explicita**. Es la diferencia practica mas frecuente frente a NumPy, donde `import numpy as np` deja todo accesible.

```python
import scipy
scipy.optimize.minimize(...)   # ❌ AttributeError: module 'scipy' has no attribute 'optimize'

from scipy import optimize
optimize.minimize(...)         # ✅
```

## Por que existe

SciPy es grande y varios submodulos arrastran dependencias pesadas (LAPACK, compilados Fortran/C). Importar **todo** en cada `import scipy` seria lento y consumiria memoria que muchas veces no se usa. La carga diferida por submodulo mantiene el arranque barato: pagas solo por lo que importas. Es una consecuencia directa de que SciPy sea la [[concepto_relacion_numpy|capa de algoritmos sobre NumPy]].

## La regla central: tres formas validas

| Forma | Sintaxis | Uso de la API | Cuando |
|-------|----------|---------------|--------|
| Submodulo como nombre | `from scipy import optimize` | `optimize.minimize(...)` | **preferida**, legible |
| Funcion directa | `from scipy.optimize import minimize` | `minimize(...)` | pocas funciones concretas |
| Ruta completa | `import scipy.optimize` | `scipy.optimize.minimize(...)` | scripts explicitos |

La forma que **no** funciona:

```python
import scipy                  # solo carga el paquete raiz
scipy.stats.norm.pdf(0)       # ❌ AttributeError
```

## Por que el `import scipy as sp` suelto es una trampa

Es habitual ver `import scipy as sp` y luego `sp.optimize…`, que **falla** por lo mismo. Si quieres el alias, importa el submodulo bajo el alias:

```python
import scipy.optimize as opt
opt.minimize(...)             # ✅
```

## Casos que fallan

| Sintoma | Causa | Solucion |
|---------|-------|----------|
| `AttributeError: module 'scipy' has no attribute 'optimize'` | Solo importaste `scipy` | `from scipy import optimize` |
| `sp.stats` falla con `import scipy as sp` | El alias no autoimporta submodulos | `import scipy.stats as stats` |
| El autocompletado no muestra el submodulo | Aun no se ha importado en la sesion | Importalo una vez y reintenta |
| Import lento la primera vez | Carga de LAPACK/compilados del submodulo | Normal; ocurre una sola vez por proceso |

## Buenas practicas

1. Importa **submodulos**, no funciones sueltas, cuando uses varias del mismo (`from scipy import optimize`).
2. Agrupa los imports de SciPy arriba del archivo; no dentro de bucles ni funciones calientes.
3. Para notebooks de exploracion, `from scipy import optimize, integrate, stats` en una linea evita sorpresas.

## Notas relacionadas

- [[concepto_relacion_numpy]]
- [[concepto_objetos_resultado]]
