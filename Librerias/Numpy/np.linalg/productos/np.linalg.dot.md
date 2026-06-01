---
title: np.linalg.dot — Producto matricial (@ / np.matmul / np.dot)
aliases:
  - dot
  - linalg.dot
  - np.linalg.dot
tags:
  - numpy
  - api/funcion
  - algebra/matricial
lib: numpy
mod: np.linalg
tipo: funcion
retorna: ndarray
inplace: false
draft: false
---

# np.linalg.dot — Producto matricial (@ / np.matmul / np.dot)

## ⚠️ Aclaración de nombre

En NumPy **no existe `np.linalg.dot` como producto matricial canónico**. El producto matricial vive en el **namespace raíz** y se expresa con:

- el operador `@` (recomendado, PEP 465),
- la función `np.matmul`,
- la función `np.dot` (más antigua, semántica ligeramente distinta en >2D).

Esta nota documenta el **producto matricial** en general. Para multiplicación elemento a elemento (Hadamard) ver `@` vs `*` y la nota [[np.multiply]].

> El producto matricial **NO es conmutativo**: en general `A @ B != B @ A`.

## Firma de la función

```python
A @ B                       # operador (recomendado)
np.matmul(x1, x2, /, out=None, *, ...) -> ndarray
np.dot(a, b, out=None) -> ndarray
```

## Valor de retorno

Devuelve el producto matricial, sumando sobre la dimensión interior compartida. Para 2D, multiplica filas de `A` por columnas de `B`.

| `A.shape` | `B.shape` | Resultado | Regla |
|-----------|-----------|-----------|-------|
| `(M, K)` | `(K, N)` | `(M, N)` | matricial estándar |
| `(K,)` | `(K,)` | escalar `()` | producto punto (1D·1D) |
| `(M, K)` | `(K,)` | `(M,)` | matriz · vector |
| `(K,)` | `(K, N)` | `(N,)` | vector · matriz |
| `(B, M, K)` | `(B, K, N)` | `(B, M, N)` | lotes de matrices (`matmul`) |

```python
import numpy as np
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

A @ B            # array([[19, 22], [43, 50]])
B @ A            # array([[23, 34], [31, 46]])  → distinto: no conmutativo
```

## Producto matricial vs producto punto

| Operación | Entrada | Suma sobre | Resultado |
|-----------|---------|------------|-----------|
| Producto punto | dos 1D `(K,)` | el eje único | escalar |
| Producto matricial | 2D `(M,K)` × `(K,N)` | dimensión `K` | matriz `(M,N)` |

El requisito siempre es que las dimensiones interiores coincidan: `(M, K) @ (K, N)`. Conviene razonar cada operación en términos de [[concepto_shape|shape]].

## Contraste con multiplicación elemento a elemento

```python
A * B            # Hadamard: array([[ 5, 12], [21, 32]])  (elemento a elemento)
A @ B            # matricial: array([[19, 22], [43, 50]])
```

`*` (y `np.multiply`) operan posición a posición con broadcasting; `@` contrae una dimensión. Son operaciones distintas: ver [[np.multiply]].

## Parámetros en detalle

| Parámetro | Aplica a | Descripción |
|-----------|----------|-------------|
| `x1`, `x2` | `matmul` | operandos; primer y último eje definen la matriz |
| `a`, `b` | `dot` | operandos del producto punto/matricial |
| `out` | ambas | ndarray destino preasignado (opcional) |

### matmul vs dot en N>2D

| Caso | `np.matmul` / `@` | `np.dot` |
|------|-------------------|----------|
| 2D × 2D | producto matricial | producto matricial (igual) |
| Pila ND | broadcasting por lotes de los 2 últimos ejes | producto tensorial (suma último de `a` con penúltimo de `b`) |
| Escalar | **no permitido** | permitido |

```python
P = np.ones((10, 2, 3))
Q = np.ones((10, 3, 4))
(P @ Q).shape    # (10, 2, 4)  → 10 productos matriciales en lote
```

## Casos de uso

### Transformación lineal de un vector

```python
M = np.array([[0, -1],
              [1,  0]])     # rotación 90°
v = np.array([1, 0])
M @ v            # array([0, 1])
```

### Cadena de transformaciones

```python
resultado = A @ B @ C       # se evalúa de izquierda a derecha
```

## Buenas prácticas

1. Usa `@` por defecto: es legible y específico de producto matricial.
2. Usa `np.matmul` cuando necesites `out=` o trabajar con lotes ND.
3. Reserva `np.dot` para producto punto de vectores o compatibilidad antigua.
4. Verifica las dimensiones interiores antes de operar: `A.shape[-1] == B.shape[-2]`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `shapes ... not aligned` | dimensiones interiores no coinciden | asegurar `(M,K)@(K,N)` |
| Esperar `A @ B == B @ A` | producto no conmutativo | respetar el orden |
| Confundir `@` con `*` | `*` es elemento a elemento | usar `@` para matricial |
| `matmul` con escalar | `matmul`/`@` no admite escalares | usar `*` o `np.dot` |

## Notas relacionadas

- [[np.multiply]]
- [[concepto_shape]]
- [[np.linalg.multi_dot]]
- [[np.linalg.matrix_power]]
