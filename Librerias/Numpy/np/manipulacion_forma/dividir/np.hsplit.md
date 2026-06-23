---
title: np.hsplit — parte un array por columnas (eje 1, atajo de split)
aliases:
  - hsplit
  - np.hsplit
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

# np.hsplit — parte un array por columnas (eje 1, atajo de split)

`np.hsplit` es un **atajo de [[np.split]] con el eje fijado en 1** (las columnas). Parte un array
**horizontalmente** y devuelve una **lista** de sub-arrays. Como atajo legible, su único valor es
hacer evidente la intención —"separar columnas"— sin escribir `axis=1`. Es la operación inversa de
[[np.hstack]].

## La idea en una fórmula

`hsplit` trocea el **eje 1**. Para una matriz $(m, n)$, partir en $s$ trozos divide las columnas y
deja las filas intactas:

$$
(m,\,n) \;\xrightarrow{\ \text{hsplit},\ s\ \text{partes}\ }\; \big[\ (m,\,n/s)\ \big]\times s
\qquad\equiv\qquad \texttt{np.split(ary, s, axis=1)}
$$

En el caso general N-D actúa sobre el eje de índice 1:
$(n_0,\,n_1,\dots)\to[\,(n_0,\,n_1/s,\dots)\,]\times s$.

> [!note] Excepción para 1D: cae al eje 0
> Un array 1D no tiene eje 1. `hsplit` lo trata como caso especial y parte el **eje 0**:
> $(n,)\to[\,(n/s,)\,]\times s$. Es la única función de la familia "h/v/d" que acepta 1D.

## Firma

```python
np.hsplit(
    ary,                  # array_like: el array a partir (1D o más)
    indices_or_sections,  # int | sequence[int]: nº de partes iguales, o puntos de corte
) -> list[ndarray]
```

No tiene parámetro `axis`: el eje está fijado (1, o 0 en 1D). Internamente llama a
`np.split(ary, indices_or_sections, axis=...)`.

## Los parámetros en detalle

### `ary` — el array a partir
`array_like`. A diferencia de [[np.vsplit]], **acepta arrays 1D** (los parte por el eje 0). Los
trozos devueltos son **vistas** (ver [[concepto_views_vs_copias]]).

### `indices_or_sections` — cómo se corta
Igual que en `split`: un `int` (partes iguales, exige que las columnas sean divisibles, si no
`ValueError`) o una secuencia de índices de corte (sin requisito de divisibilidad).

```python
M = np.arange(12).reshape(3, 4)
np.hsplit(M, 2)        # 2 arrays de (3, 2)
np.hsplit(M, [1, 3])   # (3,1), (3,2), (3,1) → cortes en columnas 1 y 3
```

## El caso N-D

`hsplit` siempre apunta al **eje 1** (salvo en 1D, donde usa el eje 0). El resto del shape no cambia.

| `ary.shape` | `indices_or_sections` | salida | equivalente |
|---|---|---|---|
| `(4, 6)` | `3` | 3 × `(4, 2)` | `split(ary, 3, axis=1)` |
| `(4, 6)` | `[2, 4]` | `(4,2)`, `(4,2)`, `(4,2)` | `split(ary, [2,4], axis=1)` |
| `(6,)` | `2` | 2 × `(3,)` | `split(ary, 2, axis=0)` (caso 1D) |
| `(2, 6, 4)` | `3` | 3 × `(2, 2, 4)` | `split(ary, 3, axis=1)` |

```python
T = np.arange(2*6*4).reshape(2, 6, 4)
[p.shape for p in np.hsplit(T, 3)]   # [(2, 2, 4), (2, 2, 4), (2, 2, 4)]
```

## Vectorización

`hsplit` no añade cómputo: es azúcar sintáctico sobre [[np.split]] que mejora la **legibilidad** en
código con matrices. Las dos líneas son idénticas en resultado y coste (vistas, sin copia); la
primera dice mejor *qué* se separa (ver [[concepto_vectorizacion]]):

```python
izq, der = np.hsplit(M, 2)            # "parto las columnas en dos"
izq, der = np.split(M, 2, axis=1)     # idéntico, menos directo de leer
```

## Valor de retorno

Devuelve una **`list` de `ndarray`** (vistas), de longitud $s$ o `len(indices)+1`. Cada trozo
conserva el shape original salvo el eje 1 (o el 0 en 1D).

| Entrada | `indices_or_sections` | longitud | shape de cada trozo |
|---|---|---|---|
| `(m, n)` divisible | `int` $s$ | $s$ | `(m, n/s)` |
| `(m, n)` | `[c1, c2]` | 3 | `(m, c1)`, `(m, c2-c1)`, `(m, n-c2)` |
| `(n,)` | `int` $s$ | $s$ | `(n/s,)` |

## Casos de uso

### Separar grupos de columnas (features)
```python
datos = np.random.rand(100, 6)
primeras, ultimas = np.hsplit(datos, [3])   # (100,3) y (100,3)
```

### Partir las columnas de una matriz 2D (visto como matriz)
`hsplit` sobre un `(2, 4)` en 2 corta el eje 1 (columnas) en dos bloques de 2, dejando las filas:

$$
\underbrace{\begin{bmatrix} 0 & 1 & 2 & 3 \\ 4 & 5 & 6 & 7 \end{bmatrix}}_{(2,\,4)}
\;\xrightarrow{\ \text{hsplit},\ 2\ }\;
\underbrace{\begin{bmatrix} 0 & 1 \\ 4 & 5 \end{bmatrix}}_{(2,\,2)}
\;,\;
\underbrace{\begin{bmatrix} 2 & 3 \\ 6 & 7 \end{bmatrix}}_{(2,\,2)}
$$

```python
M = np.arange(8).reshape(2, 4)
izq, der = np.hsplit(M, 2)            # izq:(2,2)  der:(2,2)
```

### N-D: partir el eje de columnas de un lote de matrices
```python
lote = np.arange(5*8*2).reshape(5, 8, 2)   # 5 matrices 8x2
mitades = np.hsplit(lote, 2)               # parte las 8 "columnas" en dos bloques de 4
[m.shape for m in mitades]                 # [(5, 4, 2), (5, 4, 2)]
```

### 4D: cortar el eje 1 de un lote de tensores
```python
# Tensor 4D (N=4, eje1=8, H=5, W=5): hsplit siempre trocea el eje 1
t = np.arange(4*8*5*5).reshape(4, 8, 5, 5)
mitades = np.hsplit(t, 2)                   # parte el eje 1 (8) en dos bloques de 4
[m.shape for m in mitades]                  # [(4, 4, 5, 5), (4, 4, 5, 5)]
```

### 5D: cortar el eje 1 de un lote de vídeos
```python
# Lote de clips: (N=2, C=8, T=3, H=16, W=16) → hsplit parte el eje 1 (8 canales)
clips = np.arange(2*8*3*16*16).reshape(2, 8, 3, 16, 16)
bloques = np.hsplit(clips, 2)               # parte los 8 canales en dos grupos de 4
[b.shape for b in bloques]                  # [(2, 4, 3, 16, 16), (2, 4, 3, 16, 16)]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `array split does not result in an equal division` | columnas no divisibles | usar `np.array_split(ary, n, axis=1)` |
| Cortar filas en vez de columnas | `hsplit` actúa sobre el eje 1 | para filas usar [[np.vsplit]] |
| Esperar un array y recibir una lista | devuelve `list[ndarray]` | desempaquetar o indexar |

## Notas relacionadas

- [[concepto_shape]] — qué eje trocea el atajo
- [[np.split]] — la función general (`hsplit` = `split` con `axis=1`)
- [[np.array_split]] — variante que admite partes desiguales
- [[np.vsplit]] · [[np.dsplit]] — atajos para los ejes 0 y 2
- [[np.hstack]] — la operación inversa (une por columnas)
