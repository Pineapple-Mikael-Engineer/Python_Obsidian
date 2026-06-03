---
title: np.save — Guardar un array en binario (.npy)
aliases:
  - save
  - np.save
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

# np.save — Guardar un array en binario (.npy)

## Firma de la función

```python
np.save(
    file,
    arr,
    allow_pickle=True,
    fix_imports=True
) -> None
```

## Valor de retorno

**No devuelve nada**: guarda `arr` en formato binario **.npy**, preservando exactamente `shape` y [[concepto_dtype|dtype]]. Es la forma recomendada de persistir un array de NumPy (rápida, exacta, compacta). Se recupera con [[np.load]].

```python
import numpy as np
arr = np.arange(1000).reshape(10, 100)
np.save('datos.npy', arr)       # crea datos.npy
```

## .npy vs texto

| | `np.save` (.npy) | [[np.savetxt]] (texto) |
|--|------------------|------------------------|
| Velocidad | rápida | lenta |
| Tamaño | compacto | grande |
| Precisión | exacta | depende de `fmt` |
| Dimensiones | cualquiera | solo 1D/2D |
| Legible por humanos | ❌ | ✅ |

## Parámetros en detalle

### `file` — destino

Ruta (añade `.npy` si falta) u objeto archivo.

### `arr` — array a guardar

De cualquier dimensión y dtype.

## Casos de uso

### Cachear un cálculo costoso

```python
if not os.path.exists('cache.npy'):
    np.save('cache.npy', calcular_costoso())
datos = np.load('cache.npy')
```

## Buenas prácticas

1. Úsala (frente a texto) cuando no necesites que el humano lea el archivo.
2. Para **varios** arrays en un solo archivo, usa [[np.savez]].
3. Preserva dtype y shape exactos: ideal para checkpoints intermedios.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Doble extensión `.npy.npy` | añadirla a mano | dejar que NumPy la ponga |
| Riesgo de seguridad al cargar | `allow_pickle=True` | cargar con `allow_pickle=False` si es ajeno |

## Limitaciones

- Formato binario propio de NumPy (no interoperable como CSV).

## Notas relacionadas

- [[concepto_dtype]]
- [[np.load]]
- [[np.savez]]
- [[np.savetxt]]
