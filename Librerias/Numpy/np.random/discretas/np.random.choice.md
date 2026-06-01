---
title: np.random.choice — Muestreo aleatorio de un array
aliases:
  - choice
  - random.choice
  - np.random.choice
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o int
inplace: false
draft: false
---

# np.random.choice — Muestreo aleatorio de un array

Selecciona elementos al azar de un array (o de `arange(a)` si `a` es un entero). Es la función de muestreo más versátil de NumPy: permite muestrear **con o sin reemplazo** y con **probabilidades por elemento**. Cubre desde barajar selecciones hasta muestreos ponderados.

## Firma de la función

```python
np.random.choice(
    a,
    size=None,
    replace=True,
    p=None
) -> ndarray | Any
```

## Valor de retorno

Devuelve un elemento (si `size=None`) o un [[concepto_ndarray|ndarray]] con el [[concepto_shape|shape]] de `size`, formado por elementos tomados de `a`.

| Llamada | Significado | Retorno |
|---------|-------------|---------|
| `np.random.choice(5)` | un valor de `arange(5)` | `int` en 0..4 |
| `np.random.choice([10, 20, 30])` | un elemento de la lista | `10`, `20` o `30` |
| `np.random.choice(5, size=3)` | 3 valores (con repetición) | `ndarray` shape `(3,)` |
| `np.random.choice(5, size=3, replace=False)` | 3 distintos | `ndarray` sin repetidos |
| `np.random.choice(3, p=[0.1, 0.1, 0.8])` | muestreo ponderado | casi siempre `2` |

```python
import numpy as np
np.random.choice(['a', 'b', 'c'], size=5)
# array(['c', 'a', 'c', 'b', 'a'], dtype='<U1')
```

## Parámetros en detalle

### `a` — población a muestrear

Si es un **array/lista 1D**, muestrea de sus elementos. Si es un **entero `n`**, muestrea de `arange(n)` (equivale a `[0, n)`).

```python
np.random.choice([100, 200, 300])  # de la lista
np.random.choice(10)               # de 0..9, como un randint
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]]. `None` devuelve un único elemento (no array).

```python
np.random.choice(52, size=(2, 5))  # repartir cartas en shape (2, 5)
```

### `replace` — con o sin reemplazo

`True` (defecto) permite repetir elementos; `False` los toma **sin repetición** (no puede pedir más que el tamaño de la población).

```python
np.random.choice(5, size=5, replace=False)  # permutación de 0..4
np.random.choice(5, size=3, replace=False)  # 3 distintos
```

### `p` — probabilidades por elemento

Array de pesos que debe **sumar 1** y tener la misma longitud que la población. Habilita muestreo sesgado.

```python
np.random.choice(['cara', 'cruz'], size=10, p=[0.9, 0.1])  # moneda sesgada
```

## Casos de uso

### Muestra aleatoria de filas (bootstrap)

```python
datos = np.arange(100).reshape(20, 5)
idx = np.random.choice(datos.shape[0], size=20, replace=True)  # con reemplazo
bootstrap = datos[idx]
```

### Selección sin reemplazo (sorteo)

```python
participantes = np.array(['Ana', 'Luis', 'Eva', 'Sam', 'Tom'])
ganadores = np.random.choice(participantes, size=2, replace=False)
```

### Muestreo ponderado por probabilidad

```python
clases = np.array([0, 1, 2])
pesos = np.array([0.7, 0.2, 0.1])
etiquetas = np.random.choice(clases, size=1000, p=pesos)
np.bincount(etiquetas) / 1000   # ≈ [0.7, 0.2, 0.1]
```

## Buenas prácticas

1. Con `replace=False`, `size` no puede superar el tamaño de la población.
2. `p` debe sumar 1 (con tolerancia numérica) y alinear con la longitud de `a`.
3. Para muestrear **enteros uniformes** sin una población explícita, [[np.random.randint]] suele ser más directo.
4. Para barajar un array completo in-place, considera `np.random.shuffle` o `np.random.permutation`.
5. Fija la semilla para reproducibilidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: Cannot take a larger sample than population` | `size > len(a)` con `replace=False` | reducir `size` o usar `replace=True` |
| `ValueError: probabilities do not sum to 1` | `p` mal normalizado | dividir `p` por `p.sum()` |
| `ValueError: a and p must have same size` | longitudes distintas | igualar tamaños de `a` y `p` |
| Repetidos inesperados | `replace=True` por defecto | pasar `replace=False` |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.randint]]
- [[np.random.binomial]]
- [[np.random.poisson]]
