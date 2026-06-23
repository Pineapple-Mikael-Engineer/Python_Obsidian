---
title: np.ptp — rango (peak to peak, max − min) a lo largo de un eje
aliases:
  - ptp
  - np.ptp
  - rango
  - peak to peak
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion

draft: false
---

# np.ptp — rango (peak to peak, max − min) a lo largo de un eje

`np.ptp` es una **reducción** que colapsa un eje a su **amplitud**: la diferencia entre el máximo y
el mínimo de ese eje (`max - min`). El nombre viene de *peak to peak*, "de pico a pico". Convierte un
`(2, 3)` en un `(3,)` (el rango de cada columna) o en un escalar (el rango global). Como toda
reducción, lo que importa es **qué eje desaparece**; equivale a `np.max(a, axis) - np.min(a, axis)`
pero en una pasada.

## La idea en una fórmula

El rango reduce un eje quedándose con la distancia entre sus dos extremos. Para una matriz $A$ de
shape $(m, n)$, reducir el eje `0` (las filas) produce un vector indexado por la columna $j$:

$$
\text{ptp}_j = \max_{i=0}^{m-1} A_{ij} \;-\; \min_{i=0}^{m-1} A_{ij}
\qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

El **mapa de shapes** es el de cualquier reducción: el eje de `axis` se elimina del shape.

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{ptp, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

El eje que aparece bajo $\max$ y $\min$ es el que se reduce y **desaparece** del shape (ver
[[concepto_axis_parametro]]). Con `keepdims=True` queda en tamaño 1; con `axis=None` se contraen
todos los ejes a un escalar `()`.

## Firma

```python
np.ptp(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    out=None,          # ndarray: destino preasignado
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
) -> ndarray | escalar
```

A diferencia de [[np.max]] / [[np.min]], `np.ptp` **no** tiene `initial` ni `where`.

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. El `dtype` se conserva,
y ahí está la trampa: como hay una **resta**, con enteros **sin signo** (`uint8`, `uint16`) el
`max - min` puede **desbordar** y dar un valor absurdo (ver Errores comunes).

### `axis` — qué eje se reduce
El parámetro central. `None` (defecto) calcula el rango sobre **todos** los elementos y devuelve un
escalar. Un `int` reduce ese eje. Una **tupla** reduce varios ejes a la vez:

```python
T = np.arange(2*3*4).reshape(2, 3, 4)
np.ptp(T, axis=None)      # escalar: rango global
np.ptp(T, axis=0).shape   # (3, 4)  → desaparece el eje 0
np.ptp(T, axis=1).shape   # (2, 4)  → desaparece el eje 1
np.ptp(T, axis=(0, 2)).shape  # (3,) → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje), lo idiomático para "el rango de la última dimensión"
sin importar cuántas haya.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1. Sirve para que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]), p. ej. al escalar
cada feature por su rango.

```python
M = np.array([[1, 9, 3], [7, 2, 8]])
M.ptp(axis=0).shape              # (3,)    → no broadcastea de vuelta a (2,3)
M.ptp(axis=0, keepdims=True).shape  # (1, 3)  → sí broadcastea
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype del resultado. Evita una asignación de memoria; útil en
bucles. Debe tener el shape exacto de salida.

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Léelo como "para cada combinación de los ejes que **sobreviven**, calculo `max − min` a lo largo del
que se reduce".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar | rango global |
| `(m, n)` | `0` | `(n,)` | un rango por **columna** |
| `(m, n)` | `1` | `(m,)` | un rango por **fila** |
| `(m, n)` | `None` | `()` | rango total |
| `(b, m, n)` | `0` | `(m, n)` | rango **a lo largo del lote**, celda a celda |
| `(b, m, n)` | `(1, 2)` | `(b,)` | la amplitud de cada matriz del lote |
| `(b, m, n)` | `-1` | `(b, m)` | rango de la última dimensión |

```python
# Lote de 5 imágenes RGB 2x2:  (5, 2, 2, 3)
imgs = np.arange(5*2*2*3).reshape(5, 2, 2, 3)
imgs.ptp(axis=(1, 2)).shape   # (5, 3)  → contraste espacial por canal e imagen
imgs.ptp(axis=0).shape        # (2, 2, 3) → variación píxel a píxel sobre el lote
imgs.ptp(axis=-1).shape       # (5, 2, 2) → rango entre canales de color
```
Con `keepdims=True`, esos resultados conservan los ejes reducidos en tamaño 1 (`(5, 1, 1, 3)`...),
listos para broadcastear contra `imgs`.

## Vectorización

`np.ptp` reemplaza un bucle de doble pasada (buscar el máximo y el mínimo y restarlos) escrito a
mano. Las dos versiones dan lo mismo, pero la vectorizada corre en C sobre memoria contigua:

```python
# Bucle Python (lento, explícito):
def ptp_cols(M):
    m, n = M.shape
    out = np.empty(n)
    for j in range(n):
        col = M[:, j]
        out[j] = col.max() - col.min()
    return out

# Vectorizado (NumPy recorre el eje 0 en C):
M.ptp(axis=0)
```
Es el mismo principio de [[concepto_vectorizacion]]: describes *qué* eje reducir, no *cómo* iterar.

## Valor de retorno

El **tipo** del retorno depende de `axis`; el **dtype** se conserva (sin promoción, de ahí el riesgo
de overflow con enteros sin signo):

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar de NumPy** (`np.int64`, `np.float64`...) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` |
| `(n,)` | `0` | `False` | `()` | escalar |

```python
np.ptp([1, 5, 2, 8])             # np.int64(7)   escalar: 8 − 1
M = np.array([[1, 9], [7, 2]])
np.ptp(M, axis=1)                # [8, 5]        ndarray, rango por fila
np.ptp(M, axis=0)                # [6, 7]        ndarray, rango por columna
```

> [!warning] No tiene variante `nan`
> No existe `np.nanptp`. Si hay `NaN`, se propaga (igual que en [[np.max]] / [[np.min]]). Filtra o
> enmascara los NaN antes, o calcula `np.nanmax(a, axis) - np.nanmin(a, axis)` a mano.

## Casos de uso

### Amplitud de una señal
```python
amplitud = np.ptp(onda)   # pico a pico
```

### Detectar columnas casi constantes
```python
datos = np.random.rand(100, 5)
rangos = np.ptp(datos, axis=0)        # (5,) → rango de cada feature
casi_constantes = rangos < 1e-6
```

### Escalar cada feature por su rango (reducción + broadcasting)
```python
X = np.array([[1., 10.], [3., 30.], [2., 20.]])   # (3, 2)
X / X.ptp(axis=0, keepdims=True)                  # cada columna a escala 1
```

### Rango por feature en un lote N-D (valores concretos)
```python
T = np.array([[[1, 8], [3, 2]],
              [[7, 4], [6, 5]]])      # shape (2, 2, 2)
T.ptp(axis=0)     # [[6, 4], [3, 3]]  → (max − min) entre las dos láminas
T.ptp(axis=(1, 2))  # [7, 3]          → amplitud de cada lámina
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado absurdo con `uint` | overflow de la resta `max − min` | convertir a `int`/`float` antes |
| Resultado `NaN` | hay `NaN` (se propaga; no hay `nanptp`) | filtrar/enmascarar los NaN antes |
| Broadcasting falla tras reducir | se perdió el eje reducido | `keepdims=True` |
| Sentido de `axis` invertido | confundir "rango de filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |
| Muy sensible a un outlier | el rango depende **solo** de los dos extremos | considerar percentiles ([[np.percentile]]) |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[concepto_broadcasting]] — `keepdims` para reinsertar el resultado
- [[np.max]] · [[np.min]] · [[np.percentile]]
