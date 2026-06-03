---
title: np.savez_compressed — Guardar varios arrays comprimidos (.npz)
aliases:
  - savez_compressed
  - np.savez_compressed
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

# np.savez_compressed — Guardar varios arrays comprimidos (.npz)

## Firma de la función

```python
np.savez_compressed(
    file,
    *args,
    **kwds
) -> None
```

## Valor de retorno

**No devuelve nada**: igual que [[np.savez]] pero **comprimiendo** los datos (zip deflate). Archivos más pequeños a cambio de más CPU al guardar/cargar. Se recupera igual con [[np.load]].

```python
import numpy as np
np.savez_compressed('datos.npz', X=X, y=y)
```

## compressed vs savez

| | [[np.savez]] | `np.savez_compressed` |
|--|--------------|------------------------|
| Tamaño | mayor | **menor** |
| CPU (guardar/cargar) | rápido | más lento |
| Ideal para | acceso frecuente | datos repetitivos / archivado |

La compresión es muy efectiva en arrays con **redundancia** (muchos ceros, valores repetidos); poco efectiva en datos aleatorios.

## Parámetros en detalle

Idénticos a [[np.savez]]: `file` y arrays por posición o `**kwds` (nombres recomendados).

## Casos de uso

### Archivar datasets dispersos o repetitivos

```python
np.savez_compressed('mascaras.npz', m1=mascara1, m2=mascara2)
```

## Buenas prácticas

1. Úsalo para almacenamiento/transferencia donde el tamaño importa.
2. Si vas a cargar muy a menudo, [[np.savez]] sin comprimir es más rápido.
3. La ganancia depende de la **redundancia** de los datos.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Carga lenta | descompresión en cada `load` | usar `savez` si prima la velocidad |
| Sin ahorro de tamaño | datos aleatorios | la compresión no ayuda |

## Limitaciones

- Más CPU al guardar y cargar; el ahorro depende de los datos.

## Notas relacionadas

- [[concepto_dtype]]
- [[np.savez]]
- [[np.save]]
- [[np.load]]
