---
title: np.exp2 — exponencial en base 2 (2^x) elemento a elemento (ufunc)
aliases:
  - exp2
  - np.exp2

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

# np.exp2 — exponencial en base 2 (2^x) elemento a elemento (ufunc)

`np.exp2` es una **ufunc unaria**: aplica $2^{x_i}$ a cada elemento, sin mirar a sus vecinos y **sin
cambiar el shape**. Es la exponencial en **base 2**, idéntica en valor a `2 ** x` y a
`np.power(2, x)`, pero más precisa y directa. Aparece de forma natural en contextos **binarios**
(tamaños de potencias de 2, niveles de bits) y en **escalas log2**, donde es la inversa de
[[np.log2]]. Es la versión base-2 de [[np.exp]].

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = 2^{x_i} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{exp2}\ }\ (n_0,\dots,n_k)
$$

Estrictamente creciente y positiva; sumar `1` a la entrada **duplica** la salida ($2^{x+1}=2\cdot 2^x$).
Para `x` entero da exactamente las potencias de 2.

| `x` | $2^{x}$ |
|-----|---------|
| `-1` | `0.5` |
| `0` | `1.0` |
| `3` | `8.0` |
| `10` | `1024.0` |
| `1100` | `inf` (overflow) |

## Firma

```python
np.exp2(
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
`array_like` real (ndarray, lista, escalar). Los enteros se promueven a float. El shape de la salida
es exactamente el de `x`. Como toda exponencial, **desborda** a `inf` para `x` grande (`~1024` en
`float64`).

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.exp2(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula donde es `True`; donde es `False`, la
posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). Importa para precisión y umbral de
overflow: en `float32` desborda antes (`~128`) que en `float64` (`~1024`).

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se
permiten al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.exp2` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[0., 1.], [2., 3.]],
              [[-1., 4.], [0.5, 10.]]])   # shape (2, 2, 2)
np.exp2(T).shape       # (2, 2, 2)  → shape idéntico
np.exp2(T)
# [[[ 1.        ,  2.        ], [ 4.        ,  8.        ]],
#  [[ 0.5       , 16.        ], [ 1.41421356, 1024.       ]]]
```

## Vectorización

`np.exp2` reemplaza un bucle que calcularía `2 ** x` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = 2.0 ** arr.flat[i]

# ufunc (un único bucle en C):
out = np.exp2(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión completa |
| `float32` | `float32` | desborda antes (`~128`) |
| entero (`int64`...) | `float64` | se promueve a float; el resultado **no es int** |

```python
np.exp2(np.array([0., 3.])).dtype   # float64
np.exp2([0, 1, 2, 10])              # array([   1.,    2.,    4., 1024.])
np.exp2(1100)                       # inf  (+ RuntimeWarning: overflow)
```

## Casos de uso

### Tamaños como potencias de 2
```python
bits = np.array([8, 10, 16, 20])
capacidad = np.exp2(bits)           # [256., 1024., 65536., 1048576.]
```

### Reconstruir desde una escala log2 (inversa de np.log2)
```python
octavas = np.array([0., 1., 2., 3.])
frecuencias = 440.0 * np.exp2(octavas)   # subir octavas duplica la frecuencia
```

### N-D: niveles de cuantización por elemento
```python
niveles = np.array([[1, 2], [4, 8]])     # (2, 2): bits por canal
valores = np.exp2(niveles)               # [[2., 4.], [16., 256.]]  mismo shape (2, 2)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar `int` y recibir `float` | `exp2` siempre devuelve float | castear con `.astype(int)` si el valor es entero |
| `inf` / `RuntimeWarning: overflow` | `x` grande (`>1024` en float64) | acotar `x` antes |
| Confundir base | `np.exp` es base $e$, no base 2 | usar `np.exp2` para $2^x$ |
| Buscar la inversa | el camino de vuelta es el logaritmo base 2 | usar [[np.log2]] |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.exp2` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.log2]] — su pareja inversa: logaritmo en base 2
- [[np.exp]] — la exponencial natural ($e^x$)
- [[np.power]] · [[np.expm1]]
