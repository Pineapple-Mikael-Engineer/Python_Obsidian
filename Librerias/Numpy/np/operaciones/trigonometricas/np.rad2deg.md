---
title: np.rad2deg — convierte radianes a grados elemento a elemento (ufunc)
aliases:
  - rad2deg
  - np.rad2deg
  - degrees
  - np.degrees
  - radianes a grados
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

# np.rad2deg — convierte radianes a grados elemento a elemento (ufunc)

`np.rad2deg` es una **ufunc unaria**: multiplica cada elemento por $180/\pi$ para pasar de **radianes
a grados**, sin mirar a sus vecinos y **sin cambiar el shape**. Es el paso para **leer** en grados los
resultados de las funciones trigonométricas inversas ([[np.arctan2]], [[np.arcsin]], [[np.arccos]]),
que devuelven radianes. Tiene el alias exacto `np.degrees` (misma función). Es la inversa de
[[np.deg2rad]].

## La idea en una fórmula

Cada elemento se escala de forma independiente por la constante $180/\pi$; el shape se **conserva**:

$$
z_i = x_i \cdot \frac{180}{\pi} \qquad (n_0,\dots,n_k)\ \xrightarrow{\ \text{rad2deg}\ }\ (n_0,\dots,n_k)
$$

Es una multiplicación por un escalar fijo; $\pi$ radianes se mapean a $180°$ (la composición con
[[np.deg2rad]] es la identidad).

| `x` (radianes) | `rad2deg(x)` (grados) |
|-----|------------------|
| `0` | `0.0` |
| `np.pi/2` | `90.0` |
| `np.pi` | `180.0` |
| `3*np.pi/2` | `270.0` |
| `2*np.pi` | `360.0` |

## Firma

```python
np.rad2deg(
    x,                 # array_like: ángulos en radianes
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
`array_like` **real** (ndarray, lista, escalar) interpretado como ángulos en radianes. Los enteros se
promueven a float. El shape de la salida es el de `x`.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar memoria y permite operar in-place
(`np.rad2deg(arr, out=arr)`). El dtype debe ser flotante y compatible bajo `casting`.

### `where` — máscara de cómputo
`array_like` booleano broadcasteable con `x`. Solo convierte donde es `True`; donde es `False`, la
posición conserva el valor previo de `out` (basura si no se pasó `out`). Úsalo junto con `out`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo flotante de cálculo/salida (p. ej. `float32`). No cambia el significado del valor, solo
su precisión.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla qué conversiones se permiten
al escribir en `out` o aplicar `dtype`.

### `order` — layout de memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Solo afecta al almacenamiento del resultado, no a sus valores.

## El caso N-D

`np.rad2deg` se aplica **elemento a elemento** sobre cualquier dimensión: no hay `axis`, no colapsa
nada, **conserva el shape**. Un tensor `(d0, d1, d2)` entra y sale como `(d0, d1, d2)`:

```python
T = np.array([[0., np.pi/2], [np.pi, 3*np.pi/2]])   # shape (2, 2), en radianes
np.rad2deg(T).shape       # (2, 2)  → shape idéntico
np.rad2deg(T)
# [[  0.,  90.],
#  [180., 270.]]
```

## Vectorización

`np.rad2deg` reemplaza un bucle que multiplicaría cada elemento por `180/pi`. La versión vectorizada
corre el bucle en C, sobre memoria contigua:

```python
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = arr.flat[i] * 180 / np.pi

# ufunc (un único bucle en C):
out = np.rad2deg(arr)
```

Es el principio de [[concepto_vectorizacion]]: describes la transformación, no la iteración. Multiplicar
por `180 / np.pi` a mano da lo mismo; `np.rad2deg` lo dice de forma explícita.

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** que `x` y dtype
**flotante**:

| Entrada (`x`) | dtype salida | nota |
|---------------|--------------|------|
| `float64` | `float64` | precisión por defecto |
| `float32` | `float32` | conserva la precisión |
| entero (`int64`...) | `float64` | se promueve a float |

```python
np.rad2deg(np.pi)             # 180.0  (escalar)
np.rad2deg([0, np.pi]).dtype  # float64
type(np.rad2deg([np.pi]))     # numpy.ndarray
```

## Casos de uso

### Leer en grados el ángulo de un vector
```python
ang = np.arctan2(1.0, 1.0)     # 0.7853… rad  (45° en el primer cuadrante)
np.rad2deg(ang)                # 45.0
```

### Equivalencia con el alias y con la fórmula manual
```python
np.degrees([np.pi/2, np.pi])   # [90., 180.]  (alias exacto)
np.rad2deg(np.pi) == np.pi * 180 / np.pi   # True
```

### N-D: pasar a grados un campo de fases
```python
fases = np.array([[0., np.pi/2], [np.pi, 3*np.pi/2]])   # (2, 2), radianes
np.rad2deg(fases)
# [[  0.,  90.],
#  [180., 270.]]                # mismo shape, ahora en grados
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Interpretar como grados una salida de `arctan2` | las inversas devuelven **radianes** | envolver con `np.rad2deg(...)` |
| Confundir el sentido de la conversión | `rad2deg` va de radianes **a** grados | para el camino inverso usar [[np.deg2rad]] |
| Posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` junto con `where=` |

## Notas relacionadas

- [[concepto_ufuncs]] — `np.rad2deg` es una ufunc unaria; hereda `out`/`where`/`dtype`/`casting`
- [[np.deg2rad]] — su inversa: grados → radianes
- [[np.arctan2]] · [[np.arcsin]] · [[np.arccos]] — devuelven radianes; esta conversión los pasa a grados
- [[Librerias/Numpy/np/operaciones/trigonometricas/index\|trigonométricas — todo en radianes]]
