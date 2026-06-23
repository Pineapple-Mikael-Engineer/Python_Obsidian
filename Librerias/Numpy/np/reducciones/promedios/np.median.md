---
title: np.median — Mediana (valor central)
aliases:
  - median
  - np.median
  - mediana
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

# np.median — Mediana (valor central)

`np.median` es una **reducción** que colapsa un eje y devuelve su **valor central**: ordena los
elementos a lo largo del eje y toma el del medio. Con un número **par** de elementos no hay uno
central, así que promedia los **dos centrales**. A diferencia de [[np.mean|la media]], no la
arrastran los outliers (es **robusta**): un valor extremo no desplaza el centro. Como toda
reducción, la pregunta es **"¿qué eje desaparece?"**.

## La idea en una fórmula

Mediana es el valor en la **posición central** del eje ordenado. Sea $x_{(1)}\le x_{(2)}\le\dots\le x_{(m)}$
los $m$ elementos del eje **ordenados de menor a mayor**:

**Mapa de shapes** — el eje $p$ que se reduce **desaparece** del shape (idéntico a `np.sum`):

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{median, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

**Fórmula por índices** — según la paridad de $m$:

$$
\operatorname{med}(x)=
\begin{cases}
x_{\left(\frac{m+1}{2}\right)} & m \text{ impar} \\[4pt]
\dfrac{x_{\left(\frac{m}{2}\right)}+x_{\left(\frac{m}{2}+1\right)}}{2} & m \text{ par}
\end{cases}
$$

El eje que se ordena y del que se toma el centro es el que se reduce y desaparece (ver
[[concepto_axis_parametro]]). El paréntesis $(\,\cdot\,)$ denota el elemento en esa posición del
**orden**, no del array original.

## Firma

```python
np.median(
    a,                       # array_like: el tensor de entrada
    axis=None,               # None | int | tuple[int]: eje(s) a reducir
    out=None,                # ndarray: destino preasignado
    overwrite_input=False,   # bool: permitir ordenar a in-place (lo destruye)
    keepdims=False,          # bool: conservar los ejes reducidos con tamaño 1
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. El resultado es
flotante (por el promedio del caso par). Es **sensible a `NaN`**: cualquier `NaN` en el eje
contamina su mediana (→ usar [[np.nanmedian]]).

### `axis` — qué eje se reduce
`None` (defecto) aplana y devuelve la mediana de **todos** los elementos (un escalar). Un `int`
reduce ese eje; acepta tupla y ejes negativos (`axis=-1` = último eje):

```python
T = np.ones((2, 3, 4))
np.median(T, axis=None).shape   # ()      → escalar
np.median(T, axis=0).shape      # (3, 4)  → desaparece el eje 0
np.median(T, axis=-1).shape     # (2, 3)  → desaparece el último eje
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype del resultado. Evita una asignación de memoria; debe tener
el shape exacto de salida.

### `overwrite_input` — optimización de memoria
Si `True`, permite a NumPy **ordenar `a` in-place** (lo **destruye**) en vez de trabajar sobre una
copia, ahorrando memoria. Úsalo solo si **no necesitas conservar `a`**:

```python
buf = np.random.rand(1_000_000)
m = np.median(buf, overwrite_input=True)   # rápido y sin copia, pero buf queda revuelto
```

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido queda con tamaño 1 para seguir siendo **broadcasteable** contra `a`
(ver [[concepto_broadcasting]]):

```python
M = np.array([[1., 2., 3.], [4., 5., 6.]])
np.median(M, axis=1, keepdims=True).shape  # (2, 1)  → resta la mediana de cada fila
M - np.median(M, axis=1, keepdims=True)
```

## El eje y el caso N-D

La regla es la de toda reducción: **el eje de `axis` se elimina del shape**; los demás quedan en
orden. Para cada combinación de los ejes que **sobreviven**, NumPy ordena el eje reducido y toma su
centro.

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0`/`None` | `()` escalar | mediana de todo |
| `(m, n)` | `0` | `(n,)` | una mediana por **columna** |
| `(m, n)` | `1` | `(m,)` | una mediana por **fila** |
| `(m, n)` | `None` | `()` | mediana total (aplana) |
| `(b, m, n)` | `0` | `(m, n)` | mediana **a lo largo del lote** |
| `(b, m, n)` | `-1` | `(b, m)` | mediana de la última dimensión |

```python
# Tensor (d0, d1, d2) = (3, 2, 4): 3 láminas de 2x4
T = np.arange(3*2*4).reshape(3, 2, 4)
T.median  # (no existe método; usar la función np.median)
np.median(T, axis=0).shape   # (2, 4)  → mediana de las 3 láminas, celda a celda
np.median(T, axis=-1).shape  # (3, 2)  → mediana de cada fila de 4 elementos
```
Con `keepdims=True`, esos resultados conservan los ejes reducidos en tamaño 1 (`(1, 2, 4)`,
`(3, 2, 1)`), listos para broadcastear contra `T`.

## Vectorización

`np.median` reemplaza el "ordenar y tomar el del medio" escrito a mano, aplicado a cada línea del
eje. Las dos versiones coinciden, pero la vectorizada ordena en C sobre todo el eje:

```python
# Bucle Python (lento, explícito): mediana por fila
def medianas_filas(M):
    out = np.empty(M.shape[0])
    for i, fila in enumerate(M):
        s = np.sort(fila)
        n = len(s)
        out[i] = s[n//2] if n % 2 else (s[n//2 - 1] + s[n//2]) / 2
    return out

# Vectorizado (NumPy ordena el eje 1 en C y toma el centro de golpe):
np.median(M, axis=1)
```
A diferencia de `sum`/`mean`, la mediana **necesita ordenar** (coste ~$O(n\log n)$ por línea), pero
sigue siendo el principio de [[concepto_vectorizacion]]: describes el eje, no el bucle.

## Valor de retorno

El **shape** depende de `axis`/`keepdims`; el **tipo es flotante** (por el promedio del caso par):

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar de NumPy** (float) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` (float) |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` (float) |
| `(n,)` | `0` | `False` | `()` | escalar float |

- enteros → se promueven a `float64` (el caso par puede dar `.5`).
- `float32` → `float32`; si hay algún `NaN` en el eje, la mediana de ese eje es `NaN`.

```python
np.median([1, 2, 3, 4, 5])   # 3.0  (impar: el central)
np.median([1, 2, 3, 4])      # 2.5  (par: promedio de 2 y 3)
np.median([1, 2, 100])       # 2.0  (el outlier no la desplaza)
```

## Casos de uso

### Resumen robusto frente a outliers
```python
salarios = np.array([30, 32, 31, 33, 500])   # un outlier
np.mean(salarios)     # 125.2  engañoso (lo arrastra el 500)
np.median(salarios)   # 32.0   representativo
```

### Caso par vs impar
```python
np.median([10, 20, 30])       # 20.0  → el central
np.median([10, 20, 30, 40])   # 25.0  → (20 + 30) / 2
```

### Mediana por columna
```python
datos = np.random.rand(100, 5)
np.median(datos, axis=0)   # (5,)  → mediana de cada feature
```

### N-D trabajado: mediana por feature de un lote `(b, n)`
```python
lote = np.array([[1.,  2.,  3.],     # muestra 0
                 [3.,  4.,  5.],     # muestra 1
                 [5.,  6.,  7.],     # muestra 2
                 [99., 8.,  9.]])    # muestra 3 (outlier en feature 0)
np.median(lote, axis=0)   # [4., 5., 6.]  → mediana de cada feature sobre las 4 muestras
np.mean(lote, axis=0)     # [27., 5., 6.]  → la media SÍ se va por el 99
# El eje 0 (las muestras) desaparece; en feature 0 el outlier no mueve la mediana.
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado `NaN` | hay `NaN` en el eje (la mediana es sensible) | [[np.nanmedian]] |
| `a` quedó modificado | `overwrite_input=True` reordenó `a` | dejarlo en `False` si necesitas `a` |
| Más lento que `mean` | la mediana requiere ordenar | esperado; usa `mean` si no hay outliers |
| Sentido de `axis` invertido | confundir "mediana de filas" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |
| Quería otro cuantil | la mediana es solo el percentil 50 | `np.percentile` / `np.quantile` |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — ordenar el eje en C en vez de en Python
- [[np.mean]] · [[np.average]] · [[np.nanmedian]] · [[np.std]]
