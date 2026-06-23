---
title: np.prod — multiplica (reduce) los elementos a lo largo de un eje
aliases:
  - prod
  - np.prod
  - producto
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

# np.prod — multiplica (reduce) los elementos a lo largo de un eje

`np.prod` es una **reducción**: recorre un eje del tensor y lo **colapsa** a un solo valor
**multiplicando** sus elementos. Es la gemela multiplicativa de [[np.sum]] —misma mecánica de `axis`,
mismo "¿qué eje desaparece?"— pero con un riesgo añadido: los productos **crecen mucho más rápido**
que las sumas, así que el overflow es la trampa principal. La pregunta al usarla sigue siendo
**"¿qué eje desaparece?"**, con la coletilla **"¿y desbordará?"**.

## La idea en una fórmula

Multiplicar es reducir un eje (igual que sumar, cambiando $\sum$ por $\prod$). El **mapa de shapes**
es idéntico al de `np.sum`: el eje reducido **desaparece** del shape.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{prod, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

Para una matriz $A$ de shape $(m, n)$, el producto sobre el eje `0` produce un vector indexado por la
columna $j$:

$$
p_j = \prod_{i=0}^{m-1} A_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

y el producto sobre el eje `1` produce un vector indexado por la fila $i$:

$$
r_i = \prod_{j=0}^{n-1} A_{ij} \qquad \text{(axis=1, desaparece el eje } j\text{)}
$$

El eje del **subíndice del productorio** es el que se reduce y desaparece. Con `axis=None` se
multiplican **todos** los elementos a un escalar. El **producto vacío vale 1** (el elemento neutro,
ver `initial`), igual que la suma vacía vale 0.

## Firma

```python
np.prod(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    dtype=None,        # dtype: tipo del acumulador y del resultado
    out=None,          # ndarray: destino preasignado
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
    initial=1,         # escalar: valor inicial del acumulador (neutro = 1)
    where=True,        # array_like[bool]: qué elementos entran en el producto
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Su `dtype` determina el
acumulador por defecto, y con ello el riesgo de overflow (ver `dtype`), que aquí es **agudo**.

### `axis` — qué eje se reduce
El parámetro central. `None` (defecto) multiplica **todos** los elementos y devuelve un escalar. Un
`int` reduce ese eje. Una **tupla** reduce varios ejes a la vez:

```python
T = np.ones((2, 3, 4))
np.prod(T, axis=None).shape    # ()      → escalar, se reducen los 3 ejes
np.prod(T, axis=0).shape       # (3, 4)  → desaparece el eje 0
np.prod(T, axis=1).shape       # (2, 4)  → desaparece el eje 1
np.prod(T, axis=(0, 2)).shape  # (3,)    → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje), lo idiomático para "multiplicar la última dimensión"
sin importar cuántas haya. La semántica del eje es exactamente la de [[concepto_axis_parametro]].

### `dtype` — tipo del acumulador (overflow, la trampa AGUDA)
Fija el tipo en el que se **acumula** el producto. Es **más peligroso** que en la suma: los productos
escalan **exponencialmente**, así que un `int64` desborda con muy pocos factores y lo hace **en
silencio** (resultado negativo o absurdo, no excepción):

```python
np.prod(np.arange(1, 21))                # 20! desborda int64 → resultado erróneo, sin aviso
np.prod(np.arange(1, 21), dtype=np.float64)  # 2.43e18  → seguro (pierde exactitud al final)
arr = np.array([10, 10, 10], dtype=np.int8)  # int8 llega a 127
np.prod(arr)               # -24  ← overflow silencioso (1000 mod 256)
np.prod(arr, dtype=np.int64)  # 1000
```
Regla práctica: en cuanto multipliques más de un puñado de enteros, **fija `dtype`** (a `int64` si
necesitas exactitud y cabe; a `float64` si priorizas no desbordar). Ver [[concepto_dtype]].

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Mantiene el resultado
**broadcasteable** contra el array original (ver [[concepto_broadcasting]]).

```python
M = np.array([[1, 2], [3, 4]])
M.prod(axis=1).shape                 # (2,)    → no broadcastea de vuelta a (2,2)
M.prod(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype del resultado. Evita una asignación de memoria; útil en
bucles. Debe tener el shape exacto de salida.

### `initial` — valor inicial del acumulador (neutro = 1)
Escalar que se multiplica **antes** que los datos. Su neutro es `1` (no `0` como en la suma). Permite
arrancar de un factor previo y, sobre todo, es lo que da sentido al **producto de un eje vacío**:

```python
np.prod([])               # 1.0   → producto vacío = neutro multiplicativo
np.prod([2, 3], initial=10)  # 60  → 10 · 2 · 3
```

### `where` — producto condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo entran en el producto los elementos donde `where`
es `True`; es aplicar la máscara sin construir el array filtrado.

```python
arr = np.array([2, 0, 3, 0, 4])
np.prod(arr, where=arr != 0)   # 24  → ignora los ceros
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
"Para cada combinación de los ejes que **sobreviven**, multiplico a lo largo del que se reduce".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar | producto de todo |
| `(m, n)` | `0` | `(n,)` | un producto por **columna** |
| `(m, n)` | `1` | `(m,)` | un producto por **fila** |
| `(m, n)` | `None` | `()` | producto total |
| `(b, m, n)` | `0` | `(m, n)` | producto **a lo largo del lote** |
| `(b, m, n)` | `(1, 2)` | `(b,)` | un producto por cada matriz del lote |
| `(b, m, n)` | `-1` | `(b, m)` | multiplica la última dimensión |

```python
# Tensor (2, 2, 3): un lote de 2 matrices 2x3
T = np.array([[[1, 2, 3],
               [4, 5, 6]],
              [[1, 1, 2],
               [2, 2, 2]]])
T.prod(axis=0)   # (2, 3) → multiplica las dos matrices celda a celda: [[1,2,6],[8,10,12]]
T.prod(axis=2)   # (2, 2) → producto de cada fila: [[6, 120], [2, 8]]
T.prod(axis=(1, 2))  # (2,) → un producto por matriz: [720, 16]
```
Con `keepdims=True` esos resultados conservan los ejes reducidos en tamaño 1 (`(1, 2, 3)`, `(2, 2, 1)`,
`(2, 1, 1)`), listos para broadcastear contra `T`.

## Vectorización

`np.prod` reemplaza un bucle de acumulación multiplicativa escrito a mano. Ambas versiones dan lo
mismo, pero la vectorizada corre en C sobre memoria contigua en lugar de en el intérprete de Python:

```python
# Bucle Python (lento, explícito):
def prod_cols(M):
    m, n = M.shape
    out = np.ones(n)
    for i in range(m):
        for j in range(n):
            out[j] *= M[i, j]
    return out

# Vectorizado (NumPy recorre el eje 0 en C):
M.prod(axis=0)
```
NumPy no "evita" el producto: lo ejecuta como un recorrido optimizado del eje, sin crear objetos
Python por elemento. Es el mismo principio de [[concepto_vectorizacion]]: describes *qué* eje reducir,
no *cómo* iterar.

## Valor de retorno

El tipo del retorno **depende de `axis`** y de la promoción de `dtype`:

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar de NumPy** (`np.int64`, `np.float64`...) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` |
| `(n,)` | `0` | `False` | `()` | escalar |

Reglas de `dtype` de salida (sin `dtype=` explícito):
- enteros de < `int_` (`int8`, `int16`, `int32`) se **promueven** al entero por defecto de la
  plataforma (`int64` en 64 bits) — pero esto **no basta** para evitar overflow en productos largos.
- `bool` se promueve a `int64` → `mascara.prod()` da 1 solo si **todos** son `True` (equivale a un AND).
- floats y complejos conservan su tipo (`float32` → `float32`).

```python
np.array([1, 2, 3]).prod()        # np.int64(6)   escalar, no ndarray
type(np.ones((2, 2)).prod(axis=0))  # numpy.ndarray
np.array([True, True, False]).prod()  # 0  → un False anula el producto (AND)
```

## Casos de uso

### Tamaño total a partir de un shape
```python
shape = (3, 4, 5)
np.prod(shape)   # 60  → número de elementos de un array con ese shape
```

### Probabilidad conjunta de eventos independientes (y por qué el log)
```python
p = np.array([0.9, 0.8, 0.95])
np.prod(p)   # 0.684  → probabilidad conjunta
```
Con muchas probabilidades pequeñas el producto **subdesborda** hacia 0; lo robusto es sumar logaritmos:
`np.exp(np.sum(np.log(p)))` en lugar de `np.prod(p)`.

### Producto condicional ignorando ceros
```python
arr = np.array([2, 0, 3, 4, 0])
np.prod(arr, where=arr != 0)   # 24  → sin la máscara daría 0
```

### Ejemplo trabajado en N-D
```python
T = np.array([[[1, 2, 3],
               [4, 5, 6]],
              [[1, 1, 2],
               [2, 2, 2]]])     # shape (2, 2, 3)

T.prod(axis=2)        # (2, 2) → producto de cada fila
# [[  6, 120],        ← 1·2·3=6, 4·5·6=120
#  [  2,   8]]        ← 1·1·2=2, 2·2·2=8

T.prod(axis=(1, 2))   # (2,)   → un producto por matriz del lote
# [720, 16]           ← 6·120=720, 2·8=16
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado negativo/absurdo | overflow del acumulador (crece exponencial) | `dtype=np.int64` o `np.float64` |
| Resultado 0 inesperado | algún elemento es 0 (anula todo el producto) | revisar datos o `where=a != 0` |
| Subdesbordamiento a 0 | producto de muchas probabilidades < 1 | sumar logaritmos: `exp(sum(log(p)))` |
| `NaN` en el resultado | el array contiene `NaN` (se propaga) | usar [[np.nanprod]] |
| Broadcasting falla tras multiplicar | se perdió el eje reducido | `keepdims=True` |
| Sentido de `axis` invertido | confundir "multiplico filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_dtype]] — la promoción del acumulador y el overflow
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[np.sum]] · [[np.cumprod]] · [[np.nanprod]]
