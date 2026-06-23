---
title: np.cbrt — raíz cúbica elemento a elemento (ufunc)
aliases:
  - cbrt
  - np.cbrt
  - raiz cubica
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

# np.cbrt — raíz cúbica elemento a elemento (ufunc)

`np.cbrt` es una **ufunc unaria**: aplica la **raíz cúbica** $\sqrt[3]{x_i}$ a cada elemento, de forma
independiente y **sin cambiar el shape**. Su gran ventaja frente a [[np.sqrt]] o a `x ** (1/3)` es que
**funciona con negativos**: `np.cbrt(-8)` da `-2.0`, mientras que `(-8) ** (1/3)` da `nan` (y
`np.power(-8, 1/3)` también). Por eso es la forma correcta de tomar raíces cúbicas de datos reales con
signo arbitrario.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \sqrt[3]{x_i} = \operatorname{sign}(x_i)\,|x_i|^{1/3} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{cbrt}\ }\ (n_0,\dots,n_k)
$$

Toma siempre la **raíz real** (la que conserva el signo de $x_i$), no la raíz principal compleja. Por
eso está definida sobre **todos** los reales, incluidos los negativos.

| `x` | $\sqrt[3]{x}$ |
|-----|---------------|
| `8` | `2.0` |
| `27` | `3.0` |
| `-8` | `-2.0` |
| `0` | `0.0` |
| `-1` | `-1.0` |

## Firma

```python
np.cbrt(
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
`array_like` **real** (ndarray, lista, escalar), de cualquier signo. Los enteros se promueven a float.
**No acepta complejos** (a diferencia de `np.sqrt`): es una raíz real puramente. El shape de la salida
es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.cbrt(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula la raíz donde es `True`; donde es `False`,
la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (`float32`, `float64`). No admite complejos.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.cbrt` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[1., 8.], [27., 64.]],
              [[-1., -8.], [-27., -64.]]])   # shape (2, 2, 2)
np.cbrt(T).shape       # (2, 2, 2)  → shape idéntico
np.cbrt(T)
# [[[ 1.,  2.], [ 3.,  4.]],
#  [[-1., -2.], [-3., -4.]]]               # los negativos SÍ funcionan
```

## Vectorización

`np.cbrt` reemplaza un bucle que calcularía la raíz cúbica por elemento. La versión vectorizada corre
el bucle en C, sobre memoria contigua:

```python
# Bucle Python (lento, y con el problema de los negativos):
out = np.empty_like(arr)
for i in range(arr.size):
    x = arr.flat[i]
    out.flat[i] = np.sign(x) * abs(x) ** (1/3)   # hay que tratar el signo a mano

# ufunc (un único bucle en C, ya gestiona el signo):
out = np.cbrt(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Además de
ser más rápida, evita el truco manual del signo que necesita `x ** (1/3)`. Soporta `out`/`where` como
toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | conserva la precisión |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |
| real `< 0` | `float` | devuelve la raíz real negativa, **sin warning** |

```python
np.cbrt([8, 27, 64])        # array([2., 3., 4.])
np.cbrt(-8)                 # -2.0     ← sin nan, sin warning
np.power(-8, 1/3)           # nan      ← por eso cbrt es la opción correcta
```

## Casos de uso

### Raíz cúbica de datos con signo (lo que sqrt/power no resuelven)
```python
x = np.array([-27., -1., 0., 8., 64.])
np.cbrt(x)                  # [-3., -1.,  0.,  2.,  4.]
x ** (1/3)                  # [nan, nan, 0., 2., 4.]  → falla en negativos
```

### Invertir un cubo (despejar el lado de un volumen)
```python
volumenes = np.array([8., 27., 125.])
lados = np.cbrt(volumenes)  # [2., 3., 5.]
```

### N-D: raíz cúbica por elemento de un tensor
```python
T = np.array([[[1., 8.], [27., 64.]],
              [[-1., -8.], [-27., -64.]]])   # (2, 2, 2)
np.cbrt(T)
# [[[ 1.,  2.], [ 3.,  4.]],
#  [[-1., -2.], [-3., -4.]]]               # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `nan` al usar `x ** (1/3)` con negativos | la potencia general no define raíces de negativos | usar `np.cbrt`, que toma la raíz real |
| `TypeError` con entrada compleja | `cbrt` solo acepta reales | usar `np.power(z, 1/3)` para complejos |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.cbrt` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.sqrt]] — la raíz cuadrada (que **no** admite negativos en reales)
- [[np.power]] · [[np.square]] · [[np.sign]]
