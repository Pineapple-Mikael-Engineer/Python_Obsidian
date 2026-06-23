---
title: np.dsplit — parte un array por profundidad (eje 2, atajo de split)
aliases:
  - dsplit
  - np.dsplit
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

# np.dsplit — parte un array por profundidad (eje 2, atajo de split)

`np.dsplit` es un **atajo de [[np.split]] con el eje fijado en 2** (la profundidad, *depth*). Parte
un array a lo largo de su tercer eje y devuelve una **lista** de sub-arrays. Es el caso natural para
tensores de tres ejes o más —típicamente separar los **canales** de un volumen de imágenes— y la
operación inversa de [[np.dstack]].

## La idea en una fórmula

`dsplit` trocea el **eje 2**. Para un tensor $(m, n, d)$, partir en $s$ trozos divide la profundidad
y deja filas y columnas intactas:

$$
(m,\,n,\,d) \;\xrightarrow{\ \text{dsplit},\ s\ \text{partes}\ }\; \big[\ (m,\,n,\,d/s)\ \big]\times s
\qquad\equiv\qquad \texttt{np.split(ary, s, axis=2)}
$$

En N-D actúa siempre sobre el eje de índice 2:
$(n_0,\,n_1,\,n_2,\dots)\to[\,(n_0,\,n_1,\,n_2/s,\dots)\,]\times s$.

> [!warning] Requiere `ndim >= 3`
> `dsplit` necesita que exista el eje 2: con arrays 1D o 2D lanza
> `ValueError: dsplit only works on arrays of 3 or more dimensions`. Para esos casos usa
> [[np.split]] con el `axis` adecuado.

## Firma

```python
np.dsplit(
    ary,                  # array_like: el array a partir (debe ser 3D o más)
    indices_or_sections,  # int | sequence[int]: nº de partes iguales, o puntos de corte
) -> list[ndarray]
```

No tiene parámetro `axis`: está fijado en 2. Internamente llama a
`np.split(ary, indices_or_sections, axis=2)`.

## Los parámetros en detalle

### `ary` — el array a partir
`array_like` de **al menos 3 dimensiones** (`ndim >= 3`). Los trozos devueltos son **vistas** (ver
[[concepto_views_vs_copias]]).

### `indices_or_sections` — cómo se corta
Igual que en `split`: un `int` (partes iguales, exige que la profundidad sea divisible, si no
`ValueError`) o una secuencia de índices de corte (sin requisito de divisibilidad).

```python
T = np.arange(2*2*6).reshape(2, 2, 6)
np.dsplit(T, 3)        # 3 arrays de (2, 2, 2)
np.dsplit(T, [2, 5])   # (2,2,2), (2,2,3), (2,2,1) → cortes en profundidad 2 y 5
```

## El caso N-D

`dsplit` siempre apunta al **eje 2**. El resto del shape se conserva en cada trozo.

| `ary.shape` | `indices_or_sections` | salida | equivalente |
|---|---|---|---|
| `(2, 2, 6)` | `3` | 3 × `(2, 2, 2)` | `split(ary, 3, axis=2)` |
| `(4, 4, 3)` | `3` | 3 × `(4, 4, 1)` | `split(ary, 3, axis=2)` |
| `(2, 2, 6)` | `[2, 5]` | `(2,2,2)`, `(2,2,3)`, `(2,2,1)` | `split(ary, [2,5], axis=2)` |
| `(3, 2, 4, 5)` | `2` | 2 × `(3, 2, 2, 5)` | `split(ary, 2, axis=2)` |

```python
T = np.arange(3*2*4*5).reshape(3, 2, 4, 5)
[p.shape for p in np.dsplit(T, 2)]   # [(3, 2, 2, 5), (3, 2, 2, 5)]
```

## Vectorización

`dsplit` no añade cómputo: es azúcar sintáctico sobre [[np.split]] que mejora la **legibilidad** al
trabajar con volúmenes. Las dos líneas dan lo mismo y comparten coste (vistas, sin copia); la
primera expresa mejor la intención de separar por profundidad (ver [[concepto_vectorizacion]]):

```python
r, g, b = np.dsplit(imagen, 3)            # "separo los 3 canales de profundidad"
r, g, b = np.split(imagen, 3, axis=2)     # idéntico, menos directo de leer
```

## Valor de retorno

Devuelve una **`list` de `ndarray`** (vistas), de longitud $s$ o `len(indices)+1`. Cada trozo
conserva el shape original salvo el eje 2.

| Entrada | `indices_or_sections` | longitud | shape de cada trozo |
|---|---|---|---|
| `(m, n, d)` divisible | `int` $s$ | $s$ | `(m, n, d/s)` |
| `(m, n, d)` | `[c1, c2]` | 3 | `(m,n,c1)`, `(m,n,c2-c1)`, `(m,n,d-c2)` |

## Casos de uso

### Separar los canales de color de una imagen RGB
```python
img = np.arange(4*4*3).reshape(4, 4, 3)   # imagen 4x4 con 3 canales
r, g, b = np.dsplit(img, 3)               # cada uno (4, 4, 1)
r.shape                                    # (4, 4, 1)
```

### Partir el eje de profundidad por puntos de corte
```python
vol = np.arange(2*3*8).reshape(2, 3, 8)
bloques = np.dsplit(vol, [3, 6])          # (2,3,3), (2,3,3), (2,3,2)
[b.shape for b in bloques]                # [(2, 3, 3), (2, 3, 3), (2, 3, 2)]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `dsplit only works on arrays of 3 or more dimensions` | array 1D o 2D | usar [[np.split]] con `axis` |
| `array split does not result in an equal division` | profundidad no divisible | usar `np.array_split(ary, n, axis=2)` |
| Cortar el eje equivocado | `dsplit` actúa sobre el eje 2 | para filas/columnas usar [[np.vsplit]] / [[np.hsplit]] |

## Notas relacionadas

- [[concepto_shape]] — qué eje trocea el atajo
- [[np.split]] — la función general (`dsplit` = `split` con `axis=2`)
- [[np.array_split]] — variante que admite partes desiguales
- [[np.vsplit]] · [[np.hsplit]] — atajos para los ejes 0 y 1
- [[np.dstack]] — la operación inversa (apila por profundidad)
