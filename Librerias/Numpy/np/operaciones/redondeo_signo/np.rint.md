---
title: np.rint — al entero más cercano (half-to-even), devuelve float (ufunc)
aliases:
  - rint
  - np.rint
tags:
  - numpy
  - api/funcion
  - transformaciones
lib: numpy
mod: np
tipo: funcion
retorna: ndarray
inplace: false
requiere:
  - concepto_ufuncs
draft: false
---

# np.rint — al entero más cercano (half-to-even), devuelve float (ufunc)

`np.rint` es una **ufunc unaria** que redondea cada elemento al **entero más cercano**, resolviendo
los empates `.5` con **redondeo bancario** (*half-to-even*): igual que [[np.round]] con `decimals=0`,
pero más directa (es la ufunc pura, sin el parámetro `decimals`). Conserva el shape y **devuelve
float**. Es la "round al entero" canónica de NumPy.

## La idea en una fórmula

Element-wise: cada elemento se redondea al entero más cercano de forma independiente, el shape no
cambia.

$$
z_i = \operatorname{round}_{\text{even}}(x_i)
\qquad\text{(empates } .5 \to \text{entero par)}
$$

Mapa de shapes (se conserva, ufunc unaria):

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{rint}\ }\ (n_0,\dots,n_k)
$$

El half-to-even en los empates `.5`:

```
x:      0.5   1.5   2.5   3.5   -0.5  -1.5
rint:   0.    2.    2.    4.    -0.   -2.
         ↑par  ↑par        ↑par        ↑par
```

## Firma

```python
np.rint(
    x,            # array_like: el tensor de entrada (real o complejo)
    /,
    out=None,     # ndarray | None: destino preasignado
    *,
    where=True,   # array_like[bool]: dónde calcular
    dtype=None,   # dtype: tipo de cómputo/salida
    casting='same_kind',
) -> ndarray
```

## Los parámetros en detalle

### `x` — el tensor de entrada
`array_like` (ndarray, lista, escalar). Acepta reales **y complejos** (redondea parte real e
imaginaria por separado). Los enteros se promueven a float y pasan sin cambios.

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida (dtype float/complex). Evita asignar memoria nueva; debe
ser compatible con la política de `casting`.

```python
buf = np.empty(3)
np.rint([0.5, 1.5, 2.5], out=buf)   # array([0., 2., 2.]); escribe en buf
```

### `where` — máscara de cálculo
`array_like` booleano broadcasteable con `x`. Solo redondea donde `where` es `True`; el resto conserva
lo que hubiera en `out`. Pasa `out` si usas `where` (ver [[concepto_ufuncs]]).

### `dtype` / `casting`
Como toda ufunc: `dtype` fuerza el tipo de cómputo/salida y `casting` controla las conversiones al
escribir en `out`. Rara vez se tocan.

## El caso N-D

`np.rint` es **element-wise**: actúa posición a posición, sin `axis` ni colapso de ejes. El shape de
la salida es idéntico al de la entrada en cualquier dimensión.

```python
M = np.array([[0.5, 1.5],
              [2.5, 3.5]])
np.rint(M)
# array([[0., 2.],
#        [2., 4.]])      half-to-even, mismo shape (2, 2)

T = np.random.rand(2, 3, 4) * 10
np.rint(T).shape          # (2, 3, 4)  → la forma se conserva
```

## Vectorización

`np.rint` reemplaza un bucle Python con `round()` por elemento; la ufunc recorre la memoria en C
respetando los `strides` (ver [[concepto_vectorizacion]]):

```python
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = round(float(arr.flat[i]))   # half-to-even también

# Vectorizado:
np.rint(arr)
```

## Valor de retorno

Devuelve un `ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** y dtype
**float** (siempre, a diferencia de `np.round`, que conserva el dtype de entrada):

| Entrada (shape, dtype) | salida (shape) | dtype salida |
|------------------------|----------------|--------------|
| `(n,)` float64 | `(n,)` | `float64` |
| `(m, n)` float32 | `(m, n)` | `float32` |
| `(n,)` int64 | `(n,)` | `float64` (promovido) |
| `(n,)` complex128 | `(n,)` | `complex128` |
| escalar `2.5` | `()` | `np.float64` (valor `2.0`) |

## Casos de uso

### Redondeo al entero más cercano (half-to-even)
```python
np.rint([0.5, 1.5, 2.5, 3.5])   # array([0., 2., 2., 4.])  ← NO [1,2,3,4]
np.rint([1.4, 1.6, -1.6])       # array([ 1.,  2., -2.])
```

### Convertir a enteros de verdad
```python
np.rint([1.4, 2.6, 3.5]).astype(int)   # array([1, 3, 4])
```

### N-D: cuantizar un tensor de valores continuos
```python
señal = np.array([[0.49, 1.51],
                  [2.50, 3.49]])     # (2, 2)
np.rint(señal)
# array([[0., 2.],
#        [2., 3.]])      → al entero más cercano, shape (2, 2)
```

## Diferencia con round / trunc / floor

| Función | Qué hace | `2.5` | `2.7` | `-2.7` | dtype salida | `decimals` |
|---------|----------|-------|-------|--------|--------------|-----------|
| `np.rint` | al más cercano, half-to-even | `2.` | `3.` | `-3.` | **siempre float** | no |
| [[np.round]] | al más cercano, half-to-even | `2.` | `3.` | `-3.` | conserva (float→float, int→int) | sí |
| [[np.trunc]] | hacia cero | `2.` | `2.` | `-2.` | siempre float | no |
| [[np.floor]] | hacia $-\infty$ | `2.` | `2.` | `-3.` | siempre float | no |

`rint` y `round(x)` (sin `decimals`) dan el **mismo valor**; la diferencia es que `rint` es la ufunc
pura (sin `decimals`) y siempre devuelve float, mientras que `round` admite `decimals` y conserva el
dtype.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `rint(2.5)` da `2`, no `3` | redondeo bancario *half-to-even* | es lo esperado; usa `np.floor(x+0.5)` para half-up |
| Esperar int y recibir float | `rint` siempre devuelve float | `.astype(int)` |
| Buscar un parámetro `decimals` | `rint` no lo tiene | usar [[np.round]] con `decimals` |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que conserva el shape
- [[np.round]] — la misma regla half-to-even, pero con `decimals` y conservando dtype
- [[np.trunc]] · [[np.floor]] · [[np.ceil]]
- [[Librerias/Numpy/np/operaciones/redondeo_signo/index\|redondeo_signo — la familia completa]]
