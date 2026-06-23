---
title: np.percentile — Percentil q (0-100) a lo largo de un eje
aliases:
  - percentile
  - np.percentile
  - percentil
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.percentile — Percentil q (0-100) a lo largo de un eje

`np.percentile` calcula el **percentil `q`** de los datos: el valor por debajo del cual cae el `q`%
de las observaciones. Es una **reducción** como [[np.mean]] —recorre un eje, lo **colapsa** y
devuelve un resumen—, pero en vez de promediar ordena los datos y se queda con el valor de la
posición `q`. El percentil 50 es la [[np.median|mediana]], el 25 y el 75 son los cuartiles. La
pregunta clave sigue siendo **"¿qué eje desaparece?"**, con un giro: `q` puede ser una lista, y
entonces **antepone** un eje nuevo a la salida.

## La idea en una fórmula

Ordenados los $n$ datos, el percentil `q` apunta a la posición fraccionaria
$h=(n-1)\cdot q/100$ dentro del orden. Si `h` cae **entre** dos datos, se **interpola** (por defecto
linealmente) entre el de abajo $x_{\lfloor h\rfloor}$ y el de arriba $x_{\lceil h\rceil}$:

$$
P_q = x_{\lfloor h\rfloor} + (h-\lfloor h\rfloor)\,\bigl(x_{\lceil h\rceil}-x_{\lfloor h\rfloor}\bigr)
\qquad h=(n-1)\frac{q}{100}
$$

**Mapa de shapes** — con `q` escalar, el eje reducido $p$ **desaparece** (idéntico a [[np.mean]]):

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{percentile, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

**Con `q` lista** de longitud $Q$, se **antepone** un eje de tamaño $Q$ a ese resultado:

$$
(n_0,\dots,n_k)\ \xrightarrow{\ q=[\,q_0,\dots,q_{Q-1}\,],\ \text{axis}=p\ }\ (Q,\ n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

El eje de los percentiles va **primero**, de modo que `resultado[0]` es el array del primer `q`.

## Firma

```python
np.percentile(
    a,                 # array_like: los datos
    q,                 # float | array_like: percentil(es) en [0, 100]
    axis=None,         # None | int | tuple[int]: eje(s) a reducir; None aplana
    out=None,          # ndarray: destino preasignado con el shape de salida
    overwrite_input=False,  # bool: permitir reordenar 'a' in-place (ahorra memoria)
    method='linear',   # str: regla de interpolación entre datos contiguos
    keepdims=False,    # bool: conservar el eje reducido con tamaño 1
    *,
    weights=None,      # array_like: pesos por dato (solo method='inverted_cdf')
    interpolation=None,  # DEPRECADO: alias antiguo de 'method'
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — los datos
`array_like`. El tensor de entrada. Se ordena internamente (de ahí el coste $O(n\log n)$ por eje).

### `q` — el/los percentil(es)
`float` o `array_like` en `[0, 100]`. Escalar → un valor; **lista → un array** con un eje extra al
principio. `q=0` es el mínimo, `q=100` el máximo, `q=50` la mediana:

| `q` | Significado |
|-----|-------------|
| `0` | mínimo |
| `25` | primer cuartil (Q1) |
| `50` | mediana |
| `75` | tercer cuartil (Q3) |
| `100` | máximo |

```python
datos = np.arange(1, 101)        # 1..100
np.percentile(datos, 50)         # 50.5             escalar
np.percentile(datos, [25, 75])   # [25.75, 75.25]   array de 2 → eje q antepuesto
```

### `axis` — qué eje se reduce
`None` (defecto) **aplana** y da un único percentil global. Un `int` reduce ese eje; una **tupla**
reduce varios a la vez. Mismo modelo que cualquier reducción (ver [[concepto_axis_parametro]]):

```python
M = np.arange(12).reshape(3, 4)
np.percentile(M, 50, axis=0).shape   # (4,)  → mediana por columna
np.percentile(M, 50, axis=1).shape   # (3,)  → mediana por fila
```

### `out` — buffer de salida
`ndarray` preasignado con el shape **exacto** de salida (incluido el eje de `q` si es lista). Evita
una asignación de memoria.

### `overwrite_input` — reordenar in-place
`bool`. Si `True`, NumPy puede **reordenar `a`** para evitar copiarlo (la ordenación interna se hace
sobre el propio array). Ahorra memoria con arrays grandes, pero **corrompe `a`**; úsalo solo si no
vas a reutilizarlo.

### `method` — regla de interpolación
`str`. Cuando el percentil cae **entre** dos datos, define cómo combinarlos. `'linear'` (defecto)
interpola; las demás eligen un extremo o redondean:

| `method` | Qué hace |
|----------|----------|
| `'linear'` | interpolación lineal entre los dos vecinos (defecto) |
| `'lower'` | el dato inferior |
| `'higher'` | el dato superior |
| `'nearest'` | el más cercano |
| `'midpoint'` | el punto medio de ambos |

(Existen además los métodos "tipo R" `'inverted_cdf'`, `'hazen'`, etc., para estadística formal.)

### `keepdims` — conservar el eje reducido
`bool`. Si `True`, el eje reducido **no desaparece**: queda con tamaño 1, listo para
**broadcastear** contra el array original (ver [[np.mean]] para el patrón de centrado).

### `weights` — pesos por dato
`array_like` (keyword-only). Pondera cada dato; **solo** tiene efecto con `method='inverted_cdf'`.
Para percentiles ponderados.

### `interpolation` — alias deprecado
Nombre antiguo de `method`. Deprecado desde NumPy 1.22; usa `method`.

## El caso N-D

La reducción es mecánica: **el eje de `axis` se elimina** (o queda en tamaño 1 con `keepdims`), y si
`q` es lista se **antepone** su eje. Conviene leerlo como "para cada combinación de los ejes que
sobreviven, calcula el percentil a lo largo del que se reduce":

| `a.shape` | `q` | `axis` | salida | lectura |
|-----------|-----|--------|--------|---------|
| `(n,)` | escalar | `None` | `()` escalar | percentil global |
| `(m, n)` | escalar | `0` | `(n,)` | un percentil por **columna** |
| `(m, n)` | escalar | `1` | `(m,)` | un percentil por **fila** |
| `(m, n)` | `[q0, q1]` | `0` | `(2, n)` | el eje de `q` va **primero** |
| `(b, m, n)` | escalar | `(1, 2)` | `(b,)` | percentil por lámina del lote |
| `(m, n)` | escalar | `1` | `(m, 1)` con `keepdims` | broadcasteable contra `a` |

```python
T = np.arange(24).reshape(2, 3, 4)
np.percentile(T, 50, axis=-1).shape      # (2, 3)     → colapsa la última dimensión
np.percentile(T, [25, 75], axis=0).shape # (2, 3, 4)  → eje q (2) antepuesto a (3, 4)
```

## Valor de retorno

El **shape** depende de `q`, `axis` y `keepdims`; el **tipo es siempre flotante** (la interpolación
lo fuerza, incluso con entrada entera):

| Entrada | `q` | `axis` | salida (shape) | tipo |
|---------|-----|--------|----------------|------|
| `(n,)` | escalar | `None` | `()` | **escalar** `np.float64` |
| `(m, n)` | escalar | `int` | shape sin ese eje | `ndarray` float |
| `(m, n)` | lista de `Q` | `int` | `(Q, ...)` con el eje sin reducir | `ndarray` float |
| cualquiera | cualquiera | con `keepdims` | esos ejes en tamaño 1 | `ndarray` float |

```python
np.percentile(np.arange(1, 101), 50)         # np.float64(50.5)  escalar
type(np.percentile(np.arange(12).reshape(3,4), 50, axis=0))  # numpy.ndarray
```

## Casos de uso

### Mediana = percentil 50
```python
datos = np.array([1., 2., 3., 4., 100.])
np.percentile(datos, 50)   # 3.0   → robusta al outlier (la media sería 22)
np.median(datos)           # 3.0   → equivalente
```

### Rango intercuartílico (IQR)
```python
q1, q3 = np.percentile(datos, [25, 75])   # array de 2: eje q antepuesto
iqr = q3 - q1
```

### Recortar outliers por percentiles
```python
lo, hi = np.percentile(datos, [1, 99])
recortado = np.clip(datos, lo, hi)
```

### N-D trabajado: percentil por columna
```python
M = np.array([[ 1.,  2.,  3.],
              [ 4.,  5.,  6.],
              [ 7.,  8.,  9.],
              [10., 11., 12.]])   # (4, 3): 4 muestras, 3 features
np.percentile(M, 50, axis=0)   # [5.5, 6.5, 7.5]  → mediana de cada feature
np.percentile(M, [25, 75], axis=0)
# [[3.25, 4.25, 5.25],   ← Q1 de cada columna
#  [7.75, 8.75, 9.75]]   ← Q3 de cada columna; shape (2, 3)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores absurdos / fuera de rango | se pasó `q` en `[0, 1]` en vez de `[0, 100]` | multiplicar por 100, o usar [[np.quantile]] (escala `[0, 1]`) |
| Resultado `NaN` | el array contiene `NaN` (se propaga) | [[np.median|np.nanpercentile]] |
| `a` quedó modificado | `overwrite_input=True` reordenó el array | no lo actives si reutilizas `a` |
| Eje de la salida en posición inesperada | `q` lista antepone un eje nuevo | el eje de `q` va **primero**; cuéntalo en el shape |
| `weights` ignorado | solo aplica con `method='inverted_cdf'` | fijar ese `method` |

## Notas relacionadas

- [[np.quantile]] — idéntica función con `q` en `[0, 1]` en lugar de `[0, 100]` (la API moderna)
- [[np.median]] — el caso particular `q=50`
- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[np.histogram]] · [[np.digitize]] · [[np.mean]]
