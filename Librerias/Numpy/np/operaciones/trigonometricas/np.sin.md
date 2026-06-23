---
title: np.sin — seno (en radianes) elemento a elemento (ufunc)
aliases:
  - sin
  - np.sin
  - seno
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

# np.sin — seno (en radianes) elemento a elemento (ufunc)

`np.sin` es una **ufunc unaria**: aplica el **seno** $\sin(x_i)$ a cada elemento, sin mirar a sus
vecinos y **sin cambiar el shape**. La clave que arruina la mitad de los usos: el argumento se
interpreta en **radianes**, no en grados — para grados hay que pasar antes por [[np.deg2rad]]. La
salida vive siempre en el rango $[-1, 1]$ y es **periódica** con periodo $2\pi$. Es la pareja de
[[np.cos]] y la base de [[np.tan]] (que es $\sin/\cos$).

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \sin(x_i) \in [-1, 1] \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \sin\ }\ (n_0,\dots,n_k)
$$

El argumento $x_i$ está en **radianes**. La función es periódica, $\sin(x_i + 2\pi) = \sin(x_i)$, así
que solo importa $x_i \bmod 2\pi$ (la referencia útil es $\pi \approx 3.1416$, disponible como
`np.pi`).

| `x` (rad) | $\sin(x)$ |
|-----------|-----------|
| `0` | `0.0` |
| `np.pi/6` | `0.5` |
| `np.pi/2` | `1.0` |
| `np.pi` | `~0` (≈1.2e-16) |
| `3*np.pi/2` | `-1.0` |

## Firma

```python
np.sin(
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
(`np.sin(arr, out=arr)`). El dtype debe ser flotante (la salida lo es) y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el seno donde es `True`; donde es `False`,
la posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). La salida es siempre flotante.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten al
escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.sin` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa nada,
**conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[0, np.pi/2],
              [np.pi, 3*np.pi/2]])   # shape (2, 2)
np.sin(T).shape       # (2, 2)  → shape idéntico
np.sin(T)
# [[ 0.,  1.],
#  [ ~0., -1.]]
```

## Vectorización

`np.sin` reemplaza un bucle que llamaría a `math.sin` por elemento. La versión vectorizada corre el
bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.sin(arr.flat[i])

# ufunc (un único bucle en C):
out = np.sin(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x`, dtype
**flotante** y valores en $[-1, 1]$:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | rango `[-1, 1]` |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |

```python
np.sin(np.array([0.0, np.pi/2])).dtype   # float64
np.sin(0)                                 # np.float64(0.0)  → escalar
```

## Casos de uso

### Generar una onda senoidal sobre un linspace
```python
t = np.linspace(0, 2*np.pi, 1000)   # un periodo completo
onda = np.sin(t)                     # mismo shape (1000,), valores en [-1, 1]
```

### Grados → radianes antes del seno
```python
np.sin(np.deg2rad(90))   # 1.0      → correcto
np.sin(90)               # 0.894... → 90 radianes, casi seguro un error
```

### N-D: seno por elemento de un tensor
```python
T = np.array([[0, np.pi/6],
              [np.pi/2, np.pi]])     # (2, 2)
np.sin(T)
# [[0. , 0.5],
#  [1. , ~0.]]                       # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultados sin sentido | se pasaron grados, no radianes | convertir con [[np.deg2rad]] primero |
| Esperar `0` exacto en `np.pi` | redondeo flotante (sale ≈1.2e-16) | comparar con `np.isclose` |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.sin` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.cos]] — su pareja, desfasada $\pi/2$
- [[np.tan]] · [[np.deg2rad]] · [[np.arcsin]]
