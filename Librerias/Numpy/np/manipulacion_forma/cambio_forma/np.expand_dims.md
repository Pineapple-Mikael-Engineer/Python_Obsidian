---
title: np.expand_dims — inserta un eje de tamaño 1 en la posición axis
aliases:
  - expand_dims
  - np.expand_dims
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
  - concepto_broadcasting

draft: false
---

# np.expand_dims — inserta un eje de tamaño 1 en la posición axis

`np.expand_dims` es la inversa de [[np.squeeze|squeeze]]: añade al [[concepto_shape|shape]] un eje nuevo de tamaño 1 en la posición que digas, subiendo `ndim` en 1. No replica datos ni cambia el `size`; solo crea una dimensión "virtual" que sirve para **alinear formas**. Es la herramienta clave para preparar arrays de cara al [[concepto_broadcasting|broadcasting]]: un vector `(4,)` que no casa con una matriz `(4, 3)` se vuelve compatible al convertirlo en `(4, 1)`.

## La idea en una fórmula

Expand_dims inserta un `1` en la posición `axis` de la tupla, desplazando los ejes posteriores:

$$ (n_0, \dots, n_{k-1}) \;\xrightarrow{\ \text{expand\_dims, axis}=p\ }\; (n_0, \dots, n_{p-1},\, 1,\, n_p, \dots, n_{k-1}) $$

El nuevo eje vale 1, así que el `size` no cambia (multiplicar por 1 no altera el producto). Dónde cae el `1` decide cómo se alineará la forma por la derecha en broadcasting:

$$ (3,) \;\xrightarrow{\ \text{axis}=0\ }\; (1, 3) \quad\text{(fila)} \qquad\qquad (3,) \;\xrightarrow{\ \text{axis}=1\ }\; (3, 1) \quad\text{(columna)} $$

## Firma

```python
np.expand_dims(
    a,                 # array_like: el array al que añadir el eje
    axis,              # int | tuple[int]: posición(es) donde insertar el eje de tamaño 1
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de entrada
`array_like` de cualquier forma. Se convierte a `ndarray` si no lo es. No se modifica; el resultado es una vista.

### `axis` — dónde insertar el eje
`int` o tupla de `int` (tupla admitida desde NumPy ≥ 1.18). Es la posición que ocupará el nuevo eje **en el shape de salida**. Admite valores negativos (cuentan desde el final). El rango válido es `[-(ndim+1), ndim]`.

```python
v = np.array([1, 2, 3])            # (3,)
np.expand_dims(v, axis=0).shape    # (1, 3)  → fila
np.expand_dims(v, axis=1).shape    # (3, 1)  → columna
np.expand_dims(v, axis=-1).shape   # (3, 1)  → al final sin saber ndim

a = np.ones((2, 3))
np.expand_dims(a, axis=(0, 3)).shape   # (1, 2, 3, 1)  → dos ejes a la vez
```

`axis=-1` es idiomático para "añadir un canal/eje al final" sin tener que conocer `ndim`.

## El caso N-D

La regla: el eje de tamaño 1 se inserta en la posición `axis` y todo lo demás se desplaza. Con tupla, se insertan varios ejes a la vez (las posiciones se interpretan sobre el shape final).

| `a.shape` | `axis` | salida | uso |
|-----------|--------|--------|-----|
| `(3,)` | `0` | `(1, 3)` | vector → fila |
| `(3,)` | `1` | `(3, 1)` | vector → columna |
| `(2, 3)` | `0` | `(1, 2, 3)` | añadir eje de lote |
| `(2, 3)` | `-1` | `(2, 3, 1)` | añadir eje de canal |
| `(28, 28)` | `(0, -1)` | `(1, 28, 28, 1)` | lote + canal de golpe |

```python
# Imagen 2-D → tensor con ejes de lote y canal
img = np.random.rand(28, 28)        # (28, 28)
batch = np.expand_dims(img, 0)      # (1, 28, 28)   → un solo ejemplo en el lote
canal = np.expand_dims(img, -1)     # (28, 28, 1)   → un canal al final
np.expand_dims(img, (0, -1)).shape  # (1, 28, 28, 1) → formato lote-alto-ancho-canal
```

## Vista vs copia

`np.expand_dims` devuelve **siempre una vista**: solo reescribe shape y `strides` (el nuevo eje recibe stride 0 / sin efecto), nunca mueve datos (ver [[concepto_views_vs_copias]]). Modificar el resultado modifica `a`.

## Valor de retorno

`ndarray` con el mismo `dtype` y los mismos datos que `a`, con `ndim` aumentado en tantas posiciones como indique `axis`. Siempre vista.

| Entrada | `axis` | salida | `ndim` |
|---------|--------|--------|--------|
| `(3,)` | `0` | `(1, 3)` | 1 → 2 |
| `(2, 3)` | `-1` | `(2, 3, 1)` | 2 → 3 |
| `(2, 3)` | `(0, 3)` | `(1, 2, 3, 1)` | 2 → 4 |

## Relación con `np.newaxis` y `reshape`

Tres formas equivalentes de añadir un eje de tamaño 1:

```python
v = np.arange(3)
np.expand_dims(v, 1)   # (3, 1)
v[:, np.newaxis]       # (3, 1)  → np.newaxis es un alias de None
v.reshape(-1, 1)       # (3, 1)
```

`np.newaxis` es el más compacto al indexar a mano; `expand_dims` es el más legible cuando el eje viene en una **variable** (`np.expand_dims(a, axis=eje)`) o cuando insertas varios a la vez.

## Casos de uso

### Habilitar broadcasting entre vector y matriz
```python
M = np.ones((4, 3))
v = np.array([10, 20, 30, 40])      # (4,)  → NO alinea con (4, 3) por la derecha
M + np.expand_dims(v, axis=1)       # (4, 1) sí alinea → suma una constante por fila
```

### Añadir dimensión de lote o de canal (caso N-D)
```python
img = np.arange(2*2*3).reshape(2, 2, 3)   # (2, 2, 3) → imagen RGB 2×2
lote = np.expand_dims(img, 0)             # (1, 2, 2, 3) → un ejemplo en el lote
lote.shape                                # (1, 2, 2, 3)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AxisError: axis N is out of bounds` | `axis` fuera de `[-(ndim+1), ndim]` | el rango es `ndim+1` posiciones |
| El broadcasting sigue fallando | se insertó el eje en la posición equivocada | revisar `axis=0` (fila) vs `axis=1` (columna) |
| Eje duplicado inesperado | se llamó dos veces sobre el mismo array | un solo `expand_dims` por eje deseado |
| Se quería replicar datos, no insertar | `expand_dims` no copia valores | usar [[np.repeat]] o [[np.tile]] |

## Notas relacionadas

- [[concepto_shape]] — qué es un eje de tamaño 1 y por qué no cambia el `size`
- [[concepto_broadcasting]] — el motivo principal para insertar ejes: alinear formas
- [[np.squeeze]] — la operación inversa: quita los ejes de tamaño 1
- [[np.newaxis]] · [[np.reshape]] · [[np.broadcast_to]]
