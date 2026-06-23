---
title: np.reciprocal — recíproco (1/x) elemento a elemento (ufunc)
aliases:
  - reciprocal
  - np.reciprocal
  - reciproco
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

draft: false
---

# np.reciprocal — recíproco (1/x) elemento a elemento (ufunc)

`np.reciprocal` es una **ufunc unaria**: calcula el **recíproco** $1/x_i$ de cada elemento, de forma
independiente y **sin cambiar el shape**. Tiene una **trampa grave**: con arrays de **enteros** hace
**división entera**, así que `np.reciprocal(2)` devuelve `0`, no `0.5` — y para casi cualquier entero
$\ne \pm 1$ el resultado es `0`. La regla de oro es **usar siempre floats**. Además, $x_i = 0$ produce
`inf` con warning.

> [!danger] Con enteros, `reciprocal` da CASI TODO CEROS
> `np.reciprocal(np.array([1, 2, 3, 4]))` → `array([1, 0, 0, 0])`. El recíproco entero de cualquier
> $|x| > 1$ es `0` (división entera de `1 // x`). **Convierte a float antes**:
> `np.reciprocal(arr.astype(float))` o construye el array con `dtype=float`.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \frac{1}{x_i} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{reciprocal}\ }\ (n_0,\dots,n_k)
$$

La operación está definida para $x_i \ne 0$; en $x_i = 0$ devuelve $\pm\infty$ (con `RuntimeWarning`).

| `x` (float) | $1/x$ |
|-------------|-------|
| `2.0` | `0.5` |
| `4.0` | `0.25` |
| `-0.5` | `-2.0` |
| `1.0` | `1.0` |
| `0.0` | `inf` + warning |
| `2` (int) | `0` ⚠️ división entera |

## Firma

```python
np.reciprocal(
    x,                 # array_like: el tensor de entrada (preferiblemente float)
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
`array_like` (ndarray, lista, escalar). **El dtype manda**: con enteros la división es entera y casi
todo sale `0`; con floats devuelve el recíproco real. Acepta complejos. El shape de la salida es el de
`x`. En la práctica, **conviértelo a float** antes de usar la función.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.reciprocal(arr, out=arr)`). El dtype debe ser flotante/complejo y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el recíproco donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Útil para
**saltarse los ceros**: `np.reciprocal(x, out=res, where=x != 0)`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo de cálculo/salida. Es **la solución directa a la trampa de los enteros**:
`np.reciprocal(arr, dtype=float)` calcula en flotante aunque `arr` sea entero.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.reciprocal` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1., 2.], [4., 5.]],
              [[8., 10.], [20., 25.]]])   # shape (2, 2, 2)
np.reciprocal(T).shape     # (2, 2, 2)  → shape idéntico
np.reciprocal(T)
# [[[1.  , 0.5 ], [0.25, 0.2 ]],
#  [[0.125, 0.1], [0.05, 0.04]]]
```

## Vectorización

`np.reciprocal` reemplaza un bucle que invertiría cada elemento. La versión vectorizada corre el bucle
en C, sobre memoria contigua:

```python
# Bucle Python (lento):
out = np.empty_like(arr, dtype=float)
for i in range(arr.size):
    out.flat[i] = 1.0 / arr.flat[i]

# ufunc (un único bucle en C):
out = np.reciprocal(arr.astype(float))
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Equivale a
`1 / x` (que invoca `np.divide`), pero `1 / x` **promueve a float** automáticamente y por eso suele ser
preferible cuando hay enteros de por medio. Soporta `out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x`. El dtype se
**hereda** de la entrada (de ahí la trampa con enteros):

| Entrada (`x`) | dtype salida | resultado |
|---------------|--------------|-----------|
| `float64` | `float64` | recíproco real correcto |
| `float32` | `float32` | recíproco real correcto |
| `int64` | `int64` | **división entera** → casi todo `0` ⚠️ |
| `complex128` | `complex128` | recíproco complejo |
| float `0.0` | `float` | `inf` + `RuntimeWarning` |

```python
np.reciprocal(np.array([1., 2., 4.]))   # array([1.  , 0.5 , 0.25])
np.reciprocal(np.array([1, 2, 4]))      # array([1, 0, 0])  ⚠️ enteros
np.reciprocal(np.array([2, 4]), dtype=float)   # array([0.5 , 0.25])
```

## Casos de uso

### Invertir un array (asegurando float)
```python
tasas = np.array([2, 4, 5])
periodos = np.reciprocal(tasas.astype(float))   # [0.5 , 0.25, 0.2 ]
```

### Saltarse los ceros con `where`
```python
x = np.array([1., 0., 4., 0.])
res = np.zeros_like(x)
np.reciprocal(x, out=res, where=x != 0)   # [1., 0., 0.25, 0.]  → sin inf
```

### N-D: recíproco por elemento de un tensor
```python
T = np.array([[[1., 2.], [4., 5.]],
              [[8., 10.], [20., 25.]]])   # (2, 2, 2)
np.reciprocal(T)
# [[[1.   , 0.5 ], [0.25, 0.2 ]],
#  [[0.125, 0.1 ], [0.05, 0.04]]]         # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado casi todo `0` | array de **enteros** → división entera | `arr.astype(float)` o `dtype=float` |
| `inf` + `RuntimeWarning` | algún `x == 0` | filtrar con `where=x != 0` y `out` inicializado |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.reciprocal` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.divide]] — `1 / x` general; promueve a float automáticamente
- [[np.power]] · [[np.sqrt]] · [[np.square]]
