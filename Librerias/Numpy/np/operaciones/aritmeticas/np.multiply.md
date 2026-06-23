---
title: np.multiply — producto elemento a elemento (Hadamard, ufunc binaria)
aliases:
  - multiply
  - np.multiply
  - producto elemento a elemento
  - producto de Hadamard
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

# np.multiply — producto elemento a elemento (Hadamard, ufunc binaria)

`np.multiply` es la **ufunc binaria** que multiplica dos tensores **posición a posición** (el
**producto de Hadamard**). No reduce ningún eje ni contrae dimensiones: alinea las entradas por
[[concepto_broadcasting|broadcasting]] y devuelve una salida con la **shape común**. Es la función
que respalda el operador `*`: `a * b` es exactamente `np.multiply(a, b)`. El error clásico es
confundirlo con el **producto matricial** `@` / [[np.matmul|producto matricial]], que contrae una
dimensión compartida y es algo completamente distinto (ver la sección dedicada más abajo).

## La idea en una fórmula

La operación es **elemento a elemento**: cada posición de la salida es el producto de las posiciones
correspondientes de las entradas, tras alinearlas por broadcasting.

$$
z_i = x_i \cdot y_i
$$

y en N-D, con los índices recorriendo la shape común:

$$
z_{i_0\dots i_k} = x_{i_0\dots i_k} \cdot y_{i_0\dots i_k}
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

Contrasta con el producto matricial, que **suma sobre** el eje compartido y lo elimina
($C_{ij} = \sum_k A_{ik} B_{kj}$): ahí el shape cambia; aquí **se conserva**. Ver
[[concepto_broadcasting]].

## Firma

```python
np.multiply(
    x1,                     # array_like: primer factor
    x2,                     # array_like: segundo factor
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

### `x1`, `x2` — los factores
`array_like` (ndarray, lista, escalar), broadcasteables entre sí. Sus shapes se alinean por la
derecha; el `dtype` de salida sale de promover ambos (ver `dtype`). Si ambos son escalares, el
retorno es un escalar de NumPy.

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida (la del broadcast). Evita asignar memoria nueva; permite
el **producto in-place** apuntando a un operando (p. ej. escalar en sitio):

```python
np.multiply(arr, 2, out=arr)   # duplica arr in-place, sin temporales
```

### `where` — producto condicional (máscara)
`array_like` booleano broadcasteable con las entradas. Solo se calcula donde `where` es `True`; en el
resto la salida **conserva lo que hubiera en `out`**, por lo que conviene pasar `out` explícito:

```python
a = np.array([1, 2, 3, 4])
np.multiply(a, 10, where=a % 2 == 0, out=a.copy())   # [1, 20, 3, 40]
```

### `dtype` — tipo de cómputo y de salida
Fuerza el tipo de la operación y del resultado. El producto **dispara el overflow** de enteros
pequeños mucho antes que la suma; fijar un tipo mayor lo evita:

```python
np.multiply(np.int8(20), np.int8(20))                 # -112  ← overflow (int8)
np.multiply(np.int8(20), np.int8(20), dtype=np.int64) # 400   ← correcto
```

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Importa con `out`/`dtype`: si la
conversión necesaria no entra en la política, la ufunc **lanza error** en vez de truncar en silencio.

### `order` — layout en memoria de la salida
`'K'` (defecto, imita el de las entradas), `'C'`, `'F'`, `'A'`. Solo afecta a **cómo** se almacena el
resultado, no a sus valores; relevante por rendimiento e interoperabilidad.

## `*` (Hadamard) vs `@` (producto matricial) — la distinción clave

Es el error más común de NumPy. `np.multiply` / `*` operan **posición a posición** y conservan la
shape (con broadcasting). `@` / [[np.matmul|np.matmul]] contraen la dimensión compartida y cambian la
shape. **No son intercambiables**:

```python
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[10, 20],
              [30, 40]])

A * B          # Hadamard (np.multiply): elemento a elemento
# [[ 10,  40],
#  [ 90, 160]]

A @ B          # producto matricial (np.matmul): suma filas × columnas
# [[ 70, 100],
#  [150, 220]]
```

`A * B` multiplica `A[i,j] * B[i,j]`. `A @ B` calcula `sum_k A[i,k] * B[k,j]` —contrae el eje
compartido—. Coinciden por casualidad solo en casos triviales; en general dan números distintos.

## Broadcasting y el caso N-D

`np.multiply` no tiene `axis`: su comportamiento en N-D lo dicta enteramente el broadcasting (alinear
por la derecha, rellenar con `1`, tomar el `max` por eje):

| `x1.shape` | `x2.shape` | salida | lectura |
|-----------|-----------|--------|---------|
| `(n,)` | `()` escalar | `(n,)` | escala cada elemento |
| `(m, n)` | `(n,)` | `(m, n)` | pesa **cada fila** por el vector |
| `(m, n)` | `(m, 1)` | `(m, n)` | pesa **cada fila** por un escalar distinto |
| `(b, m, n)` | `(n,)` | `(b, m, n)` | pesa la última dimensión de todo el lote |

Ejemplo: pesar cada fila de una matriz `(m, n)` por un vector `(n,)`:

```python
M = np.arange(1, 7).reshape(2, 3)   # (2, 3)
w = np.array([10, 0, 100])          # (3,)  → (1, 3)
np.multiply(M, w)
# [[ 10,   0, 300],
#  [ 40,   0, 600]]
```

Y un caso 3D, escalando por canal un lote de imágenes:

```python
imgs = np.ones((5, 2, 2, 3))        # (lote, alto, ancho, canal RGB)
ganancia = np.array([0.5, 1.0, 2.0])# (3,) → (1,1,1,3)
np.multiply(imgs, ganancia).shape   # (5, 2, 2, 3)  → escala cada canal
```

## Vectorización

`np.multiply` reemplaza el bucle Python que multiplicaría posición a posición. Las dos versiones dan
lo mismo, pero la ufunc corre en C sobre memoria contigua, respetando los `strides` y aplicando
broadcasting sin materializar formas intermedias:

```python
# Bucle Python (lento, explícito):
def producto(x, y):
    out = np.empty_like(x)
    for i in range(x.size):
        out[i] = x[i] * y[i]
    return out

# Vectorizado (un único bucle en C, con broadcasting):
np.multiply(x, y)
```

Es el principio de [[concepto_vectorizacion]]: describes *qué* operación aplicar a cada posición, no
*cómo* iterar. El operador `*` es azúcar sintáctico sobre esta misma ufunc.

## Valor de retorno

La salida tiene la **shape común del broadcasting** de las entradas; el `dtype` sale de las reglas de
promoción.

| `x1` | `x2` | salida (shape) | tipo |
|------|------|----------------|------|
| escalar | escalar | `()` | **escalar de NumPy** |
| `(n,)` | escalar | `(n,)` | `ndarray` |
| `(m, n)` | `(n,)` | `(m, n)` | `ndarray` |
| `(m, 1)` | `(1, n)` | `(m, n)` | `ndarray` |

Reglas de `dtype` (promoción, sin `dtype=` explícito):
- `int * float → float`; `float32 * float64 → float64`.
- enteros del mismo tipo conservan el tipo → **overflow temprano** con `int8`/`int16`.
- la salida es un escalar de NumPy solo si **ambas** entradas son escalares.

```python
np.multiply(np.int32(3), np.float32(2.0)).dtype   # float64 (promoción)
type(np.multiply(3, 4))                            # numpy.int64 (escalar)
```

## Casos de uso

### Escalar un array / aplicar pesos
```python
np.multiply([1, 2, 3], 10)          # [10, 20, 30]
ponderado = np.multiply(valores, pesos)   # pesos elemento a elemento
```

### Máscara como multiplicación (poner a cero)
```python
a = np.array([5, -3, 8, -1])
np.multiply(a, a > 0)               # [5, 0, 8, 0]  ← anula los negativos
```

### Distinguir Hadamard de producto matricial
```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[1, 0], [0, 1]])
A * B          # [[1, 0], [0, 4]]   Hadamard
A @ B          # [[1, 2], [3, 4]]   producto matricial (B es la identidad)
```

### Caso N-D: ganancia por canal sobre un lote de imágenes
```python
imgs = np.ones((4, 8, 8, 3))        # (lote, alto, ancho, canal)
ganancia = np.array([1.0, 0.5, 0.0])# (3,) → escala cada canal RGB
np.multiply(imgs, ganancia).shape   # (4, 8, 8, 3)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar producto **matricial** | `*` / `np.multiply` son elemento a elemento (Hadamard) | usar `@` o [[np.matmul]] |
| Resultado absurdo/negativo | overflow de enteros (el producto desborda pronto) | `dtype=np.int64` |
| `operands could not be broadcast together` | shapes incompatibles | alinear por la derecha; ver [[concepto_broadcasting]] |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.multiply` como ufunc binaria; `reduce` ≡ [[np.prod]], `accumulate` ≡ cumprod.
- [[concepto_broadcasting]] — la alineación de shapes que gobierna su salida.
- [[np.matmul]] — el producto **matricial** (`@`), que contrae una dimensión: NO confundir.
- [[np.add]] — la otra ufunc binaria base; el molde element-wise.
- [[np.divide]] · [[np.prod]] — producto-reducción de un eje.
