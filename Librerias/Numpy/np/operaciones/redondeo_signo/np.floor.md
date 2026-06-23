---
title: np.floor — suelo, redondeo hacia abajo (ufunc)
aliases:
  - floor
  - np.floor
  - suelo
tags:
  - numpy
  - api/funcion
  - transformaciones
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_ufuncs
draft: false
---

# np.floor — suelo, redondeo hacia abajo (ufunc)

`np.floor` es una **ufunc unaria**: aplica el suelo $\lfloor x\rfloor$ a cada elemento del array,
es decir, lo redondea al **mayor entero que no lo supera** (hacia $-\infty$). Es la pareja de
[[np.ceil]] (que redondea hacia $+\infty$). La trampa está en los negativos: como va siempre hacia
abajo, `floor(-2.5) = -3`, no `-2`. Conserva el shape y **devuelve float**.

## La idea en una fórmula

Es element-wise puro: cada elemento se transforma de forma independiente y el shape no cambia.

$$
z_i = \lfloor x_i\rfloor = \max\{\,k\in\mathbb{Z} : k \le x_i\,\}
$$

Mapa de shapes (la forma se conserva, es lo característico de una ufunc unaria):

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{floor}\ }\ (n_0,\dots,n_k)
$$

Visualmente, sobre la recta cada valor "cae" al entero de su izquierda:

```
x:      -2.5   -0.1    0.1    2.9
floor:  -3.    -1.     0.     2.
```

## Firma

```python
np.floor(
    x,            # array_like: el tensor de entrada (real)
    /,
    out=None,     # ndarray | None: destino preasignado
    *,
    where=True,   # array_like[bool]: dónde calcular
    dtype=None,   # dtype: tipo de cómputo/salida
    casting='same_kind',
) -> ndarray
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` real (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. **No acepta
complejos** (lanza `TypeError`): el suelo de un complejo no está definido. Los enteros pasan tal cual
(el suelo de un entero es él mismo), promovidos a float.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida (y dtype float). Evita asignar memoria nueva; útil en
bucles o para hacer la operación "in-place sobre un buffer". Debe ser compatible con la política de
`casting`.

```python
buf = np.empty(3)
np.floor([1.7, 2.2, 3.9], out=buf)   # array([1., 2., 3.]); escribe en buf
```

### `where` — máscara de cálculo
`array_like` booleano broadcasteable con `x`. Solo calcula el suelo donde `where` es `True`; el resto
conserva lo que hubiera en `out`. Como toda ufunc, **conviene pasar `out`** si usas `where`, o las
posiciones no calculadas quedan sin inicializar (ver [[concepto_ufuncs]]).

### `dtype` / `casting`
`dtype` fuerza el tipo de cómputo/salida; `casting` (`'no'`, `'safe'`, `'same_kind'`, `'unsafe'`)
controla qué conversiones se permiten al escribir en `out`. Rara vez se tocan: el resultado es float
por naturaleza.

## El caso N-D

`np.floor` es **element-wise**: opera posición a posición sin mirar los ejes, así que el shape de la
salida es **idéntico** al de la entrada en cualquier dimensión. No hay `axis` ni colapso de ejes.

```python
M = np.array([[1.2, -1.2],
              [2.8, -2.8]])
np.floor(M)
# array([[ 1., -2.],
#        [ 2., -3.]])      mismo shape (2, 2)

T = np.random.rand(4, 3, 2) * 10
np.floor(T).shape          # (4, 3, 2)  → la forma se conserva
```

## Vectorización

`np.floor` reemplaza un bucle Python con `math.floor` por elemento. La versión ufunc recorre la
memoria en C, respeta los `strides` y aplica broadcasting (ver [[concepto_vectorizacion]]):

```python
import math
# Bucle Python (lento, interpreta cada paso):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.floor(arr.flat[i])

# ufunc (un único bucle en C):
np.floor(arr)
```

## Valor de retorno

Devuelve un `ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** y dtype
**float**:

| Entrada (shape, dtype) | salida (shape) | dtype salida |
|------------------------|----------------|--------------|
| `(n,)` float64 | `(n,)` | `float64` |
| `(m, n)` float32 | `(m, n)` | `float32` |
| escalar `2.5` | `()` | `np.float64` |
| `(n,)` int64 | `(n,)` | `float64` (promovido) |

El valor sigue siendo "entero" matemáticamente, pero el **tipo es float**; convierte con
`.astype(int)` si necesitas enteros de verdad.

## Casos de uso

### Redondeo hacia abajo y conversión a int
```python
np.floor([1.9, 2.1, -0.5])              # array([ 1.,  2., -1.])
np.floor([1.9, 2.1, -0.5]).astype(int)  # array([ 1,  2, -1])
```

### Cuidado con los negativos (vs trunc)
```python
np.floor([-2.5, -2.1, -2.9])   # array([-3., -3., -3.])  ← siempre hacia -inf
np.trunc([-2.5, -2.1, -2.9])   # array([-2., -2., -2.])  ← hacia cero
```

### N-D: discretizar coordenadas en celdas de una rejilla
```python
puntos = np.array([[0.4, 9.9],
                   [3.7, 0.2],
                   [8.1, 5.5]])        # (3, 2) coordenadas continuas
celdas = np.floor(puntos).astype(int)
# array([[0, 9],
#        [3, 0],
#        [8, 5]])      → índice de celda de cada punto, shape (3, 2)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `floor(-2.5)` da `-3`, no `-2` | el suelo va hacia $-\infty$, no hacia cero | usar [[np.trunc]] si quieres hacia cero |
| Esperar int y recibir float | `floor` siempre devuelve float | `.astype(int)` |
| `TypeError` con complejos | el suelo no está definido para complejos | aplicar a `.real`/`.imag` por separado |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que conserva el shape
- [[np.ceil]] — la pareja: redondeo hacia $+\infty$
- [[np.trunc]] · [[np.rint]] · [[np.round]]
- [[Librerias/Numpy/np/operaciones/redondeo_signo/index\|redondeo_signo — la familia completa]]
