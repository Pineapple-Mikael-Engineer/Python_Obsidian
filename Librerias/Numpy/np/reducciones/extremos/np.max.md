---
title: np.max — máximo (reduce) a lo largo de un eje
aliases:
  - max
  - np.max
  - amax
  - maximo
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion

draft: false
---

# np.max — máximo (reduce) a lo largo de un eje

`np.max` es una **reducción**: recorre un eje del tensor y lo **colapsa** a un solo valor quedándose
con el **mayor** de sus elementos. Convierte un `(2, 3)` en un `(3,)` (el máximo de cada columna) o
en un escalar (el máximo global). Como toda reducción, la pregunta no es "¿el máximo?" sino
**"¿qué eje desaparece?"**. Es alias de `np.amax`.

## La idea en una fórmula

Tomar el máximo es reducir un eje quedándose con el extremo superior. Para una matriz $A$ de shape
$(m, n)$, reducir el eje `0` (las filas) produce un vector indexado por la columna $j$:

$$
M_j = \max_{i=0}^{m-1} A_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

El **mapa de shapes** es el de cualquier reducción: el eje de `axis` se elimina del shape.

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{max, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

El eje que aparece bajo el operador $\max$ es el que se reduce y **desaparece** del shape (ver
[[concepto_axis_parametro]]). Con `keepdims=True` queda en tamaño 1; con `axis=None` se contraen
todos los ejes a un escalar `()`.

## Firma

```python
np.max(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    out=None,          # ndarray: destino preasignado
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
    initial=<sin valor>,  # escalar: cota inferior de partida
    where=True,        # array_like[bool]: qué elementos compiten
) -> ndarray | escalar
```

`np.max` es un alias de `np.amax`.

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. El `dtype` se conserva
en el resultado (a diferencia de [[np.sum]], aquí no hay promoción: el máximo de `int8` es `int8`).

### `axis` — qué eje se reduce
El parámetro central. `None` (defecto) busca el máximo de **todos** los elementos y devuelve un
escalar. Un `int` reduce ese eje. Una **tupla** reduce varios ejes a la vez:

```python
T = np.arange(2*3*4).reshape(2, 3, 4)
np.max(T, axis=None)      # escalar: el máximo global
np.max(T, axis=0).shape   # (3, 4)  → desaparece el eje 0
np.max(T, axis=1).shape   # (2, 4)  → desaparece el eje 1
np.max(T, axis=(0, 2)).shape  # (3,) → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje), lo idiomático para "el máximo de la última
dimensión" sin importar cuántas haya.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Sirve para que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]); es el patrón de
la normalización min-max.

```python
M = np.array([[1, 9, 3], [7, 2, 8]])
M.max(axis=1).shape              # (2,)    → no broadcastea de vuelta a (2,3)
M.max(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
M - M.max(axis=1, keepdims=True)    # resta el máximo de cada fila (≤ 0)
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype del resultado. Evita una asignación de memoria; útil en
bucles. Debe tener el shape exacto de salida.

### `initial` — cota inferior de partida
Escalar contra el que también se compara, como un "piso" del máximo. Por defecto **no hay valor**:
el máximo sale solo de los datos. Es el único modo de que un máximo sobre un eje **vacío** no lance
error (no existe un máximo de cero elementos):

```python
np.max([], initial=-1)                 # -1.0  → sin initial, ValueError
np.max([2, 5, 1], initial=10)          # 10    → el piso gana
np.max([2, 5, 1], initial=0)           # 5     → los datos ganan
```

### `where` — máximo condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo **compiten** los elementos donde `where` es
`True`. **Requiere `initial`**: si toda una reducción queda enmascarada, el resultado es `initial`
(sin él no habría candidato y fallaría).

```python
arr = np.array([1, -2, 3, -4])
np.max(arr, where=arr > 0, initial=0)   # 3  → solo entre los positivos
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Léelo como "para cada combinación de los ejes que **sobreviven**, me quedo con el máximo a lo largo
del que se reduce".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar | máximo global |
| `(m, n)` | `0` | `(n,)` | un máximo por **columna** |
| `(m, n)` | `1` | `(m,)` | un máximo por **fila** |
| `(m, n)` | `None` | `()` | máximo total |
| `(b, m, n)` | `0` | `(m, n)` | máximo **a lo largo del lote**, celda a celda |
| `(b, m, n)` | `(1, 2)` | `(b,)` | el pico de cada matriz del lote |
| `(b, m, n)` | `-1` | `(b, m)` | máximo de la última dimensión |

```python
# Lote de 5 imágenes RGB 2x2:  (5, 2, 2, 3)
imgs = np.arange(5*2*2*3).reshape(5, 2, 2, 3)
imgs.max(axis=(1, 2)).shape   # (5, 3)  → pico espacial: un máx por canal e imagen
imgs.max(axis=0).shape        # (2, 2, 3) → máximo píxel a píxel sobre el lote
imgs.max(axis=-1).shape       # (5, 2, 2) → colapsa el canal de color
```
Con `keepdims=True`, cualquiera de esos resultados conserva los ejes reducidos en tamaño 1
(`(5, 1, 1, 3)`, `(1, 2, 2, 3)`...), listo para broadcastear contra `imgs`.

## Vectorización

`np.max` reemplaza un bucle de comparación escrito a mano. Las dos versiones dan lo mismo, pero la
vectorizada corre en C sobre memoria contigua en vez de en el intérprete de Python:

```python
# Bucle Python (lento, explícito):
def max_cols(M):
    m, n = M.shape
    out = np.full(n, -np.inf)
    for i in range(m):
        for j in range(n):
            if M[i, j] > out[j]:
                out[j] = M[i, j]
    return out

# Vectorizado (NumPy recorre el eje 0 en C):
M.max(axis=0)
```
Es el mismo principio de [[concepto_vectorizacion]]: describes *qué* eje reducir, no *cómo* iterar.
Por eso `axis` es el lenguaje natural —pides la reducción sobre una dimensión entera de golpe—.

## Valor de retorno

El **tipo** del retorno depende de `axis`; el **dtype** se conserva (no hay promoción):

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar de NumPy** (`np.int64`, `np.float64`...) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` |
| `(n,)` | `0` | `False` | `()` | escalar |

```python
M = np.array([[1, 9, 3], [7, 2, 8]])
np.max(M)          # np.int64(9)   escalar, no ndarray
np.max(M, axis=0)  # [7, 9, 8]     ndarray, máximo por columna
np.max(M, axis=1)  # [9, 8]        ndarray, máximo por fila
```

> [!warning] Propaga NaN
> Si el array contiene un `NaN`, el resultado es `NaN` (cualquier `NaN` "gana" la comparación).
> Para **ignorar** los NaN usa [[np.nanmax]].
> ```python
> np.max([1.0, np.nan, 3.0])      # nan
> np.nanmax([1.0, np.nan, 3.0])   # 3.0
> ```

## Casos de uso

### Pico global y por eje
```python
M = np.array([[1, 9, 3], [7, 2, 8]])
np.max(M)          # 9            pico global
np.max(M, axis=0)  # [7, 9, 8]    máximo por columna
np.max(M, axis=1)  # [9, 8]       máximo por fila
```

### Normalización min-max (reducción + broadcasting)
```python
a = np.array([2., 5., 1., 8.])
norm = (a - np.min(a)) / (np.max(a) - np.min(a))   # a [0, 1]
```

### Estabilización del softmax (restar el máximo por fila)
```python
logits = np.array([[1., 2., 3.], [10., 20., 30.]])
z = logits - logits.max(axis=1, keepdims=True)   # evita overflow del exp
np.exp(z) / np.exp(z).sum(axis=1, keepdims=True)
```

### Reducción parcial en N-D (valores concretos)
```python
T = np.array([[[1, 8], [3, 2]],
              [[7, 4], [6, 5]]])      # shape (2, 2, 2)
T.max(axis=0)     # [[7, 8], [6, 5]]  → máximo entre las dos "láminas"
T.max(axis=(1, 2))  # [8, 7]          → el pico de cada lámina
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado `NaN` | el array contiene `NaN` (se propaga, "gana") | usar [[np.nanmax]] |
| Se quería la **posición**, no el valor | confundir máximo con su índice | [[np.argmax]] |
| Comparar dos arrays par a par no da lo esperado | `np.max` reduce **un** array, no compara dos | usar [[np.maximum]] (elemento a elemento) |
| `zero-size array to reduction` | máximo de un eje **vacío** | pasar `initial=...` |
| Broadcasting falla tras reducir | se perdió el eje reducido | `keepdims=True` |
| Sentido de `axis` invertido | confundir "máximo de filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[concepto_broadcasting]] — `keepdims` para reinsertar el resultado
- [[np.min]] · [[np.ptp]] · [[np.argmax]] · [[np.maximum]] · [[np.nanmax]]
