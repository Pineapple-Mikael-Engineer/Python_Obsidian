---
title: np.bincount — cuenta ocurrencias de enteros no negativos
aliases:
  - bincount
  - np.bincount
tags:
  - numpy
  - api/funcion
  - estadistica

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.bincount — cuenta ocurrencias de enteros no negativos

`np.bincount` cuenta cuántas veces aparece cada **entero no negativo** en un array 1D. El resultado es un vector donde la posición `i` guarda el número de veces que aparece el valor `i`: `bincount(x)[i]` = nº de ocurrencias de `i`. Es el conteo de frecuencias más directo de NumPy cuando los datos ya son enteros pequeños y consecutivos — no hay que definir bins porque **el valor es su propio índice**. La idea en una frase: tabla de frecuencias donde el índice es el dato.

## La idea

Para un array `x` de enteros $\ge 0$, la salida es un vector `out` de longitud $\max(x)+1$ definido por:

$$ \text{out}_i \;=\; \#\{\, j : x_j = i \,\}, \qquad i = 0, 1, \dots, \max(x) $$

A diferencia de [[np.histogram]], aquí no hay bordes ni intervalos: cada entero `i` es **su propio bin**, y los enteros entre `0` y `max(x)` que no aparecen quedan con conteo `0` (no se saltan). El mapa de shapes colapsa un array de longitud `N` a un vector indexado por valor, cuya longitud la fija el **máximo** de los datos, no `N`:

$$ x\ \text{de shape}\ (N,)\ \text{con}\ x_j \ge 0 \ \xrightarrow{\ \text{bincount}\ }\ \text{out de shape}\ (\max(x)+1,) $$

## Firma

```python
np.bincount(
    x,                 # array_like 1D de enteros NO negativos
    weights=None,      # array_like | None: peso de cada elemento (mismo largo que x)
    minlength=0,       # int: longitud mínima de la salida (rellena con ceros)
) -> ndarray
```

## Los parámetros en detalle

### `x` — enteros no negativos, 1D
`array_like` **1D** de enteros $\ge 0$. Un valor negativo lanza `ValueError`; un dtype no entero también falla. El valor **máximo** determina la longitud de la salida, así que un único valor grande infla el vector con muchos ceros intermedios.

```python
np.bincount([0, 1, 1, 3, 3, 3])   # array([1, 2, 0, 3])
#   índice: 0  1  2  3
#   conteo: 1  2  0  3   ← el 2 no aparece → 0, pero ocupa su hueco
```

### `weights` — sumar pesos en vez de contar
`array_like` de **la misma longitud que `x`**. En lugar de sumar 1 por aparición, cada posición `i` acumula la suma de los pesos de los elementos que valen `i`. Esto convierte `bincount` en un **group-by / suma agrupada por índice** muy rápido (y la salida pasa a `float`):

$$ \text{out}_i \;=\; \sum_{j\,:\,x_j = i} w_j $$

```python
x = np.array([0, 1, 1, 2])
w = np.array([0.5, 1.0, 1.0, 2.0])
np.bincount(x, weights=w)   # array([0.5, 2.0, 2.0])  → suma de w por grupo de x
```

### `minlength` — longitud mínima garantizada
`int`. Fuerza a que la salida tenga **al menos** `minlength` posiciones, rellenando con ceros las que falten. Esencial cuando una clase alta puede no aparecer pero necesitas un tamaño de vector fijo (p. ej. conteos por clase con `num_clases` conocido).

```python
np.bincount([0, 1, 1], minlength=5)   # array([1, 2, 0, 0, 0])  → longitud 5 garantizada
```

## El caso N-D

`np.bincount` es **estrictamente 1D**: solo acepta arrays de una dimensión y siempre devuelve un vector 1D (índice = valor contado). No tiene parámetro `axis`. Para clasificar/contar a lo largo de un eje de un array N-D hay que recurrir a otras herramientas:

| Necesidad | Herramienta |
|---|---|
| contar enteros no negativos (1D) | `np.bincount` |
| contar valores arbitrarios + sus etiquetas | [[np.unique]] con `return_counts=True` |
| frecuencias por intervalo (floats/rangos) | [[np.histogram]] |
| histograma multidimensional | [[np.histogramdd]] |

## Valor de retorno

Un `ndarray` **1D** de longitud $\max(\max(x)+1,\ \texttt{minlength})$:

| Caso | dtype de salida | Longitud |
|------|-----------------|----------|
| sin `weights` | `int64` (conteos) | `max(max(x)+1, minlength)` |
| con `weights` | `float64` (sumas) | igual |
| `x` vacío | según `minlength` | `minlength` (o `0`) |

```python
np.bincount([2, 2, 5]).shape       # (6,)  ← longitud = max(x)+1 = 6, no len(x)
np.bincount([2, 2, 5])             # [0, 0, 2, 0, 0, 1]  ← ceros en los huecos
```

La longitud la marca el **valor máximo**, no el número de elementos — un dato como `1_000_000` produce un vector de un millón de entradas casi todas a cero.

## Casos de uso

### Frecuencia de etiquetas de clase
```python
conteos = np.bincount(etiquetas)        # nº de muestras por clase
clase_mayoritaria = np.argmax(conteos)
```

### Conteo por clase con número de clases fijo
```python
np.bincount(etiquetas, minlength=n_clases)   # vector de tamaño n_clases aunque falten clases
```

### Suma agrupada por índice (group-by rápido)
```python
np.bincount(grupos, weights=valores)    # suma de 'valores' por cada grupo entero
```

### Reconstruir un histograma desde digitize
```python
idx = np.digitize(datos, edges)         # bin de cada dato
np.bincount(idx)                        # cuántos por bin
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: x must be non-negative` | hay enteros negativos | desplazar (`x - x.min()`) o filtrar |
| `TypeError` / cast a int | `x` no es de tipo entero | convertir con `.astype(int)` |
| Salida enorme y casi vacía | un valor máximo muy grande | usar [[np.unique]] `return_counts=True` si los valores son dispersos |
| Falta una clase alta | esa clase no apareció en `x` | `minlength=n_clases` |
| `weights` ignorado/error | longitud distinta a `x` | `len(weights) == len(x)` |

## Notas relacionadas

- [[concepto_indexing]] — el índice de salida ES el valor contado
- [[np.histogram]] — frecuencias por intervalo (para floats o rangos)
- [[np.digitize]] — produce las etiquetas enteras que `bincount` cuenta
- [[np.unique]] — conteo de valores arbitrarios (no solo enteros consecutivos)
- [[Librerias/Numpy/np/estadisticas/index|estadísticas]] — el resto de la familia
