---
title: np.choose — construye un array eligiendo de una lista según un índice
aliases:
  - choose
  - np.choose
tags:
  - numpy
  - api/funcion
  - indexado

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
  - concepto_broadcasting

draft: false
---

# np.choose — construye un array eligiendo de una lista según un índice

`np.choose` construye un array donde, **para cada posición**, el valor se toma de uno entre varios arrays candidatos: un array de índices `a` decide *de cuál*. Si `choices = [c0, c1, c2]`, entonces `choose(a, choices)` en la posición `i` vale `choices[a[i]][i]`. Es un *multiplexor* elemento a elemento: `a` es la señal de selección y `choices` son las entradas. La idea en una frase: **`a` elige el array, la posición elige el elemento**.

## La idea en una fórmula

Dada una lista de $L$ arrays $c_0,\dots,c_{L-1}$ (todos broadcasteables a una forma común $(n_0,\dots,n_{k-1})$) y un array de índices `a` de esa misma forma, cada elemento de la salida es:

$$
\text{out}[\,\mathbf{i}\,] \;=\; c_{\,a[\mathbf{i}]}\,[\,\mathbf{i}\,] \qquad \text{con}\quad a[\mathbf{i}]\in\{0,\dots,L-1\}
$$

donde $\mathbf{i}=(i_0,\dots,i_{k-1})$ recorre todas las posiciones. El mapa de shapes es el de un [[concepto_broadcasting|broadcasting]] conjunto de `a` y de todos los `choices`:

$$
a.\text{shape},\ c_0.\text{shape},\dots,c_{L-1}.\text{shape}\ \xrightarrow{\ \text{broadcast}\ }\ (n_0,\dots,n_{k-1})\ =\ \text{out.shape}
$$

Visualmente, con $a=\begin{bmatrix}0 & 1\\ 1 & 0\end{bmatrix}$, $c_0=\begin{bmatrix}10 & 11\\ 12 & 13\end{bmatrix}$, $c_1=\begin{bmatrix}20 & 21\\ 22 & 23\end{bmatrix}$:

$$
\text{out}=\begin{bmatrix}c_0[0,0] & c_1[0,1]\\ c_1[1,0] & c_0[1,1]\end{bmatrix}=\begin{bmatrix}10 & 21\\ 22 & 13\end{bmatrix}
$$

## Firma

```python
np.choose(
    a,                 # array_like[int]: selector, índices en [0, len(choices)-1]
    choices,           # secuencia de array_like: los arrays candidatos
    out=None,          # ndarray: destino preasignado
    mode='raise',      # 'raise' | 'wrap' | 'clip': índices fuera de rango
) -> ndarray
```

## Los parámetros en detalle

### `a` — el selector de índices
`array_like` de **enteros** en `[0, len(choices)-1]`. Define, celda a celda, de qué array de `choices` se toma el valor. Se broadcastea con los candidatos.

### `choices` — la lista de arrays candidatos
Secuencia (lista/tupla) de `array_like` broadcasteables entre sí y con `a`. El **número** de candidatos fija el rango válido de `a`. Cada candidato aporta los valores de "su" categoría:

```python
a = np.array([0, 1, 1, 0])
choices = [np.array([10, 11, 12, 13]),    # opción 0
           np.array([20, 21, 22, 23])]    # opción 1
np.choose(a, choices)   # array([10, 21, 22, 13])
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape/dtype del resultado broadcasteado. Evita una asignación.

### `mode` — índices fuera de rango
Qué hacer cuando un valor de `a` no está en `[0, len(choices)-1]`:

| `mode` | Comportamiento |
|--------|----------------|
| `'raise'` (defecto) | lanza `ValueError` |
| `'wrap'` | da la vuelta (módulo `len(choices)`) |
| `'clip'` | recorta al candidato válido más cercano |

## El caso N-D

`a` y los `choices` se broadcastean **juntos** a una forma común; la salida tiene esa forma. El número de candidatos no es una dimensión: es la "profundidad" de la elección.

| `a.shape` | `choices` (cada uno) | salida |
|-----------|----------------------|--------|
| `(n,)` | `L` arrays `(n,)` | `(n,)` |
| `(r, c)` | `L` arrays `(r, c)` | `(r, c)` |
| `(r, c)` | `L` arrays `(1, c)` | `(r, c)` por broadcast |
| `()` escalar | `L` arrays `(r, c)` | `(r, c)` |

```python
a = np.array([[0, 1, 2],
              [2, 1, 0]])          # selector 2×3, 3 opciones
c0 = np.zeros((2, 3))
c1 = np.ones((2, 3))
c2 = np.full((2, 3), 9.0)
np.choose(a, [c0, c1, c2])
# array([[0., 1., 9.],
#        [9., 1., 0.]])  → cada celda toma de c0/c1/c2 según a
```

## Vectorización

`np.choose` reemplaza un bucle que, por cada celda, mira el índice y copia del candidato correcto:

```python
# Bucle Python (lento, explícito):
def elige(a, choices):
    out = np.empty_like(choices[0])
    for i in np.ndindex(a.shape):
        out[i] = choices[a[i]][i]
    return out

# Vectorizado (NumPy recorre las celdas en C, con broadcasting):
np.choose(a, choices)
```

Comparte el modelo de [[concepto_vectorizacion]]: describes la regla de selección, no el bucle. Frente a [[np.select]] (selección por **condiciones**) y [[np.where]] (una sola condición), `choose` es la vía cuando ya tienes el **índice entero** de la categoría.

## Valor de retorno

Siempre un `ndarray` con la forma del broadcasting conjunto de `a` y `choices`. El `dtype` es el resultado de la **promoción** de los `dtype` de los candidatos (p. ej. mezclar `int` y `float` da `float`).

| `a` | `choices` | salida (shape) | dtype |
|-----|-----------|----------------|-------|
| `(r, c)` | `L` arrays `(r, c)` int | `(r, c)` | int |
| `(r, c)` | mezcla int + float | `(r, c)` | float (promovido) |
| `(1, c)` | `L` arrays `(r, 1)` | `(r, c)` | promovido |

## Casos de uso

### Aplicar una paleta por categoría
```python
categoria = np.array([0, 2, 1, 0])       # etiqueta de cada punto
rojo   = np.full(4, 255)
verde  = np.full(4, 128)
azul   = np.full(4,  64)
np.choose(categoria, [rojo, verde, azul])  # array([255,  64, 128, 255])
```

### N-D: seleccionar por categoría en una rejilla
```python
clase = np.array([[0, 1],
                  [1, 0]])               # 2×2, 2 clases
fondo = np.zeros((2, 2))
objeto = np.arange(4).reshape(2, 2) + 1.0
np.choose(clase, [fondo, objeto])
# array([[0., 2.],
#        [3., 0.]])
```

### Escalar broadcasteado contra candidatos N-D
```python
np.choose(1, [np.zeros((2, 2)), np.ones((2, 2))])
# array([[1., 1.],
#        [1., 1.]])  → elige el candidato 1 entero
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `invalid entry in choice array` | índice de `a` ≥ `len(choices)` | validar, o `mode='clip'`/`'wrap'` |
| Resultado raro por broadcasting | shapes de `choices` no alinean con `a` | igualar/broadcastear las formas |
| Se buscaba selección por condición | `choose` quiere índices, no booleanos | usar [[np.select]] o [[np.where]] |
| Lento con muchas opciones | `choices` muy largo | usar [[np.take]] con fancy indexing |

## Notas relacionadas

- [[concepto_indexing]] — la familia de selección de la que `choose` forma parte
- [[concepto_broadcasting]] — `a` y los candidatos se alinean por broadcasting
- [[np.select]] — el análogo con condiciones booleanas en vez de índices
- [[np.take]] · [[np.where]]
