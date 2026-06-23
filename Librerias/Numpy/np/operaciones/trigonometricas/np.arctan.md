---
title: np.arctan — arcotangente (inverso de la tangente) elemento a elemento (ufunc)
aliases:
  - arctan
  - np.arctan
  - arcotangente
tags:
  - numpy
  - api/funcion
  - trigonometricas

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
  - concepto_vectorizacion

draft: false
---

# np.arctan — arcotangente (inverso de la tangente) elemento a elemento (ufunc)

`np.arctan` es una **ufunc unaria**: aplica la **arcotangente** $\arctan(x_i)$ a cada elemento,
devolviendo el ángulo **en radianes** cuya tangente es $x_i$. Es el inverso de [[np.tan]], **no mira
a sus vecinos** y **conserva el shape**. A diferencia de `arcsin`/`arccos`, **acepta todo
$\mathbb{R}$**: no hay dominio restringido ni `nan` por entrada fuera de rango. Su salida vive en el
intervalo **abierto** $(-\pi/2,\pi/2)$, al que se aproxima asintóticamente cuando $x\to\pm\infty$. Su
límite: solo distingue **2 cuadrantes**; para el ángulo de un punto $(x,y)$ con el cuadrante correcto
se usa [[np.arctan2]].

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \arctan(x_i) \in \left(-\tfrac{\pi}{2},\,\tfrac{\pi}{2}\right) \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \arctan\ }\ (n_0,\dots,n_k)
$$

es la rama de la tangente invertible en $(-\pi/2,\pi/2)$, definida para **cualquier** real (el
recorrido de la tangente es todo $\mathbb{R}$). Es impar y monótona creciente; los extremos son
asíntotas que nunca se alcanzan:

| `x` | $\arctan(x)$ (rad) | en grados |
|-----|--------------------|-----------|
| `-∞` | `→ -π/2` (no alcanzado) | `→ -90°` |
| `-1` | `-π/4 ≈ -0.785` | `-45°` |
| `0` | `0.0` | `0°` |
| `1` | `π/4 ≈ 0.785` | `45°` |
| `+∞` | `→ π/2` (no alcanzado) | `→ 90°` |

## Firma

```python
np.arctan(
    x,                 # array_like: el tensor de entrada (real, cualquier valor)
    /,
    out=None,          # ndarray | None: destino preasignado
    *,
    where=True,        # array_like[bool]: máscara de cómputo
    casting='same_kind',  # política de conversión de tipos
    order='K',         # 'K' | 'C' | 'F' | 'A': layout de memoria del resultado
    dtype=None,        # dtype: fuerza el tipo de cómputo/salida
) -> ndarray | escalar
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` **real** (ndarray, lista, escalar). Acepta **cualquier** valor real, sin restricción de
dominio; los enteros se promueven a float. Incluso `np.inf` es válido (da $\pm\pi/2$). El shape de la
salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.arctan(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula la arcotangente donde es `True`; donde es
`False`, la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con
`out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). El resultado es siempre flotante.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se
permiten al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.arctan` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[-100.0, -1.0], [0.0, 1.0]],
              [[100.0,   0.5], [2.0, -0.5]]])   # shape (2, 2, 2), cualquier real
np.arctan(T).shape       # (2, 2, 2)  → shape idéntico
np.arctan(T)
# [[[-1.5608, -0.7854], [ 0.    ,  0.7854]],
#  [[ 1.5608,  0.4636], [ 1.1071, -0.4636]]]
```

## Vectorización

`np.arctan` reemplaza un bucle que llamaría a `math.atan` por elemento. La versión vectorizada corre
el bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.atan(arr.flat[i])

# ufunc (un único bucle en C):
out = np.arctan(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where`/`dtype`/`casting` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x`, dtype
**flotante** y valores en el intervalo abierto $(-\pi/2,\pi/2)$ (radianes):

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | rama principal en `(-π/2, π/2)` |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |
| `np.inf` / `-np.inf` | `float` | `π/2` / `-π/2` (sin warning) |

```python
np.arctan(1)                  # 0.7853981633974483  (π/4)
np.arctan(np.inf)             # 1.5707963267948966  (π/2)  → sin nan
np.arctan([0, 1, -1]).dtype   # float64
```

## Casos de uso

### Ángulo de una pendiente
```python
angulo = np.rad2deg(np.arctan(dy / dx))   # inclinación en grados
```

### El cuadrante: por qué arctan2 lo resuelve
```python
np.arctan(1 / 1)        # π/4    para (x, y) = (1, 1)   → 1er cuadrante, OK
np.arctan(-1 / -1)      # π/4    para (x, y) = (-1, -1) → ¡mismo valor! el signo se perdió
np.arctan2(-1, -1)      # -3π/4  → cuadrante correcto usando AMBOS signos
```

### N-D: arcotangente por elemento de un tensor
```python
T = np.array([[[-100.0, -1.0], [0.0, 1.0]],
              [[100.0,   0.5], [2.0, -0.5]]])   # (2, 2, 2)
np.arctan(T)
# [[[-1.5608, -0.7854], [ 0.    ,  0.7854]],
#  [[ 1.5608,  0.4636], [ 1.1071, -0.4636]]]     # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Cuadrante incorrecto | `arctan(y/x)` pierde el signo de cada componente | usar [[np.arctan2]] con `(y, x)` separados |
| `ZeroDivisionError` / `inf` al formar `y/x` | divides por `x = 0` antes de pasar a `arctan` | usar [[np.arctan2]], que maneja `x = 0` |
| Resultado "en grados raro" | el retorno está en **radianes** | convertir con `np.rad2deg` |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.arctan` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.tan]] — la función que invierte ($\tan$ restringida a $(-\pi/2,\pi/2)$)
- [[np.arctan2]] — la versión binaria con el cuadrante correcto a partir de `(y, x)`
- [[np.arcsin]] · [[np.arccos]] · [[np.rad2deg]]
