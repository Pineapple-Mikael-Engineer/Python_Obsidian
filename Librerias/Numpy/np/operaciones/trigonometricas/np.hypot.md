---
title: np.hypot — hipotenusa (norma 2D) sin overflow intermedio (ufunc binaria)
aliases:
  - hypot
  - np.hypot
  - hipotenusa
  - norma euclidea
tags:
  - numpy
  - api/funcion
  - transformaciones

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

draft: false
---

# np.hypot — hipotenusa (norma 2D) sin overflow intermedio (ufunc binaria)

`np.hypot` es una **ufunc binaria**: toma dos tensores (los catetos) y devuelve $\sqrt{x_i^2 + y_i^2}$
**posición a posición**, es decir la longitud de la hipotenusa / la norma euclídea 2D. No reduce
ningún eje: alinea las entradas por [[concepto_broadcasting|broadcasting]] y produce la **shape
común**. Su valor frente a escribir `np.sqrt(x**2 + y**2)` a mano es que **evita el overflow/underflow
intermedio**: nunca calcula $x^2$ ni $y^2$ explícitamente, así que funciona con magnitudes que
desbordarían al elevarse al cuadrado. La pregunta al usarla no es "¿qué eje desaparece?" (ninguno)
sino **"¿qué shape común sale del broadcasting de los dos catetos?"** (ver [[concepto_ufuncs]]).

## La idea en una fórmula

La operación es **elemento a elemento**: cada posición de la salida es la hipotenusa de las posiciones
correspondientes de las entradas, tras alinearlas por broadcasting.

$$
z_i = \sqrt{x_i^{\,2} + y_i^{\,2}}
$$

y en N-D, con los índices recorriendo la shape común:

$$
z_{i_0\dots i_k} = \sqrt{x_{i_0\dots i_k}^{\,2} + y_{i_0\dots i_k}^{\,2}}
$$

El **mapa de shapes es el de broadcasting**: las entradas se alinean **por la derecha**, se rellena con
`1` a la izquierda y cada eje toma el `max` (válido si en cada eje coinciden o uno es `1`):

$$
(\dots, a_{k-1}, a_k),\ (\dots, b_{k-1}, b_k)\ \xrightarrow{\ \text{broadcast}\ }\ (\dots,\,\max(a_{k-1},b_{k-1}),\,\max(a_k,b_k))
$$

```text
x      (3,)            catetos horizontales
y      (3, 1)          catetos verticales  →  (3, 1)
---------------
eje -1:  3 vs 1  →  3      ← uno es 1, se estira
eje -2:  1 vs 3  →  3      ← x se rellena a (1, 3)
---------------
z      (3, 3)          tabla de hipotenusas
```

Toda la lógica de alineación vive en [[concepto_broadcasting]].

## Firma

```python
np.hypot(
    x1,                     # array_like: primer cateto
    x2,                     # array_like: segundo cateto
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

### `x1`, `x2` — los catetos
`array_like` **real** (ndarray, lista, escalar). Deben ser **broadcasteables** entre sí; sus shapes se
alinean por la derecha. El `dtype` de salida sale de promover ambos. Si ambos son escalares, el retorno
es un escalar de NumPy, no un `ndarray`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida (la del broadcast). Evita asignar memoria nueva; útil en
bucles. El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con las entradas. Solo se calcula donde es `True`; en el resto, la
salida **conserva lo que hubiera en `out`**. Por eso con `where` casi siempre se pasa `out` explícito
(si no, esas posiciones quedan sin inicializar).

### `dtype` — tipo de cómputo y de salida
Fuerza el tipo flotante en el que se opera y se devuelve (p. ej. `float32`). Controla la precisión del
resultado.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`; si la conversión necesaria no entra en la política, la ufunc
**lanza error** en vez de truncar en silencio.

### `order` — layout en memoria de la salida
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta a **cómo** se almacena el resultado, no a sus valores.

## Broadcasting y el caso N-D

`np.hypot` no tiene `axis`: su comportamiento en N-D lo dicta enteramente el broadcasting. La regla es
mecánica —alinear por la derecha, rellenar con `1`, tomar el `max` por eje—:

| `x1.shape` | `x2.shape` | salida | lectura |
|-----------|-----------|--------|---------|
| `()` escalar | `()` escalar | `()` | una sola hipotenusa |
| `(n,)` | `(n,)` | `(n,)` | hipotenusa par a par (norma de `n` vectores 2D) |
| `(n,)` | `()` escalar | `(n,)` | un cateto fijo contra cada elemento |
| `(m, 1)` | `(1, n)` | `(m, n)` | malla: hipotenusa de cada par `(x_i, y_j)` |
| `(b, n)` | `(b, n)` | `(b, n)` | norma 2D por elemento de un lote |

Ejemplo: malla de distancias al origen con dos vectores de coordenadas:

```python
x = np.array([3., 4., 5.])       # (3,) → (1, 3)
y = np.array([0., 6., 8.])[:, None]   # (3, 1)
np.hypot(x, y)                   # (3, 3)
# [[ 3.        ,  4.        ,  5.        ],
#  [ 6.70820393,  7.21110255,  7.81024968],
#  [ 8.54400375,  8.94427191,  9.43398113]]
```

## Vectorización

`np.hypot` reemplaza el bucle Python que calcularía `math.hypot` posición a posición. La ufunc corre en
C sobre memoria contigua, respeta los `strides` y aplica broadcasting sin materializar formas
intermedias:

```python
import math
# Bucle Python (lento, explícito):
out = np.empty_like(x)
for i in range(x.size):
    out.flat[i] = math.hypot(x.flat[i], y.flat[i])

# Vectorizado (un único bucle en C, con broadcasting):
np.hypot(x, y)
```

Es el principio de [[concepto_vectorizacion]]: describes *qué* operación aplicar a cada posición, no
*cómo* iterar. Además es **numéricamente más robusto** que `np.sqrt(x**2 + y**2)`: la versión a mano
calcula los cuadrados y puede **desbordar** (con `x` grande, `x**2` se va a `inf`) o perder precisión
con valores muy pequeños; `np.hypot` reescala internamente para evitarlo.

## Valor de retorno

La salida tiene la **shape común del broadcasting** de las entradas y dtype **flotante**; el tipo sale
de las reglas de promoción.

| `x1` | `x2` | salida (shape) | tipo |
|------|------|----------------|------|
| escalar | escalar | `()` | **escalar de NumPy** (`np.float64`...) |
| `(n,)` | escalar | `(n,)` | `ndarray` |
| `(n,)` | `(n,)` | `(n,)` | `ndarray` |
| `(m, 1)` | `(1, n)` | `(m, n)` | `ndarray` |
| entero | entero | según shape | `float64` (se promueve a float) |

```python
np.hypot(3, 4)                 # 5.0   (escalar de NumPy)
type(np.hypot(3, 4))           # numpy.float64
type(np.hypot([3], [4]))       # numpy.ndarray
np.hypot([3, 5], [4, 12]).dtype  # float64
```

## Casos de uso

### Hipotenusa básica (el clásico 3-4-5)
```python
np.hypot(3.0, 4.0)             # 5.0
np.hypot([3, 5, 8], [4, 12, 15])   # [ 5., 13., 17.]
```

### Norma de un conjunto de vectores 2D
```python
vx = np.array([1., -3., 0.])
vy = np.array([0.,  4., 5.])
np.hypot(vx, vy)               # [1., 5., 5.]  → longitud de cada vector
```

### Robustez frente a overflow (lo que aporta hypot)
```python
big = 1e200
np.sqrt(big**2 + big**2)       # inf   ← big**2 desborda a float64
np.hypot(big, big)             # 1.4142…e200   ← sin overflow intermedio
```

### Mapa de distancias al origen (broadcasting N-D)
```python
xs = np.linspace(-1, 1, 3)         # (3,)
ys = np.linspace(-1, 1, 3)[:, None] # (3, 1)
np.hypot(xs, ys)                   # (3, 3) → distancia de cada celda al origen
# [[1.41421356, 1.        , 1.41421356],
#  [1.        , 0.        , 1.        ],
#  [1.41421356, 1.        , 1.41421356]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `inf` con `np.sqrt(x**2+y**2)` | `x**2` desborda el float antes de la raíz | usar `np.hypot(x, y)` (sin cuadrado explícito) |
| `operands could not be broadcast together` | shapes de los catetos incompatibles | alinear por la derecha; ver [[concepto_broadcasting]] |
| Esperar `int` y recibir `float` | la raíz siempre devuelve float | castear aparte con `.astype(int)` si procede |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |
| Usarla para norma N-D (no solo 2 catetos) | `np.hypot` es **binaria** (2 entradas) | para norma de muchos ejes usar `np.linalg.norm` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.hypot` es una ufunc binaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_broadcasting]] — la alineación de shapes que gobierna su salida
- [[np.arctan2]] — el ángulo del mismo vector; juntos dan la forma polar `(r, θ)`
- [[np.sqrt]] · [[np.square]] · [[np.add]]
- [[Librerias/Numpy/np/operaciones/trigonometricas/index\|trigonométricas — todo en radianes]]
