---
title: np.floor_divide — división entera hacia abajo (ufunc del operador //)
aliases:
  - floor_divide
  - np.floor_divide
  - division entera
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ufuncs
  - concepto_broadcasting

draft: false
---

# np.floor_divide — división entera hacia abajo (ufunc del operador //)

`np.floor_divide` calcula la **división entera redondeada hacia abajo** (hacia $-\infty$) elemento a
elemento: es el cociente "que cabe" descartando la parte fraccionaria. Es la [[concepto_ufuncs|ufunc]]
que respalda el operador `//`, así que `a // b` invoca `np.floor_divide(a, b)`. Forma con
[[np.remainder]] el par cociente/resto que cumple la identidad de división euclídea.

## La idea en una fórmula

Cada elemento de la salida es el suelo del cociente real:

$$ z_i = \left\lfloor \frac{x_i}{y_i} \right\rfloor $$

El **suelo** $\lfloor\cdot\rfloor$ redondea hacia $-\infty$, no hacia cero: por eso con negativos
`-7 // 2` da `-4` (no `-3`). Junto a [[np.remainder]] satisface la identidad euclídea, que es la
forma más fiable de recordar su comportamiento:

$$ x_i = (x_i \mathbin{//} y_i)\, y_i + (x_i \bmod y_i) \qquad\Longleftrightarrow\qquad
\texttt{a == (a//b)*b + a\%b} $$

Como toda ufunc binaria, las shapes se alinean por [[concepto_broadcasting|broadcasting]] (alineación
por la derecha) y la salida toma la shape común:

$$ (n_0,\dots,n_k),\ (m_0,\dots,m_k)\ \xrightarrow{\ \text{broadcast}\ }\
(\max(n_0,m_0),\,\dots,\,\max(n_k,m_k)) $$

## Firma

```python
np.floor_divide(
    x1, x2, /,          # array_like: dividendo y divisor (se broadcastean)
    out=None,           # ndarray | None: destino preasignado
    *,
    where=True,         # array_like[bool]: máscara de cómputo
    casting='same_kind',# política de conversión de tipos
    order='K',          # orden de memoria del resultado
    dtype=None,         # dtype: tipo de cómputo/salida
) -> ndarray
```

## Los parámetros en detalle

### `x1`, `x2` — dividendo y divisor
`array_like` (ndarray, lista, escalar). Se broadcastean entre sí: pueden tener shapes distintas
mientras sean compatibles por la derecha. Si ambos son enteros el resultado es entero; si alguno es
float, el resultado es float (pero con valor entero, ver `dtype`).

```python
np.floor_divide([7, 8, 9], 4)   # array([1, 2, 2])
np.floor_divide(7, 2)           # 3
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de la salida (el de broadcasting). Evita la asignación de un array
nuevo; útil en bucles. Puede ser uno de los operandos para operar in-place.

```python
buf = np.empty(3, dtype=int)
np.floor_divide([10, 20, 30], 3, out=buf)   # escribe en buf
```

### `where` — cómputo condicional (máscara)
`array_like` booleano broadcasteable con la entrada. Solo calcula donde es `True`; donde es `False`
se conserva el valor previo de `out`. Útil para **evitar la división por cero**: enmascara los
divisores nulos en lugar de dejar que NumPy emita el warning.

```python
x = np.array([10, 20, 30])
y = np.array([2, 0, 3])
out = np.zeros_like(x)
np.floor_divide(x, y, out=out, where=y != 0)   # salta el divisor 0
```

### `dtype` — tipo de cómputo y salida
Fuerza el tipo en el que se calcula y se devuelve. Por defecto sale de la promoción de `x1` y `x2`
(`int // int → int`, `float // int → float`).

### `casting` — política de conversión
`'no' | 'equiv' | 'safe' | 'same_kind' | 'unsafe'`. Controla qué conversiones se permiten al combinar
tipos o al escribir en `out`. Por defecto `'same_kind'`. Si `out` tiene un dtype incompatible, lanza
error en vez de truncar en silencio.

### `order` — orden de memoria del resultado
`'K' | 'C' | 'F' | 'A'`. Determina el layout del array de salida. Rara vez importa salvo por
rendimiento al encadenar operaciones; por defecto `'K'` (conserva el del input lo más posible).

## Broadcasting y el caso N-D

La operación es **element-wise pura**: no hay eje que se reduzca, la shape de salida es simplemente la
shape común de broadcasting. Un caso N-D típico es dividir un tensor por un vector que se alinea en el
último eje.

| `x1.shape` | `x2.shape` | salida | lectura |
|-----------|-----------|--------|---------|
| `(n,)` | `()` escalar | `(n,)` | cada elemento entre el mismo divisor |
| `(m, n)` | `(n,)` | `(m, n)` | cada fila entre el vector (alineado por la derecha) |
| `(b, m, n)` | `(1, n)` | `(b, m, n)` | mismo divisor por columna en todo el lote |

```python
T = np.arange(24).reshape(2, 3, 4)   # (2, 3, 4)
divs = np.array([1, 2, 3, 4])        # (4,) → se alinea al último eje
np.floor_divide(T, divs).shape       # (2, 3, 4)
np.floor_divide(T, divs)[0]
# [[ 0,  0,  0,  0],
#  [ 4,  2,  2,  1],
#  [ 8,  4,  3,  2]]
```

## Vectorización

`np.floor_divide` reemplaza un bucle Python que aplicaría `//` elemento a elemento. La versión
vectorizada recorre los datos en C, con [[concepto_broadcasting|broadcasting]] y sin crear objetos
Python por elemento:

```python
# Bucle Python (lento, explícito):
out = np.empty_like(x)
for i in range(x.size):
    out[i] = x[i] // y[i]

# Vectorizado (un único bucle en C):
out = np.floor_divide(x, y)   # ≡ x // y
```

## Valor de retorno

`ndarray` (o escalar de NumPy si ambas entradas son escalares) con la shape común de broadcasting. El
dtype sale de la promoción de las entradas:

| `x1` dtype | `x2` dtype | salida dtype | nota |
|-----------|-----------|--------------|------|
| `int` | `int` | `int` | cociente entero exacto |
| `float` | `int` / `float` | `float` | valor entero pero tipo float (`7.0 // 2.0 == 3.0`) |
| entero, divisor `0` | — | `0` + `RuntimeWarning` | no es `nan` (los enteros no tienen `nan`) |
| float, divisor `0.0` | — | `inf`/`nan` + warning | propaga como float |

```python
np.floor_divide(7, 2)        # 3       (int)
np.floor_divide(7.0, 2.0)    # 3.0     (float, redondeado a -inf)
np.floor_divide(-7, 2)       # -4      (suelo, NO -3)
```

## Casos de uso

### Cociente y resto a la vez (división euclídea)
```python
a, b = np.array([7, -7, 8]), 3
q = np.floor_divide(a, b)    # [ 2, -3,  2]
r = np.remainder(a, b)       # [ 1,  2,  2]
np.all(a == q * b + r)       # True  → identidad a == (a//b)*b + a%b
```
Para obtener ambos de una sola pasada existe [[np.divmod]], que retorna `(q, r)`.

### Convertir un índice plano a coordenadas de fila
```python
idx = np.array([0, 1, 2, 3, 4, 5])
filas = np.floor_divide(idx, 3)   # [0, 0, 0, 1, 1, 1]  índice → fila (ancho 3)
cols  = np.remainder(idx, 3)      # [0, 1, 2, 0, 1, 2]  columna
```

### Empaquetar bytes / cambiar de unidad
```python
total_seg = np.array([3661, 7322])
horas = np.floor_divide(total_seg, 3600)   # [1, 2]
```

### Ejemplo N-D: cuantizar un tensor
```python
T = np.arange(24).reshape(2, 3, 4)
np.floor_divide(T, 5)        # agrupa cada valor en "cubos" de tamaño 5, conserva (2,3,4)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-7 // 2 == -4` "sorprende" | redondea hacia $-\infty$, no hacia cero | usar `np.trunc(x/y)` si quieres redondeo hacia cero |
| `RuntimeWarning: divide by zero` | divisor `0` (devuelve `0` en enteros) | `where=y != 0` o validar el divisor |
| resultado float donde se esperaba int | un operando es float | castear con `.astype(int)` o usar entradas enteras |
| `a//b` distinto de C/C++ | Python/NumPy usan suelo; C trunca | comparar con `np.fmod`/`np.trunc` para semántica de C |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que ejecuta `//`
- [[concepto_broadcasting]] — cómo se alinean `x1` y `x2`
- [[np.remainder]] · [[np.mod]] — el resto que completa la identidad euclídea
- [[np.divide]] — división real (siempre float) · [[np.divmod]] — cociente y resto juntos
