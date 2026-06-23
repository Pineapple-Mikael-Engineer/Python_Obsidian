---
title: np.subtract — resta elemento a elemento (ufunc binaria)
aliases:
  - subtract
  - np.subtract
  - resta elemento a elemento
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

# np.subtract — resta elemento a elemento (ufunc binaria)

`np.subtract` es la **ufunc binaria** que resta dos tensores **posición a posición**. No reduce
ningún eje: alinea las entradas por [[concepto_broadcasting|broadcasting]] y produce una salida con
la **shape común**. Es la función que respalda el operador binario `-`: `a - b` es exactamente
`np.subtract(a, b)`. A diferencia de la suma, **no es conmutativa**: `np.subtract(a, b)` ≠
`np.subtract(b, a)` (el orden de los operandos importa). Comparte estructura con [[np.add]]; ver
[[concepto_ufuncs]].

## La idea en una fórmula

La operación es **elemento a elemento**: cada posición de la salida es la diferencia de las
posiciones correspondientes de las entradas, tras alinearlas por broadcasting.

$$
z_i = x_i - y_i
$$

y en N-D, con los índices recorriendo la shape común:

$$
z_{i_0\dots i_k} = x_{i_0\dots i_k} - y_{i_0\dots i_k}
$$

El **mapa de shapes es el de broadcasting**: las entradas se alinean **por la derecha**, se rellena
con `1` a la izquierda y cada eje toma el `max` (válido si en cada eje coinciden o uno es `1`):

$$
(\dots, a_{k-1}, a_k),\ (\dots, b_{k-1}, b_k)\ \xrightarrow{\ \text{broadcast}\ }\ (\dots,\,\max(a_{k-1},b_{k-1}),\,\max(a_k,b_k))
$$

```text
x      (3, 4)
y         (4,)  →  (1, 4)     ← rellena con 1 por la izquierda
---------------
eje -1:  4 vs 4  →  4
eje -2:  3 vs 1  →  3         ← uno es 1, se estira
---------------
z      (3, 4)
```

Toda la lógica de alineación vive en [[concepto_broadcasting]].

## Firma

```python
np.subtract(
    x1,                     # array_like: minuendo
    x2,                     # array_like: sustraendo
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

### `x1`, `x2` — minuendo y sustraendo
`array_like` (ndarray, lista, escalar), broadcasteables entre sí. El **orden importa**: `x1` es el
minuendo y `x2` el sustraendo. Sus shapes se alinean por la derecha y el `dtype` de salida sale de
promover ambos (ver `dtype`). Si ambos son escalares, el retorno es un escalar de NumPy.

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida (la del broadcast). Evita asignar memoria nueva; permite
la **resta in-place** apuntando a un operando:

```python
np.subtract(acum, paso, out=acum)   # resta in-place sin crear temporales
```

### `where` — resta condicional (máscara)
`array_like` booleano broadcasteable con las entradas. Solo se calcula donde `where` es `True`; en el
resto la salida **conserva lo que hubiera en `out`**, por lo que conviene pasar `out` explícito:

```python
a = np.array([10, 20, 30, 40])
np.subtract(a, 5, where=a > 15, out=a.copy())   # [10, 15, 25, 35]
```

### `dtype` — tipo de cómputo y de salida
Fuerza el tipo de la operación y del resultado. Crítico con enteros **sin signo**: una diferencia
negativa desborda (wrap-around). Forzar un tipo con signo lo evita:

```python
np.subtract(np.uint8(3), np.uint8(5))                # 254  ← wrap-around (uint8)
np.subtract(np.uint8(3), np.uint8(5), dtype=np.int16) # -2  ← correcto
```

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Importa con `out`/`dtype`: si la
conversión necesaria no entra en la política, la ufunc **lanza error** en vez de truncar en silencio.

### `order` — layout en memoria de la salida
`'K'` (defecto, imita el de las entradas), `'C'`, `'F'`, `'A'`. Solo afecta a **cómo** se almacena el
resultado, no a sus valores; relevante por rendimiento e interoperabilidad.

## Broadcasting y el caso N-D

`np.subtract` no tiene `axis`: su comportamiento en N-D lo dicta enteramente el broadcasting (alinear
por la derecha, rellenar con `1`, tomar el `max` por eje):

| `x1.shape` | `x2.shape` | salida | lectura |
|-----------|-----------|--------|---------|
| `(n,)` | `()` escalar | `(n,)` | resta el escalar a cada elemento |
| `(m, n)` | `(n,)` | `(m, n)` | resta el vector a **cada fila** |
| `(m, n)` | `(m, 1)` | `(m, n)` | resta un valor por fila |
| `(b, m, n)` | `(n,)` | `(b, m, n)` | resta el vector a la última dimensión del lote |

Ejemplo: restar la media por columna a cada fila de una matriz (centrar datos) —un `(n,)` sobre cada
fila de un `(m, n)`—:

```python
datos = np.array([[1., 2., 3.],
                  [4., 5., 6.]])     # (2, 3)
media = datos.mean(axis=0)           # (3,)  → (1, 3)
np.subtract(datos, media)
# [[-1.5, -1.5, -1.5],
#  [ 1.5,  1.5,  1.5]]
```

Y un caso 3D, restando un vector a lo largo del último eje de un lote:

```python
T = np.ones((4, 2, 3))               # (4, 2, 3)
v = np.array([1, 2, 3])              # (3,)  → (1, 1, 3) → (4, 2, 3)
np.subtract(T, v).shape              # (4, 2, 3)
```

## Vectorización

`np.subtract` reemplaza el bucle Python que restaría posición a posición. Las dos versiones dan lo
mismo, pero la ufunc corre en C sobre memoria contigua, respetando los `strides` y aplicando
broadcasting sin materializar formas intermedias:

```python
# Bucle Python (lento, explícito):
def resta(x, y):
    out = np.empty_like(x)
    for i in range(x.size):
        out[i] = x[i] - y[i]
    return out

# Vectorizado (un único bucle en C, con broadcasting):
np.subtract(x, y)
```

Es el principio de [[concepto_vectorizacion]]: describes *qué* operación aplicar a cada posición, no
*cómo* iterar. El operador binario `-` es azúcar sintáctico sobre esta misma ufunc.

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
- `int - float → float`; `float32 - float64 → float64`.
- enteros **sin signo** conservan el tipo → una diferencia negativa **desborda** (wrap-around).
- la salida es un escalar de NumPy solo si **ambas** entradas son escalares.

```python
np.subtract(np.int32(5), np.float32(1.5)).dtype   # float64 (promoción)
type(np.subtract(5, 2))                            # numpy.int64 (escalar)
```

## Casos de uso

### Resta simple y con escalar
```python
np.subtract([5, 7, 9], [1, 2, 3])   # [4, 5, 6]
np.subtract([5, 7, 9], 2)           # [3, 5, 7]
```

### Centrar datos restando la media por columna
```python
centrado = np.subtract(datos, datos.mean(axis=0))   # cada columna queda con media 0
```

### Error entre predicción y objetivo
```python
error = np.subtract(prediccion, objetivo)
```

### Caso N-D: quitar un offset por canal a un lote de imágenes
```python
imgs = np.ones((5, 2, 2, 3))        # (lote, alto, ancho, canal RGB)
offset = np.array([10, 20, 30])     # (3,) → (1,1,1,3)
np.subtract(imgs, offset).shape     # (5, 2, 2, 3)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores enormes con `uint` | diferencia negativa desborda (wrap-around) | convertir a `int`/`float` o `dtype=` con signo |
| Resultado en orden invertido | `np.subtract` **no es conmutativa**; se cambió `x1`/`x2` | respetar minuendo (`x1`) − sustraendo (`x2`) |
| `operands could not be broadcast together` | shapes incompatibles | alinear por la derecha; ver [[concepto_broadcasting]] |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.subtract` como ufunc binaria; sus métodos `reduce`/`accumulate`.
- [[concepto_broadcasting]] — la alineación de shapes que gobierna su salida.
- [[concepto_dtype]] — promoción de tipos y el overflow de `uint`.
- [[np.add]] — la operación hermana (conmutativa); el molde de ufunc binaria.
- [[np.multiply]] · [[np.diff]] — diferencias **consecutivas** a lo largo de un eje.
