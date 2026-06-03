---
title: scipy.linalg.svd — descomposicion en valores singulares (U, s, Vh)
aliases:
  - svd
  - scipy.linalg.svd
  - valores singulares
tags:
  - scipy
  - api/funcion
  - algebra-lineal
lib: scipy
tipo: funcion
mod: scipy.linalg
retorna: tuple (ndarray, ndarray, ndarray)
requiere:
  - numpy
draft: false
---

# scipy.linalg.svd — descomposicion en valores singulares (U, s, Vh)

Descompone cualquier matriz `a` de forma `(M, N)` como `a = U·diag(s)·Vh`, donde `U` `(M, M)` y `Vh` `(N, N)` son **unitarias/ortogonales** y `s` es el array de **valores singulares no negativos en orden descendente** (rutina LAPACK `gesdd`/`gesvd`). Es la factorizacion mas robusta del algebra lineal numerica: existe para toda matriz y revela rango, nucleo, pseudoinversa y mejor aproximacion de bajo rango.

> Clave: `s` es un **array 1D** de valores singulares, **no** una matriz diagonal. Para reconstruir `a` hay que expandirlo. `scipy.linalg.svd` corre sobre LAPACK; ver [[concepto_relacion_numpy]].

## Firma

```python
scipy.linalg.svd(
    a,                      # array_like: matriz (M, N)
    full_matrices=True,     # bool: formas completas de U y Vh
    compute_uv=True,        # bool: False -> devuelve solo 's'
    overwrite_a=False,      # bool: permite sobrescribir 'a'
    check_finite=True,      # bool: valida ausencia de NaN/inf
    lapack_driver='gesdd',  # str: 'gesdd' (rapido) | 'gesvd' (clasico)
) -> tuple | ndarray
```

## Valor de retorno

Con `compute_uv=True` (por defecto) devuelve **tres objetos** (`K = min(M, N)`):

| Posicion | Nombre | Forma (`full_matrices=True`) | Forma (`full_matrices=False`) | Significado |
|----------|--------|------------------------------|-------------------------------|-------------|
| `[0]` | `U` | `(M, M)` | `(M, K)` | Vectores singulares izquierdos (columnas) |
| `[1]` | `s` | `(K,)` | `(K,)` | Valores singulares, **array 1D**, descendentes |
| `[2]` | `Vh` | `(N, N)` | `(K, N)` | Vectores singulares derechos, ya **conjugado-transpuestos** |

Con `compute_uv=False` devuelve **solo** el array `s` `(K,)`.

```python
U, s, Vh = svd(a)                       # tres salidas
s        = svd(a, compute_uv=False)     # solo valores singulares
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| SVD completa | `svd(A)` -> `(U, s, Vh)` |
| SVD reducida (economica) | `svd(A, full_matrices=False)` |
| Solo valores singulares | `svd(A, compute_uv=False)` |
| Driver clasico mas robusto | `svd(A, lapack_driver='gesvd')` |

## Parametros en detalle

### `a` (obligatorio)

Matriz `(M, N)`, real o compleja, de cualquier rango. No requiere ser cuadrada ni invertible.

```python
import numpy as np
from scipy.linalg import svd

A = np.array([[1.0, 2.0],
              [3.0, 4.0],
              [5.0, 6.0]])
U, s, Vh = svd(A, full_matrices=False)
recon = U @ np.diag(s) @ Vh
np.allclose(recon, A)    # → True   (hay que expandir s a diag)
```

### `full_matrices`

Con `True` (def.), `U` y `Vh` son cuadradas completas. Con `False`, se recortan a `K = min(M, N)` columnas/filas: la **SVD economica**, suficiente para reconstruir `a` y mucho mas barata cuando `M` y `N` difieren mucho.

### `compute_uv`

`False` devuelve **solo** `s`. Util cuando solo interesan rango, norma 2 (`s[0]`) o numero de condicion, sin pagar el coste de los vectores singulares.

### `lapack_driver`

`'gesdd'` (divide y venceras) es el default y el mas rapido. `'gesvd'` es el algoritmo clasico, mas lento pero a veces mas robusto en casos patologicos.

## Casos de uso

### Rango numerico

El rango es el numero de valores singulares por encima de una tolerancia relativa a `s[0]`.

```python
s = svd(A, compute_uv=False)
tol = s[0] * max(A.shape) * np.finfo(float).eps
rank = int((s > tol).sum())
```

### Numero de condicion

Razon entre el mayor y el menor valor singular; cuantifica la sensibilidad del sistema.

```python
s = svd(A, compute_uv=False)
cond = s[0] / s[-1]    # numero de condicion en norma 2
```

### Pseudoinversa (minimos cuadrados / sistemas deficientes)

`A^+ = V·diag(1/s)·U^H`, invirtiendo solo los valores singulares no nulos. Es la base de `scipy.linalg.pinv`.

```python
U, s, Vh = svd(A, full_matrices=False)
A_pinv = Vh.T @ np.diag(1.0 / s) @ U.T
```

### Compresion / PCA de bajo rango

Quedarse con los `k` mayores valores singulares da la mejor aproximacion de rango `k` (teorema de Eckart-Young): base de PCA y compresion de imagenes/datos.

```python
k = 1
A_k = U[:, :k] @ np.diag(s[:k]) @ Vh[:k, :]   # mejor aproximacion rango-1
```

## Buenas practicas

1. Usa `full_matrices=False` salvo que necesites las bases completas del nucleo/cokernel: es mas rapido y usa menos memoria.
2. Si solo necesitas rango, norma 2 o condicion, pasa `compute_uv=False`.
3. Recuerda que `s` es **1D**: para reconstruir usa `np.diag(s)` (o `U[:, :k] * s[:k]` por broadcasting).
4. `Vh` ya viene transpuesta-conjugada; los vectores singulares derechos son sus **filas**, no columnas.
5. Cambia a `lapack_driver='gesvd'` si `gesdd` da resultados sospechosos en una matriz muy mal condicionada.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tratar `s` como matriz | `s` es un array 1D | Expandir con `np.diag(s)` para reconstruir |
| Usar `V` cuando se devuelve `Vh` | `Vh` ya esta transpuesta-conjugada | `V = Vh.conj().T` si necesitas `V` |
| `U @ s @ Vh` falla por formas | `full_matrices=True` deja `U`/`Vh` no compatibles con `s` recortado | Usar `full_matrices=False` o rellenar la diagonal |
| Dividir por `s` con ceros | Matriz deficiente de rango | Truncar los `s` por debajo de la tolerancia |
| Coste alto en matrices enormes | SVD densa es `O(M·N·min(M,N))` | Usar SVD truncada (`scipy.sparse.linalg.svds`) |

## Limitaciones

- SVD densa es costosa para matrices muy grandes; para pocas componentes usar SVD truncada de `scipy.sparse.linalg`.
- Devuelve siempre `Vh` (no `V`): hay que conjugar-transponer si se quiere `V`.
- No aprovecha estructura especial (simetria, dispersion): para matrices simetricas, la diagonalizacion via `eigh` puede ser preferible.

## Notas relacionadas

- [[scipy.linalg.eig]]
- [[scipy.linalg.qr]]
- [[concepto_relacion_numpy]]
