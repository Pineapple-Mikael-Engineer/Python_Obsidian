---
title: np.negative — negación elemento a elemento (ufunc del - unario)
aliases:
  - negative
  - np.negative
  - negacion
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

# np.negative — negación elemento a elemento (ufunc del - unario)

`np.negative` cambia el signo de cada elemento de un array. Es la [[concepto_ufuncs|ufunc]] **unaria**
que respalda el operador `-` unario, así que `-x` invoca `np.negative(x)`. Al ser unaria no combina
dos arrays: toma uno solo y devuelve otro de la **misma shape**, con cada valor negado.

## La idea en una fórmula

Cada elemento de la salida es el opuesto del de la entrada:

$$ z_i = -\,x_i $$

No hay broadcasting entre dos operandos (es unaria), así que la transformación de shapes es la
**identidad**: la salida conserva exactamente la forma de la entrada. Aun así sigue las reglas de una
[[concepto_broadcasting|ufunc]] respecto a `out` y `where`:

$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{negative}\ }\ (n_0,\dots,n_k) $$

## Firma

```python
np.negative(
    x, /,               # array_like: el array a negar
    out=None,           # ndarray | None: destino preasignado
    *,
    where=True,         # array_like[bool]: máscara de cómputo
    casting='same_kind',# política de conversión de tipos
    order='K',          # orden de memoria del resultado
    dtype=None,         # dtype: tipo de cómputo/salida
) -> ndarray
```

## Los parámetros en detalle

### `x` — el array de entrada
`array_like` (ndarray, lista, escalar). Único operando: `np.negative` es **unaria**. La salida tiene
su misma shape y, por defecto, su mismo dtype.

```python
np.negative([1, -2, 3])   # array([-1,  2, -3])
np.negative(5)            # -5
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con la shape de `x`. Permite negar **in-place** pasando el propio array, lo que
evita asignar memoria nueva:

```python
arr = np.array([1.0, -2.0, 3.0])
np.negative(arr, out=arr)   # arr ahora es [-1., 2., -3.]  (sin copia)
```

### `where` — cómputo condicional (máscara)
`array_like` booleano broadcasteable con `x`. Solo niega donde es `True`; donde es `False` conserva lo
que hubiera en `out`. Útil para negar **solo** ciertos elementos (p. ej. los negativos, equivalente a
un valor absoluto manual). Conviene pasar `out` para no dejar posiciones sin inicializar.

```python
x = np.array([-3, 1, -5, 2])
out = x.copy()
np.negative(x, out=out, where=x < 0)   # niega solo los negativos → [3, 1, 5, 2]
```

### `dtype` — tipo de cómputo y salida
Fuerza el tipo de cálculo/resultado. Por defecto conserva el de `x`.

### `casting` — política de conversión
`'no' | 'equiv' | 'safe' | 'same_kind' | 'unsafe'`. Qué conversiones se permiten al escribir en `out`
o forzar `dtype`. Por defecto `'same_kind'`.

### `order` — orden de memoria del resultado
`'K' | 'C' | 'F' | 'A'`. Layout del array de salida; por defecto `'K'` (conserva el de `x`).

## Broadcasting y el caso N-D

Al ser unaria, `np.negative` **no transforma la shape**: cada elemento se niega en su sitio, sea cual
sea la dimensión. No hay eje que se reduzca ni alineación entre operandos.

| `x.shape` | salida | lectura |
|-----------|--------|---------|
| `(n,)` | `(n,)` | niega cada elemento |
| `(m, n)` | `(m, n)` | niega toda la matriz, mismo shape |
| `(b, m, n)` | `(b, m, n)` | niega todo el tensor, conserva la forma |

```python
T = np.arange(-12, 12).reshape(2, 3, 4)   # (2, 3, 4)
np.negative(T).shape                      # (2, 3, 4)  ← shape intacto
np.negative(T)[0, 0]                       # [12, 11, 10,  9]  (eran -12..-9)
```

## Vectorización

Reemplaza un bucle Python que cambiaría el signo elemento a elemento; la versión vectorizada corre en
C sobre memoria contigua:

```python
# Bucle Python (lento):
out = np.empty_like(x)
for i in range(x.size):
    out[i] = -x[i]

# Vectorizado (un bucle en C):
out = np.negative(x)   # ≡ -x
```

## Valor de retorno

`ndarray` (o escalar de NumPy si la entrada es escalar) con la **misma shape** que `x` y, por defecto,
el mismo dtype:

| `x` dtype | salida dtype | nota |
|-----------|--------------|------|
| `int` con signo / `float` | igual | negación matemática normal |
| `uint` (sin signo) | **igual `uint`** | wrap-around modular, **no** hay negativos (ver trampa) |
| `complex` | `complex` | niega parte real e imaginaria |

```python
np.negative(np.array([1, 2, 3]))            # [-1, -2, -3]
np.negative(np.array([1.5, -2.5]))          # [-1.5,  2.5]
```

## Casos de uso

### Invertir el signo de un array (operador `-`)
```python
v = np.array([3.0, -1.0, 4.0])
-v                          # array([-3.,  1., -4.])   ≡ np.negative(v)
```

### Negar in-place sin copia (bucles de simulación)
```python
fuerza = np.random.randn(1_000_000)
np.negative(fuerza, out=fuerza)   # invierte el signo reutilizando el buffer
```

### Valor absoluto "a mano" con `where` (didáctico)
```python
x = np.array([-3, 1, -5, 2])
abs_x = x.copy()
np.negative(x, out=abs_x, where=x < 0)   # [3, 1, 5, 2]  (mejor usar np.abs)
```

### Ejemplo N-D: invertir un campo vectorial
```python
campo = np.arange(-12, 12).reshape(2, 3, 4)   # tensor (2,3,4)
np.negative(campo)   # invierte cada componente, conserva la forma (2,3,4)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `-x` con `uint8` da valores enormes | los enteros **sin signo** no tienen negativos: hay wrap-around modular (`-1 → 255`) | castear a un tipo con signo antes (`x.astype(np.int16)`) |
| posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` (p. ej. `x.copy()`) cuando se usa `where` |
| esperar que cambie la shape | es unaria: shape de salida = shape de entrada | no hay reducción ni broadcasting entre operandos |
| confundir con valor absoluto | `negative` siempre invierte el signo | usar [[np.absolute]] para magnitud |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que ejecuta el `-` unario
- [[concepto_broadcasting]] — `out`/`where` como en toda ufunc (aquí sin alinear operandos)
- [[np.subtract]] — el `-` binario · [[np.absolute]] — magnitud sin signo
- [[np.positive]] — la ufunc del `+` unario (copia con signo intacto)
