---
title: np.broadcast_to — estira un array a una forma mayor sin copiar
aliases:
  - broadcast_to
  - np.broadcast_to
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

# np.broadcast_to — estira un array a una forma mayor sin copiar

`np.broadcast_to` materializa explícitamente el [[concepto_broadcasting|broadcasting]] que NumPy aplica de forma implícita en `a + b`: toma un array y lo **estira** a una forma destino mayor, repitiendo virtualmente sus valores a lo largo de los ejes que valían 1 (o que no existían). Lo hace **sin copiar**: el resultado es una vista cuyos `strides` valen 0 en los ejes estirados, así que avanzar por ese eje repite el mismo dato. El precio de no copiar es que el resultado es **de solo lectura**.

## La idea en una fórmula

Broadcast_to alinea la forma de entrada por la derecha contra la forma destino y estira los ejes de tamaño 1 (y los ejes nuevos por la izquierda) hasta encajar:

$$ (n_0, \dots, n_{k-1}) \;\xrightarrow{\ \text{broadcast\_to, } S\ }\; S = (s_0, \dots, s_{r-1}) \qquad (r \ge k) $$

válido **si y solo si**, tras rellenar la entrada con `1` por la izquierda hasta `r` ejes, en cada eje $n_i = s_i$ o $n_i = 1$. El eje que valía 1 se "estira" a $s_i$ sin almacenar nada nuevo:

$$ [\,1,2,3\,]_{(3,)} \;\xrightarrow{\ (2,3)\ }\; \begin{bmatrix} 1 & 2 & 3 \\ 1 & 2 & 3 \end{bmatrix} \qquad\text{(la fila se repite, pero solo hay una en memoria)} $$

## Firma

```python
np.broadcast_to(
    array,             # array_like: el array a estirar
    shape,             # tuple[int]: la forma destino (debe ser broadcasteable con la de array)
    subok=False,       # bool: si conservar subclases de ndarray (np.matrix, etc.)
) -> ndarray
```

## Los parámetros en detalle

### `array` — el array de entrada
`array_like`. Es el array cuyos valores se repetirán. Su forma debe ser **broadcasteable** a `shape` siguiendo las reglas de alineación por la derecha.

### `shape` — la forma destino
Tupla de `int`. Es la forma final del resultado, que debe ser **igual o mayor** que la de `array` y compatible con broadcasting. No puede ser menor ni reorganizar el `size` libremente (eso es [[np.reshape|reshape]]): broadcast_to solo **estira**, no reordena.

```python
a = np.array([1, 2, 3])              # (3,)
np.broadcast_to(a, (2, 3))           # estira a (2, 3): la fila se repite 2 veces
np.broadcast_to(a, (4, 3)).shape     # (4, 3)
np.broadcast_to(a, (3, 2))           # ValueError: (3,) no alinea con (3, 2)
```

### `subok` — conservar la subclase
`bool` (defecto `False`). Si `True`, conserva subclases de `ndarray` (como `np.matrix`); si `False`, el resultado es un `ndarray` base. Rara vez se toca.

## El caso N-D

La regla es la del broadcasting: alinear por la derecha, rellenar con `1` por la izquierda y estirar cada eje de tamaño 1 hasta el destino. Los ejes nuevos (los que la entrada no tenía) se añaden por la izquierda.

| `array.shape` | `shape` | ¿válido? | qué se estira |
|---------------|---------|----------|---------------|
| `(3,)` | `(2, 3)` | sí | nuevo eje 0 (1→2) |
| `(1, 3)` | `(4, 3)` | sí | eje 0 (1→4) |
| `(3, 1)` | `(3, 5)` | sí | eje 1 (1→5) |
| `(1, 4, 1)` | `(2, 4, 5)` | sí | ejes 0 y 2 |
| `(3,)` | `(3, 2)` | no | 3 no alinea con 2 por la derecha |

```python
# Vector RGB estirado a un lote de imágenes (b, alto, ancho, 3)
color = np.array([255, 128, 0])              # (3,)
fondo = np.broadcast_to(color, (4, 2, 2, 3)) # (4, 2, 2, 3) → mismo color en todo el lote
fondo.shape                                  # (4, 2, 2, 3)
np.shares_memory(color, fondo)               # True → no copió nada
```
Aunque `fondo` "ocupa" 48 valores lógicos, en memoria sigue habiendo solo 3: los `strides` 0 los repiten.

## Vista vs copia

`np.broadcast_to` **siempre devuelve una vista de solo lectura**, nunca copia (ver [[concepto_views_vs_copias]]). Los ejes estirados tienen `stride = 0`: el mismo byte se lee muchas veces. Por eso NumPy la marca como **no escribible** — escribir en una celda "estirada" afectaría a todas las que comparten ese byte, casi siempre un bug:

```python
a = np.array([1, 2, 3])
b = np.broadcast_to(a, (2, 3))
b.flags.writeable          # False → solo lectura
b.strides                  # (0, 8)  → el eje 0 no avanza en memoria
np.shares_memory(a, b)     # True

b[0, 0] = 99               # ValueError: assignment destination is read-only
```

Si necesitas escribir, haz una copia explícita: `np.broadcast_to(a, shape).copy()` (ahí sí materializa los datos repetidos).

## Valor de retorno

`ndarray` de la forma `shape` pedida, mismo `dtype` que `array`, **vista de solo lectura** que comparte el buffer de `array`:

| Entrada | `shape` | salida | escribible | ¿copia? |
|---------|---------|--------|------------|---------|
| `(3,)` | `(2, 3)` | `(2, 3)` | no | no (vista, strides 0) |
| `(3, 1)` | `(3, 5)` | `(3, 5)` | no | no |
| `(3,)` + `.copy()` | `(2, 3)` | `(2, 3)` | sí | sí (materializa) |

## Casos de uso

### Materializar una forma común sin gastar memoria
```python
media = np.array([0.1, 0.2, 0.3])       # (3,)  → media por canal
vista = np.broadcast_to(media, (1000, 3))  # (1000, 3) sin replicar nada en memoria
# útil para pasar a una función que exige la forma completa
```

### Crear un fondo/constante con forma de imagen (caso N-D)
```python
color = np.array([10, 20, 30])               # (3,) RGB
lienzo = np.broadcast_to(color, (2, 2, 3))   # (2, 2, 3)
lienzo
# array([[[10, 20, 30], [10, 20, 30]],
#        [[10, 20, 30], [10, 20, 30]]])
```

### Comparar el coste frente a `np.tile`
```python
v = np.arange(3)
np.broadcast_to(v, (1000, 3))     # 0 bytes extra (vista de solo lectura)
np.tile(v, (1000, 1))             # copia física de 3000 valores (escribible)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: ... cannot be broadcast to ...` | la forma destino no alinea por la derecha | ajustar `shape` o usar [[np.expand_dims]] antes |
| `assignment destination is read-only` | intentar escribir en la vista estirada | `np.broadcast_to(a, s).copy()` si necesitas escribir |
| El destino tiene **menos** ejes que la entrada | broadcast_to solo agranda | usar `reshape`/`squeeze`, no broadcast_to |
| Se esperaba una copia y se modificó el original | confundirla con `tile`/`repeat` | usar `np.tile`/`np.repeat` para datos físicos |

## Notas relacionadas

- [[concepto_broadcasting]] — las reglas de alineación que broadcast_to materializa
- [[concepto_views_vs_copias]] — por qué es una vista de solo lectura (strides 0)
- [[np.expand_dims]] — inserta el eje de tamaño 1 que luego se estira
- [[np.reshape]] · [[np.tile]] · [[np.repeat]]
