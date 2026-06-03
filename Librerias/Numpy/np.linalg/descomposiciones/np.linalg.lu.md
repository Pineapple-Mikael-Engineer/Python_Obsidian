---
title: np.linalg.lu — ⚠️ NO existe en NumPy (descomposición LU vive en SciPy)
aliases:
  - lu
  - linalg.lu
  - np.linalg.lu
tags:
  - numpy
  - api/funcion
  - algebra/matricial
  - aviso/no-existe-en-numpy
lib: numpy
mod: np.linalg
tipo: funcion
retorna: "N/A — no existe en NumPy (ver scipy.linalg.lu → tuple (P, L, U))"
inplace: false
draft: false
---

# np.linalg.lu — ⚠️ NO existe en NumPy

> [!warning] Esta función NO existe en NumPy
> `np.linalg.lu` **no está disponible en NumPy**. Llamarla lanza `AttributeError: module 'numpy.linalg' has no attribute 'lu'`. La descomposición LU vive en **SciPy** (`scipy.linalg.lu`, `scipy.linalg.lu_factor`), no en NumPy.

Esta nota se conserva en el vault porque la descomposición LU es un pilar del álgebra lineal numérica y es la pregunta natural junto a [[np.linalg.qr|QR]] y Cholesky. Aquí se documenta **qué es**, **por qué NumPy no la expone** y **qué usar en su lugar**.

## Qué es la descomposición LU

Factoriza una matriz cuadrada `a` como `a = P @ L @ U`, donde:

| Factor | Nombre | Propiedad |
|--------|--------|-----------|
| `P` | Matriz de permutación | Reordena filas (pivoteo parcial, estabilidad) |
| `L` | Triangular **inferior** | Diagonal de unos (convención usual) |
| `U` | Triangular **superior** | Contiene los pivotes |

Es la base de la eliminación gaussiana con pivoteo y el método estándar para resolver sistemas densos `A x = b` y calcular determinantes.

## ⚠️ Por qué no está en NumPy

NumPy expone el **resultado** de la LU (resolver sistemas, determinante, inversa) pero **no** la factorización LU explícita. Internamente, `np.linalg.solve` y `np.linalg.det` llaman a LAPACK (`*getrf`/`*getrs`) que sí hace LU, pero NumPy no publica una API `lu()` que devuelva `(P, L, U)`. Esa API la ofrece SciPy.

```python
import numpy as np
np.linalg.lu        # AttributeError: module 'numpy.linalg' has no attribute 'lu'
```

## ✅ Alternativas reales

### Opción A — usar SciPy (factorización LU explícita)

```python
# ⚠️ Esto es SciPy, NO NumPy
import scipy.linalg as sla
P, L, U = sla.lu(A)            # a = P @ L @ U   (tupla de 3 arrays)
np.allclose(A, P @ L @ U)      # True

# Variante para resolver sistemas (formato compacto LAPACK):
lu, piv = sla.lu_factor(A)
x = sla.lu_solve((lu, piv), b)
```

| Función SciPy | Retorno | Uso |
|---------------|---------|-----|
| `scipy.linalg.lu(a)` | tupla `(P, L, U)` | factores explícitos legibles |
| `scipy.linalg.lu_factor(a)` | tupla `(lu, piv)` | formato compacto para resolver |
| `scipy.linalg.lu_solve((lu, piv), b)` | `x` | reutiliza la factorización |

### Opción B — quedarse en NumPy (sin LU explícita)

Si tu objetivo final es resolver o factorizar, NumPy cubre los casos habituales **sin** exponer LU:

| Quieres… | Usa en NumPy | Comentario |
|----------|--------------|------------|
| Resolver `A x = b` | [[np.linalg.solve]] | internamente hace LU con pivoteo |
| Resolver con `A` simétrica definida positiva | [[np.linalg.cholesky]] | más eficiente que LU |
| Mínimos cuadrados / ortogonalizar | [[np.linalg.qr]] | estable para sistemas rectangulares |
| Determinante | `np.linalg.det` | usa LU por debajo |
| Inversa | `np.linalg.inv` | rara vez necesaria; prefiere `solve` |

```python
# En vez de factorizar con LU para resolver, hazlo directo:
x = np.linalg.solve(A, b)      # NumPy aplica LU internamente
```

## Buenas prácticas

1. No busques `np.linalg.lu`: no existe. Si necesitas los factores `(P, L, U)`, importa `scipy.linalg`.
2. Para **resolver** sistemas, prefiere [[np.linalg.solve]] antes que factorizar a mano.
3. Si la matriz es simétrica definida positiva, [[np.linalg.cholesky]] es la opción correcta y más barata.
4. Reserva la LU explícita de SciPy para cuando necesites reutilizar la factorización (`lu_factor`/`lu_solve`) o inspeccionar los factores.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AttributeError: module 'numpy.linalg' has no attribute 'lu'` | LU no existe en NumPy | usar `scipy.linalg.lu` o [[np.linalg.solve]] |
| `ImportError`/SciPy ausente | SciPy no instalado | `pip install scipy`, o resolver con NumPy puro |
| `LinAlgError: Singular matrix` (al resolver) | matriz singular, sin LU válida | revisar el sistema; usar [[np.linalg.lstsq]] |
| Esperar 2 factores | `scipy.linalg.lu` devuelve **3** `(P, L, U)` | desempaquetar tres variables |

## Notas relacionadas

- [[np.linalg.solve]]
- [[np.linalg.cholesky]]
- [[np.linalg.qr]]
- [[np.linalg.svd]]
- [[concepto_shape]]
