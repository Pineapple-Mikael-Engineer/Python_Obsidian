---
title: np.var — varianza (dispersión promedio al cuadrado) a lo largo de un eje
aliases:
  - var
  - np.var
  - varianza
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

# np.var — varianza (dispersión promedio al cuadrado) a lo largo de un eje

`np.var` es una **reducción** estadística: recorre un eje, calcula la media de esos elementos y
devuelve el **promedio de las desviaciones al cuadrado** respecto a esa media. Como toda reducción,
el eje recorrido **desaparece** del shape (un `(2, 3)` se convierte en un `(3,)` o en un escalar).
Mide *cuánto se dispersan* los datos alrededor de su centro; está en **unidades al cuadrado** (su
raíz es la [[np.std|desviación típica]], en las unidades originales). La pregunta de siempre al
usarla no es "¿varianza?" sino **"¿qué eje desaparece y con qué divisor (`ddof`)?"**.

## La idea en una fórmula

Como en cualquier reducción, el eje reducido se elimina del shape (ver [[concepto_axis_parametro]]).
Para una matriz $A$ de shape $(m, n)$, reducir sobre el eje `0` produce un vector indexado por la
columna $j$, y reducir sobre el eje `1` uno indexado por la fila $i$:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{var, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

La varianza de un conjunto de $N$ valores $x_i$ con media $\bar{x}$ es el promedio de las
desviaciones al cuadrado, donde el divisor lo controla `ddof`:

$$ \sigma^2 = \frac{1}{N-\text{ddof}}\sum_{i}(x_i-\bar{x})^2 \qquad \bar{x}=\frac{1}{N}\sum_i x_i $$

Con `ddof=0` (defecto) el divisor es $N$ (varianza **poblacional**); con `ddof=1` es $N-1$
(varianza **muestral** insesgada). El eje del sumatorio es el que se contrae.

## Firma

```python
np.var(
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
cálculo se promociona a `float64` (la varianza casi nunca es entera).

### `axis` — qué eje se reduce
El parámetro central. `None` (defecto) usa **todos** los elementos y devuelve un escalar. Un `int`
reduce ese eje; una **tupla** reduce varios a la vez:

```python
T = np.ones((2, 3, 4))
np.var(T, axis=None).shape    # ()      → escalar, se reducen los 3 ejes
np.var(T, axis=0).shape       # (3, 4)  → desaparece el eje 0
np.var(T, axis=1).shape       # (2, 4)  → desaparece el eje 1
np.var(T, axis=(0, 2)).shape  # (3,)    → desaparecen los ejes 0 y 2
```
Acepta ejes negativos (`axis=-1` = último eje).

### `ddof` — delta degrees of freedom (el parámetro que más confunde)
Es lo que distingue varianza **poblacional** de **muestral**. El divisor del promedio **no** es
siempre $N$, sino $N-\text{ddof}$:

| `ddof` | Divisor | Significado |
|--------|---------|-------------|
| `0` (defecto) | $N$ | varianza **poblacional**: describes los datos que tienes, son *toda* la población |
| `1` | $N-1$ | varianza **muestral** insesgada: estimas la varianza de una población **a partir de una muestra** (corrección de Bessel) |

La intuición de por qué `ddof=1` divide por $N-1$: al calcular $\bar{x}$ *desde los propios datos*,
las desviaciones tienden a ser un poco más pequeñas de lo que serían respecto a la media real de la
población; dividir por $N-1$ en vez de $N$ **compensa** ese sesgo a la baja.

```python
datos = np.array([2.0, 4.0, 6.0])      # N = 3, media = 4
np.var(datos)            # 2.667  → ddof=0: (4+0+4)/3   (poblacional)
np.var(datos, ddof=1)    # 4.0    → ddof=1: (4+0+4)/2   (muestral)
```
Regla práctica: si los datos **son** toda la población, `ddof=0`; si son una **muestra** de algo
mayor (lo habitual en estadística), `ddof=1`. La mayoría de paquetes estadísticos usan `ddof=1` por
defecto, por eso NumPy "discrepa" si no lo fijas.

> [!warning] `ddof >= N` rompe el cálculo
> Si `ddof` iguala o supera el número de elementos reducidos, el divisor $N-\text{ddof}$ es $\le 0$:
> sale `NaN` (división por cero) o un negativo sin sentido, con un *RuntimeWarning*.

### `dtype` — tipo del acumulador y del resultado
Fija el tipo en el que se acumulan las sumas intermedias. Con datos `float16` o enteros, forzar
`np.float64` evita pérdida de precisión en la media y en las desviaciones (ver [[concepto_dtype]]).

```python
chico = np.array([1, 2, 3, 4], dtype=np.float16)
np.var(chico)                  # precisión limitada de float16
np.var(chico, dtype=np.float64)  # acumulación más precisa
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype exactos del resultado. Evita una asignación de memoria;
útil en bucles.

### `keepdims` — conservar el eje reducido como tamaño 1
Si `True`, el eje reducido **no desaparece**: queda con tamaño 1, de modo que el resultado siga
siendo **broadcasteable** contra el array original (ver [[concepto_broadcasting]]).

```python
M = np.array([[1., 2.], [3., 10.]])
M.var(axis=1).shape              # (2,)    → no broadcastea de vuelta a (2,2)
M.var(axis=1, keepdims=True).shape  # (2, 1)  → sí broadcastea
```

### `where` — cálculo condicional (máscara)
`array_like` booleano broadcasteable con `a`. Solo los elementos donde `where` es `True` entran en
la media y en la varianza; el resto se ignora sin crear el array filtrado.

```python
arr = np.array([1., 2., 3., 1000.])
np.var(arr, where=arr < 100)   # varianza solo de [1, 2, 3], ignora el outlier
```

## El eje y el caso N-D

La regla es mecánica: **el eje (o ejes) de `axis` se elimina del shape**; los demás quedan en orden.
Léelo como "para cada combinación de los ejes que **sobreviven**, calculo la varianza a lo largo del
que se reduce".

| `a.shape` | `axis` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `0` o `None` | `()` escalar | varianza de todo |
| `(m, n)` | `0` | `(n,)` | una varianza por **columna** (feature) |
| `(m, n)` | `1` | `(m,)` | una varianza por **fila** |
| `(m, n)` | `None` | `()` | varianza global |
| `(b, m, n)` | `0` | `(m, n)` | varianza **a lo largo del lote**, por posición |
| `(b, m, n)` | `(1, 2)` | `(b,)` | una varianza por cada matriz del lote |
| `(b, m, n)` | `-1` | `(b, m)` | varianza a lo largo de la última dimensión |

```python
# Lote de 4 muestras, cada una un vector de 3 features:  (4, 3)
X = np.array([[1.,  10.,  100.],
              [2.,  10.,  200.],
              [3.,  10.,  300.],
              [4.,  10.,  400.]])
X.var(axis=0)              # [1.25, 0., 12500.]  → varianza por feature; la 2ª es constante
X.var(axis=0, ddof=1)      # [1.667, 0., 16666.7] → versión muestral (divide por 3)

# Tensor (lote de 5 imágenes RGB 2x2):  (5, 2, 2, 3)
imgs = np.random.rand(5, 2, 2, 3)
imgs.var(axis=(1, 2)).shape   # (5, 3)  → varianza espacial: un vector RGB por imagen
imgs.var(axis=0).shape        # (2, 2, 3) → varianza por píxel sobre el lote
```

## Vectorización

`np.var` reemplaza el bucle de "media, restar, elevar al cuadrado, promediar" escrito a mano. Ambas
versiones dan lo mismo, pero la vectorizada corre en C sobre memoria contigua:

```python
# Bucle Python (lento, explícito):
def var_manual(x, ddof=0):
    n = len(x)
    media = sum(x) / n
    return sum((xi - media) ** 2 for xi in x) / (n - ddof)

# Vectorizado (NumPy recorre el eje en C):
np.var(x, ddof=0)
```
NumPy describe *qué* eje reducir, no *cómo* iterar: ese es el principio de
[[concepto_vectorizacion]]. Por eso `axis` es el lenguaje natural —pides la varianza sobre una
dimensión entera de golpe—.

## Valor de retorno

El tipo del retorno **depende de `axis`**; el `dtype` es flotante salvo que fuerces otro:

| Entrada | `axis` | `keepdims` | salida (shape) | tipo |
|---------|--------|------------|----------------|------|
| `(m, n)` | `None` | `False` | `()` | **escalar de NumPy** (`np.float64`) |
| `(m, n)` | `int`/`tuple` | `False` | shape sin esos ejes | `ndarray` |
| `(m, n)` | cualquiera | `True` | esos ejes en tamaño 1 | `ndarray` |
| `(n,)` | `0` | `False` | `()` | escalar |

Reglas de `dtype` de salida (sin `dtype=` explícito):
- enteros → se promocionan a `float64` (la varianza no suele ser entera).
- `float32` conserva `float32`; `float16` conserva `float16` (de ahí el riesgo de precisión).

```python
np.var([1, 2, 3])              # np.float64(0.667)   escalar, no ndarray
type(np.ones((2, 2)).var(axis=0))   # numpy.ndarray
np.var(np.ones((2, 2)).astype(np.float32)).dtype   # float32
```

## Casos de uso

### Variabilidad por feature y la más variable
```python
matriz = np.array([[1., 5.,  2.],
                   [2., 5., 20.],
                   [3., 5., 60.]])
varianzas = np.var(matriz, axis=0)   # [0.667, 0., 600.4]
mas_variable = np.argmax(varianzas)  # 2  → la 3ª columna es la que más dispersa
```

### Detectar columnas constantes (varianza 0)
```python
constantes = np.var(matriz, axis=0) == 0   # [False, True, False]
```

### Muestral vs poblacional
```python
muestra = np.array([4., 8., 6., 5., 3., 7.])
np.var(muestra)          # poblacional (÷N)
np.var(muestra, ddof=1)  # muestral insesgada (÷N-1), la convención estadística
```

### Reducción parcial de un tensor N-D
```python
batch = np.random.rand(32, 10)     # 32 muestras, 10 features
batch.var(axis=0).shape            # (10,)  → varianza por feature sobre el lote
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valor distinto al de otra librería (R, pandas, Excel) | `ddof` por defecto es 0 (poblacional) | usar `ddof=1` para muestral |
| `NaN` / *RuntimeWarning* de división | `ddof >= N` en el eje reducido | reducir `ddof` o revisar el tamaño del eje |
| Magnitud "rara", demasiado grande | está al **cuadrado** | usar [[np.std]] para las unidades originales |
| `NaN` en el resultado | el array contiene `NaN` (se propaga) | usar [[np.nanvar]] |
| Broadcasting falla tras reducir | se perdió el eje reducido | `keepdims=True` |
| Sentido de `axis` invertido | confundir "por fila" con "sobre el eje 0" | el eje de `axis` **desaparece**; mira el shape de salida |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué significa reducir un eje
- [[concepto_vectorizacion]] — por qué `axis` sustituye al bucle
- [[concepto_dtype]] — precisión del acumulador
- [[np.std]] · [[np.mean]] · [[np.average]] · [[np.nanvar]]
