---
title: normales — distribuciones normales / gaussianas
tags:
  - numpy
  - indice
draft: false
---

# normales — distribuciones normales / gaussianas

La distribución **normal (gaussiana)** es la más importante en estadística: aparece en errores de medida, fenómenos naturales y, sobre todo, como resultado del **teorema central del límite** —la suma de muchas variables independientes converge a una normal sin importar su distribución de origen—. Su densidad de probabilidad (PDF), centrada en la media $\mu$ y con desviación típica $\sigma$, es:

$$ f(x) = \frac{1}{\sigma\sqrt{2\pi}}\, e^{-\frac{(x-\mu)^2}{2\sigma^2}} $$

NumPy ofrece tres funciones que muestrean esta distribución con **interfaces distintas**. La elección es cuestión de qué parámetros necesitas y cómo prefieres pasar la forma de salida (ver [[concepto_shape]]).

## Las tres funciones

| Función | Distribución | Forma de salida | Cuándo usarla |
|---------|--------------|-----------------|---------------|
| [[np.random.normal]] | N(μ, σ²) | `size` (entero o tupla) | **la principal**: media `loc` y desviación `scale` arbitrarias |
| [[np.random.standard_normal]] | N(0, 1) | `size` como **tupla** | la forma canónica de pedir N(0,1) |
| [[np.random.randn]] | N(0, 1) | dimensiones **sueltas** `randn(2, 3)` | atajo legacy estilo MATLAB |

`normal(loc, scale, size)` es la general; `standard_normal` y `randn` son su caso particular $\mu=0,\ \sigma=1$ y se diferencian solo en cómo reciben la forma: **tupla** (`standard_normal((2, 3))`) frente a **dimensiones sueltas** (`randn(2, 3)`).

## Muestreo gaussiano: estándar → general

La normal estándar $N(0,1)$ es el bloque base. Cualquier $N(\mu, \sigma^2)$ se obtiene desplazando y escalando una muestra estándar $z$:

$$ x = \mu + \sigma\, z, \qquad z \sim N(0,1) $$

Por eso las tres funciones están relacionadas: `normal(loc, scale, size)` equivale a `loc + scale * standard_normal(size)`. Si ya conoces media y desviación, `normal` los hace explícitos en el código y evita la transformación manual; si solo necesitas N(0,1), `standard_normal` (o `randn`) son más directas. La media y desviación de las muestras se recuperan con [[np.mean]] y [[np.std]].

## Regla de elección

- Necesitas **media (`loc`) y desviación (`scale`) concretas** → [[np.random.normal]].
- Quieres **N(0,1)** y tu forma es una tupla (o vive en una variable) → [[np.random.standard_normal]].
- Quieres **N(0,1)** rápido con dimensiones sueltas (código legacy/MATLAB) → [[np.random.randn]].

```python
import numpy as np
np.random.seed(0)

np.random.normal(loc=5, scale=2, size=(3, 4))    # N(5, 4), forma (3, 4)
np.random.standard_normal((3, 4))                # N(0, 1), interfaz tupla
np.random.randn(3, 4)                            # N(0, 1), dimensiones sueltas

# Equivalencia estándar → general (las dos líneas dan la misma distribución):
np.random.normal(loc=50, scale=5, size=1000)
50 + 5 * np.random.standard_normal(1000)
```

> [!tip] Versión moderna (API recomendada)
> Las tres funciones de arriba usan el **estado global** del generador, que `np.random.seed` modifica de forma compartida. En código nuevo, crea un generador propio con [[np.random.default_rng]] y usa sus métodos:
> ```python
> rng = np.random.default_rng(seed=0)      # generador aislado y reproducible
> rng.normal(loc=5, scale=2, size=(3, 4))  # N(5, 4)
> rng.standard_normal((3, 4))              # N(0, 1)  (no hay rng.randn)
> ```
> Mismo muestreo gaussiano, sin estado global compartido.

## Notas relacionadas

- [[np.random.normal]] · [[np.random.standard_normal]] · [[np.random.randn]]
- [[np.random.default_rng]] — el generador moderno sin estado global
- [[concepto_shape]] — cómo `size` define la forma de salida
- [[np.mean]] · [[np.std]] — recuperar μ y σ de las muestras
