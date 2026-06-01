---
title: np.savez — Guardar varios arrays en un .npz
aliases:
  - savez
  - np.savez
tags:
  - numpy
  - api/funcion
  - io

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: None
inplace: false

# --- Dependencias ---
requiere:
  - concepto_dtype

draft: false
---

# np.savez — Guardar varios arrays en un .npz

## Firma de la función

```python
np.savez(
    file,
    *args,
    **kwds
) -> None
```

## Valor de retorno

**No devuelve nada**: guarda **varios arrays** en un único archivo `.npz` (un zip de `.npy` sin comprimir). Se recuperan con [[np.load]] por nombre.

```python
import numpy as np
x = np.arange(10)
y = np.ones((3, 3))
np.savez('datos.npz', x=x, matriz=y)     # nombres por kwargs

d = np.load('datos.npz')
d['x'], d['matriz']
```

## Nombrar los arrays

| Forma | Acceso |
|-------|--------|
| `np.savez(f, a, b)` (posicional) | `arr_0`, `arr_1` (auto) |
| `np.savez(f, x=a, y=b)` (kwargs) | `'x'`, `'y'` (recomendado) |

## Parámetros en detalle

### `file` — destino

Ruta (añade `.npz`).

### `*args`, `**kwds` — arrays

Posicionales → nombres automáticos; por palabra clave → nombre explícito (preferible).

## Casos de uso

### Guardar un dataset completo

```python
np.savez('dataset.npz', X_train=X_train, y_train=y_train, X_test=X_test)
```

## Buenas prácticas

1. Usa **kwargs** para nombrar los arrays de forma legible.
2. Para ahorrar espacio (a costa de CPU), usa [[np.savez_compressed]].
3. Para un solo array, [[np.save]] es suficiente.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Nombres `arr_0`, `arr_1` confusos | se pasaron posicionales | usar kwargs nombrados |
| Archivo no cierra | `np.load` sin `with` | usar `with np.load(...)` |

## Limitaciones

- Sin compresión (archivos grandes): ver [[np.savez_compressed]].

## Notas relacionadas

- [[concepto_dtype]]
- [[np.savez_compressed]]
- [[np.save]]
- [[np.load]]
