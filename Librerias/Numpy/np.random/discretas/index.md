---
title: discretas — distribuciones de valores enteros o categorías
tags:
  - numpy
  - indice
draft: false
---

# discretas — distribuciones de valores enteros o categorías

Distribuciones y muestreo para variables aleatorias que toman **valores enteros** o de un **conjunto finito**. Son la base de las simulaciones de procesos de conteo, el muestreo aleatorio y los modelos estadísticos discretos. [[np.random.randint]] (enteros uniformes) y [[np.random.choice]] (muestreo de una población) son las de uso más frecuente; `binomial` y `poisson` aparecen sobre todo en modelado estadístico.

## Funciones

| Función | Qué hace | Distribución |
|---------|----------|--------------|
| [[np.random.randint]] | enteros uniformes en `[low, high)`; la más usada para índices y splits | uniforme discreta |
| [[np.random.choice]] | muestreo de un array o rango, con o sin reemplazo y con probabilidades | categórica / muestreo |
| [[np.random.binomial]] | número de éxitos en `n` ensayos Bernoulli con probabilidad `p` | $\binom{n}{k}p^k(1-p)^{n-k}$ |
| [[np.random.poisson]] | número de eventos en un intervalo con tasa media `lam` | $\dfrac{\lambda^k e^{-\lambda}}{k!}$ |
| `random_integers` (eliminada) | rango cerrado `[low, high]` — usar [[np.random.randint]] | uniforme discreta |

**Cómo elegir.** Para un entero uniforme o un índice aleatorio, `randint`. Para sacar elementos de una población concreta (con pesos, sin reposición, o para bootstrap), `choice`. Para un **conteo acotado** (cuántas caras en `n` lanzamientos, cuántos clientes compran en `n` visitas), `binomial`. Para un **conteo no acotado** por intervalo (llamadas por hora, fallos por día), `poisson`. Recuerda los dos puentes entre ellas: `binomial(n, p)` con `n` grande y `p` pequeño tiende a `poisson(n*p)`, y `poisson` con `lam` grande tiende a la normal.

## Ejemplos rápidos

```python
import numpy as np
np.random.seed(0)

# Enteros uniformes en [0, 10)
np.random.randint(0, 10, size=5)            # array([5, 0, 3, 3, 7])

# Binomial: caras en 10 lanzamientos (p=0.5)
np.random.binomial(n=10, p=0.5, size=5)     # array([4, 6, 5, 3, 5])

# Poisson: llamadas por minuto (tasa lam=3)
np.random.poisson(lam=3, size=5)            # array([3, 0, 3, 4, 2])

# Choice sin reemplazo
np.random.choice(['a', 'b', 'c'], size=2, replace=False)

# Choice con probabilidades no uniformes
np.random.choice([1, 2, 3], size=4, p=[0.1, 0.6, 0.3])
```

> [!tip] Versión moderna: el `Generator` de `default_rng`
> Desde NumPy 1.17, lo recomendado es crear un generador con [[np.random.default_rng]] y llamar a sus métodos —reproducibles y aislados del estado global— en vez de las funciones `np.random.*`:
> ```python
> rng = np.random.default_rng(0)
> rng.integers(0, 10, size=5)              # ↔ randint  (ojo: parámetro endpoint)
> rng.choice(['a','b','c'], size=2, replace=False)
> rng.binomial(10, 0.5, size=5)
> rng.poisson(3, size=5)
> ```
> La equivalencia es directa salvo en `integers`, que por defecto es `[low, high)` pero admite `endpoint=True` para un rango cerrado.

> [!warning] `random_integers` está deprecada y fuera de la documentación
> `np.random.random_integers` (rango **cerrado** `[low, high]`) está deprecada desde NumPy 1.11 y su entrada se **eliminó de la documentación** oficial. Usa `randint(low, high+1)` —o `rng.integers(low, high, endpoint=True)`— para un rango inclusivo, y `randint`/`rng.integers` para el semiabierto habitual.

## Notas relacionadas

- [[np.random.default_rng]] — la API moderna basada en `Generator`
- [[concepto_shape]] — `size` define la forma de salida
