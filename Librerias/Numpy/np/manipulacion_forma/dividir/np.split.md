---
title: np.split — parte un array en sub-arrays a lo largo de un eje
aliases:
  - split
  - np.split
  - dividir
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
  - concepto_axis_parametro

draft: false
---

# np.split — parte un array en sub-arrays a lo largo de un eje

`np.split` toma un único array y lo **corta** a lo largo de un eje, devolviendo una **lista** de
sub-arrays. Es la operación inversa de [[np.concatenate]]: donde `concatenate` une varios arrays
por un eje, `split` deshace esa unión partiendo ese mismo eje. La pregunta al usarla es **"¿qué eje
se parte y en cuántos trozos?"**; los demás ejes quedan intactos.

## La idea en una fórmula

Partir es **trocear un eje**. Si el array tiene shape $(n_0,\dots,n_{k-1})$ y se parte el eje $p$
(de tamaño $n_p$) en $s$ partes iguales, cada sub-array conserva todos los demás ejes y solo cambia
el eje $p$, que pasa a valer $n_p/s$:

$$
(n_0,\dots,n_{p-1},\,n_p,\,n_{p+1},\dots,n_{k-1})
\;\xrightarrow{\ \text{split},\ s\ \text{partes, axis}=p\ }\;
\big[\ (n_0,\dots,\,n_p/s,\,\dots,n_{k-1})\ \big]\times s
$$

El resultado es una **lista de $s$ arrays**, todos con el mismo shape (modo entero). Con **puntos de
corte** $[c_1, c_2, \dots]$ en vez de un entero, los trozos tienen tamaños $c_1,\ c_2-c_1,\ \dots$
a lo largo del eje $p$ (como el slicing de Python `ary[:c1]`, `ary[c1:c2]`, ...) y **no** tienen por
qué ser iguales.

> [!warning] Modo entero: división exacta o `ValueError`
> Con un entero $s$, el eje **debe** ser divisible: $n_p \bmod s = 0$. Si no, NumPy lanza
> `ValueError`. Para repartir un eje no divisible sin error, usa [[np.array_split]].

## Firma

```python
np.split(
    ary,                  # array_like: el array a partir
    indices_or_sections,  # int | sequence[int]: nº de partes iguales, o puntos de corte
    axis=0,               # int: eje a lo largo del cual se parte
) -> list[ndarray]
```

## Los parámetros en detalle

### `ary` — el array a partir
`array_like` de cualquier dimensión. Se convierte a `ndarray` si no lo es. No se modifica: los
sub-arrays devueltos son **vistas** sobre su buffer (ver [[concepto_views_vs_copias]]), no copias.

### `indices_or_sections` — cómo se corta (los dos modos)
El parámetro central, con dos interpretaciones según su tipo:

- **`int` $s$ → $s$ partes iguales.** Exige que el eje sea divisible (`n_p % s == 0`), si no
  `ValueError`.

  ```python
  np.split(np.arange(9), 3)   # 3 partes de (3,)
  np.split(np.arange(10), 3)  # ValueError: división no exacta → usar array_split
  ```

- **secuencia de índices `[c1, c2, ...]` → puntos de corte.** Trocea como el slicing de Python:
  `ary[:c1]`, `ary[c1:c2]`, ..., `ary[cN:]`. No requiere divisibilidad y los trozos pueden tener
  tamaños distintos. Índices fuera de rango producen sub-arrays **vacíos** (no error).

  ```python
  np.split(np.arange(8), [3, 5])
  # [array([0,1,2]), array([3,4]), array([5,6,7])]
  ```

### `axis` — qué eje se parte
`int`, por defecto `0` (el primer eje: filas en 2D). Solo cambia **ese** eje; el resto del shape se
conserva en todos los trozos. Acepta ejes negativos (`axis=-1` = último eje).

```python
M = np.arange(12).reshape(3, 4)
np.split(M, 2, axis=1)   # 2 arrays de (3, 2) → parte las columnas
```

## El caso N-D

La regla es mecánica: **solo el eje de `axis` se trocea; todos los demás ejes quedan idénticos** en
cada sub-array. Lee la salida como "el mismo tensor, pero con el eje partido".

| `ary.shape` | `indices_or_sections` | `axis` | salida | lectura |
|---|---|---|---|---|
| `(6,)` | `3` | `0` | 3 × `(2,)` | parte el vector en 3 |
| `(6,)` | `[2, 4]` | `0` | `(2,)`, `(2,)`, `(2,)` | cortes en 2 y 4 |
| `(4, 4)` | `2` | `1` | 2 × `(4, 2)` | parte las columnas |
| `(2, 6, 4)` | `3` | `1` | 3 × `(2, 2, 4)` | trocea el eje central |
| `(2, 6, 4)` | `2` | `-1` | 2 × `(2, 6, 2)` | parte el último eje |

```python
# Tensor (2 lotes, 6 filas, 4 columnas): partir el eje del medio
T = np.arange(2*6*4).reshape(2, 6, 4)
partes = np.split(T, 3, axis=1)   # lista de 3 arrays, cada uno (2, 2, 4)
[p.shape for p in partes]         # [(2, 2, 4), (2, 2, 4), (2, 2, 4)]
```

## Vectorización

`np.split` no copia datos: sustituye un bucle de slicing manual por un único corte declarativo. Las
dos versiones producen lo mismo, pero la de NumPy expresa *qué* eje partir, no *cómo* iterar
calculando los índices (ver [[concepto_vectorizacion]]):

```python
# Slicing manual (calcular los índices a mano):
def split3(arr):
    n = len(arr) // 3
    return [arr[0:n], arr[n:2*n], arr[2*n:3*n]]

# Equivalente declarativo:
np.split(arr, 3)
```

Cada sub-array es una **vista** (comparte buffer con `ary`), así que la operación es O(1) en memoria:
no se copia ni un byte, solo se crean nuevas tuplas de shape/strides.

## Valor de retorno

Devuelve una **`list` de `ndarray`** (no un array). Su longitud es $s$ (modo entero) o
`len(indices) + 1` (modo cortes). Cada elemento es una **vista** sobre `ary`.

| Entrada | `indices_or_sections` | longitud de la lista | shape de cada trozo |
|---|---|---|---|
| `(n,)` divisible | `int` $s$ | $s$ | `(n/s,)` |
| `(m, n)` | `int` $s$, `axis=0` | $s$ | `(m/s, n)` |
| `(m, n)` | `[c1, c2]`, `axis=1` | 3 | `(m, c1)`, `(m, c2-c1)`, `(m, n-c2)` |

```python
type(np.split(np.arange(6), 3))   # <class 'list'>
[a.shape for a in np.split(np.arange(6), 3)]   # [(2,), (2,), (2,)]
```

Como devuelve una lista, lo idiomático es **desempaquetar** cuando sabes cuántos trozos hay:

```python
a, b, c = np.split(np.arange(6), 3)
```

## Casos de uso

### Separar features y target (cortar columnas)
```python
datos = np.random.rand(100, 5)
X, y = np.split(datos, [4], axis=1)   # X:(100,4)  y:(100,1)
```

### Partir en lotes iguales
```python
lotes = np.split(np.arange(12), 4)    # 4 lotes de (3,)
```

### N-D: trocear el eje espacial de un tensor de imágenes
```python
# Lote de 8 imágenes 4x4 en escala de grises: (8, 4, 4)
imgs = np.arange(8*4*4).reshape(8, 4, 4)
mitades = np.split(imgs, 2, axis=1)   # parte cada imagen en mitad superior/inferior
[m.shape for m in mitades]            # [(8, 2, 4), (8, 2, 4)]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `array split does not result in an equal division` | eje no divisible por el entero | usar [[np.array_split]] |
| Esperar un array y recibir una lista | `split` devuelve `list[ndarray]` | desempaquetar (`a, b = ...`) o indexar |
| Cortes en el eje equivocado | `axis` por defecto es `0` | pasar `axis` explícito |
| Modificar un trozo cambia el original | los trozos son vistas | copiar con `.copy()` si se necesita independencia |

## Notas relacionadas

- [[concepto_shape]] — qué le pasa al shape al partir un eje
- [[concepto_axis_parametro]] — qué eje se trocea
- [[np.array_split]] — variante que admite partes desiguales (sin exigir división exacta)
- [[np.concatenate]] — la operación inversa (une por un eje)
- [[np.vsplit]] · [[np.hsplit]] · [[np.dsplit]] — atajos por eje fijo
