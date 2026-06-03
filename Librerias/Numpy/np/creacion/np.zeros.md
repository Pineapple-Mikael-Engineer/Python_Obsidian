---
title: np.zeros — Array inicializado a ceros
aliases:
  - zeros
  - np.zeros
tags:
  - numpy
  - api/funcion
  - creacion

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
  - concepto_dtype

draft: false
---

# np.zeros — Array inicializado a ceros

## Firma de la función

```python
np.zeros(
    shape,
    dtype=float,
    order='C',
    *,
    like=None
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] del `shape` indicado con todos sus elementos a `0`. El `dtype` por defecto es `float64`.

| Llamada | Shape | dtype | Contenido |
|---------|-------|-------|-----------|
| `np.zeros(3)` | `(3,)` | `float64` | `[0., 0., 0.]` |
| `np.zeros((2, 3))` | `(2, 3)` | `float64` | matriz de ceros |
| `np.zeros(3, dtype=int)` | `(3,)` | `int64` | `[0, 0, 0]` |
| `np.zeros((2, 2), dtype=bool)` | `(2, 2)` | `bool` | `[[False, False], ...]` |

```python
import numpy as np
np.zeros((2, 3))
# array([[0., 0., 0.],
#        [0., 0., 0.]])
```

## Parámetros en detalle

### `shape` — forma del array

Entero para 1D, o tupla para nD. Define el [[concepto_shape|shape]] exacto. Es el único parámetro obligatorio.

```python
np.zeros(5)         # (5,)   vector
np.zeros((3, 4))    # (3, 4) matriz
np.zeros((2, 3, 4)) # (2, 3, 4) tensor
```

### `dtype` — tipo de los ceros

A diferencia de la mayoría de funciones, **el defecto es `float`**, no entero. Especifícalo si necesitas otro tipo (ver [[concepto_dtype]]).

```python
np.zeros(3).dtype              # float64
np.zeros(3, dtype=np.int8)     # [0, 0, 0] en int8
np.zeros(2, dtype=complex)     # [0.+0.j, 0.+0.j]
```

### `order` — disposición en memoria

`'C'` (filas contiguas, por defecto) o `'F'` (columnas contiguas). Solo relevante en 2D+ por rendimiento. Ver [[concepto_contiguidad_memoria]].

## Casos de uso

### Preasignar antes de un bucle de llenado

```python
n = 1000
resultado = np.zeros(n)          # reservar memoria una sola vez
for i in range(n):
    resultado[i] = i ** 2        # llenar in-place
```

### Acumulador para sumas

```python
acumulado = np.zeros((3, 3))
for matriz in lista_de_matrices:
    acumulado += matriz          # parte de cero
```

### Máscara o lienzo en blanco

```python
lienzo = np.zeros((100, 100), dtype=np.uint8)   # imagen negra 100x100
```

## Buenas prácticas

1. Úsalo para **preasignar** y luego llenar; evita crecer arrays dinámicamente.
2. Recuerda que el defecto es `float`: pon `dtype=int` si trabajas con enteros.
3. Para copiar el shape/dtype de otro array, usa [[np.zeros_like]].
4. Si necesitas otro valor constante distinto de 0, usa [[np.full]].
5. Para un array sin inicializar (más rápido si vas a sobreescribir todo), considera [[np.empty]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Floats donde esperabas ints | dtype por defecto es `float` | `np.zeros(n, dtype=int)` |
| `TypeError` con varios argumentos | `np.zeros(2, 3)` interpreta `3` como dtype | usar tupla: `np.zeros((2, 3))` |
| Memoria alta | `float64` por defecto | declarar dtype menor |

## Limitaciones

- Inicializar a cero tiene un coste; si vas a sobreescribir cada elemento, [[np.empty]] evita ese paso.
- No genera secuencias ni patrones: para eso están [[np.arange]] y [[np.linspace]].

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_dtype]]
- [[np.ones]]
- [[np.full]]
- [[np.empty]]
- [[np.zeros_like]]
- [[np.array]]
