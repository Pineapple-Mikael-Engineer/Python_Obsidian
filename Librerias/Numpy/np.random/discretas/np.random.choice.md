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
retorna: ndarray | Any
inplace: false
requiere:
  - concepto_shape
draft: false
---

# np.random.choice — Muestreo aleatorio de un array

Selecciona elementos al azar de un array `a` (o de `arange(a)` si `a` es un entero). Es la función de muestreo más versátil de NumPy: muestrea **con o sin reemplazo** y con **probabilidades por elemento**. Cubre desde el barajado de una selección hasta el remuestreo con reposición (bootstrap) y el muestreo ponderado.

## La idea

Dada una población $a = (a_0, a_1, \dots, a_{N-1})$ de tamaño $N$, cada extracción elige el elemento $a_i$ con probabilidad $p_i$. Sin `p`, la distribución es **uniforme** ($p_i = 1/N$); con `p`, es la categórica que tú definas:

$$ P(\text{extraer } a_i) = p_i, \qquad \sum_{i=0}^{N-1} p_i = 1 $$

El parámetro `replace` decide si las extracciones son **independientes** (`True`, con reposición, puede repetir) o **sin reposición** (`False`, cada elemento sale como máximo una vez). Para enteros uniformes sin una población explícita, [[np.random.randint]] suele ser más directo.

## Firma

```python
np.random.choice(
    a,              # int | array_like 1D: población (o arange(a) si es int)
    size=None,      # int | tuple[int] | None: forma de la salida
    replace=True,   # bool: con reposición (True) o sin ella (False)
    p=None,         # array_like[float] | None: probabilidades por elemento
) -> ndarray | Any
```

## Los parámetros en detalle

### `a` — población a muestrear

Si es un **array/lista 1D**, muestrea de sus elementos (de cualquier dtype: enteros, floats, strings). Si es un **entero `n`**, muestrea de `arange(n)`, equivalente a `[0, n)`.

```python
np.random.choice([100, 200, 300])  # de la lista
np.random.choice(10)               # de 0..9, como un randint
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]]. `None` devuelve un **único elemento** (escalar, no array).

```python
np.random.choice(52, size=(2, 5))  # repartir cartas en shape (2, 5)
```

### `replace` — con o sin reemplazo

`True` (defecto) permite **repetir** elementos: cada extracción es independiente. `False` los toma **sin repetición**, por lo que `size` no puede superar el tamaño de la población.

```python
np.random.choice(5, size=5, replace=False)  # permutación de 0..4
np.random.choice(5, size=3, replace=False)  # 3 distintos
```

### `p` — probabilidades por elemento

Array de pesos que debe **sumar 1** (con tolerancia numérica) y tener la **misma longitud** que la población. Habilita el muestreo sesgado; sin él, todos los elementos son equiprobables.

```python
np.random.choice(['cara', 'cruz'], size=10, p=[0.9, 0.1])  # moneda sesgada
```

## size y la forma de salida

`size` se traslada literalmente al shape de salida; cada celda se rellena con un elemento de `a`:

$$ \texttt{size}=(n_0, \dots, n_{k-1}) \;\longrightarrow\; \texttt{shape} = (n_0, \dots, n_{k-1}), \quad \text{con valores en } a $$

```python
np.random.choice(10, size=(2, 3, 4, 5)).shape      # (2, 3, 4, 5)    → 4D de enteros 0..9
np.random.choice(['a','b'], size=(2,3,4,5,6)).shape # (2, 3, 4, 5, 6) → 5D de strings
```

Con `replace=False`, el **total** de extracciones (`prod(size)`) no puede superar `len(a)`, aunque `size` sea multidimensional.

## Casos de uso

### Muestra aleatoria de filas con reposición (bootstrap)

```python
datos = np.arange(100).reshape(20, 5)
idx = np.random.choice(datos.shape[0], size=20, replace=True)  # con reemplazo
bootstrap = datos[idx]   # remuestreo bootstrap de las 20 filas
```

### Selección sin reemplazo (sorteo)

```python
participantes = np.array(['Ana', 'Luis', 'Eva', 'Sam', 'Tom'])
ganadores = np.random.choice(participantes, size=2, replace=False)  # 2 distintos
```

### Muestreo ponderado por probabilidad

```python
clases = np.array([0, 1, 2])
pesos = np.array([0.7, 0.2, 0.1])
etiquetas = np.random.choice(clases, size=1000, p=pesos)
np.bincount(etiquetas) / 1000   # ≈ [0.7, 0.2, 0.1]
```

> [!tip] Versión moderna: `rng.choice`
> La API recomendada desde NumPy 1.17 usa un `Generator` de [[np.random.default_rng]] con el método **`rng.choice`**, de firma casi idéntica pero con un extra importante: **`axis`**, que permite muestrear **filas o columnas** de un array N-D (la clásica solo acepta poblaciones 1D), y `shuffle=False` para conservar el orden cuando `replace=False`.
> ```python
> rng = np.random.default_rng(0)
> rng.choice(5, size=3, replace=False)              # 3 enteros distintos de 0..4
> rng.choice(matriz, size=10, axis=0)               # 10 filas de un array 2D
> rng.choice(['a','b','c'], size=4, p=[.2,.3,.5])   # muestreo ponderado
> ```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: Cannot take a larger sample than population` | `size > len(a)` con `replace=False` | reducir `size` o usar `replace=True` |
| `ValueError: probabilities do not sum to 1` | `p` mal normalizado | dividir `p` por `p.sum()` |
| `ValueError: a and p must have same size` | longitudes distintas | igualar tamaños de `a` y `p` |
| Repetidos inesperados | `replace=True` por defecto | pasar `replace=False` |
| Muestrear filas falla | la clásica solo acepta `a` 1D | usar `rng.choice(..., axis=0)` |

## Notas relacionadas

- [[concepto_shape]] — `size` define la forma de salida
- [[np.random.default_rng]] — `rng.choice`, el reemplazo moderno con `axis`
- [[np.random.randint]] — enteros uniformes sin población explícita
- [[np.random.permutation]] · [[np.random.binomial]] · [[np.random.poisson]]
