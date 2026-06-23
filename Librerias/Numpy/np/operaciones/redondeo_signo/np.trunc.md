---
title: np.trunc — truncamiento hacia cero (ufunc)
aliases:
  - trunc
  - np.trunc
  - truncar
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

# np.trunc — truncamiento hacia cero (ufunc)

`np.trunc` es una **ufunc unaria** que **quita la parte decimal** de cada elemento, redondeando
siempre **hacia cero**. Para positivos coincide con [[np.floor]]; para negativos coincide con
[[np.ceil]]: `trunc(2.7) = 2` y `trunc(-2.7) = -2` (a diferencia de `floor(-2.7) = -3`). Conserva el
shape y **devuelve float**. Es "borrar lo que hay después del punto".

## La idea en una fórmula

Element-wise: cada elemento pierde su parte fraccionaria de forma independiente, el shape no cambia.

$$
z_i = \operatorname{trunc}(x_i) = \operatorname{sign}(x_i)\,\big\lfloor |x_i|\big\rfloor =
\begin{cases}\lfloor x_i\rfloor & x_i \ge 0\\[2pt] \lceil x_i\rceil & x_i < 0\end{cases}
$$

Mapa de shapes (se conserva, ufunc unaria):

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{trunc}\ }\ (n_0,\dots,n_k)
$$

Sobre la recta, cada valor "cae" hacia el **cero**:

```
x:      -2.7   -0.5    0.5    2.7
trunc:  -2.    -0.     0.     2.
        ←——— hacia 0 ———→
```

## Firma

```python
np.trunc(
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
`array_like` real (ndarray, lista, escalar). **No acepta complejos** (`TypeError`). Los enteros se
promueven a float y pasan sin cambios (no tienen parte decimal).

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida (dtype float). Evita asignar memoria nueva; debe ser
compatible con la política de `casting`.

```python
buf = np.empty(3)
np.trunc([1.9, -1.9, 2.5], out=buf)   # array([ 1., -1.,  2.]); escribe en buf
```

### `where` — máscara de cálculo
`array_like` booleano broadcasteable con `x`. Solo trunca donde `where` es `True`; el resto conserva
lo que hubiera en `out`. Conviene pasar `out` siempre que uses `where` (ver [[concepto_ufuncs]]).

### `dtype` / `casting`
Igual que en toda ufunc: `dtype` fuerza el tipo de cómputo/salida y `casting` controla las
conversiones permitidas al escribir en `out`. Rara vez se tocan.

## El caso N-D

`np.trunc` es **element-wise**: actúa posición a posición, sin `axis` ni colapso de ejes. El shape de
la salida es idéntico al de la entrada en cualquier dimensión.

```python
M = np.array([[ 1.9, -1.9],
              [ 2.5, -2.5]])
np.trunc(M)
# array([[ 1., -1.],
#        [ 2., -2.]])      mismo shape (2, 2), siempre hacia 0

T = np.random.rand(3, 4, 5) * 10 - 5
np.trunc(T).shape           # (3, 4, 5)  → la forma se conserva
```

## Vectorización

`np.trunc` reemplaza un bucle Python con `math.trunc` por elemento; la ufunc recorre la memoria en C
respetando los `strides` (ver [[concepto_vectorizacion]]):

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.trunc(arr.flat[i])

# Vectorizado:
np.trunc(arr)
```

## Valor de retorno

Devuelve un `ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** y dtype
**float**:

| Entrada (shape, dtype) | salida (shape) | dtype salida |
|------------------------|----------------|--------------|
| `(n,)` float64 | `(n,)` | `float64` |
| `(m, n)` float32 | `(m, n)` | `float32` |
| `(n,)` int64 | `(n,)` | `float64` (promovido) |
| escalar `-2.7` | `()` | `np.float64` (valor `-2.0`) |

El valor es entero matemáticamente, pero el **tipo es float**; usa `.astype(int)` para enteros.

## Casos de uso

### Quedarse con la parte entera (hacia cero)
```python
np.trunc([3.9, -3.9, 0.7])   # array([ 3., -3.,  0.])
```

### Comparativa floor / ceil / trunc / round (positivo y negativo)

La diferencia entre las cuatro se ve mejor con un valor positivo y uno negativo:

| `x` | `np.floor` (→ −∞) | `np.ceil` (→ +∞) | `np.trunc` (→ 0) | `np.round` (par) |
|-----|-------------------|------------------|------------------|-------------------|
| `2.5` | `2.` | `3.` | `2.` | `2.` |
| `-2.5` | `-3.` | `-2.` | `-2.` | `-2.` |
| `2.7` | `2.` | `3.` | `2.` | `3.` |
| `-2.7` | `-3.` | `-2.` | `-2.` | `-3.` |

`trunc` y `floor` coinciden en positivos; `trunc` y `ceil` coinciden en negativos.

### N-D: separar parte entera y fraccionaria de un tensor
```python
T = np.array([[ 1.25, -1.75],
              [ 3.50, -0.40]])     # (2, 2)
parte_entera = np.trunc(T)
# array([[ 1., -1.],
#        [ 3., -0.]])
parte_frac = T - parte_entera      # lo que queda tras el punto
# array([[ 0.25, -0.75],
#        [ 0.5 , -0.4 ]])          → ambos mantienen shape (2, 2)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `trunc(-2.7)` da `-2`, no `-3` | trunca hacia cero, no hacia $-\infty$ | usar [[np.floor]] si quieres hacia $-\infty$ |
| Esperar int y recibir float | `trunc` siempre devuelve float | `.astype(int)` |
| `TypeError` con complejos | truncamiento no definido para complejos | aplicar a `.real`/`.imag` |
| Confundir con `int(x)` por elemento | `int()` también trunca hacia 0, pero no vectoriza | `np.trunc` es la versión array |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que conserva el shape
- [[np.floor]] — coincide en positivos; difiere en negativos
- [[np.ceil]] — coincide en negativos
- [[np.rint]] · [[np.round]]
- [[Librerias/Numpy/np/operaciones/redondeo_signo/index\|redondeo_signo — la familia completa]]
