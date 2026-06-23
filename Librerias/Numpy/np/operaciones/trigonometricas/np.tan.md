---
title: np.tan — tangente (en radianes) elemento a elemento (ufunc)
aliases:
  - tan
  - np.tan
  - tangente
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

# np.tan — tangente (en radianes) elemento a elemento (ufunc)

`np.tan` es una **ufunc unaria**: aplica la **tangente** $\tan(x_i) = \sin(x_i)/\cos(x_i)$ a cada
elemento, sin mirar a sus vecinos y **sin cambiar el shape**. Como en [[np.sin]] y [[np.cos]], el
argumento se interpreta en **radianes**, no en grados — para grados hay que pasar antes por
[[np.deg2rad]]. La trampa propia de la tangente: donde $\cos(x_i) \to 0$ (en $\pi/2$ y sus múltiplos
$\pi/2 + k\pi$) la función **diverge** hacia $\pm\infty$; como el float casi nunca cae exactamente en
$\pi/2$, NumPy no devuelve `inf` sino un **valor enorme** (≈1.6e16) e inestable.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \tan(x_i) = \frac{\sin(x_i)}{\cos(x_i)} \in (-\infty, \infty) \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \tan\ }\ (n_0,\dots,n_k)
$$

El argumento $x_i$ está en **radianes**. A diferencia de seno y coseno, el rango es **toda la recta
real**: cerca de las asíntotas $x_i = \pi/2 + k\pi$ (donde $\cos = 0$) el valor explota. La referencia
$\pi \approx 3.1416$ está en `np.pi`.

| `x` (rad) | $\tan(x)$ |
|-----------|-----------|
| `0` | `0.0` |
| `np.pi/4` | `~1.0` |
| `np.pi/2` | valor enorme (≈1.6e16, **no** `inf`) |
| `np.pi` | `~0` |
| `3*np.pi/4` | `~-1.0` |

## Firma

```python
np.tan(
    x,                 # array_like: el tensor de entrada (radianes)
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

### `x` — el tensor de entrada (en radianes)
`array_like` real (ndarray, lista, escalar) interpretado en **radianes**. Los enteros se promueven a
float. Si tienes grados, conviértelos antes con `np.deg2rad`; pasar grados crudos no da error, da un
resultado silenciosamente equivocado. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.tan(arr, out=arr)`). El dtype debe ser flotante (la salida lo es) y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula la tangente donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Útil para **saltar
las asíntotas**: enmascara los puntos cercanos a $\pi/2 + k\pi$. Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). La salida es siempre flotante.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten al
escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.tan` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[0, np.pi/4],
              [np.pi/2, np.pi]])     # shape (2, 2)
np.tan(T).shape       # (2, 2)  → shape idéntico
np.tan(T)
# [[0.000e+00, 1.000e+00],
#  [1.633e+16, ~0.       ]]          # el 1.6e16 es la asíntota en pi/2
```

## Vectorización

`np.tan` reemplaza un bucle que llamaría a `math.tan` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.tan(arr.flat[i])

# ufunc (un único bucle en C):
out = np.tan(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**; los valores no están acotados (pueden ser enormes cerca de las asíntotas):

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | rango no acotado; ≈1.6e16 cerca de `pi/2` |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |

```python
np.tan(np.array([0.0, np.pi/4])).dtype   # float64
np.tan(0)                                 # np.float64(0.0)  → escalar
```

## Casos de uso

### Pendiente a partir de un ángulo en grados
```python
pendiente = np.tan(np.deg2rad(angulo_grados))   # convierte grados antes
```

### Saltar las asíntotas con una máscara
```python
x = np.linspace(-np.pi, np.pi, 200)
seguro = np.abs(np.cos(x)) > 1e-6     # lejos de pi/2 + k*pi
out = np.full_like(x, np.nan)
np.tan(x, out=out, where=seguro)      # los puntos críticos quedan en NaN
```

### N-D: tangente por elemento de un tensor
```python
T = np.array([[0, np.pi/4],
              [np.pi/3, np.pi]])       # (2, 2)
np.tan(T)
# [[0.   , 1.   ],
#  [1.732, ~0.  ]]                     # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor gigantesco (≈1e16) | `x` cae cerca de `np.pi/2 + k*pi` (asíntota) | evitar/enmascarar la asíntota con `where=` |
| Esperar `inf` exacto en `np.pi/2` | el float no cae justo en `pi/2`; sale enorme pero finito | no comparar con `np.inf`; usar un umbral |
| Resultados sin sentido | se pasaron grados, no radianes | convertir con [[np.deg2rad]] primero |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.tan` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.sin]] · [[np.cos]] — la tangente es su cociente $\sin/\cos$
- [[np.deg2rad]] · [[np.arctan]] · [[np.arctan2]]
