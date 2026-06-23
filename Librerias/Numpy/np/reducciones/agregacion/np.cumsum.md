---
title: np.cumsum — suma acumulada (scan) a lo largo de un eje
aliases:
  - cumsum
  - np.cumsum
  - suma acumulada
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_vectorizacion
  - concepto_dtype

draft: false
---

# np.cumsum — suma acumulada (scan) a lo largo de un eje

`np.cumsum` es un **scan**, no una reducción: en cada posición guarda la suma de todo lo anterior
(incluido el propio elemento). A diferencia de [[np.sum]], que **colapsa** el eje a un valor,
`np.cumsum` **conserva el shape**: produce un array del mismo tamaño con los **prefijos acumulados**.
Aquí `axis` **no colapsa, dirige**: marca la dirección en la que se barre el array.

## La idea en una fórmula

Un scan transforma una secuencia en sus sumas de prefijos. El **mapa de shapes** es lo que lo
distingue de `np.sum`: la forma **no cambia**.

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{cumsum, axis}=p\ }\ (n_0,\dots,n_k) \qquad \text{(shape conservado)} $$

La fórmula por índices, para un vector $a$ recorrido a lo largo del eje:

$$
c_k = \sum_{i \le k} a_i \qquad (c_0 = a_0,\quad c_k = c_{k-1} + a_k)
$$

El elemento $k$-ésimo es la suma de los $k+1$ primeros. **Contraste con [[np.sum]]**: `sum` devuelve
solo $c_{n-1}$ (el último prefijo, el total) y tira el eje; `cumsum` devuelve **toda la trayectoria**
$c_0, c_1, \dots, c_{n-1}$ y mantiene el eje. El **último elemento de `cumsum` es exactamente `sum`**.

Con `axis=None` (defecto) el array se **aplana primero** y el scan se hace en 1D:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{cumsum, axis=None}\ }\ (n_0 \cdot n_1 \cdots n_k,) $$

## Firma

```python
np.cumsum(
    a,             # array_like: el tensor de entrada
    axis=None,     # None | int: eje a lo largo del cual acumular (None = aplanar a 1D)
    dtype=None,    # dtype: tipo del acumulador y del resultado
    out=None,      # ndarray: destino preasignado
) -> ndarray
```

A diferencia de `np.sum`, **no** tiene `keepdims`, `initial` ni `where` (el scan no colapsa nada que
reinsertar y la dependencia secuencial no admite máscara directa).

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Su `dtype` fija el
acumulador por defecto (y el riesgo de overflow, ver `dtype`).

### `axis` — el eje que se BARRE (dirige, no colapsa)
La diferencia clave con las reducciones. `None` (defecto) **aplana** el array a 1D y acumula sobre
ese vector. Un `int` acumula **a lo largo** de ese [[concepto_axis_parametro|eje]] **conservando el
shape**: el eje no desaparece, se recorre. No acepta tupla de ejes (un scan barre un solo eje).

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
np.cumsum(M)          # axis=None → aplana: [1, 3, 6, 10, 15, 21]   shape (6,)
np.cumsum(M, axis=0)  # baja por columnas: [[1, 2, 3], [5, 7, 9]]   shape (2, 3)
np.cumsum(M, axis=1)  # a lo largo de filas: [[1, 3, 6], [4, 9, 15]] shape (2, 3)
```
`axis=-1` es el último eje, idiomático para "acumular la última dimensión".

### `dtype` — tipo del acumulador
Fija el tipo en el que se acumula. Como en [[np.sum]], evita el **overflow silencioso** de enteros
pequeños; aquí importa además que los **prefijos intermedios** también pueden desbordar antes que el
total. Ver [[concepto_dtype]].

```python
arr = np.ones(300, dtype=np.int8)
np.cumsum(arr)[-1]                 # -44  ← overflow silencioso (300 mod 256)
np.cumsum(arr, dtype=np.int64)[-1] # 300  ← acumulador seguro
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con **el mismo shape que `a`** (o que `a` aplanado si `axis=None`) y dtype
compatible. Evita una asignación de memoria.

## El eje y el caso N-D

El shape **siempre se conserva** (salvo `axis=None`, que aplana). `axis` elige la dirección del
barrido; los demás ejes se acumulan de forma **independiente**.

| `a.shape` | `axis` | salida (shape) | lectura |
|-----------|--------|----------------|---------|
| `(n,)` | `0` / `None` | `(n,)` | prefijos del vector |
| `(m, n)` | `None` | `(m·n,)` | aplana y acumula en 1D |
| `(m, n)` | `0` | `(m, n)` | acumula **bajando** por cada columna |
| `(m, n)` | `1` | `(m, n)` | acumula **a lo largo** de cada fila |
| `(b, m, n)` | `0` | `(b, m, n)` | suma de prefijos a lo largo del lote |
| `(b, m, n)` | `-1` | `(b, m, n)` | acumula la última dimensión, fila a fila |

```python
# Tensor (2, 2, 3): un lote de 2 matrices 2x3
T = np.array([[[1, 2, 3],
               [4, 5, 6]],
              [[1, 1, 1],
               [2, 2, 2]]])
np.cumsum(T, axis=2)   # barre la última dim de cada fila, shape (2, 2, 3):
# [[[ 1,  3,  6],      ← 1, 1+2, 1+2+3
#   [ 4,  9, 15]],     ← 4, 4+5, 4+5+6
#  [[ 1,  2,  3],
#   [ 2,  4,  6]]]
np.cumsum(T, axis=0)   # acumula entre las dos matrices del lote:
# matriz[0] = T[0]; matriz[1] = T[0] + T[1]
```
Cada "línea" a lo largo de `axis` se trata como una secuencia independiente; el resultado conserva la
geometría completa.

## Vectorización

`np.cumsum` resuelve un patrón que **no se puede vectorizar como suma directa**: cada salida depende
de la anterior (dependencia secuencial). NumPy traslada ese bucle a C en vez de ejecutarlo en el
intérprete:

```python
# Bucle Python (lento, explícito):
def cumsum_1d(a):
    out = np.empty_like(a)
    acc = 0
    for i in range(len(a)):
        acc += a[i]
        out[i] = acc
    return out

# Vectorizado (NumPy recorre la dependencia en C):
np.cumsum(a)
```
Es el ejemplo canónico de [[concepto_vectorizacion]] para **dependencias secuenciales**: el bucle no
se elimina (cada paso necesita el anterior), pero se ejecuta compilado y sin objetos Python por
elemento.

## Valor de retorno

Siempre un `ndarray` (nunca un escalar 0-d, a diferencia de `np.sum`):

| Entrada (shape) | `axis` | salida (shape) | dtype |
|-----------------|--------|----------------|-------|
| `(n,)` | `0` / `None` | `(n,)` | ndarray |
| `(m, n)` | `0` / `1` | `(m, n)` | ndarray (shape conservado) |
| `(m, n)` | `None` | `(m·n,)` | ndarray aplanado |
| N-D | `int` | **misma** que la entrada | ndarray |

Reglas de `dtype` (sin `dtype=` explícito): igual que [[np.sum]] — enteros pequeños se promueven al
entero por defecto de la plataforma (`int64`), `bool` → `int64` (el cumsum de una máscara da el
**conteo acumulado** de `True`), floats y complejos conservan su tipo.

```python
np.cumsum([True, False, True, True])  # [1, 1, 2, 3]  → conteo acumulado
type(np.cumsum([1, 2, 3]))            # numpy.ndarray  (incluso en 1D)
```

## Casos de uso

### Saldo acumulado en el tiempo
```python
movimientos = np.array([100, -30, 50, -20])
saldo = np.cumsum(movimientos)   # [100, 70, 120, 100]  → saldo tras cada movimiento
```

### CDF empírica (distribución acumulada)
```python
frecuencias = np.array([2, 3, 5, 1])
cdf = np.cumsum(frecuencias) / np.sum(frecuencias)   # [0.18, 0.45, 0.91, 1.0]
```

### Sumas de prefijos para consultas de rango
```python
a = np.array([3, 1, 4, 1, 5, 9])
pre = np.cumsum(a)            # [3, 4, 8, 9, 14, 23]
# suma de a[2:5] = pre[4] - pre[1] = 14 - 4 = 10
```

### Ejemplo trabajado en N-D (el barrido por el eje)
```python
T = np.array([[[1, 2, 3],
               [4, 5, 6]],
              [[1, 1, 1],
               [2, 2, 2]]])    # shape (2, 2, 3)

np.cumsum(T, axis=2)   # acumula a lo largo de la última dimensión, shape (2, 2, 3)
# [[[ 1,  3,  6],      ← prefijos de [1,2,3]
#   [ 4,  9, 15]],     ← prefijos de [4,5,6]
#  [[ 1,  2,  3],      ← prefijos de [1,1,1]
#   [ 2,  4,  6]]]     ← prefijos de [2,2,2]

np.cumsum(T, axis=0)[1]  # T[0] + T[1] = [[2, 3, 4], [6, 7, 8]]  (último prefijo del lote = np.sum(T, axis=0))
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado aplanado a 1D | `axis=None` por defecto en 2D+ | pasar `axis` explícito |
| Overflow en enteros | acumulador pequeño (también en prefijos intermedios) | `dtype=np.int64` |
| `NaN` contamina el resto de la serie | `NaN` se propaga acumulativamente hacia adelante | usar [[np.nancumsum]] |
| Esperar un escalar | `cumsum` **conserva el shape**, no reduce | para el total usar [[np.sum]] |

## Notas relacionadas

- [[concepto_axis_parametro]] — aquí `axis` dirige el barrido, no colapsa
- [[concepto_vectorizacion]] — el scan como dependencia secuencial llevada a C
- [[concepto_dtype]] — el acumulador y el overflow
- [[np.sum]] · [[np.cumprod]] · [[np.diff]] · [[np.nancumsum]]
