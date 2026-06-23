---
title: np.ceil — techo (entero superior) elemento a elemento (ufunc)
aliases:
  - ceil
  - np.ceil
  - techo
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
  - concepto_vectorizacion

draft: false
---

# np.ceil — techo (entero superior) elemento a elemento (ufunc)

`np.ceil` es una **ufunc unaria**: aplica el **techo** $\lceil x_i\rceil$ a cada elemento, es decir el
**menor entero $\ge x_i$**, sin mirar a sus vecinos y **sin cambiar el shape**. Es redondear *siempre
hacia arriba* sobre la recta real. La trampa habitual: aunque el resultado es un valor entero, lo
devuelve como **`float`**, no como `int`. Es la pareja de [[np.floor]] (que redondea hacia abajo).

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \lceil x_i\rceil = \min\{\, m \in \mathbb{Z} : m \ge x_i \,\} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{ceil}\ }\ (n_0,\dots,n_k)
$$

"El menor entero que no se queda corto". Cuidado con los negativos: $\lceil -2.7\rceil = -2$ (sube hacia
el cero), no $-3$.

| `x` | $\lceil x\rceil$ |
|-----|------------------|
| `2.1` | `3.0` |
| `2.9` | `3.0` |
| `-2.1` | `-2.0` |
| `-2.9` | `-2.0` |
| `3.0` | `3.0` |

## Firma

```python
np.ceil(
    x,                 # array_like: el tensor de entrada (real)
    /,
    out=None,          # ndarray | None: destino preasignado
    *,
    where=True,        # array_like[bool]: máscara de cómputo
    casting='same_kind',  # política de conversión de tipos
    order='K',         # 'K' | 'C' | 'F' | 'A': layout de memoria del resultado
    dtype=None,        # dtype: fuerza el tipo de cómputo/salida
) -> ndarray
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` **real** (ndarray, lista, escalar). Los enteros se promueven a float (su techo coincide con
ellos mismos). No acepta complejos. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.ceil(arr, out=arr)`). El dtype debe ser flotante (la salida lo es) y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el techo donde es `True`; donde es `False`,
la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). No sirve para obtener enteros: aunque el
valor sea entero, sale como float; para enteros se castea aparte con `.astype(int)`.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten al
escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.ceil` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1.2, 2.7], [-1.5, 0.1]],
              [[3.9, -3.9], [4.0, 4.5]]])   # shape (2, 2, 2)
np.ceil(T).shape       # (2, 2, 2)  → shape idéntico
np.ceil(T)
# [[[ 2.,  3.], [-1.,  1.]],
#  [[ 4., -3.], [ 4.,  5.]]]
```

## Vectorización

`np.ceil` reemplaza un bucle que llamaría a `math.ceil` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.ceil(arr.flat[i])

# ufunc (un único bucle en C):
out = np.ceil(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | el valor es entero pero el tipo sigue siendo float |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float; el resultado **no es int** |

```python
np.ceil(np.array([2.1, 2.9])).dtype    # float64
np.ceil([1.2, 2.7, -1.5])              # array([ 2.,  3., -1.])
np.ceil(total / por_pagina).astype(int)  # castea aparte si quieres enteros
```

## Casos de uso

### Número de lotes/páginas necesarios
```python
paginas = np.ceil(total / por_pagina).astype(int)   # siempre cubre el resto
```

### Redondear hacia arriba a múltiplos
```python
x = np.array([12, 47, 83])
np.ceil(x / 10) * 10     # [20., 50., 90.]  al siguiente múltiplo de 10
```

### N-D: techo por elemento de un tensor
```python
T = np.array([[[1.2, 2.7], [-1.5, 0.1]],
              [[3.9, -3.9], [4.0, 4.5]]])   # (2, 2, 2)
np.ceil(T)
# [[[ 2.,  3.], [-1.,  1.]],
#  [[ 4., -3.], [ 4.,  5.]]]               # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar `int` y recibir `float` | `ceil` siempre devuelve float | castear con `.astype(int)` |
| `ceil(-2.7)` da `-2`, no `-3` | el techo sube hacia el cero en negativos | usar [[np.floor]] si querías ir hacia abajo |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.ceil` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.floor]] — su pareja: redondea hacia abajo ($\lfloor x\rfloor$)
- [[np.trunc]] · [[np.round]] · [[np.sign]]
