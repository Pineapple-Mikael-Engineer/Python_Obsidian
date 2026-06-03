---
title: np.stack — Apilar arrays creando un eje nuevo
aliases:
  - stack
  - np.stack
  - apilar
tags:
  - numpy
  - api/funcion
  - manipulacion

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
  - concepto_axis_parametro

draft: false
---

# np.stack — Apilar arrays creando un eje nuevo

## Firma de la función

```python
np.stack(
    arrays,
    axis=0,
    out=None
) -> ndarray
```

## Valor de retorno

Devuelve un **nuevo** [[concepto_ndarray|ndarray]] con **una dimensión más** (`ndim + 1`). A diferencia de [[np.concatenate]], `stack` crea un eje nuevo donde se colocan los arrays de entrada.

| Entrada | `axis` | Shape salida |
|---------|--------|--------------|
| 3 arrays de `(4,)` | `0` | `(3, 4)` |
| 3 arrays de `(4,)` | `1` | `(4, 3)` |
| 2 arrays de `(2, 3)` | `0` | `(2, 2, 3)` |
| 2 arrays de `(2, 3)` | `-1` | `(2, 3, 2)` |

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
np.stack((a, b), axis=0)
# array([[1, 2, 3],
#        [4, 5, 6]])           # (2, 3)
np.stack((a, b), axis=1)
# array([[1, 4],
#        [2, 5],
#        [3, 6]])              # (3, 2)
```

## Regla fundamental

> Todos los arrays deben tener **exactamente el mismo shape**. El nuevo eje aparece en la posición `axis`.

```python
a = np.ones((2, 3))
b = np.ones((2, 3))
np.stack((a, b)).shape        # (2, 2, 3)  → eje nuevo al frente
np.stack((a, b), axis=-1).shape  # (2, 3, 2)  → eje nuevo al final
```

## stack vs concatenate

| Aspecto | `np.stack` | [[np.concatenate]] |
|---------|-----------|--------------------|
| Eje | crea uno **nuevo** | usa uno **existente** |
| Shapes de entrada | idénticos | iguales salvo el eje de unión |
| `ndim` resultado | `+1` | igual |
| Uso típico | apilar muestras en un batch | extender datos en un eje |

```python
imgs = [np.random.rand(28, 28) for _ in range(32)]
batch = np.stack(imgs, axis=0)   # (32, 28, 28)  → eje de batch nuevo
```

## Parámetros en detalle

### `arrays` — secuencia de arrays

Lista o tupla de arrays del **mismo shape**.

### `axis` — posición del nuevo eje

Entero en el rango `[-(ndim+1), ndim]`. Define dónde se inserta el eje creado.

## Atajos relacionados

| Función | Equivale a |
|---------|-----------|
| [[np.vstack]] | apilar como filas (eje 0) |
| [[np.hstack]] | unir como columnas (eje 1) |
| [[np.dstack]] | apilar en profundidad (eje 2) |
| [[np.column_stack]] | tratar 1D como columnas |

## Casos de uso

### Construir un batch para un modelo

```python
muestras = [preprocesar(x) for x in lote]   # cada una (3, 224, 224)
batch = np.stack(muestras)                   # (N, 3, 224, 224)
```

### Combinar coordenadas X e Y en pares

```python
x = np.array([0, 1, 2])
y = np.array([9, 8, 7])
puntos = np.stack((x, y), axis=1)   # [[0,9],[1,8],[2,7]]  shape (3, 2)
```

### Apilar canales en una imagen

```python
r, g, b = canal_r, canal_g, canal_b   # cada uno (H, W)
img = np.stack((r, g, b), axis=-1)    # (H, W, 3)
```

## Buenas prácticas

1. Usa `stack` cuando los arrays representan **elementos paralelos** que quieres indexar por un eje nuevo (muestras, canales, time-steps).
2. Si en cambio quieres **alargar** datos en un eje que ya existe, usa [[np.concatenate]].
3. Todos los arrays deben tener idéntico shape: valida antes si vienen de fuentes distintas.
4. `axis=-1` es cómodo para apilar como última dimensión (canales) sin conocer `ndim`.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `all input arrays must have the same shape` | shapes distintos | igualar formas (ej. `reshape`/`pad`) antes |
| Dimensión de más inesperada | se usó `stack` donde tocaba `concatenate` | elegir según si quieres eje nuevo o no |
| `axis out of bounds` | `axis` fuera de `[-(ndim+1), ndim]` | usar un eje válido |

## Limitaciones

- Exige shapes idénticos (más estricto que `concatenate`).
- Siempre añade exactamente un eje; para unir sin crear ejes, usa `concatenate`.
- Siempre copia los datos.

## Notas relacionadas

- [[concepto_shape]]
- [[concepto_axis_parametro]]
- [[np.concatenate]]
- [[np.vstack]]
- [[np.hstack]]
- [[np.dstack]]
