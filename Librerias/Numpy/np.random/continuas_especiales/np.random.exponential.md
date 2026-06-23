---
title: np.random.exponential — Muestras de la distribución exponencial
aliases: [exponential, random.exponential, np.random.exponential]
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray o float
inplace: false
draft: false
---

# np.random.exponential — Muestras de la distribución exponencial

Genera muestras de una distribución **exponencial**, que modela el **tiempo entre eventos** de un proceso de Poisson (llegadas de clientes, fallos de un componente, desintegraciones). Su rasgo característico es que **no tiene memoria**: la probabilidad de esperar otro intervalo no depende de cuánto hayas esperado ya. Se parametriza por la **escala** `scale = 1/λ`, donde `λ` es la tasa media de eventos por unidad de tiempo.

## La idea

La densidad de la exponencial sobre `x ≥ 0`, escrita con la tasa `λ`, es:

$$ f(x;\lambda) \;=\; \lambda\,e^{-\lambda x}, \qquad x \ge 0 $$

NumPy no recibe `λ` sino su inversa, la **escala** $\theta = $ `scale` $= 1/\lambda$, de modo que la misma densidad se lee:

$$ f(x;\theta) \;=\; \frac{1}{\theta}\,e^{-x/\theta}, \qquad x \ge 0 $$

Aquí el único **parámetro de forma/escala** es `scale`. Propiedades clave:

- Media $\mathbb{E}[X] = \theta = $ `scale` y varianza $\operatorname{Var}[X] = \theta^2$.
- Es muy **asimétrica**: cola larga a la derecha, masa concentrada cerca de 0.
- Es el caso particular de la gamma con `shape=1`.

> [!tip] Versión moderna
> La API recomendada desde NumPy 1.17 usa un generador explícito en vez del estado global. Ver [[np.random.default_rng]].
> ```python
> rng = np.random.default_rng()
> rng.exponential(scale=2.0, size=1000)
> ```

## Firma

```python
np.random.exponential(scale=1.0, size=None) -> ndarray | float
```

## Los parámetros en detalle

### `scale` — escala (inversa de la tasa)

Es `1/λ`. A mayor `scale`, eventos más espaciados (tasa baja); a menor `scale`, eventos frecuentes. Por defecto `1.0`. Debe ser `> 0`. Acepta escalar o array (se combina por [[concepto_broadcasting|broadcasting]] con `size`).

```python
np.random.exponential(scale=0.5)   # tasa λ=2 eventos/unidad → esperas cortas
np.random.exponential(scale=5.0)   # tasa λ=0.2 → esperas largas
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del resultado. Con `None` devuelve un único `float`.

```python
np.random.exponential(1.0)             # escalar
np.random.exponential(1.0, size=1000)  # vector (1000,)
np.random.exponential(1.0, (3, 4))     # matriz (3, 4)
```

## size y la forma de salida

Devuelve reales no negativos con media tendente a `scale` y varianza a `scale²`.

| Llamada | Distribución | Shape | dtype |
|---------|--------------|-------|-------|
| `np.random.exponential()` | Exp(scale=1) | `()` escalar | `float` |
| `np.random.exponential(2.0, 5)` | Exp(scale=2) | `(5,)` | `float64` |
| `np.random.exponential(10)` | Exp(scale=10), media ≈ 10 | `()` escalar | `float` |
| `np.random.exponential(1.0, (2, 3))` | Exp(scale=1) | `(2, 3)` | `float64` |

```python
import numpy as np
np.random.seed(0)
np.random.exponential(scale=2.0, size=4)
# array([1.59, 2.39, 0.47, 1.78])  → media tiende a 2.0
```

## Casos de uso

### Simular tiempos entre llegadas en una cola

```python
# λ = 3 clientes/min → scale = 1/3 min entre llegadas
entre_llegadas = np.random.exponential(scale=1/3, size=10)
instantes = np.cumsum(entre_llegadas)   # tiempos absolutos de llegada
```

### Tiempos de vida en un estudio de fiabilidad

```python
# Componente con vida media de 5000 horas
vidas = np.random.exponential(scale=5000, size=1000)
vidas.mean()   # ≈ 5000
```

### Equivalencia con la gamma de forma 1

```python
# exponential(scale) ≡ gamma(shape=1, scale)
np.random.gamma(shape=1, scale=2.0, size=1000)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Media muy distinta a la esperada | Pasar `λ` en lugar de `1/λ` | Usar `scale = 1/lambda` |
| `ValueError: scale < 0` | `scale` negativo | Garantizar `scale > 0` |
| Confundir con conteo de eventos | La exponencial da tiempos, no conteos | Para conteos usa [[np.random.poisson]] |
| Esperar simetría | La exponencial es muy asimétrica | Es correcto: cola larga a la derecha |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.default_rng]]
- [[np.random.gamma]]
- [[np.random.seed]]
- [[np.random.lognormal]]
