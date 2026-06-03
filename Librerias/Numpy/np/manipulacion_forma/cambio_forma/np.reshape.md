---
title: np.reshape — Cambiar la forma sin alterar los datos
aliases:
  - reshape
  - np.reshape
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

# np.reshape — Cambiar la forma sin alterar los datos

## Firma de la función

```python
np.reshape(
    a,
    newshape,
    order='C'
) -> ndarray
```

## Valor de retorno

Devuelve un [[concepto_ndarray|ndarray]] con el nuevo [[concepto_shape|shape]] y **los mismos datos**. Casi siempre es una [[concepto_views_vs_copias|vista]] (comparte memoria); solo copia si el array no es contiguo y el nuevo orden lo exige.

| Entrada | newshape | Salida |
|---------|----------|--------|
| `arange(12)` | `(3, 4)` | matriz 3×4 |
| `arange(12)` | `(2, 6)` | matriz 2×6 |
| `arange(12)` | `(2, 2, 3)` | tensor 2×2×3 |
| `arange(12)` | `(-1, 4)` | `(3, 4)` (dim inferida) |

```python
import numpy as np
np.reshape(np.arange(6), (2, 3))
# array([[0, 1, 2],
#        [3, 4, 5]])
```

## Regla fundamental

> El producto de las dimensiones debe conservarse: `producto(newshape) == a.size`.

```python
np.arange(12).reshape(3, 4)   # OK  → 3*4 = 12
np.arange(12).reshape(3, 5)   # ValueError → 15 != 12
```

## Parámetros en detalle

### `a` — array de entrada

El array a reinterpretar. No se modifica.

### `newshape` — forma destino

Entero o tupla. Una de las dimensiones puede ser `-1` y NumPy la **infiere** a partir del resto:

```python
arr = np.arange(12)
arr.reshape(3, -1)    # NumPy deduce 4 → (3, 4)
arr.reshape(-1, 6)    # NumPy deduce 2 → (2, 6)
arr.reshape(-1)       # aplana a (12,)
```

Solo se permite **un** `-1` por llamada.

### `order` — orden de lectura/escritura

| Valor | Significado |
|-------|-------------|
| `'C'` (por defecto) | recorre por filas (última dimensión primero) |
| `'F'` | recorre por columnas (estilo Fortran) |
| `'A'` | `'F'` si el array es Fortran-contiguo, si no `'C'` |

```python
a = np.arange(6)
a.reshape(2, 3, order='C')   # [[0,1,2],[3,4,5]]
a.reshape(2, 3, order='F')   # [[0,2,4],[1,3,5]]
```

## Método equivalente

Existe como método del array, forma más habitual en la práctica:

```python
arr.reshape(3, 4)        # método (admite enteros sueltos)
np.reshape(arr, (3, 4))  # función
```

## Casos de uso

### Convertir un vector en matriz

```python
datos = np.arange(1, 13)          # (12,)
tabla = datos.reshape(3, 4)       # 3 filas, 4 columnas
```

### Aplanar para procesar y volver a la forma

```python
img = np.random.rand(28, 28)
plano = img.reshape(-1)           # (784,) para una capa densa
vuelta = plano.reshape(28, 28)    # recuperar la imagen
```

### Añadir un eje de tamaño 1 (alternativa a expand_dims)

```python
v = np.arange(3)
v.reshape(1, -1)   # (1, 3) fila
v.reshape(-1, 1)   # (3, 1) columna
```

## Buenas prácticas

1. Usa `-1` para no calcular dimensiones a mano y reducir errores.
2. Recuerda que devuelve una **vista**: modificar el resultado puede alterar el original.
3. Para garantizar independencia, añade `.copy()`.
4. Para añadir o quitar ejes de tamaño 1, [[np.expand_dims]] y [[np.squeeze]] son más expresivos.
5. Si necesitas un aplanado explícito, [[np.ravel]] comunica mejor la intención.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `cannot reshape array of size N into shape (...)` | `producto(newshape) != size` | ajustar dimensiones o usar `-1` |
| `can only specify one unknown dimension` | dos `-1` en `newshape` | dejar solo uno |
| El original cambió inesperadamente | era una vista | usar `.copy()` |
| Orden de elementos no esperado | `order` por defecto `'C'` | revisar `order='F'` si vienes de Fortran/MATLAB |

## Limitaciones

- No puede cambiar el número total de elementos: para eso está [[np.resize]] (que copia y rellena).
- Devuelve copia (no vista) si el array no es contiguo en el `order` pedido.
- No reordena datos físicamente; solo reinterpreta los `strides`.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_views_vs_copias]]
- [[np.ravel]]
- [[np.expand_dims]]
- [[np.squeeze]]
- [[np.transpose]]
