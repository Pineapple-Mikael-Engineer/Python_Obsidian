---
title: np/manipulacion_forma/cambio_forma — nueva forma sin copiar datos
tags:
  - numpy
  - indice
draft: false
---

# np/manipulacion_forma/cambio_forma — nueva forma sin copiar datos

Cambiar la `shape` de un array sin alterar sus elementos ni su orden lineal. Las cuatro funciones de esta carpeta reinterpretan el mismo buffer de memoria bajo un esquema diferente de filas, columnas o dimensiones. El resultado es una **vista** en la gran mayoria de casos — modificar el resultado modifica el original, y viceversa.

La regla de oro que ninguna de estas funciones puede violar: el numero total de elementos debe ser identico antes y despues. `(3, 4)` puede convertirse en `(2, 6)`, `(12,)` o `(1, 3, 4)`, pero nunca en `(3, 5)`. Cualquier violacion lanza `ValueError`.

## Cuando se genera una copia

Una vista solo es posible cuando el array es **C-contiguo** (layout por filas, el default de NumPy) o **F-contiguo** (layout Fortran). Si el array resulto de una operacion de indexado no basica — por ejemplo `a[::2]` — sus strides no permiten representar el nuevo shape sin reorganizar datos. En ese caso NumPy genera silenciosamente una copia. Para detectarlo: `np.shares_memory(a, b)`.

## Funciones

### [[np.reshape]] — forma arbitraria

La navaja suiza de este grupo. Acepta cualquier nueva shape compatible con el numero de elementos. La dimension `-1` se calcula automaticamente: `a.reshape(3, -1)` en un array de 12 elementos produce `(3, 4)`. El parametro `order` controla si se recorren los elementos en orden C (filas primero, default) o Fortran (columnas primero).

### [[np.ravel]] — aplanar a 1D

Devuelve una vista 1D del array recorriendo sus elementos en el orden indicado por `order` (default: C). Es equivalente a `a.reshape(-1)` pero expresa la intencion con mas claridad: "quiero un array plano". Devuelve copia cuando el array no es contiguo en el orden solicitado.

### [[np.squeeze]] — eliminar dimensiones de tamano 1

Elimina todas las dimensiones de longitud 1 de la shape. Un array `(1, 5, 1)` se convierte en `(5,)`. Se puede especificar `axis` para eliminar solo dimensiones concretas en vez de todas. Util para limpiar el output de funciones que devuelven shapes infladas innecesariamente. **Peligro**: si no se controla que dimensiones se eliminan, puede cambiar el numero de ejes de forma inesperada.

### [[np.expand_dims]] — insertar una dimension de tamano 1

El inverso de `squeeze`: inserta una dimension de longitud 1 en la posicion `axis`. `np.expand_dims(a, 0)` sobre un vector `(5,)` produce `(1, 5)`. Es equivalente a `a[np.newaxis, :]` pero mas explicito cuando se trabaja con `axis` como variable. Muy usado para adaptar un vector a operaciones de broadcasting que esperan una matriz fila o columna.

## Tabla de funciones

| Funcion | Shape de entrada | Shape de salida | Vista si posible |
|---------|-----------------|-----------------|------------------|
| [[np.reshape]] | Cualquiera | Cualquiera compatible | Si |
| [[np.ravel]] | Cualquiera | `(n,)` plano | Si |
| [[np.squeeze]] | Con dimensiones de tamano 1 | Sin dimensiones de tamano 1 | Si |
| [[np.expand_dims]] | Cualquiera | Una dimension mas de tamano 1 | Si |

## Patron comun: preparar arrays para broadcasting

```python
import numpy as np

a = np.array([1, 2, 3])     # shape (3,)
b = np.array([10, 20])      # shape (2,)

# Sin reshape: error de broadcasting
# Con reshape: suma exterior
a_col = a.reshape(-1, 1)    # shape (3, 1)
result = a_col + b           # shape (3, 2) — broadcasting valido
```

`expand_dims` es la alternativa mas legible para este patron cuando el eje es variable.
