---
title: np.put — escribe valores in-place por índices planos (inverso de take)
aliases:
  - put
  - np.put
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

# np.put — escribe valores in-place por índices planos (inverso de take)

`np.put` **escribe** valores dentro de un array recorriéndolo por su **índice plano** (estilo
`a.flat`), exactamente la operación inversa de [[np.take]] (que **lee** por índice plano). No
devuelve nada: **muta** `a` en el sitio. La clave que gobierna su comportamiento es que `ind`
indexa siempre el array **aplanado**, ignorando la forma N-D: `put(a, ind, v)` es literalmente
`a.flat[ind] = v`.

## La idea en una fórmula

`put` no transforma la forma: deja `a` con su mismo shape y solo reescribe las celdas señaladas.
La operación es la asignación sobre la vista plana del array:

$$ \texttt{np.put}(a,\ \mathbf{ind},\ \mathbf{v}) \;\equiv\; a.\texttt{flat}[\,\mathbf{ind}\,] = \mathbf{v} $$

Sobre un array de shape $(n_0,\dots,n_{k-1})$, el índice plano $p$ apunta a la celda multidimensional
en orden C (row-major):

$$ p \;\longleftrightarrow\; (i_0,\dots,i_{k-1}) \quad\text{con}\quad p = \sum_{d=0}^{k-1} i_d \prod_{e>d} n_e $$

Por eso en una matriz $(2,3)$ el índice plano `4` cae en `(1, 1)`: se cuenta fila por fila.

## Firma

```python
np.put(
    a,                 # ndarray: el array a modificar (in-place)
    ind,               # array_like[int]: índices PLANOS (sobre a.flat)
    v,                 # array_like: valores a escribir (se reciclan por broadcast)
    mode='raise',      # {'raise', 'wrap', 'clip'}: qué hacer con índices fuera de rango
) -> None
```

## Los parámetros en detalle

### `a` — el array a modificar
`ndarray` (no `array_like`: debe ser un array real, porque se escribe in-place sobre su buffer).
Conserva su shape; solo cambian los valores de las celdas indicadas. Si necesitas conservar el
original, copia antes con `a.copy()`.

### `ind` — los índices planos
`array_like` de enteros interpretados sobre `a.flat`, **no** por (fila, columna). Un entero `4` en
una matriz `(2,3)` apunta a la 5ª celda en orden C, no a la fila 4. Acepta índices negativos
(cuentan desde el final del array plano).

```python
M = np.zeros((2, 3))
np.put(M, [0, 4], 1)     # posiciones planas 0 y 4
M
# [[1., 0., 0.],
#  [0., 1., 0.]]          ← el 4 cayó en (1, 1)
```

### `v` — los valores a escribir
`array_like`. Si hay **menos** valores que índices, se **reciclan** (broadcast por repetición
cíclica); si hay más, sobran los últimos. Un escalar se difunde a todos los índices.

```python
a = np.zeros(5)
np.put(a, [0, 1, 2, 3], [9, 8])   # v se recicla: 9,8,9,8
a   # [9., 8., 9., 8., 0.]
```

### `mode` — índices fuera de rango
Qué hacer cuando un índice excede el tamaño del array plano:
- `'raise'` (defecto) — lanza `IndexError`.
- `'wrap'` — envuelve con módulo (`ind % a.size`).
- `'clip'` — recorta al rango válido (los negativos van a `0`, los grandes al último).

```python
a = np.zeros(3)
np.put(a, [5], 1, mode='wrap')   # 5 % 3 = 2
a   # [0., 0., 1.]
```

## El caso N-D

`np.put` **aplana** siempre: trabaja sobre $(n_0\cdots n_{k-1})$ elementos en orden C, sin importar
cuántos ejes tenga `a`. No existe parámetro `axis`. Esto lo hace cómodo para sembrar valores sueltos,
pero **inadecuado** para escribir por coordenadas: para eso usa indexado directo `a[filas, cols] = v`,
que sí respeta los ejes.

```python
T = np.zeros((2, 2, 2))     # 8 celdas planas: 0..7
np.put(T, [0, 7], [1, 1])   # primera y última celda
T
# [[[1., 0.], [0., 0.]],
#  [[0., 0.], [0., 1.]]]
```

## Vectorización

`np.put` reemplaza un bucle de asignación dispersa por una sola llamada en C. Las dos versiones
hacen lo mismo, pero la vectorizada no crea objetos Python por elemento:

```python
# Bucle Python (explícito):
def put_manual(a, ind, v):
    flat = a.ravel()
    for k, p in enumerate(ind):
        flat[p] = v[k % len(v)]   # reciclado manual

# Vectorizado:
np.put(a, ind, v)
```

A diferencia de `a[mask] = v`, `np.put` toma directamente los **índices**, no una máscara: es la
herramienta natural cuando ya tienes las posiciones planas (p. ej. salidas de [[np.argsort]] o de
`np.ravel_multi_index`). Ver [[concepto_indexing]].

## Valor de retorno

**`None`**. La función no devuelve nada útil; su efecto es la **mutación in-place** de `a`.

| Llamada | Retorno | Efecto |
|---------|---------|--------|
| `np.put(a, ind, v)` | `None` | `a.flat[ind] = v` |
| `x = np.put(a, ind, v)` | `x is None` | bug típico: se pierde `a` si reasignas |

```python
a = np.arange(5)
r = np.put(a, [0, 2], [99, 88])
r        # None
a        # [99, 1, 88, 3, 4]  ← el resultado está en a, no en r
```

## Casos de uso

### Sembrar posiciones concretas en un buffer
```python
buffer = np.zeros(10)
np.put(buffer, [1, 4, 7], -1)
buffer   # [0,-1,0,0,-1,0,0,-1,0,0]
```

### Inverso de take (round-trip)
```python
a = np.array([10, 20, 30, 40])
ind = [0, 3]
vals = np.take(a, ind)      # [10, 40]   ← leer
np.put(a, ind, vals * 2)    # escribir el doble en su sitio
a   # [20, 20, 30, 80]
```

### N-D: marcar esquinas de un tensor por índice plano
```python
T = np.zeros((3, 3))
np.put(T, [0, 2, 6, 8], 1)   # las 4 esquinas en orden C
T
# [[1., 0., 1.],
#  [0., 0., 0.],
#  [1., 0., 1.]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `a` quedó en `None` | se asignó el retorno (`a = np.put(...)`) | llamar sin asignar; el efecto está en `a` |
| Posiciones inesperadas en N-D | `ind` es **plano**, no por coordenadas | usar `a[filas, cols] = v` |
| `IndexError` | índice fuera de rango con `mode='raise'` | `mode='clip'` / `'wrap'` o validar `ind` |
| El original se modificó sin querer | `put` muta `a` | copiar antes con `a.copy()` |

## Notas relacionadas

- [[concepto_indexing]] — el índice plano y las familias de indexado
- [[np.take]] — la operación inversa: leer por índice plano
- [[np.putmask]] — escribir in-place por máscara booleana en lugar de por índice
- [[Librerias/Numpy/np/seleccion/index|selección]] — el resto de la familia
