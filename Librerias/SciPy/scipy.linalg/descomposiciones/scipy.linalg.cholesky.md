---
title: scipy.linalg.cholesky — factorizacion de Cholesky de matriz SPD
aliases:
  - cholesky
  - scipy.linalg.cholesky
  - factorizacion de Cholesky
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
draft: false
---

# scipy.linalg.cholesky — factorizacion de Cholesky de matriz SPD

Factoriza una matriz `a` **simetrica/hermitica y definida positiva** (SPD) como `a = U^H·U` (o `a = L·L^H` si `lower=True`), con `U` triangular superior y `L` triangular inferior (rutina LAPACK `potrf`). Devuelve **un solo array triangular** (superior por defecto). Es ~2x mas rapida que LU porque explota la simetria, y **lanza `LinAlgError` si la matriz no es definida positiva** — de hecho es la forma barata estandar de **testear definicion positiva**.

> A diferencia de `lu`/`svd`, esta funcion devuelve **un unico array**, no una tupla. SciPy corre sobre LAPACK; ver [[concepto_relacion_numpy]].

## Firma

```python
scipy.linalg.cholesky(
    a,                   # array_like: matriz (M, M) simetrica/hermitica SPD
    lower=False,         # bool: True -> devuelve L (inferior); False -> U (superior)
    overwrite_a=False,   # bool: permite sobrescribir 'a'
    check_finite=True,   # bool: valida ausencia de NaN/inf
) -> ndarray
```

## Valor de retorno

Devuelve **un solo array** triangular `(M, M)`:

| `lower` | Devuelve | Relacion |
|---------|----------|----------|
| `False` (def.) | `U` triangular superior | `a = U^H·U` |
| `True` | `L` triangular inferior | `a = L·L^H` |

La parte no usada del triangulo se devuelve como ceros. No existe la otra mitad: `U` y `L` son conjugado-transpuestas entre si (`L = U^H`).

```python
U = cholesky(a)               # a = U^H @ U
L = cholesky(a, lower=True)   # a = L @ L^H
```

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Factor superior | `cholesky(A)` -> `U` |
| Factor inferior | `cholesky(A, lower=True)` -> `L` |
| Test de definicion positiva | `try: cholesky(A) except LinAlgError: ...` |
| Sin validar finitud | `cholesky(A, check_finite=False)` |

## Parametros en detalle

### `a` (obligatorio)

Matriz cuadrada `(M, M)` **simetrica** (real) o **hermitica** (compleja) y **definida positiva**. Solo se lee un triangulo; la otra mitad se ignora (se asume la simetria).

```python
import numpy as np
from scipy.linalg import cholesky

A = np.array([[4.0, 2.0],
              [2.0, 3.0]])         # SPD
L = cholesky(A, lower=True)
np.allclose(L @ L.T, A)            # → True
```

### `lower`

Selecciona que triangulo se calcula y devuelve. `False` (def.) da `U` con `a = U^H·U`; `True` da `L` con `a = L·L^H`. Elige segun la convencion del algoritmo que consuma el factor.

### `overwrite_a`, `check_finite`

`overwrite_a=True` reutiliza el buffer de `a` (mas rapido, lo destruye). `check_finite=False` salta la validacion de finitud.

## Casos de uso

### Test barato de definicion positiva

Si Cholesky no lanza, la matriz es SPD; si lanza `LinAlgError`, no lo es. Es mas rapido y fiable que mirar autovalores.

```python
from numpy.linalg import LinAlgError

def es_definida_positiva(A):
    try:
        cholesky(A)
        return True
    except LinAlgError:
        return False
```

### Resolver sistemas SPD (mas rapido que LU)

Con `a = L·L^H`, el sistema `A·x = b` se resuelve con dos sustituciones triangulares. En la practica se usa la pareja `cho_factor` + `cho_solve`.

```python
import numpy as np
from scipy.linalg import cho_factor, cho_solve

A = np.array([[4.0, 2.0], [2.0, 3.0]])
c = cho_factor(A)                 # factoriza una vez
x = cho_solve(c, [1.0, 2.0])      # resuelve A x = b reutilizando
```

### Muestreo gaussiano multivariante

Para generar muestras de `N(mu, Sigma)` se usa `x = mu + L·z` con `z ~ N(0, I)` y `L` el factor de Cholesky de la covarianza `Sigma`.

```python
mu = np.array([0.0, 0.0])
Sigma = np.array([[2.0, 0.8], [0.8, 1.0]])
L = cholesky(Sigma, lower=True)
z = np.random.standard_normal(2)
muestra = mu + L @ z              # ~ N(mu, Sigma)
```

## Buenas practicas

1. Usa Cholesky (no LU) siempre que la matriz sea SPD: la mitad de operaciones y mayor estabilidad.
2. Aprovecha el `LinAlgError` como **test** de definicion positiva en vez de calcular autovalores.
3. Para resolver sistemas SPD con multiples RHS usa `cho_factor` + `cho_solve`.
4. Fija una convencion (`lower=True` o `False`) coherente con el resto del codigo para evitar transposiciones accidentales.
5. Si la matriz es solo **semidefinida** (algun autovalor cero) Cholesky fallara: usa SVD o una factorizacion pivotada.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| `LinAlgError: not positive definite` | Matriz no SPD (autovalor <= 0) | Verificar simetria/SPD; usar LU o regularizar |
| Esperar una tupla `(L, U)` | Cholesky devuelve **un solo** triangulo | Desempaquetar un unico array |
| Mezclar convenciones `U` vs `L` | Confundir `a=U^H U` con `a=L L^H` | Fijar `lower` y reconstruir con el factor correcto |
| Usarla en matriz no simetrica | Solo lee un triangulo, ignora el otro | Asegurar simetria antes de factorizar |
| Falla por error de redondeo en SPD limite | Casi singular | Añadir `eps·I` (regularizacion) |

## Limitaciones

- Solo para matrices **SPD** (simetricas/hermiticas definidas positivas); no sirve para matrices generales ni indefinidas.
- Falla con matrices semidefinidas o numericamente casi singulares: requieren regularizacion o SVD.
- No revela autovalores ni rango directamente; para eso usar `eigh` o `svd`.

## Notas relacionadas

- [[scipy.linalg.lu]]
- [[scipy.linalg.eig]]
- [[concepto_relacion_numpy]]
