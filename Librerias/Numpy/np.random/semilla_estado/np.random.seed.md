---
title: np.random.seed — Fija la semilla del RNG global legacy (reproducibilidad)
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

# np.random.seed — fija la semilla del RNG global

`np.random.seed` reinicializa el estado del **generador legacy global** (`RandomState`, basado en Mersenne Twister) que respalda a **todas** las funciones `np.random.*`. Tras sembrar, la secuencia pseudoaleatoria pasa a ser **determinista y reproducible**: misma semilla → misma secuencia.

> [!important] La forma moderna es pasar la semilla a un Generator
> `seed` actúa sobre un **estado GLOBAL** compartido por todo el proceso —frágil y propenso a interferencias—. La práctica recomendada por NumPy es **no usar `seed`** y, en su lugar, crear un generador local con [[np.random.default_rng]]:
> ```python
> rng = np.random.default_rng(0)   # Generator independiente, sin estado global
> rng.random(3); rng.normal(size=5)
> ```
> Esta nota documenta la API legacy por compatibilidad; en código nuevo, prefiere `default_rng`.

## Firma de la función

```python
np.random.seed(
    seed=None,   # None | int | array_like[int]: valor de la semilla
) -> None
```

## Valor de retorno

No devuelve nada (`None`); su efecto es **global y lateral**: sobreescribe el estado interno del `RandomState` compartido. Todo lo que se genere después (`rand`, `randn`, `permutation`, `choice`...) sale de esa secuencia determinista.

| Llamada | Retorno | Efecto |
|---------|---------|--------|
| `np.random.seed(0)` | `None` | fija la semilla global a `0` |
| `np.random.seed(42)` | `None` | fija la semilla global a `42` |
| `np.random.seed(None)` | `None` | re-siembra desde entropía del SO (no reproducible) |

```python
import numpy as np
np.random.seed(0)
np.random.rand(3)
# array([0.5488135 , 0.71518937, 0.60276338])

np.random.seed(0)        # misma semilla → misma secuencia
np.random.rand(3)
# array([0.5488135 , 0.71518937, 0.60276338])
```

## Parámetros en detalle

### `seed` — valor de la semilla

Entero `≥ 0`, secuencia de enteros, o `None`, que inicializa el estado del `RandomState` global. Mismo `seed` → misma secuencia **en la misma versión de NumPy**.

```python
np.random.seed(0)        # int
np.random.seed(123456)   # int grande
np.random.seed([1, 2])   # secuencia de enteros (semilla compuesta)
np.random.seed(None)     # entropía del SO → NO reproducible
```

Un `seed` negativo o no entero lanza error.

## Casos de uso

### Reproducibilidad de un experimento

```python
np.random.seed(42)
datos = np.random.randn(1000)        # mismos 1000 valores en cada ejecución
```

### Tests deterministas

```python
def test_muestreo():
    np.random.seed(0)
    assert np.random.randint(0, 10) == 5
```

### Equivalente moderno (preferido)

```python
rng = np.random.default_rng(42)      # local, sin tocar nada global
datos = rng.standard_normal(1000)
```

## Buenas prácticas

1. Siembra **una sola vez** al inicio del script, nunca dentro de un bucle.
2. En código nuevo, prefiere [[np.random.default_rng]] frente a la semilla global.
3. La reproducibilidad solo se garantiza con la **misma versión** de NumPy.
4. Para pausar/reanudar a mitad de secuencia, usa [[np.random.get_state]] y [[np.random.set_state]].

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Resultados distintos pese a sembrar | otra librería re-siembra el RNG global | usar `default_rng` local |
| `ValueError: Seed must be non-negative` | `seed` negativo | usar entero `≥ 0` |
| Semilla sin efecto | se llama **después** de generar números | sembrar antes de generar |
| No reproducible entre máquinas | distinta versión de NumPy | fijar la versión del entorno |

## Notas relacionadas

- [[np.random.default_rng]] — la alternativa moderna recomendada (sin estado global)
- [[np.random.get_state]] · [[np.random.set_state]] — leer/restaurar el estado legacy
- [[np.random.permutation]] — una de las funciones que esta semilla hace reproducibles
- [[concepto_aleatoriedad_rng]]
