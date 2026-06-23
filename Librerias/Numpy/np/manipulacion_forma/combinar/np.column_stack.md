---
title: np.column_stack — apila vectores 1D como columnas
aliases:
  - column_stack
  - np.column_stack
  - apilar columnas
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

# np.column_stack — apila vectores 1D como columnas

`np.column_stack` toma una secuencia de **vectores 1D** y los pone uno al lado de otro como **columnas** de una matriz 2D. Es el atajo que resuelve la trampa de [[np.hstack]], que con vectores 1D los aplana en vez de formar columnas. Internamente promueve cada `(n,)` a una columna `(n, 1)` y luego concatena por el eje 1. Es el patrón clásico para construir una matriz de datos a partir de vectores de características.

## La idea en una fórmula

Cada vector 1D de longitud $n$ se convierte en columna `(n, 1)` y se concatena por el eje 1:

$$
\underbrace{(n,),\;\dots,\;(n,)}_{r\ \text{vectores}}\;\xrightarrow{\ \text{column\_stack}\ }\;(n,\,r)
$$

Cada uno de los $r$ vectores es una columna; el eje 1 mide $r$. Los arrays ya 2D se concatenan por el eje 1 tal cual (se comporta como hstack para ellos).

$$
\begin{bmatrix} 1 \\ 2 \\ 3 \end{bmatrix},\;\begin{bmatrix} 4 \\ 5 \\ 6 \end{bmatrix}\;\xrightarrow{\ \text{column\_stack}\ }\;\begin{bmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{bmatrix}\qquad (3,),(3,)\to(3,2)
$$

## La diferencia con hstack

Es justo el caso que hstack hace mal:

```python
x = np.array([1, 2, 3]); y = np.array([4, 5, 6])
np.hstack((x, y))         # [1 2 3 4 5 6]   → (6,)   aplana
np.column_stack((x, y))   # [[1,4],[2,5],[3,6]]  → (3, 2)  columnas
```

## Firma

```python
np.column_stack(
    tup,   # secuencia de array_like (1D o 2D)
) -> ndarray
```

## Los parámetros en detalle

### `tup` — la secuencia de arrays
Tupla o lista de `array_like` 1D o 2D. Cada 1D de longitud $n$ se trata como columna `(n, 1)`; los 2D se dejan igual. **Todos deben coincidir en la longitud del eje 0** (mismo número de filas). Mezclar 1D y 2D del mismo nº de filas es válido.

## El caso N-D

`column_stack` es 1D/2D por diseño: equivale a `hstack` tras convertir los 1D en columnas. Para tensores N-D no es la herramienta (usa [[np.concatenate]] o [[np.stack]]).

| Entrada | Salida | Equivale a |
|---|---|---|
| tres `(3,)` | `(3,3)` | `stack(axis=1)` |
| `(3,)`, `(3,2)` | `(3,3)` | `hstack` tras promover el 1D |
| dos `(3,2)` | `(3,4)` | `hstack` |

```python
np.column_stack((x, y))      # vectores 1D como columnas
np.stack((x, y), axis=1)     # equivalente si todas son 1D del mismo largo
```

## Vectorización

Promueve los 1D a `(n, 1)` y concatena por el eje 1 en una sola pasada, reservando el buffer `(n, r)` y copiando cada columna. Evita el `hstack` + `reshape` manual y el bucle de copia ([[concepto_vectorizacion]]).

## Valor de retorno

Un **nuevo** `ndarray` (copia) 2D de shape `(n, r)` para $r$ vectores de longitud $n$. dtype: promoción común de las entradas.

## Casos de uso

### Construir una matriz de diseño desde variables
```python
edad = np.array([25, 30, 45])
ingreso = np.array([30000, 45000, 80000])
X = np.column_stack((edad, ingreso))   # (3, 2)  → cada variable una columna
```

### Emparejar coordenadas X, Y
```python
xs = np.array([0, 1, 2]); ys = np.array([9, 8, 7])
puntos = np.column_stack((xs, ys))     # cada fila es un punto (x, y), (3, 2)
```

### Mezclar un vector con una matriz (mismo nº de filas)
```python
v = np.array([1, 2, 3])          # (3,)
M = np.array([[4, 5], [6, 7], [8, 9]])   # (3, 2)
np.column_stack((v, M))          # (3, 3)  → v se vuelve la primera columna
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| Resultado 1D inesperado | se usó [[np.hstack]] con vectores 1D | usar `column_stack` |
| `dimensions must match` | longitudes (nº de filas) distintas | igualar el largo de los vectores |
| Querías profundidad, no columnas | column_stack une por el eje 1 | usar [[np.dstack]] |

## Notas relacionadas

- [[concepto_shape]] — el vector `(n,)` frente a la columna `(n, 1)`
- [[np.hstack]] — el atajo que aplana los 1D (el problema que esto resuelve)
- [[np.vstack]] — el equivalente por filas
- [[np.stack]] · [[np.concatenate]] · [[np.dstack]] — las funciones base y hermanas
