---
title: np.quantile — Cuantil q (0-1) a lo largo de un eje
aliases:
  - quantile
  - np.quantile
  - cuantil
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

# np.quantile — Cuantil q (0-1) a lo largo de un eje

`np.quantile` es la versión **moderna** de [[np.percentile]]: hace exactamente lo mismo —reduce un
eje y devuelve el valor por debajo del cual cae una fracción `q` de los datos— pero con `q` expresado
en **`[0, 1]`** en lugar de `[0, 100]`. El cuantil `0.5` es la [[np.median|mediana]], `0.25` y `0.75`
son los cuartiles. Es la API que NumPy recomienda hoy; la escala `[0, 1]` es la convención
estadística estándar y evita confusiones. Como toda reducción, la pregunta clave es **"¿qué eje
desaparece?"** (ver [[concepto_axis_parametro]]).

## La idea en una fórmula

Es `percentile` con la escala cambiada: `quantile(a, q) == percentile(a, 100*q)`. Ordenados los $n$
datos, el cuantil `q` apunta a la posición fraccionaria $h=(n-1)\cdot q$ del orden; si cae **entre**
dos datos se **interpola** (linealmente por defecto):

$$
Q_q = x_{\lfloor h\rfloor} + (h-\lfloor h\rfloor)\,\bigl(x_{\lceil h\rceil}-x_{\lfloor h\rfloor}\bigr)
\qquad h=(n-1)\,q,\quad q\in[0,\ 1]
$$

**Mapa de shapes** — con `q` escalar, el eje reducido $p$ **desaparece**:

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{quantile, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

**Con `q` lista** de longitud $Q$, se **antepone** un eje de tamaño $Q$:

$$
(n_0,\dots,n_k)\ \xrightarrow{\ q=[\,q_0,\dots,q_{Q-1}\,],\ \text{axis}=p\ }\ (Q,\ n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

## Firma

```python
np.quantile(
    a,                 # array_like: los datos
    q,                 # float | array_like: cuantil(es) en [0, 1]
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

La firma es **idéntica** a la de [[np.percentile]]; lo único que cambia es el dominio de `q`.

## Los parámetros en detalle

### `a` — los datos
`array_like`. El tensor de entrada; se ordena internamente.

### `q` — el/los cuantil(es)
`float` o `array_like` en **`[0, 1]`** (¡no `[0, 100]`!). Escalar → un valor; **lista → un array**
con un eje extra al principio:

| `q` | Equivale a percentil | Significado |
|-----|----------------------|-------------|
| `0.0` | `0` | mínimo |
| `0.25` | `25` | primer cuartil (Q1) |
| `0.5` | `50` | mediana |
| `0.75` | `75` | tercer cuartil (Q3) |
| `1.0` | `100` | máximo |

```python
datos = np.arange(1, 101)          # 1..100
np.quantile(datos, 0.5)            # 50.5             escalar
np.quantile(datos, [0.25, 0.75])   # [25.75, 75.25]   array de 2 → eje q antepuesto
```

### `axis` — qué eje se reduce
`None` (defecto) aplana y da un cuantil global. Un `int` reduce ese eje; una **tupla** reduce varios.
Mismo modelo de reducción que [[concepto_axis_parametro]].

### `out` — buffer de salida
`ndarray` preasignado con el shape exacto de salida (incluido el eje de `q` si es lista).

### `overwrite_input` — reordenar in-place
`bool`. Si `True`, NumPy puede **reordenar `a`** para no copiarlo: ahorra memoria pero **corrompe
`a`**. Úsalo solo si no vas a reutilizarlo.

### `method` — regla de interpolación
`str`. Cuando el cuantil cae entre dos datos, define cómo combinarlos:

| `method` | Qué hace |
|----------|----------|
| `'linear'` | interpolación lineal entre los dos vecinos (defecto) |
| `'lower'` | el dato inferior |
| `'higher'` | el dato superior |
| `'nearest'` | el más cercano |
| `'midpoint'` | el punto medio de ambos |

(Más los métodos "tipo R": `'inverted_cdf'`, `'hazen'`, `'weibull'`, etc.)

### `keepdims` — conservar el eje reducido
`bool`. Si `True`, el eje reducido queda con tamaño 1, listo para **broadcastear** contra `a`.

### `weights` — pesos por dato
`array_like` (keyword-only). Pondera cada dato; **solo** con `method='inverted_cdf'`.

### `interpolation` — alias deprecado
Nombre antiguo de `method`. Deprecado desde NumPy 1.22.

## El caso N-D

Mecánico e idéntico a [[np.percentile]]: **el eje de `axis` se elimina** (o queda en tamaño 1 con
`keepdims`), y si `q` es lista se **antepone** su eje:

| `a.shape` | `q` | `axis` | salida | lectura |
|-----------|-----|--------|--------|---------|
| `(n,)` | escalar | `None` | `()` escalar | cuantil global |
| `(m, n)` | escalar | `0` | `(n,)` | un cuantil por **columna** |
| `(m, n)` | escalar | `1` | `(m,)` | un cuantil por **fila** |
| `(m, n)` | `[q0, q1]` | `0` | `(2, n)` | el eje de `q` va **primero** |
| `(b, m, n)` | escalar | `(1, 2)` | `(b,)` | cuantil por lámina del lote |

```python
T = np.arange(24).reshape(2, 3, 4)
np.quantile(T, 0.5, axis=-1).shape       # (2, 3)     → colapsa la última dimensión
np.quantile(T, [0.25, 0.75], axis=0).shape  # (2, 3, 4)  → eje q (2) antepuesto a (3, 4)
```

## Valor de retorno

El **shape** depende de `q`, `axis` y `keepdims`; el **tipo es siempre flotante**:

| Entrada | `q` | `axis` | salida (shape) | tipo |
|---------|-----|--------|----------------|------|
| `(n,)` | escalar | `None` | `()` | **escalar** `np.float64` |
| `(m, n)` | escalar | `int` | shape sin ese eje | `ndarray` float |
| `(m, n)` | lista de `Q` | `int` | `(Q, ...)` con el eje sin reducir | `ndarray` float |
| cualquiera | cualquiera | con `keepdims` | esos ejes en tamaño 1 | `ndarray` float |

```python
np.quantile(np.arange(1, 101), 0.5)   # np.float64(50.5)  escalar
type(np.quantile(np.arange(12).reshape(3,4), 0.5, axis=0))  # numpy.ndarray
```

## Casos de uso

### Mediana = cuantil 0.5
```python
datos = np.array([1., 2., 3., 4., 100.])
np.quantile(datos, 0.5)    # 3.0   → robusta al outlier
np.median(datos)           # 3.0   → equivalente
```

### Rango intercuartílico (IQR)
```python
q1, q3 = np.quantile(datos, [0.25, 0.75])
iqr = q3 - q1
```

### Recortar outliers por cuantiles
```python
lo, hi = np.quantile(datos, [0.01, 0.99])
recortado = np.clip(datos, lo, hi)
```

### N-D trabajado: cuantil por columna
```python
M = np.array([[ 1.,  2.,  3.],
              [ 4.,  5.,  6.],
              [ 7.,  8.,  9.],
              [10., 11., 12.]])   # (4, 3): 4 muestras, 3 features
np.quantile(M, 0.5, axis=0)    # [5.5, 6.5, 7.5]  → mediana de cada feature
np.quantile(M, [0.25, 0.75], axis=0)
# [[3.25, 4.25, 5.25],   ← Q1 de cada columna
#  [7.75, 8.75, 9.75]]   ← Q3 de cada columna; shape (2, 3)
```

### Equivalencia con percentile
```python
np.quantile(datos, 0.9) == np.percentile(datos, 90)   # True (salvo épsilon)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: quantiles must be in [0, 1]` | se pasó `q` en escala `[0, 100]` (hábito de `percentile`) | dividir entre 100, o usar [[np.percentile]] |
| Resultado `NaN` | el array contiene `NaN` (se propaga) | `np.nanquantile` |
| `a` quedó modificado | `overwrite_input=True` reordenó el array | no lo actives si reutilizas `a` |
| Eje de la salida en posición inesperada | `q` lista antepone un eje nuevo | el eje de `q` va **primero** |
| `weights` ignorado | solo aplica con `method='inverted_cdf'` | fijar ese `method` |

## Notas relacionadas

- [[np.percentile]] — la misma función con `q` en `[0, 100]` (API histórica, ojo a la escala)
- [[np.median]] — el caso particular `q=0.5`
- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[np.histogram]] · [[np.digitize]] · [[np.mean]]
