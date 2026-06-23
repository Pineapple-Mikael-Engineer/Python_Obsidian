---
title: np.sum — suma (reduce) los elementos a lo largo de un eje
aliases:
  - sum
  - np.sum
  - suma
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
  - concepto_dtype

draft: false
---

# np.sum — suma (reduce) los elementos a lo largo de un eje

`np.sum` es una **reducción**: recorre un eje del tensor y lo **colapsa** a un solo valor sumando
sus elementos. Es la operación que convierte un `(2, 3)` en un `(3,)` (sumando las filas) o en un
escalar (sumando todo). La pregunta que siempre hay que responder al usarla no es "¿suma?" sino
**"¿qué eje desaparece?"**.

## La idea en una fórmula

Sumar es reducir un eje. Para una matriz $A$ de shape $(m, n)$, sumar sobre el eje `0` (las filas)
produce un vector indexado por la columna $j$:

$$
s_j = \sum_{i=0}^{m-1} A_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

y sumar sobre el eje `1` produce un vector indexado por la fila $i$:

$$
r_i = \sum_{j=0}^{n-1} A_{ij} \qquad \text{(axis=1, desaparece el eje } j\text{)}
$$

El eje que aparece en el **subíndice del sumatorio** es el que se reduce y **desaparece** del shape.
Esa es toda la intuición de `axis` en una reducción (ver [[concepto_axis_parametro]]).

## Firma

```python
np.sum(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    dtype=None,        # dtype: tipo del acumulador y del resultado
    out=None,          # ndarray: destino preasignado
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
    initial=0,         # escalar: valor inicial del acumulador
    where=True,        # array_like[bool]: qué elementos entran en la suma
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Su `dtype` determina
el acumulador por defecto (y con ello el riesgo de overflow, ver `dtype`).

### `axis` — qué eje se reduce
El parámetro central. `None` (defecto) suma **todos** los elementos y devuelve un escalar. Un `int`
reduce ese eje. Una **tupla** reduce varios ejes a la vez:

```python
T = np.ones((2, 3, 4))
np.sum(T, axis=None).shape    # ()      → escalar, se reducen los 3 ejes
np.sum(T, axis=0).shape       # (3, 4)  → desaparece el eje 0
np.sum(T, axis=1).shape       # (2, 4)  → desaparece el eje 1
np.sum(T, axis=(0, 2)).shape  # (3,)    → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje), lo idiomático para "sumar la última dimensión"
sin importar cuántas haya.

### `dtype` — tipo del acumulador (la trampa del overflow)
Fija el tipo en el que se **acumula** la suma, no solo el del resultado. Es crítico con enteros de
pocos bits: el acumulador hereda el `dtype` de `a` y puede **desbordar en silencio**.

```python
arr = np.ones(300, dtype=np.int8)   # int8 llega hasta 127
arr.sum()                 # -44  ← overflow silencioso (300 mod 256)
arr.sum(dtype=np.int64)   # 300  ← acumulador seguro
```
Para floats rara vez hace falta; para `bool`/`int8`/`int16` que vas a sumar en masa, fíjalo.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Sirve para que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]).

```python
M = np.array([[1, 2], [3, 4]])
M.sum(axis=1).shape              # (2,)    → no broadcastea de vuelta a (2,2)
M.sum(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
M / M.sum(axis=1, keepdims=True)    # normaliza cada fila (suma 1)
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype del resultado. Evita una asignación de memoria; útil en
bucles. Debe tener el shape exacto de salida.

### `initial` — valor inicial del acumulador
Escalar que se suma **antes** que los datos (el "elemento neutro" de partida, por defecto `0`).
Permite fijar un piso o sumar a un total previo. Es el único modo de que una suma sobre un eje
**vacío** no sea simplemente `0`:

```python
np.sum([], initial=10)              # 10.0
np.sum([[1, 2], [3, 4]], initial=100)  # 110
```

### `where` — suma condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo entran en la suma los elementos donde `where` es `True`; es como aplicar la máscara sin crear el array filtrado.

```python
arr = np.array([1, -2, 3, -4])
np.sum(arr, where=arr > 0)   # 4  → solo los positivos
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Conviene leerlo como "para cada combinación de los ejes que **sobreviven**, sumo a lo largo del que
se reduce".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar | suma todo |
| `(m, n)` | `0` | `(n,)` | una suma por **columna** |
| `(m, n)` | `1` | `(m,)` | una suma por **fila** |
| `(m, n)` | `None` | `()` | suma total |
| `(b, m, n)` | `0` | `(m, n)` | suma **a lo largo del lote**: matriz promedio acumulada |
| `(b, m, n)` | `(1, 2)` | `(b,)` | un total por cada matriz del lote |
| `(b, m, n)` | `-1` | `(b, m)` | suma la última dimensión |

```python
# Tensor (lote de 5 imágenes RGB 2x2):  (5, 2, 2, 3)
imgs = np.arange(5*2*2*3).reshape(5, 2, 2, 3)
imgs.sum(axis=(1, 2)).shape   # (5, 3)  → suma espacial: un vector RGB por imagen
imgs.sum(axis=0).shape        # (2, 2, 3) → imagen "acumulada" sobre el lote
imgs.sum(axis=-1).shape       # (5, 2, 2) → colapsa el canal de color
```
Con `keepdims=True`, cualquiera de esos resultados conserva los ejes reducidos en tamaño 1
(`(5, 1, 1, 3)`, `(1, 2, 2, 3)`...), listo para broadcastear contra `imgs`.

## Vectorización

`np.sum` reemplaza un bucle de acumulación escrito a mano. Las dos versiones dan lo mismo, pero la
vectorizada corre en C sobre memoria contigua en vez de en el intérprete de Python:

```python
# Bucle Python (lento, explícito):
def suma_cols(M):
    m, n = M.shape
    out = np.zeros(n)
    for i in range(m):
        for j in range(n):
            out[j] += M[i, j]
    return out

# Vectorizado (NumPy recorre el eje 0 en C):
M.sum(axis=0)
```
NumPy no "evita" la suma: la ejecuta como un recorrido optimizado del eje, sin crear objetos Python
por elemento. Es el mismo principio de [[concepto_vectorizacion]]: describes *qué* eje reducir, no
*cómo* iterar. Por eso `axis` es el lenguaje natural —pides la reducción sobre una dimensión entera
de golpe—.

## Valor de retorno

El tipo del retorno **depende de `axis`** y el `dtype` de la promoción:

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar de NumPy** (`np.int64`, `np.float64`...) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` |
| `(n,)` | `0` | `False` | `()` | escalar |

Reglas de `dtype` de salida (sin `dtype=` explícito):
- enteros de < `int_` (p. ej. `int8`, `int16`) se **promueven** al entero por defecto de la
  plataforma (`int64` en 64 bits) para reducir overflow.
- `bool` se promueve a `int64` → por eso `mascara.sum()` **cuenta** (`True`=1).
- floats y complejos conservan su tipo (`float32` → `float32`).

```python
np.array([1, 2, 3]).sum()         # np.int64(6)      escalar, no ndarray
type(np.ones((2,2)).sum(axis=0))  # numpy.ndarray
(np.array([True, True, False])).sum()  # 2  → cuenta de True
```

## Casos de uso

### Total, subtotales y conteo
```python
ventas = np.array([[100, 200], [150, 250]])
ventas.sum()          # 700           total
ventas.sum(axis=0)    # [250, 450]    por producto (columna)
(ventas > 180).sum()  # 2             cuántas celdas superan 180
```

### Normalizar filas (reducción + broadcasting)
```python
P = np.array([[2., 1., 1.], [0., 3., 1.]])
P / P.sum(axis=1, keepdims=True)   # cada fila suma 1 (distribución)
```

### Reducción parcial de un tensor N-D
```python
batch = np.random.rand(32, 10)     # 32 muestras, 10 features
batch.sum(axis=0).shape            # (10,)  → suma por feature sobre el lote
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado negativo/absurdo | overflow del acumulador (`int8`/`int16`) | `dtype=np.int64` |
| `NaN` en el resultado | el array contiene `NaN` (se propaga) | usar [[np.nansum]] |
| Broadcasting falla tras sumar | se perdió el eje reducido | `keepdims=True` |
| Sentido de `axis` invertido | confundir "sumo filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |
| Suma de eje vacío da 0 inesperado | no se fijó `initial` | `initial=...` o validar antes |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[concepto_broadcasting]] — `keepdims` para reinsertar el resultado
- [[np.prod]] · [[np.cumsum]] · [[np.mean]] · [[np.nansum]]
