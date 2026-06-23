---
title: np.vsplit — parte un array por filas (eje 0, atajo de split)
aliases:
  - vsplit
  - np.vsplit
tags:
  - numpy
  - api/funcion
  - manipulacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: list[ndarray]
inplace: false

# --- Dependencias ---
requiere:
  - concepto_shape

draft: false
---

# np.vsplit — parte un array por filas (eje 0, atajo de split)

`np.vsplit` es un **atajo de [[np.split]] con el eje fijado en 0** (las filas). Parte un array
**verticalmente** y devuelve una **lista** de sub-arrays. Su valor es la legibilidad: deja claro que
la intención es separar grupos de filas, sin escribir `axis=0`. Es la operación inversa de
[[np.vstack]].

## La idea en una fórmula

`vsplit` trocea el **eje 0**. Para una matriz $(m, n)$, partir en $s$ trozos divide las filas y deja
las columnas intactas:

$$
(m,\,n) \;\xrightarrow{\ \text{vsplit},\ s\ \text{partes}\ }\; \big[\ (m/s,\,n)\ \big]\times s
\qquad\equiv\qquad \texttt{np.split(ary, s, axis=0)}
$$

En N-D actúa siempre sobre el eje de índice 0:
$(n_0,\,n_1,\dots)\to[\,(n_0/s,\,n_1,\dots)\,]\times s$.

> [!warning] Requiere `ndim >= 2`
> A diferencia de [[np.hsplit]], `vsplit` **no acepta arrays 1D**: lanza
> `ValueError: vsplit only works on arrays of 2 or more dimensions`. Para partir un vector usa
> [[np.split]] directamente.

## Firma

```python
np.vsplit(
    ary,                  # array_like: el array a partir (debe ser 2D o más)
    indices_or_sections,  # int | sequence[int]: nº de partes iguales, o puntos de corte
) -> list[ndarray]
```

No tiene parámetro `axis`: está fijado en 0. Internamente llama a
`np.split(ary, indices_or_sections, axis=0)`.

## Los parámetros en detalle

### `ary` — el array a partir
`array_like` de **al menos 2 dimensiones** (`ndim >= 2`). Los trozos devueltos son **vistas** (ver
[[concepto_views_vs_copias]]).

### `indices_or_sections` — cómo se corta
Igual que en `split`: un `int` (partes iguales, exige que las filas sean divisibles, si no
`ValueError`) o una secuencia de índices de corte (sin requisito de divisibilidad).

```python
M = np.arange(12).reshape(4, 3)
np.vsplit(M, 2)        # 2 arrays de (2, 3)
np.vsplit(M, [1, 3])   # (1,3), (2,3), (1,3) → cortes en filas 1 y 3
```

## El caso N-D

`vsplit` siempre apunta al **eje 0**. El resto del shape se conserva en cada trozo.

| `ary.shape` | `indices_or_sections` | salida | equivalente |
|---|---|---|---|
| `(6, 4)` | `3` | 3 × `(2, 4)` | `split(ary, 3, axis=0)` |
| `(6, 4)` | `[1, 4]` | `(1,4)`, `(3,4)`, `(2,4)` | `split(ary, [1,4], axis=0)` |
| `(6, 2, 4)` | `2` | 2 × `(3, 2, 4)` | `split(ary, 2, axis=0)` |

```python
T = np.arange(6*2*4).reshape(6, 2, 4)
[p.shape for p in np.vsplit(T, 3)]   # [(2, 2, 4), (2, 2, 4), (2, 2, 4)]
```

## Vectorización

`vsplit` no añade cómputo: es azúcar sintáctico sobre [[np.split]] orientado a la **legibilidad** con
matrices. Las dos líneas dan lo mismo y comparten coste (vistas, sin copia); la primera comunica
mejor la intención (ver [[concepto_vectorizacion]]):

```python
arriba, abajo = np.vsplit(M, 2)            # "parto las filas en dos"
arriba, abajo = np.split(M, 2, axis=0)     # idéntico, menos directo de leer
```

## Valor de retorno

Devuelve una **`list` de `ndarray`** (vistas), de longitud $s$ o `len(indices)+1`. Cada trozo
conserva el shape original salvo el eje 0.

| Entrada | `indices_or_sections` | longitud | shape de cada trozo |
|---|---|---|---|
| `(m, n)` divisible | `int` $s$ | $s$ | `(m/s, n)` |
| `(m, n)` | `[c1, c2]` | 3 | `(c1, n)`, `(c2-c1, n)`, `(m-c2, n)` |

## Casos de uso

### Separar un dataset en bloques de filas
```python
datos = np.random.rand(100, 8)
bloques = np.vsplit(datos, 5)   # 5 bloques de (20, 8)
```

### N-D: partir el primer eje de un lote de matrices
```python
lote = np.arange(6*3*2).reshape(6, 3, 2)   # 6 matrices 3x2
grupos = np.vsplit(lote, 3)                # 3 grupos de 2 matrices cada uno
[g.shape for g in grupos]                  # [(2, 3, 2), (2, 3, 2), (2, 3, 2)]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `vsplit only works on arrays of 2 or more dimensions` | array 1D | usar [[np.split]] |
| `array split does not result in an equal division` | filas no divisibles | usar `np.array_split(ary, n, axis=0)` |
| Cortar columnas en vez de filas | `vsplit` actúa sobre el eje 0 | para columnas usar [[np.hsplit]] |

## Notas relacionadas

- [[concepto_shape]] — qué eje trocea el atajo
- [[np.split]] — la función general (`vsplit` = `split` con `axis=0`)
- [[np.array_split]] — variante que admite partes desiguales
- [[np.hsplit]] · [[np.dsplit]] — atajos para los ejes 1 y 2
- [[np.vstack]] — la operación inversa (une por filas)
