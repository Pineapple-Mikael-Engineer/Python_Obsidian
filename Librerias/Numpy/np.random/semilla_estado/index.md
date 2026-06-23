---
title: semilla_estado — reproducibilidad y estado del generador
tags:
  - numpy
  - indice
draft: false
---

# semilla_estado — reproducibilidad y estado del generador

La **semilla** inicializa el generador pseudoaleatorio a un estado conocido: con la misma semilla, la misma secuencia de llamadas produce **exactamente** los mismos números en cualquier máquina (misma versión de NumPy). Sin semilla fija, cada ejecución es distinta. El **estado** del generador es la "memoria" interna que determina qué número viene después; las funciones de esta carpeta lo fijan, leen y restauran.

> [!important] La forma moderna es [[np.random.default_rng]]
> [[np.random.seed]], [[np.random.get_state]] y [[np.random.set_state]] operan todas sobre un **único RNG global legacy** (`RandomState`, Mersenne Twister) compartido por todo el proceso. Eso es frágil: si otra librería llama a `np.random.*` en medio de tu cálculo, el estado se desplaza y la reproducibilidad se rompe **en silencio**. La API moderna construye un **generador local** que encapsula su propio estado:
> ```python
> rng = np.random.default_rng(42)   # independiente, sin estado global
> rng.random(5); rng.normal(size=3)
> ```
> En código nuevo, usa `default_rng`. Las tres funciones de abajo se documentan por compatibilidad legacy.

## Funciones

| Función | Rol | Estado |
|---------|-----|--------|
| [[np.random.default_rng]] | **constructor del Generator moderno (recomendado)** | por objeto |
| [[np.random.seed]] | fija la semilla del generador global | global legacy |
| [[np.random.get_state]] | captura el estado actual como tupla | global legacy |
| [[np.random.set_state]] | restaura un estado previo de `get_state` | global legacy |

`seed` cubre el caso más común: reproducibilidad simple con un número fijo al inicio del script. `get_state`/`set_state` cubren un caso avanzado: **pausar y reanudar** una secuencia sin volver al principio (útil para reanudar simulaciones largas desde un punto exacto).

## Legacy ↔ moderno

La migración es casi mecánica: se crea un `rng` una vez y se cambia el prefijo `np.random.` por `rng.`.

| Legacy (estado global) | Moderno (Generator) |
|------------------------|---------------------|
| `np.random.seed(s)` | `rng = np.random.default_rng(s)` |
| `np.random.rand(...)` | `rng.random(...)` |
| `np.random.randn(...)` | `rng.standard_normal(...)` |
| `np.random.randint(a, b)` | `rng.integers(a, b)` |
| `np.random.normal(m, s)` | `rng.normal(m, s)` |
| `np.random.get_state()` | `rng.bit_generator.state` (un `dict`) |
| `np.random.set_state(t)` | `rng.bit_generator.state = d` |

## Patrón de uso (legacy)

```python
import numpy as np

# Reproducibilidad simple
np.random.seed(42)
a = np.random.rand(5)            # siempre el mismo resultado

# Pausar y reanudar
np.random.seed(0)
x = np.random.rand(3)
estado = np.random.get_state()   # guardar la posición exacta
y = np.random.rand(3)
np.random.set_state(estado)      # volver a esa posición
z = np.random.rand(3)
# y == z (misma secuencia desde el mismo estado)
```

## Patrón de uso (moderno, preferido)

```python
rng = np.random.default_rng(42)      # no toca el estado global
a = rng.random(5)

estado = rng.bit_generator.state     # checkpoint por objeto (dict)
y = rng.random(3)
rng.bit_generator.state = estado     # rebobinar
z = rng.random(3)                    # y == z
```

`default_rng` encapsula el estado en el objeto `rng`, eliminando el problema de interferencia entre librerías.
