---
title: np.random.gamma — Muestras de la distribución gamma
aliases: [gamma, random.gamma, np.random.gamma]
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

# np.random.gamma — Muestras de la distribución gamma

Genera muestras de una distribución **Gamma(k, θ)**, que modela el **tiempo de espera hasta que ocurren `k` eventos** de un proceso de Poisson, es decir la suma de `k` exponenciales independientes. Generaliza a la exponencial mediante dos parámetros: la **forma** (`shape`, número de eventos / curvatura, $k$) y la **escala** (`scale`, $\theta = 1/\lambda$). Aparece en fiabilidad, tiempos agregados, modelos de lluvia y como prior bayesiano de tasas.

## La idea

La densidad de la Gamma sobre `x ≥ 0` depende de la **forma** $k = $ `shape` y la **escala** $\theta = $ `scale`:

$$ f(x;k,\theta) \;=\; \frac{x^{\,k-1}\,e^{-x/\theta}}{\Gamma(k)\,\theta^{\,k}} \;\propto\; x^{\,k-1}\,e^{-x/\theta}, \qquad x \ge 0 $$

donde $\Gamma(k)$ es la función gamma, que solo normaliza el área a 1. La intuición de los dos parámetros:

- `shape` ($k$) controla la **curvatura**: con `k<1` la masa se agolpa cerca de 0 con cola larga; con `k` grande la forma se vuelve casi simétrica (tiende a normal).
- `scale` ($\theta$) **estira el eje horizontal**: misma forma, valores mayores.

Propiedades clave:

- Media $\mathbb{E}[X] = k\theta = $ `shape·scale` y varianza $\operatorname{Var}[X] = k\theta^2 = $ `shape·scale²`.
- Con `shape=1` recupera la **exponencial** de escala `scale`.
- `gamma(shape=df/2, scale=2)` es la **chi-cuadrado** con `df` grados de libertad.

> [!tip] Versión moderna
> La API recomendada desde NumPy 1.17 usa un generador explícito en vez del estado global. Ver [[np.random.default_rng]].
> ```python
> rng = np.random.default_rng()
> rng.gamma(shape=2.0, scale=2.0, size=1000)
> ```

## Firma

```python
np.random.gamma(shape, scale=1.0, size=None) -> ndarray | float
```

## Los parámetros en detalle

### `shape` — parámetro de forma (k)

Controla la curvatura. Valores bajos (`<1`) concentran masa cerca de 0 con cola larga; `shape=1` es exponencial; valores altos hacen la distribución cada vez más simétrica (tiende a normal). Debe ser `> 0`. Acepta escalar o array (broadcasting con `scale` y `size`).

```python
np.random.gamma(0.5)   # muy asimétrica, masa cerca de 0
np.random.gamma(1.0)   # equivale a exponencial(scale)
np.random.gamma(10.0)  # casi acampanada
```

### `scale` — escala (1/λ)

Estira el eje horizontal: misma forma, valores más grandes. Es `1/λ`, igual que en la exponencial. Por defecto `1.0`. Debe ser `> 0`.

```python
np.random.gamma(2.0, scale=1.0)   # media ≈ 2
np.random.gamma(2.0, scale=5.0)   # media ≈ 10
```

### `size` — forma de la salida

Entero o tupla que fija el [[concepto_shape|shape]] del array; `None` devuelve un escalar.

```python
np.random.gamma(3.0, size=1000)     # vector (1000,)
np.random.gamma(3.0, size=(4, 5))   # matriz (4, 5)
```

## size y la forma de salida

Devuelve reales no negativos con media tendente a `shape·scale` y varianza a `shape·scale²`.

| Llamada | Distribución | Shape | dtype |
|---------|--------------|-------|-------|
| `np.random.gamma(2.0)` | Gamma(2, 1) | `()` escalar | `float` |
| `np.random.gamma(2.0, size=4)` | Gamma(2, 1) | `(4,)` | `float64` |
| `np.random.gamma(2.0, 3.0)` | Gamma(2, 3), media ≈ 6 | `()` escalar | `float` |
| `np.random.gamma(9.0, size=(2, 2))` | Gamma(9, 1), casi simétrica | `(2, 2)` | `float64` |

```python
import numpy as np
np.random.seed(0)
np.random.gamma(shape=2.0, scale=2.0, size=3)
# array([4.12, 6.78, 1.43])  → media tiende a 2*2 = 4
```

## Casos de uso

### Tiempo total hasta el k-ésimo fallo

```python
# Espera hasta el 3er fallo, tasa media 1 fallo cada 100 h (scale=100)
espera_3_fallos = np.random.gamma(shape=3, scale=100, size=1000)
espera_3_fallos.mean()   # ≈ 300
```

### Modelar montos agregados (totales de lluvia, importes de seguros)

```python
# Distribución sesgada y positiva, calibrada por momentos
montos = np.random.gamma(shape=2.5, scale=40, size=5000)
```

### Recuperar la exponencial y la chi-cuadrado

```python
np.random.gamma(shape=1, scale=2.0, size=1000)    # ≡ exponential(scale=2)
np.random.gamma(shape=4/2, scale=2, size=1000)    # ≡ chisquare(df=4)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Confundir `shape` (forma) con `size` (dimensiones) | Ambos se llaman parecido | `shape`=parámetro k, `size`=forma del array |
| `ValueError: shape < 0` | Forma o escala no positivas | Garantizar `shape > 0` y `scale > 0` |
| Media inesperada | Olvidar que media = `shape*scale` | Calibrar ambos parámetros juntos |
| Esperar valores negativos | La gamma es estrictamente positiva | Usar otra distribución si necesitas negativos |

## Notas relacionadas

- [[concepto_shape]]
- [[np.random.default_rng]]
- [[np.random.exponential]]
- [[np.random.chisquare]]
- [[np.random.seed]]
