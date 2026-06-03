---
title: np.random.seed — Fija la semilla del RNG global para reproducibilidad
aliases:
  - seed
  - random.seed
  - np.random.seed
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: None
inplace: false
draft: false
---

# np.random.seed — Fija la semilla del RNG global

## Firma de la función

```python
np.random.seed(
    seed=None
) -> None
```

## Valor de retorno

No devuelve nada (`None`). Su efecto es **global y lateral**: reinicializa el estado interno del generador legacy compartido (`RandomState`) que respalda a todas las funciones de `np.random.*`. Tras fijar la semilla, la secuencia de números pseudoaleatorios producida es **determinista y reproducible**.

| Llamada | Retorno | Efecto |
|---------|---------|--------|
| `np.random.seed(0)` | `None` | Fija la semilla global a `0` |
| `np.random.seed(42)` | `None` | Fija la semilla global a `42` |
| `np.random.seed(None)` | `None` | Re-siembra desde una fuente del SO (no reproducible) |

```python
import numpy as np
np.random.seed(0)
np.random.rand(3)
# array([0.5488135 , 0.71518937, 0.60276338])

np.random.seed(0)        # misma semilla → misma secuencia
np.random.rand(3)
# array([0.5488135 , 0.71518937, 0.60276338])
```

> [!warning] API moderna recomendada
> Estas funciones usan el **RNG GLOBAL legacy** (`RandomState`), un estado mutable compartido por todo el proceso. La API **moderna** recomendada por NumPy es crear un generador local explícito:
> ```python
> rng = np.random.default_rng(0)   # Generator independiente
> rng.random(3)                    # rng.normal(), rng.integers(), ...
> ```
> Evita acoplamiento global, es más rápido y reproducible por objeto.

## Parámetros en detalle

### `seed` — valor de la semilla

Entero (o secuencia de enteros / `None`) que inicializa el estado del `RandomState` global. Mismo `seed` → misma secuencia en la misma versión de NumPy.

```python
np.random.seed(0)        # int
np.random.seed(123456)   # int grande
np.random.seed(None)     # entropía del SO → NO reproducible
np.random.seed([1, 2])   # secuencia de enteros
```

Un `seed` negativo o no entero lanza error.

## Casos de uso

### Reproducibilidad de un experimento

```python
np.random.seed(42)
datos = np.random.randn(1000)   # mismos 1000 valores en cada ejecución
```

### Tests deterministas

```python
def test_muestreo():
    np.random.seed(0)
    assert np.random.randint(0, 10) == 5
```

## Buenas prácticas

1. Fija la semilla **una sola vez** al inicio del script, no dentro de bucles.
2. Para código nuevo, prefiere [[np.random.default_rng]] frente a la semilla global.
3. La reproducibilidad solo está garantizada con la **misma versión** de NumPy.
4. Para guardar/restaurar el estado exacto a mitad de una secuencia, usa [[np.random.get_state]] y [[np.random.set_state]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultados distintos pese a sembrar | Otra librería re-siembra el RNG global | Usar `default_rng` local |
| `ValueError: Seed must be non-negative` | `seed` negativo | Usar entero ≥ 0 |
| Semilla sin efecto | Se llama después de generar números | Sembrar antes de generar |
| No reproducible entre máquinas | Distinta versión de NumPy | Fijar versión del entorno |

## Notas relacionadas

- [[np.random.get_state]]
- [[np.random.set_state]]
- [[np.random.default_rng]]
- [[np.random.permutation]]
- [[concepto_aleatoriedad_rng]]
