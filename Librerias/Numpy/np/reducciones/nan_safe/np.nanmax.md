---
title: np.nanmax — máximo (reduce) a lo largo de un eje, ignorando NaN
aliases:
  - nanmax
  - np.nanmax
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

# np.nanmax — máximo (reduce) a lo largo de un eje, ignorando NaN

`np.nanmax` es la variante **NaN-safe** de [[np.max]]: hace exactamente lo mismo —reduce un eje
quedándose con el **mayor** de sus elementos— pero **omite los `NaN`** en vez de propagarlos. Donde
`np.max([1, np.nan, 9])` da `nan` (cualquier `NaN` "gana" la comparación), `np.nanmax` los descarta y
devuelve `9.0`. Para todo lo demás —el sentido de `axis`, el mapa de shapes, `keepdims`— se comporta
igual que su gemela; esta nota se centra en el NaN y en sus trampas.

## La idea en una fórmula

El mapa de shapes es idéntico al de cualquier reducción (ver [[concepto_axis_parametro]]): el eje de
`axis` se elimina del shape.

$$
(n_0,\dots,n_k)\ \xrightarrow{\ \text{nanmax, axis}=p\ }\ (n_0,\dots,n_{p-1},\,n_{p+1},\dots,n_k)
$$

La única diferencia frente a [[np.max]] está en el conjunto sobre el que se maximiza: el máximo se
toma solo entre los elementos **no-NaN** del eje. Para una matriz $A$ de shape $(m, n)$, sobre el
eje `0`:

$$
M_j = \max_{\substack{i\in[0,m)\\ A_{ij}\,\neq\,\text{NaN}}} A_{ij} \qquad \text{(axis=0, desaparece el eje } i\text{)}
$$

Con `keepdims=True` el eje queda en tamaño 1; con `axis=None` se contraen todos los ejes a un escalar.

## Parámetros

Los mismos que [[np.max]] —`a`, `axis`, `out`, `keepdims`— con idéntica semántica; remito a esa nota
para el detalle de cada uno. `nanmax` **no** tiene `initial` ni `where` (a diferencia de `np.max`).

```python
np.nanmax(
    a,                 # array_like: el tensor de entrada
    axis=None,         # None | int | tuple[int]: eje(s) a reducir
    out=None,          # ndarray: destino preasignado
    keepdims=False,    # bool: conservar los ejes reducidos con tamaño 1
) -> ndarray | escalar
```

## NaN: el comportamiento clave

La regla normal: el `NaN` se **omite** del cálculo, como si no estuviera en el eje. El resto se
comporta como [[np.max]].

> [!warning] Slice todo-NaN → NaN + `RuntimeWarning`
> Si **todos** los elementos de un eje son `NaN`, no queda ningún candidato válido. `nanmax` no
> lanza error: devuelve `NaN` para ese slice y emite un `RuntimeWarning: All-NaN slice encountered`.
> Esto es importante porque el resultado **parece** un cálculo normal pero esconde un eje vacío de
> datos válidos.
> ```python
> np.nanmax([np.nan, np.nan])      # nan  + RuntimeWarning
> ```
> Es justo lo contrario de [[np.nanargmax]], que en el mismo caso lanza un **`ValueError`** (no hay
> índice que devolver).

## Ejemplos

### Pico ignorando huecos
```python
np.nanmax([1.0, np.nan, 9.0, 2.0])   # 9.0   (np.max daría nan)
```

### Reducción por eje con NaN salpicados
```python
A = np.array([[1., np.nan, 3.],
              [np.nan, 5., 2.]])
np.nanmax(A, axis=0)   # [1., 5., 3.]   máximo por columna, ignorando los NaN
np.nanmax(A, axis=1)   # [3., 5.]       máximo por fila
```

### N-D con un slice todo-NaN
```python
T = np.array([[[1., 8.], [np.nan, np.nan]],
              [[7., 4.], [6., 5.]]])     # shape (2, 2, 2)
np.nanmax(T, axis=2)
# [[ 8., nan],     ← la fila [nan, nan] da nan + RuntimeWarning
#  [ 7.,  6.]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `RuntimeWarning: All-NaN slice encountered` | un eje quedó **todo NaN** | filtrar esos ejes antes, o aceptar el `NaN` resultante |
| Se quería la **posición** del máximo válido | confundir valor con índice | usar [[np.nanargmax]] |
| El resultado sigue siendo `NaN` con `np.max` | se usó la gemela que **propaga** NaN | usar `np.nanmax` |
| Datos sin NaN, código más lento | `nanmax` hace un recorrido extra para enmascarar | usar [[np.max]] si se garantiza ausencia de NaN |

## Notas relacionadas

- [[concepto_axis_parametro]] — qué eje se colapsa y cómo queda el shape
- [[np.max]] — la gemela que **propaga** NaN; el comportamiento base de la reducción
- [[np.nanmin]] · [[np.nanargmax]] · [[Librerias/Numpy/np/reducciones/nan_safe/index|variantes nan-safe]]
