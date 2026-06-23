---
title: np.round — redondea al entero (o decimal) más cercano, half-to-even (ufunc)
aliases:
  - round
  - np.round
  - around
  - np.around
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

# np.round — redondea al entero (o decimal) más cercano, half-to-even (ufunc)

`np.round` (idéntico a `np.around`) redondea cada elemento al valor más cercano con el número de
decimales que pidas (`decimals`). Conserva el shape y el **mismo dtype** (float→float). La trampa
crítica, y lo que más sorprende, es que **no** usa el redondeo "de colegio" (half-up): usa
**redondeo bancario** o *half-to-even*, que en los empates `.5` redondea al entero **par** más
cercano. Por eso `round(0.5) = 0` y `round(2.5) = 2`, pero `round(1.5) = 2`.

## La idea en una fórmula

Element-wise: cada elemento se redondea de forma independiente, el shape no cambia. Con `decimals=d`
se redondea a una rejilla de paso $10^{-d}$:

$$
z_i = \frac{\operatorname{round}_{\text{even}}\!\big(x_i \cdot 10^{d}\big)}{10^{d}}
$$

donde $\operatorname{round}_{\text{even}}$ es "al entero más cercano, y en empates al **par**". Mapa
de shapes (se conserva, ufunc unaria):

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{round}\ }\ (n_0,\dots,n_k)
$$

El **half-to-even** sobre los empates `.5`:

```
x:       0.5   1.5   2.5   3.5   4.5   -0.5  -1.5  -2.5
round:   0.    2.    2.    4.    4.    -0.   -2.   -2.
                ↑ par  ↑ par  ↑ par         ↑ par  ↑ par
```

## Firma

```python
np.round(
    a,            # array_like: el tensor de entrada
    decimals=0,   # int: nº de decimales; puede ser negativo
    out=None,     # ndarray | None: destino preasignado
) -> ndarray
```

> [!note] Como ufunc subyacente
> `np.round`/`np.around` envuelven la ufunc `np.rint` (con `decimals=0`). Cuando se llama como
> ufunc directa también acepta `where`/`dtype`/`casting`, pero la firma pública expuesta es la de
> arriba.

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` (ndarray, lista, escalar), real o complejo. Para complejos redondea **parte real e
imaginaria por separado**. Los enteros se devuelven sin cambios (no hay nada que redondear).

### `decimals` — número de decimales (puede ser negativo)
El parámetro distintivo. `0` (defecto) redondea al entero. Positivo conserva decimales; **negativo**
redondea a la izquierda del punto (decenas, centenas...):

```python
np.round([3.14159, 2.71828], 2)   # array([3.14, 2.72])
np.round(3.14159, 0)              # 3.0
np.round([12, 18, 25, 49], -1)    # array([10., 20., 20., 50.])  ← a la decena
np.round(1234, -2)                # 1200  → a la centena
```
Ojo: con `decimals > 0` el resultado **no es exacto** porque los floats binarios no representan
exactamente la mayoría de decimales (`round(2.675, 2)` da `2.67`, no `2.68`).

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape de salida. Debe tener un dtype compatible con el resultado (si la
entrada es float, el `out` debe poder almacenar floats). Evita asignar memoria nueva.

## El caso N-D

`np.round` es **element-wise**: actúa posición a posición, sin `axis` ni colapso de ejes. El shape de
la salida es idéntico al de la entrada en cualquier dimensión.

```python
M = np.array([[0.5, 1.5],
              [2.5, 3.5]])
np.round(M)
# array([[0., 2.],
#        [2., 4.]])      half-to-even, mismo shape (2, 2)

T = np.random.rand(2, 3, 4)
np.round(T, 3).shape     # (2, 3, 4)  → la forma se conserva
```

## Vectorización

`np.round` reemplaza un bucle Python con `round()` por elemento (que además en Python 3 también es
half-to-even, pero interpretado paso a paso). La ufunc recorre la memoria en C
(ver [[concepto_vectorizacion]]):

```python
# Bucle Python (lento):
out = np.empty_like(arr)
for i in range(arr.size):
    out.flat[i] = round(float(arr.flat[i]), 2)

# Vectorizado:
np.round(arr, 2)
```

## Valor de retorno

Devuelve un `ndarray` (o escalar de NumPy si la entrada es escalar) con el **mismo shape** y, a
diferencia de `floor`/`rint`, **conserva el dtype** de la entrada:

| Entrada (shape, dtype) | `decimals` | salida (shape) | dtype salida |
|------------------------|-----------|----------------|--------------|
| `(n,)` float64 | `0` | `(n,)` | `float64` (sigue float, no int) |
| `(m, n)` float32 | `2` | `(m, n)` | `float32` |
| `(n,)` int64 | cualquiera | `(n,)` | `int64` (sin cambios) |
| `(n,)` complex128 | `0` | `(n,)` | `complex128` |
| escalar `2.5` | `0` | `()` | `np.float64` (valor `2.0`) |

Clave: `np.round(2.7)` es `3.0` (**float**), no `3`. Convierte con `.astype(int)` si necesitas
enteros.

## Casos de uso

### Redondeo half-to-even (la sorpresa)
```python
np.round([0.5, 1.5, 2.5, 3.5])   # array([0., 2., 2., 4.])  ← NO [1,2,3,4]
np.round([-0.5, -1.5, -2.5])     # array([-0., -2., -2.])
```

### Decimales y decimales negativos
```python
np.round([3.14159, 9.87654], 3)  # array([3.142, 9.877])
np.round([153, 248, 950], -2)    # array([200., 200., 1000.])  ← a la centena
```

### N-D: redondear una tabla de probabilidades
```python
P = np.array([[0.123, 0.877],
              [0.455, 0.545],
              [0.500, 0.500]])     # (3, 2)
np.round(P, 1)
# array([[0.1, 0.9],
#        [0.5, 0.5],
#        [0.5, 0.5]])      → cada celda a 1 decimal, shape (3, 2)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `round(2.5)` da `2`, no `3` | redondeo bancario *half-to-even* | es el comportamiento correcto; usa `np.floor(x+0.5)` si necesitas half-up |
| `round(2.675, 2)` da `2.67` | el float `2.675` no es exacto en binario | usar `decimal.Decimal` si necesitas exactitud decimal |
| Esperar int y recibir float | conserva dtype: float→float | `.astype(int)` |
| `decimals` no acepta arrays | es un escalar `int`, no por-elemento | redondear por bloques o escalar la entrada |

## Notas relacionadas

- [[concepto_ufuncs]] — el motor element-wise que conserva el shape
- [[np.rint]] — la misma idea (half-to-even) pero sin `decimals` y devolviendo siempre float
- [[np.trunc]] · [[np.floor]] · [[np.ceil]]
- [[Librerias/Numpy/np/operaciones/redondeo_signo/index\|redondeo_signo — la familia completa]]
