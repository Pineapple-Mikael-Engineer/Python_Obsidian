---
title: ufuncs — Universal Functions (el motor element-wise)
aliases:
  - ufunc
  - universal function
  - funciones universales
tags:
  - numpy
  - concepto
  - ufuncs
  - rendimiento
lib: numpy
tipo: concepto
requiere:
  - concepto_ndarray
  - concepto_vectorizacion
  - concepto_broadcasting
draft: false
---

# ufuncs — Universal Functions (el motor element-wise)

## Definición fundamental

Una **ufunc** (Universal Function) es una **función compilada en C que opera elemento a elemento** sobre [[concepto_ndarray|arrays de NumPy]], aplicando [[concepto_broadcasting|broadcasting]] automático y promoción de tipos. `np.add`, `np.sin`, `np.exp` o `np.greater` son ufuncs.

Es el motor real de la [[concepto_vectorizacion|vectorización]]: el bucle sobre los elementos vive dentro de la ufunc, no en Python. Los operadores `+ - * /` son **azúcar sintáctico** sobre ufuncs: `a + b` invoca `np.add(a, b)`.

## Por qué existen

Sin ufuncs, aplicar una operación matemática a un array exigiría un bucle Python, lento porque interpreta cada paso:

```python
# Bucle Python (lento: interpreta n veces)
out = np.empty_like(arr)
for i in range(arr.size):
    out[i] = math.sin(arr[i])

# ufunc (un único bucle en C, con broadcasting)
out = np.sin(arr)
```

La ufunc recorre los datos en C, respeta los `strides` del array y aplica broadcasting sin materializar formas intermedias.

## La regla / el modelo central

Una ufunc se caracteriza por su número de entradas (`nin`) y salidas (`nout`), y aplica la misma operación a cada posición tras alinear las formas con broadcasting:

$$ z_{i_0\dots i_k} = f\big(x_{i_0\dots i_k},\ y_{i_0\dots i_k}\big) $$

donde los índices recorren la **shape común** resultante del broadcasting de las entradas. La salida tiene esa shape común; el `dtype` sale de las reglas de promoción (ver [[concepto_dtype|sistema de dtypes]]).

### Clasificación por aridad

| Tipo | `nin` | Ejemplos |
|------|-------|----------|
| Unarias | 1 | `np.sin`, `np.log`, `np.exp`, `np.absolute` |
| Binarias | 2 | `np.add`, `np.multiply`, `np.power`, `np.greater` |
| "Ternarias" | 3 | `np.clip` (en la práctica; `np.where` no es ufunc) |

## Parámetros comunes de toda ufunc

Toda ufunc acepta un puñado de parámetros que controlan **dónde** escribe, **sobre qué** elementos opera y **con qué tipo**:

| Parámetro | Qué hace | Cuándo importa |
|-----------|----------|----------------|
| `out=` | Escribe el resultado en un array existente (incluso el de entrada → in-place) | Reutilizar memoria, evitar arrays temporales |
| `where=` | Máscara booleana: solo calcula donde es `True`; el resto conserva el valor previo de `out` | Aplicación condicional sin indexar |
| `dtype=` | Fuerza el tipo de cómputo/salida | Controlar precisión o evitar overflow del acumulador |
| `casting=` | Política de conversión permitida: `'no'`, `'equiv'`, `'safe'`, `'same_kind'`, `'unsafe'` | Bloquear conversiones con pérdida |

```python
arr = np.random.rand(1_000_000)

# out: reutiliza memoria, sin asignación extra
buf = np.empty_like(arr)
np.sin(arr, out=buf)

# out + where: solo recalcula los elementos > 0.5
mascara = arr > 0.5
np.sin(arr, out=arr, where=mascara)   # los <= 0.5 quedan intactos

# dtype + casting: fuerza float32 y prohíbe perder precisión
np.multiply(arr, 2, dtype=np.float32, casting='same_kind')
```

> [!warning] `where` necesita un `out` definido
> Donde `where` es `False`, el resultado conserva lo que hubiera en `out`. Si no pasas `out`, esas posiciones quedan **sin inicializar** (basura). Con `where` casi siempre se pasa `out` explícito.

## Los métodos de una ufunc (lo que suele faltar)

Las ufuncs **binarias** exponen métodos que reutilizan la operación para reducir, acumular o expandir un array. Son el corazón "oculto" de NumPy: `np.sum` es `np.add.reduce`, `np.cumsum` es `np.add.accumulate`.

| Método | Equivale a | Mapa de shapes |
|--------|-----------|----------------|
| `reduce(a, axis)` | reducir un eje (`np.sum`, `np.prod`...) | colapsa el eje reducido |
| `accumulate(a, axis)` | sumas/productos parciales (`np.cumsum`, `np.cumprod`) | conserva la shape |
| `reduceat(a, idx)` | reduce por segmentos `[idx[i]:idx[i+1])` | `(n,) → (len(idx),)` |
| `outer(a, b)` | combina **cada** par `(a_i, b_j)` | `a.shape + b.shape` |
| `at(a, idx, b)` | aplica in-place en índices (con repetidos) | modifica `a`, no retorna |

### `reduce` — colapsa un eje

```python
a = np.array([1, 2, 3, 4])
np.add.reduce(a)               # 1+2+3+4 = 10   (≡ np.sum)
np.multiply.reduce(a)          # 1*2*3*4 = 24   (≡ np.prod)

m = np.array([[1, 2, 3],
              [4, 5, 6]])
np.add.reduce(m, axis=0)       # [5, 7, 9]   colapsa el eje 0
```

Mapa de shapes (idéntico al de [[concepto_axis_parametro|axis]]):
$$ (n_0,\dots,n_k)\ \xrightarrow{\ \text{reduce, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k) $$

### `accumulate` — resultados parciales (≡ cumsum)

```python
a = np.array([1, 2, 3, 4])
np.add.accumulate(a)           # [1, 3, 6, 10]   (≡ np.cumsum)
np.multiply.accumulate(a)      # [1, 2, 6, 24]   (≡ np.cumprod)
```

### `reduceat` — reducir por segmentos

Para índices `idx`, reduce cada tramo `a[idx[i] : idx[i+1])` (el último llega hasta el final):

```python
a = np.array([1, 2, 3, 4, 5, 6])
np.add.reduceat(a, [0, 2, 4])  # [3, 7, 11]
# tramos: a[0:2]=1+2=3, a[2:4]=3+4=7, a[4:]=5+6=11
```

### `outer` — combinar todos los pares

`outer(a, b)` aplica la ufunc a **cada** par `(a_i, b_j)`, expandiendo las formas. Es el caso general del producto externo:

$$ (n_0,\dots,n_{p-1}),\ (m_0,\dots,m_{q-1})\ \xrightarrow{\ \text{outer}\ }\ (n_0,\dots,n_{p-1},\,m_0,\dots,m_{q-1}) $$

con la celda $C_{i_0\dots i_{p-1},\,j_0\dots j_{q-1}} = f\big(a_{i_0\dots i_{p-1}},\, b_{j_0\dots j_{q-1}}\big)$.

```python
a = np.array([1, 2, 3])        # (3,)
b = np.array([10, 20, 30])     # (3,)

np.multiply.outer(a, b)        # (3,) + (3,) → (3, 3)  tabla de multiplicar
# [[10, 20, 30],
#  [20, 40, 60],
#  [30, 60, 90]]

np.add.outer(a, b)             # cada suma a_i + b_j
# [[11, 21, 31],
#  [12, 22, 32],
#  [13, 23, 33]]
```

Ejemplo N-D del mapa de shapes: con `a.shape = (2, 3)` y `b.shape = (4,)`, `np.multiply.outer(a, b).shape == (2, 3, 4)`.

### `at` — operación in-place con índices repetidos

A diferencia de `a[idx] += b`, `np.add.at` **acumula** correctamente cuando un índice se repite:

```python
a = np.zeros(5)
np.add.at(a, [0, 2, 2, 4], 1)  # el índice 2 se incrementa DOS veces
a                              # [1., 0., 2., 0., 1.]
```

## Casting y promoción de tipos

Las ufuncs promueven al tipo más general entre las entradas (ver [[concepto_dtype|sistema de dtypes]]): `int + float → float`. El parámetro `casting` controla qué conversiones se permiten.

```python
i = np.array([1, 2, 3], dtype=np.int32)
f = np.array([0.5, 1.5, 2.5], dtype=np.float32)
np.add(i, f).dtype             # float64 (promoción)

# casting='no' prohíbe convertir el float
np.add(i, 0.5, casting='no')   # TypeError: Cannot cast ufunc input...
```

> [!warning] `out` con dtype incompatible
> Si `out` tiene un dtype que la política de `casting` no permite, la ufunc lanza error en vez de truncar silenciosamente. Ej.: escribir `np.add(f, f, out=int_array)` con el `casting` por defecto (`'same_kind'`) falla porque `float → int` no es seguro.

## Crear ufuncs propias

| Vía | Velocidad | Uso |
|-----|-----------|-----|
| ufunc nativa | 1× (referencia) | siempre que exista |
| `np.frompyfunc` | ~10–50× más lenta | prototipado; retorna `object` |
| `np.vectorize` | ~50–100× más lenta | comodidad + broadcasting, no rendimiento |

```python
def f(x, y):
    return x**2 + y**2

uf = np.frompyfunc(f, 2, 1)    # retorna dtype object (no optimizado)
np.vectorize(f, otypes=[np.float64])(np.array([1, 2]), np.array([3, 4]))
```

> [!note] `np.vectorize` no acelera
> Es un envoltorio cómodo (firma, broadcasting) pero el bucle sigue en Python. Cuando importa la velocidad, hay que componer ufuncs nativas, no vectorizar funciones Python.

## Casos que fallan

| Error | Causa | Solución |
|-------|-------|----------|
| `'numpy.ufunc' object has no attribute 'reduce'` falla en unarias | `reduce`/`accumulate`/`outer` necesitan una ufunc **binaria** (asociativa) | usar `np.add`, `np.multiply`...; no `np.sin.reduce` |
| `Cannot cast ufunc output` | `out` con dtype incompatible bajo la política `casting` | ajustar `out` o pasar `casting='unsafe'` conscientemente |
| posiciones con basura tras `where` | `where=` sin `out` inicializado | pasar siempre `out=` cuando se usa `where=` |
| `reduceat` da tramos inesperados | el último índice reduce hasta el final del array, no un tramo fijo | revisar la convención de segmentos `[idx[i]:idx[i+1])` |

## Relación con otros conceptos

- [[concepto_vectorizacion]] — la ufunc es lo que hace que la vectorización sea rápida.
- [[concepto_broadcasting]] — toda ufunc alinea sus entradas con broadcasting.
- [[concepto_ndarray]]
- [[concepto_dtype]]
- [[concepto_axis_parametro]]
- [[np.frompyfunc]]
- [[np.vectorize]]
