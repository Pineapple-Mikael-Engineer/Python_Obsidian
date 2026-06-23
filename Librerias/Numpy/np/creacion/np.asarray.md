---
title: np.asarray — convierte a ndarray sin copiar si ya lo es
aliases:
  - asarray
  - np.asarray
tags:
  - numpy
  - api/funcion
  - creacion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_ndarray

draft: false
---

# np.asarray — convierte a ndarray sin copiar si ya lo es

`np.asarray` hace lo mismo que [[np.array]] pero con `copy=False` por defecto: **convierte la entrada en un [[concepto_ndarray|ndarray]], reutilizándolo sin copiar si ya es un array del dtype pedido**. Si le pasas una lista, la materializa (no hay más remedio); pero si le pasas un `ndarray` ya compatible, **devuelve el mismo objeto** sin tocar la memoria. Es la herramienta idiomática para escribir funciones que acepten *listas O arrays* indistintamente, sin pagar una copia cuando el llamador ya trajo un array.

## La idea

`asarray` es una **conversión idempotente**: garantiza que a la salida tienes un `ndarray`, pero hace el mínimo trabajo posible para conseguirlo.

$$ \texttt{asarray}(x) = \begin{cases} x & \text{si } x \text{ ya es ndarray del dtype/orden pedido (sin copia)} \\ \texttt{array}(x) & \text{en caso contrario (materializa un buffer nuevo)} \end{cases} $$

La diferencia con [[np.array]] está en una sola línea de su definición conceptual: `array` tiene `copy=True` (siempre duplica), `asarray` tiene `copy=False` (duplica solo si hace falta). De hecho `np.asarray(a)` equivale a `np.array(a, copy=False)`. Esa elección la convierte en el saneador de entradas por excelencia: ponerla al inicio de una función no cuesta nada cuando ya recibes un array. La frontera entre compartir y duplicar memoria se trata en [[concepto_views_vs_copias]].

## Firma

```python
np.asarray(
    a,            # array_like: datos de entrada (lista, tupla, escalar, ndarray...)
    dtype=None,   # dtype | None: tipo deseado; None = el de la entrada o el inferido
    order='K',    # {'K', 'A', 'C', 'F'}: layout en memoria deseado
    *,
    like=None,    # array_like: array de referencia (protocolo array API)
) -> ndarray
```

## Los parámetros en detalle

### `a` — los datos de entrada

`array_like`: lo que se quiere garantizar como `ndarray`. Si ya es un `ndarray` **del mismo `dtype` y orden pedidos**, se devuelve **tal cual** (mismo objeto, misma memoria). Si es una lista/tupla/escalar, se construye un buffer nuevo.

```python
a = np.array([1, 2, 3])
np.asarray(a) is a               # True   → mismo objeto, no copió
np.asarray([1, 2, 3]) is a       # False  → una lista obliga a materializar
```

### `dtype` — fuerza el tipo (y entonces sí copia)

Si se especifica y **no coincide** con el dtype de la entrada, `asarray` **debe copiar** para castear: ya no puede reutilizar el buffer.

```python
a = np.array([1, 2, 3])          # int64
np.asarray(a, dtype=np.int64) is a   # True   → mismo dtype, sin copia
b = np.asarray(a, dtype=np.float64)  # distinto dtype → COPIA
np.shares_memory(a, b)               # False
```

### `order` — layout deseado

`'C'`, `'F'`, `'A'`, `'K'` (defecto). Si pides un orden que la entrada no cumple, fuerza una copia reordenada; si ya lo cumple, no copia. Ver los strides en [[concepto_ndarray]].

### `like` — referencia de array API

`array_like` de referencia para crear el resultado con la misma librería que el objeto pasado (protocolo array API). Rara vez se usa en código NumPy puro.

> [!note] `asarray` vs `asanyarray`
> `np.asarray` **degrada** subclases a `ndarray` base (equivale a `subok=False`). Si necesitas conservar subclases como `np.matrix` o un masked array, usa `np.asanyarray`, que es idéntica pero con `subok=True`.

## El caso N-D

`asarray` **no cambia la forma**: respeta el `shape` de lo que recibe (igual que [[np.array]] al inferir desde anidamiento). Su decisión de copiar o no es independiente del número de ejes; lo que cuenta es si el `dtype`/orden coinciden.

```python
# Una entrada 4-D: si ya es ndarray compatible, asarray la devuelve intacta
T = np.arange(24).reshape(2, 2, 2, 3)   # shape (2, 2, 2, 3), int64
np.asarray(T) is T                       # True   → sin copia, da igual que sea 4-D
np.asarray(T).shape                      # (2, 2, 2, 3)

# Desde listas anidadas 3-D: materializa el buffer (no había array previo)
nd = np.asarray([[[1, 2], [3, 4]],
                 [[5, 6], [7, 8]]])
nd.shape                                 # (2, 2, 2)
nd.ndim                                  # 3
```

La regla mecánica: con un `ndarray` ya compatible la conversión es $O(1)$ sea cual sea su dimensionalidad; con una secuencia Python el coste es proporcional al `size` porque hay que recorrer el anidamiento y aplanarlo al buffer.

## Casos de uso

### Sanear la entrada de una función (el uso idiomático)

```python
def normaliza(x):
    x = np.asarray(x)        # acepta lista O array; no copia si ya es array
    return x / x.sum()

normaliza([1, 2, 3])         # funciona con lista
arr = np.array([1., 2., 3.])
normaliza(arr)               # con array NO hizo copia de más
```

### Garantizar un dtype mínimo sin copiar de balde

```python
def a_float(x):
    return np.asarray(x, dtype=np.float64)   # copia solo si no era float64 ya

a_float([1, 2, 3])           # materializa en float64
y = np.array([1., 2., 3.])
a_float(y) is y              # True  → ya era float64, sin copia
```

### Contraste directo con `np.array`

```python
a = np.array([1, 2, 3])
np.array(a)   is a   # False  → array SIEMPRE copia
np.asarray(a) is a   # True   → asarray reutiliza si puede
```

Si necesitas garantía de independencia (modificar sin tocar el original), usa `np.array(a)` o `a.copy()`; si solo necesitas "asegúrame que es un array", usa `np.asarray`. Ver [[concepto_views_vs_copias]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Modificar el resultado corrompe el original | `asarray` devolvió el **mismo** array (no copió) | usar [[np.array]] o `.copy()` si necesitas independencia |
| Esperar una copia y no obtenerla | `asarray` no copia si el dtype/orden ya coinciden | forzar con `np.array(a)` o `np.asarray(a).copy()` |
| Subclase degradada a ndarray | `asarray` aplica `subok=False` | usar `np.asanyarray` para conservar la subclase |
| Copia inesperada al pedir `dtype` | el dtype no coincidía con el de la entrada | omitir `dtype` o castear conscientemente |

## Notas relacionadas

- [[np.array]] — la versión que **siempre copia** (`copy=True`); `asarray` es su contraparte permisiva
- [[concepto_ndarray]] — la estructura que esta función garantiza a la salida
- [[concepto_views_vs_copias]] — por qué "no copiar" significa compartir memoria con la entrada
- [[concepto_dtype]] — cuándo un `dtype` distinto fuerza la copia
- [[np.zeros]] · [[np.ones]] · [[np.arange]]
