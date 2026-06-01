---
title: ndarray.tobytes — Obtener los bytes crudos del buffer
aliases:
  - tobytes
  - ndarray.tobytes
tags:
  - numpy
  - api/metodo
  - io
lib: numpy
obj: ndarray
tipo: metodo
retorna: bytes
inplace: false
draft: false
---

# ndarray.tobytes — Obtener los bytes crudos del buffer

## Firma del método

```python
ndarray.tobytes(order="C") -> bytes
```

## Valor de retorno

| Retorna | Significado |
|---------|-------------|
| `bytes` | Copia inmutable de los bytes crudos del buffer. No modifica el array (solo lo exporta a memoria). |

Devuelve la representación binaria en bruto, sin metadatos de `shape` ni [[concepto_dtype|dtype]]. Reemplaza al antiguo `tostring`, **deprecado**. Para reconstruir el array usa `np.frombuffer` indicando el dtype.

```python
import numpy as np
arr = np.array([1, 2, 3], dtype=np.uint8)
b = arr.tobytes()       # b'\x01\x02\x03'
len(b)                  # 3  → 1 byte por elemento (uint8)
np.frombuffer(b, dtype=np.uint8)    # array([1, 2, 3], dtype=uint8)
```

## Parámetros en detalle

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `order` | str | `'C'` (filas, def.), `'F'` (columnas) o `'A'` (según layout). Afecta el orden de los bytes en arrays >1D. |

```python
m = np.array([[1, 2], [3, 4]], dtype=np.uint8)
m.tobytes('C')      # b'\x01\x02\x03\x04'  → por filas
m.tobytes('F')      # b'\x01\x03\x02\x04'  → por columnas
```

## Casos de uso

```python
# Enviar un array por red o guardarlo en una columna BLOB
payload = arr.tobytes()
# Reconstruir en el otro extremo (hay que conocer dtype y shape)
arr2 = np.frombuffer(payload, dtype=np.uint8).reshape(arr.shape)
```

## Buenas prácticas

1. Transmite siempre `dtype`, `shape` y `order` junto a los bytes.
2. Para persistir en disco con metadatos, prefiere [[np.save]].
3. `np.frombuffer` da un array de **solo lectura**; copia si necesitas mutarlo.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `AttributeError: tostring` | método deprecado/eliminado | usar `tobytes` |
| Lectura desordenada en 2D | `order` distinto al de escritura | usar el mismo `order` al leer |
| Array de solo lectura | `np.frombuffer` no copia | `.copy()` si hace falta escribir |

## Notas relacionadas

- [[concepto_dtype]]
- [[ndarray.tofile]]
