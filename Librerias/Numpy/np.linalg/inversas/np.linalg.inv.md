---
title: np.linalg.inv — inversa de una matriz cuadrada
aliases:
  - inv
  - linalg.inv
  - np.linalg.inv
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.linalg.inv — inversa de una matriz cuadrada

`np.linalg.inv` calcula la **inversa** $A^{-1}$ de una matriz cuadrada: la única matriz que cumple
$A A^{-1} = A^{-1} A = I$ (la identidad). Es la operación que "deshace" la transformación lineal de
$A$. Existe solo si $A$ es **cuadrada** y **no singular** ($\det A \neq 0$); si no, lanza
`LinAlgError`. La pregunta clave al usarla no es "¿la calculo?", sino **"¿de verdad necesito la
inversa explícita, o solo quiero resolver un sistema?"** (ver el aviso de abajo).

> [!danger] Para resolver $Ax=b$ usa [[np.linalg.solve]], NO `inv(A) @ b`
> Casi nunca necesitas la inversa explícita. Si tu objetivo es resolver el sistema $Ax = b$,
> `np.linalg.solve(A, b)` es **más rápido** (factoriza una vez, sin construir la inversa entera) y
> **numéricamente más estable** (acumula menos error de redondeo). Reserva `inv` para cuando de
> verdad necesites la matriz $A^{-1}$ como objeto (covarianzas, transformaciones reutilizadas).

## La idea en una fórmula

La inversa es el elemento neutro del producto matricial: deshace a $A$. Para $A$ cuadrada de shape
$(n, n)$,

$$
A A^{-1} = A^{-1} A = I_n
$$

donde $I_n$ es la identidad $n \times n$. El cómputo no es la fórmula de adjuntos/determinante (que
es inestable), sino una **factorización LU** con sustitución.

**El mapa de shapes** (entrada → salida, incluido el caso por lotes N-D):

$$
(\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}},\, n,\, n)\ \xrightarrow{\ \text{inv}\ }\ (\underbrace{n_0,\dots,n_{k-1}}_{\text{lote}},\, n,\, n)
$$

Los **dos últimos ejes** forman la matriz cuadrada que se invierte; los `…` anteriores son ejes de
lote que se conservan tal cual. El shape **no cambia**: invertir es un mapa $(\dots,n,n) \to
(\dots,n,n)$ que reemplaza cada matriz por su inversa.

## Firma

```python
np.linalg.inv(a) -> ndarray
```

## Los parámetros en detalle

### `a` — la matriz (o pila de matrices) a invertir
`array_like` de shape `(..., n, n)`. El **último par de ejes** debe formar una matriz cuadrada; el
[[concepto_shape|shape]] decide si se invierte una sola matriz o una pila entera. Su `dtype` se
promueve a flotante (`float64` o `complex128`) porque la inversa rara vez es entera.

```python
A = np.array([[1., 2.], [3., 4.]])
np.linalg.inv(A).shape       # (2, 2)  → una sola matriz

pila = np.random.rand(5, 3, 3)
np.linalg.inv(pila).shape    # (5, 3, 3)  → 5 inversas de 3×3, sin bucle
```

No hay más parámetros: `inv` no acepta `out`, `rcond` ni tolerancias. Si la matriz puede ser
singular o rectangular, esa es justo la frontera con [[np.linalg.pinv]].

## El caso N-D

En 2D es la inversa de toda la vida. En **N-D**, `inv` trata los **dos últimos ejes** como la
matriz cuadrada y **todos los anteriores como un lote** (batch) que se procesa en paralelo:

| `a.shape` | salida | lectura |
|-----------|--------|---------|
| `(n, n)` | `(n, n)` | una inversa |
| `(k, n, n)` | `(k, n, n)` | `k` inversas independientes |
| `(b, k, n, n)` | `(b, k, n, n)` | lote 2D de inversas |
| `(m, n)` con `m≠n` | — | `LinAlgError` (no cuadrada) |

```python
T = np.random.rand(8, 3, 3)   # 8 matrices 3×3
inv_T = np.linalg.inv(T)
inv_T.shape                   # (8, 3, 3)
(T @ inv_T)[0]                # ≈ I₃ (la inversa de la matriz 0)
```
Cada matriz del lote se invierte por separado; si **una sola** es singular, la llamada entera falla.

## Vectorización

El caso por lotes es [[concepto_vectorizacion]] puro: invertir muchas matrices **sin bucle Python**,
delegando en LAPACK. Las dos versiones dan lo mismo, pero la vectorizada recorre el lote en código
compilado:

```python
# Bucle Python: una inversa por elemento del lote
def batch_inv(T):
    out = np.empty_like(T)
    for i in range(T.shape[0]):
        out[i] = np.linalg.inv(T[i])
    return out

# Vectorizado: NumPy recorre el lote en C / LAPACK
np.linalg.inv(T)
```
Mismo resultado; la versión vectorizada evita `T.shape[0]` saltos al intérprete.

## Valor de retorno

| Entrada (shape, dtype) | salida | tipo |
|---|---|---|
| `(n, n)` real no singular | `(n, n)` | `ndarray` `float64` |
| `(n, n)` complejo | `(n, n)` | `ndarray` `complex128` |
| `(..., n, n)` pila | `(..., n, n)` | `ndarray` |
| singular | — | lanza `LinAlgError: Singular matrix` |
| no cuadrada | — | lanza `LinAlgError: Last 2 dimensions must be square` |

El resultado **siempre es flotante** (o complejo), aunque la entrada sea entera. El shape coincide
con el de la entrada.

## Casos de uso

### Inversa de una matriz de coeficientes
```python
A = np.array([[2., 1.], [1., 3.]])
Ainv = np.linalg.inv(A)
Ainv               # [[ 0.6, -0.2], [-0.2,  0.4]]
A @ Ainv           # [[1., 0.], [0., 1.]]  → identidad (salvo error numérico)
```

### Comprobar inversibilidad antes de invertir
```python
A = np.array([[1., 2.], [2., 4.]])   # filas proporcionales → singular
np.linalg.det(A)                     # 0.0  → no invertible
# np.linalg.inv(A)                   # LinAlgError: Singular matrix
np.linalg.cond(A)                    # enorme → aviso de inestabilidad
```

### Pila N-D: invertir muchas matrices a la vez
```python
np.random.seed(0)
T = np.random.rand(4, 2, 2)     # 4 matrices 2×2
inv_T = np.linalg.inv(T)
inv_T.shape                     # (4, 2, 2)
np.allclose(T @ inv_T, np.eye(2))   # True → cada par A·A⁻¹ es la identidad
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Singular matrix` | determinante = 0 (filas/columnas dependientes) | usar [[np.linalg.pinv]] o revisar el sistema |
| `LinAlgError: Last 2 dimensions must be square` | matriz no cuadrada | usar `pinv` para rectangulares |
| Lento e inestable al resolver sistemas | usar `inv(A) @ b` | usar `solve(A, b)` |
| Resultado impreciso | matriz mal condicionada (`cond` alto) | reformular; preferir `solve`/`lstsq` |
| Una inversa falla en un lote correcto | **una** matriz del lote es singular | validar cada matriz antes de apilar |

## Notas relacionadas

- [[np.linalg.solve]] — resolver $Ax=b$ sin construir la inversa (el camino recomendado)
- [[np.linalg.pinv]] — pseudoinversa para matrices no cuadradas o singulares
- [[np.linalg.det]] · [[np.linalg.tensorinv]]
- [[concepto_shape]] — el mapa `(...,n,n) → (...,n,n)`
