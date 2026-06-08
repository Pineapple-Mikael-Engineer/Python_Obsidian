---
title: semilla_estado — control de reproducibilidad
tags:
  - numpy
  - indice
draft: false
---

# semilla_estado — control de reproducibilidad

La semilla inicializa el generador pseudoaleatorio a un estado conocido, garantizando reproducibilidad: con la misma semilla, la misma secuencia de llamadas produce exactamente los mismos numeros en cualquier maquina. Sin semilla fija, cada ejecucion produce resultados diferentes. El estado del generador es la "memoria" interna que determina que numero viene despues; las tres funciones de esta carpeta permiten leer y escribir ese estado.

## Funciones

| Funcion | Descripcion |
|---------|-------------|
| [[np.random.seed]] | Fija la semilla del generador global |
| [[np.random.get_state]] | Captura el estado actual del generador como tupla |
| [[np.random.set_state]] | Restaura un estado previo capturado con `get_state` |

`seed` cubre el caso mas comun: reproducibilidad simple con un numero fijo al inicio del script. El convenio en ciencia es documentar la semilla usada junto a los resultados para que cualquier persona pueda replicar exactamente el analisis. Limitacion importante: el generador es global — si otra libreria llama a `np.random` en medio del calculo, el estado se perturba y la reproducibilidad se rompe.

`get_state` / `set_state` cubren un caso mas avanzado: pausar y reanudar una secuencia sin volver al principio. Util para reanudar simulaciones largas desde un punto exacto sin repetir todo el computo anterior.

## Patron de uso

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
# y == z (misma secuencia desde el mismo estado)
```

## Alternativa moderna

```python
rng = np.random.default_rng(seed=42)   # no afecta al estado global
```

`default_rng` encapsula el estado en el objeto `rng` sin tocar el generador global, eliminando el problema de interferencia entre librerias.
