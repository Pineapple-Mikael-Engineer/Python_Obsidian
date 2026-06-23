---
title: np.random.set_state — Restaura un estado previo del RNG global legacy
aliases:
  - set_state
  - random.set_state
  - np.random.set_state
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

# np.random.set_state — restaura el estado del RNG global

`np.random.set_state` sobreescribe el estado interno del generador legacy global (`RandomState`, Mersenne Twister) con un `state` capturado antes por [[np.random.get_state]]. A partir de ahí la secuencia pseudoaleatoria continúa **exactamente** desde ese punto. Es la operación inversa de `get_state`, y como ella, de uso **avanzado/legacy**: con [[np.random.default_rng]] el estado se restaura por objeto, sin tocar nada global.

> [!note] Equivalente moderno
> Restaura el **RNG global legacy**. Con `rng = np.random.default_rng()`, el equivalente es asignar `rng.bit_generator.state = estado_dict`, evitando el estado global.

## Firma de la función

```python
np.random.set_state(
    state,   # tuple: la tupla devuelta por get_state(legacy=True)
) -> None
```

## Valor de retorno

No devuelve nada (`None`); su efecto es **global**: reemplaza el estado del `RandomState` compartido por el de `state`. Todo lo que se genere después sale desde el punto restaurado.

| Llamada | Retorno | Efecto |
|---------|---------|--------|
| `np.random.set_state(estado)` | `None` | restaura el RNG global al punto capturado |

```python
import numpy as np
np.random.seed(0)
estado = np.random.get_state()
x1 = np.random.rand(3)

np.random.set_state(estado)        # rebobinar al checkpoint
x2 = np.random.rand(3)
np.allclose(x1, x2)                # True
```

## Parámetros en detalle

### `state` — estado a restaurar

Debe ser la **tupla** devuelta por [[np.random.get_state]] (con `legacy=True`), con el formato `('MT19937', keys, pos, has_gauss, cached_gaussian)`. No se construye a mano: trátala como un objeto opaco que solo viaja de `get_state` a `set_state`.

```python
estado = np.random.get_state()     # capturar
# ... generar números ...
np.random.set_state(estado)        # restaurar idéntico
```

## Casos de uso

### Rebobinar para repetir una secuencia

```python
estado = np.random.get_state()
muestra_a = np.random.randn(5)
np.random.set_state(estado)
muestra_b = np.random.randn(5)     # idéntica a muestra_a
```

### Restaurar desde un checkpoint persistido

```python
import pickle
with open('rng.pkl', 'rb') as f:
    estado = pickle.load(f)
np.random.set_state(estado)        # reanudar reproducibilidad
```

### Equivalente moderno

```python
rng = np.random.default_rng(0)
rng.bit_generator.state = estado_dict   # restaura por objeto, sin estado global
```

## Buenas prácticas

1. Pasa **exactamente** la tupla de [[np.random.get_state]], sin modificarla.
2. Empareja captura y restauración en la **misma versión** de NumPy.
3. En código nuevo, prefiere [[np.random.default_rng]] y `bit_generator.state`.
4. Útil junto a [[np.random.seed]] cuando necesitas **reanudar**, no reiniciar.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: state must be ...` | `state` con formato inválido | usar la tupla de `get_state()` |
| No reproduce la secuencia | estado capturado con `legacy=False` | capturar con `legacy=True` |
| `TypeError` | se pasa un `dict` en vez de tupla | usar el formato legacy clásico |

## Notas relacionadas

- [[np.random.get_state]] — la captura del estado que aquí se restaura
- [[np.random.seed]] — fija la semilla de partida del mismo RNG global
- [[np.random.default_rng]] — `rng.bit_generator.state` en la API moderna
- [[concepto_aleatoriedad_rng]]
