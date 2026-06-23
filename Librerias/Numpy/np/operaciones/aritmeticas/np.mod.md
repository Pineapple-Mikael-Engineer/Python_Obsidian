---
title: np.mod — resto de la división elemento a elemento (ufunc)
aliases:
  - mod
  - np.mod
  - remainder
  - modulo
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

draft: false
---

# np.mod — resto de la división elemento a elemento (ufunc)

`np.mod` (idéntica a `np.remainder`) es la [[concepto_ufuncs|ufunc]] binaria que respalda al operador `%`: calcula el **resto** de dividir cada elemento de `x1` entre el de `x2`, alineando las formas con [[concepto_broadcasting|broadcasting]]. Es la herramienta de la periodicidad: paridad, wrap-around de índices, relojes y coordenadas cíclicas. Lo verdaderamente importante de esta función es **de qué signo sale el resultado**: el signo sigue al **divisor** (convención de Python), a diferencia de `np.fmod`, que sigue al dividendo (estilo C).

## La idea en una fórmula

El resto se define usando el **floor** (redondeo hacia abajo) del cociente, lo que fija el signo del resultado al del divisor:

$$
z_i = x_{1,i} - \left\lfloor \frac{x_{1,i}}{x_{2,i}} \right\rfloor \, x_{2,i}
$$

La operación se aplica posición a posición sobre la shape común del broadcasting de `x1` y `x2`:

$$
(\dots),\ (\dots)\ \xrightarrow{\ \text{broadcast}\ }\ (\max(a_0,b_0),\,\dots,\,\max(a_k,b_k))
$$

Como se usa $\lfloor\cdot\rfloor$ (no truncamiento hacia cero), el resultado queda siempre en el intervalo del divisor: para `x2 > 0` cae en `[0, x2)`; para `x2 < 0` cae en `(x2, 0]`. Por eso **el signo lo pone el divisor**.

## Firma

```python
np.mod(
    x1,              # array_like: dividendo
    x2,              # array_like: divisor
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

### `x1` — el dividendo
`array_like` (ndarray, lista, escalar). Es el número del que se toma el resto. Se broadcastea contra `x2`.

### `x2` — el divisor (fija el signo y el rango)
`array_like` broadcasteable con `x1`. **El parámetro clave**: el signo del resultado coincide con el de `x2`, y el resultado vive en el intervalo definido por `x2`. Si vale `0`, NumPy emite un `RuntimeWarning` y rellena con `nan` (floats) o `0` (enteros), sin lanzar excepción.

```python
np.mod([-7, -7], [3, -3])   # array([ 2, -1])
# -7 % 3 = 2 (signo del divisor +)    -7 % -3 = -1 (signo del divisor -)
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de salida. Evita una asignación de memoria. Combinado con `where`, deja intactas las posiciones no calculadas (útil para evitar el `nan` del divisor cero).

### `where` — resto condicional (máscara)
`array_like` booleano broadcasteable. Solo calcula donde es `True`; donde es `False`, conserva lo que hubiera en `out`. Es el modo de saltar los divisores cero sin warning:

```python
a = np.array([10, 20, 30])
b = np.array([3, 0, 7])
np.mod(a, b, out=np.zeros_like(a), where=b != 0)
# array([1, 0, 2])   → no calcula donde b == 0
```

> [!warning] `where` necesita `out`
> Donde `where` es `False` el resultado queda sin inicializar si no pasas `out`. Pasa siempre `out` al usar `where`.

### `dtype` — tipo de cómputo y salida
Fuerza el tipo del resultado. Con enteros conserva enteros; con floats, floats. Útil para fijar `float64` cuando vas a mezclar tipos.

### `casting` — política de conversión
`'no'`, `'equiv'`, `'safe'`, `'same_kind'` (defecto), `'unsafe'`. Controla las conversiones entre entradas y hacia `out`.

### `order` — disposición en memoria
`'K'` (defecto), `'C'`, `'F'`, `'A'`. Afecta solo al *layout* del resultado.

## Broadcasting y el caso N-D

El divisor se broadcastea contra el dividendo por la derecha, así que puedes aplicar un **módulo distinto por columna** a toda una matriz o tensor sin bucles.

```python
# Un módulo distinto por columna sobre todas las filas
A = np.array([[10, 10, 10],
              [25, 25, 25]])              # (2, 3)
mods = np.array([3, 4, 7])               # (3,) → (1, 3): un divisor por columna
np.mod(A, mods)
# array([[1, 2, 3],
#        [1, 1, 4]])                       → columna k tomada módulo mods[k]; shape (2, 3)
```

```python
# Envolver coordenadas de un tensor a una caja periódica por eje
coords = np.random.randint(-50, 100, size=(4, 5, 3))   # 4x5 puntos en 3D
caja   = np.array([10, 20, 30])                          # (3,) tamaño por eje
np.mod(coords, caja)                                     # cada eje en [0, tamaño); shape (4, 5, 3)
```

## Vectorización

`np.mod` reemplaza el bucle de resto escrito a mano. Las dos versiones coinciden, pero la ufunc corre en C con broadcasting (ver [[concepto_vectorizacion]]):

```python
# Bucle Python (lento, explícito):
def restos(a, b):
    out = np.empty(len(a), dtype=int)
    for i in range(len(a)):
        out[i] = a[i] % b[i]
    return out

# Vectorizado (un único bucle en C):
a % b            # ≡ np.mod(a, b)
```

## Valor de retorno

`ndarray` con la shape del broadcasting de `x1` y `x2`; el `dtype` sigue la promoción de las entradas:

| `x1` | `x2` | salida (dtype) | rango del resultado |
|------|------|----------------|---------------------|
| `int64` | `int64 > 0` | `int64` | `[0, x2)` |
| `int64` | `int64 < 0` | `int64` | `(x2, 0]` |
| `float64` | `float64` | `float64` | mismo signo que `x2` |
| cualquiera | `0` | promovido | `nan` (float) / `0` (int) + warning |

```python
np.mod(np.array([5, 6, 7, 8]), 3)   # array([2, 0, 1, 2])
type(np.mod(7, 3))                   # numpy.int64 (escalar, dos entradas escalares)
```

## Casos de uso

### Paridad y múltiplos
```python
arr = np.arange(10)
arr[arr % 2 == 0]        # pares: [0, 2, 4, 6, 8]
np.mod(arr, 3) == 0      # múltiplos de 3
```

### Wrap-around de índices (mantener en `[0, n)`)
```python
indices = np.array([-1, 0, 5, 7])
np.mod(indices, 5)       # array([4, 0, 0, 2])   → siempre en [0, 5)
```

### Coordenadas cíclicas (reloj de 24 horas)
```python
horas = np.array([23, 24, 26, 49])
np.mod(horas, 24)        # array([23,  0,  2,  1])
```

### mod vs fmod con números negativos (la diferencia clave)
`np.mod` sigue al **divisor**; `np.fmod` sigue al **dividendo** (estilo C). Se ve solo con signos mezclados:

```python
np.mod(-7, 3)     #  2   → signo del divisor (+)
np.fmod(-7, 3)    # -1   → signo del dividendo (-)

np.mod(7, -3)     # -2   → signo del divisor (-)
np.fmod(7, -3)    #  1   → signo del dividendo (+)
```

Para periodicidad y wrap-around quieres `np.mod` (resultado siempre en el rango del divisor); para emular C o quedarte con el signo del dividendo, `np.fmod`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Signo inesperado con negativos | `np.mod` sigue al **divisor**, no al dividendo | usar `np.fmod` si quieres el signo del dividendo |
| `RuntimeWarning` + `nan`/`0` | algún `x2 == 0` | `where=x2 != 0` con `out` |
| Índice negativo tras "wrap" | se usó `%` mental de C en lugar de `np.mod` | `np.mod` ya mantiene en `[0, n)` para `n > 0` |
| Resto float con ruido (`9.999...`) | error de redondeo en flotantes | redondear o trabajar en enteros si es posible |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que respalda al operador `%`.
- [[concepto_broadcasting]] — cómo se alinea el divisor contra el dividendo.
- [[np.fmod]] — resto con el signo del **dividendo** (estilo C).
- [[np.divide]] · [[np.floor_divide]] · [[concepto_vectorizacion]]
