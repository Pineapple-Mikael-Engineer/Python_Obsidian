---
title: np.random.set_state — Restaura un estado previo del RNG global
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

# np.random.set_state — Restaura el estado del RNG global

## Firma de la función

```python
np.random.set_state(
    state
) -> None
```

## Valor de retorno

No devuelve nada (`None`). Su efecto es **global**: sobreescribe el estado interno del generador legacy compartido (`RandomState`) con el `state` proporcionado, normalmente obtenido antes con [[np.random.get_state]]. A partir de ahí, la secuencia pseudoaleatoria continúa **exactamente** desde ese punto.

| Llamada | Retorno | Efecto |
|---------|---------|--------|
| `np.random.set_state(estado)` | `None` | Restaura el RNG global al punto capturado |

```python
import numpy as np
np.random.seed(0)
estado = np.random.get_state()
x1 = np.random.rand(3)

np.random.set_state(estado)        # rebobinar al checkpoint
x2 = np.random.rand(3)
np.allclose(x1, x2)                # True
```

> [!note] API moderna
> Restaura el **RNG global legacy**. En la API **moderna** (`rng = np.random.default_rng()`) el equivalente es asignar `rng.bit_generator.state = estado_dict`, evitando estado global.

## Parámetros en detalle

### `state` — estado a restaurar

Debe ser la **tupla** devuelta por [[np.random.get_state]] (con `legacy=True`), con el formato `('MT19937', keys, pos, has_gauss, cached_gaussian)`. No se construye a mano.

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

## Buenas prácticas

1. Pasa **exactamente** la tupla de [[np.random.get_state]], sin modificarla.
2. Empareja captura y restauración en la misma versión de NumPy.
3. Para código nuevo, prefiere [[np.random.default_rng]] y `bit_generator.state`.
4. Útil junto a [[np.random.seed]] cuando necesitas reanudar, no reiniciar.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `ValueError: state must be ...` | `state` con formato inválido | Usar la tupla de `get_state()` |
| No reproduce la secuencia | Estado mezclado con `legacy=False` | Capturar con `legacy=True` |
| `TypeError` | Se pasa un `dict` en vez de tupla | Usar formato legacy clásico |

## Notas relacionadas

- [[np.random.get_state]]
- [[np.random.seed]]
- [[np.random.default_rng]]
- [[concepto_aleatoriedad_rng]]
