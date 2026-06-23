---
title: np.transpose — permuta (reordena) los ejes del array
aliases:
  - transpose
  - np.transpose
  - transponer
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

# np.transpose — permuta (reordena) los ejes del array

`np.transpose` **reordena los ejes** de un array según una permutación `axes`; por defecto los
**invierte todos**. No mueve ni un byte: reinterpreta el mismo buffer cambiando el orden de los
`strides`, así que devuelve una [[concepto_views_vs_copias|vista]] de coste $O(1)$. Es la
generalización N-D de "transponer una matriz": la pregunta no es "¿transpongo?" sino **"¿a qué
posición va cada eje?"**.

## La idea en una fórmula

Transponer es aplicar una permutación $\sigma$ a la tupla de ejes. Si `axes` define la permutación,
el shape se reordena según ella:

$$
(n_0, n_1, \dots, n_{k-1}) \;\xrightarrow{\ \text{transpose, axes}=\sigma\ }\; (n_{\sigma(0)}, n_{\sigma(1)}, \dots, n_{\sigma(k-1)})
$$

A nivel de elemento, el contenido no cambia: solo se reordenan los índices. La posición $(j_0,\dots,j_{k-1})$
de la salida lee la posición $(\dots)$ de la entrada cuyo índice $i_{\sigma(d)} = j_d$:

$$
B_{\,j_0,\dots,j_{k-1}} \;=\; A_{\,i_0,\dots,i_{k-1}} \quad\text{con}\quad j_d = i_{\sigma(d)}
$$

El **caso por defecto** (`axes=None`) es la inversión total $\sigma = (k-1,\dots,1,0)$. Para una
matriz $(m,n)$ eso intercambia filas y columnas:

$$
\begin{bmatrix} a & b & c \\ d & e & f \end{bmatrix} \;\xrightarrow{\ \text{.T}\ }\; \begin{bmatrix} a & d \\ b & e \\ c & f \end{bmatrix}
$$

## Firma

```python
np.transpose(
    a,            # array_like: el tensor de entrada
    axes=None,    # None | tuple[int] | list[int]: permutación de los ejes
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` de cualquier dimensión. Se convierte a `ndarray` si no lo es. Sobre un array **1D**
no hace nada útil: con un solo eje no hay nada que permutar (`(3,)` sigue siendo `(3,)`).

### `axes` — la permutación de ejes
Tupla (o lista) que es una **permutación de `range(ndim)`**: la posición `i` del resultado toma el
eje `axes[i]` del original. Cada eje debe aparecer **exactamente una vez**. Si es `None` (defecto),
invierte el orden completo de los ejes.

```python
T = np.ones((2, 3, 4))
np.transpose(T, (1, 0, 2)).shape   # (3, 2, 4)  → intercambia ejes 0 y 1
np.transpose(T, (2, 0, 1)).shape   # (4, 2, 3)  → lleva el último eje al frente
np.transpose(T, (2, 1, 0)).shape   # (4, 3, 2)  → equivale a None (inversión total)
```

Si `axes` no es una permutación válida (falta un eje, se repite, o hay un índice fuera de rango),
lanza `ValueError: axes don't match array`.

## El caso N-D

La regla es mecánica: **el eje `axes[i]` del original pasa a ocupar la posición `i`** en la salida.
El resto del array no se reorganiza en memoria; solo cambia el orden en que se interpretan los ejes.

| `a.shape` | `axes` | salida | lectura |
|-----------|--------|--------|---------|
| `(m, n)` | `None` | `(n, m)` | transpuesta clásica de matriz |
| `(2, 3, 4)` | `None` | `(4, 3, 2)` | invierte los tres ejes |
| `(2, 3, 4)` | `(0, 2, 1)` | `(2, 4, 3)` | intercambia los dos últimos |
| `(2, 3, 4)` | `(1, 0, 2)` | `(3, 2, 4)` | intercambia los dos primeros |
| `(2, 3, 4)` | `(2, 0, 1)` | `(4, 2, 3)` | rota: el último eje al frente |

```python
# Imagen RGB en formato HWC → CHW (canal al frente)
img = np.arange(2*2*3).reshape(2, 2, 3)   # (alto, ancho, canal)
chw = np.transpose(img, (2, 0, 1))        # (3, 2, 2)  canal, alto, ancho
chw.shape                                  # (3, 2, 2)
img[0, 1, 2] == chw[2, 0, 1]               # True  → mismo dato, índices reordenados
```

> [!note] No confundir con [[np.linalg.matrix_transpose]]
> `np.transpose` con `axes=None` **invierte TODOS** los ejes. Para lotes de matrices suele quererse
> intercambiar solo los **dos últimos** (transponer cada matriz del lote dejando intacto el eje de
> lote): eso lo hace [[np.linalg.matrix_transpose]] (o el atributo `.mT`), no `transpose`. En
> `(b, m, n)`, `transpose` da `(n, m, b)` pero `matrix_transpose` da `(b, n, m)`.

## Vista vs copia

`np.transpose` **siempre devuelve una vista**: reordenar ejes es exactamente reordenar la tupla de
`strides`, sin tocar el buffer (ver [[concepto_ndarray|strides]]). Por eso es $O(1)$ y por eso
**escribir en el resultado modifica el original**.

```python
M = np.arange(6).reshape(2, 3)
Mt = M.T
Mt.base is M          # True   → comparten buffer
Mt[0, 0] = 99
M[0, 0]               # 99     → la escritura se ve en el original
```

El resultado deja de ser C-contiguo (sus strides quedan reordenados). Si una librería externa exige
memoria contigua, fuerza la copia con `np.ascontiguousarray(resultado)` (ver
[[concepto_contiguidad_memoria]]).

## Valor de retorno

| Entrada | `axes` | salida (shape) | tipo |
|---------|--------|----------------|------|
| `(m, n)` | `None` | `(n, m)` | `ndarray` (vista) |
| `(n_0,\dots,n_{k-1})` | permutación $\sigma$ | `(n_{σ(0)},…,n_{σ(k-1)})` | `ndarray` (vista) |
| `(n,)` | cualquiera | `(n,)` | `ndarray` (vista, sin cambio) |

El `dtype` se conserva siempre. Nunca devuelve escalar.

## Casos de uso

### Transponer para una multiplicación matricial
```python
A = np.random.rand(3, 5)
B = np.random.rand(3, 5)
C = A.T @ B          # (5, 3) @ (3, 5) → (5, 5)
```

### El atajo `.T` (inversión total)
```python
M = np.array([[1, 2, 3], [4, 5, 6]])   # (2, 3)
M.T.shape                               # (3, 2)
# Ojo: en 1D no hace nada
np.array([1, 2, 3]).T.shape             # (3,)  → para una columna usa reshape(-1, 1)
```

### N-D: convención de imagen HWC → CHW
```python
img = np.random.rand(224, 224, 3)     # alto, ancho, canal
chw = np.transpose(img, (2, 0, 1))    # (3, 224, 224)  canal, alto, ancho
```

### Permutar solo dos ejes (existe alternativa más clara)
```python
T = np.ones((2, 3, 4))
np.transpose(T, (0, 2, 1)).shape   # (2, 4, 3)
# equivalente más legible: np.swapaxes(T, 1, 2)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `.T` no hace nada | el array es 1D (un solo eje) | `reshape(-1, 1)` o [[np.expand_dims]] para una columna |
| `ValueError: axes don't match array` | `axes` no es permutación de `range(ndim)` | incluir cada eje exactamente una vez |
| Se modificó el original al escribir | el retorno es una vista | `.copy()` si necesitas independencia |
| Otra función rompe por no contiguo | transpose deja strides reordenados | `np.ascontiguousarray(resultado)` |
| Se invirtieron todos los ejes sin querer | `axes=None` invierte TODO, no solo los 2 últimos | usar [[np.linalg.matrix_transpose]] o `.mT` para lotes |

## Notas relacionadas

- [[concepto_shape]] — el mapa de shapes de la permutación
- [[concepto_views_vs_copias]] — por qué es una vista
- [[concepto_contiguidad_memoria]] — el resultado deja de ser contiguo
- [[np.swapaxes]] — intercambiar exactamente dos ejes
- [[np.moveaxis]] — mover un eje conservando el orden del resto
- [[np.linalg.matrix_transpose]] — transponer solo los dos últimos ejes (lotes de matrices)
- [[np.reshape]]
