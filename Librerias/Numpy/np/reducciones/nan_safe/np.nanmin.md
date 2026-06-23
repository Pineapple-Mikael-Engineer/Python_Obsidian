---
title: np.nanmin — mínimo (reduce) a lo largo de un eje, ignorando NaN
aliases:
  - nanmin
  - np.nanmin
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray | escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro

draft: false
---

# np.nanmin — mínimo (reduce) a lo largo de un eje, ignorando NaN

`np.nanmin` es la variante **NaN-safe** de [[np.min]]: hace lo mismo —reduce un eje quedándose con el
**menor** de sus elementos— pero **omite los `NaN`** en vez de propagarlos. Donde
`np.min([3, np.nan, 1])` da `nan`, `np.nanmin` los descarta y devuelve `1.0`. El sentido de `axis`,
el mapa de shapes y `keepdims` son los de su gemela; esta nota se centra en el NaN y sus trampas.

## La idea en una fórmula

El mapa de shapes es el de cualquier reducción (ver [[concepto_axis_parametro]]): el eje de `axis`
se elimina del shape.

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{nanmin, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

La única diferencia frente a [[np.min]] es el conjunto sobre el que se minimiza: el mínimo se toma
solo entre los elementos **no-NaN** del eje. Para una matriz $A$ de shape $(m, n)$, sobre el eje `0`:

$$
m_j = \min_{\substack{i\in[0,m)\\ A_{ij}\,\neq\,\text{NaN}}} A_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

Con `keepdims=True` el eje queda en tamaño 1; con `axis=None` se contraen todos los ejes a un escalar.

## Parámetros

Los mismos que [[np.min]] —`a`, `axis`, `out`, `keepdims`— con idéntica semántica; remito a esa nota
para el detalle. `nanmin` **no** tiene `initial` ni `where` (a diferencia de `np.min`).

```python
np.nanmin(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    out=None,          # ndarray: destino preasignado
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
) -> ndarray | escalar
```

## NaN: el comportamiento clave

La regla normal: el `NaN` se **omite** del cálculo, como si no estuviera en el eje. El resto se
comporta como [[np.min]].

> [!warning] Slice todo-NaN → NaN + `RuntimeWarning`
> Si **todos** los elementos de un eje son `NaN`, no queda ningún candidato válido. `nanmin` no
> lanza error: devuelve `NaN` para ese slice y emite un `RuntimeWarning: All-NaN slice encountered`.
> El resultado **parece** un cálculo normal pero esconde un eje sin datos válidos.
> ```python
> np.nanmin([np.nan, np.nan])      # nan  + RuntimeWarning
> ```
> Es lo contrario de [[np.nanargmin]], que en el mismo caso lanza un **`ValueError`** (no hay índice
> que devolver).

## Ejemplos

### Suelo ignorando huecos
```python
np.nanmin([3.0, np.nan, 1.0, 2.0])   # 1.0   (np.min daría nan)
```

### Reducción por eje con NaN salpicados
```python
A = np.array([[3., np.nan, 1.],
              [np.nan, 5., 4.]])
np.nanmin(A, axis=0)   # [3., 5., 1.]   mínimo por columna, ignorando los NaN
np.nanmin(A, axis=1)   # [1., 4.]       mínimo por fila
```

### N-D con un slice todo-NaN
```python
T = np.array([[[1., 8.], [np.nan, np.nan]],
              [[7., 4.], [6., 5.]]])     # shape (2, 2, 2)
np.nanmin(T, axis=2)
# [[ 1., nan],     ← la fila [nan, nan] da nan + RuntimeWarning
#  [ 4.,  5.]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: All-NaN slice encountered` | un eje quedó **todo NaN** | filtrar esos ejes antes, o aceptar el `NaN` resultante |
| Se quería la **posición** del mínimo válido | confundir valor con índice | usar [[np.nanargmin]] |
| El resultado sigue siendo `NaN` con `np.min` | se usó la gemela que **propaga** NaN | usar `np.nanmin` |
| Datos sin NaN, código más lento | `nanmin` hace un recorrido extra para enmascarar | usar [[np.min]] si se garantiza ausencia de NaN |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se colapsa y cómo queda el shape
- [[np.min]] — la gemela que **propaga** NaN; el comportamiento base de la reducción
- [[np.nanmax]] · [[np.nanargmin]] · [[Librerias/Numpy/np/reducciones/nan_safe/index|variantes nan-safe]]
