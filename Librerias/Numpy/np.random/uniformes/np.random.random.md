---
title: np.random.random — Uniforme [0,1) con shape como tupla (size)
aliases:
  - random
  - random.random
  - np.random.random
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.random — Uniforme [0,1) con shape como tupla (size)

## Firma de la función

```python
np.random.random(size=None) -> ndarray
# size = entero o TUPLA con el shape completo (no dimensiones sueltas)
```

Genera valores con distribución **uniforme continua en `[0, 1)`** (0 incluido, 1 excluido), exactamente igual que [[np.random.rand]]. Lo que cambia es la **firma**: `random` recibe **un único parámetro `size`** que es el shape (una tupla), no dimensiones posicionales separadas.

## Valor de retorno

| Entrada | Retorno | Ejemplo |
|---------|---------|---------|
| `random()` | `float` escalar | `0.638...` |
| `random(3)` | ndarray `(3,)` | `[0.11, 0.92, 0.50]` |
| `random((2, 3))` | ndarray `(2, 3)` | matriz 2×3 |
| `random(size=(2, 3, 4))` | ndarray `(2, 3, 4)` | tensor 3D |

```python
import numpy as np
np.random.random((2, 3))
# array([[0.512, 0.044, 0.909],
#        [0.181, 0.336, 0.500]])
```

## Parámetros en detalle

### `size` — el shape como TUPLA

Único argumento. Es el [[concepto_shape|shape]] del resultado expresado como entero (1D) o **tupla** (nD). Por defecto `None` devuelve un escalar.

```python
np.random.random()          # escalar float
np.random.random(5)         # (5,)     vector
np.random.random((3, 4))    # (3, 4)   matriz — TUPLA obligatoria
np.random.random((2, 3, 4)) # (2, 3, 4) tensor
np.random.random(size=(3,)) # forma explícita por keyword
```

⚠️ **Contraste de firma (confusión nº1):** `random` toma **una tupla**; `rand` toma **dimensiones sueltas**.

| Llamada | Función | Resultado |
|---------|---------|-----------|
| `np.random.random((2, 3))` | random (tupla) | ✅ matriz `(2, 3)` |
| `np.random.random(2, 3)` | random con args sueltos | ❌ `TypeError` |
| `np.random.rand(2, 3)` | rand (args sueltos) | ✅ matriz `(2, 3)` |
| `np.random.rand((2, 3))` | rand con tupla | ❌ `TypeError` |

**Aliases exactos:** `np.random.random_sample`, `np.random.ranf` y `np.random.sample` son la **misma función** que ésta (misma firma `size=None`). Ésta es la forma canónica.

## Casos de uso

### Generar a partir de un shape guardado en variable

```python
shape = (3, 4)
M = np.random.random(shape)   # cómodo: el shape ya es una tupla
```

### Muestreo en [0,1)

```python
u = np.random.random(10000)
u.mean()    # ≈ 0.5
```

### Escalar a [a, b) manualmente

```python
a, b = -1, 1
x = a + (b - a) * np.random.random((2, 2))   # uniforme en [-1, 1)
```

## Buenas prácticas

1. Usa `random` cuando el shape venga ya como **tupla/variable**; usa [[np.random.rand]] cuando escribas las dimensiones sueltas.
2. Prefiere `random` (canónica) frente a sus aliases `random_sample` / `ranf` / `sample` por claridad.
3. Para un rango arbitrario `[low, high)` usa directamente `np.random.uniform`.
4. Fija semilla (`np.random.seed`) o usa un `Generator` moderno para reproducibilidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con `random(2, 3)` | pasar dimensiones sueltas | usar tupla: `random((2, 3))` |
| Confundirla con `rand` | firmas opuestas | `rand`=sueltos, `random`=tupla |
| Esperabas `[low, high)` | solo da `[0, 1)` | usar `np.random.uniform` |
| Resultados no reproducibles | sin semilla | `np.random.seed(0)` antes |

## Notas relacionadas

- [[np.random.rand]]
- [[np.random.uniform]]
- [[np.random.random_sample]]
- [[concepto_shape]]
