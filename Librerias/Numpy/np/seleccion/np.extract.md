---
title: np.extract — extrae los elementos donde la condición es True (aplanados)
aliases:
  - extract
  - np.extract
tags:
  - numpy
  - api/funcion
  - seleccion

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

# np.extract — extrae los elementos donde la condición es True (aplanados)

`np.extract(condition, arr)` devuelve los **valores** de `arr` en las posiciones donde `condition`
es verdadera, aplanados a un array 1D. A diferencia de [[np.nonzero]] o [[np.argwhere]] (que dan
*dónde*), `extract` da el *qué*: los elementos en sí. Es literalmente el indexado booleano
`arr[condition.astype(bool)]` con nombre de función —existe sobre todo por simetría con su inversa
`np.place`—. En código nuevo, la máscara directa `arr[arr > 0]` suele ser más idiomática (ver
[[concepto_indexing]]); `extract` resulta útil cuando la condición ya viene como array aparte.

## La idea en una fórmula

Ambos argumentos se aplanan en orden C y se conserva el elemento de `arr` allí donde la condición es
`True`. La salida es siempre 1D, con tantos elementos como `True` haya:

$$ \text{arr de shape}\ (n_0,\dots,n_{k-1}) \ \xrightarrow[\ \text{condition}\ ]{\ \text{extract}\ }\ \text{shape}\ (N,),\qquad N = \#\{\text{True}\} $$

Por índices, sobre los arrays aplanados $\hat{\text{arr}}$ y $\hat{\text{cond}}$ de longitud
$n_0\cdots n_{k-1}$, la salida es la subsecuencia:

$$ \text{out} \;=\; \big[\ \hat{\text{arr}}[p]\ :\ \hat{\text{cond}}[p]\ \big],\qquad p = 0,1,\dots $$

La equivalencia exacta con el indexado booleano:

$$ \texttt{np.extract(cond, arr)} \;=\; \texttt{arr.ravel()[cond.ravel().astype(bool)]} $$

## Firma

```python
np.extract(
    condition,    # array_like: máscara (se interpreta como booleana)
    arr,          # array_like: el array del que se extraen los valores
) -> ndarray  # 1D, shape (N,)
```

## Los parámetros en detalle

### `condition` — la máscara
`array_like`. Se convierte a booleano por truthiness: `0`/`0.0`/`False` → no se extrae; cualquier
otro valor → sí. No tiene por qué ser ya `bool` (un array de enteros funciona, los no-cero marcan).
Suele tener el mismo shape que `arr`; si no, ambos se aplanan y se emparejan posición a posición en
orden C, así que **conviene que coincidan en tamaño** para evitar emparejamientos confusos.

### `arr` — el array de valores
`array_like`. Es de aquí de donde salen los elementos devueltos. Su `dtype` se conserva en la salida.
Se recorre aplanado en orden C, de modo que la estructura N-D se pierde: el resultado es siempre 1D.

```python
arr = np.array([1, 2, 3, 4, 5])
cond = arr % 2 == 0
np.extract(cond, arr)         # [2, 4]
```

## El caso N-D

`extract` **siempre aplana**: da igual que `arr` sea 2D o 3D, la salida es 1D en orden C. Es la
diferencia clave con [[np.where]] modo selección (que preserva el shape):

```python
M = np.arange(12).reshape(3, 4)
#  [[ 0,  1,  2,  3],
#   [ 4,  5,  6,  7],
#   [ 8,  9, 10, 11]]
np.extract(M % 3 == 0, M)     # [0, 3, 6, 9]   → 1D, recorrido fila por fila

T = np.arange(24).reshape(2, 3, 4)
np.extract(T > 20, T)         # [21, 22, 23]   → aplanado, sin estructura 3D
```

Si necesitas conservar la forma, esto no es la herramienta: usa `np.where(cond, arr, otro)` para
mantener el shape, o [[np.argwhere]] si quieres las coordenadas.

## Vectorización

`extract` reemplaza el bucle que filtra a mano:

```python
# Bucle Python (lento, explícito):
out = [v for v, c in zip(arr.ravel(), cond.ravel()) if c]
out = np.array(out)

# Vectorizado (equivalentes entre sí):
out = np.extract(cond, arr)
out = arr[cond.astype(bool)]      # indexado booleano directo (más idiomático)
```

Las dos versiones vectorizadas recorren el buffer en C y construyen una **copia** 1D (el indexado
booleano nunca devuelve vista, ver [[concepto_indexing]]). La diferencia con `arr[cond]` es solo de
estilo: `extract` acepta condiciones no-booleanas y existe como pareja de `np.place`.

## Valor de retorno

Siempre un **`ndarray` 1D** (copia), conserve `arr` la forma que conserve:

| `arr` (shape) | `condition` | Salida | dtype |
|---------------|-------------|--------|-------|
| `(n,)` | misma shape | `(N,)` | el de `arr` |
| `(m, n)` | misma shape | `(N,)` aplanado | el de `arr` |
| `(n_0,…,n_{k-1})` | misma shape | `(N,)` aplanado en orden C | el de `arr` |

`N` es el número de `True` de `condition`. Si ninguno es `True`, la salida es un array vacío `(0,)`.
El `dtype` es el de `arr` (no el de la condición).

## Casos de uso

### Filtrar valores que cumplen una condición
```python
datos = np.array([3, -1, 4, -1, 5, 9, -2])
np.extract(datos > 0, datos)       # [3, 4, 5, 9]   ≡ datos[datos > 0]
```

### Condición sobre un array, valores de otro
```python
notas   = np.array([4.0, 7.5, 6.0, 9.0])
aprueba = np.array([0,   1,   0,   1])     # máscara externa (no booleana)
np.extract(aprueba, notas)         # [7.5, 9.0]
```

### N-D: recoger los valores de una región
```python
img = np.arange(16).reshape(4, 4)
np.extract(img > 9, img)           # [10, 11, 12, 13, 14, 15]  → 1D
```

### Comparación con las hermanas
```python
M = np.array([[0, 5], [3, 0]])
np.extract(M > 0, M)               # [5, 3]            → valores (qué)
np.nonzero(M > 0)                  # (array([0,1]), array([1,0]))  → tupla por eje (dónde)
np.argwhere(M > 0)                 # [[0,1],[1,0]]     → array (N,k) de coordenadas
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar conservar el shape | `extract` **siempre** aplana a 1D | usar [[np.where]] modo selección |
| `condition` y `arr` de tamaños distintos | se aplanan y emparejan por posición | igualar shapes antes |
| Querer las posiciones, no los valores | `extract` da los valores | [[np.nonzero]] / [[np.argwhere]] |
| Pensar que devuelve una vista | indexado booleano siempre copia | asumir copia (ver [[concepto_indexing]]) |

## Notas relacionadas

- [[concepto_indexing]] — `extract(cond, arr)` ≡ `arr[cond.astype(bool)]` (indexado booleano)
- [[np.where]] — modo selección si quieres conservar el shape
- [[np.nonzero]] · [[np.argwhere]] — las posiciones en vez de los valores
- [[np.place]] · [[np.compress]] · [[np.take]]
