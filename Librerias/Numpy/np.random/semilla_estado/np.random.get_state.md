---
title: np.random.get_state — Devuelve el estado interno del RNG global
aliases:
  - get_state
  - random.get_state
  - np.random.get_state
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: tuple
inplace: false
draft: false
---

# np.random.get_state — Captura el estado del RNG global

## Firma de la función

```python
np.random.get_state(
    legacy=True
) -> tuple
```

## Valor de retorno

Devuelve una **tupla** que describe el estado interno completo del generador legacy global (`RandomState`, basado en Mersenne Twister). Permite **guardar** un punto exacto de la secuencia y luego **restaurarlo** con [[np.random.set_state]], reanudando los mismos números.

| Elemento de la tupla | Tipo | Significado |
|----------------------|------|-------------|
| `'MT19937'` | `str` | Nombre del algoritmo (Mersenne Twister) |
| `keys` | `ndarray` (uint32, 624) | Vector de estado interno |
| `pos` | `int` | Posición actual dentro del vector |
| `has_gauss` | `int` | Si hay un gaussiano en caché |
| `cached_gaussian` | `float` | Valor gaussiano cacheado |

```python
import numpy as np
np.random.seed(0)
estado = np.random.get_state()
type(estado)        # <class 'tuple'>
estado[0]           # 'MT19937'
estado[1].shape     # (624,)
```

> [!note] API moderna
> Esta función opera sobre el **RNG global legacy**. En la API **moderna** con `rng = np.random.default_rng()`, el estado se gestiona por objeto mediante `rng.bit_generator.state` (un `dict`), sin tocar estado global.

## Parámetros en detalle

### `legacy` — formato del estado

`True` (por defecto) devuelve la tupla clásica compatible con [[np.random.set_state]]. `False` devuelve un `dict` del bit generator subyacente.

```python
np.random.get_state()              # tupla legacy (por defecto)
np.random.get_state(legacy=False)  # dict del BitGenerator
```

## Casos de uso

### Guardar y restaurar para repetir una secuencia

```python
estado = np.random.get_state()
a = np.random.rand(3)
np.random.set_state(estado)        # rebobinar
b = np.random.rand(3)
np.allclose(a, b)                  # True → misma secuencia
```

### Checkpoint de reproducibilidad a mitad de proceso

```python
np.random.seed(0)
_ = np.random.rand(100)            # consumir 100 números
checkpoint = np.random.get_state() # capturar el punto exacto
```

## Buenas prácticas

1. Empareja siempre con [[np.random.set_state]]: el estado solo es útil para restaurarlo.
2. No edites los componentes de la tupla a mano; trátala como opaca.
3. Para código nuevo, usa [[np.random.default_rng]] y `rng.bit_generator.state`.
4. El estado solo es válido en la **misma versión** de NumPy.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Estado no restaura la secuencia | Se generó algo entre `get` y `set` en otro punto | Capturar y restaurar de forma contigua |
| Incompatibilidad al restaurar | Mezcla `legacy=False` con `set_state` clásico | Mantener `legacy=True` en ambos |
| Serialización inválida | Guardar la tupla sin preservar el `ndarray` | Usar `pickle`/`np.save` sobre el componente array |

## Notas relacionadas

- [[np.random.set_state]]
- [[np.random.seed]]
- [[np.random.default_rng]]
- [[concepto_aleatoriedad_rng]]
