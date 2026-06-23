---
title: np.stack — apila arrays a lo largo de un eje nuevo
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

# np.stack — apila arrays a lo largo de un eje nuevo

`np.stack` toma $r$ arrays **del mismo shape** y los coloca a lo largo de un **eje nuevo** que no existía. El resultado tiene una dimensión más (`ndim + 1`). Ahí está toda la diferencia con [[np.concatenate]]: concatenate hace crecer un eje **existente**, stack **inserta uno**. Es la herramienta para construir un lote a partir de muestras paralelas: $N$ imágenes de igual tamaño se vuelven un tensor con un eje de lote nuevo.

## La idea en una fórmula

Dados $r$ arrays, todos de shape $(n_0,\dots,n_{k-1})$, stack inserta un eje de tamaño $r$ en la posición `axis`:

$$
\underbrace{(n_0,\dots,n_{k-1}),\;\dots,\;(n_0,\dots,n_{k-1})}_{r\ \text{arrays}}\;\xrightarrow{\ \text{axis}=p\ }\;(n_0,\dots,n_{p-1},\,\overbrace{r}^{\text{nuevo}},\,n_p,\dots,n_{k-1})
$$

El eje nuevo (de tamaño $r$ = número de arrays) se mete **entre** los ejes existentes según `axis`; los demás conservan su orden. Con tres vectores $(4,)$ apilados en `axis=0` aparece un eje de tamaño 3 al frente:

$$
\begin{bmatrix} 1 & 2 & 3 \end{bmatrix},\;\begin{bmatrix} 4 & 5 & 6 \end{bmatrix}\;\xrightarrow{\ \text{axis}=0\ }\;\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}\qquad (3,),(3,)\to(2,3)
$$

## La diferencia con concatenate

Es el par que más conviene tener claro. Mismos dos vectores `(3,)`:

```python
a = np.array([1, 2, 3]); b = np.array([4, 5, 6])
np.concatenate((a, b)).shape   # (6,)    → crece el eje EXISTENTE (3+3)
np.stack((a, b)).shape         # (2, 3)  → aparece un eje NUEVO de tamaño 2
```

| Aspecto | `np.stack` | [[np.concatenate]] |
|---|---|---|
| El eje | crea uno **nuevo** | usa uno **existente** |
| Shapes de entrada | **idénticos** | iguales salvo en `axis` |
| `ndim` resultado | `+1` | igual |
| Uso típico | apilar muestras en un lote | alargar datos en un eje |

## Firma

```python
np.stack(
    arrays,    # secuencia de array_like, TODOS del mismo shape
    axis=0,    # int: posición donde se inserta el eje nuevo
    out=None,  # ndarray: destino preasignado
) -> ndarray
```

## Los parámetros en detalle

### `arrays` — la secuencia a apilar
Lista o tupla de `array_like`. **Todos deben tener exactamente el mismo shape** (más estricto que concatenate). El número de arrays es el tamaño del eje nuevo.

### `axis` — dónde se inserta el eje nuevo
`int` en el rango `[-(ndim+1), ndim]` (defecto `0`). Marca la posición del eje creado en el shape de salida: `axis=0` lo pone al frente, `axis=-1` al final.

```python
a = np.ones((2, 3)); b = np.ones((2, 3))
np.stack((a, b)).shape           # (2, 2, 3)  → eje nuevo al frente
np.stack((a, b), axis=-1).shape  # (2, 3, 2)  → eje nuevo al final
np.stack((a, b), axis=1).shape   # (2, 2, 3)  → eje nuevo en medio
```

### `out` — escribir en un buffer existente
`ndarray` preasignado con el shape y dtype exactos de la salida (la del eje ya insertado). Evita una asignación; útil en bucles.

## El caso N-D

Para $r$ arrays de shape $(n_0,\dots,n_{k-1})$, el shape de salida tiene $k+1$ ejes: los originales más uno de tamaño $r$ en la posición `axis`.

| Entrada | `axis` | Salida | Lectura |
|---|---|---|---|
| 3 arrays `(4,)` | `0` | `(3,4)` | 3 filas |
| 3 arrays `(4,)` | `1` | `(4,3)` | 3 columnas |
| 2 arrays `(2,3)` | `0` | `(2,2,3)` | eje de lote nuevo |
| 2 arrays `(2,3)` | `-1` | `(2,3,2)` | eje de canal al final |
| 32 arrays `(28,28)` | `0` | `(32,28,28)` | un lote |

```python
imgs = [np.random.rand(28, 28) for _ in range(32)]
batch = np.stack(imgs, axis=0)   # (32, 28, 28)  → eje de lote nuevo

# Canales R, G, B (cada uno (H, W)) apilados como última dimensión:
r, g, b = (np.zeros((4, 4)) for _ in range(3))
img = np.stack((r, g, b), axis=-1)   # (4, 4, 3)
```

## Vectorización

`stack` equivale a expandir cada array con un eje de tamaño 1 en `axis` y luego concatenar, pero lo hace de una vez: reserva el buffer de salida $(\dots,r,\dots)$ y copia cada array en su rebanada. Frente al patrón manual:

```python
# Manual (lo que stack hace por dentro):
np.concatenate([a[None], b[None]], axis=0)   # a[None] = a con eje nuevo
# Directo:
np.stack([a, b], axis=0)
```

Igual que en [[concepto_vectorizacion]], describes *qué* eje crear, no cómo iterar copiando muestra a muestra.

## Valor de retorno

Siempre un **nuevo** `ndarray` (copia) con `ndim + 1` ejes. El dtype es la promoción común de las entradas.

| Entradas | `axis` | Salida (shape) | dtype |
|---|---|---|---|
| $r$ arrays `(n,)` | `0` | `(r, n)` | promoción común |
| $r$ arrays `(n,)` | `1` | `(n, r)` | promoción común |
| $r$ arrays `(m,n)` | `p` | `(m,n)` con `r` insertado en `p` | promoción común |

## Casos de uso

### Apilar dos vectores como filas de una matriz
Apilar en `axis=0` dos vectores `(3,)` los convierte en las dos filas de una `(2,3)`:

$$
\begin{bmatrix} 1 & 2 & 3 \end{bmatrix},\;\begin{bmatrix} 4 & 5 & 6 \end{bmatrix}\;\xrightarrow{\ \text{axis}=0\ }\;\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
$$

```python
a = np.array([1, 2, 3]); b = np.array([4, 5, 6])
np.stack((a, b), axis=0)   # [[1,2,3],[4,5,6]]   → (2, 3)
```

### Emparejar coordenadas X e Y
```python
x = np.array([0, 1, 2]); y = np.array([9, 8, 7])
puntos = np.stack((x, y), axis=1)   # [[0,9],[1,8],[2,7]]  → (3, 2)
```

### 4D: armar un lote de imágenes RGB
Apilar $8$ imágenes `(3, 32, 32)` (canales, alto, ancho) inserta un eje de lote al frente y produce un tensor **4D**:

```python
imgs = [np.random.rand(3, 32, 32) for _ in range(8)]   # 8 imágenes (3,32,32)
batch = np.stack(imgs, axis=0)                          # (8, 3, 32, 32)  → 4D
# ejes: (lote=8, canal=3, alto=32, ancho=32)
batch[0].shape                                          # (3, 32, 32)  → una imagen
```

### 5D: apilar un conjunto de vídeos
Cada vídeo es un tensor 4D `(10, 3, 32, 32)` (frames, canal, alto, ancho). Apilar $4$ de ellos inserta un eje de "vídeo" al frente y da un tensor **5D**:

```python
videos = [np.random.rand(10, 3, 32, 32) for _ in range(4)]   # 4 vídeos 4D
lote = np.stack(videos, axis=0)                              # (4, 10, 3, 32, 32)  → 5D
# ejes: (vídeo=4, frame=10, canal=3, alto=32, ancho=32)
lote[1, 5].shape                                            # (3, 32, 32)  → frame 5 del vídeo 1
```

## Errores comunes

| Error | Causa | Solución |
|---|---|---|
| `all input arrays must have the same shape` | shapes distintos entre sí | igualar formas (`reshape`/`pad`) antes |
| Aparece una dimensión de más inesperada | se usó `stack` donde tocaba [[np.concatenate]] | elegir según si quieres eje nuevo o no |
| `axis ... is out of bounds` | `axis` fuera de `[-(ndim+1), ndim]` | usar una posición válida |
| Falta el eje nuevo | se usó `concatenate` queriendo apilar | usar `stack` |

## Notas relacionadas

- [[concepto_shape]] — el eje nuevo y el `ndim + 1`
- [[concepto_axis_parametro]] — dónde se inserta el eje
- [[np.concatenate]] — la alternativa por eje existente
- [[np.vstack]] · [[np.hstack]] · [[np.dstack]] · [[np.column_stack]] — atajos por eje fijo
- [[np.split]] — la operación inversa
