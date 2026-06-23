---
title: np.diagflat — matriz diagonal a partir de la entrada aplanada
aliases:
  - diagflat
  - np.diagflat
tags:
  - numpy
  - api/funcion
  - creacion
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.diagflat — matriz diagonal a partir de la entrada aplanada

`np.diagflat` **siempre construye** una matriz diagonal: toma la entrada, la **aplana** a un vector 1D
(en orden de filas) y coloca esos valores en la diagonal de una matriz cuadrada nueva. Es la variante
de [[np.diag]] dedicada solo a *construir*: a diferencia de `diag`, no es ambivalente —da igual que la
entrada sea 1D, 2D o de cualquier forma, primero la aplana y luego diagonaliza—.

## La idea

La entrada se aplana a $v = [d_0, d_1, \dots, d_{n-1}]$ y se coloca en la diagonal de una matriz
$n \times n$ de ceros:

$$
\text{diagflat}([d_0, d_1, d_2]) = \begin{bmatrix} d_0 & 0 & 0 \\ 0 & d_1 & 0 \\ 0 & 0 & d_2 \end{bmatrix}
$$

Lo distintivo es el aplanado previo: una matriz 2D de entrada **no** se diagonaliza por su diagonal,
sino que se estira a un vector y *todos* sus elementos van a la diagonal del resultado:

$$
\text{diagflat}\!\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\;\xrightarrow{\ \text{aplana}\ }\; [1, 2, 3, 4]
\;\xrightarrow{\ \text{diagonaliza}\ }\;
\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 2 & 0 & 0 \\ 0 & 0 & 3 & 0 \\ 0 & 0 & 0 & 4 \end{bmatrix}
$$

**Mapa de shapes**: si la entrada tiene `size` $= n$, la salida es $(n+|k|,\ n+|k|)$. El tamaño total
manda, no la forma. Ver [[concepto_shape]].

$$
\text{shape cualquiera, size } n \xrightarrow{\ \text{diagflat}\ } (n+|k|,\ n+|k|)
$$

## Firma

```python
np.diagflat(
    v,      # array_like: se aplana a 1D antes de diagonalizar
    k=0,    # int: diagonal donde colocar los valores (0 principal, >0 arriba, <0 abajo)
) -> ndarray
```

## Los parámetros en detalle

### `v` — la entrada (se aplana siempre)
`array_like` de **cualquier forma**. Internamente se hace `np.asarray(v).ravel()`, así que su `size`
(no su shape) determina el orden de la matriz. Este aplanado es justo lo que la distingue de
[[np.diag]], que en 2D *extraería* la diagonal en vez de usar todos los elementos.

```python
np.diagflat([1, 2, 3])
# array([[1, 0, 0],
#        [0, 2, 0],
#        [0, 0, 3]])

np.diagflat([[1, 2], [3, 4]])   # se aplana a [1,2,3,4] → matriz 4×4
# array([[1, 0, 0, 0],
#        [0, 2, 0, 0],
#        [0, 0, 3, 0],
#        [0, 0, 0, 4]])
```

### `k` — diagonal donde colocar los valores
`int` (defecto `0`). Igual que en [[np.diag]]: `0` principal, `k > 0` superdiagonal, `k < 0`
subdiagonal. Desplazar **agranda** la matriz a $(n+|k|, n+|k|)$ para que los valores quepan.

```python
np.diagflat([1, 2], k=1)
# array([[0, 1, 0],
#        [0, 0, 2],
#        [0, 0, 0]])   → 3×3
```

## Casos de uso

### Diagonalizar valores que vienen en una matriz
Cuando los valores a colocar en la diagonal ya están en una estructura 2D y no quieres aplanarlos a
mano:
```python
pesos = np.array([[0.1, 0.2], [0.3, 0.4]])
np.diagflat(pesos)   # 4×4 con los 4 pesos en la diagonal
```

### Construir sin preocuparse por la forma de entrada
`diagflat` es el "construir defensivo": funcione lo que funcione la entrada (lista de listas, array
2D), siempre produce la matriz diagonal esperada, mientras que `np.diag` cambiaría de modo.

## `np.diagflat` vs `np.diag`

| | `np.diagflat(v)` | `np.diag(v)` |
|--|------------------|--------------|
| Entrada 1D | construye diagonal | construye diagonal |
| Entrada 2D | **aplana** y construye (size = $m \cdot n$) | **extrae** la diagonal |
| Modo | siempre **construir** | ambivalente según `ndim` |

Si solo vas a construir y no quieres que la dimensión de la entrada cambie el comportamiento,
`diagflat` es la elección segura.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Matriz enorme inesperada con entrada 2D | se aplanó todo: size $= m \cdot n$ valores en la diagonal | usar [[np.diag]] si solo querías la diagonal de esos datos |
| Esperar extracción | `diagflat` solo **construye** | para extraer usa [[np.diag]] o [[np.diagonal]] |
| Matriz más grande con `k != 0` | el desplazamiento agranda a $(n+|k|)$ | es correcto |

## Notas relacionadas

- [[concepto_shape]] — manda el `size` aplanado, no la forma de entrada
- [[np.diag]] — la versión ambivalente (construye 1D, extrae 2D)
- [[np.diagonal]] — extracción con vista y soporte de lotes N-D
- [[np.eye]] · [[np.identity]] — diagonal constante de unos
