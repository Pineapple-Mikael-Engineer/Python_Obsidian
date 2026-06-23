---
title: np.pad — añade relleno (padding) alrededor del array
aliases:
  - pad
  - np.pad
  - padding
  - relleno
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

draft: false
---

# np.pad — añade relleno (padding) alrededor del array

`np.pad` **agranda** el array añadiendo un borde de relleno alrededor: cada eje crece según cuántas
posiciones se pidan antes y después. Es la operación detrás del *padding* de imágenes y convoluciones
(ampliar el marco para que el kernel alcance los bordes), y la forma "no circular" de desplazar con
relleno frente a [[np.roll]]. El parámetro `mode` decide **con qué** se rellena el borde.

## La idea en una fórmula

Rellenar es **sumar al tamaño de cada eje** lo que se añade antes y después. Si en el eje $i$ se
añaden $p_i^{\text{before}}$ y $p_i^{\text{after}}$ posiciones, el eje crece por su suma
$p_i = p_i^{\text{before}} + p_i^{\text{after}}$:

$$ (n_0,\dots,n_{k-1}) \;\xrightarrow{\ \text{pad},\ \text{pad\_width}=((p_0^{b},p_0^{a}),\dots)\ }\; (n_0 + p_0,\ \dots,\ n_{k-1} + p_{k-1}) $$

Por índices (modo `'constant'` con valor $c$), la salida copia el array en el centro y pone $c$ fuera.
Para `[a, b, c]` con `pad_width=(1, 2)` y `constant_values=0`:

$$ [\,a,\ b,\ c\,] \;\xrightarrow{\ (1,\,2),\ c=0\ }\; [\,0,\ a,\ b,\ c,\ 0,\ 0\,] $$

El array original queda **embebido** en una "tela" más grande; `mode` solo cambia qué hay en esa tela.

## Firma

```python
np.pad(
    array,                 # array_like: el array a rellenar
    pad_width,             # int | tuple | sequence: cuánto añadir antes/después por eje
    mode='constant',       # str | callable: con qué se rellena el borde
    **kwargs,              # parámetros del modo: constant_values, stat_length, end_values...
) -> ndarray
```

## Los parámetros en detalle

### `array` — el array a rellenar
`array_like` de cualquier dimensión. Queda embebido (sin modificarse) en el centro de la salida.

### `pad_width` — cuánto se añade en cada eje
El parámetro central. Especifica el relleno **antes** y **después** por eje. Formas admitidas:
- **`int`** — el mismo relleno antes y después en **todos** los ejes.
- **`(before, after)`** — un par aplicado a todos los ejes por igual.
- **`((b0, a0), (b1, a1), …)`** — un par **por eje**, control total.

```python
np.pad([1, 2, 3], 2)             # [0,0,1,2,3,0,0]   → 2 a cada lado
np.pad([1, 2, 3], (1, 2))        # [0,1,2,3,0,0]     → 1 antes, 2 después
```

### `mode` — con qué se rellena el borde
Decide el contenido del marco. Los más usados:
- **`'constant'`** (defecto) — un valor fijo (ver `constant_values`); por defecto `0`.
- **`'edge'`** — repite el valor del borde más cercano.
- **`'reflect'`** — espeja los valores sin repetir el borde (`[1,2,3]` → `…2,1|1,2,3|3,2…` no, sino `…3,2|1,2,3|2,1…`).
- **`'wrap'`** — envuelve de forma circular (el borde opuesto entra, como [[np.roll]] pero ampliando).

```python
a = np.array([1, 2, 3])
np.pad(a, 2, mode='edge')      # [1,1,1,2,3,3,3]
np.pad(a, 2, mode='reflect')   # [3,2,1,2,3,2,1]
np.pad(a, 2, mode='wrap')      # [2,3,1,2,3,1,2]
```

### `constant_values` — el valor del relleno (modo `'constant'`)
Escalar o pares por eje (`(before, after)`). Solo aplica con `mode='constant'`.

```python
np.pad([1, 2, 3], 2, constant_values=-1)         # [-1,-1,1,2,3,-1,-1]
np.pad([1, 2, 3], (1, 1), constant_values=(7, 9))  # [7,1,2,3,9]
```

### `**kwargs` de otros modos
`stat_length` (para `'mean'`/`'median'`/`'maximum'`: cuántos valores del borde usar para el
estadístico), `end_values` (para `'linear_ramp'`), `reflect_type` (`'even'`/`'odd'` en `'reflect'`).
Solo importan según el `mode` elegido.

## El caso N-D

La regla: **cada eje crece por la suma de su `(before, after)`**; un eje con `(0, 0)` no se toca. En
N-D `pad_width` lleva un par por eje.

| `array.shape` | `pad_width` | salida | lectura |
|---------------|-------------|--------|---------|
| `(n,)` | `2` | `(n+4,)` | 2 a cada lado |
| `(n,)` | `(1, 2)` | `(n+3,)` | 1 antes, 2 después |
| `(m, n)` | `1` | `(m+2, n+2)` | marco de 1 en todo el contorno |
| `(m, n)` | `((1,1),(0,0))` | `(m+2, n)` | solo arriba/abajo (filas) |
| `(h, w, c)` | `((1,1),(1,1),(0,0))` | `(h+2, w+2, c)` | borde espacial, canales intactos |

```python
img = np.arange(2*2).reshape(2, 2)
np.pad(img, 1, mode='constant')
# [[0,0,0,0],
#  [0,0,1,0],
#  [0,2,3,0],
#  [0,0,0,0]]   → (4, 4): marco de ceros alrededor del 2×2 original
```

El último patrón —rellenar alto y ancho pero **no** el eje de canales— es exactamente el padding de
una imagen RGB antes de una convolución.

## Vectorización

`np.pad` reemplaza el bucle que crea un array grande de ceros y copia el original dentro. La versión
vectorizada asigna la salida y rellena cada borde según el `mode` en C, de una sola vez:

```python
# Manual (modo 'constant', 1D):
out = np.zeros(len(a) + b + c, dtype=a.dtype)
out[b:b+len(a)] = a

# Vectorizado, N-D y con modos:
np.pad(a, (b, c), mode='constant')
```

El valor de [[concepto_vectorizacion]] aquí es sobre todo de **expresividad**: `mode='reflect'` o
`'wrap'` a mano en N-D es tedioso y propenso a errores de índice; `np.pad` lo encapsula.

## Valor de retorno

Siempre un **`ndarray` nuevo** (copia agrandada), con el `dtype` de `array` conservado y el shape
ampliado eje por eje según `pad_width`.

| Entrada | `pad_width` | salida (shape) |
|---------|-------------|----------------|
| `(n,)` | `(b, a)` | `(n + b + a,)` |
| `(m, n)` | `p` (int) | `(m + 2p, n + 2p)` |
| `(m, n)` | `((b0,a0),(b1,a1))` | `(m + b0 + a0, n + b1 + a1)` |
| `(d0,…,d_{k-1})` | un par por eje | `(d_i + b_i + a_i)_i` |

## Casos de uso

### Marco de ceros alrededor de una matriz
```python
M = np.array([[1, 2], [3, 4]])
np.pad(M, 1)            # (4, 4) con borde de ceros
```

### Padding de una imagen para convolución (N-D, solo lo espacial)
```python
img = np.zeros((128, 256, 3))                 # (alto, ancho, canales)
borde = np.pad(img, ((2,2),(2,2),(0,0)),      # 2 px de marco
               mode='reflect')
borde.shape   # (132, 260, 3)  → canales intactos, espacio ampliado
```

### Desplazar con relleno (no circular, frente a roll)
```python
x = np.array([1, 2, 3, 4])
np.pad(x, (1, 0), mode='constant')[:-1]   # [0,1,2,3]  → shift derecha rellenando con 0
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `pad_width` rechazado | número de pares ≠ número de ejes | dar un par `(before, after)` por eje |
| Se rellena el eje equivocado | orden de los pares en `pad_width` | usar `(0, 0)` en los ejes a preservar |
| `constant_values` ignorado | el `mode` no es `'constant'` | fijar `mode='constant'` o el kwarg del modo correcto |
| Borde circular inesperado | `mode='wrap'` | usar `'constant'`/`'edge'` si no se quería envolver |

## Notas relacionadas

- [[concepto_shape]] — cada eje crece por su `(before, after)`
- [[np.roll]] — desplazar circularmente (sin rellenar)
- [[np.repeat]] · [[np.tile]] — agrandar duplicando datos en vez de rellenar
- [[concepto_broadcasting]] — alternativa cuando solo hay que alinear shapes
