---
title: np.random.get_state — Captura el estado interno del RNG global legacy
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

# np.random.get_state — captura el estado del RNG global

`np.random.get_state` devuelve una **tupla** que describe el estado interno completo del generador legacy global (`RandomState`, basado en Mersenne Twister **MT19937**). Sirve para **guardar** un punto exacto de la secuencia y luego **restaurarlo** con [[np.random.set_state]], reanudando los mismos números. Es una herramienta de uso **avanzado/legacy**: en código nuevo el estado se gestiona por objeto con [[np.random.default_rng]].

> [!note] Equivalente moderno
> Esta función opera sobre el **RNG global legacy**. Con `rng = np.random.default_rng()`, el estado vive **por objeto** en `rng.bit_generator.state` (un `dict`), sin tocar nada global. Es la forma recomendada de capturar/restaurar.

## Firma de la función

```python
np.random.get_state(
    legacy=True,   # bool: True → tupla clásica; False → dict del BitGenerator
) -> tuple
```

## Valor de retorno

Devuelve la **tupla** opaca del estado del Mersenne Twister. No es un valor para leer a mano: su único uso es pasarla intacta a [[np.random.set_state]].

| Elemento de la tupla | Tipo | Significado |
|----------------------|------|-------------|
| `'MT19937'` | `str` | nombre del algoritmo (Mersenne Twister) |
| `keys` | `ndarray` (uint32, 624) | vector de estado interno |
| `pos` | `int` | posición actual dentro del vector |
| `has_gauss` | `int` | si hay un gaussiano en caché |
| `cached_gaussian` | `float` | valor gaussiano cacheado |

```python
import numpy as np
np.random.seed(0)
estado = np.random.get_state()
type(estado)        # <class 'tuple'>
estado[0]           # 'MT19937'
estado[1].shape     # (624,)
```

## Parámetros en detalle

### `legacy` — formato del estado

`True` (por defecto) devuelve la **tupla clásica** compatible con [[np.random.set_state]]. `False` devuelve un `dict` del bit generator subyacente (no intercambiable con la tupla).

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

### Equivalente moderno

```python
rng = np.random.default_rng(0)
estado = rng.bit_generator.state   # dict, no tupla; por objeto
```

## Buenas prácticas

1. Empareja **siempre** con [[np.random.set_state]]: el estado solo sirve para restaurarlo.
2. No edites los componentes de la tupla a mano; trátala como opaca.
3. En código nuevo, usa [[np.random.default_rng]] y `rng.bit_generator.state`.
4. El estado solo es válido en la **misma versión** de NumPy.

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| El estado no restaura la secuencia | se generó algo entre `get` y `set` en otro punto | capturar y restaurar de forma contigua |
| Incompatibilidad al restaurar | se mezcla `legacy=False` con `set_state` clásico | mantener `legacy=True` en ambos extremos |
| Serialización inválida | se guarda la tupla sin preservar el `ndarray` | `pickle`/`np.save` sobre el componente array |

## Notas relacionadas

- [[np.random.set_state]] — la operación inversa (restaura el estado)
- [[np.random.seed]] — fija la semilla de partida del mismo RNG global
- [[np.random.default_rng]] — `rng.bit_generator.state` en la API moderna
- [[concepto_aleatoriedad_rng]]
