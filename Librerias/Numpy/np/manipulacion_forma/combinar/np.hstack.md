---
title: np.hstack — apila por columnas (eje 1), atajo de concatenate
aliases:
  - hstack
  - np.hstack
  - apilar horizontal
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.hstack — apila por columnas (eje 1), atajo de concatenate

`np.hstack` une una secuencia de arrays **a lo largo del eje 1** (las columnas) para arrays 2D o más. Es un **atajo de [[np.concatenate]]**, pero con una trampa de dimensión: para arrays **1D une por el eje 0** (no hay eje 1 en un vector), de modo que dos `(3,)` dan `(6,)` y no columnas. Es la forma de "crecer a lo ancho": añadir columnas a una matriz.

## La idea en una fórmula

Para 2D+, concatena por el eje 1, que se **suma**; para 1D, por el eje 0:

$$
(m,\,a),(m,\,b)\;\xrightarrow{\ \text{hstack, 2D}\ }\;(m,\,a+b)\qquad\qquad (a,),(b,)\;\xrightarrow{\ \text{hstack, 1D}\ }\;(a+b,)
$$

Es decir, `axis = 1` si `ndim >= 2`, y `axis = 0` si `ndim == 1`. En 2D, pega bloques uno al lado del otro:

$$
\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix},\;\begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix}\;\xrightarrow{\ \text{hstack}\ }\;\begin{bmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}\qquad (3,1),(3,1)\to(3,2)
$$

## El caso 1D (cuidado)

Con vectores 1D, hstack **aplana** (une en eje 0), no crea columnas:

```python
np.hstack((np.array([1, 2]), np.array([3, 4])))   # [1 2 3 4]  → (4,)
```

Para tratar vectores 1D **como columnas**, usa [[np.column_stack]].

## Firma

```python
np.hstack(
    tup,         # secuencia de array_like
    *,
    dtype=None,  # dtype: tipo del resultado (NumPy reciente)
    casting="same_kind",
) -> ndarray
```

## Los parámetros en detalle

### `tup` — la secuencia de arrays
Tupla o lista de `array_like`. En 2D deben coincidir en el número de **filas** (eje 0); en 1D, no hay restricción de shape salvo ser 1D. El eje de unión depende del `ndim`.

### `dtype` / `casting`
Fuerzan el [[concepto_dtype|dtype]] de salida y la regla de conversión, igual que en [[np.concatenate]].

## El caso N-D

| Entrada | Eje de unión | Salida | Equivale a |
|---|---|---|---|
| dos `(3,)` | 0 (1D) | `(6,)` | `concatenate(axis=0)` |
| `(2,3)`, `(2,2)` | 1 | `(2,5)` | `concatenate(axis=1)` |
| `(2,3,4)`, `(2,5,4)` | 1 | `(2,8,4)` | `concatenate(axis=1)` |

```python
np.hstack((a, b))                # 1 si 2D+, 0 si 1D
np.concatenate((a, b), axis=1)   # equivalente para arrays 2D+
```

## Vectorización

Como atajo de concatenate, reserva el buffer una vez y copia cada bloque en su banda de columnas. El antipatrón es apilar en bucle: acumula en una lista y une una vez ([[concepto_vectorizacion]]).

## Valor de retorno

Un **nuevo** `ndarray` (copia). Para 2D+ crece el eje 1; para 1D, el eje 0. dtype: promoción común (o el forzado).

## Casos de uso

### Añadir columnas a una matriz de diseño
```python
X = np.ones((100, 3))
extra = np.random.rand(100, 2)
X = np.hstack((X, extra))      # (100, 5)
```

### Concatenar tramos de una señal 1D
```python
señal = np.hstack((tramo1, tramo2, tramo3))   # une en eje 0
```

### N-D: crecer el eje central de un tensor
```python
A = np.zeros((2, 3, 4)); B = np.zeros((2, 5, 4))
np.hstack((A, B)).shape        # (2, 8, 4)  → concatenate(axis=1)
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| Vectores 1D se aplanan en vez de formar columnas | hstack une 1D por el eje 0 | usar [[np.column_stack]] |
| `dimensions ... must match` | nº de filas distinto en 2D | igualar el eje 0 |
| Eje de unión inesperado | depende de `ndim` (0 en 1D, 1 en 2D+) | para control explícito, [[np.concatenate]] |

## Notas relacionadas

- [[concepto_shape]] — por qué 1D no tiene eje de columnas
- [[np.concatenate]] — la función base (hstack = `axis=1` en 2D+)
- [[np.vstack]] — el equivalente por filas
- [[np.column_stack]] — apilar vectores 1D como columnas de verdad
