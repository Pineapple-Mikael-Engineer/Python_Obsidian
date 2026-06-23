---
title: np.full_like — crea un array con un valor constante y la misma shape y dtype que otro
aliases:
  - full_like
  - np.full_like
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

# np.full_like — crea un array con un valor constante y la misma shape y dtype que otro

`np.full_like(a, fill_value)` crea un [[concepto_ndarray|ndarray]] **relleno con un valor constante** que **hereda la forma y el dtype** de un array de referencia `a`. Es la versión "igual que este" de [[np.full]], y la más general de la familia `_like`: con `fill_value=0` equivale a [[np.zeros_like]] y con `fill_value=1` a [[np.ones_like]]. Sirve para crear un array de centinelas (`-1`, `np.inf`, `np.nan`) o de un valor por defecto **con exactamente la misma forma y tipo** que un array dado.

## La idea

`np.full_like` **lee** la forma y el dtype de `a` y fabrica un array con cada celda puesta a `fill_value`. Equivale a `np.full(a.shape, fill_value, dtype=a.dtype)`, más conciso y robusto.

$$ (a,\ \text{fill\_value}) \;\xrightarrow{\ \text{full\_like}\ }\; \text{array con shape } a.\text{shape},\ \text{dtype } a.\text{dtype},\ \text{donde } z_{i_0\dots i_{k-1}} = \text{fill\_value} $$

La forma de salida **es** `a.shape` y el dtype **es** `a.dtype`, salvo que los sobrescribas. Ojo: el `fill_value` se **castea al dtype de `a`**, así que un float en una referencia entera se trunca (ver más abajo).

## Firma

```python
np.full_like(
    a,                 # array_like: el array de referencia (se copian su shape y dtype)
    fill_value,        # escalar (o broadcasteable): el valor constante de relleno
    dtype=None,        # dtype: sobrescribe el dtype heredado de a
    order='K',         # {'K', 'C', 'F', 'A'}: disposición en memoria (K = como a)
    subok=True,        # bool: conservar la subclase de a (matrix, masked array...)
    shape=None,        # int | tuple[int]: sobrescribe la shape heredada de a
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de referencia
Obligatorio. De él se toman **`shape` y `dtype`** por defecto. Sus valores no se usan, solo sus metadatos. Ver [[concepto_shape]] y [[concepto_dtype]].

```python
ref = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3), dtype int64
np.full_like(ref, 7)
# array([[7, 7, 7],
#        [7, 7, 7]])   → mismos (2, 3) e int64
```

### `fill_value` — el valor constante
El valor que va en todas las celdas. Se **castea al dtype de la salida** (el de `a` salvo que pases `dtype`). Aquí está la trampa: rellenar con un float en una referencia **entera** trunca.

```python
ref_int = np.zeros(3, dtype=int)
np.full_like(ref_int, 2.9)   # [2, 2, 2]  → 2.9 se trunca al int64 de la referencia
np.full_like(ref_int, 2.9, dtype=float)   # [2.9, 2.9, 2.9]  → con dtype explícito, no
```

### `dtype` — sobrescribir el tipo heredado
Ignora `a.dtype` y usa el indicado; también determina el casteo del `fill_value`. Útil cuando el valor (p. ej. `np.nan`) no cabe en el dtype de `a`.

```python
np.full_like(ref, np.nan, dtype=float)   # (2, 3) de nan en float, pese a que ref es int
```

### `order` — disposición en memoria
`'K'` (por defecto) imita la de `a`; `'C'`/`'F'` fuerzan filas/columnas contiguas; `'A'` elige `'F'` si `a` es Fortran-contiguo y `'C'` si no.

### `subok` — conservar la subclase
Con `True` (defecto) mantiene la subclase de `a`; con `False` devuelve un `ndarray` base.

### `shape` — sobrescribir la forma heredada
Usa la forma indicada conservando el dtype de `a` (salvo que pases `dtype`).

```python
np.full_like(ref, 9, shape=(4,))   # [9, 9, 9, 9] en int64
```

## El caso N-D

Crear un tensor de centinelas con la forma exacta de otro, sin reescribirla a mano.

```python
# Referencia 4D: un lote de imágenes (lote, canal, alto, ancho)
entrada = np.random.rand(2, 3, 4, 5).astype(np.float32)   # 4D
centinela = np.full_like(entrada, -1.0)   # hereda (2, 3, 4, 5) y float32, todo -1
centinela.shape   # (2, 3, 4, 5)
centinela.ndim    # 4
centinela.dtype   # float32  → NO el float64 por defecto

# Referencia 5D: un lote de vídeo (lote, frames, canal, alto, ancho)
video = np.zeros((8, 16, 3, 64, 64), dtype=np.float32)   # 5D
maximos = np.full_like(video, np.inf)   # mismo (8, 16, 3, 64, 64) y float32, todo inf
maximos.shape   # (8, 16, 3, 64, 64)
maximos.ndim    # 5
maximos[0, 0, 0, 0, 0]   # inf  → centinela "máximo aún no hallado"
```

El `(2, 3, 4, 5)` hereda el `float32` de la referencia y se rellena con el centinela elegido. Para `np.inf`/`np.nan` conviene que `a` sea de tipo float (o pasar `dtype=float`), porque esos valores no existen en enteros.

## Casos de uso

### Centinela con la forma de un array dado
```python
distancias = np.full_like(grafo_pesos, np.inf)   # ∞ inicial, misma forma/tipo
sin_asignar = np.full_like(indices, -1)          # -1 = "sin asignar"
```

### Reemplazar todo un array por un valor por defecto
```python
reset = np.full_like(buffer, 0.5)   # misma forma/tipo, todo 0.5
```

### Marcar "dato ausente" con NaN respetando la forma
```python
hueco = np.full_like(serie, np.nan, dtype=float)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El `fill_value` float se truncó | se casteó al dtype **entero** de `a` | pasar `dtype=float` |
| `nan`/`inf` "se rompen" | `a` es de tipo entero | `dtype=float` |
| Esperabas el dtype de `fill_value` | `full_like` usa el dtype de `a`, no el del valor | pasar `dtype=...` explícito |
| Querías copiar los valores de `a` | `full_like` solo copia shape/dtype | usar `a.copy()` |

## Notas relacionadas

- [[np.full]] — la versión con `shape` explícita
- [[concepto_shape]] · [[concepto_dtype]] — lo que se hereda de `a` (y al que se castea `fill_value`)
- [[np.zeros_like]] · [[np.ones_like]] · [[np.empty_like]] — la familia `_like` (casos particulares)
