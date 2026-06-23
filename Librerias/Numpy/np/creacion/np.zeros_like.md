---
title: np.zeros_like — crea un array de ceros con la misma shape y dtype que otro
aliases:
  - zeros_like
  - np.zeros_like
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

# np.zeros_like — crea un array de ceros con la misma shape y dtype que otro

`np.zeros_like(a)` crea un [[concepto_ndarray|ndarray]] de **ceros que hereda la forma y el dtype** de un array de referencia `a`, sin que tengas que escribir su `shape` ni su `dtype` a mano. Es la versión "igual que este" de [[np.zeros]]: el patrón típico es `salida = np.zeros_like(entrada)` para crear un **buffer del mismo tamaño y tipo** que aquello con lo que vas a operar. Si `a` cambia de forma en el futuro, el código no se rompe: `zeros_like` se adapta solo.

## La idea

En vez de pedir una `shape` explícita, `np.zeros_like` **lee** la forma y el dtype de `a` y fabrica un array de ceros con ellos. Equivale a `np.zeros(a.shape, dtype=a.dtype)`, pero más conciso y robusto.

$$ a \text{ con shape } (n_0,\dots,n_{k-1}) \text{ y dtype } \tau \;\xrightarrow{\ \text{zeros\_like}\ }\; \text{array de ceros con shape } (n_0,\dots,n_{k-1}) \text{ y dtype } \tau $$

La forma de salida **es** `a.shape` y el dtype **es** `a.dtype`, salvo que los sobrescribas con los parámetros `shape=` / `dtype=`.

## Firma

```python
np.zeros_like(
    a,                 # array_like: el array de referencia (se copian su shape y dtype)
    dtype=None,        # dtype: sobrescribe el dtype heredado de a
    order='K',         # {'K', 'C', 'F', 'A'}: disposición en memoria (K = como a)
    subok=True,        # bool: conservar la subclase de a (p. ej. matrix, masked array)
    shape=None,        # int | tuple[int]: sobrescribe la shape heredada de a
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de referencia
Obligatorio. De él se toman **`shape` y `dtype`** por defecto. No se copian sus *valores* (el resultado es todo ceros), solo sus metadatos de forma y tipo (ver [[concepto_shape]] y [[concepto_dtype]]).

```python
ref = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3), dtype int64
np.zeros_like(ref)
# array([[0, 0, 0],
#        [0, 0, 0]])   → mismos (2, 3) e int64, NO float
```

### `dtype` — sobrescribir el tipo heredado
Si lo pasas, ignora `a.dtype` y usa el que indiques. Útil para crear un buffer de **otra precisión** pero con la misma forma.

```python
np.zeros_like(ref, dtype=np.float32)   # (2, 3) de ceros en float32
```

### `order` — disposición en memoria
`'K'` (por defecto) imita la disposición de `a` lo más posible; `'C'`/`'F'` la fuerzan a filas/columnas contiguas; `'A'` usa `'F'` si `a` es Fortran-contiguo y `'C'` en caso contrario.

### `subok` — conservar la subclase
Si `True` (defecto), el resultado mantiene la **subclase** de `a` (por ejemplo `np.matrix` o un masked array). Con `subok=False` siempre devuelve un `ndarray` base.

### `shape` — sobrescribir la forma heredada
Si lo pasas, ignora `a.shape` y usa la forma indicada, pero **conservando el dtype** de `a` (salvo que también pases `dtype`). Permite "mismo tipo que `a`, otra forma".

```python
np.zeros_like(ref, shape=(4,))   # [0, 0, 0, 0] en int64 (dtype de ref, shape nueva)
```

## El caso N-D

`zeros_like` brilla justo en N-D: copiar a mano la forma de un tensor 4D o 5D es tedioso y frágil; aquí se hereda sola.

```python
# Referencia 4D: un lote de imágenes (lote, canal, alto, ancho)
entrada = np.random.rand(2, 3, 4, 5).astype(np.float32)   # 4D
salida = np.zeros_like(entrada)   # hereda shape (2, 3, 4, 5) y dtype float32
salida.shape   # (2, 3, 4, 5)
salida.ndim    # 4
salida.dtype   # float32  → NO el float64 por defecto de np.zeros

# Referencia 5D: un lote de vídeo (lote, frames, canal, alto, ancho)
video = np.empty((8, 16, 3, 64, 64), dtype=np.uint8)   # 5D
buffer = np.zeros_like(video)   # mismo (8, 16, 3, 64, 64) y uint8
buffer.shape   # (8, 16, 3, 64, 64)
buffer.ndim    # 5
buffer.dtype   # uint8
```

Lo importante: `np.zeros((2, 3, 4, 5))` daría `float64`, pero `np.zeros_like(entrada)` respeta el `float32` de la referencia. Heredar el dtype evita promociones silenciosas y duplicar memoria.

## Casos de uso

### Buffer de salida "igual que" la entrada
```python
def normalizar(x):
    out = np.zeros_like(x)        # mismo shape y dtype que x
    out[:] = (x - x.mean()) / x.std()
    return out
```

### Acumulador del tamaño de un array dado
```python
acum = np.zeros_like(primera_matriz)   # parte de cero, misma forma/tipo
for m in matrices:
    acum += m
```

### Inicializar gradientes a cero (mismo shape que los pesos)
```python
grad = np.zeros_like(pesos)    # un cero por cada parámetro
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperabas `float64` y salió otro tipo | hereda el `dtype` de `a`, no el defecto `float` | pasar `dtype=float` explícito |
| Querías copiar los valores de `a` | `zeros_like` solo copia shape/dtype, los valores son 0 | usar `a.copy()` o [[np.array]]`(a)` |
| Forma inesperada tras reutilizar el código | `a` cambió de shape | es el comportamiento deseado; fija `shape=` si la quieres constante |

## Notas relacionadas

- [[np.zeros]] — la versión con `shape` explícita
- [[concepto_shape]] · [[concepto_dtype]] — lo que se hereda de `a`
- [[np.ones_like]] · [[np.empty_like]] · [[np.full_like]] — la familia `_like`
- [[np.full_like]] — misma idea con un valor de relleno arbitrario
