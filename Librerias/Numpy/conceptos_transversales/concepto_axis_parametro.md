---
title: Axis — El parámetro que dirige las operaciones por eje
aliases:
  - axis
  - eje
  - parametro axis
tags:
  - numpy
  - concepto
  - reducciones
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_shape
draft: false
---

# Axis — El parámetro que dirige las operaciones por eje

## Definición fundamental

El parámetro **`axis`** indica **a lo largo de qué dimensión** se aplica una operación. Aparece en casi todas las reducciones y manipulaciones (`sum`, `mean`, `max`, `concatenate`, `sort`...). Es el control direccional de NumPy, el que conecta cada operación con un eje concreto de un [[concepto_ndarray|tensor]].

**Característica esencial:** `axis=k` significa "recorrer y **colapsar** el eje `k`", dejando intactos los demás. El eje sobre el que operas es el que **desaparece** del [[concepto_shape|shape]] resultado.

## Por qué existe

Una matriz `(2, 3)` se puede sumar de tres formas distintas: bajando por columnas, a lo largo de cada fila, o todo a la vez. Sin un parámetro que elija la dirección, NumPy tendría que ofrecer una función por cada combinación (`sum_columnas`, `sum_filas`...). `axis` unifica todas esas variantes en un único argumento: **una operación, un eje, una dirección**.

```python
import numpy as np
M = np.arange(6).reshape(2, 3)   # [[0,1,2],[3,4,5]]

M.sum(axis=0)   # baja por columnas   → [3, 5, 7]
M.sum(axis=1)   # recorre cada fila   → [3, 12]
M.sum()         # todo                → 15
```

## La regla central

> El eje indicado en `axis` es el que se **consume**. El shape resultado es el shape original sin esa posición.

| Shape entrada | `axis` | Qué se colapsa | Shape salida |
|---------------|--------|----------------|--------------|
| `(2, 3)` | `0` | filas | `(3,)` |
| `(2, 3)` | `1` | columnas | `(2,)` |
| `(2, 3)` | `None` | todo | `()` escalar |
| `(2, 3, 4)` | `0` | primer eje | `(3, 4)` |
| `(2, 3, 4)` | `1` | eje medio | `(2, 4)` |
| `(2, 3, 4)` | `2` | último eje | `(2, 3)` |

### El mapa de shapes formal

Para una reducción sobre el eje $p$ de un tensor de shape $(n_0,\dots,n_k)$, ese eje **se elimina** del shape:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

Con una **tupla de ejes** `axis=(p,q)` desaparecen **ambos** a la vez:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{axis}=(p,q)\ }\ (\dots,\,n_{p-1},\,n_{p+1},\dots,\,n_{q-1},\,n_{q+1},\dots) $$

Con `keepdims=True`, los ejes reducidos **no desaparecen**: quedan con tamaño $1$ en su posición original:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{axis}=p,\ \text{keepdims}\ }\ (n_0,\dots,n_{p-1},\,1,\,n_{p+1},\dots,n_k) $$

Y el caso `axis=None` contrae **todos** los ejes a un escalar de shape `()`.

## Por qué confunde (y cómo fijar la intuición)

La trampa: `axis=0` no significa "por filas" en el sentido de "una operación por fila". Significa **moverse a lo largo del eje 0** (hacia abajo, entre filas), produciendo un resultado **por columna**.

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])

M.sum(axis=0)   # [5, 7, 9]   → suma BAJANDO por cada columna (colapsa filas)
M.sum(axis=1)   # [6, 15]     → suma A LO LARGO de cada fila (colapsa columnas)
M.sum()         # 21          → colapsa todo
```

**Regla mnemotécnica:** "el eje que pongo en `axis` es el que se va". `axis=0` borra la dimensión de las filas → quedan las columnas.

## Visualización direccional

```
M (shape 2x3):          axis=0  ↓ (recorre filas)        axis=1  → (recorre columnas)
                        colapsa el eje 0                  colapsa el eje 1
  col0 col1 col2
  [ 1    2    3 ]       resultado: [5, 7, 9]  shape (3,)  resultado: [6, 15] shape (2,)
  [ 4    5    6 ]
```

## El truco de `keepdims`

Tras reducir, el eje desaparece. `keepdims=True` lo conserva con tamaño 1, lo que mantiene la compatibilidad para [[concepto_broadcasting|broadcasting]] posterior.

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])

s = M.sum(axis=1)                 # shape (2,)    → [6, 15]
sk = M.sum(axis=1, keepdims=True) # shape (2, 1)  → [[6],[15]]

# Normalizar cada fila por su suma: necesita (2,1) para alinear con (2,3)
M / sk     # OK por broadcasting
# M / s    # ValueError: (2,3) vs (2,) no alinea
```

## Ejemplos progresivos

### Nivel 1: reducciones en 2D

```python
M = np.arange(6).reshape(2, 3)   # [[0,1,2],[3,4,5]]

M.max(axis=0)   # [3, 4, 5]   → máximo por columna
M.max(axis=1)   # [2, 5]      → máximo por fila
M.mean()        # 2.5         → media global
```

### Nivel 2: `argmax` y la posición a lo largo del eje

```python
M = np.array([[1, 9, 3],
              [7, 2, 8]])

M.argmax(axis=0)  # [1, 0, 1]  → índice de fila con el max en cada columna
M.argmax(axis=1)  # [1, 2]     → índice de columna con el max en cada fila
```

### Nivel 3: axis negativo y en 3D

`axis=-1` es siempre el último eje, útil cuando el `ndim` varía.

```python
T = np.ones((2, 3, 4))

T.sum(axis=-1).shape   # (2, 3)   → colapsa el último eje (equivale a axis=2)
T.sum(axis=0).shape    # (3, 4)
T.sum(axis=(0, 2)).shape  # (3,)  → axis acepta tupla: colapsa varios ejes
```

## Operaciones donde `axis` no reduce, sino que dirige

No todas las operaciones con `axis` colapsan un eje; algunas lo usan como dirección:

| Operación | Rol de `axis` | Efecto |
|-----------|---------------|--------|
| `sum`, `mean`, `max` | reduce | el eje desaparece |
| `cumsum`, `cumprod` | acumula a lo largo | el shape se conserva |
| `sort`, `argsort` | ordena a lo largo | el shape se conserva |
| `concatenate` | une a lo largo | crece el eje indicado |
| `stack` | crea un eje nuevo | aparece un eje extra |
| `flip` | invierte a lo largo | el shape se conserva |

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

np.concatenate([A, B], axis=0).shape   # (4, 2)  → apila filas
np.concatenate([A, B], axis=1).shape   # (2, 4)  → apila columnas
```

## Casos que fallan (errores típicos)

### Error 1: confundir el sentido de axis=0 / axis=1

```python
M = np.array([[1, 2], [3, 4]])
# Quiero la media de cada fila → es axis=1, no axis=0
M.mean(axis=1)   # [1.5, 3.5]  correcto
M.mean(axis=0)   # [2.0, 3.0]  media por columna (no era esto)
```

### Error 2: axis fuera de rango

```python
M = np.ones((2, 3))   # ndim = 2, ejes válidos: 0, 1, -1, -2
M.sum(axis=2)
# AxisError: axis 2 is out of bounds for array of dimension 2
```

### Error 3: perder el eje y romper un broadcasting posterior

```python
M = np.ones((3, 4))
medias = M.mean(axis=1)              # shape (3,)  → no alinea con (3,4)
# M - medias  → ValueError
M - M.mean(axis=1, keepdims=True)    # OK con keepdims (3,1)
```

## Relación con otros conceptos

- [[concepto_ndarray]]
- [[concepto_shape]]
- [[concepto_broadcasting]]
- [[concepto_vectorizacion]]
- [[np.sum]]
- [[np.argmax]]
