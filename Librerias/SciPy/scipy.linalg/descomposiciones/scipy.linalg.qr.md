---
title: scipy.linalg.qr — factorizacion QR (Q ortogonal, R triangular)
aliases:
  - qr
  - scipy.linalg.qr
  - factorizacion QR
tags:
  - scipy
  - api/funcion
  - algebra-lineal
lib: scipy
tipo: funcion
mod: scipy.linalg
retorna: tuple (ndarray, ndarray)
requiere:
  - numpy
draft: false
---

# scipy.linalg.qr — factorizacion QR (Q ortogonal, R triangular)

Factoriza una matriz `a` de forma `(M, N)` como `a = Q·R`, con `Q` **ortogonal** (`Q^H·Q = I`, sus columnas son una base ortonormal) y `R` **triangular superior** (rutina LAPACK `geqrf` + `orgqr`). Es la herramienta numericamente estable para **minimos cuadrados** y para **ortonormalizar** un conjunto de vectores. El parametro `mode` controla que se devuelve y las formas de `Q`/`R`.

> `scipy.linalg.qr` ofrece mas opciones (`pivoting`, `mode='raw'`) que `numpy.linalg.qr` y corre siempre sobre LAPACK; ver [[concepto_relacion_numpy]].

## Firma

```python
scipy.linalg.qr(
    a,                   # array_like: matriz (M, N)
    overwrite_a=False,   # bool: permite sobrescribir 'a'
    lwork=None,          # int: tamaño del workspace LAPACK (auto si None)
    mode='full',         # str: 'full' | 'economic' | 'r' | 'raw'
    pivoting=False,      # bool: QR con pivoteo de columnas (añade 'P')
    check_finite=True,   # bool: valida ausencia de NaN/inf
) -> tuple
```

## Valor de retorno

El contenido y las formas dependen de `mode` (con `M >= N`, `K = min(M, N)`):

| `mode` | Devuelve | Forma `Q` | Forma `R` |
|--------|----------|-----------|-----------|
| `'full'` (def.) | `(Q, R)` | `(M, M)` | `(M, N)` |
| `'economic'` | `(Q, R)` | `(M, K)` | `(K, N)` |
| `'r'` | `(R,)` | — | `(M, N)` o `(K, N)` |
| `'raw'` | `((qr, tau), R)` | reflectores Householder crudos | `(M, N)` |

Con `pivoting=True` se añade un array extra `P` (vector de indices de columna) al final de la tupla, tal que `a[:, P] = Q·R`.

```python
Q, R = qr(a)                       # mode='full'
Q, R = qr(a, mode='economic')      # Q reducida (M, K)
R,   = qr(a, mode='r')             # solo R (ojo: tupla de 1)
Q, R, P = qr(a, pivoting=True)     # con pivoteo de columnas
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| QR completa | `qr(A)` -> `(Q, R)` |
| QR reducida (economica) | `qr(A, mode='economic')` |
| Solo el factor R | `qr(A, mode='r')` |
| QR con pivoteo de columnas | `qr(A, pivoting=True)` -> `(Q, R, P)` |

## Parametros en detalle

### `a` (obligatorio)

Matriz `(M, N)`, real o compleja. El caso tipico de minimos cuadrados es `M > N` (mas ecuaciones que incognitas).

```python
import numpy as np
from scipy.linalg import qr

A = np.array([[1.0, 2.0],
              [3.0, 4.0],
              [5.0, 6.0]])
Q, R = qr(A, mode='economic')
np.allclose(Q @ R, A)            # → True
np.allclose(Q.T @ Q, np.eye(2)) # → True   (columnas ortonormales)
```

### `mode`

- `'full'`: `Q` cuadrada `(M, M)`, base ortonormal completa de R^M.
- `'economic'`: `Q` reducida `(M, K)`; suficiente y mas barata para minimos cuadrados.
- `'r'`: omite `Q` y devuelve solo `R` (ahorra memoria si `Q` no hace falta).
- `'raw'`: devuelve los reflectores de Householder sin ensamblar `Q`; para uso experto con rutinas LAPACK posteriores.

### `pivoting`

QR con **pivoteo de columnas** (LAPACK `geqp3`): reordena columnas por norma decreciente, revelando el rango numerico y mejorando la estabilidad en matrices casi deficientes de rango. Devuelve el array de permutacion `P`.

### `overwrite_a`, `check_finite`

`overwrite_a=True` reutiliza el buffer de `a`. `check_finite=False` salta la validacion de finitud para ganar velocidad.

## Casos de uso

### Minimos cuadrados via QR

Para `min ||A·x - b||`, con `A = Q·R` el sistema se reduce a `R·x = Q^H·b`, que se resuelve por sustitucion regresiva (triangular).

```python
import numpy as np
from scipy.linalg import qr, solve_triangular

A = np.array([[1.0, 1.0], [1.0, 2.0], [1.0, 3.0]])
b = np.array([1.0, 2.0, 2.0])

Q, R = qr(A, mode='economic')
x = solve_triangular(R, Q.T @ b)   # solucion de minimos cuadrados
```

### Ortonormalizacion de vectores

Las columnas de `Q` son una base ortonormal del espacio generado por las columnas de `A`: equivale a un Gram-Schmidt numericamente estable.

```python
V = np.random.rand(5, 3)
Q, _ = qr(V, mode='economic')      # Q: base ortonormal del span de V
```

## Buenas practicas

1. Para minimos cuadrados usa `mode='economic'`: `Q` completa `(M, M)` desperdicia memoria si `M >> N`.
2. Si solo necesitas `R` (p.ej. para el factor de Cholesky implicito de `A^H·A`), usa `mode='r'`.
3. Recuerda que `mode='r'` devuelve una **tupla de un elemento**: desempaqueta con `R, = qr(A, mode='r')`.
4. Activa `pivoting=True` cuando sospeches deficiencia de rango o mal condicionamiento.
5. Prefiere QR a las ecuaciones normales `A^H·A·x = A^H·b`: estas elevan al cuadrado el numero de condicion.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `R` no es triangular para `M < N` | `R` es trapezoidal si hay mas columnas que filas | Esperado; sigue cumpliendo `a = Q·R` |
| Desempaquetar mal `mode='r'` | Devuelve `(R,)`, no `R` | Usar `R, = qr(A, mode='r')` |
| `Q @ R != A` con pivoting | El pivoteo permuta columnas | Comparar `Q @ R` con `A[:, P]` |
| Memoria excesiva en `M >> N` | `mode='full'` crea `Q` `(M, M)` | Usar `mode='economic'` |
| Usar ecuaciones normales | Pierde precision por condicion al cuadrado | Resolver via QR |

## Limitaciones

- No revela por si sola el rango salvo con `pivoting=True`; para rango fiable, SVD es el estandar.
- `mode='raw'` devuelve estructuras de bajo nivel utiles solo con LAPACK directo.
- Para sistemas cuadrados bien condicionados, LU suele ser mas barata que QR.

## Notas relacionadas

- [[scipy.linalg.svd]]
- [[scipy.linalg.lu]]
- [[concepto_relacion_numpy]]
