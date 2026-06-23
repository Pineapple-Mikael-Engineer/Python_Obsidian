---
title: np.fromfunction — construye un array evaluando una función sobre los índices
aliases:
  - fromfunction
  - np.fromfunction
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
  - concepto_shape
  - concepto_vectorizacion

draft: false
---

# np.fromfunction — construye un array evaluando una función sobre los índices

`np.fromfunction` crea un array de un `shape` dado **evaluando una función sobre los índices de cada posición**. En lugar de darle los valores, le das una **regla** que depende de las coordenadas: `fromfunction(f, (m, n))` llama a `f(I, J)`, donde `I` y `J` son las **rejillas de índices** de cada eje. El valor de la celda `(i, j)` es `f(i, j)`. Es la forma directa de fabricar patrones que dependen de la posición (tablas de sumar, tableros, gradientes, distancias) de manera [[concepto_vectorizacion|vectorizada]].

## La idea

El resultado es un tensor cuyo elemento en cada posición es la función evaluada en esa **coordenada**:

$$ A[i_0, i_1, \dots, i_{k-1}] \;=\; f(i_0, i_1, \dots, i_{k-1}) $$

La pieza no obvia: `f` **no se llama celda a celda**. NumPy genera primero, para un `shape` $(n_0,\dots,n_{k-1})$, una rejilla de índices **por cada eje** —cada una con el shape completo— y se las pasa todas juntas a `f`, que se evalúa de golpe sobre arrays:

$$ (n_0,\dots,n_{k-1}) \ \xrightarrow{\ \text{fromfunction}\ }\ f(\underbrace{I_0}_{\text{shape completo}}, \dots, \underbrace{I_{k-1}}_{\text{shape completo}}) $$

Por eso `f` debe escribirse de forma **vectorizada** (operar sobre arrays), no asumir escalares. El número de argumentos que recibe `f` es exactamente `len(shape)` (un array de índices por dimensión).

## Firma

```python
np.fromfunction(
    function,      # callable: recibe ndim arrays de índices, devuelve los valores
    shape,         # tuple[int]: forma del array de salida
    *,
    dtype=float,   # dtype: tipo de los arrays de ÍNDICES que se pasan a function
    **kwargs,      # se reenvían a function
) -> ndarray
```

## Los parámetros en detalle

### `function` — la regla sobre los índices

Callable que recibe `len(shape)` arrays de índices (uno por eje) y devuelve el array de valores. Cada array de índices tiene el **shape completo** de salida y contiene el índice de su eje:

```python
# Para shape (2, 3), function recibe DOS arrays, ambos de shape (2, 3):
#   i = [[0, 0, 0],      j = [[0, 1, 2],
#        [1, 1, 1]]           [0, 1, 2]]
# y el resultado es function(i, j), evaluado de una vez sobre esos arrays.
```

Debe ser vectorizable: usa operaciones de NumPy (`+`, `%`, `np.sqrt`, `==`...), no `if` sobre escalares.

### `shape` — forma del array de salida

Tupla `(n_0, ..., n_{k-1})`. Determina tanto el shape del resultado como **cuántos arrays de índices** recibe `function` (uno por dimensión). Ver [[concepto_shape]].

### `dtype` — tipo de los arrays de índices

Tipo de las rejillas de índices que se pasan a `function` (por defecto `float`). Casi siempre conviene `int`, porque los índices son enteros y muchas operaciones (`%`, indexado, `==`) esperan enteros.

```python
np.fromfunction(lambda i, j: i + j, (3, 3))            # índices float → suma 0.0, 1.0...
np.fromfunction(lambda i, j: i + j, (3, 3), dtype=int) # índices int   → 0, 1, 2... (lo habitual)
```

### `**kwargs` — argumentos extra para `function`

Cualquier keyword adicional se reenvía a `function` (rara vez necesario).

## El caso N-D

La regla escala a cualquier dimensión: para un `shape` de `k` ejes, `function` recibe `k` rejillas de índices `f(I_0, ..., I_{k-1})`, y el valor de cada celda es la función de sus `k` coordenadas. Veamos un ejemplo **3-D**, una "tabla de sumar tridimensional" `i + j + k`:

```python
# shape (2, 3, 4): function recibe TRES arrays de índices, cada uno de shape (2, 3, 4)
suma3d = np.fromfunction(lambda i, j, k: i + j + k, (2, 3, 4), dtype=int)
suma3d.shape   # (2, 3, 4)
suma3d
# array([[[0, 1, 2, 3],
#         [1, 2, 3, 4],
#         [2, 3, 4, 5]],
#
#        [[1, 2, 3, 4],
#         [2, 3, 4, 5],
#         [3, 4, 5, 6]]])
```

Lectura: el elemento `suma3d[1, 2, 3]` vale `1 + 2 + 3 = 6` (la esquina final). Cada uno de los tres arrays de índices `i`, `j`, `k` tiene shape `(2, 3, 4)`:

$$ A[i, j, k] = i + j + k, \qquad (i,j,k) \in \{0,1\}\times\{0,1,2\}\times\{0,1,2,3\} $$

El mismo principio sirve en 4-D y más: `np.fromfunction(lambda a, b, c, d: ..., (n0, n1, n2, n3))` recibiría cuatro rejillas. La función se evalúa **una sola vez** sobre arrays del shape completo, no $n_0 n_1 n_2 n_3$ veces.

## Casos de uso

### Tabla de sumar (índices `i + j`)

```python
np.fromfunction(lambda i, j: i + j, (3, 3), dtype=int)
# array([[0, 1, 2],
#        [1, 2, 3],
#        [2, 3, 4]])
```

### Tablero de ajedrez (`(i + j) % 2`)

```python
np.fromfunction(lambda i, j: (i + j) % 2, (8, 8), dtype=int)
# patrón 0/1 alternado, como un tablero
```

### Matriz identidad booleana (`i == j`)

```python
np.fromfunction(lambda i, j: i == j, (3, 3), dtype=int)
# diagonal True, resto False  (equivale a np.eye(3, dtype=bool))
```

### Distancias al origen

```python
np.fromfunction(lambda i, j: np.sqrt(i**2 + j**2), (5, 5))
# distancia euclídea de cada celda a (0, 0)
```

### Gradiente lineal (solo depende de una coordenada)

```python
np.fromfunction(lambda i, j: j, (4, 4), dtype=int)
# cada columna es constante: rampa horizontal 0,1,2,3
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `function` falla con arrays | se escribió asumiendo escalares (`if`, `math.sqrt`) | vectorizar: usar ops de NumPy (`np.where`, `np.sqrt`) |
| Índices flotantes inesperados | `dtype` por defecto es `float` | pasar `dtype=int` |
| `f` recibe menos/más args de los esperados | nº de argumentos ≠ `len(shape)` | la función debe tomar **un argumento por eje** |
| Resultado constante donde se esperaba variación | la función ignora alguna coordenada | usar todos los índices que se necesiten (`i`, `j`, `k`...) |
| Lentitud con lógica compleja | función Python no vectorizable | construir con operaciones de array directas |

## Notas relacionadas

- [[concepto_shape]] — el shape decide cuántas rejillas de índices recibe la función
- [[concepto_vectorizacion]] — por qué `function` se evalúa de una vez sobre arrays, no celda a celda
- [[np.indices]] — genera explícitamente las rejillas de índices que `fromfunction` pasa a la función
- [[np.meshgrid]] · [[np.full]] · [[np.eye]] · [[np.arange]]
