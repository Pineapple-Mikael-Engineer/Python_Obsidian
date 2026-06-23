---
title: np.ones_like — crea un array de unos con la misma shape y dtype que otro
aliases:
  - ones_like
  - np.ones_like
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

# np.ones_like — crea un array de unos con la misma shape y dtype que otro

`np.ones_like(a)` crea un [[concepto_ndarray|ndarray]] de **unos que hereda la forma y el dtype** de un array de referencia `a`. Es la versión "igual que este" de [[np.ones]]: en vez de escribir `shape` y `dtype` a mano, los copia de `a`. Sirve para crear máscaras "todo activo", factores de escala neutros o columnas de unos **con exactamente la misma forma y tipo** que un array que ya tienes.

## La idea

`np.ones_like` **lee** la forma y el dtype de `a` y fabrica un array de unos con ellos. Equivale a `np.ones(a.shape, dtype=a.dtype)`, más conciso y robusto ante cambios de forma de `a`.

$$ a \text{ con shape } (n_0,\dots,n_{k-1}) \text{ y dtype } \tau \;\xrightarrow{\ \text{ones\_like}\ }\; \text{array de unos con shape } (n_0,\dots,n_{k-1}) \text{ y dtype } \tau $$

La forma de salida **es** `a.shape` y el dtype **es** `a.dtype`, salvo que los sobrescribas con `shape=` / `dtype=`.

## Firma

```python
np.ones_like(
    a,                 # array_like: el array de referencia (se copian su shape y dtype)
    dtype=None,        # dtype: sobrescribe el dtype heredado de a
    order='K',         # {'K', 'C', 'F', 'A'}: disposición en memoria (K = como a)
    subok=True,        # bool: conservar la subclase de a (matrix, masked array...)
    shape=None,        # int | tuple[int]: sobrescribe la shape heredada de a
) -> ndarray
```

## Los parámetros en detalle

### `a` — el array de referencia
Obligatorio. De él se toman **`shape` y `dtype`** por defecto; sus *valores* no se usan (la salida es todo unos). Ver [[concepto_shape]] y [[concepto_dtype]].

```python
ref = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3), dtype int64
np.ones_like(ref)
# array([[1, 1, 1],
#        [1, 1, 1]])   → mismos (2, 3) e int64
```

### `dtype` — sobrescribir el tipo heredado
Ignora `a.dtype` y usa el indicado. Para unos de otra precisión con la misma forma.

```python
np.ones_like(ref, dtype=np.float32)   # (2, 3) de unos en float32
```

### `order` — disposición en memoria
`'K'` (por defecto) imita la de `a`; `'C'`/`'F'` fuerzan filas/columnas contiguas; `'A'` elige `'F'` si `a` es Fortran-contiguo y `'C'` si no.

### `subok` — conservar la subclase
Con `True` (defecto) el resultado mantiene la subclase de `a`; con `False` devuelve un `ndarray` base.

### `shape` — sobrescribir la forma heredada
Usa la forma indicada conservando el dtype de `a` (salvo que pases `dtype` también). Permite "mismo tipo que `a`, otra forma".

```python
np.ones_like(ref, shape=(4,))   # [1, 1, 1, 1] en int64
```

## El caso N-D

Heredar la forma de un tensor 4D o 5D evita copiarla a mano y mantiene el dtype de la referencia.

```python
# Referencia 4D: un lote de mapas de características (lote, canal, alto, ancho)
entrada = np.random.rand(2, 3, 4, 5).astype(np.float32)   # 4D
mascara = np.ones_like(entrada)   # hereda (2, 3, 4, 5) y float32
mascara.shape   # (2, 3, 4, 5)  → máscara "todo activo" del tamaño de la entrada
mascara.ndim    # 4
mascara.dtype   # float32

# Referencia 5D: un lote de vídeo (lote, frames, canal, alto, ancho)
video = np.zeros((8, 16, 3, 64, 64), dtype=np.uint8)   # 5D
pesos = np.ones_like(video)   # mismo (8, 16, 3, 64, 64) y uint8
pesos.shape   # (8, 16, 3, 64, 64)
pesos.ndim    # 5
pesos.dtype   # uint8
```

`np.ones((2, 3, 4, 5))` daría `float64`; `np.ones_like(entrada)` respeta el `float32` de la referencia. Heredar el dtype evita promociones y memoria duplicada.

## Casos de uso

### Máscara "todo activo" del tamaño de un array
```python
mascara = np.ones_like(datos, dtype=bool)   # todo True, misma forma que datos
```

### Factor de escala neutro del mismo shape
```python
escala = np.ones_like(señal)    # neutro de la multiplicación, misma forma
ajustada = señal * escala
```

### Columna/array de unos a partir de un vector dado
```python
x = np.array([1.0, 2.0, 3.0])
A = np.column_stack([np.ones_like(x), x])   # [[1, x0], [1, x1], [1, x2]]
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Esperabas `float64` y salió otro tipo | hereda el `dtype` de `a` | pasar `dtype=float` explícito |
| Querías copiar los valores de `a` | `ones_like` solo copia shape/dtype, los valores son 1 | usar `a.copy()` |
| `1` en un array entero donde querías `1.0` | el dtype heredado es entero | `dtype=float` |

## Notas relacionadas

- [[np.ones]] — la versión con `shape` explícita
- [[concepto_shape]] · [[concepto_dtype]] — lo que se hereda de `a`
- [[np.zeros_like]] · [[np.empty_like]] · [[np.full_like]] — la familia `_like`
