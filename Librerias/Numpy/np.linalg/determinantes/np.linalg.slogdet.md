---
title: np.linalg.slogdet — signo y log|det| (estable frente al overflow de det)
aliases:
  - slogdet
  - linalg.slogdet
  - np.linalg.slogdet
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: namedtuple (sign, logabsdet)
inplace: false
requiere:
  - concepto_shape
  - concepto_vectorizacion
draft: false
---

# np.linalg.slogdet — signo y logaritmo del determinante

`np.linalg.slogdet` calcula el determinante **partido en dos piezas estables**: el **signo** y el
**logaritmo de su valor absoluto**, en lugar del número entero. Esto evita exactamente el problema
de [[np.linalg.det]]: como el determinante es un producto exponencialmente grande o pequeño, `det`
**desborda** (`inf`) o **subdesborda** (`0`) en matrices grandes; trabajar en escala logarítmica
nunca lo hace. Es la forma correcta de obtener $\det$ (o, sobre todo, $\log|\det|$) cuando la matriz
es grande o sus valores son muy dispares.

## La idea en una fórmula

`slogdet` devuelve el par $(\text{sign}, \text{logabsdet})$ que **factoriza** el determinante en su
signo y la magnitud de su logaritmo:

$$
\det(A) \;=\; \text{sign}\cdot e^{\,\text{logabsdet}}
\qquad\text{con}\qquad
\text{logabsdet} = \ln\lvert\det(A)\rvert
$$

La gracia es que `logabsdet` puede ser un número manejable (p. ej. $4605$) aunque el determinante
real ($e^{4605}$) desborde cualquier flotante. **El mapa de shapes** es el mismo de `det` —colapsar
la matriz a un escalar— pero produciendo **dos** salidas con esa misma forma de lote:

$$
(\underbrace{\dots}_{\text{lote}},\, n,\, n)\ \xrightarrow{\ \text{slogdet}\ }\
\underbrace{(\dots)}_{\text{sign}}\ ,\ \underbrace{(\dots)}_{\text{logabsdet}}
$$

Para una sola matriz $(n,n)$ ambas salidas son **escalares** `()`; para un lote $(b,n,n)$ ambas son
`(b,)`.

## Firma

```python
np.linalg.slogdet(a) -> SlogdetResult(sign, logabsdet)   # namedtuple de 2 ndarray/escalares
```

Como `det`, no tiene parámetros opcionales: toda la información está en el shape de `a`. El retorno
es un **namedtuple** `SlogdetResult` con campos `sign` y `logabsdet` (accesibles por nombre o por
desempaquetado).

## Los parámetros en detalle

### `a` — la matriz (o pila de matrices)
`array_like` con los **dos últimos ejes cuadrados**: shape `(..., n, n)`. Los ejes anteriores son de
**lote** y `slogdet` se aplica de forma independiente a cada bloque $n\times n$ (ver
[[concepto_shape]]). Igual que `det`, el cálculo es por descomposición **LU**, así que opera siempre
en flotante (entrada entera → cómputo `float64`).

## El caso N-D

Los **dos últimos ejes** son la matriz; **todo lo anterior es lote**. Cada bloque $n\times n$
colapsa a un par escalar `(sign, logabsdet)`, así que **ambas** salidas tienen el shape del lote:

| `a.shape` | `sign.shape` | `logabsdet.shape` | lectura |
|-----------|--------------|-------------------|---------|
| `(n, n)` | `()` escalar | `()` escalar | una sola matriz |
| `(b, n, n)` | `(b,)` | `(b,)` | un par por cada una de las `b` matrices |
| `(b, c, n, n)` | `(b, c)` | `(b, c)` | una rejilla `b×c` de pares |

```python
batch = np.array([[[1., 2.], [3., 4.]],    # det = -2
                  [[2., 0.], [0., 2.]]])   # det =  4
sign, logabsdet = np.linalg.slogdet(batch)
sign        # array([-1.,  1.])         → (2,)
logabsdet   # array([0.6931, 1.3863])   → log(2), log(4)
sign * np.exp(logabsdet)   # array([-2.,  4.])  → reconstruye cada det
```

## Vectorización

Igual que `det`, el soporte `(..., n, n)` es [[concepto_vectorizacion]]: NumPy recorre el lote en C
(LAPACK) en vez de iterar en Python. El bucle equivalente sería:

```python
# Bucle Python: un (sign, logabsdet) por matriz
def slogdet_loop(batch):
    out = [np.linalg.slogdet(M) for M in batch]
    return np.array([s for s, _ in out]), np.array([l for _, l in out])

# Vectorizado: una llamada, dos ndarray alineados con el lote
sign, logabsdet = np.linalg.slogdet(batch)
```

## Valor de retorno

`slogdet` devuelve un **namedtuple de dos elementos** `SlogdetResult(sign, logabsdet)` — hay que
**desempaquetar las dos salidas** (es el error clásico tratarlo como un escalar). Ambas comparten el
shape del lote:

| Campo | shape | dtype | significado |
|-------|-------|-------|-------------|
| `sign` | `(...)` | `float64` (o `complex128` si `a` compleja) | signo del determinante: `-1`, `0` o `+1` (complejo de módulo 1 si `a` es compleja) |
| `logabsdet` | `(...)` | `float64` | $\ln\lvert\det(A)\rvert$ — el logaritmo natural del valor absoluto |

Casos especiales del par, con la **desambiguación de las dos salidas**:

| Situación | `sign` | `logabsdet` | reconstrucción `sign·e^logabsdet` |
|-----------|--------|-------------|-----------------------------------|
| $\det > 0$ | `+1.0` | $\ln(\det)$ | $\det$ |
| $\det < 0$ | `-1.0` | $\ln(\lvert\det\rvert)$ | $\det$ |
| matriz **singular** ($\det = 0$) | `0.0` | `-inf` | `0.0` |

```python
sign, logabsdet = np.linalg.slogdet(np.array([[1., 2.], [3., 4.]]))
sign                        # np.float64(-1.0)
logabsdet                   # np.float64(0.6931...)   = log(2)
sign * np.exp(logabsdet)    # -2.0  → reconstruye det(A)
```

## Casos de uso

### Determinante que desbordaría con `det`
```python
M = np.eye(2000) * 10.0          # det "real" = 10**2000 → inf en det()
sign, logabsdet = np.linalg.slogdet(M)
sign, logabsdet                  # (1.0, 4605.17...)  → estable, sin overflow
```

### Log-verosimilitud gaussiana (donde aparece $\log\det\Sigma$)
La densidad normal multivariante lleva un término $-\tfrac12\log\det\Sigma$. `slogdet` da ese
$\log\det$ **directamente**, sin pasar por el determinante (que para una covarianza grande
desbordaría):

```python
Sigma = np.array([[2.0, 0.3], [0.3, 1.0]])
sign, logdet = np.linalg.slogdet(Sigma)
# log p(x) = -0.5 * (k*log(2π) + logdet + mahalanobis)
assert sign > 0     # una covarianza válida es definida positiva → det > 0
log_det = logdet    # se usa tal cual, sin exponenciar
```

### Detectar singularidad en un lote
```python
batch = np.random.rand(50, 4, 4)
sign, logabsdet = np.linalg.slogdet(batch)
singulares = (sign == 0)          # o logabsdet == -inf
singulares.sum()                  # cuántas matrices del lote son singulares
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Last 2 dimensions of the array must be square` | matriz no cuadrada | reformar a `(..., n, n)` |
| Tratar la salida como un escalar | olvidar que devuelve **dos** valores | desempacar `sign, logabsdet = ...` |
| Reconstruir y volver a desbordar | `sign * np.exp(logabsdet)` con det enorme | trabajar con `logabsdet` sin exponenciar |
| No detectar singularidad | esperar una excepción | comprobar `sign == 0` o `logabsdet == -inf` |
| Confundir `logabsdet` con $\log\det$ con signo | es el log del **valor absoluto** | el signo va aparte, en `sign` |

## Notas relacionadas

- [[concepto_shape]] — los dos últimos ejes son la matriz; el resto es lote
- [[concepto_vectorizacion]] — signo y log de un lote sin bucle (LAPACK)
- [[np.linalg.det]] — el determinante directo, que `slogdet` reemplaza cuando hay riesgo de overflow
- [[np.linalg.inv]] · [[np.linalg.solve]]
