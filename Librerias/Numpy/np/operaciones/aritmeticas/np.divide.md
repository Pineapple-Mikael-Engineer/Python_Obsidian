---
title: np.divide — división real elemento a elemento (ufunc)
aliases:
  - divide
  - np.divide
  - true_divide
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
  - concepto_broadcasting
  - concepto_dtype

draft: false
---

# np.divide — división real elemento a elemento (ufunc)

`np.divide` (alias `np.true_divide`) es la [[concepto_ufuncs|ufunc]] binaria que respalda al operador `/`: divide cada elemento de `x1` entre el correspondiente de `x2`, alineando las formas con [[concepto_broadcasting|broadcasting]]. Es una **división real**: aunque las dos entradas sean enteras, el resultado **siempre es flotante** (`5 / 2 == 2.5`, nunca `2`). La pregunta clave al usarla no es "¿divide?" sino **"¿qué pasa donde el divisor es cero?"** — y la respuesta es `inf`/`nan` con aviso, no una excepción.

## La idea en una fórmula

La operación se aplica posición a posición sobre la shape común que resulta del broadcasting de `x1` y `x2`:

$$
z_i = \frac{x_{1,i}}{x_{2,i}} \qquad \text{(elemento a elemento, en } \mathbb{R}\text{)}
$$

y el mapa de shapes es simplemente el del broadcasting de las dos entradas:

$$
(\dots),\ (\dots)\ \xrightarrow{\ \text{broadcast}\ }\ (\max(a_0,b_0),\,\dots,\,\max(a_k,b_k))
$$

El resultado tiene esa shape común y un `dtype` **flotante** (ver `dtype` más abajo). Donde $x_{2,i}=0$, la división no aborta: produce $\pm\infty$ (numerador no nulo) o `nan` (`0/0`).

## Firma

```python
np.divide(
    x1,              # array_like: dividendo (numerador)
    x2,              # array_like: divisor (denominador)
    /,
    out=None,        # ndarray | None: destino preasignado
    *,
    where=True,      # array_like[bool]: dónde calcular
    dtype=None,      # dtype: tipo de cómputo/salida
    casting='same_kind',  # política de conversión
    order='K',       # disposición en memoria de la salida
) -> ndarray
```

## Los parámetros en detalle

### `x1` — dividendo (numerador)
`array_like` (ndarray, lista, escalar). Es la cantidad que se reparte. Se broadcastea contra `x2`.

### `x2` — divisor (denominador)
`array_like` broadcasteable con `x1`. **El parámetro con trampa**: donde valga `0`, NumPy no lanza excepción, sino que emite un `RuntimeWarning` y rellena con `inf` (si el numerador es no nulo) o `nan` (si es `0/0`).

```python
np.divide([1., 0., 3.], [0., 0., 1.])   # RuntimeWarning
# array([inf, nan,  3.])
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida. Evita una asignación de memoria. Combinado con `where`, es la base de la **división segura** (ver abajo): las posiciones no calculadas conservan el valor que ya tuviera `out`.

### `where` — división condicional (máscara)
`array_like` booleano broadcasteable con las entradas. Solo se calcula donde es `True`; donde es `False`, el resultado **conserva lo que hubiera en `out`**. Es el modo idiomático de dividir solo donde el divisor no es cero, sin warning ni `inf`:

```python
a = np.array([1., 2., 3.])
b = np.array([0., 2., 0.])
np.divide(a, b, out=np.zeros_like(a), where=b != 0)
# array([0., 1., 0.])   → no calcula donde b == 0; deja el 0 del buffer
```

> [!warning] `where` necesita `out`
> Donde `where` es `False` el resultado queda **sin inicializar** si no pasas `out`. Por eso la división segura siempre lleva `out=np.zeros_like(...)` (o un buffer con el valor de relleno deseado).

### `dtype` — tipo de cómputo y salida
Fuerza el tipo del resultado. Aunque las entradas sean enteras, `np.divide` produce `float64` por defecto; con `dtype` puedes pedir `float32` para ahorrar memoria. No permite forzar un entero (la división real no es entera; para eso está `np.floor_divide`).

```python
np.divide(np.array([1, 2, 3]), 2).dtype             # float64 (¡aunque entren ints!)
np.divide(np.array([1, 2, 3]), 2, dtype=np.float32) # float32
```

### `casting` — política de conversión
Controla qué conversiones de tipo se permiten al combinar entradas o escribir en `out`: `'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Importa con `out`: escribir un `float64` en un `out` de `float32` requiere al menos `'same_kind'`.

### `order` — disposición en memoria
`'K'` (defecto, imita la de las entradas), `'C'` (filas), `'F'` (columnas), `'A'`. Solo afecta al *layout* del resultado, no a los valores. Relevante para rendimiento al encadenar operaciones.

## Broadcasting y el caso N-D

El reparto sigue las reglas de [[concepto_broadcasting|broadcasting]] alineando por la derecha. Un caso típico N-D: normalizar cada fila de una matriz por su total, o cada "lámina" de un tensor por un vector de escalas.

```python
# Dividir un tensor (2, 3, 4) por un vector de 4 escalas (una por columna)
T = np.arange(2*3*4, dtype=float).reshape(2, 3, 4)
escala = np.array([1., 2., 4., 8.])          # (4,) → (1, 1, 4)
T / escala                                    # cada columna k se divide por escala[k]
# shape resultado: (2, 3, 4)
```

```python
# Normalizar cada fila de una matriz por su suma (broadcasting con keepdims)
M = np.array([[2., 1., 1.], [0., 3., 1.]])
M / M.sum(axis=1, keepdims=True)              # (2,3) / (2,1) → (2,3); cada fila suma 1
```

## Vectorización

`np.divide` reemplaza el bucle de división escrito a mano. Las dos versiones dan lo mismo, pero la ufunc recorre la memoria en C, sin objetos Python por elemento (ver [[concepto_vectorizacion]]):

```python
# Bucle Python (lento, explícito):
def divide_lento(a, b):
    out = np.empty(len(a), dtype=float)
    for i in range(len(a)):
        out[i] = a[i] / b[i]
    return out

# Vectorizado (un único bucle en C, con broadcasting):
a / b            # ≡ np.divide(a, b)
```

## Valor de retorno

`ndarray` con la shape del broadcasting de `x1` y `x2`, y `dtype` **siempre flotante**:

| `x1` (dtype) | `x2` (dtype) | salida (dtype) |
|--------------|--------------|----------------|
| `int64` | `int64` | **`float64`** (¡no entero!) |
| `float32` | `float32` | `float32` |
| `float64` | `int64` | `float64` |
| `complex128` | cualquiera | `complex128` |

```python
np.divide(np.array([6, 3]), np.array([2, 2]))   # array([3., 1.5])  → float64
type(np.divide(6, 2))                            # numpy.float64 (escalar 0-d)
```

Si las dos entradas son escalares, el retorno es un **escalar de NumPy**, no un ndarray.

## Casos de uso

### Tasas, proporciones y promedios
```python
aciertos = np.array([8, 5, 10])
intentos = np.array([10, 10, 10])
aciertos / intentos              # array([0.8, 0.5, 1. ])
```

### Normalizar un histograma a probabilidades
```python
conteos = np.array([2, 5, 3])
probs = np.divide(conteos, conteos.sum())   # array([0.2, 0.5, 0.3])
```

### División segura (evitar `inf`/`nan` por divisor cero)
```python
num = np.array([1., 2., 3., 4.])
den = np.array([0., 2., 0., 4.])
np.divide(num, den, out=np.full_like(num, np.nan), where=den != 0)
# array([nan, 1., nan, 1.])   → controla tú el relleno, sin warning
```

### Caso N-D: dividir cada imagen de un lote por su brillo medio
```python
imgs = np.random.rand(5, 8, 8)               # 5 imágenes 8x8
medias = imgs.mean(axis=(1, 2), keepdims=True)  # (5, 1, 1)
imgs / medias                                 # cada imagen normalizada; shape (5, 8, 8)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: divide by zero` / `invalid value` | algún `x2 == 0` | `where=x2 != 0` con `out` |
| `inf`/`nan` inesperados en el resultado | división por cero silenciosa | división segura con `out`+`where` |
| Esperar un entero y recibir floats | `np.divide` es división **real** | usar `np.floor_divide` (`//`) para el cociente entero |
| `Cannot cast` al usar `out` | `out` de dtype incompatible bajo `casting` | usar `out` flotante o ajustar `casting` |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que respalda al operador `/`.
- [[concepto_broadcasting]] — cómo se alinean `x1` y `x2`.
- [[np.floor_divide]] — cociente entero (`//`).
- [[np.mod]] · [[np.multiply]] · [[concepto_dtype]]
