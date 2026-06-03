---
title: scipy.linalg.solve — resuelve el sistema lineal a·x = b
aliases:
  - solve
  - scipy.linalg.solve
  - resolver sistema lineal
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

# scipy.linalg.solve — resuelve el sistema lineal a·x = b

Resuelve el sistema de ecuaciones lineales `a·x = b` para `x`, donde `a` es una matriz cuadrada `(n, n)` y `b` un vector `(n,)` o una matriz `(n, m)` (varios lados derechos a la vez). Internamente factoriza `a` con LAPACK (LU por defecto) y resuelve por sustitucion; **nunca** calcula la inversa. Devuelve un `ndarray` con la solucion `x`.

> REGLA DE ORO: para resolver `a·x = b` usa `solve`, **nunca** `inv(a) @ b`. `solve` es mas rapido (factoriza, no invierte) y numericamente mejor condicionado. Como toda `scipy.linalg`, se apoya siempre en BLAS/LAPACK y es un superset de `numpy.linalg`; ver [[concepto_relacion_numpy]].

## Firma

```python
scipy.linalg.solve(
    a,                   # array (n, n): matriz de coeficientes cuadrada
    b,                   # array (n,) o (n, m): lado(s) derecho(s)
    lower=False,         # bool: si assume_a triangular/sym, usar solo triangulo inferior
    overwrite_a=False,   # bool: permite sobrescribir 'a' (ahorra memoria)
    overwrite_b=False,   # bool: permite sobrescribir 'b'
    check_finite=True,   # bool: valida que no haya NaN/inf (False -> mas rapido, inseguro)
    assume_a='gen',      # str: estructura de 'a' -> 'gen' | 'sym' | 'her' | 'pos'
    transposed=False,    # bool: resuelve a^T · x = b en su lugar
) -> ndarray
```

## Valor de retorno

| Salida | Tipo | Forma | Significado |
|--------|------|-------|-------------|
| `x` | `ndarray` | `(n,)` o `(n, m)` | Solucion del sistema; misma forma que `b` |

```python
x = solve(A, b)   # A @ x ≈ b
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Sistema general | `solve(A, b)` |
| Matriz simetrica | `solve(A, b, assume_a='sym')` |
| Matriz definida positiva (Cholesky) | `solve(A, b, assume_a='pos')` |
| Varios lados derechos | `solve(A, B)` con `B` de forma `(n, m)` |
| Resolver `Aᵀ x = b` | `solve(A, b, transposed=True)` |

## Parametros en detalle

### `a`, `b` (obligatorios)

`a` debe ser cuadrada `(n, n)` y no singular. `b` puede ser un vector `(n,)` o una matriz `(n, m)`; en el segundo caso resuelve un sistema por cada columna reutilizando la **misma** factorizacion (mucho mas barato que `m` llamadas sueltas).

```python
import numpy as np
from scipy.linalg import solve

A = np.array([[3.0, 2.0], [1.0, 2.0]])
b = np.array([12.0, 8.0])
x = solve(A, b)
x    # → [2., 3.]   (3·2 + 2·3 = 12 ; 1·2 + 2·3 = 8)
```

### `assume_a`

Declara la estructura de `a` para elegir el algoritmo LAPACK optimo. Si la afirmacion es **falsa**, el resultado sera incorrecto sin avisar.

| Valor | Estructura | Factorizacion | Cuando |
|-------|-----------|---------------|--------|
| `'gen'` | general (defecto) | LU con pivoteo | caso comun, sin estructura |
| `'sym'` | simetrica real | LDLᵀ | `a == a.T` |
| `'her'` | hermitica compleja | LDLᴴ | `a == a.conj().T` |
| `'pos'` | simetrica definida positiva | Cholesky | la mas rapida y estable; matrices de rigidez, covarianzas |

```python
# Definida positiva: Cholesky, ~2x mas rapido que LU general
x = solve(A, b, assume_a='pos')
```

### `lower`

Solo relevante con `assume_a` simetrica/hermitica/positiva: indica si los datos validos estan en el triangulo inferior (`True`) o superior (`False`). El otro triangulo se ignora.

### `transposed`

Si `True`, resuelve `aᵀ·x = b` sin transponer explicitamente `a` (ahorra una copia). No soportado para `a` compleja.

### `overwrite_a`, `overwrite_b`, `check_finite`

`overwrite_*` autorizan reutilizar la memoria de los arrays de entrada (mas rapido si ya no los necesitas; pueden quedar corruptos tras la llamada). `check_finite=False` salta la validacion de `NaN`/`inf`: acelera, pero ante datos sucios produce resultados sin sentido.

## Casos de uso

### Sistema de ecuaciones de un balance

```python
import numpy as np
from scipy.linalg import solve

# Mezcla: 2 corrientes que deben dar 100 kg al 30% de soluto
#  x + y = 100 ;  0.5 x + 0.2 y = 30
A = np.array([[1.0, 1.0], [0.5, 0.2]])
b = np.array([100.0, 30.0])
x = solve(A, b)
x    # → [33.33..., 66.66...]  kg de cada corriente
```

### Red de resistencias (analisis nodal)

```python
# Leyes de Kirchhoff -> G·V = I  (G: matriz de conductancias, I: inyecciones)
G = np.array([[ 3.0, -1.0, -1.0],
              [-1.0,  4.0, -1.0],
              [-1.0, -1.0,  3.0]])   # siemens
I = np.array([5.0, 0.0, -5.0])       # amperios
V = solve(G, I, assume_a='sym')      # G simetrica -> LDLᵀ
V    # → tensiones nodales en voltios
```

### Equilibrio estatico (varios casos de carga)

```python
# Misma matriz de rigidez K, varias cargas F (columnas) -> una factorizacion
K = np.array([[10.0, -2.0], [-2.0, 6.0]])
F = np.array([[1.0, 0.0, 2.0],
              [0.0, 1.0, 1.0]])      # 3 casos de carga
U = solve(K, F, assume_a='pos')      # K definida positiva
U.shape    # → (2, 3): un vector de desplazamientos por columna
```

## Buenas practicas

1. Usa `solve`, no `inv(A) @ b`: mas rapido y mejor condicionado.
2. Si la matriz es definida positiva (rigidez, covarianza, laplaciano), pasa `assume_a='pos'`: aprovecha Cholesky.
3. Para varios lados derechos agrupa en una matriz `b` `(n, m)` y llama **una** vez: reutiliza la factorizacion.
4. Comprueba `A @ x` frente a `b` (residuo) cuando dudes del condicionamiento.
5. Deja `check_finite=True` salvo en bucles criticos con datos ya validados.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `LinAlgError: singular matrix` | `a` no invertible (det≈0) | Revisar el modelo; usar `lstsq` si no hay solucion unica |
| `ValueError: ... must be square` | `a` no es `(n, n)` | Sistema sobre/infradeterminado -> `lstsq` |
| Solucion incorrecta sin aviso | `assume_a` no coincide con la estructura real | Usar `'gen'` si no estas seguro |
| Resultado lento en bucle | `inv(A) @ b` o re-factorizar cada vez | Factorizar una vez (`lu_factor`/`cho_factor`) y reusar |
| `ValueError` con `b` mal alineado | Filas de `b` ≠ filas de `a` | Asegurar `b.shape[0] == n` |

## Limitaciones

- Requiere `a` **cuadrada** y no singular; para sistemas rectangulares o minimos cuadrados usa `lstsq`.
- Para muchas resoluciones con la misma `a` pero `b` que llegan en momentos distintos, conviene `lu_factor` + `lu_solve` (o `cho_factor` + `cho_solve`) y no llamar a `solve` repetidamente.
- Para matrices dispersas grandes, esto es denso: usar `scipy.sparse.linalg.spsolve`.
- No estima por si solo el condicionamiento; si `a` esta mal condicionada, la solucion puede ser inexacta sin lanzar error.

## Notas relacionadas

- [[scipy.linalg.inv]]
- [[scipy.linalg.det]]
- [[concepto_relacion_numpy]]
