---
title: np.std — desviación típica (dispersión en las unidades originales) a lo largo de un eje
aliases:
  - std
  - np.std
  - desviacion estandar
  - desviacion tipica
tags:
  - numpy
  - api/funcion
  - estadistica

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
  - concepto_dtype

draft: false
---

# np.std — desviación típica (dispersión en las unidades originales) a lo largo de un eje

`np.std` es una **reducción** estadística: recorre un eje y devuelve la **raíz cuadrada de la
[[np.var|varianza]]**, es decir, una medida de cuánto se dispersan los datos alrededor de su
[[np.mean|media]], pero expresada en las **mismas unidades** que los datos (no al cuadrado). Como
toda reducción, el eje recorrido **desaparece** del shape (un `(2, 3)` pasa a `(3,)` o a escalar).
Es la varianza "legible": si los datos son metros, la desviación típica también está en metros. La
pregunta de siempre al usarla no es "¿desviación?" sino **"¿qué eje desaparece y con qué divisor
(`ddof`)?"**.

## La idea en una fórmula

Como toda reducción, el eje reducido se elimina del shape (ver [[concepto_axis_parametro]]); el mapa
de shapes es idéntico al de [[np.var]] —solo cambia que al final se toma la raíz:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{std, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

La desviación típica de $N$ valores $x_i$ con media $\bar{x}$ es la raíz de la varianza, con el
divisor controlado por `ddof`:

$$ \sigma = \sqrt{\frac{1}{N-\text{ddof}}\sum_i (x_i-\bar{x})^2} \qquad \bar{x}=\frac{1}{N}\sum_i x_i $$

Es exactamente $\sqrt{\sigma^2}$: la relación con [[np.var]] es directa,
`np.std(a, ddof=k) == np.sqrt(np.var(a, ddof=k))`. Con `ddof=0` (defecto) el divisor es $N$
(poblacional); con `ddof=1` es $N-1$ (muestral). El eje del sumatorio es el que se contrae.

## Firma

```python
np.std(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    dtype=None,        # dtype: tipo del acumulador y del resultado
    out=None,          # ndarray: destino preasignado
    ddof=0,            # int: delta degrees of freedom (divisor = N - ddof)
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
    where=True,        # array_like[bool]: qué elementos entran en el cálculo
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Si es entero, el
cálculo se promociona a `float64`.

### `axis` — qué eje se reduce
El parámetro central. `None` (defecto) usa **todos** los elementos y devuelve un escalar. Un `int`
reduce ese eje; una **tupla** reduce varios a la vez:

```python
T = np.ones((2, 3, 4))
np.std(T, axis=None).shape    # ()      → escalar, se reducen los 3 ejes
np.std(T, axis=0).shape       # (3, 4)  → desaparece el eje 0
np.std(T, axis=1).shape       # (2, 4)  → desaparece el eje 1
np.std(T, axis=(0, 2)).shape  # (3,)    → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje).

### `ddof` — delta degrees of freedom (el parámetro que más confunde)
Idéntico a [[np.var]]: distingue desviación **poblacional** de **muestral** cambiando el divisor de
la varianza interna, que es $N-\text{ddof}$:

| `ddof` | Divisor | Significado |
|--------|---------|-------------|
| `0` (defecto) | $N$ | desviación **poblacional**: los datos son *toda* la población |
| `1` | $N-1$ | desviación **muestral** insesgada: estimas la dispersión de una población **a partir de una muestra** (corrección de Bessel) |

La intuición: al calcular $\bar{x}$ desde los propios datos, las desviaciones salen algo más
pequeñas de lo que serían respecto a la media real; dividir por $N-1$ **compensa** ese sesgo a la
baja antes de tomar la raíz.

```python
datos = np.array([2.0, 4.0, 6.0])      # N = 3, media = 4
np.std(datos)            # 1.633  → ddof=0 (poblacional),  sqrt(2.667)
np.std(datos, ddof=1)    # 2.0    → ddof=1 (muestral),     sqrt(4.0)
```
Regla práctica: si los datos **son** la población completa, `ddof=0`; si son una **muestra**,
`ddof=1` (la convención estadística por defecto en R, pandas con `.std()`, etc.).

> [!warning] `ddof >= N` rompe el cálculo
> Si `ddof` iguala o supera el número de elementos reducidos, el divisor $N-\text{ddof}$ es $\le 0$:
> sale `NaN` (la raíz de un negativo / división por cero), con un *RuntimeWarning*.

### `dtype` — tipo del acumulador y del resultado
Fija el tipo de las sumas intermedias. Con datos `float16` o enteros, forzar `np.float64` evita
pérdida de precisión en la media y en las desviaciones (ver [[concepto_dtype]]).

```python
chico = np.array([1, 2, 3, 4], dtype=np.float16)
np.std(chico, dtype=np.float64)   # acumulación más precisa que en float16
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype exactos del resultado. Evita una asignación de memoria;
útil en bucles.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1, de modo que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]). Es justo lo que
hace falta para estandarizar (z-score) por columnas.

```python
M = np.array([[1., 2.], [3., 10.]])
M.std(axis=1).shape              # (2,)    → no broadcastea de vuelta a (2,2)
M.std(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
```

### `where` — cálculo condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo los elementos donde `where` es `True` entran en
el cálculo; el resto se ignora sin crear el array filtrado.

```python
arr = np.array([1., 2., 3., 1000.])
np.std(arr, where=arr < 100)   # desviación solo de [1, 2, 3], ignora el outlier
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Léelo como "para cada combinación de los ejes que **sobreviven**, calculo la desviación a lo largo
del que se reduce".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar | desviación de todo |
| `(m, n)` | `0` | `(n,)` | una desviación por **columna** (feature) |
| `(m, n)` | `1` | `(m,)` | una desviación por **fila** |
| `(m, n)` | `None` | `()` | desviación global |
| `(b, m, n)` | `0` | `(m, n)` | desviación **a lo largo del lote**, por posición |
| `(b, m, n)` | `(1, 2)` | `(b,)` | una desviación por cada matriz del lote |
| `(b, m, n)` | `-1` | `(b, m)` | desviación a lo largo de la última dimensión |

```python
# Lote de 4 muestras, cada una un vector de 3 features:  (4, 3)
X = np.array([[1.,  10.,  100.],
              [2.,  10.,  200.],
              [3.,  10.,  300.],
              [4.,  10.,  400.]])
X.std(axis=0)              # [1.118, 0., 111.8]  → desviación por feature; la 2ª es constante
X.std(axis=0, ddof=1)      # [1.291, 0., 129.1]  → versión muestral (divide por 3)

# Tensor (lote de 5 imágenes RGB 2x2):  (5, 2, 2, 3)
imgs = np.random.rand(5, 2, 2, 3)
imgs.std(axis=(1, 2)).shape   # (5, 3)  → desviación espacial: un vector RGB por imagen
imgs.std(axis=0).shape        # (2, 2, 3) → desviación por píxel sobre el lote
```

## Vectorización

`np.std` reemplaza el bucle de "media, restar, elevar al cuadrado, promediar, raíz" escrito a mano.
Ambas versiones dan lo mismo, pero la vectorizada corre en C sobre memoria contigua:

```python
# Bucle Python (lento, explícito):
def std_manual(x, ddof=0):
    n = len(x)
    media = sum(x) / n
    return (sum((xi - media) ** 2 for xi in x) / (n - ddof)) ** 0.5

# Vectorizado (NumPy recorre el eje en C):
np.std(x, ddof=0)
```
NumPy describe *qué* eje reducir, no *cómo* iterar: el principio de [[concepto_vectorizacion]]. Por
eso `axis` es el lenguaje natural —pides la desviación sobre una dimensión entera de golpe—.

## Valor de retorno

El tipo del retorno **depende de `axis`**; el `dtype` es flotante salvo que fuerces otro:

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar de NumPy** (`np.float64`) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` |
| `(n,)` | `0` | `False` | `()` | escalar |

Reglas de `dtype` de salida (sin `dtype=` explícito):
- enteros → se promocionan a `float64`.
- `float32` conserva `float32`; `float16` conserva `float16`.

```python
np.std([2, 4, 4, 4, 5, 5, 7, 9])    # np.float64(2.0)   escalar, no ndarray
np.std([5, 5, 5, 5])                # 0.0  → sin dispersión
type(np.ones((2, 2)).std(axis=0))   # numpy.ndarray
```

## Casos de uso

### Estandarizar datos (z-score) por columna
El uso por excelencia: centrar y escalar cada feature. `keepdims=True` mantiene el broadcasting.

```python
datos = np.array([[1., 100.],
                  [2., 200.],
                  [3., 300.]])
mu = np.mean(datos, axis=0, keepdims=True)   # (1, 2)
sd = np.std(datos,  axis=0, keepdims=True)   # (1, 2)
z = (datos - mu) / sd     # cada columna queda con media 0 y desviación 1
```

### Dispersión por feature
```python
desviaciones = np.std(matriz, axis=0)   # una desviación por columna
```

### Muestral vs poblacional
```python
muestra = np.array([4., 8., 6., 5., 3., 7.])
np.std(muestra)          # poblacional (÷N)
np.std(muestra, ddof=1)  # muestral insesgada (÷N-1), la convención estadística
```

### Reducción parcial de un tensor N-D
```python
batch = np.random.rand(32, 10)     # 32 muestras, 10 features
batch.std(axis=0).shape            # (10,)  → desviación por feature sobre el lote
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor distinto al de otra librería (R, pandas, Excel) | `ddof` por defecto es 0 (poblacional) | usar `ddof=1` para muestral |
| `NaN` / *RuntimeWarning* de división | `ddof >= N` en el eje reducido | reducir `ddof` o revisar el tamaño del eje |
| División por cero al estandarizar | la desviación es 0 (columna constante) | manejar ese caso aparte (p. ej. dejar la columna sin escalar) |
| `NaN` en el resultado | el array contiene `NaN` (se propaga) | usar [[np.nanstd]] |
| Broadcasting falla en el z-score | se perdió el eje reducido | `keepdims=True` en `mean` y `std` |
| Sentido de `axis` invertido | confundir "por fila" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[concepto_dtype]] — precisión del acumulador
- [[np.var]] · [[np.mean]] · [[np.average]] · [[np.nanstd]]
