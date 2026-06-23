---
title: np.putmask — escribe valores in-place donde una máscara es True
aliases:
  - putmask
  - np.putmask
tags:
  - numpy
  - api/funcion
  - indexado

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: None
inplace: true

# --- Dependencias ---
requiere:
  - concepto_indexing

draft: false
---

# np.putmask — escribe valores in-place donde una máscara es True

`np.putmask` **escribe** valores en un array exactamente en las posiciones donde una **máscara
booleana** es `True`, dejándolo igual donde es `False`. Es la versión funcional de la asignación
booleana `a[mask] = values`, con una diferencia importante en cómo recicla `values`. No devuelve
nada: **muta** `a` en el sitio. La idea en una frase: `putmask(a, mask, values)` es como
`a[mask] = values` pero con **reciclado por tamaño total**, no por número de `True`.

## La idea en una fórmula

`putmask` conserva el shape de `a` y reescribe solo las celdas seleccionadas por la máscara. Para
cada posición $i$ del array aplanado:

$$ a_i \;\leftarrow\; \begin{cases} \texttt{values}[\,i \bmod L\,] & \text{si } \texttt{mask}_i = \texttt{True} \\[2pt] a_i & \text{si } \texttt{mask}_i = \texttt{False} \end{cases} $$

donde $L$ es el número de elementos de `values`. La clave —y la diferencia con `a[mask] = v`— es
que el índice de `values` se cuenta sobre **todas** las posiciones ($i \bmod L$), no solo sobre las
`True`.

## Firma

```python
np.putmask(
    a,         # ndarray: el array a modificar (in-place)
    mask,      # array_like[bool]: máscara, broadcasteable al shape de a
    values,    # array_like: valores a escribir donde mask es True (se reciclan por i % len)
) -> None
```

## Los parámetros en detalle

### `a` — el array a modificar
`ndarray` real (se escribe sobre su buffer). Conserva shape y dtype; los valores escritos se
**castean** al dtype de `a` (un float escrito en un array `int` se trunca, sin aviso).

### `mask` — la máscara booleana
`array_like` de booleanos, broadcasteable al shape de `a`. Las posiciones `True` se sobrescriben;
las `False` quedan intactas. Suele venir de una condición (`a > 0`).

```python
a = np.array([1, 2, 3, 4])
np.putmask(a, a > 2, 0)
a   # [1, 2, 0, 0]
```

### `values` — los valores a escribir
`array_like`. Si tiene menos elementos que `a`, se **recicla cíclicamente sobre el array entero**
(índice `i % len(values)`), no sobre las posiciones `True`. Esto es lo que lo distingue de
`a[mask] = values`, que recicla sobre el número de `True`.

```python
a = np.arange(6)              # [0,1,2,3,4,5]
mask = np.array([True, False, True, False, True, False])
np.putmask(a, mask, [10, 20])
# en i=0 (True) escribe values[0%2]=10
# en i=2 (True) escribe values[2%2]=10
# en i=4 (True) escribe values[4%2]=10
a   # [10, 1, 10, 3, 10, 5]
```

## El caso N-D

`np.putmask` no tiene `axis`: opera sobre el array **aplanado** en orden C. La `mask` se broadcastea
al shape de `a` y `values` se recicla sobre el total de elementos. Sirve igual en cualquier
dimensión, conservando el shape de `a`.

```python
M = np.arange(9).reshape(3, 3)
np.putmask(M, M % 2 == 0, -1)   # marca los pares
M
# [[-1,  1, -1],
#  [ 3, -1,  5],
#  [-1,  7, -1]]
```

## Vectorización

`np.putmask` reemplaza un bucle de asignación condicional por una sola pasada en C:

```python
# Bucle Python:
flat = a.ravel()
for i in range(a.size):
    if mask.flat[i]:
        flat[i] = values[i % len(values)]

# Vectorizado:
np.putmask(a, mask, values)
```

### Diferencia con `a[mask] = values`

Ambos escriben in-place donde la máscara es `True`, pero **reciclan `values` distinto**:

| | `a[mask] = values` | `np.putmask(a, mask, values)` |
|---|---|---|
| Índice de `values` | sobre el número de `True` (k-ésimo `True` ← `values[k]`) | sobre **todo** el array (`i % len`) |
| `len(values)` exige | divisor del nº de `True` | divisor del nº **total** de elementos |
| Caso escalar | idéntico | idéntico |

```python
a = np.arange(6); mask = a % 2 == 0     # 3 True (en 0,2,4)
b = a.copy()

a[mask] = [10, 20, 30]    # asignación booleana: True por True → 10,20,30
# a → [10, 1, 20, 3, 30, 5]

np.putmask(b, mask, [10, 20, 30])   # i%3 en cada True: i=0→10, i=2→30, i=4→20
# b → [10, 1, 30, 3, 20, 5]   ← distinto reciclado
```

Para un valor escalar (`np.putmask(a, mask, 0)`) no hay diferencia: ambos rellenan con `0`. Ver
[[concepto_indexing]] para la familia booleana.

## Valor de retorno

**`None`**. El efecto es la mutación in-place de `a`.

| Llamada | Retorno | Efecto |
|---------|---------|--------|
| `np.putmask(a, mask, v)` | `None` | reescribe `a` donde `mask` |
| `x = np.putmask(...)` | `x is None` | el resultado vive en `a`, no en `x` |

## Casos de uso

### Saturar / recortar por condición (variante de clip)
```python
señal = np.array([-5, 3, 12, -2, 20])
np.putmask(señal, señal < 0, 0)        # a 0 los negativos
señal   # [0, 3, 12, 0, 20]
```

### Reemplazar NaN in-place sin copiar
```python
x = np.array([1.0, np.nan, 3.0, np.nan])
np.putmask(x, np.isnan(x), 0.0)
x   # [1., 0., 3., 0.]
```

### N-D: poner a cero los valores grandes de un tensor
```python
T = np.arange(8).reshape(2, 2, 2)
np.putmask(T, T > 4, 0)
T
# [[[0, 1], [2, 3]],
#  [[4, 0], [0, 0]]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Reciclado distinto al esperado | `values` se indexa por `i % len`, no por nº de `True` | usar escalar, o `a[mask] = v` si quieres reciclado por `True` |
| Valores truncados | `values` se castea al dtype de `a` (float→int) | crear `a` con el dtype adecuado |
| `a` quedó en `None` | se asignó el retorno | llamar sin asignar |
| El original cambió sin querer | `putmask` muta `a` | copiar antes con `a.copy()` |

## Notas relacionadas

- [[concepto_indexing]] — la familia booleana y la asignación `a[mask] = v`
- [[np.put]] — escribir in-place por índice plano en lugar de por máscara
- [[np.clip]] — recortar a un rango sin escribir máscaras a mano
- [[Librerias/Numpy/np/seleccion/index|selección]] — el resto de la familia
