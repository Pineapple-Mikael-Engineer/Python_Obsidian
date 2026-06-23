---
title: np.clip — recorta (satura) los valores a un rango
aliases:
  - clip
  - np.clip
  - recortar
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_broadcasting
  - concepto_vectorizacion

draft: false
---

# np.clip — recorta (satura) los valores a un rango

`np.clip` fuerza cada valor de `a` dentro del intervalo $[a_{min}, a_{max}]$: lo que cae por debajo se sube a $a_{min}$, lo que cae por encima se baja a $a_{max}$, el resto se deja igual. Es una operación elemento a elemento que **conserva el shape** y solo *satura* los extremos. La idea en una frase: **acotar sin filtrar** — ningún elemento se elimina, solo se fija a los bordes.

## La idea en una fórmula

Para cada elemento $x_i$ de `a`, con límites $a_{min}$ y $a_{max}$:

$$
z_i \;=\; \min\!\big(\max(x_i,\ a_{min}),\ a_{max}\big)
\;=\;
\begin{cases}
a_{min} & x_i < a_{min}\\
x_i & a_{min}\le x_i\le a_{max}\\
a_{max} & x_i > a_{max}
\end{cases}
$$

Al ser elemento a elemento, el **shape se conserva** exactamente (salvo broadcasting de los límites):

$$
(n_0,\dots,n_{k-1})\ \xrightarrow{\ \text{clip}\ }\ (n_0,\dots,n_{k-1})
$$

Si $a_{min}$/$a_{max}$ son arrays, se [[concepto_broadcasting|broadcastean]] contra `a` y el rango puede ser **distinto por elemento**.

## Firma

```python
np.clip(
    a,                 # array_like: el tensor a recortar
    a_min,             # escalar | array_like | None: límite inferior (None = sin tope inferior)
    a_max,             # escalar | array_like | None: límite superior (None = sin tope superior)
    out=None,          # ndarray: destino (out=a recorta in-place)
    **kwargs,          # where, casting, order... (semántica de ufunc)
) -> ndarray
```

## Los parámetros en detalle

### `a` — el tensor de entrada
`array_like`. Se convierte a `ndarray` si no lo es. Solo se modifican los valores que caen fuera del rango.

### `a_min`, `a_max` — los límites del intervalo
Escalares, `array_like` (broadcasteables con `a`) o `None`. Un `None` **desactiva** ese extremo, dejando una saturación de un solo lado:

```python
a = np.array([-3, 0, 4, 9])
np.clip(a, 0, None)    # array([0, 0, 4, 9])  → solo piso (equiv. ReLU)
np.clip(a, None, 5)    # array([-3, 0, 4, 5])  → solo techo
```

Si ambos son arrays, el rango es **por elemento**:

```python
minimos = np.array([0, 1, 2, 3])
np.clip(a, minimos, 5)   # cada posición tiene su propio mínimo
```

> [!warning] Rango invertido
> Si `a_min > a_max`, el resultado es el valor de `a_max` en todas partes (el `max` interior y luego el `min` colapsan): no lanza error, simplemente da basura. Asegura `a_min <= a_max`.

### `out` — escribir en un buffer existente
`ndarray` con el shape del resultado. Con `out=a` el recorte es **in-place** (sobrescribe el original, sin copia extra):

```python
np.clip(a, 0, 1, out=a)   # modifica a directamente
```

### `**kwargs` (`where`, `casting`, `order`…)
`np.clip` es una ufunc, así que admite los keywords estándar. El más útil es `where` (array booleano broadcasteable): solo recorta donde es `True`, dejando intactas las demás posiciones de `out`.

## El caso N-D

`clip` es elemento a elemento: el shape de la salida es **igual** al de `a` (tras broadcastear los límites). No hay ejes que colapsen ni reordenar.

| `a.shape` | `a_min` / `a_max` | salida |
|-----------|-------------------|--------|
| `(n,)` | escalares | `(n,)` |
| `(r, c)` | escalares | `(r, c)` |
| `(r, c)` | `a_min` de shape `(c,)` | `(r, c)` (broadcast por columna) |
| `(b, r, c)` | escalares | `(b, r, c)` |

```python
# Tensor (lote, alto, ancho) de "imágenes"
img = np.array([[[-20, 300],
                 [120,  50]]])     # shape (1, 2, 2)
np.clip(img, 0, 255)
# array([[[  0, 255],
#         [120,  50]]])  → mismo shape, solo se saturan extremos
```

## Vectorización

`np.clip` reemplaza un bucle con dos comparaciones por elemento. Como ufunc, recorre el tensor en C:

```python
# Bucle Python (lento, explícito):
def recorta(a, lo, hi):
    out = a.copy()
    for i in np.ndindex(a.shape):
        if   out[i] < lo: out[i] = lo
        elif out[i] > hi: out[i] = hi
    return out

# Vectorizado (ufunc: min(max(...)) sobre todo el array en C):
np.clip(a, lo, hi)
```

Equivale a `np.minimum(np.maximum(a, a_min), a_max)`, pero en una sola pasada. Mismo modelo de [[concepto_vectorizacion]]: describes el rango, no el recorrido.

## Valor de retorno

Siempre un `ndarray` con el **mismo shape** que `a` (tras broadcasting de los límites). El `dtype` se **conserva** —`clip` no promueve—, lo que tiene una trampa: recortar enteros con un límite float **no** convierte el resultado a float; castea tú si lo necesitas.

| Entrada (shape, dtype) | límites | salida (shape) | dtype |
|------------------------|---------|----------------|-------|
| `(r, c)` int | escalares int | `(r, c)` | int (conservado) |
| `(r, c)` int | float | `(r, c)` | int (truncado, **no** promueve) |
| `(r, c)` float | escalares | `(r, c)` | float |
| `(n,)` | `a_min` array `(n,)` | `(n,)` | el de `a` |

## Casos de uso

### Mantener valores en un rango válido
```python
pixeles = np.clip(pixeles, 0, 255).astype(np.uint8)   # imagen válida
probs   = np.clip(probs, 1e-7, 1 - 1e-7)              # evitar log(0)
```

### ReLU (rectificación)
```python
np.clip(x, 0, None)   # equivale a max(0, x)
```

### N-D: saturar un tensor con límites por canal
```python
# (alto, ancho, canal): límite superior distinto por canal RGB
img = np.array([[[300, 100,  50]]])     # shape (1, 1, 3)
tope = np.array([255, 200, 128])        # uno por canal → broadcast
np.clip(img, 0, tope)
# array([[[255, 100,  50]]])  → el rojo se satura a 255, el resto no
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado constante absurdo | `a_min > a_max` (rango invertido) | asegurar `a_min <= a_max` |
| El dtype no cambia al recortar con float | `clip` conserva el dtype de `a` | castear con `.astype(...)` |
| Se buscaba filtrar valores | `clip` **fija** al borde, no elimina | usar máscaras / [[np.where]] |
| Solo un extremo recortado | el otro límite quedó como valor real, no `None` | pasar `None` para desactivarlo |

## Notas relacionadas

- [[concepto_broadcasting]] — límites array recortan con rango por elemento
- [[concepto_vectorizacion]] — `clip` es una ufunc que recorre en C
- [[np.minimum]] · [[np.maximum]] — las piezas que `clip` combina
- [[np.where]] · [[np.select]]
