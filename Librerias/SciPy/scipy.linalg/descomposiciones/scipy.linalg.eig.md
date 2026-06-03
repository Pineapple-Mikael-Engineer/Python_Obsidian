---
title: scipy.linalg.eig — autovalores y autovectores (w, v)
aliases:
  - eig
  - scipy.linalg.eig
  - autovalores autovectores
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

# scipy.linalg.eig — autovalores y autovectores (w, v)

Resuelve el problema de autovalores `a·v = w·v` de una matriz cuadrada general (rutina LAPACK `geev`). Devuelve la **tupla** `(w, v)`: `w` es el array de **autovalores** (en general **complejos**, aunque `a` sea real) y `v` es la matriz cuyas **columnas** son los autovectores derechos normalizados. Con `b != None` resuelve el problema **generalizado** `a·v = w·b·v`.

> Para matrices **simetricas/hermiticas** usa `eigh`: da autovalores **reales y ordenados**, es mas rapido y mas estable. Prefierelo siempre que aplique. SciPy corre sobre LAPACK; ver [[concepto_relacion_numpy]].

## Firma

```python
scipy.linalg.eig(
    a,                   # array_like: matriz (M, M) general
    b=None,              # array_like | None: matriz del problema generalizado a v = w b v
    left=False,          # bool: tambien calcular autovectores izquierdos
    right=True,          # bool: calcular autovectores derechos (def.)
    overwrite_a=False,   # bool: permite sobrescribir 'a'
    overwrite_b=False,   # bool: permite sobrescribir 'b'
    check_finite=True,   # bool: valida ausencia de NaN/inf
    homogeneous_eigvals=False,  # bool: devuelve autovalores en forma homogenea
) -> tuple
```

## Valor de retorno

Por defecto (`right=True`, `left=False`) devuelve **dos arrays**:

| Posicion | Nombre | Forma | Significado |
|----------|--------|-------|-------------|
| `[0]` | `w` | `(M,)` | Autovalores, **complejos** en general, sin orden garantizado |
| `[1]` | `vr` | `(M, M)` | Autovectores derechos: la **columna** `vr[:, i]` corresponde a `w[i]` |

Con `left=True` se añade `vl` (autovectores izquierdos) a la tupla. Variante relacionada: `eigvals(a)` devuelve **solo** `w`.

```python
w, v = eig(a)                  # autovalores + autovectores derechos
w, vl, vr = eig(a, left=True)  # tambien autovectores izquierdos
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Autovalores + autovectores | `eig(A)` -> `(w, v)` |
| Solo autovalores | `eigvals(A)` -> `w` |
| Problema generalizado | `eig(A, B)` -> resuelve `A v = w B v` |
| Matriz simetrica/hermitica | `eigh(A)` -> `(w_real_ordenado, v)` |

## Parametros en detalle

### `a` (obligatorio)

Matriz cuadrada `(M, M)`, real o compleja, **no necesariamente simetrica**. Por eso los autovalores salen en general complejos.

```python
import numpy as np
from scipy.linalg import eig

A = np.array([[0.0, -1.0],
              [1.0,  0.0]])     # rotacion: autovalores ±i
w, v = eig(A)
w     # → [0.+1.j, 0.-1.j]   (complejos aunque A sea real)
```

Verificacion del par autovalor/autovector (columna `i`):

```python
i = 0
np.allclose(A @ v[:, i], w[i] * v[:, i])   # → True
```

### `b` (problema generalizado)

Si se pasa, resuelve `a·v = w·b·v` (rutina `ggev`). Aparece en mecanica de vibraciones (matrices de masa y rigidez `K·v = w·M·v`) y en analisis de estabilidad.

```python
K = np.array([[6.0, -2.0], [-2.0, 4.0]])   # rigidez
M = np.array([[2.0,  0.0], [ 0.0, 1.0]])   # masa
w, v = eig(K, M)                            # K v = w M v
```

### `left`, `right`

`right=True` (def.) calcula autovectores derechos `vr` (`a·vr = w·vr`). `left=True` añade los izquierdos `vl` (`vl^H·a = w·vl^H`), utiles en analisis de sensibilidad y sistemas dinamicos.

### `overwrite_a`, `overwrite_b`, `check_finite`

Optimizaciones: reutilizar buffers de entrada y/o saltar la validacion de finitud para ganar velocidad.

## Casos de uso

### Modos de vibracion (problema generalizado)

Las frecuencias naturales `omega` salen de `K·v = omega^2·M·v`; los autovectores son las formas modales.

```python
import numpy as np
from scipy.linalg import eig

w, modos = eig(K, M)
frecuencias = np.sqrt(np.real(w))   # omega = sqrt(autovalor)
```

### Estabilidad de un sistema dinamico

Para `x' = A·x`, el sistema es estable si **todos** los autovalores tienen parte real negativa.

```python
w = eig(A, right=False)[0]
estable = np.all(np.real(w) < 0)
```

### PCA via matriz de covarianza (simetrica -> eigh)

La covarianza es simetrica: `eigh` da autovalores reales ya **ordenados ascendentemente** y autovectores ortonormales, ideales para componentes principales.

```python
from scipy.linalg import eigh

C = np.cov(datos, rowvar=False)      # simetrica
vals, vecs = eigh(C)                  # reales y ordenados
componentes = vecs[:, ::-1]          # de mayor a menor varianza
```

## Buenas practicas

1. Si la matriz es **simetrica/hermitica**, usa `eigh`: autovalores reales, ordenados, mas rapido y estable. Reserva `eig` para matrices generales.
2. Si solo necesitas los autovalores, usa `eigvals` / `eigvalsh`: evitas calcular autovectores.
3. Recuerda que los autovectores son **columnas** de `v`: el de `w[i]` es `v[:, i]`, no `v[i, :]`.
4. No asumas orden en `w` de `eig`: ordena tu mismo si lo necesitas (`np.argsort`).
5. Trabaja con tipos complejos al manipular `w`/`v` de `eig`, aunque `a` sea real; toma `np.real`/`np.imag` solo cuando sepas que corresponde.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Tomar autovectores como filas | Son **columnas** de `v` | Usar `v[:, i]` para `w[i]` |
| Esperar autovalores reales | `eig` los da complejos en general | Usar `eigh` si la matriz es simetrica |
| Asumir orden de `w` | `eig` no ordena | Ordenar con `np.argsort(w)` |
| Comparar con `numpy.linalg.eig` y diferir | Distinta ruta LAPACK / signo de autovectores | Diferencias de signo/fase son validas |
| Usar `eig` en matriz SPD grande | Mas lento y menos estable que `eigh` | Cambiar a `eigh`/`eigvalsh` |

## Limitaciones

- Para matrices simetricas/hermiticas es subоptima: `eigh` es mas rapida, estable y ordena.
- No explota dispersion: para pocas componentes de matrices grandes/sparse usar `scipy.sparse.linalg.eigs`.
- El signo/fase de los autovectores no es unico; no esperes reproducibilidad bit a bit entre backends.

## Notas relacionadas

- [[scipy.linalg.svd]]
- [[scipy.linalg.cholesky]]
- [[concepto_relacion_numpy]]
