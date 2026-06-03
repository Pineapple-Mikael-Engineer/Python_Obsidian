---
title: scipy.linalg.norm — norma de vector o matriz segun ord
aliases:
  - norm
  - scipy.linalg.norm
  - norma vectorial
  - norma matricial
tags:
  - scipy
  - api/funcion
  - algebra-lineal
lib: scipy
tipo: funcion
mod: scipy.linalg
retorna: float
requiere:
  - numpy
  - concepto_relacion_numpy
draft: false
---

# scipy.linalg.norm — norma de vector o matriz segun ord

Calcula una **norma** de un array, interpretado como **vector** (1D) o como **matriz** (2D). El tipo de norma lo fija `ord`, cuyo significado **cambia segun la dimension del array**: el mismo `ord` mide cosas distintas en vector y en matriz. Por defecto devuelve un `float`; si se pasa `axis`, devuelve un `ndarray` con las normas a lo largo de ese eje.

Sirve para cuantificar magnitud o distancia: tamaño de un **residuo** `‖A·x − b‖`, **condicionamiento** de un sistema, terminos de **regularizacion** (L1, L2) y errores entre soluciones.

## Firma

```python
scipy.linalg.norm(
    a,                  # array_like: vector (1D) o matriz (2D)
    ord=None,           # {None, 'fro', 'nuc', int, inf, -inf}: tipo de norma
    axis=None,          # None | int | tuple: eje(s) sobre los que normar
    keepdims=False,     # bool: conservar dimensiones reducidas
    check_finite=True   # bool: validar que no haya NaN/inf antes de calcular
) -> float | ndarray
```

## Valor de retorno

| Entrada | `axis` | Retorno |
|---------|--------|---------|
| Vector o matriz | `None` | `float` (una sola norma) |
| Matriz 2D | `int` | `ndarray` 1D (norma por fila/columna) |
| ndarray | `tuple` de 2 | `ndarray` (norma matricial por bloques) |

```python
import numpy as np
from scipy.linalg import norm

norm(np.array([3.0, 4.0]))   # → 5.0   (euclidea, ord=2 por defecto en vector)
```

## Significado de `ord` (vector vs matriz)

| `ord` | Vector (`a` es 1D) | Matriz (`a` es 2D) |
|-------|--------------------|--------------------|
| `None` | norma 2 (euclidea) | Frobenius (raiz de Σ aij²) |
| `'fro'` | — (no valido) | Frobenius |
| `'nuc'` | — (no valido) | nuclear (suma de valores singulares) |
| `2` | euclidea `sqrt(Σ x²)` | norma espectral (mayor valor singular) |
| `1` | taxicab `Σ |x|` | maxima suma absoluta de **columna** |
| `np.inf` | maximo `|x|` | maxima suma absoluta de **fila** |
| `-np.inf` | minimo `|x|` | minima suma absoluta de fila |
| `-1` | `1 / Σ(1/|x|)` (raro) | minima suma absoluta de columna |
| `-2` | menor `|x|` invertido (raro) | menor valor singular |
| `0` | numero de elementos **no nulos** | — (no valido) |

> [!note] El mismo `ord` no es la misma norma
> `ord=1` en un vector suma valores absolutos; `ord=1` en una matriz toma la maxima suma de columnas. `ord=2` en vector es la longitud euclidea; en matriz es la norma espectral (un SVD, mas caro). Siempre piensa primero si `a` es 1D o 2D.

## Formas basicas de llamada

| Objetivo | Llamada |
|----------|---------|
| Longitud euclidea de un vector | `norm(v)` |
| Norma 1 (taxicab) de vector | `norm(v, 1)` |
| Maximo absoluto de vector | `norm(v, np.inf)` |
| Conteo de no-ceros | `norm(v, 0)` |
| Frobenius de matriz | `norm(M)` o `norm(M, 'fro')` |
| Norma espectral de matriz | `norm(M, 2)` |
| Norma de cada fila | `norm(M, axis=1)` |
| Norma de cada columna | `norm(M, axis=0)` |

## Parametros en detalle

### `a` (obligatorio)

El array a medir. Si es **1D** se trata como vector; si es **2D**, como matriz. La interpretacion de `ord` depende de esto.

```python
import numpy as np
from scipy.linalg import norm

v = np.array([1.0, -2.0, 2.0])
norm(v)          # → 3.0          (euclidea: sqrt(1+4+4))
norm(v, 1)       # → 5.0          (taxicab: 1+2+2)
norm(v, np.inf)  # → 2.0          (maximo absoluto)
norm(v, 0)       # → 3.0          (no-ceros)
```

### `ord`

Selecciona la norma segun la tabla anterior. En matrices, `2` y `'nuc'` requieren un **SVD** (costoso); `1`, `np.inf` y `'fro'` son baratas.

```python
M = np.array([[1.0, 2.0],
              [3.0, 4.0]])
norm(M)           # → 5.4772...   Frobenius (sqrt(1+4+9+16))
norm(M, 2)        # → 5.4649...   espectral (mayor valor singular)
norm(M, 1)        # → 6.0         max suma de columna (|2|+|4|)
norm(M, np.inf)   # → 7.0         max suma de fila (|3|+|4|)
```

### `axis`

Permite calcular **muchas normas a la vez** sobre un eje. Con `axis=1` obtienes la norma de cada fila; con `axis=0`, de cada columna. El retorno pasa a ser un `ndarray`.

```python
M = np.array([[3.0, 4.0],
              [6.0, 8.0]])
norm(M, axis=1)   # → [ 5., 10.]   norma de cada fila
norm(M, axis=0)   # → [6.7082, 8.9442]   norma de cada columna
```

### `keepdims`

Si `True`, el eje reducido se conserva con tamaño 1; util para **dividir por la norma** con broadcasting (normalizar filas).

```python
filas = M / norm(M, axis=1, keepdims=True)   # cada fila queda con norma 1
```

### `check_finite`

Por defecto `True`: valida que no haya `NaN`/`inf`. Ponerlo en `False` ahorra esa comprobacion cuando los datos ya son confiables, ganando algo de velocidad.

## Casos de uso

### Residuo de un sistema lineal

```python
import numpy as np
from scipy.linalg import norm, solve

A = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([9.0, 8.0])
x = solve(A, b)
residuo = norm(A @ x - b)    # → ~0.0   ‖Ax - b‖, mide calidad de la solucion
```

### Numero de condicion (estabilidad)

```python
# cond(A) = ‖A‖ · ‖A^{-1}‖ con norma espectral indica sensibilidad del sistema
from scipy.linalg import inv
cond = norm(A, 2) * norm(inv(A), 2)
cond     # → grande => mal condicionado (la solucion amplifica errores)
```

### Error entre dos soluciones / regularizacion

```python
x_aprox = np.array([1.01, 1.98])
x_exact = np.array([1.00, 2.00])
err  = norm(x_aprox - x_exact)        # error L2 absoluto
rel  = norm(x_aprox - x_exact) / norm(x_exact)   # error relativo
pen  = norm(x_aprox, 1)               # penalizacion L1 (regularizacion tipo Lasso)
```

## Buenas practicas

1. Identifica primero si `a` es vector o matriz: define que mide cada `ord`.
2. Para error **relativo** divide entre la norma del valor de referencia, no solo el absoluto.
3. Usa `axis` + `keepdims=True` para normalizar filas/columnas por broadcasting en un paso.
4. Evita `ord=2`/`'nuc'` en matrices grandes si basta `'fro'`: el SVD es mas caro.
5. Esta `norm` es el analogo en SciPy de la de NumPy; prefierela en codigo numerico serio por consistencia con el resto de `scipy.linalg`, como se explica en la relacion entre ambas librerias.

## Errores comunes

| Error | Causa | Solucion |
|-------|-------|----------|
| Norma matricial inesperada | Se uso `ord` de vector sobre matriz 2D | Revisar la tabla vector vs matriz |
| `ValueError: Invalid norm order` | `ord='nuc'`/`'fro'` sobre vector 1D | Solo validos en matrices |
| `0` no cuenta lo esperado | `ord=0` solo cuenta no-ceros, no es L0 real | Es el conteo de entradas distintas de cero |
| Resultado escalar cuando se queria por fila | Falto `axis` | Pasar `axis=1` (filas) o `axis=0` (columnas) |
| Broadcasting falla al normalizar | Norma colapso la dimension | Usar `keepdims=True` |
| `NaN` propagado silenciosamente | `check_finite=False` con datos sucios | Dejar `check_finite=True` o limpiar antes |

## Limitaciones

- Solo distingue **vector (1D)** y **matriz (2D)**; para tensores de mas ejes usa `axis` explicito o `numpy.linalg.norm`.
- Las normas matriciales `2`, `-2` y `'nuc'` implican un SVD: costosas en matrices grandes.
- No calcula normas de operadores en formato disperso; para eso usar utilidades de `scipy.sparse.linalg`.
- `ord=0` no es una norma matematica (no homogenea); es solo un conteo de no-ceros conveniente.

## Notas relacionadas

- [[scipy.linalg.solve]]
- [[scipy.linalg.inv]]
- [[scipy.linalg.svd]]
- [[concepto_relacion_numpy]]
