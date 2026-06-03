---
title: np.linalg.norm — Norma de vector o matriz
aliases:
  - norm
  - linalg.norm
  - np.linalg.norm
tags:
  - numpy
  - api/funcion
  - algebra/vectorial

# --- Clasificación ---
lib: numpy
mod: np.linalg
tipo: funcion

# --- Comportamiento ---
retorna: float o ndarray
inplace: false

draft: false
---

# np.linalg.norm — Norma de vector o matriz

## Firma de la función

```python
np.linalg.norm(
    x,
    ord=None,
    axis=None,
    keepdims=False
) -> float | ndarray
```

## Valor de retorno

Devuelve la **magnitud** de `x` según la norma elegida por `ord`. Si `axis=None` y `x` es 1D o 2D, devuelve un escalar (`float`); con `axis` calcula la norma a lo largo de ese eje y devuelve un `ndarray`.

| Entrada | `axis` | `ord` | Salida |
|---------|--------|-------|--------|
| `(n,)` | `None` | `None` (=2) | escalar (norma euclídea) |
| `(m, n)` | `None` | `None` (=`'fro'`) | escalar (Frobenius) |
| `(m, n)` | `0` o `1` | norma de vector | `ndarray` (norma por columna/fila) |
| `(m, n)` | `None` | `2` | escalar (norma espectral) |

```python
import numpy as np
v = np.array([3, 4])
np.linalg.norm(v)        # 5.0  → euclídea (sqrt(9+16))
np.linalg.norm(v, ord=1) # 7.0  → suma de |componentes|
```

## Parámetros en detalle

### `x` — array de entrada

Vector (1D) o matriz (2D). La interpretación de `ord` depende de la dimensión de `x`.

### `ord` — tipo de norma

El mismo valor significa cosas distintas según `x` sea vector o matriz. Por defecto `None` da la euclídea (vectores) o la de Frobenius (matrices).

| `ord` | Vector (1D) | Matriz (2D) |
|-------|-------------|-------------|
| `None` | euclídea (L2) | Frobenius |
| `2` | euclídea (L2) | norma espectral (mayor valor singular) |
| `1` | suma de `|x_i|` (L1) | máxima suma de columna |
| `np.inf` | máximo `|x_i|` | máxima suma de fila |
| `-np.inf` | mínimo `|x_i|` | mínima suma de fila |
| `'fro'` | — | Frobenius (raíz de la suma de cuadrados) |
| `'nuc'` | — | nuclear (suma de valores singulares) |
| `0` | nº de elementos no nulos | — |

```python
M = np.array([[1, 2], [3, 4]])
np.linalg.norm(M)           # 5.477...  → Frobenius
np.linalg.norm(M, ord='nuc')# 5.830...  → suma de valores singulares
np.linalg.norm(M, ord=2)    # 5.464...  → norma espectral
```

### `axis` — eje sobre el que normar

Entero o tupla. Permite calcular muchas normas a la vez, p.ej. la norma de cada fila de una matriz de vectores. El eje indicado se colapsa (ver [[concepto_shape]]).

```python
P = np.array([[3, 4], [6, 8]])
np.linalg.norm(P, axis=1)   # [5., 10.]  → norma por fila
```

### `keepdims` — conservar dimensiones

Si `True`, el eje reducido se mantiene con tamaño 1, útil para [[concepto_broadcasting|broadcasting]] (p.ej. normalizar filas dividiendo por su norma).

```python
P = np.array([[3, 4], [6, 8]])
P / np.linalg.norm(P, axis=1, keepdims=True)   # vectores unitarios por fila
```

## Casos de uso

### Distancia euclídea entre dos puntos

```python
a = np.array([1, 2])
b = np.array([4, 6])
np.linalg.norm(a - b)   # 5.0
```

### Normalizar un vector a magnitud 1

```python
v = np.array([3, 4])
v / np.linalg.norm(v)   # [0.6, 0.8]
```

## Buenas prácticas

1. Para normas de muchos vectores apilados, usa `axis` en vez de un bucle Python.
2. Combina `axis` con `keepdims=True` cuando vayas a dividir el array original por su norma.
3. Recuerda que `ord=2` cambia de significado entre vectores (euclídea) y matrices (espectral, costosa porque usa SVD).
4. Para distancias, `np.linalg.norm(a - b)` es más legible que calcular la raíz a mano.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Norma matricial inesperada | `ord=2` en matriz da la espectral, no la euclídea elemento a elemento | usar `'fro'` para Frobenius |
| `ValueError: Invalid norm order` | `ord` no válido para esa dimensión (p.ej. `'fro'` en vector) | elegir un `ord` compatible con la dim de `x` |
| Resultado escalar cuando se esperaba por fila | falta `axis` | pasar `axis=0` o `axis=1` |
| Broadcasting falla al normalizar | se perdió el eje | `keepdims=True` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.linalg.cond]]
- [[np.linalg.matrix_rank]]
- [[np.linalg.svd]]
- [[np.linalg.inv]]
