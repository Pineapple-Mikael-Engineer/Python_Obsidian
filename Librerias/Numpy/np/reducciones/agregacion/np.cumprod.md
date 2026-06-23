---
title: np.cumprod — producto acumulado (scan) a lo largo de un eje
aliases:
  - cumprod
  - np.cumprod
  - producto acumulado
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

# np.cumprod — producto acumulado (scan) a lo largo de un eje

`np.cumprod` es un **scan** multiplicativo: en cada posición guarda el producto de todo lo anterior
(incluido el propio elemento). Es la gemela multiplicativa de [[np.cumsum]] —misma mecánica de barrido
y **mismo shape conservado**— y, como [[np.prod]], arrastra el riesgo de **overflow** (el crecimiento
es exponencial). A diferencia de [[np.prod]], que colapsa el eje al producto total, `np.cumprod`
**conserva el shape** y devuelve toda la trayectoria de productos parciales.

## La idea en una fórmula

Un scan multiplicativo transforma una secuencia en sus productos de prefijos. El **mapa de shapes**
no cambia la forma:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{cumprod, axis}=p\ }\ (n_0,\dots,n_k) \qquad \text{(shape conservado)} $$

La fórmula por índices, para un vector $a$ recorrido a lo largo del eje:

$$
c_k = \prod_{i \le k} a_i \qquad (c_0 = a_0,\quad c_k = c_{k-1} \cdot a_k)
$$

El elemento $k$-ésimo es el producto de los $k+1$ primeros. **Contraste con [[np.prod]]**: `prod`
devuelve solo $c_{n-1}$ (el último prefijo, el producto total) y tira el eje; `cumprod` devuelve
**toda la trayectoria** $c_0, c_1, \dots, c_{n-1}$ y mantiene el eje. El **último elemento de
`cumprod` es exactamente `prod`**.

Con `axis=None` (defecto) el array se **aplana primero** y el scan se hace en 1D:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{cumprod, axis=None}\ }\ (n_0 \cdot n_1 \cdots n_k,) $$

## Firma

```python
np.cumprod(
    a,             # array_like: el tensor de entrada
    axis=None,     # None | int: eje a lo largo del cual acumular (None = aplanar a 1D)
    dtype=None,    # dtype: tipo del acumulador y del resultado
    out=None,      # ndarray: destino preasignado
) -> ndarray
```

Como `np.cumsum`, **no** tiene `keepdims`, `initial` ni `where`.

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Se convierte a `ndarray` si no lo es. Su `dtype` fija el
acumulador por defecto, y con él el riesgo de overflow (ver `dtype`), que aquí es **agudo**.

### `axis` — el eje que se BARRE (dirige, no colapsa)
`None` (defecto) **aplana** el array a 1D y acumula sobre ese vector. Un `int` acumula **a lo largo**
de ese [[concepto_axis_parametro|eje]] **conservando el shape**: el eje se recorre, no desaparece. No
acepta tupla de ejes (un scan barre un solo eje).

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
np.cumprod(M)          # axis=None → aplana: [1, 2, 6, 24, 120, 720]   shape (6,)
np.cumprod(M, axis=0)  # baja por columnas: [[1, 2, 3], [4, 10, 18]]   shape (2, 3)
np.cumprod(M, axis=1)  # a lo largo de filas: [[1, 2, 6], [4, 20, 120]] shape (2, 3)
```
`axis=-1` es el último eje, idiomático para "acumular la última dimensión".

### `dtype` — tipo del acumulador (overflow AGUDO)
Fija el tipo en el que se acumula el producto. Es **más peligroso** que en `cumsum`: el crecimiento
es **multiplicativo/exponencial**, así que los prefijos desbordan muy pronto y **en silencio**
(resultado negativo o absurdo, sin excepción). Ver [[concepto_dtype]].

```python
np.cumprod(np.arange(1, 21))[-1]                 # 20! desborda int64 → erróneo, sin aviso
np.cumprod(np.arange(1, 21), dtype=np.float64)[-1]  # 2.43e18  → seguro (pierde exactitud)
```
Regla práctica: con enteros y más de un puñado de factores, **fija `dtype`** (`int64` si cabe;
`float64` si priorizas no desbordar).

### `out` — escribir en un buffer existente
`ndarray` preasignado con **el mismo shape que `a`** (o que `a` aplanado si `axis=None`) y dtype
compatible. Evita una asignación de memoria.

## El eje y el caso N-D

El shape **siempre se conserva** (salvo `axis=None`, que aplana). `axis` elige la dirección del
barrido; los demás ejes se acumulan de forma **independiente**.

| `a.shape` | `axis` | salida (shape) | lectura |
|-----------|--------|----------------|---------|
| `(n,)` | `0` / `None` | `(n,)` | productos de prefijos del vector |
| `(m, n)` | `None` | `(m·n,)` | aplana y acumula en 1D |
| `(m, n)` | `0` | `(m, n)` | acumula **bajando** por cada columna |
| `(m, n)` | `1` | `(m, n)` | acumula **a lo largo** de cada fila |
| `(b, m, n)` | `0` | `(b, m, n)` | producto de prefijos a lo largo del lote |
| `(b, m, n)` | `-1` | `(b, m, n)` | acumula la última dimensión, fila a fila |

```python
# Tensor (2, 2, 3): un lote de 2 matrices 2x3
T = np.array([[[1, 2, 3],
               [4, 5, 6]],
              [[1, 1, 2],
               [2, 2, 2]]])
np.cumprod(T, axis=2)  # barre la última dim de cada fila, shape (2, 2, 3):
# [[[ 1,  2,  6],      ← 1, 1·2, 1·2·3
#   [ 4, 20, 120]],    ← 4, 4·5, 4·5·6
#  [[ 1,  1,  2],
#   [ 2,  4,  8]]]
```
Cada "línea" a lo largo de `axis` se trata como una secuencia independiente; el resultado conserva la
geometría completa.

## Vectorización

`np.cumprod` resuelve una **dependencia secuencial** (cada salida depende de la anterior): no se
vectoriza como producto directo, pero NumPy lleva ese bucle a C en vez de ejecutarlo en el intérprete:

```python
# Bucle Python (lento, explícito):
def cumprod_1d(a):
    out = np.empty_like(a)
    acc = 1
    for i in range(len(a)):
        acc *= a[i]
        out[i] = acc
    return out

# Vectorizado (NumPy recorre la dependencia en C):
np.cumprod(a)
```
Es un caso de [[concepto_vectorizacion]] con dependencia secuencial: el bucle no desaparece (cada paso
necesita el anterior), pero se ejecuta compilado y sin objetos Python por elemento.

## Valor de retorno

Siempre un `ndarray` (nunca un escalar 0-d):

| Entrada (shape) | `axis` | salida (shape) | dtype |
|-----------------|--------|----------------|-------|
| `(n,)` | `0` / `None` | `(n,)` | ndarray |
| `(m, n)` | `0` / `1` | `(m, n)` | ndarray (shape conservado) |
| `(m, n)` | `None` | `(m·n,)` | ndarray aplanado |
| N-D | `int` | **misma** que la entrada | ndarray |

Reglas de `dtype` (sin `dtype=` explícito): enteros pequeños se promueven al entero por defecto de la
plataforma (`int64`) —insuficiente contra el overflow en productos largos—; `bool` → `int64` (el
cumprod de una máscara es un **AND acumulado**: cae a 0 en el primer `False` y ya no se recupera);
floats y complejos conservan su tipo.

```python
np.cumprod([True, True, False, True])  # [1, 1, 0, 0]  → AND acumulado
type(np.cumprod([1, 2, 3]))            # numpy.ndarray  (incluso en 1D)
```

## Casos de uso

### Factor de capitalización compuesta
```python
tasas = np.array([1.05, 1.03, 1.04])   # +5%, +3%, +4%
crecimiento = np.cumprod(tasas)        # [1.05, 1.0815, 1.12476]  → capital acumulado por periodo
```

### Factoriales parciales
```python
np.cumprod(np.arange(1, 6))   # [1, 2, 6, 24, 120]  → 1!, 2!, 3!, 4!, 5!
```

### Supervivencia: probabilidad de seguir vivo tras cada paso
```python
p_sobrevivir = np.array([0.99, 0.98, 0.97, 0.95])
np.cumprod(p_sobrevivir)   # [0.99, 0.9702, 0.9411, 0.8940]  → prob. acumulada
```

### Ejemplo trabajado en N-D
```python
T = np.array([[[1, 2, 3],
               [4, 5, 6]],
              [[1, 1, 2],
               [2, 2, 2]]])    # shape (2, 2, 3)

np.cumprod(T, axis=2)  # acumula a lo largo de la última dimensión, shape (2, 2, 3)
# [[[ 1,  2,  6],      ← productos de prefijos de [1,2,3]
#   [ 4, 20, 120]],    ← productos de prefijos de [4,5,6]
#  [[ 1,  1,  2],      ← [1,1,2]
#   [ 2,  4,  8]]]     ← [2,2,2]
# El último elemento de cada línea coincide con np.prod sobre ese eje.
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado aplanado a 1D | `axis=None` por defecto en 2D+ | pasar `axis` explícito |
| Overflow / resultado absurdo | crecimiento multiplicativo (también en prefijos) | `dtype=np.float64` o `np.int64` |
| Todo 0 a partir de cierto punto | un factor es 0 anula el resto de la trayectoria | revisar datos |
| `NaN` contamina el resto de la serie | `NaN` se propaga acumulativamente | usar [[np.nancumprod]] |
| Esperar un escalar | `cumprod` **conserva el shape**, no reduce | para el total usar [[np.prod]] |

## Notas relacionadas

- [[concepto_axis_parametro]] — aquí `axis` dirige el barrido, no colapsa
- [[concepto_vectorizacion]] — el scan como dependencia secuencial llevada a C
- [[concepto_dtype]] — el acumulador y el overflow (agudo aquí)
- [[np.cumsum]] · [[np.prod]] · [[np.nancumprod]]
