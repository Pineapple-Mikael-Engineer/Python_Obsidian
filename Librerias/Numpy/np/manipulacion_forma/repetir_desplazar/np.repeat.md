---
title: np.repeat — repite cada elemento r veces a lo largo de un eje
aliases:
  - repeat
  - np.repeat
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
  - concepto_axis_parametro

draft: false
---

# np.repeat — repite cada elemento r veces a lo largo de un eje

`np.repeat` **duplica cada elemento** del array `r` veces de forma consecutiva a lo largo de un eje:
el `[1, 2, 3]` se convierte en `[1, 1, 2, 2, 3, 3]`, no en `[1, 2, 3, 1, 2, 3]`. La unidad que se
repite es el **elemento individual** (in situ), y por eso el eje elegido **crece** mientras los demás
quedan intactos. Esta es la diferencia exacta con [[np.tile]], que repite el **bloque entero**.

## La idea en una fórmula

Repetir es **estirar un eje**. Con `repeats=r` constante, el eje `p` se multiplica por `r` y el
resto del shape no cambia:

$$ (n_0,\dots,n_p,\dots,n_{k-1}) \;\xrightarrow{\ \text{repeat}=r,\ \text{axis}=p\ }\; (n_0,\dots,n_p\cdot r,\dots,n_{k-1}) $$

Si `repeats` es un **array** $(r_0,\dots,r_{n_p-1})$ (una cuenta por elemento del eje), el tamaño
nuevo es la **suma** de las repeticiones, no un producto:

$$ n_p \;\xrightarrow{\ \text{repeats}=(r_0,\dots,r_{n_p-1})\ }\; \textstyle\sum_{i} r_i $$

Por índices, en 1D cada posición de salida copia el elemento de entrada cuyo "bloque" la contiene.
Para `[a, b]` con `r=3`:

$$ [\,a,\ b\,] \;\xrightarrow{\ r=3\ }\; [\,a,\ a,\ a,\ b,\ b,\ b\,] $$

## Firma

```python
np.repeat(
    a,             # array_like: el array de entrada
    repeats,       # int | array_like[int]: cuántas veces se repite (global o por elemento)
    axis=None,     # None | int: eje a lo largo del cual repetir (None aplana primero)
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Sus elementos son la
**unidad atómica** que se duplica.

### `repeats` — cuántas veces se repite cada elemento
El parámetro central. Dos formas:
- **`int`** — todos los elementos del eje se repiten el **mismo** número de veces.
- **`array_like[int]`** — una cuenta por elemento a lo largo del eje; permite repeticiones
  **desiguales**. Su longitud debe igualar el tamaño de ese eje (o ser un escalar broadcasteable).

```python
np.repeat([1, 2, 3], 2)            # [1, 1, 2, 2, 3, 3]   → r constante
np.repeat([1, 2, 3], [1, 2, 3])    # [1, 2, 2, 3, 3, 3]   → r por elemento
```

### `axis` — a lo largo de qué eje se repite
`None` (defecto) **aplana** el array a 1D y repite sobre esa secuencia. Un `int` repite a lo largo de
ese [[concepto_axis_parametro|eje]] conservando los demás: con `axis=0` duplica **filas**, con
`axis=1` duplica **columnas**.

```python
M = np.array([[1, 2], [3, 4]])
np.repeat(M, 2, axis=0)   # [[1,2],[1,2],[3,4],[3,4]]   → (4, 2)
np.repeat(M, 2, axis=1)   # [[1,1,2,2],[3,3,4,4]]       → (2, 4)
```

## El caso N-D

La regla es mecánica: **solo el eje de `axis` se multiplica**; los otros no se tocan. Con `axis=None`
el resultado es siempre 1D de longitud `size * r`.

| `a.shape` | `repeats` | `axis` | salida | lectura |
|-----------|-----------|--------|--------|---------|
| `(n,)` | `r` | `None`/`0` | `(n·r,)` | cada elemento `r` veces |
| `(n,)` | `[r_0,…]` | `0` | `(Σ r_i,)` | repeticiones desiguales |
| `(m, n)` | `r` | `0` | `(m·r, n)` | cada **fila** `r` veces |
| `(m, n)` | `r` | `1` | `(m, n·r)` | cada **columna** `r` veces |
| `(m, n)` | `r` | `None` | `(m·n·r,)` | aplana y repite |
| `(b, h, w)` | `r` | `-1` | `(b, h, w·r)` | estira la última dimensión |

```python
T = np.arange(2*3).reshape(2, 3)
np.repeat(T, 3, axis=0).shape   # (6, 3)  → el eje 0 se triplica
np.repeat(T, 2, axis=1).shape   # (2, 6)  → el eje 1 se duplica
```

## Vectorización

`np.repeat` reemplaza el bucle que construye una lista repitiendo elementos. La versión vectorizada
recorre el eje en C y materializa la copia de una vez, sin objetos Python por elemento:

```python
# Bucle Python (lento, explícito):
def repetir(a, r):
    out = []
    for x in a:
        out += [x] * r
    return np.array(out)

# Vectorizado:
np.repeat(a, r)
```

Es la versión "estiramiento de eje" del mismo principio de [[concepto_vectorizacion]]: describes
*cuánto* crece el eje, no *cómo* iterar para llenarlo.

## Valor de retorno

Siempre un **`ndarray` nuevo** (nunca una vista: materializa los datos duplicados), con el `dtype` de
`a` conservado.

| Entrada | `repeats` | `axis` | salida (shape) |
|---------|-----------|--------|----------------|
| `(n,)` | `r` | `None`/`0` | `(n·r,)` |
| `(m, n)` | `r` | `0` | `(m·r, n)` |
| `(m, n)` | `r` | `1` | `(m, n·r)` |
| `(m, n)` | `[r_0,…,r_{m-1}]` | `0` | `(Σ r_i, n)` |
| cualquiera | `r` | `None` | `(size·r,)` 1D |

## Casos de uso

### Expandir etiquetas por conteo de grupo
```python
clases  = np.array([0, 1, 2])
conteos = np.array([3, 2, 4])
np.repeat(clases, conteos)   # [0,0,0,1,1,2,2,2,2]  → repeticiones desiguales
```

### Repetir cada fila de una matriz `(2,2)`
Con `axis=0` cada fila se duplica in situ (no se intercala el bloque entero). El eje 0 pasa de 2 a 4:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\;\xrightarrow{\ \text{repeat}=2,\ \text{axis}=0\ }\;
\begin{bmatrix} 1 & 2 \\ 1 & 2 \\ 3 & 4 \\ 3 & 4 \end{bmatrix}
$$

```python
M = np.array([[1, 2], [3, 4]])
np.repeat(M, 2, axis=0).shape   # (4, 2)  → cada fila dos veces seguida
```

### Upsample espacial de imágenes repitiendo filas y columnas
Encadenar `repeat` en los dos ejes espaciales hace *nearest-neighbour upsampling*: cada píxel pasa a ocupar un bloque `2×2`:

$$
\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}
\;\xrightarrow{\ \text{axis}=0,\ \text{axis}=1\ }\;
\begin{bmatrix} 1 & 1 & 2 & 2 \\ 1 & 1 & 2 & 2 \\ 3 & 3 & 4 & 4 \\ 3 & 3 & 4 & 4 \end{bmatrix}
$$

```python
# Lote de imágenes (N, C, H, W): doblamos alto y ancho
x = np.arange(8*3*32*32).reshape(8, 3, 32, 32)
grande = np.repeat(np.repeat(x, 2, axis=2), 2, axis=3)
grande.shape   # (8, 3, 64, 64)  → N y C intactos, H y W ×2
```

### Duplicar el lote completo en un tensor 4D `(N, C, H, W)`
Repetir sobre `axis=0` clona cada imagen del lote (útil para *test-time augmentation* o emparejar tamaños de batch). Solo crece el eje del lote:

```python
x = np.arange(8*3*32*32).reshape(8, 3, 32, 32)   # (N=8, C=3, H=32, W=32)
np.repeat(x, 2, axis=0).shape                     # (16, 3, 32, 32)
# eje 0 (lote): 8 → 16 ; canales y espacio sin tocar
```

### Replicar fotogramas en un tensor de vídeo 5D `(N, T, C, H, W)`
En un lote de clips, `axis=1` es el tiempo `T`. Repetir ese eje **duplica cada fotograma** (slow-motion ingenuo / aumentar la tasa temporal); el resto del shape no cambia:

```python
video = np.zeros((4, 8, 3, 32, 32))   # (N=4, T=8, C=3, H=32, W=32)
np.repeat(video, 3, axis=1).shape     # (4, 24, 3, 32, 32)
# eje 1 (tiempo): 8 → 24 ; lote, canales y espacio intactos
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Matriz aplanada inesperadamente | `axis=None` por defecto | pasar `axis` explícito |
| `operands could not be broadcast` | `repeats` array de largo distinto al eje | igualar longitud al tamaño del eje |
| Se quería `[1,2,1,2]` y salió `[1,1,2,2]` | se buscaba repetir el bloque | usar [[np.tile]] |
| Memoria alta | materializa todas las copias | si es para operar, considerar broadcasting |

## Notas relacionadas

- [[concepto_shape]] — el eje que crece en el mapa de shapes
- [[concepto_axis_parametro]] — qué eje se estira
- [[np.tile]] — repite el bloque entero (no el elemento)
- [[np.roll]] · [[np.pad]]
