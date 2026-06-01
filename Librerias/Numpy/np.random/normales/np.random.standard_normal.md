---
title: np.random.standard_normal — Normal estándar (shape como tupla)
aliases: [standard_normal, random.standard_normal, np.random.standard_normal]
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

# np.random.standard_normal — Normal estándar (shape como tupla)

## Firma de la función

```python
np.random.standard_normal(size=None) -> ndarray | float
```

Recibe el `size` como **un único argumento de shape** (entero o tupla). Misma distribución que [[np.random.randn]], distinta firma.

## Valor de retorno

Devuelve muestras de la distribución **normal estándar** (media `0`, desviación `1`). Con `size` devuelve un [[concepto_ndarray|ndarray]] `float64` de ese [[concepto_shape|shape]]; con `size=None` devuelve un escalar `float`.

| Llamada | Shape | dtype | Contenido |
|---------|-------|-------|-----------|
| `np.random.standard_normal()` | `()` (escalar) | `float` | un valor ~ N(0,1) |
| `np.random.standard_normal(3)` | `(3,)` | `float64` | vector de 3 muestras |
| `np.random.standard_normal((2, 3))` | `(2, 3)` | `float64` | matriz 2×3 |
| `np.random.standard_normal((2, 3, 4))` | `(2, 3, 4)` | `float64` | tensor |

```python
import numpy as np
np.random.seed(0)
np.random.standard_normal((2, 3))
# array([[ 1.76405235,  0.40015721,  0.97873798],
#        [ 2.2408932 ,  1.86755799, -0.97727788]])
```

## Parámetros en detalle

### `size` — shape como entero o tupla

A diferencia de [[np.random.randn]] (dimensiones como args sueltos), aquí el shape se pasa **como un solo argumento**: entero para 1D o tupla para nD. Esto la hace cómoda cuando el shape ya vive en una variable.

```python
np.random.standard_normal(5)        # (5,)    vector
np.random.standard_normal((2, 3))   # (2, 3)  matriz
np.random.standard_normal()         # escalar float

forma = (3, 4)
np.random.standard_normal(forma)    # acepta la tupla directamente
```

## Casos de uso

### Generar con un shape almacenado en variable

```python
forma = (1000, 3)
muestras = np.random.standard_normal(forma)   # sin desempaquetar
```

### Escalar a una normal arbitraria

```python
media, desv = 10, 2
x = media + desv * np.random.standard_normal((500,))   # N(10, 4)
```

Equivalente a [[np.random.normal]]`(loc=media, scale=desv, size=...)`.

## Buenas prácticas

1. Úsala cuando el shape sea una **tupla** (más legible que `randn(*forma)`).
2. Para resultados idénticos con args sueltos, usa [[np.random.randn]]: misma distribución.
3. Si necesitas media o desviación distintas de 0/1, usa [[np.random.normal]].
4. Fija `np.random.seed(...)` para reproducibilidad.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `TypeError` con `standard_normal(2, 3)` | se pasaron args sueltos en vez de una tupla | `standard_normal((2, 3))` |
| Esperaba media≠0 / desv≠1 | siempre es N(0,1) | escalar a mano o usar `np.random.normal` |
| Resultados no reproducibles | falta semilla | `np.random.seed(0)` antes |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.randn]]
- [[np.random.normal]]
- [[np.random.seed]]
