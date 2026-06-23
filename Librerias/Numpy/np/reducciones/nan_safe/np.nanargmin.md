---
title: np.nanargmin — índice (no valor) del mínimo a lo largo de un eje, ignorando NaN
aliases:
  - nanargmin
  - np.nanargmin
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | int
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_indexing

draft: false
---

# np.nanargmin — índice (no valor) del mínimo a lo largo de un eje, ignorando NaN

`np.nanargmin` es la variante **NaN-safe** de [[np.argmin]]: colapsa un eje y devuelve el **índice
entero** del mínimo, pero busca ese mínimo **ignorando los `NaN`**. Donde
`np.argmin([np.nan, 5, 1])` puede apuntar al `NaN` y devolver `0`, `nanargmin` lo descarta y devuelve
`2` (la posición del `1`). El sentido de `axis`, el mapa de shapes y la interpretación del índice
(referido al eje, o **aplanado** con `axis=None`) son los de su gemela; esta nota se centra en el NaN
y su trampa, que aquí es **más severa** que en [[np.nanmin]].

## La idea en una fórmula

El mapa de shapes es el de cualquier reducción que devuelve índices (ver [[concepto_axis_parametro]]):
el eje de `axis` desaparece y los valores de salida son índices en el rango del eje reducido.

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{nanargmin, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
\quad\text{con valores en } [0,\,n_p)
$$

La diferencia frente a [[np.argmin]] es que el `\arg\min` se toma solo entre los elementos **no-NaN**.
Para una matriz $A$ de shape $(m, n)$, sobre el eje `0`:

$$
\text{nanargmin}_j \;=\; \arg\min_{\substack{i\in[0,m)\\ A_{ij}\,\neq\,\text{NaN}}} A_{ij}
\qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

Con `axis=None` (defecto) aplana primero y devuelve un único índice escalar sobre el array 1D.

## Parámetros

Los mismos que [[np.argmin]] —`a`, `axis` (un solo eje, no acepta tupla), `out`, `keepdims`— con
idéntica semántica; remito a esa nota para el detalle y para la traducción del índice aplanado con
`np.unravel_index` (ver [[concepto_indexing]]).

```python
np.nanargmin(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int: eje a lo largo del cual buscar el mínimo
    out=None,          # ndarray: destino preasignado (dtype entero)
    *,
    keepdims=False,    # bool: conservar el eje reducido con tamaño 1
) -> ndarray | intp
```

## NaN: el comportamiento clave

La regla normal: el `NaN` se **omite** de la búsqueda, así que el índice devuelto nunca apunta a un
`NaN`. El resto se comporta como [[np.argmin]] (empates: gana el primero).

> [!danger] Slice todo-NaN → `ValueError` (¡no es un warning!)
> Aquí está la trampa que **distingue** a `nanargmin` de [[np.nanmin]]. Si **todos** los elementos
> de un eje son `NaN`, no existe ningún índice válido que devolver —no hay mínimo entre cero
> candidatos—, así que `nanargmin` **lanza un `ValueError: All-NaN slice encountered`**. No es un
> `RuntimeWarning` recuperable como en `nanmin`: es un **error** que aborta la llamada.
> ```python
> np.nanargmin([np.nan, np.nan])   # ValueError: All-NaN slice encountered
> np.nanmin([np.nan, np.nan])      # nan  (solo warning) — comportamiento distinto
> ```
> En un array N-D basta con que **un solo** slice del eje reducido sea todo-NaN para que toda la
> llamada falle. Filtra o valida esos ejes antes.

## Ejemplos

### Índice del mínimo válido
```python
np.nanargmin([np.nan, 5.0, 1.0, 3.0])   # 2   (np.argmin podría dar 0, el NaN)
```

### Recuperar el valor desde el índice
```python
arr = np.array([3., np.nan, 1., 2.])
i = np.nanargmin(arr)   # 2
arr[i]                  # 1.0
```

### Reducción por eje (sin slices todo-NaN)
```python
A = np.array([[3., np.nan, 1.],
              [np.nan, 5., 4.]])
np.nanargmin(A, axis=0)   # [0, 1, 0]   por columna: qué fila gana, ignorando NaN
np.nanargmin(A, axis=1)   # [2, 1]      por fila: qué columna gana
```

### N-D con un slice todo-NaN → falla
```python
T = np.array([[[1., 8.], [np.nan, np.nan]],
              [[7., 4.], [6., 5.]]])     # shape (2, 2, 2)
np.nanargmin(T, axis=2)
# ValueError: All-NaN slice encountered  ← la fila [nan, nan] no tiene índice válido
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: All-NaN slice encountered` | un eje (o un slice en N-D) quedó **todo NaN** | filtrar/validar esos ejes **antes**; no es recuperable como en `nanmin` |
| Índice "raro" en 2D+ | con `axis=None` el índice es **aplanado**, no fila/columna | `np.unravel_index(idx, a.shape)` |
| Se esperaba el **valor**, no la posición | `nanargmin` devuelve el índice | indexar `a[idx]` o usar [[np.nanmin]] |
| El índice apunta a un `NaN` con `np.argmin` | se usó la gemela que **no** ignora NaN | usar `np.nanargmin` |
| `axis=(0, 1)` falla | `nanargmin` **no** acepta tupla de ejes | reducir un solo eje, o sobre el aplanado |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se colapsa y cómo queda el shape
- [[concepto_indexing]] — `np.unravel_index` para traducir el índice aplanado
- [[np.argmin]] — la gemela que **no** ignora NaN (su índice puede apuntar a un NaN)
- [[np.nanmin]] · [[np.nanargmax]] · [[Librerias/Numpy/np/reducciones/nan_safe/index|variantes nan-safe]]
