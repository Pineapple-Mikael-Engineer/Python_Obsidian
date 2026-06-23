---
title: np.empty_like — crea un array SIN inicializar con la misma shape y dtype que otro
aliases:
  - empty_like
  - np.empty_like
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

# np.empty_like — crea un array SIN inicializar con la misma shape y dtype que otro

`np.empty_like(a)` reserva un [[concepto_ndarray|ndarray]] **sin inicializar** que **hereda la forma y el dtype** de un array de referencia `a`. Es la versión "igual que este" de [[np.empty]]: el buffer más rápido posible con la misma forma y tipo que `a`, pensado como **destino de una operación que lo va a sobrescribir entero** (el `out=` de una ufunc, el resultado de un bucle). Como en `np.empty`, su contenido es **basura** hasta que lo escribes.

> [!warning] La trampa heredada: NO asumas que es cero
> `np.empty_like` no inicializa nada; copia de `a` solo la **forma** y el **dtype**, no sus valores. El contenido es indefinido. Nunca lo **leas** antes de haberlo **escrito** entero.

## La idea

`np.empty_like` **lee** la forma y el dtype de `a` y reserva un buffer con ellos, sin tocar su contenido. Equivale a `np.empty(a.shape, dtype=a.dtype)`, más conciso y robusto.

$$ a \text{ con shape } (n_0,\dots,n_{k-1}) \text{ y dtype } \tau \;\xrightarrow{\ \text{empty\_like}\ }\; \text{buffer SIN inicializar con shape } (n_0,\dots,n_{k-1}) \text{ y dtype } \tau $$

La forma de salida **es** `a.shape` y el dtype **es** `a.dtype`, salvo que los sobrescribas con `shape=` / `dtype=`. La diferencia con `zeros_like`/`ones_like` es que aquí **no se paga** el coste de inicializar.

## Firma

```python
np.empty_like(
    a,                 # array_like: el array de referencia (se copian su shape y dtype)
    dtype=None,        # dtype: sobrescribe el dtype heredado de a
    order='K',         # {'K', 'C', 'F', 'A'}: disposición en memoria (K = como a)
    subok=True,        # bool: conservar la subclase de a (matrix, masked array...)
    shape=None,        # int | tuple[int]: sobrescribe la shape heredada de a
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de referencia
Obligatorio. De él se toman **`shape` y `dtype`** por defecto. Sus valores **no** se copian: el contenido queda indefinido. Ver [[concepto_shape]] y [[concepto_dtype]].

```python
ref = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3), dtype int64
np.empty_like(ref)
# array([[...basura...]])   → mismos (2, 3) e int64, valores arbitrarios
```

### `dtype` — sobrescribir el tipo heredado
Ignora `a.dtype` y usa el indicado. Para un buffer de otra precisión con la misma forma.

```python
np.empty_like(ref, dtype=np.float32)   # (2, 3) sin inicializar, en float32
```

### `order` — disposición en memoria
`'K'` (por defecto) imita la de `a`; `'C'`/`'F'` fuerzan filas/columnas contiguas; `'A'` elige `'F'` si `a` es Fortran-contiguo y `'C'` si no.

### `subok` — conservar la subclase
Con `True` (defecto) mantiene la subclase de `a`; con `False` devuelve un `ndarray` base.

### `shape` — sobrescribir la forma heredada
Usa la forma indicada conservando el dtype de `a` (salvo que pases `dtype` también).

```python
np.empty_like(ref, shape=(10,))   # 10 elementos sin inicializar, int64
```

## El caso N-D

El uso por excelencia: reservar el **buffer de salida** de una operación vectorizada sobre un tensor, sin pagar la inicialización ni reescribir la forma.

```python
# Referencia 4D: un lote de imágenes (lote, canal, alto, ancho)
entrada = np.random.rand(2, 3, 4, 5).astype(np.float32)   # 4D
salida = np.empty_like(entrada)   # hereda (2, 3, 4, 5) y float32, SIN inicializar
salida.shape   # (2, 3, 4, 5)
salida.ndim    # 4
np.multiply(entrada, 2.0, out=salida)   # se sobrescribe TODO salida de una vez

# Referencia 5D: un lote de vídeo (lote, frames, canal, alto, ancho)
video = np.zeros((8, 16, 3, 64, 64), dtype=np.uint8)   # 5D
buffer = np.empty_like(video)   # mismo (8, 16, 3, 64, 64) y uint8, sin inicializar
buffer.shape   # (8, 16, 3, 64, 64)
buffer.ndim    # 5
# ⚠️ buffer es basura hasta que se rellena entero
```

El `(2, 3, 4, 5)` se reserva con el dtype `float32` de la referencia (no el `float64` por defecto), y el patrón correcto es pasarlo como `out=` a una ufunc, que escribe los 120 elementos de golpe.

## Casos de uso

### Buffer de salida de una ufunc (sin inicializar)
```python
res = np.empty_like(a)        # mismo shape/dtype que a, sin coste de inicializar
np.multiply(a, 2, out=res)    # la ufunc rellena res por completo
```

### Destino de un bucle que rellena todo el array
```python
out = np.empty_like(serie)
for i in range(out.shape[0]):
    out[i] = transformar(serie[i])   # se escribe cada posición
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Valores "aleatorios" inesperados | se leyó antes de escribirlo entero | rellenar al 100 % antes de leer |
| Asumir que son ceros | `empty_like` **no** inicializa | usar [[np.zeros_like]] si necesitas ceros |
| Solo se rellenó parte del array | el resto sigue con basura | rellenar todo o usar [[np.zeros_like]] |
| Esperabas `float64` | hereda el `dtype` de `a` | pasar `dtype=float` |

## Notas relacionadas

- [[np.empty]] — la versión con `shape` explícita
- [[concepto_shape]] · [[concepto_dtype]] — lo que se hereda de `a`
- [[np.zeros_like]] · [[np.ones_like]] · [[np.full_like]] — la familia `_like` (las otras sí inicializan)
