---
title: np.sum — Suma de elementos a lo largo de un eje
aliases:
  - sum
  - np.sum
  - suma
tags:
  - numpy
  - api/funcion
  - reducciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray o escalar
inplace: false

# --- Dependencias ---
requiere:
  - concepto_axis_parametro
  - concepto_dtype

draft: false
---

# np.sum — Suma de elementos a lo largo de un eje

## Firma de la función

```python
np.sum(
    a,
    axis=None,
    dtype=None,
    out=None,
    keepdims=False,
    initial=0,
    where=True
) -> ndarray | escalar
```

## Valor de retorno

Suma los elementos de `a`. El [[concepto_axis_parametro|eje]] indicado se **colapsa**; con `axis=None` (por defecto) suma todo y devuelve un escalar.

| Entrada | `axis` | Salida |
|---------|--------|--------|
| `(2, 3)` | `None` | escalar (suma total) |
| `(2, 3)` | `0` | `(3,)` (suma por columna) |
| `(2, 3)` | `1` | `(2,)` (suma por fila) |

```python
import numpy as np
M = np.array([[1, 2, 3],
              [4, 5, 6]])
np.sum(M)          # 21
np.sum(M, axis=0)  # [5, 7, 9]
np.sum(M, axis=1)  # [6, 15]
```

## Parámetros en detalle

### `a` — array de entrada

Array o secuencia de números.

### `axis` — eje a sumar

Entero, tupla de enteros o `None`. Recuerda: el eje indicado **desaparece** del shape resultado (ver [[concepto_axis_parametro]]).

```python
T = np.ones((2, 3, 4))
np.sum(T, axis=(0, 2)).shape   # (3,)  → suma sobre dos ejes
```

### `dtype` — tipo del acumulador

Controla el [[concepto_dtype|dtype]] de la suma. Clave para evitar **overflow** con enteros pequeños:

```python
arr = np.ones(1000, dtype=np.int8)
np.sum(arr)                  # puede desbordar el acumulador
np.sum(arr, dtype=np.int64)  # acumulador seguro
```

### `keepdims` — conservar dimensiones

Si `True`, el eje reducido se mantiene con tamaño 1, útil para [[concepto_broadcasting|broadcasting]] posterior.

```python
M = np.array([[1, 2], [3, 4]])
M / np.sum(M, axis=1, keepdims=True)   # normaliza cada fila
```

### `where` — suma condicional

Máscara booleana: suma solo donde `where` es `True`.

```python
arr = np.array([1, -2, 3, -4])
np.sum(arr, where=arr > 0)   # 4  → solo positivos
```

## Casos de uso

### Total y subtotales

```python
ventas = np.array([[100, 200], [150, 250]])
np.sum(ventas)            # 700  total
np.sum(ventas, axis=0)    # [250, 450]  por producto
```

### Contar elementos que cumplen una condición

```python
datos = np.array([1, 5, 2, 8, 3])
np.sum(datos > 3)   # 2  → True cuenta como 1
```

## Buenas prácticas

1. Con enteros de pocos bits, fija `dtype` para evitar overflow silencioso.
2. Usa `keepdims=True` cuando vayas a dividir/restar el resultado del array original.
3. `np.sum(mascara)` es el idioma para **contar** condiciones (True=1).
4. Si hay NaN, usa [[np.nansum]] para ignorarlos en lugar de propagar NaN.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultado erróneo por overflow | acumulador de pocos bits | `dtype=np.int64` |
| `NaN` en el resultado | el array contiene NaN | usar [[np.nansum]] |
| Broadcasting falla tras sumar | se perdió el eje | `keepdims=True` |
| Sentido de `axis` invertido | confundir filas/columnas | recordar: el eje indicado se colapsa |

## Limitaciones

- Propaga NaN: cualquier NaN hace que el resultado sea NaN (usar variante `nan`).
- El método `arr.sum(...)` es equivalente y a menudo más corto.

## Notas relacionadas

- [[concepto_axis_parametro]]
- [[concepto_dtype]]
- [[concepto_broadcasting]]
- [[np.prod]]
- [[np.cumsum]]
- [[np.mean]]
- [[np.nansum]]
