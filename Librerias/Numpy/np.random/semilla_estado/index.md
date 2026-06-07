---
title: semilla_estado — control de reproducibilidad
tags:
  - numpy
  - indice
draft: false
---

# semilla_estado — control de reproducibilidad

Funciones para controlar el estado del generador global de `np.random`. Permiten fijar resultados para reproducibilidad o pausar/reanudar una secuencia aleatoria.

## Funciones

| Funcion | Descripcion |
|---------|-------------|
| [[np.random.seed]] | Fija la semilla del generador global |
| [[np.random.get_state]] | Captura el estado actual del generador |
| [[np.random.set_state]] | Restaura un estado previo |

## Patron de uso

- `seed` para reproducibilidad simple: un numero fijo al inicio del script.
- `get_state` / `set_state` para pausar y reanudar una secuencia sin volver al principio.

```python
import numpy as np

# Reproducibilidad simple
np.random.seed(42)
a = np.random.rand(5)   # siempre el mismo resultado

# Pausar y reanudar
np.random.seed(0)
x = np.random.rand(3)
estado = np.random.get_state()   # guardar posicion
y = np.random.rand(3)
np.random.set_state(estado)      # volver a esa posicion
z = np.random.rand(3)
# y == z (misma secuencia)
```

## Alternativa moderna

```python
rng = np.random.default_rng(seed=42)   # no afecta al estado global
```

`default_rng` es preferible en codigo nuevo porque encapsula el estado en el objeto `rng` sin tocar el generador global.
