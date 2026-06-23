---
title: np/manipulacion_forma/dividir — partir arrays en sub-arrays
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/dividir — partir arrays en sub-arrays

El **inverso de `combinar/`**: toma un único array y lo parte, a lo largo de un eje, en una **lista**
de sub-arrays. Donde [[np.concatenate]] une varios arrays por un eje, las funciones de aquí deshacen
esa unión troceando ese mismo eje. Todos los sub-arrays resultantes son **vistas** del original
—comparten su buffer de memoria—, por lo que modificarlos modifica el array fuente (ver
[[concepto_views_vs_copias]]).

Todas las funciones comparten la misma firma base `f(ary, indices_or_sections[, axis])` y solo
cambian en qué eje actúan y si exigen división exacta.

## split vs array_split: la división exacta

La diferencia clave de la familia está en el **modo entero** (cuando el segundo argumento es un
número $N$ de partes):

- [[np.split]] **exige división exacta**: si el eje no es divisible por $N$, lanza `ValueError`.
- [[np.array_split]] **admite partes desiguales**: reparte el resto entre los primeros trozos, así
  que **nunca falla** por el tamaño. Partir 7 elementos en 3 da trozos de `3, 2, 2`.

Con una **lista de índices de corte** (`np.split(a, [3, 7])`) ninguno de los dos exige
divisibilidad: ambos trocean como el slicing de Python (`a[:3]`, `a[3:7]`, `a[7:]`).

```python
import numpy as np

np.split(np.arange(9), 3)          # OK → 3 partes de (3,)
# np.split(np.arange(10), 3)       # ValueError: división no exacta
[a.shape for a in np.array_split(np.arange(10), 3)]   # [(4,), (3,), (3,)]
```

## Los atajos por eje fijo: vsplit / hsplit / dsplit

Tres envoltorios de `split` con el `axis` ya fijado. No añaden cómputo: solo hacen el código más
legible al nombrar la dirección del corte. Cada uno equivale a `np.split(ary, ..., axis=<eje>)`.

| Atajo | Eje | Corta | Equivale a | `ndim` mínimo |
|---|---|---|---|---|
| [[np.vsplit]] | 0 | filas (vertical) | `split(a, ..., axis=0)` | 2 |
| [[np.hsplit]] | 1 | columnas (horizontal) | `split(a, ..., axis=1)` | 2 (acepta 1D → eje 0) |
| [[np.dsplit]] | 2 | profundidad (*depth*) | `split(a, ..., axis=2)` | 3 |

`hsplit` es el único que tolera arrays 1D (cae al eje 0); `vsplit` requiere 2D y `dsplit` requiere 3D.

## Tabla de funciones

| Función | Eje | Partes desiguales | Devuelve | Inverso de |
|---|---|---|---|---|
| [[np.split]] | cualquiera (default 0) | no (exige exacto) | `list[ndarray]` (vistas) | [[np.concatenate]] |
| [[np.array_split]] | cualquiera (default 0) | **sí** | `list[ndarray]` (vistas) | [[np.concatenate]] |
| [[np.vsplit]] | 0 (filas) | no | `list[ndarray]` (vistas) | [[np.vstack]] |
| [[np.hsplit]] | 1 (columnas) | no | `list[ndarray]` (vistas) | [[np.hstack]] |
| [[np.dsplit]] | 2 (profundidad) | no | `list[ndarray]` (vistas) | [[np.dstack]] |

> [!important] Todas devuelven una LISTA, no un array
> El retorno es siempre una `list` de `ndarray`. Lo idiomático es **desempaquetar** cuando se conoce
> el número de trozos: `izq, der = np.hsplit(M, 2)`.

## Entero vs índices de corte

```python
import numpy as np

a = np.arange(12).reshape(4, 3)

# Partes iguales (entero): debe ser exacto con split
partes = np.vsplit(a, 2)        # 2 matrices de (2, 3) — OK
# np.vsplit(a, 3)               # ValueError: 4 no es divisible entre 3
partes = np.array_split(a, 3)   # OK → (2,3), (1,3), (1,3)

# Posiciones arbitrarias (lista de índices): siempre válido
partes = np.vsplit(a, [1, 3])   # shapes (1,3), (2,3), (1,3)
```

## Relación con combinar

`dividir/` y `combinar/` son inversos lógicos, pero **no simétricos en memoria**:

- `split` y compañía → **vistas** (sin copia, O(1) en memoria).
- `concatenate` de esas vistas → **copia** a un buffer nuevo.

Iterar sobre los sub-arrays de un array grande es barato; reunirlos en un array nuevo tiene coste.
