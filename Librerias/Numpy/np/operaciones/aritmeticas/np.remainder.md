---
title: np.remainder — resto con signo del divisor (ufunc del operador %)
aliases:
  - remainder
  - np.remainder
  - resto
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

# np.remainder — resto con signo del divisor (ufunc del operador %)

`np.remainder` calcula el **resto de la división entera** elemento a elemento, con el signo del
**divisor** (semántica de Python). Es la [[concepto_ufuncs|ufunc]] que respalda el operador `%`, así
que `a % b` invoca `np.remainder(a, b)`. Es el **nombre canónico** del módulo en NumPy: [[np.mod]] es
exactamente la misma función (un alias). Forma con [[np.floor_divide]] el par cociente/resto.

## La idea en una fórmula

El resto se define a partir del cociente redondeado hacia abajo (ver [[np.floor_divide]]):

$$ z_i = x_i - \left\lfloor \frac{x_i}{y_i} \right\rfloor y_i $$

De aquí salen dos hechos clave. Primero, el resultado tiene **el signo de $y_i$** (el divisor) y vive
en el intervalo $[0, y_i)$ si $y_i>0$. Segundo, junto a [[np.floor_divide]] cumple la identidad de
división euclídea:

$$ x_i = (x_i \mathbin{//} y_i)\, y_i + z_i \qquad\Longleftrightarrow\qquad
\texttt{a == (a//b)*b + a\%b} $$

Como toda ufunc binaria, alinea sus entradas por [[concepto_broadcasting|broadcasting]] y la salida
toma la shape común:

$$ (n_0,\dots,n_k),\ (m_0,\dots,m_k)\ \xrightarrow{\ \text{broadcast}\ }\
(\max(n_0,m_0),\,\dots,\,\max(n_k,m_k)) $$

## Firma

```python
np.remainder(
    x1, x2, /,          # array_like: dividendo y divisor (se broadcastean)
    out=None,           # ndarray | None: destino preasignado
    *,
    where=True,         # array_like[bool]: máscara de cómputo
    casting='same_kind',# política de conversión de tipos
    order='K',          # orden de memoria del resultado
    dtype=None,         # dtype: tipo de cómputo/salida
) -> ndarray
```

## Los parámetros en detalle

### `x1`, `x2` — dividendo y divisor
`array_like` (ndarray, lista, escalar), broadcasteables entre sí. El **signo del resultado lo fija
`x2`** (el divisor), no `x1`. Si ambos son enteros el resto es entero; si alguno es float, es float.

```python
np.remainder([5, 6, 7, 8], 3)   # array([2, 0, 1, 2])
np.remainder(-7, 3)             #  2   ← signo del divisor (positivo)
np.remainder(7, -3)             # -2   ← signo del divisor (negativo)
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Evita asignar un array nuevo; puede ser uno de los
operandos para operar in-place.

### `where` — cómputo condicional (máscara)
`array_like` booleano broadcasteable. Solo calcula donde es `True`; el resto conserva el valor previo
de `out`. La aplicación típica es **saltar divisores nulos** sin disparar el warning.

```python
x = np.array([10, 20, 30])
y = np.array([3, 0, 4])
out = np.zeros_like(x)
np.remainder(x, y, out=out, where=y != 0)   # ignora el divisor 0
```

### `dtype` — tipo de cómputo y salida
Fuerza el tipo de cálculo/resultado. Por defecto sale de la promoción de `x1` y `x2`.

### `casting` — política de conversión
`'no' | 'equiv' | 'safe' | 'same_kind' | 'unsafe'`. Qué conversiones se permiten al combinar tipos o
escribir en `out`. Por defecto `'same_kind'`.

### `order` — orden de memoria del resultado
`'K' | 'C' | 'F' | 'A'`. Layout del array de salida; importa por rendimiento al encadenar
operaciones. Por defecto `'K'`.

## np.remainder vs np.fmod (el contraste del signo)

Es la confusión más frecuente. `np.remainder` (`%`) sigue el signo del **divisor**; `np.fmod` sigue
el del **dividendo** (semántica de C). Coinciden cuando los operandos tienen el mismo signo; difieren
con negativos.

| Función | Operador | Signo del resultado | Fórmula |
|---------|----------|---------------------|---------|
| `np.remainder` / `np.mod` | `%` | del **divisor** (`x2`) | $x - \lfloor x/y\rfloor\,y$ |
| `np.fmod` | — | del **dividendo** (`x1`) | $x - \operatorname{trunc}(x/y)\,y$ |

```python
np.remainder(-7, 3)   #  2   resto en [0, 3), signo del divisor
np.fmod(-7, 3)        # -1   signo del dividendo (-7), estilo C
np.remainder(7, -3)   # -2
np.fmod(7, -3)        #  1
```

## Broadcasting y el caso N-D

Operación **element-wise pura**: no se reduce ningún eje, la shape de salida es la shape común de
broadcasting. El caso N-D habitual es tomar el resto de un tensor contra un vector alineado al último
eje.

| `x1.shape` | `x2.shape` | salida | lectura |
|-----------|-----------|--------|---------|
| `(n,)` | `()` escalar | `(n,)` | resto contra el mismo divisor |
| `(m, n)` | `(n,)` | `(m, n)` | un divisor por columna, repetido en cada fila |
| `(b, m, n)` | `(1, 1, n)` | `(b, m, n)` | mismo periodo por columna en todo el lote |

```python
T = np.arange(24).reshape(2, 3, 4)   # (2, 3, 4)
mods = np.array([2, 3, 4, 5])        # (4,) → alinea al último eje
np.remainder(T, mods).shape          # (2, 3, 4)
np.remainder(T, mods)[0]
# [[0, 1, 2, 3],
#  [0, 2, 2, 2],
#  [0, 0, 2, 1]]
```

## Vectorización

Reemplaza un bucle Python que aplicaría `%` elemento a elemento; la versión vectorizada corre en C con
[[concepto_broadcasting|broadcasting]]:

```python
# Bucle Python (lento):
out = np.empty_like(x)
for i in range(x.size):
    out[i] = x[i] % y[i]

# Vectorizado (un bucle en C):
out = np.remainder(x, y)   # ≡ x % y
```

## Valor de retorno

`ndarray` (o escalar de NumPy si ambas entradas son escalares) con la shape común de broadcasting. El
dtype sale de la promoción; el signo, del divisor:

| `x1` | `x2` | salida | nota |
|------|------|--------|------|
| `int` | `int` | `int` en $[0, |y|)$ con signo de `y` | resto entero |
| `float` | `float`/`int` | `float` | resto en punto flotante |
| cualquiera | divisor `0` | `0` (int) / `nan` (float) + `RuntimeWarning` | enmascarar con `where` |

```python
np.remainder([5, 6, 7, 8], 3)   # array([2, 0, 1, 2])  int
np.remainder(5.5, 2.0)          # 1.5                   float
```

## Casos de uso

### Paridad y múltiplos
```python
arr = np.arange(10)
pares = np.remainder(arr, 2) == 0     # [ True False  True ...]
```

### Envolver índices en un rango (wrap-around)
```python
idx = np.array([-1, 0, 5, 12])
np.remainder(idx, 10)   # [9, 0, 5, 2]  → siempre en [0, 10), incluso negativos
```

### Coordenadas cíclicas (reloj, ángulos)
```python
minutos = np.array([70, 130, 1450])
np.remainder(minutos, 60)   # [10, 10, 10]  minuto dentro de la hora
```

### Ejemplo N-D: posición dentro de cada bloque
```python
T = np.arange(24).reshape(2, 3, 4)
np.remainder(T, 5)   # posición de cada valor dentro de bloques de tamaño 5, conserva (2,3,4)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| signo inesperado con negativos | sigue al **divisor**, no al dividendo | usar `np.fmod` para signo del dividendo (estilo C) |
| `RuntimeWarning: divide by zero` | divisor `0` | `where=x2 != 0` o validar el divisor |
| esperar `np.mod` distinto de `np.remainder` | son la **misma** función (alias) | indiferente; `remainder` es el nombre canónico |
| resto float donde se esperaba int | un operando es float | castear a entero o usar entradas enteras |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que ejecuta `%`
- [[concepto_broadcasting]] — cómo se alinean `x1` y `x2`
- [[np.mod]] — mismo cálculo (alias) · [[np.floor_divide]] — el cociente que completa la identidad
- [[np.divmod]] — devuelve `(cociente, resto)` en una pasada
