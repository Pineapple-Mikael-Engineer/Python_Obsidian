---
title: np.add — suma elemento a elemento (ufunc binaria)
aliases:
  - add
  - np.add
  - suma elemento a elemento
tags:
  - numpy
  - api/funcion
  - operaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs
  - concepto_broadcasting
  - concepto_dtype

draft: false
---

# np.add — suma elemento a elemento (ufunc binaria)

`np.add` es la **ufunc binaria** que suma dos tensores **posición a posición**. No reduce ningún
eje: recorre las entradas alineándolas por [[concepto_broadcasting|broadcasting]] y produce una
salida con la **shape común**. Es la función que respalda el operador `+`: `a + b` es exactamente
`np.add(a, b)`. La pregunta al usarla no es "¿qué eje desaparece?" (no desaparece ninguno) sino
**"¿qué shape común sale del broadcasting de las entradas?"**. Es el molde de toda ufunc binaria
element-wise (ver [[concepto_ufuncs]]).

## La idea en una fórmula

La operación es **elemento a elemento**: cada posición de la salida es la suma de las posiciones
correspondientes de las entradas, tras alinearlas por broadcasting.

$$
z_i = x_i + y_i
$$

y en N-D, con los índices recorriendo la shape común:

$$
z_{i_0\dots i_k} = x_{i_0\dots i_k} + y_{i_0\dots i_k}
$$

El **mapa de shapes es el de broadcasting**: las entradas se alinean **por la derecha**, se rellena
con `1` a la izquierda y cada eje toma el `max` (válido si en cada eje coinciden o uno es `1`):

$$
(\dots, a_{k-1}, a_k),\ (\dots, b_{k-1}, b_k)\ \xrightarrow{\ \text{broadcast}\ }\ (\dots,\,\max(a_{k-1},b_{k-1}),\,\max(a_k,b_k))
$$

```text
x      (2, 3)
y         (3,)  →  (1, 3)     ← rellena con 1 por la izquierda
---------------
eje -1:  3 vs 3  →  3
eje -2:  2 vs 1  →  2         ← uno es 1, se estira
---------------
z      (2, 3)
```

Toda la lógica de alineación vive en [[concepto_broadcasting]].

## Firma

```python
np.add(
    x1,                     # array_like: primer sumando
    x2,                     # array_like: segundo sumando
    /,
    out=None,               # ndarray | None: destino preasignado
    *,
    where=True,             # array_like[bool]: máscara de cómputo
    dtype=None,             # dtype: tipo de cómputo/salida
    casting='same_kind',    # política de conversión
    order='K',              # layout en memoria de la salida
) -> ndarray | escalar
```

## Los parámetros en detalle

### `x1`, `x2` — los sumandos
`array_like` (ndarray, lista, escalar). Deben ser **broadcasteables** entre sí; sus shapes se
alinean por la derecha. El `dtype` de salida sale de promover ambos (ver `dtype`). Si ambos son
escalares, el retorno es un escalar de NumPy, no un `ndarray`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida (la del broadcast). Evita asignar memoria nueva; útil
en bucles. Permite la **suma in-place** apuntando al propio operando:

```python
np.add(total, fila, out=total)   # acumula sobre total sin crear arrays temporales
```

### `where` — suma condicional (máscara)
`array_like` booleano broadcasteable con las entradas. Solo se calcula donde `where` es `True`; en
el resto, la salida **conserva lo que hubiera en `out`**. Por eso con `where` casi siempre se pasa
`out` explícito (si no, esas posiciones quedan sin inicializar):

```python
a = np.array([1, -2, 3, -4])
np.add(a, 100, where=a > 0, out=np.zeros_like(a))   # [101, 0, 103, 0]
```

### `dtype` — tipo de cómputo y de salida
Fuerza el tipo en el que se opera y se devuelve. Útil para evitar overflow de enteros pequeños o
fijar precisión:

```python
np.add(np.int8(100), np.int8(100))                 # -56  ← overflow (int8)
np.add(np.int8(100), np.int8(100), dtype=np.int64) # 200  ← acumulador seguro
```

### `casting` — política de conversión
Controla qué conversiones de tipo se permiten: `'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto),
`'unsafe'`. Importa con `out` o `dtype`: si la conversión necesaria no entra en la política, la ufunc
**lanza error** en vez de truncar en silencio (p. ej. escribir un resultado `float` en un `out` de
enteros con `'same_kind'`).

### `order` — layout en memoria de la salida
`'K'` (defecto, imita el layout de las entradas), `'C'` (filas contiguas), `'F'` (columnas), `'A'`.
Solo afecta a **cómo** se almacena el resultado, no a sus valores. Relevante por rendimiento al
encadenar operaciones o interoperar con código C/Fortran.

## Broadcasting y el caso N-D

`np.add` no tiene `axis`: su comportamiento en N-D lo dicta enteramente el broadcasting. La regla es
mecánica —alinear por la derecha, rellenar con `1`, tomar el `max` por eje—:

| `x1.shape` | `x2.shape` | salida | lectura |
|-----------|-----------|--------|---------|
| `(n,)` | `()` escalar | `(n,)` | suma el escalar a cada elemento |
| `(m, n)` | `(n,)` | `(m, n)` | suma el vector a **cada fila** |
| `(m, n)` | `(m, 1)` | `(m, n)` | suma un valor por fila (columna) |
| `(m, 1)` | `(1, n)` | `(m, n)` | malla: cada par fila/columna |
| `(b, m, n)` | `(n,)` | `(b, m, n)` | suma el vector a la última dimensión de todo el lote |

Ejemplo: un vector `(n,)` sobre cada fila de una matriz `(m, n)`:

```python
M = np.arange(6).reshape(2, 3)   # (2, 3)
v = np.array([10, 20, 30])       # (3,)  → (1, 3)
np.add(M, v)
# [[10, 21, 32],
#  [13, 24, 35]]
```

Y un caso 3D, sumando un vector a lo largo del último eje de un lote:

```python
T = np.ones((4, 2, 3))           # (4, 2, 3)
v = np.array([1, 2, 3])          # (3,)  → (1, 1, 3) → (4, 2, 3)
np.add(T, v).shape               # (4, 2, 3)
```

Para sumar a **otro** eje hay que insertarle un eje con `np.newaxis` antes de operar.

## Vectorización

`np.add` reemplaza el bucle Python que sumaría posición a posición. Las dos versiones dan lo mismo,
pero la ufunc corre en C sobre memoria contigua, respetando los `strides` y aplicando broadcasting
sin materializar formas intermedias:

```python
# Bucle Python (lento, explícito):
def suma(x, y):
    out = np.empty_like(x)
    for i in range(x.size):
        out[i] = x[i] + y[i]
    return out

# Vectorizado (un único bucle en C, con broadcasting):
np.add(x, y)
```

Es el principio de [[concepto_vectorizacion]]: describes *qué* operación aplicar a cada posición, no
*cómo* iterar. El operador `+` es azúcar sintáctico sobre esta misma ufunc.

## Los métodos de la ufunc

Por ser binaria, `np.add` expone los métodos de toda ufunc binaria (ver [[concepto_ufuncs]]). Dos son
fundamentales:

- `np.add.reduce(a, axis)` — **reduce** un eje sumando sus elementos. Es exactamente lo que hace
  [[np.sum]]: `np.add.reduce(a) ≡ np.sum(a)`.
- `np.add.accumulate(a, axis)` — sumas **parciales** acumuladas, conservando la shape. Equivale a
  `np.cumsum`.

```python
a = np.array([1, 2, 3, 4])
np.add.reduce(a)        # 10           (≡ np.sum)
np.add.accumulate(a)    # [1, 3, 6, 10] (≡ np.cumsum)
np.add.outer(a, a)      # tabla de sumas (4, 4)
```

## Valor de retorno

La salida tiene la **shape común del broadcasting** de las entradas; el `dtype` sale de las reglas de
promoción.

| `x1` | `x2` | salida (shape) | tipo |
|------|------|----------------|------|
| escalar | escalar | `()` | **escalar de NumPy** (`np.int64`...) |
| `(n,)` | escalar | `(n,)` | `ndarray` |
| `(m, n)` | `(n,)` | `(m, n)` | `ndarray` |
| `(m, 1)` | `(1, n)` | `(m, n)` | `ndarray` |

Reglas de `dtype` (promoción, sin `dtype=` explícito):
- `int + float → float`; `float32 + float64 → float64`.
- enteros del mismo tipo conservan el tipo → **riesgo de overflow** con `int8`/`int16`.
- la salida es un escalar de NumPy solo si **ambas** entradas son escalares.

```python
np.add(np.int32(1), np.float32(0.5)).dtype   # float64 (promoción)
type(np.add(1, 2))                           # numpy.int64 (escalar)
type(np.add([1], 2))                         # numpy.ndarray
```

## Casos de uso

### Suma simple y con escalar
```python
np.add([1, 2, 3], [4, 5, 6])   # [5, 7, 9]
np.add([1, 2, 3], 10)          # [11, 12, 13]  (broadcasting del escalar)
```

### Acumular en un buffer sin copias
```python
total = np.zeros(3)
for fila in matriz:
    np.add(total, fila, out=total)   # in-place, sin arrays temporales
```

### Suma con broadcasting (vector a cada fila)
```python
M = np.ones((3, 4))
v = np.array([1, 2, 3, 4])
np.add(M, v)                   # suma v a cada una de las 3 filas
```

### Caso N-D: sesgo por canal sobre un lote de imágenes
```python
imgs = np.zeros((5, 2, 2, 3))      # (lote, alto, ancho, canal RGB)
bias = np.array([10, 20, 30])      # (3,) → (1,1,1,3)
np.add(imgs, bias).shape           # (5, 2, 2, 3)  → suma el bias por canal
```

### Reducir/acumular con los métodos de la ufunc
```python
a = np.array([1, 2, 3, 4])
np.add.reduce(a)        # 10            (≡ np.sum)
np.add.accumulate(a)    # [1, 3, 6, 10] (≡ np.cumsum)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `operands could not be broadcast together` | shapes incompatibles | alinear por la derecha; ver [[concepto_broadcasting]] |
| Resultado negativo/absurdo | overflow de enteros (`int8`/`int16`) | `dtype=np.int64` |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` con `where=` |
| `Cannot cast ufunc output` | `out`/`dtype` incompatible con `casting` | ajustar `out`/`dtype` o `casting='unsafe'` consciente |
| Esperar que `(n,)` sume por columnas | broadcasting alinea por la derecha (es fila) | forzar columna con `v[:, np.newaxis]` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.add` es el molde de ufunc binaria; `reduce`/`accumulate`/`outer`.
- [[concepto_broadcasting]] — la alineación de shapes que gobierna su salida.
- [[concepto_dtype]] — la promoción de tipos del resultado.
- [[np.sum]] — `np.add.reduce`: la versión que reduce un eje.
- [[np.subtract]] · [[np.multiply]] · [[np.divide]] · [[np.cumsum]]
