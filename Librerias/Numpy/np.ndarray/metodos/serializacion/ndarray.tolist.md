---
title: ndarray.tolist — convierte el array a una lista anidada de Python nativo
aliases:
  - tolist
  - ndarray.tolist
tags:
  - numpy
  - api/metodo
  - serializacion
lib: numpy
mod: np.ndarray
obj: ndarray
tipo: metodo
retorna: list | escalar
inplace: false
requiere:
  - concepto_dtype
draft: false
---

# ndarray.tolist — convierte el array a una lista anidada de Python nativo

`ndarray.tolist` convierte el tensor a una estructura de **listas de Python anidadas** cuyas hojas son
**escalares nativos** (`int`, `float`, `bool`, `complex`), no `np.int64` ni `np.float64`. Es el puente
hacia el mundo no-NumPy: JSON, plantillas, APIs y librerías que no entienden tipos de NumPy. El precio
es que se **pierde el** [[concepto_dtype|dtype]] y la compacidad del buffer.

## La idea

NumPy → Python puro. La salida **refleja el `shape`**: cada eje se convierte en un nivel de anidamiento
de listas. Un `(2, 3)` da una lista de 2 listas de 3 elementos; un `(2, 2, 2)` da listas de listas de
listas. El caso límite: un array **0-D** (`ndim == 0`) no devuelve lista sino el escalar suelto.

$$ (n_0, n_1, \dots, n_k)\ \xrightarrow{\ \text{tolist}\ }\ \underbrace{[\,[\,\dots[\,x\,]\dots]\,]}_{k+1\ \text{niveles de lista}} $$

Lo esencial: no es `list(arr)` (que daría una lista de **sub-arrays** de NumPy en el primer eje), sino
una conversión **recursiva y completa** hasta los escalares de Python.

## Firma

```python
ndarray.tolist() -> list | int | float | bool | complex
```

No recibe parámetros.

## Los parámetros en detalle

`tolist()` no acepta ningún argumento. El único factor que cambia la salida es el `ndim` del array, que
determina la **profundidad del anidamiento**:

```python
import numpy as np

np.array(5).tolist()              # 5            → 0-D: escalar suelto, NO [5]
np.array([1, 2, 3]).tolist()      # [1, 2, 3]    → 1-D: una lista
np.array([[1, 2], [3, 4]]).tolist()  # [[1, 2], [3, 4]]  → 2-D: lista de listas
```

## Valor de retorno

La salida es una estructura de Python **puro**; el tipo de cada hoja es el escalar nativo equivalente al
`dtype`, y la profundidad es `ndim`:

| Entrada (`shape`, `dtype`) | Salida | Tipo de las hojas |
|---|---|---|
| `()`, `int64` | escalar | `int` |
| `(3,)`, `float64` | `[f, f, f]` | `float` |
| `(2, 2)`, `bool` | `[[b, b], [b, b]]` | `bool` |
| `(2, 3)`, `complex128` | lista de listas | `complex` |
| `(2, 2, 2)`, `int32` | listas triple-anidadas | `int` |

```python
arr = np.array([[1, 2], [3, 4]], dtype=np.int32)
arr.tolist()                  # [[1, 2], [3, 4]]
type(arr.tolist()[0][0])      # <class 'int'>   → int de Python, NO np.int32
```

El `dtype` se pierde **deliberadamente**: `int8`, `int32` e `int64` colapsan todos a `int` de Python; los
flotantes a `float`. No modifica el array original (solo lo exporta).

## Round-trip

La función inversa es el constructor `np.array`. Como la lista no lleva metadatos de tipo, NumPy
**reinfiere** el `dtype` (que puede no coincidir con el original), salvo que lo fijes a mano:

```python
arr  = np.array([[1, 2], [3, 4]], dtype=np.int32)
lst  = arr.tolist()                       # [[1, 2], [3, 4]]
back = np.array(lst)                       # dtype reinferido → int64 (no int32)
back = np.array(lst, dtype=arr.dtype)      # recupera el dtype original
np.array_equal(arr, back)                  # True
```

> [!warning] El `dtype` no sobrevive al viaje
> `np.array(arr.tolist())` reconstruye los **valores**, no el tipo: un `float32` vuelve como `float64`.
> Para un round-trip exacto pasa `dtype=arr.dtype`, o evita `tolist` y usa [[ndarray.dump]] / `np.save`.

## Casos de uso

### Serializar a JSON (el caso estrella)
`json.dumps` no acepta tipos de NumPy; `tolist()` los traduce a tipos que sí entiende:

```python
import json
arr = np.array([1.5, 2.5, 3.5])
json.dumps(arr.tolist())          # '[1.5, 2.5, 3.5]'
# json.dumps(arr)                 → TypeError: Object of type ndarray is not JSON serializable
```

### Ejemplo N-D: un tensor `(2, 2, 2)`
La salida replica fielmente la jerarquía de ejes:

```python
t = np.arange(8).reshape(2, 2, 2)
t.tolist()
# [[[0, 1], [2, 3]],
#  [[4, 5], [6, 7]]]   → 3 niveles de lista, hojas int de Python
```

### Extraer un único escalar nativo
Para un array de 1 elemento, `tolist()` (o `.item()`) entrega el escalar de Python limpio:

```python
np.array([42]).tolist()       # [42]
np.array(42).tolist()         # 42      → directamente int, sin lista
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Se pierde el `dtype` al reconstruir | `tolist` no guarda el tipo; `np.array` reinfiere | `np.array(lst, dtype=arr.dtype)` |
| `0-D` no devuelve lista | un array escalar da el valor suelto, no `[v]` | esperar un escalar, o `np.atleast_1d` antes |
| Memoria/tiempo altos en arrays grandes | las listas de Python pesan ~28 B por `int` frente al buffer compacto | no usar `tolist` en arrays masivos; serializar binario |
| `TypeError` al hacer `json.dumps(arr)` | JSON no conoce los escalares de NumPy | aplicar `.tolist()` **antes** de serializar |
| Confundir con `list(arr)` | `list(arr)` solo itera el primer eje (deja sub-arrays NumPy) | usar `tolist()` para conversión recursiva completa |

## Notas relacionadas

- [[concepto_dtype]] — el tipo que `tolist` descarta al pasar a Python nativo
- [[ndarray.tobytes]] — la otra cara: a bytes crudos en vez de a objetos Python
- [[ndarray.dump]] — serialización que **sí** conserva dtype y shape
- [[index]] — métodos de serialización del ndarray
