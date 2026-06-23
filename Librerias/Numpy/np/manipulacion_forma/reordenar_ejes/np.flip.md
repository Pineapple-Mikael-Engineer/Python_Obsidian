---
title: np.flip — invierte el orden de los elementos a lo largo de un eje
aliases:
  - flip
  - np.flip
  - voltear
  - invertir
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

draft: false
---

# np.flip — invierte el orden de los elementos a lo largo de un eje

`np.flip` **invierte el orden de los elementos** a lo largo de uno o varios ejes (`axis`). A
diferencia de [[np.transpose]] y compañía, **no reordena ejes**: el shape se conserva intacto, lo que
cambia es el *contenido*, que pasa a recorrerse al revés. Con `axis=None` voltea a lo largo de todos
los ejes. No copia: invertir un eje es negar su `stride` y mover el puntero al último elemento, así
que devuelve una [[concepto_views_vs_copias|vista]] de coste $O(1)$.

## La idea en una fórmula

El **shape se conserva**; lo que se invierte es el orden de los índices a lo largo de `axis`. Para un
flip sobre el eje $p$:

$$
(n_0, \dots, n_{k-1}) \;\xrightarrow{\ \text{flip, axis}=p\ }\; (n_0, \dots, n_{k-1}) \quad\text{(misma forma, contenido invertido)}
$$

A nivel de elemento, el índice del eje volteado se refleja ($i_p \to n_p - 1 - i_p$):

$$
B_{\,i_0,\dots,i_p,\dots} \;=\; A_{\,i_0,\dots,\,n_p - 1 - i_p,\,\dots}
$$

Sobre un vector, es simplemente leerlo de derecha a izquierda:

$$
\begin{bmatrix} a & b & c & d \end{bmatrix} \;\xrightarrow{\ \text{flip}\ }\; \begin{bmatrix} d & c & b & a \end{bmatrix}
$$

## Firma

```python
np.flip(
    a,           # array_like: el tensor de entrada
    axis=None,   # None | int | tuple[int]: eje(s) a invertir
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like` de cualquier dimensión. Se convierte a `ndarray` si no lo es.

### `axis` — qué eje(s) se invierten
`None` (defecto) invierte a lo largo de **todos** los ejes. Un `int` invierte solo ese eje. Una
**tupla** invierte varios a la vez. Admite ejes negativos. Es el parámetro central: define en qué
dirección se "voltea" el array.

```python
M = np.array([[1, 2, 3],
              [4, 5, 6]])
np.flip(M, axis=0)     # invierte las filas    → [[4,5,6],[1,2,3]]
np.flip(M, axis=1)     # invierte las columnas → [[3,2,1],[6,5,4]]
np.flip(M, axis=None)  # invierte todo         → [[6,5,4],[3,2,1]]
np.flip(M)             # axis=None por defecto  (idéntico al anterior)
```

> [!note] Atajos para 2D
> `np.fliplr(m)` invierte de izquierda a derecha (equivale a `np.flip(m, axis=1)`) y `np.flipud(m)`
> de arriba a abajo (equivale a `np.flip(m, axis=0)`). Solo son azúcar legible para matrices.

## El caso N-D

El shape **nunca cambia**: `flip` solo decide en qué dirección se recorre cada eje afectado. En un
tensor de imágenes esto sirve para reflejos (horizontal, vertical) sin reorganizar dimensiones.

| `a.shape` | `axis` | salida (shape) | lectura |
|-----------|--------|----------------|---------|
| `(n,)` | `0` o `None` | `(n,)` | vector al revés |
| `(m, n)` | `0` | `(m, n)` | filas en orden inverso (vertical) |
| `(m, n)` | `1` | `(m, n)` | columnas en orden inverso (horizontal) |
| `(m, n)` | `None` | `(m, n)` | ambos ejes invertidos (rotación 180°) |
| `(b, h, w, c)` | `2` | `(b, h, w, c)` | reflejo horizontal del lote de imágenes |

```python
# Lote de imágenes (b, alto, ancho, canal): reflejo horizontal
imgs = np.arange(2*2*2*3).reshape(2, 2, 2, 3)
flipped = np.flip(imgs, axis=2)          # invierte el eje ancho
flipped.shape                            # (2, 2, 2, 3)  → shape intacto
imgs[0, 0, 0, 0] == flipped[0, 0, -1, 0] # True  → el primer píxel pasa al último
```

## Vista vs copia

`np.flip` **devuelve una vista**: invertir un eje equivale a **negar su `stride`** y desplazar el
puntero de inicio al último elemento de ese eje (ver [[concepto_ndarray|strides]]). El buffer no se
toca, por eso es $O(1)$ y el resultado **comparte memoria** con `a`.

```python
v = np.arange(5)
r = np.flip(v)
r.base is v      # True
r[0] = 99
v[-1]            # 99  → mismo buffer, el "primero" de r es el último de v
```

El resultado no es C-contiguo (su stride es negativo); usa `.copy()` o `np.ascontiguousarray` si una
librería lo exige (ver [[concepto_contiguidad_memoria]]).

## Valor de retorno

| Entrada | `axis` | salida (shape) | tipo |
|---------|--------|----------------|------|
| `(n,)` | `0`/`None` | `(n,)` | `ndarray` (vista) |
| `(m, n)` | `int`/`tuple`/`None` | **igual a la entrada** | `ndarray` (vista) |
| `(n_0,\dots,n_{k-1})` | cualquiera | `(n_0,\dots,n_{k-1})` | `ndarray` (vista) |

El shape y el `dtype` **siempre se conservan**. Nunca devuelve escalar.

## Casos de uso

### Invertir un vector
```python
np.flip(np.array([1, 2, 3, 4]))   # [4, 3, 2, 1]
```

### Reflejo horizontal y vertical de una imagen 2D
```python
img = np.arange(9).reshape(3, 3)
np.fliplr(img)   # reflejo horizontal  (== np.flip(img, 1))
np.flipud(img)   # reflejo vertical    (== np.flip(img, 0))
np.flip(img)     # rotación 180°       (ambos ejes)
```

### N-D: voltear el eje temporal de una serie por lotes
```python
serie = np.random.rand(16, 100, 3)   # (lote, tiempo, canal)
inv = np.flip(serie, axis=1)         # (16, 100, 3)  cada serie del revés en el tiempo
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AxisError: axis N is out of bounds` | `axis` fuera de rango | usar ejes válidos (o negativos) |
| Se modificó el original | el retorno es una vista | `.copy()` si necesitas independencia |
| Otra función rompe por no contiguo / stride negativo | flip deja un stride negativo | `np.ascontiguousarray(resultado)` |
| Se esperaba reordenar ejes, no el contenido | `flip` conserva el shape; voltea elementos | usar [[np.transpose]] / [[np.moveaxis]] |

## Notas relacionadas

- [[concepto_shape]] — el shape se conserva; solo se invierte el contenido
- [[concepto_views_vs_copias]] — por qué es una vista (stride negativo)
- [[np.transpose]] — reordenar ejes (no el contenido)
- [[np.roll]] — desplazar circularmente (sin invertir)
