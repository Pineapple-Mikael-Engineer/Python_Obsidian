---
title: np.clip — Acotar valores a un rango
aliases:
  - clip
  - np.clip
  - recortar
tags:
  - numpy
  - api/funcion
  - transformaciones

# --- Clasificación ---
lib: numpy
mod: np
tipo: funcion

# --- Comportamiento ---
retorna: ndarray
inplace: false

# --- Dependencias ---
requiere:
  - concepto_broadcasting

draft: false
---

# np.clip — Acotar valores a un rango

## Firma de la función

```python
np.clip(
    a,
    a_min,
    a_max,
    out=None,
    **kwargs
) -> ndarray
```

## Valor de retorno

Devuelve un array donde cada valor se **recorta** al rango `[a_min, a_max]`: menores que `a_min` pasan a `a_min`, mayores que `a_max` pasan a `a_max`, el resto se mantiene.

| Entrada | `a_min, a_max` | Salida |
|---------|----------------|--------|
| `[-2, 0, 5, 10]` | `0, 8` | `[0, 0, 5, 8]` |
| `[1, 2, 3]` | `None, 2` | `[1, 2, 2]` |

```python
import numpy as np
np.clip([-5, 0, 5, 15], 0, 10)   # array([ 0,  0,  5, 10])
```

## Parámetros en detalle

### `a` — array de entrada

Array a recortar.

### `a_min`, `a_max` — límites

Escalares, arrays (broadcast con `a`, ver [[concepto_broadcasting]]), o `None` para no acotar ese extremo.

```python
np.clip(a, 0, None)    # solo límite inferior (equiv. ReLU)
np.clip(a, None, 1)    # solo límite superior
```

### `out` — array de salida

Permite recortar in-place pasando `out=a`.

```python
np.clip(a, 0, 1, out=a)   # modifica a directamente
```

## Casos de uso

### Mantener valores en un rango válido

```python
pixeles = np.clip(pixeles, 0, 255).astype(np.uint8)
probs = np.clip(probs, 1e-7, 1 - 1e-7)   # evitar log(0)
```

### ReLU (rectificación)

```python
np.clip(x, 0, None)   # equivale a max(0, x)
```

### Límites por elemento (broadcasting)

```python
minimos = np.array([0, 1, 2])
np.clip(datos, minimos, 10)
```

## Buenas prácticas

1. Usa `None` para acotar solo un extremo.
2. Para evitar `log(0)`/`inf`, recorta a un epsilon pequeño antes.
3. `out=a` evita una copia si vas a sobrescribir el original.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `a_min > a_max` da resultados raros | rango invertido | asegurar `a_min <= a_max` |
| dtype no cambia al recortar | `clip` conserva dtype | castear si hace falta (`.astype`) |

## Limitaciones

- No filtra ni elimina valores: los **fija** al borde (para filtrar usa máscaras).

## Notas relacionadas

- [[concepto_broadcasting]]
- [[np.where]]
- [[np.minimum]]
- [[np.maximum]]
