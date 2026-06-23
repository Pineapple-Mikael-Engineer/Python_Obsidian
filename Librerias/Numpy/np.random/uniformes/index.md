---
title: uniformes — generar números con distribución uniforme
tags:
  - numpy
  - indice
draft: false
---

# uniformes — generar números con distribución uniforme

La distribución **uniforme** es el punto de partida de toda aleatoriedad numérica: dentro de un rango, todos los valores son igualmente probables. Esta carpeta cubre las tres funciones *legacy* de `np.random` para muestrearla. Todas producen la misma distribución; lo que cambia entre ellas es **cómo se pasa la forma del array** (dimensiones sueltas frente a tupla `size`) y si el **rango** es fijo `[0, 1)` o configurable.

> [!tip] Versión moderna
> Las tres funciones de aquí operan sobre el **estado global** de `np.random` (el que fija `np.random.seed`), hoy considerado *legacy*. La API recomendada crea un generador propio y aislado con [[np.random.default_rng]]:
> ```python
> rng = np.random.default_rng()
> rng.random(size=(2, 3))        # equivalente de np.random.random
> rng.uniform(-1, 1, size=(2, 3)) # equivalente de np.random.uniform
> ```
> `Generator` unifica la interfaz: siempre `size=` como tupla, sin la variante de dimensiones sueltas.

## Las funciones

| Función | Rango | Interfaz de shape | Cuándo usarla |
|---|---|---|---|
| [[np.random.rand]] | `[0, 1)` | dimensiones **sueltas**: `rand(3, 4)` | atajo de conveniencia (estilo MATLAB) |
| [[np.random.random]] | `[0, 1)` | **tupla** `size`: `random((3, 4))` | la forma **canónica**; preferida sobre `rand` |
| [[np.random.uniform]] | `[low, high)` | **tupla** `size` + `low`/`high` | cuando el rango importa y conviene explicitarlo |

## rand vs random vs uniform

La elección es sencilla:

- **`rand`** y **`random`** dan lo mismo (`[0, 1)`); solo difieren en la firma. `rand(2, 3)` toma las dimensiones **sueltas**; `random((2, 3))` toma una **tupla**. Si el shape ya está en una variable, `random(mi_shape)` es lo cómodo.
- **`uniform`** es `random` con el rango parametrizado: `uniform(low, high, size)` cubre cualquier intervalo `[low, high)` sin reescalar a mano.

```python
import numpy as np
np.random.seed(0)

np.random.rand(3)              # shape como argumentos sueltos
np.random.random((3,))         # misma distribución, interfaz de tupla
np.random.uniform(0, 1, 3)     # idéntico, con rango explícito

# Uniforme en un rango arbitrario:
np.random.uniform(low=-5, high=5, size=(2, 3))
```

> [!note] Los alias `ranf` / `sample` / `random_sample` ya no existen
> Históricamente `np.random.random_sample`, `np.random.ranf` y `np.random.sample` eran **alias exactos** de [[np.random.random]] (misma firma `size=None`): cuatro nombres para la misma función. Se han eliminado en NumPy moderno; usa siempre `np.random.random` o el `Generator` de [[np.random.default_rng]].

## Notas relacionadas

- [[np.random.default_rng]] — la API moderna recomendada (`Generator`)
- [[np.random.seed]] — fijar la semilla del estado global *legacy*
- [[concepto_shape]] — la forma del array generado por `size`
