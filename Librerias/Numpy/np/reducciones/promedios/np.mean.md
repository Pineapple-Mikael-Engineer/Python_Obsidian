---
title: np.mean — Media aritmética
aliases:
  - mean
  - np.mean
  - media
  - promedio
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_dtype

draft: false
---

# np.mean — Media aritmética

`np.mean` es una **reducción**: recorre un eje del tensor, lo **colapsa** y devuelve la media
aritmética (la suma de sus elementos dividida por cuántos hay) de ese eje. Igual que [[np.sum]],
convierte un `(2, 3)` en un `(3,)` o en un escalar; la diferencia es que **divide por el número de
elementos reducidos**. La pregunta clave al usarla no es "¿promedia?" sino **"¿qué eje desaparece?"**.

## La idea en una fórmula

Promediar es reducir un eje y dividir por su longitud. Para una matriz $A$ de shape $(m, n)$,
promediar sobre el eje `0` (las filas) produce un vector indexado por la columna $j$, donde se
suman los $m$ elementos del eje que se reduce y se divide por $m$:

**Mapa de shapes** — el eje $p$ que se reduce **desaparece** del shape (idéntico a `np.sum`):

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{mean, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

**Fórmula por índices** — promediando sobre el eje `0` (de longitud $m$):

$$
\bar{x}_j=\frac{1}{m}\sum_{i=0}^{m-1} a_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

El eje que aparece en el **subíndice del sumatorio** es el que se reduce y desaparece, y $m$ es
justo su longitud. Esa es toda la intuición de `axis` en una reducción (ver
[[concepto_axis_parametro]]).

## Firma

```python
np.mean(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    dtype=None,        # dtype: tipo del acumulador interno (precisión)
    out=None,          # ndarray: destino preasignado
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
    where=True,        # array_like[bool]: qué elementos entran en la media
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. El resultado es
**siempre flotante** aunque `a` sea entero (la división lo fuerza).

### `axis` — qué eje se reduce
El parámetro central. `None` (defecto) promedia **todos** los elementos y devuelve un escalar. Un
`int` reduce ese eje. Una **tupla** reduce varios ejes a la vez (la media se calcula sobre todos
los elementos de esos ejes en conjunto):

```python
T = np.ones((2, 3, 4))
np.mean(T, axis=None).shape    # ()      → escalar, se reducen los 3 ejes
np.mean(T, axis=0).shape       # (3, 4)  → desaparece el eje 0
np.mean(T, axis=1).shape       # (2, 4)  → desaparece el eje 1
np.mean(T, axis=(0, 2)).shape  # (3,)    → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje), lo idiomático para "media de la última dimensión".

### `dtype` — precisión del acumulador
Fija el tipo en el que se **acumula** la suma antes de dividir, no solo el del resultado. Con
entrada `int` o `float16` el acumulador hereda un tipo de poca precisión y la media puede perder
exactitud o desbordar; conviene `dtype=np.float64` (ver [[concepto_dtype]]):

```python
arr = np.full(1000, 200, dtype=np.int16)
np.mean(arr)                  # acumula en float estrecho → puede perder precisión
np.mean(arr, dtype=np.float64)  # 200.0  ← acumulador seguro
```
Para `float64` rara vez hace falta; para `int*`/`float16` masivos, fíjalo.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype del resultado. Evita una asignación de memoria; útil en
bucles. Debe tener el shape exacto de salida.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Sirve para que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]), justo lo que se
necesita al **centrar** datos:

```python
M = np.array([[1., 2.], [3., 4.]])
M.mean(axis=1).shape              # (2,)    → no broadcastea de vuelta a (2,2)
M.mean(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
M - M.mean(axis=1, keepdims=True)    # centra cada fila (media 0)
```

### `where` — media condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo entran en el cálculo (numerador y conteo del
denominador) los elementos donde `where` es `True`; es como promediar sobre el subconjunto sin
crear el array filtrado. Es el modo idiomático de ignorar `NaN` sin [[np.nanmean]]:

```python
arr = np.array([1, 2, np.nan, 4])
np.mean(arr, where=~np.isnan(arr))   # 2.333  → ignora el NaN del conteo y la suma
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Conviene leerlo como "para cada combinación de los ejes que **sobreviven**, promedio a lo largo del
que se reduce".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar | media de todo |
| `(m, n)` | `0` | `(n,)` | una media por **columna** |
| `(m, n)` | `1` | `(m,)` | una media por **fila** |
| `(m, n)` | `None` | `()` | media total |
| `(b, m, n)` | `0` | `(m, n)` | media **a lo largo del lote**: matriz media |
| `(b, m, n)` | `(1, 2)` | `(b,)` | una media por cada matriz del lote |
| `(b, m, n)` | `-1` | `(b, m)` | media de la última dimensión |

```python
# Tensor (d0, d1, d2) = (3, 2, 4): 3 láminas de 2x4
T = np.arange(3*2*4).reshape(3, 2, 4)
T.mean(axis=0).shape       # (2, 4)  → lámina "media" sobre las 3 láminas
T.mean(axis=(1, 2)).shape  # (3,)    → una media por lámina
T.mean(axis=-1).shape      # (3, 2)  → colapsa la última dimensión
```
Con `keepdims=True`, cualquiera de esos resultados conserva los ejes reducidos en tamaño 1
(`(1, 2, 4)`, `(3, 1, 1)`...), listo para broadcastear contra `T`.

## Vectorización

`np.mean` reemplaza un bucle de acumulación-y-división escrito a mano. Las dos versiones dan lo
mismo, pero la vectorizada corre en C sobre memoria contigua en vez de en el intérprete de Python:

```python
# Bucle Python (lento, explícito):
def media_cols(M):
    m, n = M.shape
    out = np.zeros(n)
    for j in range(n):
        for i in range(m):
            out[j] += M[i, j]
        out[j] /= m
    return out

# Vectorizado (NumPy recorre el eje 0 en C y divide de golpe):
M.mean(axis=0)
```
NumPy describe *qué* eje reducir, no *cómo* iterar: es el mismo principio de
[[concepto_vectorizacion]]. Por eso `axis` es el lenguaje natural —pides la media sobre una
dimensión entera de una vez—.

## Valor de retorno

El **shape** depende de `axis`/`keepdims`; el **tipo es siempre flotante**:

| Entrada (dtype) | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` int/float | `None` | `False` | `()` | **escalar de NumPy** (`np.float64`) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` (float) |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` (float) |
| `(n,)` | `0` | `False` | `()` | escalar float |

Reglas de `dtype` de salida (sin `dtype=` explícito):
- enteros y `bool` → se promueven a `float64` (la división siempre da float).
- `float32` → `float32`; `float16` → `float16` (de ahí el riesgo de precisión: usa `dtype=`).
- `complex` → conserva su tipo complejo.

```python
np.array([1, 2, 3, 4]).mean()        # np.float64(2.5)  escalar, no ndarray
type(np.ones((2, 2)).mean(axis=0))   # numpy.ndarray
np.ones((2, 2), dtype=np.float32).mean(axis=0).dtype  # float32
```

## Casos de uso

### Media global, por columna y por fila
```python
notas = np.array([[4., 6., 8.], [5., 7., 9.]])
notas.mean()          # 6.5            media de todo
notas.mean(axis=0)    # [4.5, 6.5, 8.5]  media por asignatura (columna)
notas.mean(axis=1)    # [6., 7.]       media por alumno (fila)
```

### Centrar datos (reducción + broadcasting)
```python
datos = np.random.rand(100, 4)
centrado = datos - datos.mean(axis=0, keepdims=True)  # cada feature con media 0
```

### Ignorar NaN sin np.nanmean
```python
x = np.array([1., 2., np.nan, 4.])
np.mean(x, where=~np.isnan(x))   # 2.333
```

### N-D trabajado: media por feature de un lote `(b, n)`
```python
lote = np.array([[1., 2., 3.],     # muestra 0
                 [3., 4., 5.],     # muestra 1
                 [5., 6., 7.],     # muestra 2
                 [7., 8., 9.]])    # muestra 3   → shape (4, 3): 4 muestras, 3 features
lote.mean(axis=0)   # [4., 5., 6.]  → media de cada feature sobre las 4 muestras
lote.mean(axis=1)   # [2., 4., 6., 8.]  → media de los 3 features por muestra
# El eje 0 (las muestras) desaparece en el primer caso; el eje 1 (features) en el segundo.
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado `NaN` | el array contiene `NaN` (se propaga) | [[np.nanmean]] o `where=~np.isnan(a)` |
| Pérdida de precisión | acumulador `int`/`float16` | `dtype=np.float64` |
| Broadcasting falla al centrar | se perdió el eje reducido | `keepdims=True` |
| Media engañosa | hay outliers que la desplazan | usar [[np.median]] |
| Sentido de `axis` invertido | confundir "media de filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[concepto_dtype]] — precisión del acumulador
- [[np.sum]] · [[np.average]] · [[np.median]] · [[np.std]] · [[np.nanmean]]
