---
title: np.tile — repite el array entero como un mosaico
aliases:
  - tile
  - np.tile
  - mosaico
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
  - concepto_broadcasting

draft: false
---

# np.tile — repite el array entero como un mosaico

`np.tile` repite el **array completo** como las baldosas de un mosaico: `[1, 2, 3]` con `reps=2` se
convierte en `[1, 2, 3, 1, 2, 3]`, no en `[1, 1, 2, 2, 3, 3]`. La unidad que se repite es el
**bloque entero**, y `reps` controla cuántas baldosas se ponen en cada eje. Es la operación
complementaria de [[np.repeat]] (que repite el elemento, no el bloque).

## La idea en una fórmula

Embaldosar es **multiplicar cada dimensión** por su número de repeticiones. Si `reps` tiene tantas
componentes como ejes, $(r_0,\dots,r_{k-1})$, cada eje se escala por su `r`:

$$ (n_0,\dots,n_{k-1}) \;\xrightarrow{\ \text{tile},\ \text{reps}=(r_0,\dots,r_{k-1})\ }\; (r_0\cdot n_0,\dots,r_{k-1}\cdot n_{k-1}) $$

Cuando `reps` tiene **más** componentes que ejes tiene `A`, el array se promociona primero añadiendo
ejes de tamaño 1 **por la izquierda** hasta igualar el rango; luego se aplica la fórmula. En 1D, con
`reps=r` escalar:

$$ [\,a,\ b\,] \;\xrightarrow{\ \text{reps}=3\ }\; [\,a,\ b,\ a,\ b,\ a,\ b\,] $$

frente a la repetición por elemento de [[np.repeat]], que daría `[a, a, a, b, b, b]`.

## Firma

```python
np.tile(
    A,      # array_like: el bloque a repetir
    reps,   # int | tuple[int]: número de baldosas por eje
) -> ndarray
```

## Los parámetros en detalle

### `A` — el bloque a repetir
`array_like` (ndarray, lista, escalar). Es la **baldosa**: se copia entera en cada posición del
mosaico.

### `reps` — cuántas baldosas en cada eje
El parámetro central. Un `int` repite a lo largo del último eje; una **tupla** da la cuenta por eje.
La regla de rangos:
- si `len(reps) == A.ndim`, cada eje se multiplica por su componente;
- si `len(reps) > A.ndim`, `A` gana ejes de tamaño 1 **por la izquierda** hasta igualar;
- si `len(reps) < A.ndim`, `reps` se completa con `1` **por la izquierda** (ejes no repetidos).

```python
np.tile([1, 2], 3)        # [1, 2, 1, 2, 1, 2]
np.tile([1, 2], (2, 2))   # [[1,2,1,2],
                          #  [1,2,1,2]]           → A pasa a (1,2), reps (2,2) → (2,4)
np.tile([1, 2, 3], (2, 1)).shape   # (2, 3)       → 2 filas, la fila intacta
```

## El caso N-D

La regla es directa: **cada eje se multiplica por su `reps`**; los ejes que falten en `reps` se
rellenan con `1` (no se repiten).

| `A.shape` | `reps` | salida | lectura |
|-----------|--------|--------|---------|
| `(n,)` | `r` | `(n·r,)` | el vector `r` veces seguido |
| `(n,)` | `(a, b)` | `(a, n·b)` | `A` promociona a `(1, n)` |
| `(m, n)` | `(a, b)` | `(m·a, n·b)` | mosaico `a×b` de la matriz |
| `(m, n)` | `r` | `(m, n·r)` | `reps` → `(1, r)`: repite columnas |
| `(d0, d1, d2)` | `(a, b, c)` | `(d0·a, d1·b, d2·c)` | embaldosa en 3D |

```python
patron = np.array([[0, 1],
                   [1, 0]])
np.tile(patron, (2, 3)).shape   # (4, 6)  → 2 baldosas en alto, 3 en ancho
```

## Vectorización

`np.tile` reemplaza el bucle que concatena copias del array. La versión vectorizada calcula el shape
final y rellena el mosaico en C, sin construir y pegar listas en Python:

```python
# Bucle Python (lento, explícito):
def tile1d(a, r):
    out = []
    for _ in range(r):
        out += list(a)
    return np.array(out)

# Vectorizado:
np.tile(a, r)
```

A menudo el [[concepto_broadcasting|broadcasting]] **evita materializar** el mosaico: si solo
necesitas alinear shapes para operar, broadcastear es más barato en memoria que crear todas las
baldosas. `tile` se reserva para cuando de verdad necesitas el array repetido como dato.

## Valor de retorno

Siempre un **`ndarray` nuevo** (copia materializada), con el `dtype` de `A`. El `ndim` de salida es
`max(A.ndim, len(reps))`.

| Entrada | `reps` | salida (shape) |
|---------|--------|----------------|
| `(n,)` | `r` | `(n·r,)` |
| `(n,)` | `(a, b)` | `(a, n·b)` |
| `(m, n)` | `(a, b)` | `(m·a, n·b)` |
| `(d0, d1, d2)` | `(a, b, c)` | `(d0·a, d1·b, d2·c)` |

## Casos de uso

### Construir un damero repitiendo un patrón `(2,2)`
El bloque entero se replica como baldosa, no el elemento. Con `reps=(2,2)` el `2×2` se embaldosa en un `4×4`:

$$
\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}
\;\xrightarrow{\ \text{tile},\ \text{reps}=(2,2)\ }\;
\begin{bmatrix} 0 & 1 & 0 & 1 \\ 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 1 \\ 1 & 0 & 1 & 0 \end{bmatrix}
$$

```python
patron  = np.array([[0, 1], [1, 0]])
tablero = np.tile(patron, (4, 4))    # (8, 8)  → damero tipo ajedrez
```

### Replicar un vector como filas de una matriz
```python
fila = np.array([1, 2, 3])
np.tile(fila, (5, 1))   # (5, 3): la misma fila repetida 5 veces
```

### Difundir una imagen plantilla a todo un lote 4D `(N, C, H, W)`
Una sola imagen `(1, 3, 32, 32)` se replica `N` veces en el eje del lote dejando canales y espacio intactos (`reps=1` en esos ejes). Es la forma materializada de lo que normalmente haría el [[concepto_broadcasting|broadcasting]]:

```python
plantilla = np.zeros((1, 3, 32, 32))     # una imagen base (N=1)
lote = np.tile(plantilla, (8, 1, 1, 1))  # reps por eje: solo el lote crece
lote.shape                                # (8, 3, 32, 32)  → 8 copias idénticas
```

### Mosaico espacial de un canal (ampliar alto y ancho)
Embaldosar solo los dos ejes espaciales repite la baldosa como un *tiling* de textura; el shape de cada eje se multiplica por su `reps`:

```python
canal = np.arange(2*2).reshape(2, 2)   # (2, 2)
np.tile(canal, (3, 4)).shape           # (6, 8)  → 3 baldosas de alto, 4 de ancho
```

### Replicar un clip plantilla a un lote de vídeo 5D `(N, T, C, H, W)`
Con un clip base `(1, 4, 3, 32, 32)` y `reps` de 5 componentes, solo el eje del lote se repite; tiempo, canales y espacio quedan fijos:

```python
clip = np.zeros((1, 4, 3, 32, 32))         # (N=1, T=4, C=3, H=32, W=32)
np.tile(clip, (6, 1, 1, 1, 1)).shape       # (6, 4, 3, 32, 32)
# eje 0 (lote): 1 → 6 ; los otros cuatro ejes intactos
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Salió `[1,2,1,2]` y se quería `[1,1,2,2]` | se buscaba repetir el elemento | usar [[np.repeat]] |
| Memoria alta por materializar copias | `tile` crea el array completo | usar [[concepto_broadcasting|broadcasting]] si es para operar |
| Ejes inesperados | `reps` con más dims promociona `A` por la izquierda | ajustar `reps` al rango deseado |

## Notas relacionadas

- [[concepto_shape]] — cada dimensión se multiplica por su `reps`
- [[concepto_broadcasting]] — la alternativa sin materializar el mosaico
- [[np.repeat]] — repite el elemento, no el bloque
- [[np.roll]] · [[np.pad]]
