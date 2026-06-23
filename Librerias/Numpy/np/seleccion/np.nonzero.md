---
title: np.nonzero — índices de los elementos no nulos (una tupla por eje)
aliases:
  - nonzero
  - np.nonzero
tags:
  - numpy
  - api/funcion
  - seleccion

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: tuple
inplace: false

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.nonzero — índices de los elementos no nulos (una tupla por eje)

`np.nonzero` localiza **dónde** un array es distinto de cero. No devuelve los valores ni un array de
coordenadas, sino una **tupla de arrays de índices**: un array por cada eje del tensor, de forma que
los $j$-ésimos elementos de todos ellos, leídos en paralelo, dan las coordenadas del $j$-ésimo
elemento no-cero. Ese formato "tupla por eje" es exactamente lo que necesita el indexado avanzado
(ver [[concepto_indexing]]): `a[np.nonzero(cond)]` recupera de golpe los elementos que cumplen
`cond`. Es la operación detrás del modo-índices de [[np.where]].

## La idea en una fórmula

Para una entrada de $k$ ejes, `nonzero` produce $k$ arrays paralelos, cada uno de longitud $N$ (el
número de elementos no-cero). El array $j$-ésimo lista las coordenadas a lo largo del eje $j$:

$$ a\ \text{de shape}\ (n_0,\dots,n_{k-1}) \ \xrightarrow{\ \text{nonzero}\ }\ \big(\mathbf{r}_0,\dots,\mathbf{r}_{k-1}\big),\qquad \mathbf{r}_j\ \text{de shape}\ (N,) $$

donde $N = \#\{\text{posiciones con } a\neq 0\}$, y la coordenada completa del elemento no-cero
número $m$ es $\big(\mathbf{r}_0[m],\dots,\mathbf{r}_{k-1}[m]\big)$. Los elementos se recorren en
orden **C (fila por fila)**, así que la salida sale ordenada por ese recorrido.

Indexar con la tupla recupera los valores, todos aplanados a 1D:

$$ a\big[\,\mathbf{r}_0,\dots,\mathbf{r}_{k-1}\,\big]\ \longrightarrow\ \text{shape}\ (N,) $$

## Firma

```python
np.nonzero(
    a,    # array_like: el tensor de entrada (cualquier dtype)
) -> tuple[ndarray, ...]
```

También existe como método: `a.nonzero()` es idéntico.

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` de cualquier `dtype`. Lo que cuenta como "cero" es el valor neutro de su tipo: `0` para
enteros, `0.0` para floats, `False` para booleanos, `''` para strings, `0+0j` para complejos. Todo
lo demás es "no-cero" y se reporta. Sobre una **máscara booleana** (`a > 0`), los `True` son los
no-cero, que es el uso más habitual. Cuidado: `np.nan` cumple `nan != 0`, así que **cuenta como
no-cero**.

## El caso N-D

El número de arrays de la tupla es siempre `a.ndim`. En 1D hay un solo array (de ahí el típico
`[0]`); en 2D se desempaqueta en `(filas, columnas)`; en N-D, un array por eje:

```python
# 1D → tupla de 1 array
np.nonzero(np.array([0, 3, 0, 5]))       # (array([1, 3]),)

# 2D → tupla de 2 arrays (filas, columnas)
M = np.array([[0, 5], [3, 0]])
filas, cols = np.nonzero(M)
filas, cols                              # (array([0, 1]), array([1, 0]))
list(zip(filas, cols))                   # [(0, 1), (1, 0)]  → coordenadas

# 3D → tupla de 3 arrays
T = np.array([[[0, 5], [0, 0]],
              [[7, 0], [0, 9]]])         # shape (2, 2, 2)
z, f, c = np.nonzero(T)
z, f, c        # (array([0,1,1]), array([0,0,1]), array([1,0,1]))
T[z, f, c]     # [5, 7, 9]  → valores en orden C
```

La regla mecánica: el `m`-ésimo no-cero está en la coordenada formada por el `m`-ésimo elemento de
cada array de la tupla.

## Vectorización

`nonzero` reemplaza el barrido manual con dos bucles anidados que acumulan coordenadas en listas:

```python
# Bucle Python (lento, explícito):
filas, cols = [], []
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if M[i, j] != 0:
            filas.append(i); cols.append(j)

# Vectorizado:
filas, cols = np.nonzero(M)
```

NumPy recorre el buffer en C y construye los arrays de índices de una pasada; además, el resultado
queda en el formato exacto para indexar (`a[np.nonzero(cond)]`) sin reconvertir nada. Es el mismo
principio de [[concepto_vectorizacion]]: describes *qué* buscas, no *cómo* iterar.

## Valor de retorno

Siempre una **tupla**, nunca un array suelto:

| Entrada (shape) | Retorno | Cada array | dtype |
|-----------------|---------|------------|-------|
| `(n,)` | tupla de **1** array | `(N,)` | `intp` |
| `(m, n)` | tupla de **2** arrays | `(N,)` cada uno | `intp` |
| `(n_0,…,n_{k-1})` | tupla de **`k`** arrays | `(N,)` cada uno | `intp` |

`N` es el número de elementos no-cero (`np.count_nonzero(a)`). Si no hay ninguno, la tupla trae `k`
arrays vacíos `(0,)`. El `dtype` de los índices es siempre `intp` (el entero de indexación de la
plataforma). Para obtener un **array de coordenadas** `(N, k)` en vez de la tupla, usa
[[np.argwhere]].

## Casos de uso

### Indexar los elementos que cumplen una condición
```python
arr = np.array([5, -2, 8, -1])
arr[np.nonzero(arr > 0)]    # [5, 8]   ≡ arr[arr > 0], pero con la tupla explícita
```

### Recuperar las posiciones de una condición
```python
idx = np.nonzero(señal > umbral)[0]        # índices 1D donde se supera el umbral
```

### Contar no-ceros (mejor con la función dedicada)
```python
len(np.nonzero(arr)[0])     # funciona, pero...
np.count_nonzero(arr)       # ...esto es más directo y no construye los índices
```

### N-D: coordenadas de los activos en un tensor
```python
vol = np.zeros((4, 4, 4)); vol[1, 2, 3] = vol[0, 0, 1] = 1
coords = np.nonzero(vol)              # tupla de 3 arrays
np.transpose(coords)                  # array (2, 3) con las coordenadas (≡ np.argwhere)
# [[0, 0, 1],
#  [1, 2, 3]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperar un array y recibir una tupla | `nonzero` **siempre** devuelve tupla | indexar `[0]` en 1D, o desempaquetar |
| `nan` aparece como no-cero | `nan != 0` es `True` | filtrar `nan` antes si molesta |
| Querer coordenadas `(N, k)` y obtener tupla | formato distinto | usar [[np.argwhere]] (= `transpose(nonzero)`) |
| Usarlo solo para contar | construye índices innecesarios | `np.count_nonzero` |

## Notas relacionadas

- [[concepto_indexing]] — por qué la tupla es justo lo que pide el indexado avanzado
- [[np.where]] — `where(cond)` es exactamente `nonzero(cond)`
- [[np.argwhere]] — la misma información como array `(N, k)` de coordenadas
- [[np.extract]] · [[np.count_nonzero]] · [[np.take]]
