---
title: scipy.linalg.inv — inversa de una matriz cuadrada
aliases:
  - inv
  - scipy.linalg.inv
  - inversa de matriz
tags:
  - scipy
  - api/funcion
  - algebra-lineal
lib: scipy
tipo: funcion
mod: scipy.linalg
retorna: ndarray
requiere:
  - numpy
  - concepto_relacion_numpy
draft: false
---

# scipy.linalg.inv — inversa de una matriz cuadrada

Calcula la inversa `a⁻¹` de una matriz cuadrada `(n, n)`, tal que `a @ a⁻¹ = I`. Internamente factoriza con LU (LAPACK `getrf`/`getri`) y resuelve; siempre se apoya en BLAS/LAPACK, como toda `scipy.linalg`. Devuelve un `ndarray` `(n, n)`. Lanza `LinAlgError` si `a` es singular (no invertible).

> [!warning] No la uses para resolver sistemas
> Para resolver `a·x = b` **no** escribas `inv(a) @ b`: es mas lento (invertir cuesta mas que factorizar y resolver) y numericamente peor condicionado. Usa `solve`. `inv` solo se justifica cuando necesitas la **inversa explicita** como objeto (matrices de covarianza, propagacion de incertidumbre, formulas cerradas que la contienen). Detalle del backend LAPACK en [[concepto_relacion_numpy]].

## Firma

```python
scipy.linalg.inv(
    a,                   # array (n, n): matriz cuadrada a invertir
    overwrite_a=False,   # bool: permite sobrescribir 'a' (ahorra memoria)
    check_finite=True,   # bool: valida ausencia de NaN/inf (False -> mas rapido, inseguro)
) -> ndarray
```

## Valor de retorno

| Salida | Tipo | Forma | Significado |
|--------|------|-------|-------------|
| `a_inv` | `ndarray` | `(n, n)` | Matriz inversa; `a @ a_inv ≈ I` |

```python
Ai = inv(A)   # A @ Ai ≈ identidad
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Inversa basica | `inv(A)` |
| Sobrescribiendo la entrada | `inv(A, overwrite_a=True)` |
| Sin validar finitud (bucle critico) | `inv(A, check_finite=False)` |

## Parametros en detalle

### `a` (obligatorio)

Matriz cuadrada `(n, n)` y no singular. Si `det(a) ≈ 0` (o, mejor dicho, si esta mal condicionada), la inversa o bien falla con `LinAlgError` o sale numericamente basura.

```python
import numpy as np
from scipy.linalg import inv

A = np.array([[4.0, 7.0], [2.0, 6.0]])
Ai = inv(A)
Ai           # → [[ 0.6, -0.7], [-0.2,  0.4]]
A @ Ai       # → [[1., 0.], [0., 1.]]  (identidad, salvo epsilon)
```

### `overwrite_a`

Si `True`, LAPACK puede reutilizar la memoria de `a` durante el calculo (ahorra una copia). Tras la llamada `a` queda en estado indefinido; usalo solo si no vuelves a necesitar la matriz original.

### `check_finite`

Con `True` (defecto) valida que no haya `NaN`/`inf` antes de llamar a LAPACK; pasar `inf` a LAPACK puede colgar o devolver basura. `False` ahorra ese chequeo en bucles con datos ya saneados.

## Casos de uso

### Inversa explicita justificada: matriz de covarianza

```python
import numpy as np
from scipy.linalg import inv

# Matriz de precision = inversa de la covarianza (se necesita la inversa como tal)
Sigma = np.array([[2.0, 0.3], [0.3, 1.0]])
P = inv(Sigma)        # matriz de precision, usada en gaussianas / Mahalanobis
P    # → [[ 0.515..., -0.154...], [-0.154...,  1.030...]]
```

### Comparacion: resolver un sistema (NO usar inv)

```python
from scipy.linalg import inv, solve

A = np.array([[3.0, 2.0], [1.0, 2.0]])
b = np.array([12.0, 8.0])

x_malo  = inv(A) @ b     # funciona, pero lento y peor condicionado
x_bueno = solve(A, b)    # CORRECTO: factoriza y resuelve directo
x_bueno  # → [2., 3.]
```

### Forma cuadratica con inversa (distancia de Mahalanobis)

```python
# d² = (x - mu)ᵀ Σ⁻¹ (x - mu): aqui la inversa entra en una formula cerrada
mu = np.array([0.0, 0.0])
x  = np.array([1.0, 1.0])
Pinv = inv(Sigma)
d2 = (x - mu) @ Pinv @ (x - mu)
d2   # → distancia de Mahalanobis al cuadrado
```

## Buenas practicas

1. Pregunta primero: ¿necesitas la inversa **como objeto** o solo resolver un sistema? Si es lo segundo, usa `solve`.
2. Antes de invertir, valora el condicionamiento con `np.linalg.cond(A)`; un valor enorme anuncia una inversa poco fiable.
3. Verifica con `A @ inv(A)` que se aproxime a la identidad cuando dudes.
4. Si vas a reusar la misma `A` para varios sistemas, factoriza con `lu_factor` en vez de invertir.
5. Deja `check_finite=True` salvo en codigo de rendimiento con datos garantizados.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `LinAlgError: singular matrix` | `a` no invertible (det≈0) | Revisar el modelo; usar `pinv` (pseudoinversa) si procede |
| `inv(A) @ b` lento o impreciso | Antipatron: invertir para resolver | Usar `solve(A, b)` |
| `ValueError: ... must be square` | `a` no es `(n, n)` | Para rectangulares usar `pinv` |
| Inversa con valores enormes/ruido | `a` mal condicionada | Revisar `cond(A)`; reformular o regularizar |
| Cuelgue / resultado raro con `inf` | `check_finite=False` con datos sucios | Mantener `check_finite=True` |

## Limitaciones

- Solo matrices **cuadradas** no singulares; para rectangulares o singulares usa `pinv` (pseudoinversa de Moore-Penrose).
- Calcular la inversa para luego resolver sistemas es ineficiente y menos estable que `solve`.
- Para matrices dispersas grandes la inversa suele ser densa y prohibitiva: evita invertir, usa solvers dispersos.
- No avisa de mal condicionamiento: una inversa puede salir formalmente sin error y ser inutil.

## Notas relacionadas

- [[scipy.linalg.solve]]
- [[scipy.linalg.det]]
- [[concepto_relacion_numpy]]
