---
title: np.random.lognormal — Muestras de la distribución log-normal
aliases:
  - lognormal
  - random.lognormal
  - np.random.lognormal
tags:
  - numpy
  - api/funcion
  - aleatorio
lib: numpy
mod: np.random
tipo: funcion
retorna: ndarray | float
inplace: false
draft: false
---

# np.random.lognormal — Muestras de la distribución log-normal

`np.random.lognormal` muestrea **magnitudes positivas que surgen de efectos multiplicativos**: una variable es log-normal cuando **su logaritmo es normal**. Aparece donde el crecimiento es proporcional (precios de activos, ingresos, tamaños de archivo, concentraciones, tiempos de respuesta). Sus parámetros `mean` y `sigma` describen la normal subyacente del **logaritmo**, no la media ni la desviación de los valores finales.

> [!tip] Versión moderna
> Esta función usa el **estado global** de `np.random` (el que fija [[np.random.seed]]), hoy considerado *legacy*. La API recomendada crea un generador propio y aislado con [[np.random.default_rng]]:
> ```python
> rng = np.random.default_rng()
> rng.lognormal(mean=0.0, sigma=1.0, size=(4, 4))   # equivalente moderno
> ```
> El método `rng.lognormal` tiene la misma firma; cambia solo de dónde sale la aleatoriedad.

## La idea

Se muestrea $Y \sim \mathcal{N}(\mu, \sigma^2)$ y se devuelve $X = e^Y$. Por eso todos los valores son **estrictamente positivos** y la distribución tiene **cola larga a la derecha**. La mediana es $e^\mu$, pero la media es **mayor**, $e^{\mu + \sigma^2/2}$, por la asimetría.

$$ f(x) = \frac{1}{x\,\sigma\sqrt{2\pi}}\,\exp\!\left(-\frac{(\ln x - \mu)^2}{2\sigma^2}\right), \quad x > 0,\ \ \mu = \texttt{mean},\ \sigma = \texttt{sigma} $$

$$ Y \sim \mathcal{N}(\mu, \sigma^2),\qquad X = e^{Y} \sim \mathrm{LogNormal}(\mu, \sigma) \quad \text{con shape } \texttt{size} $$

La clave práctica: `mean` y `sigma` viven en el **espacio del logaritmo**, no en el de los datos.

## Firma

```python
np.random.lognormal(
    mean=0.0,    # float | array_like: media μ de la normal subyacente (log)
    sigma=1.0,   # float | array_like: desviación σ > 0 de la normal subyacente (log)
    size=None,   # int | tuple[int] | None: shape de salida; None → escalar
) -> ndarray | float
```

## Los parámetros en detalle

### `mean` — media del logaritmo (escala / mediana)

Media de la normal subyacente. Como $e^{\texttt{mean}}$ es la **mediana** de la log-normal, este parámetro fija el orden de magnitud central. Puede ser cualquier real (positivo o negativo).

```python
np.random.lognormal(mean=0.0)   # mediana ≈ exp(0) = 1
np.random.lognormal(mean=3.0)   # mediana ≈ exp(3) ≈ 20
```

### `sigma` — desviación del logaritmo (forma / dispersión)

Desviación estándar de la normal subyacente, debe ser `> 0`. Controla la asimetría y el ancho: con `sigma` pequeño la log-normal es casi simétrica; con `sigma` grande la cola derecha se dispara.

```python
np.random.lognormal(0, 0.25)   # estrecha, casi simétrica
np.random.lognormal(0, 1.5)    # muy asimétrica, cola larga
```

### `size` — forma de la salida

Entero o tupla que define el [[concepto_shape|shape]] del array; `None` devuelve un único `float`.

```python
np.random.lognormal(0, 1, size=1000)    # vector (1000,)
np.random.lognormal(0, 1, size=(4, 4))  # matriz (4, 4)
```

## size y la forma de salida

La forma del array generado es exactamente `size`; cada muestra es i.i.d. y siempre positiva. Sin `size`, el retorno es un `float` escalar (no un array `0-d`).

| Llamada | `size` | retorno | shape |
|---|---|---|---|
| `np.random.lognormal()` | `None` | `float` positivo | — |
| `np.random.lognormal(0, 1, 4)` | `int` | `ndarray` | `(4,)` |
| `np.random.lognormal(0, 1, (2, 3))` | `tuple` | `ndarray` | `(2, 3)` |

```python
import numpy as np
np.random.seed(0)
np.random.lognormal(mean=0.0, sigma=1.0, size=3)
# array([5.73, 1.49, 2.65])  → mediana ≈ exp(0) = 1, media ≈ exp(0.5) ≈ 1.65
```

## Casos de uso

### Simular precios o ingresos con sesgo positivo

```python
# Ingresos con mediana ≈ exp(10) ≈ 22026 y dispersión moderada
ingresos = np.random.lognormal(mean=10, sigma=0.5, size=10000)
np.median(ingresos)   # ≈ 22026
ingresos.mean()       # mayor que la mediana por la cola derecha
```

### Calibrar a partir de datos reales

```python
datos = np.array([12.0, 18.0, 9.0, 30.0, 22.0])
log = np.log(datos)
sim = np.random.lognormal(mean=log.mean(), sigma=log.std(), size=1000)
```

### Comprobar mediana frente a media

```python
m = np.random.lognormal(mean=0, sigma=1, size=100000)
np.median(m)   # ≈ exp(0) = 1
m.mean()       # ≈ exp(0 + 1/2) ≈ 1.65  (siempre supera a la mediana)
```

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Pasar la media de los valores como `mean` | `mean` es la media del **logaritmo** | usar `np.log(datos).mean()` |
| `ValueError: sigma < 0` | desviación negativa | garantizar `sigma > 0` |
| Media muestral mayor de la esperada | la media es `exp(mean+sigma²/2)`, no `exp(mean)` | comparar con la fórmula correcta |
| Esperar valores negativos | la log-normal es siempre positiva | usar [[np.random.normal]] si necesitas negativos |

## Notas relacionadas

- [[np.random.normal]] — la normal subyacente al logaritmo
- [[np.random.gamma]] — otra distribución positiva y asimétrica
- [[np.random.exponential]] — caso multiplicativo más simple
- [[np.random.default_rng]] · [[np.random.seed]] · [[concepto_shape]]
