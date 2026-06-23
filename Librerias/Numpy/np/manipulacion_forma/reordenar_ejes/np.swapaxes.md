---
title: np.swapaxes — intercambia dos ejes del array
aliases:
  - swapaxes
  - np.swapaxes
tags:
  - numpy
  - api/funcion
  - shape

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
  - concepto_views_vs_copias

draft: false
---

# np.swapaxes — intercambia dos ejes del array

`np.swapaxes` **intercambia exactamente dos ejes** (`axis1` y `axis2`) y deja el resto en su sitio.
Es el caso particular de [[np.transpose]] cuando la permutación afecta solo a dos posiciones, y como
él no copia nada: reordena los `strides` y devuelve una [[concepto_views_vs_copias|vista]] de coste
$O(1)$. Cuando tu intención es literalmente "cambia estos dos ejes de orden", es la opción más
explícita.

## La idea en una fórmula

Intercambiar los ejes $i$ y $j$ es la transposición que permuta solo esas dos posiciones del shape
(el resto de los tamaños quedan donde estaban):

$$
(\dots, n_i, \dots, n_j, \dots) \;\xrightarrow{\ \text{swapaxes}(i,\,j)\ }\; (\dots, n_j, \dots, n_i, \dots)
$$

A nivel de elemento solo se cruzan esos dos índices; el dato es el mismo:

$$
B_{\dots,\,p,\,\dots,\,q,\,\dots} \;=\; A_{\dots,\,q,\,\dots,\,p,\,\dots}
$$

Es simétrico: el orden de los argumentos no importa, `swapaxes(a, i, j)` == `swapaxes(a, j, i)`.

## Firma

```python
np.swapaxes(
    a,        # array_like: el tensor de entrada
    axis1,    # int: primer eje a intercambiar
    axis2,    # int: segundo eje a intercambiar
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` de cualquier dimensión. Se convierte a `ndarray` si no lo es.

### `axis1`, `axis2` — los dos ejes a intercambiar
Enteros en `0..ndim-1` (admiten **negativos**: `-1` es el último eje). El orden entre ellos es
irrelevante. Si coinciden (`axis1 == axis2`), el array no cambia. Fuera de rango lanza `AxisError`.

```python
T = np.ones((2, 3, 4))
np.swapaxes(T, 1, 2).shape    # (2, 4, 3)
np.swapaxes(T, 0, -1).shape   # (4, 3, 2)  → equivale a swapaxes(T, 0, 2)
```

## El caso N-D

Solo los dos ejes nombrados se cruzan; todos los demás conservan su posición. En `(b, m, n)`
intercambiar `1, 2` transpone cada matriz del lote dejando intacto el eje de lote.

| `a.shape` | `axis1, axis2` | salida | lectura |
|-----------|----------------|--------|---------|
| `(m, n)` | `0, 1` | `(n, m)` | transpuesta de matriz |
| `(2, 3, 4)` | `0, 2` | `(4, 3, 2)` | cruza primero y último |
| `(2, 3, 4)` | `1, 2` | `(2, 4, 3)` | transpone cada matriz del lote |
| `(b, m, n, p)` | `1, 3` | `(b, p, n, m)` | cruza ejes 1 y 3, deja 0 y 2 |

```python
# Lote de 8 matrices 3x5 → transponer cada una a 5x3, sin tocar el lote
lote = np.random.rand(8, 3, 5)
lote_T = np.swapaxes(lote, 1, 2)   # (8, 5, 3)
lote[0, 1, 2] == lote_T[0, 2, 1]   # True
```

## Vista vs copia

`np.swapaxes` **siempre devuelve una vista**: cruzar dos ejes es cruzar sus dos entradas en la tupla
de `strides`, sin tocar el buffer (ver [[concepto_ndarray|strides]]). El resultado **comparte memoria**
con `a`, así que escribir en él muta el original.

```python
T = np.arange(24).reshape(2, 3, 4)
S = np.swapaxes(T, 1, 2)
S.base is T      # True
S[0, 0, 0] = 99
T[0, 0, 0]       # 99  → mismo buffer
```

Tras el intercambio el array deja de ser C-contiguo; usa `np.ascontiguousarray` si una librería lo
exige (ver [[concepto_contiguidad_memoria]]).

## Valor de retorno

| Entrada | `axis1, axis2` | salida (shape) | tipo |
|---------|----------------|----------------|------|
| `(m, n)` | `0, 1` | `(n, m)` | `ndarray` (vista) |
| `(\dots,n_i,\dots,n_j,\dots)` | `i, j` | con $n_i$ y $n_j$ cruzados | `ndarray` (vista) |
| cualquiera | `k, k` | igual a la entrada | `ndarray` (vista) |

El `dtype` se conserva. Nunca devuelve escalar.

## Casos de uso

### De (batch, features, tiempo) a (batch, tiempo, features)
```python
datos = np.random.rand(32, 10, 100)     # (batch, feat, tiempo)
datos = np.swapaxes(datos, 1, 2)        # (32, 100, 10)
```

### Transponer la matriz interna de un lote
```python
lote = np.random.rand(8, 3, 5)
lote_T = np.swapaxes(lote, 1, 2)        # cada matriz 3x5 → 5x3
```

### Equivalencia con transpose
```python
T = np.ones((2, 3, 4))
np.swapaxes(T, 0, 2)            # más legible para dos ejes
np.transpose(T, (2, 1, 0))     # misma salida con permutación completa
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AxisError: axis N is out of bounds` | `axis1`/`axis2` fuera de rango | usar ejes válidos (`0..ndim-1` o negativos) |
| Se modificó el original | el retorno es una vista | `.copy()` si necesitas independencia |
| Otra función rompe por no contiguo | swapaxes deja strides reordenados | `np.ascontiguousarray(resultado)` |
| Se quería mover un eje, no cruzar dos | swapaxes desordena el par; no conserva el resto | usar [[np.moveaxis]] |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes del intercambio
- [[concepto_views_vs_copias]] — por qué es una vista
- [[concepto_contiguidad_memoria]] — el resultado deja de ser contiguo
- [[np.transpose]] — permutación general de todos los ejes
- [[np.moveaxis]] — mover un eje conservando el orden del resto
