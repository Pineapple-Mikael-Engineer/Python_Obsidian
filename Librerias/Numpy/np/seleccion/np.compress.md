---
title: np.compress — selecciona sub-arrays donde un booleano 1D es True, por eje
aliases:
  - compress
  - np.compress
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.compress — selecciona sub-arrays donde un booleano 1D es True, por eje

`np.compress` **filtra a lo largo de un eje**: recibe un booleano **1D** (`condition`) y se queda
con los sub-arrays (filas, columnas, planos...) de ese eje donde el booleano es `True`, descartando
los demás. Es como una máscara booleana, pero aplicada **por eje** en vez de elemento a elemento: el
eje seleccionado **se reduce** al número de `True`, y los demás ejes quedan intactos. Devuelve una
**copia**.

## La idea en una fórmula

Sobre un eje $p$ de longitud $n_p$, una condición booleana de longitud $n_p$ con $t$ valores `True`
**encoge ese eje a $t$**, dejando el resto del shape igual:

$$ (n_0,\dots,n_{p-1},\,n_p,\,n_{p+1},\dots,n_{k-1}) \ \xrightarrow{\ \text{compress, axis}=p\ }\ (n_0,\dots,n_{p-1},\,t,\,n_{p+1},\dots,n_{k-1}) $$

con $t = \sum_i \texttt{condition}_i$. Por índices, se conservan las posiciones del eje donde la
condición es `True`, en orden:

$$ \text{out}[\dots, j, \dots] = a[\dots, \iota(j), \dots] \quad\text{con}\quad \iota(j) = \text{el } j\text{-ésimo índice donde condition es True} $$

Si `axis=None`, NumPy **aplana** `a` primero y la condición filtra sobre el array plano, devolviendo
un resultado 1D.

## Firma

```python
np.compress(
    condition,    # array_like[bool]: booleano 1D a lo largo del eje
    a,            # array_like: el array de entrada
    axis=None,    # None | int: eje sobre el que filtrar (None = aplana)
    out=None,     # ndarray: destino preasignado opcional
) -> ndarray
```

## Los parámetros en detalle

### `condition` — el booleano 1D
`array_like` de booleanos, **unidimensional**. Su longitud puede ser **menor** que el tamaño del eje
(solo se examinan las primeras posiciones; las que no cubre se descartan) o igual. No se broadcastea:
es estrictamente 1D y se alinea contra el eje elegido.

```python
a = np.array([10, 20, 30, 40])
np.compress([True, False, True], a)   # condition más corta que a: ignora la posición 3
# [10, 30]                            ← solo examina índices 0,1,2
```

### `a` — el array de entrada
`array_like`. No se modifica; el resultado es una **copia**. Puede tener cualquier número de
dimensiones; el filtrado actúa sobre un solo eje.

### `axis` — el eje a filtrar
`None` (defecto) aplana `a` y filtra sobre el array plano → resultado 1D. Un `int` filtra **ese eje**:
con `axis=0` selecciona filas, con `axis=1` columnas, etc. Es el parámetro que diferencia `compress`
de [[np.extract]] (que siempre aplana).

```python
M = np.arange(12).reshape(3, 4)
np.compress([True, False, True], M, axis=0)   # filas 0 y 2
# [[ 0,  1,  2,  3],
#  [ 8,  9, 10, 11]]
np.compress([False, True, True, False], M, axis=1)   # columnas 1 y 2
# [[ 1,  2],
#  [ 5,  6],
#  [ 9, 10]]
```

### `out` — destino preasignado
`ndarray` opcional con el shape exacto del resultado. Evita asignar memoria nueva; rara vez necesario
porque el shape de salida depende del número de `True` (hay que conocerlo de antemano).

## El caso N-D

La regla es mecánica: **solo el eje de `axis` cambia de tamaño** (pasa de $n_p$ a $t$ `True`); todos
los demás ejes se conservan idénticos. Es equivalente a `a[:, ..., cond, ..., :]` con la máscara en
la posición de `axis`, o a `np.take(a, np.nonzero(cond)[0], axis=axis)`.

```python
T = np.arange(24).reshape(2, 3, 4)        # (lote, fila, col)
np.compress([True, False], T, axis=0).shape    # (1, 3, 4)  → un lote
np.compress([True, False, True], T, axis=1).shape  # (2, 2, 4)  → 2 filas por lote
np.compress([True, True, False, False], T, axis=2).shape  # (2, 3, 2)  → 2 columnas
```

Cada llamada deja intactos los ejes que no son `axis` y encoge ese eje al número de `True`.

## Vectorización

`np.compress` evita construir la máscara N-D y el bucle de selección por eje a mano:

```python
# Bucle Python (selección por filas):
out = np.array([fila for fila, keep in zip(M, cond) if keep])

# Vectorizado:
np.compress(cond, M, axis=0)
```

Internamente equivale a indexar con los índices `True` (`np.nonzero(cond)[0]`) a lo largo del eje:
NumPy recorre el eje en C y copia los sub-arrays seleccionados, sin crear listas intermedias. Es la
forma "por eje" del indexado booleano descrito en [[concepto_indexing]].

## Valor de retorno

Siempre un **`ndarray`** (copia, nunca vista). El shape coincide con `a` salvo en el eje filtrado,
que pasa a tener $t$ = nº de `True`. El dtype se conserva.

| `a.shape` | `axis` | `condition` | salida |
|-----------|--------|-------------|--------|
| `(n,)` | `None`/`0` | $t$ True | `(t,)` |
| `(m, n)` | `0` | $t$ True (sobre $m$) | `(t, n)` |
| `(m, n)` | `1` | $t$ True (sobre $n$) | `(m, t)` |
| `(b, m, n)` | `None` | $t$ True (sobre $b\cdot m\cdot n$) | `(t,)` aplanado |
| `(b, m, n)` | `1` | $t$ True (sobre $m$) | `(b, t, n)` |

## Casos de uso

### Filtrar filas de una tabla por una condición precomputada
```python
datos = np.array([[1, 100], [2, 50], [3, 200], [4, 75]])
caros = datos[:, 1] > 90              # [True, False, True, False]
np.compress(caros, datos, axis=0)
# [[  1, 100],
#  [  3, 200]]                        ← solo las filas "caras"
```

### Quedarse con columnas seleccionadas
```python
M = np.arange(12).reshape(3, 4)
np.compress([True, False, False, True], M, axis=1)   # 1ª y 4ª columna
# [[ 0,  3],
#  [ 4,  7],
#  [ 8, 11]]
```

### N-D: descartar lotes de un tensor
```python
imgs = np.arange(2*2*2).reshape(2, 2, 2)   # 2 "imágenes" 2×2
validas = [False, True]
np.compress(validas, imgs, axis=0)
# [[[4, 5],
#   [6, 7]]]                            → shape (1, 2, 2), solo la imagen válida
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado 1D inesperado | se omitió `axis` (defecto `None` aplana) | pasar `axis=0`/`1`/... |
| `condition` 2D | debe ser **1D** | aplanar la condición o usar máscara booleana `a[mask]` |
| Se filtran pocas posiciones | `condition` más corta que el eje | igualar su longitud al tamaño del eje |
| Se esperaba una vista | `compress` devuelve **copia** | asumir copia (igual que el booleano) |

## Notas relacionadas

- [[concepto_indexing]] — la familia booleana vs el filtrado por eje
- [[np.extract]] — el equivalente que **siempre aplana** (sin `axis`)
- [[np.take]] — seleccionar por índices a lo largo de un eje
- [[np.nonzero]] — convierte la condición en los índices que `compress` usa
- [[Librerias/Numpy/np/seleccion/index|selección]] — el resto de la familia
