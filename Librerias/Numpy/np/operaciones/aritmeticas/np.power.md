---
title: np.power — potencia elemento a elemento (ufunc)
aliases:
  - power
  - np.power
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

# np.power — potencia elemento a elemento (ufunc)

`np.power` es la [[concepto_ufuncs|ufunc]] binaria que respalda al operador `**`: eleva cada elemento de la base `x1` al exponente correspondiente de `x2`, alineando las formas con [[concepto_broadcasting|broadcasting]]. Es la herramienta natural para tablas de potencias, decaimientos geométricos y polinomios vectorizados. Tiene **dos trampas de enteros** que conviene tener presentes: un exponente entero **negativo** sobre base entera es un error, y las potencias enteras grandes **desbordan en silencio**.

## La idea en una fórmula

La operación se aplica posición a posición sobre la shape común del broadcasting de `x1` (base) y `x2` (exponente):

$$
z_i = x_{1,i}^{\,x_{2,i}} \qquad \text{(base } x_1\text{, exponente } x_2\text{)}
$$

y el mapa de shapes es el del broadcasting de las dos entradas:

$$
(\dots),\ (\dots)\ \xrightarrow{\ \text{broadcast}\ }\ (\max(a_0,b_0),\,\dots,\,\max(a_k,b_k))
$$

El resultado tiene esa shape común; el `dtype` sale de la promoción de las entradas (entero si ambas son enteras — con riesgo de overflow —, flotante si alguna lo es).

## Firma

```python
np.power(
    x1,              # array_like: base
    x2,              # array_like: exponente
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

### `x1` — la base
`array_like` (ndarray, lista, escalar). Se broadcastea contra el exponente. Su `dtype` (junto al de `x2`) decide si el cálculo es entero o flotante, y con ello el riesgo de overflow.

### `x2` — el exponente
`array_like` broadcasteable con `x1`. **El parámetro con trampa**: si tanto la base como el exponente son **enteros** y el exponente es **negativo**, NumPy lanza `ValueError` (no puede representar `2**-1 == 0.5` en un entero). La solución es usar base flotante.

```python
np.power(2, 3)        # 8
np.power(2, -1)       # ValueError: Integers to negative integer powers are not allowed.
np.power(2.0, -1)     # 0.5   → base flotante, OK
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida. Evita una asignación; útil en bucles que reutilizan memoria. Su `dtype` debe ser compatible bajo `casting`.

### `where` — potencia condicional (máscara)
`array_like` booleano broadcasteable. Solo calcula donde es `True`; donde es `False`, conserva el valor previo de `out`. Como en toda ufunc, conviene pasar `out` cuando se usa `where` para no dejar posiciones sin inicializar.

```python
base = np.array([2., 3., 4.])
np.power(base, 2, out=np.zeros_like(base), where=base > 2)
# array([0., 9., 16.])   → no eleva donde base <= 2
```

### `dtype` — tipo de cómputo y salida
Fuerza el tipo del resultado. Es la palanca contra el **overflow**: pedir `dtype=np.float64` (o usar bases float) evita que potencias grandes se desborden como enteros.

```python
np.power(np.int32(10), 10)                 # 1410065408  ← overflow silencioso (int32)
np.power(10, 10, dtype=np.float64)         # 1e10        ← seguro
```

### `casting` — política de conversión
Controla las conversiones permitidas entre entradas y hacia `out`: `'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`.

### `order` — disposición en memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Afecta solo al *layout* del resultado, no a los valores.

## Broadcasting y el caso N-D

Con broadcasting puedes elevar toda una matriz a un vector de exponentes distinto **por columna** (o por fila), sin bucles. El vector de exponentes se alinea por la derecha contra la matriz.

```python
# Una potencia distinta por columna, sobre todas las filas
bases = np.array([[2., 2., 2.],
                  [3., 3., 3.]])            # (2, 3)
exps  = np.array([1., 2., 3.])             # (3,) → (1, 3): exponente por columna
np.power(bases, exps)
# array([[ 2.,  4.,  8.],
#        [ 3.,  9., 27.]])                  → columna k elevada a exps[k]; shape (2, 3)
```

```python
# Construir la matriz de Vandermonde: x_i^j para cada x y cada potencia j
x = np.array([1., 2., 3.])                 # (3,) → (3, 1)
j = np.arange(4)                            # (4,) → (1, 4)
np.power(x[:, None], j)                     # (3, 4): fila i = [x_i^0, x_i^1, x_i^2, x_i^3]
```

## Vectorización

`np.power` reemplaza el bucle de exponenciación. Ambas versiones coinciden, pero la ufunc corre en C con broadcasting (ver [[concepto_vectorizacion]]):

```python
# Bucle Python (lento, explícito):
def potencias(bases, exps):
    out = np.empty(len(bases))
    for i in range(len(bases)):
        out[i] = bases[i] ** exps[i]
    return out

# Vectorizado (un único bucle en C):
bases ** exps        # ≡ np.power(bases, exps)
```

## Valor de retorno

`ndarray` con la shape del broadcasting de base y exponente; el `dtype` sigue las reglas de promoción:

| `x1` (base) | `x2` (exp) | salida (dtype) | nota |
|-------------|------------|----------------|------|
| `int64` | `int64 ≥ 0` | `int64` | riesgo de **overflow** silencioso |
| `int64` | `int64 < 0` | — | **`ValueError`** |
| `float64` | cualquiera | `float64` | exponentes negativos/fraccionarios OK |
| `int64` | `float64` | `float64` | promoción a float |

```python
np.power(np.array([1, 2, 3]), 2)        # array([1, 4, 9])     int64
np.power(np.array([1., 2., 3.]), 0.5)   # array([1., 1.41, 1.73])  float64 (raíces)
```

Con dos escalares el retorno es un **escalar de NumPy**, no un ndarray.

## Casos de uso

### Cuadrados, raíces y recíprocos
```python
np.power(x, 2)       # cuadrado   (o np.square, más directa)
np.power(x, 0.5)     # raíz       (o np.sqrt)
np.power(x, -1)      # recíproco  (requiere x float)
```

### Decaimiento geométrico discreto
```python
np.power(0.9, np.arange(10))   # [1, 0.9, 0.81, 0.729, ...]
```

### Evaluar un polinomio vectorizado (Vandermonde + coeficientes)
```python
x = np.array([1., 2., 3.])
coef = np.array([1., -2., 1.])               # 1 - 2x + x^2
V = np.power(x[:, None], np.arange(3))       # (3, 3)
V @ coef                                       # valor del polinomio en cada x
```

### Caso N-D: potencias por canal de un tensor
```python
T = np.abs(np.random.rand(4, 5, 3))          # 4x5 píxeles, 3 canales
gamma = np.array([0.45, 0.5, 0.6])           # (3,) → corrección por canal
np.power(T, gamma)                            # cada canal con su exponente; shape (4, 5, 3)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `Integers to negative integer powers are not allowed` | base int, exponente int negativo | usar base flotante (`x.astype(float)`) |
| Resultado negativo/absurdo en potencias grandes | overflow entero silencioso | `dtype=np.float64` o base float |
| `nan` con base negativa y exponente fraccionario | raíces de negativos no son reales | usar complejos, o `np.float_power` para promoción más laxa |
| Pérdida de precisión en exponentes negativos | `np.power` no promueve a float automáticamente | usar [[np.float_power]] (siempre float) o `np.sqrt` para raíces |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que respalda al operador `**`.
- [[concepto_broadcasting]] — cómo se alinean base y exponente (potencias por columna).
- [[np.float_power]] — variante que promueve siempre a flotante (sin el error de enteros).
- [[np.square]] · [[np.sqrt]] · [[np.exp]] · [[concepto_dtype]]
