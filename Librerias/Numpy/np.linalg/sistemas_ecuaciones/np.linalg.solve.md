---
title: np.linalg.solve — resuelve el sistema lineal Ax = b con A cuadrada
aliases:
  - solve
  - linalg.solve
  - np.linalg.solve
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

# np.linalg.solve — resuelve el sistema lineal $A\mathbf{x}=\mathbf{b}$

`np.linalg.solve` halla el vector $\mathbf{x}$ que satisface $A\mathbf{x}=\mathbf{b}$ cuando $A$ es
**cuadrada e invertible**. Es la herramienta canónica para resolver un sistema determinado: en vez de
calcular la inversa y multiplicar, factoriza $A$ una sola vez y sustituye. La pregunta que responde no
es "¿cuál es $A^{-1}$?" sino directamente "¿qué $\mathbf{x}$ resuelve el sistema?".

> [!regla] Regla de oro: `solve(A, b)`, nunca `inv(A) @ b`
> Para resolver $A\mathbf{x}=\mathbf{b}$ **siempre** se usa `np.linalg.solve(A, b)`, no
> `np.linalg.inv(A) @ b`. Es **más rápido** (una factorización LU en vez de invertir + multiplicar) y
> **numéricamente más estable** (no propaga el error de calcular la inversa explícitamente). Invertir
> solo tiene sentido si necesitas $A^{-1}$ como objeto en sí mismo, cosa rarísima. Ver [[np.linalg.inv]].

## La idea en una fórmula

El sistema lineal y su solución formal:

$$
A\mathbf{x}=\mathbf{b} \qquad\Longrightarrow\qquad \mathbf{x}=A^{-1}\mathbf{b}
\quad\text{(conceptual; NumPy no invierte: factoriza)}
$$

Internamente NumPy aplica una **factorización LU con pivoteo** $PA=LU$ y resuelve por sustitución hacia
adelante y hacia atrás, lo que cuesta $\mathcal{O}(n^3)$ una vez y $\mathcal{O}(n^2)$ por cada término
independiente extra.

**El mapa de shapes** — $A$ ocupa los dos últimos ejes (la matriz $n\times n$); $\mathbf{b}$ es un
vector $(\dots,n)$ o un bloque de varios lados $(\dots,n,k)$:

$$
(\dots,\,n,\,n)\ ,\ (\dots,\,n)\ \xrightarrow{\ \text{solve}\ }\ (\dots,\,n)
$$
$$
(\dots,\,n,\,n)\ ,\ (\dots,\,n,\,k)\ \xrightarrow{\ \text{solve}\ }\ (\dots,\,n,\,k)
\qquad (k\ \text{lados a la vez})
$$

Los `…` previos son **ejes de lote** que se alinean por broadcasting (ver [[concepto_shape]]): una pila
de sistemas $A_i\mathbf{x}_i=\mathbf{b}_i$ se resuelve de golpe. El eje de tamaño $n$ común a $A$ y
$\mathbf{b}$ es el que se "contrae" al resolver.

```text
┌ 3 1 ┐ ┌ x0 ┐   ┌ 9 ┐        3·x0 + 1·x1 = 9
│ 1 2 │ │ x1 │ = │ 8 │   →    1·x0 + 2·x1 = 8   →   x = [2, 3]
└─────┘ └────┘   └───┘
```

## Firma

```python
np.linalg.solve(a, b) -> ndarray
```

## Los parámetros en detalle

### `a` — matriz de coeficientes
`array_like` de shape `(..., M, M)`. Debe ser **cuadrada** (los dos últimos ejes iguales) y **no
singular** (determinante distinto de cero). Los ejes anteriores son lote. Si `a` no es cuadrada, usa
[[np.linalg.lstsq]]; si es singular, lanza `LinAlgError`.

### `b` — término(s) independiente(s)
`array_like` de shape `(..., M)` (un solo lado) o `(..., M, K)` (`K` lados con la misma `a`). El
[[concepto_shape|shape]] del resultado **sigue al de `b`**: vector si `b` es vector, matriz si `b` trae
varias columnas.

```python
A = np.array([[2., 0.],
              [0., 4.]])
B = np.array([[2., 6.],
              [4., 8.]])      # dos lados a la vez (dos columnas)
np.linalg.solve(A, B)        # [[1., 3.], [1., 2.]]  → una columna por sistema
```

> `solve` no tiene parámetros opcionales (`out`, `dtype`, etc.). El control fino del cómputo no se
> expone; para variantes (triangular, definida positiva) hay que recurrir a `scipy.linalg`.

## El caso N-D

Con ejes de lote, `solve` resuelve **una pila de sistemas** sin bucle. Los dos últimos ejes de `a` son
la matriz; los anteriores se alinean con los de `b` por broadcasting:

| `a.shape` | `b.shape` | `x.shape` | qué pasa |
|-----------|-----------|-----------|----------|
| `(M, M)` | `(M,)` | `(M,)` | un sistema, un lado |
| `(M, M)` | `(M, K)` | `(M, K)` | `K` lados, misma matriz (una sola LU) |
| `(B, M, M)` | `(B, M)` | `(B, M)` | **lote**: `B` sistemas, cada uno su matriz |
| `(B, M, M)` | `(M,)` | `(B, M)` | el mismo `b` resuelto contra cada `A` del lote |

```python
A = np.random.rand(8, 3, 3) + np.eye(3)   # 8 matrices 3x3 (invertibles)
b = np.random.rand(8, 3)                  # 8 lados
x = np.linalg.solve(A, b)
x.shape                                    # (8, 3)  → 8 soluciones, sin bucle
np.allclose(np.einsum('bij,bj->bi', A, x), b)   # True
```

## Vectorización

El lote de `solve` es [[concepto_vectorizacion|vectorización]] pura: resolver muchos sistemas sin
recorrer Python, delegando cada factorización en LAPACK (la biblioteca numérica que NumPy usa por debajo).

```python
# Bucle Python: una llamada a solve por sistema del lote
def batch_solve(A, b):
    out = np.empty_like(b)
    for i in range(A.shape[0]):
        out[i] = np.linalg.solve(A[i], b[i])
    return out

# Vectorizado: NumPy recorre el lote en C / LAPACK
np.linalg.solve(A, b)
```

Mismo resultado; la versión vectorizada evita `A.shape[0]` saltos al intérprete. Y recuerda: incluso
para un solo sistema, `solve(A, b)` ya está vectorizado frente a la receta ingenua `inv(A) @ b`.

## Valor de retorno

Devuelve **siempre** un `ndarray` `x` con el shape de `b` (nunca una tupla, a diferencia de
[[np.linalg.lstsq]]):

| `a` | `b` | `x` (shape) | tipo |
|-----|-----|-------------|------|
| `(M, M)` | `(M,)` | `(M,)` | `ndarray` |
| `(M, M)` | `(M, K)` | `(M, K)` | `ndarray` |
| `(..., M, M)` | `(..., M)` | `(..., M)` | `ndarray` |
| singular | cualquiera | — | lanza `LinAlgError` |

- El `dtype` se **promueve a punto flotante**: enteros de entrada salen como `float64` (la solución de un
  sistema entero no es entera en general). Entradas complejas conservan `complex`.

```python
A = np.array([[3., 1.],
              [1., 2.]])
b = np.array([9., 8.])
x = np.linalg.solve(A, b)
x                  # [2., 3.]
A @ x              # [9., 8.]  → recupera b
```

## Casos de uso

### Sistema 3×3 determinado
```python
A = np.array([[1., 2., 3.],
              [2., 5., 3.],
              [1., 0., 8.]])
b = np.array([6., 4., 9.])
np.linalg.solve(A, b)   # solución única del sistema
```

### Varios términos independientes con la misma matriz
```python
A = np.array([[4., 3.],
              [6., 3.]])
B = np.column_stack([[7., 9.], [1., 3.]])
np.linalg.solve(A, B)   # cada columna de la salida resuelve una columna de B
```
Una sola factorización LU sirve para todas las columnas: mucho más barato que resolver una por una.

### Lote N-D de sistemas
```python
A = np.tile(np.array([[2., 1.], [1., 3.]]), (5, 1, 1))  # (5, 2, 2)
b = np.random.rand(5, 2)
np.linalg.solve(A, b).shape   # (5, 2)  → 5 sistemas resueltos a la vez
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `LinAlgError: Singular matrix` | `a` no invertible (det = 0) | revisar el sistema; usar [[np.linalg.lstsq]] |
| `LinAlgError: Last 2 dimensions of the array must be square` | `a` no cuadrada | usar `lstsq` para sistemas rectangulares |
| Usar `inv(A) @ b` | costumbre | **siempre** `solve(A, b)`: más rápido y estable |
| `ValueError` de dimensiones | shapes de `a` y `b` incompatibles | alinear: `a` `(M, M)`, `b` `(M,)` o `(M, K)` |
| Resultado inestable | `a` mal condicionada | comprobar `np.linalg.cond(a)` antes de confiar en `x` |

## Notas relacionadas

- [[concepto_shape]] — razonar el sistema como una operación sobre los dos últimos ejes
- [[concepto_vectorizacion]] — el lote de sistemas sin bucle (LAPACK)
- [[np.linalg.inv]] — la inversa; casi nunca la quieres para resolver
- [[np.linalg.lstsq]] — cuando `A` no es cuadrada o es singular (mínimos cuadrados)
- [[np.linalg.tensorsolve]] — la versión tensorial N-D
- [[index]] — sistemas de ecuaciones
