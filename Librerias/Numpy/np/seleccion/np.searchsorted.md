---
title: np.searchsorted — índices de inserción en un array ordenado (búsqueda binaria)
aliases:
  - searchsorted
  - np.searchsorted
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.searchsorted — índices de inserción en un array ordenado (búsqueda binaria)

`np.searchsorted` responde, para un array **ya ordenado** `a`, la pregunta "¿en qué posición habría
que insertar cada valor de `v` para que `a` siga ordenado?". Lo resuelve con **búsqueda binaria**
($O(\log n)$ por consulta), no con un barrido lineal. Es la pieza base de **binning**, **interpolación**
e **inserción manteniendo el orden**. La idea en una frase: devuelve, por cada valor buscado, su
índice de inserción en `a`.

## La idea en una fórmula

Cada valor de `v` se mapea a un índice de inserción; la forma de la salida **copia la forma de `v`**:

$$ v\ \text{de shape}\ (m_0,\dots,m_{r-1}) \ \xrightarrow{\ \text{searchsorted}(a,\,\cdot)\ }\ \text{índices de shape}\ (m_0,\dots,m_{r-1}) $$

Para un escalar buscado $x$ en `a` ordenado de longitud $n$, el índice $i$ devuelto cumple:

$$ \texttt{side='left'}:\quad a_{i-1} < x \le a_i \qquad\qquad \texttt{side='right'}:\quad a_{i-1} \le x < a_i $$

es decir, `a[:i]` queda a la izquierda del punto de inserción y `a[i:]` a la derecha. El índice está
en $[0, n]$: `0` si $x$ va antes de todo, `n` si va después de todo. La propiedad clave:
`np.insert(a, i, x)` mantiene `a` ordenado.

## Firma

```python
np.searchsorted(
    a,               # array_like 1D: array ORDENADO ascendente (o con sorter)
    v,               # array_like: valor(es) a insertar; su shape dicta la salida
    side='left',     # {'left', 'right'}: lado de empate (<= vs <)
    sorter=None,     # array_like[int] | None: índices que ordenan a (de argsort)
) -> ndarray | escalar
```

## Los parámetros en detalle

### `a` — el array ordenado de referencia
`array_like` **1D** que debe estar **ordenado ascendentemente** (NumPy no lo verifica; si no lo está,
los resultados carecen de sentido). Si tu array no está ordenado, pásalo por `np.sort` o usa `sorter`.

### `v` — los valores a localizar
`array_like` (escalar o N-D). El **shape de la salida es el shape de `v`**: un escalar da un índice
escalar, un array `(m,)` da `(m,)` índices, un `(p, q)` da `(p, q)`.

```python
a = np.array([1, 3, 5, 7, 9])
np.searchsorted(a, 4)            # 2     → 4 va entre 3 y 5
np.searchsorted(a, [0, 4, 10])   # [0, 2, 5]  → antes de todo / en medio / después de todo
```

### `side` — el lado del empate
Decide a qué lado de un valor **igual** se inserta:
- `'left'` (defecto) — primer hueco donde `a[i-1] < v <= a[i]`; el nuevo valor va **antes** de los
  iguales.
- `'right'` — `a[i-1] <= v < a[i]`; va **después** de los iguales.

La diferencia solo importa cuando `v` coincide con un valor de `a`; con `right - left` se cuenta
cuántas veces aparece un valor:

```python
a = np.array([1, 2, 2, 2, 3])
np.searchsorted(a, 2, side='left')    # 1   → antes del primer 2
np.searchsorted(a, 2, side='right')   # 4   → después del último 2
# right - left = 3  → hay tres '2' en a
```

### `sorter` — orden indirecto
`array_like` de enteros que ordena `a` (típicamente `np.argsort(a)`), para usar `searchsorted` sin
copiar/reordenar un array desordenado. Los índices devueltos son posiciones en el `a` **ordenado por
`sorter`**.

```python
a = np.array([3, 1, 2])
s = np.argsort(a)               # [1, 2, 0]  → ordena a como [1,2,3]
np.searchsorted(a, 2, sorter=s) # 1   → posición de 2 en el orden lógico
```

## El caso N-D

`a` es siempre **1D** (la tabla ordenada de referencia). La dimensionalidad la aporta `v`: la salida
**reproduce el shape de `v`**, aplicando la búsqueda binaria a cada elemento de forma independiente.

```python
a = np.array([0, 10, 20, 30])
v = np.array([[5, 15],
              [25, 35]])         # shape (2, 2)
np.searchsorted(a, v)
# [[1, 2],
#  [3, 4]]                       → shape (2, 2), el de v
```

## Vectorización

`np.searchsorted` reemplaza un bucle de búsqueda binaria escrito a mano, ejecutándolo en C para
**todos** los valores de `v` de golpe:

```python
# Bucle Python (búsqueda binaria manual por valor):
import bisect
idx = [bisect.bisect_left(a, x) for x in v]

# Vectorizado (una sola llamada, en C):
np.searchsorted(a, v)
```

Frente a `(a < x).sum()` —que también da el índice de inserción pero recorre **todo** `a` en $O(n)$—,
`searchsorted` es $O(\log n)$ por consulta gracias a que `a` está ordenado. Es la herramienta
correcta cuando haces muchas consultas sobre una misma tabla ordenada. Ver [[concepto_indexing]].

## Valor de retorno

El tipo y shape **siguen a `v`**:

| `v` | `side` | salida |
|-----|--------|--------|
| escalar | cualquiera | índice **escalar** (`np.intp`) en $[0, n]$ |
| `(m,)` | cualquiera | `ndarray` `(m,)` de índices |
| `(p, q)` | cualquiera | `ndarray` `(p, q)` de índices |

El dtype de los índices es entero (`np.intp`). Los valores caen en $[0, \text{len}(a)]$.

## Casos de uso

### Binning: asignar cada dato a su intervalo
```python
bordes = np.array([0, 10, 20, 30])      # límites de los bins
datos  = np.array([5, 15, 25, 35])
np.searchsorted(bordes, datos)          # [1, 2, 3, 4]  → nº de bin de cada dato
```

### Interpolación: localizar el tramo de cada x
```python
xs = np.array([0., 1., 2., 3.])         # nodos (ordenados)
x  = 1.7
i  = np.searchsorted(xs, x)             # 2  → x cae entre xs[1] y xs[2]
# luego se interpola entre xs[i-1] y xs[i]
```

### Insertar manteniendo el orden
```python
a = np.array([1, 3, 5, 7])
nuevos = np.array([2, 6])
pos = np.searchsorted(a, nuevos)        # [1, 3]
np.insert(a, pos, nuevos)               # [1, 2, 3, 5, 6, 7]  ← sigue ordenado
```

### Contar ocurrencias / consultas de rango
```python
a = np.array([1, 2, 2, 2, 3, 5])
lo = np.searchsorted(a, 2, side='left')   # 1
hi = np.searchsorted(a, 2, side='right')  # 4
hi - lo                                    # 3  → cuántos '2' hay
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Índices sin sentido | `a` no está ordenado | `np.sort(a)` o pasar `sorter=np.argsort(a)` |
| Empates en el lado equivocado | `side` por defecto `'left'` | usar `side='right'` según convenga |
| `IndexError` al usar el índice | el índice puede ser `len(a)` (inserción al final) | acotar con `np.clip` antes de indexar |
| Resultado escalar donde se esperaba array | `v` era escalar | pasar `v` como array `(m,)` |

## Notas relacionadas

- [[concepto_indexing]] — selección por índices y su shape
- [[np.sort]] — produce el `a` ordenado que `searchsorted` requiere
- [[np.argsort]] — genera el `sorter` para búsquedas sobre arrays desordenados
- [[np.insert]] — usa los índices devueltos para insertar manteniendo el orden
- [[Librerias/Numpy/np/seleccion/index|selección]] — el resto de la familia
