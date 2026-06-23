---
title: np.arccos — arcocoseno (inverso del coseno) elemento a elemento (ufunc)
aliases:
  - arccos
  - np.arccos
  - arcocoseno
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

# np.arccos — arcocoseno (inverso del coseno) elemento a elemento (ufunc)

`np.arccos` es una **ufunc unaria**: aplica el **arcocoseno** $\arccos(x_i)$ a cada elemento,
devolviendo el ángulo **en radianes** cuyo coseno es $x_i$. Es el inverso de [[np.cos]], **no mira a
sus vecinos** y **conserva el shape**. Como `arcsin`, tiene **dominio restringido** a $x\in[-1,1]$
(el recorrido del coseno); fuera de ahí devuelve `nan` con warning. Su rango de salida es $[0,\pi]$
(la rama principal): a diferencia de `arcsin`, el resultado nunca es negativo. La pregunta al usarla
no es "¿qué eje desaparece?" sino **"¿está mi `x` dentro de [-1, 1]?"** —crítico al venir de un
producto escalar donde el redondeo puede dar `1.0000001`—.

## La idea en una fórmula

Cada elemento se transforma de forma independiente; el shape se **conserva**:

$$
z_i = \arccos(x_i) \in [0,\,\pi] \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \arccos\ }\ (n_0,\dots,n_k)
$$

es la rama del coseno invertible en $[0,\pi]$, definida solo donde $x_i\in[-1,1]$. Decrece de $\pi$
(en $x=-1$) a $0$ (en $x=1$); fuera del dominio → `nan`:

| `x` | $\arccos(x)$ (rad) | en grados |
|-----|--------------------|-----------|
| `-1` | `π ≈ 3.142` | `180°` |
| `-0.5` | `2.094` | `120°` |
| `0` | `π/2 ≈ 1.571` | `90°` |
| `0.5` | `1.047` | `60°` |
| `1` | `0.0` | `0°` |
| `1.5` | `nan` + warning | fuera de dominio |

## Firma

```python
np.arccos(
    x,                 # array_like: el tensor de entrada (real, en [-1, 1])
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
`array_like` **real** (ndarray, lista, escalar). Cada valor debe estar en $[-1,1]$; los enteros se
promueven a float. Fuera del dominio → `nan` + `RuntimeWarning`. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.arccos(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo calcula el arcocoseno donde es `True`; donde es
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

`np.arccos` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[[-1.0, -0.5], [0.0, 0.5]],
              [[1.0,  0.25], [0.75, -0.25]]])   # shape (2, 2, 2), todo en [-1, 1]
np.arccos(T).shape       # (2, 2, 2)  → shape idéntico
np.arccos(T)
# [[[3.1416, 2.0944], [1.5708, 1.0472]],
#  [[0.    , 1.3181], [0.7227, 1.8235]]]
```

## Vectorización

`np.arccos` reemplaza un bucle que llamaría a `math.acos` por elemento. La versión vectorizada corre
el bucle en C, sobre memoria contigua:

```python
import math
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = math.acos(arr.flat[i])

# ufunc (un único bucle en C):
out = np.arccos(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Soporta
`out`/`where`/`dtype`/`casting` como toda ufunc.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x`, dtype
**flotante** y valores en $[0,\pi]$ (radianes):

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | rama principal en `[0, π]`, nunca negativa |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |
| valor fuera de `[-1, 1]` | `float` con `nan` | sin ángulo real → `nan` + warning |

```python
np.arccos(0)                  # 1.5707963267948966  (π/2)
np.arccos(-1)                 # 3.141592653589793   (π)
np.arccos([1, 0.5, 0]).dtype  # float64
```

## Casos de uso

### Ángulo entre dos vectores (similitud coseno)
```python
cos_sim = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
angulo  = np.arccos(np.clip(cos_sim, -1, 1))   # recorta: el redondeo puede dar 1.0000001
```

### Blindar el dominio frente al redondeo
```python
c = np.array([-1.0000003, 0.2, 1.0000001])   # fuera de [-1, 1] por punto flotante
np.arccos(np.clip(c, -1, 1))                  # sin nan
```

### N-D: arcocoseno por elemento de un tensor
```python
T = np.array([[[-1.0, -0.5], [0.0, 0.5]],
              [[1.0,  0.25], [0.75, -0.25]]])   # (2, 2, 2), dominio válido
np.arccos(T)
# [[[3.1416, 2.0944], [1.5708, 1.0472]],
#  [[0.    , 1.3181], [0.7227, 1.8235]]]         # mismo shape
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `nan` por `1.0000001` | redondeo en el producto escalar saca `x` de `[-1, 1]` | `np.clip(x, -1, 1)` antes de invertir |
| `nan` + `RuntimeWarning` | `x` fuera del dominio `[-1, 1]` | recortar con [[np.clip]] |
| Resultado "en grados raro" | el retorno está en **radianes** | convertir con `np.rad2deg` |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.arccos` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[concepto_vectorizacion]] — por qué sustituye al bucle por elemento
- [[np.cos]] — la función que invierte ($\cos$ restringido a $[0,\pi]$)
- [[np.arcsin]] · [[np.arctan]] · [[np.arctan2]] · [[np.clip]] · [[np.rad2deg]]
