---
title: np.random.permutation — Copia permutada aleatoriamente (no toca el original)
aliases:
  - permutation
  - random.permutation
  - np.random.permutation
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray
inplace: false
draft: false
---

# np.random.permutation — permuta devolviendo una copia

`np.random.permutation` devuelve una **copia nueva** de `x` con sus elementos reordenados al azar; **no modifica** el original. Es la contraparte segura de [[np.random.shuffle]] (que baraja in-place y devuelve `None`). Acepta también un entero `n`, en cuyo caso permuta `np.arange(n)` —el modo idiomático de generar índices aleatorios sin construir el array antes—.

## La idea en una fórmula

Una permutación es una biyección $\sigma$ de los índices del **primer eje**. Si `x` tiene [[concepto_shape|shape]] $(n_0, n_1, \dots, n_{k-1})$, la salida tiene **el mismo shape** y se construye reordenando solo el eje 0:

$$ y_{\,i,\;\dots} \;=\; x_{\,\sigma(i),\;\dots} \qquad \sigma \in S_{n_0} \text{ (permutación de } \{0,\dots,n_0-1\}) $$

El shape no cambia —**no es una reducción**—, lo que cambia es el orden a lo largo del eje 0:

$$ (n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{permutation}\ }\; (n_0, n_1, \dots, n_{k-1}) $$

En arrays N-D, cada "fila" del eje 0 (un sub-tensor de shape $(n_1,\dots,n_{k-1})$) se mueve **entera**: su contenido interno no se mezcla.

## Firma de la función

```python
np.random.permutation(
    x,   # int | array_like: tamaño n, o array a permutar por el eje 0
) -> ndarray
```

## Valor de retorno

Devuelve un **`ndarray` nuevo**; `x` queda intacto. El comportamiento depende del tipo de `x`:

| `x` | Resultado | Eje permutado |
|-----|-----------|---------------|
| entero `n` | copia de `np.arange(n)` barajada | — |
| array 1D | copia barajada | único eje |
| array N-D | copia barajada por el **primer eje** | eje 0 (filas) |

```python
import numpy as np
np.random.seed(0)

np.random.permutation(5)
# array([2, 0, 1, 3, 4])   → permuta arange(5)

original = np.array([10, 20, 30, 40])
np.random.permutation(original)
# array([20, 40, 10, 30])
original
# array([10, 20, 30, 40])   → intacto (es una copia)
```

## Parámetros en detalle

### `x` — entero a expandir o array a permutar

- Si es un **`int`** `n`, equivale a permutar `np.arange(n)`: devuelve los enteros `0..n-1` en orden aleatorio. Útil para barajar índices.
- Si es un **array** de cualquier shape, se baraja a lo largo del **primer eje**; cada fila se mantiene unida.

```python
M = np.arange(9).reshape(3, 3)
np.random.permutation(M)
# reordena filas completas; las columnas internas NO se mezclan
# p. ej. array([[6, 7, 8],
#               [0, 1, 2],
#               [3, 4, 5]])
```

## El eje y el caso N-D

La regla es: **solo se permuta el eje 0**. Para mezclar a lo largo de otro eje, o **todos** los elementos, hay que actuar antes o usar otra herramienta.

```python
T = np.arange(24).reshape(2, 3, 4)   # (2, 3, 4)
np.random.permutation(T).shape       # (2, 3, 4) → solo reordena los 2 bloques del eje 0

# ¿mezclar TODOS los elementos de una matriz? aplanar primero:
A = np.arange(9).reshape(3, 3)
np.random.permutation(A.ravel()).reshape(3, 3)   # ahora sí se mezcla todo

# ¿permutar por otro eje? usar el Generator moderno con axis:
rng = np.random.default_rng(0)
rng.permuted(A, axis=1)              # permuta dentro de cada fila
```

## Casos de uso

### Barajar índices sin alterar los datos

```python
idx = np.random.permutation(len(datos))
datos_barajados = datos[idx]         # 'datos' original intacto
```

### Dividir en train/test

```python
perm = np.random.permutation(n)
train, test = perm[:800], perm[800:]
```

### Barajar features y etiquetas en paralelo

```python
idx = np.random.permutation(len(X))
X_s, y_s = X[idx], y[idx]            # mismo orden en ambos
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperabas mezclar **todos** los elementos de una matriz | solo permuta el eje 0 | aplanar con `ravel()` antes, o `rng.permuted(x, axis=...)` |
| Creías que modificaba `x` | `permutation` devuelve una **copia** | usar [[np.random.shuffle]] para in-place |
| Resultado no reproducible | sin semilla fijada | [[np.random.seed]] antes, o `np.random.default_rng(s)` |
| Pasaste un `float` esperando `arange` | solo `int` o array | redondear/convertir a `int` |

## Notas relacionadas

- [[np.random.shuffle]] — la versión in-place (devuelve `None`)
- [[np.random.default_rng]] — `rng.permutation` / `rng.permuted` en la API moderna
- [[np.random.seed]] — reproducibilidad de la permutación
- [[concepto_shape]] — qué eje se reordena
- [[concepto_views_vs_copias]] — por qué el original no cambia
